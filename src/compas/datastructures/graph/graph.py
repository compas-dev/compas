from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from random import sample
from random import choice
from ast import literal_eval

from compas.datastructures.datastructure import Datastructure
from compas.datastructures.attributes import NodeAttributeView
from compas.datastructures.attributes import EdgeAttributeView


class Graph(Datastructure):
    """Base graph data structure for describing the topological relationships between nodes connected by edges.

    Parameters
    ----------
    name : str, optional
        The name of the datastructure.
    default_node_attributes : dict[str, Any], optional
        Default values for node attributes.
    default_edge_attributes : dict[str, Any], optional
        Default values for edge attributes.

    Attributes
    ----------
    attributes : dict[str, Any]
        General attributes of the data structure that are included in the data representation and serialization.
    default_node_attributes : dict[str, Any]
        dictionary containing default values for the attributes of nodes.
        It is recommended to add a default to this dictionary using :meth:`update_default_node_attributes`
        for every node attribute used in the data structure.
    default_edge_attributes : dict[str, Any]
        dictionary containing default values for the attributes of edges.
        It is recommended to add a default to this dictionary using :meth:`update_default_edge_attributes`
        for every edge attribute used in the data structure.

    Examples
    --------
    >>>

    """

    def __init__(self, name=None, default_node_attributes=None, default_edge_attributes=None):
        super(Graph, self).__init__()
        self._max_node = -1
        self.attributes = {"name": name or "Graph"}
        self.node = {}
        self.edge = {}
        self.adjacency = {}
        self.default_node_attributes = {}
        self.default_edge_attributes = {}
        if default_node_attributes:
            self.default_node_attributes.update(default_node_attributes)
        if default_edge_attributes:
            self.default_edge_attributes.update(default_edge_attributes)

    # --------------------------------------------------------------------------
    # data
    # --------------------------------------------------------------------------

    @property
    def DATASCHEMA(self):
        import schema

        return schema.Schema(
            {
                "attributes": dict,
                "dna": dict,
                "dea": dict,
                "node": dict,
                "edge": dict,
                "adjacency": dict,
                "max_node": schema.And(int, lambda x: x >= -1),
            }
        )

    @property
    def JSONSCHEMANAME(self):
        return "graph"

    @property
    def data(self):
        data = {
            "attributes": self.attributes,
            "dna": self.default_node_attributes,
            "dea": self.default_edge_attributes,
            "node": {},
            "edge": {},
            "adjacency": {},
            "max_node": self._max_node,
        }
        for key in self.node:
            data["node"][repr(key)] = self.node[key]
        for u in self.edge:
            ru = repr(u)
            data["edge"][ru] = {}
            for v in self.edge[u]:
                rv = repr(v)
                data["edge"][ru][rv] = self.edge[u][v]
        for u in self.adjacency:
            ru = repr(u)
            data["adjacency"][ru] = {}
            for v in self.adjacency[u]:
                rv = repr(v)
                data["adjacency"][ru][rv] = None
        return data

    @data.setter
    def data(self, data):
        if "data" in data:
            data = data["data"]
        attributes = data.get("attributes") or {}
        default_node_attributes = data.get("dna") or {}
        default_edge_attributes = data.get("dea") or {}
        node = data.get("node") or {}
        edge = data.get("edge") or {}
        adjacency = data.get("adjacency") or {}
        if "max_int_key" in data:
            max_node = data["max_int_key"]
        else:
            max_node = data.get("max_node")
        self._max_node = max_node
        self.attributes.update(attributes)
        self.default_node_attributes.update(default_node_attributes)
        self.default_edge_attributes.update(default_edge_attributes)
        # add the nodes
        self.node = {literal_eval(key): attr for key, attr in iter(node.items())}
        # add the edges
        self.edge = {}
        for u, nbrs in iter(edge.items()):
            nbrs = nbrs or {}
            u = literal_eval(u)
            self.edge[u] = {}
            for v, attr in iter(nbrs.items()):
                attr = attr or {}
                v = literal_eval(v)
                self.edge[u][v] = attr
        # add the adjacency
        self.adjacency = {}
        for u, nbrs in iter(adjacency.items()):
            nbrs = nbrs or {}
            u = literal_eval(u)
            self.adjacency[u] = {}
            for v, _ in iter(nbrs.items()):
                v = literal_eval(v)
                self.adjacency[u][v] = None

    # --------------------------------------------------------------------------
    # properties
    # --------------------------------------------------------------------------

    @property
    def name(self):
        return self.attributes.get("name") or self.__class__.__name__

    @name.setter
    def name(self, value):
        self.attributes["name"] = value

    # --------------------------------------------------------------------------
    # customization
    # --------------------------------------------------------------------------

    def __str__(self):
        tpl = "<Graph with {} nodes, {} edges>"
        return tpl.format(self.number_of_nodes(), self.number_of_edges())

    # --------------------------------------------------------------------------
    # constructors
    # --------------------------------------------------------------------------

    @classmethod
    def from_edges(cls, edges):
        """Create a new graph instance from information about the edges.

        Parameters
        ----------
        edges : list[tuple[hashable, hashable]]
            The edges of the graph as pairs of node identifiers.

        Returns
        -------
        :class:`~compas.datastructures.Graph`

        """
        graph = cls()
        for u, v in edges:
            if u not in graph.node:
                graph.add_node(u)
            if v not in graph.node:
                graph.add_node(v)
            graph.add_edge(u, v)

    @classmethod
    def from_networkx(cls, graph):
        """Create a new graph instance from a NetworkX DiGraph instance.

        Parameters
        ----------
        graph : networkx.DiGraph
            NetworkX instance of a directed graph.

        Returns
        -------
        :class:`~compas.datastructures.Graph`

        """
        g = cls()
        g.attributes.update(graph.graph)

        for node in graph.nodes():
            g.add_node(node, **graph.nodes[node])

        for edge in graph.edges():
            g.add_edge(*edge, **graph.edges[edge])

        return g

    def to_networkx(self):
        """Create a new NetworkX graph instance from a graph.

        Returns
        -------
        networkx.DiGraph
            A newly created NetworkX DiGraph.

        """
        import networkx as nx

        graph = nx.DiGraph()
        graph.graph.update(self.attributes)

        for node, attr in self.nodes(data=True):
            graph.add_node(node, **attr)

        for edge, attr in self.edges(data=True):
            graph.add_edge(*edge, **attr)

        return graph

    # --------------------------------------------------------------------------
    # helpers
    # --------------------------------------------------------------------------

    def clear(self):
        """Clear all the network data.

        Returns
        -------
        None

        """
        del self.node
        del self.edge
        del self.adjacency
        self.node = {}
        self.edge = {}
        self.adjacency = {}

    def get_any_node(self):
        """Get the identifier of a random node.

        .. deprecated:: 1.13.3
            Use :meth:`node_sample` instead.

        Returns
        -------
        hashable
            The identifier of the node.

        """
        return self.get_any_nodes(1)[0]

    def get_any_nodes(self, n, exclude_leaves=False):
        """Get a list of identifiers of a random set of n nodes.

        .. deprecated:: 1.13.3
            Use :meth:`node_sample` instead.

        Parameters
        ----------
        n : int
            The number of random nodes.
        exclude_leaves : bool, optional
            If True, exclude the leaves (nodes with only one connected edge) from the set.

        Returns
        -------
        list[hashable]
            The identifiers of the nodes.

        """
        if exclude_leaves:
            nodes = set(self.nodes()) - set(self.leaves())
        else:
            nodes = self.nodes()
        return sample(list(nodes), n)

    def get_any_edge(self):
        """Get the identifier of a random edge.

        .. deprecated:: 1.13.3
            Use :meth:`edge_sample` instead.

        Returns
        -------
        tuple[hashable, hashable]
            The identifier of the edge in the form of a pair of vertex identifiers.

        """
        return choice(list(self.edges()))

    def get_any_edges(self, n):
        """Get the identifiers of a set of random edges.

        .. deprecated:: 1.13.3
            Use :meth:`edge_sample` instead.

        Parameters
        ----------
        n : int
            The number of edges in the set.

        Returns
        -------
        list[tuple[hashable, hashable]]
            The identifiers of the random edges.

        """
        return sample(list(self.edges()), n)

    def node_sample(self, size=1):
        """Get a list of identifiers of a random set of n nodes.

        Parameters
        ----------
        size : int, optional
            The size of the sample.

        Returns
        -------
        list[hashable]
            The identifiers of the nodes.

        """
        return sample(list(self.nodes()), size)

    def edge_sample(self, size=1):
        """Get the identifiers of a set of random edges.

        Parameters
        ----------
        size : int, optional
            The size of the sample.

        Returns
        -------
        list[tuple[hashable, hashable]]
            The identifiers of the random edges.

        """
        return sample(list(self.edges()), size)

    def key_index(self):
        """Returns a dictionary that maps node identifiers to their corresponding index in a node list or array.

        Returns
        -------
        dict[hashable, int]
            A dictionary of key-index pairs.

        """
        return {key: index for index, key in enumerate(self.nodes())}

    def index_key(self):
        """Returns a dictionary that maps the indices of a node list to keys in a node dictionary.

        Returns
        -------
        dict[int, hashable]
            A dictionary of index-key pairs.

        """
        return dict(enumerate(self.nodes()))

    def uv_index(self):
        """Returns a dictionary that maps edge keys (i.e. pairs of vertex keys)
        to the corresponding edge index in a list or array of edges.

        Returns
        -------
        dict[tuple[hashable, hashable], int]
            A dictionary of uv-index pairs.

        """
        return {(u, v): index for index, (u, v) in enumerate(self.edges())}

    def index_uv(self):
        """Returns a dictionary that maps edges in a list to the corresponding
        vertex key pairs.

        Returns
        -------
        dict[int, tuple[hashable, hashable]]
            A dictionary of index-uv pairs.

        """
        return dict(enumerate(self.edges()))

    # --------------------------------------------------------------------------
    # builders
    # --------------------------------------------------------------------------

    def add_node(self, key=None, attr_dict=None, **kwattr):
        """Add a node and specify its attributes (optional).

        Parameters
        ----------
        key : hashable, optional
            An identifier for the node.
            Defaults to None, in which case an identifier of type int is automatically generated.
        attr_dict : dict[str, Any], optional
            A dictionary of vertex attributes.
        **kwattr : dict[str, Any], optional
            A dictionary of additional attributes compiled of remaining named arguments.

        Returns
        -------
        hashable
            The identifier of the node.

        Notes
        -----
        If no key is provided for the node, one is generated
        automatically. An automatically generated key increments the highest
        integer key in use by 1.

        Examples
        --------
        >>> graph = Graph()
        >>> node = graph.add_node()
        >>> node
        0

        """
        if key is None:
            key = self._max_node = self._max_node + 1
        try:
            if key > self._max_node:
                self._max_node = key
        except (ValueError, TypeError):
            pass

        if key not in self.node:
            self.node[key] = {}
            self.edge[key] = {}
            self.adjacency[key] = {}
        attr = attr_dict or {}
        attr.update(kwattr)
        self.node[key].update(attr)
        return key

    def add_edge(self, u, v, attr_dict=None, **kwattr):
        """Add an edge and specify its attributes.

        Parameters
        ----------
        u : hashable
            The identifier of the first node of the edge.
        v : hashable
            The identifier of the second node of the edge.
        attr_dict : dict[str, Any], optional
            A dictionary of edge attributes.
        **kwattr : dict[str, Any], optional
            A dictionary of additional attributes compiled of remaining named arguments.

        Returns
        -------
        tuple[hashable, hashable]
            The identifiers of the edge nodes.

        Examples
        --------
        >>>

        """
        attr = attr_dict or {}
        attr.update(kwattr)
        if u not in self.node:
            u = self.add_node(u)
        if v not in self.node:
            v = self.add_node(v)
        data = self.edge[u].get(v, {})
        data.update(attr)
        self.edge[u][v] = data
        if v not in self.adjacency[u]:
            self.adjacency[u][v] = None
        if u not in self.adjacency[v]:
            self.adjacency[v][u] = None
        return u, v

    # --------------------------------------------------------------------------
    # modifiers
    # --------------------------------------------------------------------------

    def delete_node(self, key):
        """Delete a node from the graph.

        Parameters
        ----------
        key : hashable
            The identifier of the node.

        Returns
        -------
        None

        Examples
        --------
        >>>

        """
        if key in self.edge:
            del self.edge[key]
        if key in self.adjacency:
            del self.adjacency[key]
        if key in self.node:
            del self.node[key]
        for u in list(self.edge):
            for v in list(self.edge[u]):
                if v == key:
                    del self.edge[u][v]
        for u in self.adjacency:
            for v in list(self.adjacency[u]):
                if v == key:
                    del self.adjacency[u][v]

    def delete_edge(self, u, v):
        """Delete an edge from the network.

        Parameters
        ----------
        u : hashable
            The identifier of the first node.
        v : hashable
            The identifier of the second node.

        Returns
        -------
        None

        Examples
        --------
        >>>

        """
        del self.adjacency[u][v]
        del self.adjacency[v][u]
        if u in self.edge and v in self.edge[u]:
            del self.edge[u][v]
        if v in self.edge and u in self.edge[v]:
            del self.edge[v][u]

    # --------------------------------------------------------------------------
    # info
    # --------------------------------------------------------------------------

    def summary(self):
        """Return a summary of the graph.

        Returns
        -------
        str
            The formatted summary.

        """
        tpl = "\n".join(
            [
                "{} summary",
                "=" * (len(self.name) + len(" summary")),
                "- nodes: {}",
                "- edges: {}",
            ]
        )
        return tpl.format(self.name, self.number_of_nodes(), self.number_of_edges())

    def number_of_nodes(self):
        """Compute the number of nodes of the graph.

        Returns
        -------
        int
            The number of nodes.

        """
        return len(list(self.nodes()))

    def number_of_edges(self):
        """Compute the number of edges of the graph.

        Returns
        -------
        int
            The number of edges.

        """
        return len(list(self.edges()))

    # --------------------------------------------------------------------------
    # accessors
    # --------------------------------------------------------------------------

    def nodes(self, data=False):
        """Iterate over the nodes of the network.

        Parameters
        ----------
        data : bool, optional
            If True, yield the node attributes in addition to the node identifiers.

        Yields
        ------
        hashable | tuple[hashable, dict[str, Any]]
            If `data` is False, the next node identifier.
            If `data` is True, the next node as a (key, attr) tuple.

        """
        for key in self.node:
            if not data:
                yield key
            else:
                yield key, self.node_attributes(key)

    def nodes_where(self, conditions=None, data=False, **kwargs):
        """Get nodes for which a certain condition or set of conditions is true.

        Parameters
        ----------
        conditions : dict, optional
            A set of conditions in the form of key-value pairs.
            The keys should be attribute names. The values can be attribute
            values or ranges of attribute values in the form of min/max pairs.
        data : bool, optional
            If True, yield the node attributes in addition to the node identifiers.

        Yields
        ------
        hashable | tuple[hashable, dict[str, Any]]
            If `data` is False, the next node that matches the condition.
            If `data` is True, the next node and its attributes.

        """
        conditions = conditions or {}
        conditions.update(kwargs)

        for key, attr in self.nodes(True):
            is_match = True

            for name, value in conditions.items():
                method = getattr(self, name, None)

                if callable(method):
                    val = method(key)
                    if isinstance(val, list):
                        if value not in val:
                            is_match = False
                            break
                        break
                    if isinstance(value, (tuple, list)):
                        minval, maxval = value
                        if val < minval or val > maxval:
                            is_match = False
                            break
                    else:
                        if value != val:
                            is_match = False
                            break

                else:
                    if name not in attr:
                        is_match = False
                        break
                    if isinstance(attr[name], list):
                        if value not in attr[name]:
                            is_match = False
                            break
                        break
                    if isinstance(value, (tuple, list)):
                        minval, maxval = value
                        if attr[name] < minval or attr[name] > maxval:
                            is_match = False
                            break
                    else:
                        if value != attr[name]:
                            is_match = False
                            break

            if is_match:
                if data:
                    yield key, attr
                else:
                    yield key

    def nodes_where_predicate(self, predicate, data=False):
        """Get nodes for which a certain condition or set of conditions is true using a lambda function.

        Parameters
        ----------
        predicate : callable
            The condition you want to evaluate.
            The callable takes 2 parameters: the node identifier and the node attributes, and should return True or False.
        data : bool, optional
            If True, yield the node attributes in addition to the node identifiers.

        Yields
        ------
        hashable | tuple[hashable, dict[str, Any]]
            If `data` is False, the next node that matches the condition.
            If `data` is True, the next node and its attributes.

        Examples
        --------
        >>>

        """
        for key, attr in self.nodes(True):
            if predicate(key, attr):
                if data:
                    yield key, attr
                else:
                    yield key

    def edges(self, data=False):
        """Iterate over the edges of the network.

        Parameters
        ----------
        data : bool, optional
            If True, yield the edge attributes in addition to the edge identifiers.

        Yields
        ------
        tuple[hashable, hashable] | tuple[tuple[hashable, hashable], dict[str, Any]]
            If `data` is False, the next edge identifier (u, v).
            If `data` is True, the next edge identifier and its attributes as a ((u, v), attr) tuple.

        """
        for u, nbrs in iter(self.edge.items()):
            for v, attr in iter(nbrs.items()):
                if data:
                    yield (u, v), attr
                else:
                    yield u, v

    def edges_where(self, conditions=None, data=False, **kwargs):
        """Get edges for which a certain condition or set of conditions is true.

        Parameters
        ----------
        conditions : dict, optional
            A set of conditions in the form of key-value pairs.
            The keys should be attribute names. The values can be attribute
            values or ranges of attribute values in the form of min/max pairs.
        data : bool, optional
            If True, yield the edge attributes in addition to the edge identifiers.
        **kwargs : dict[str, Any], optional
            Additional conditions provided as named function arguments.

        Yields
        ------
        tuple[hashable, hashable] | tuple[tuple[hashable, hashable], dict[str, Any]]
            If `data` is False, the next edge identifier (u, v).
            If `data` is True, the next edge identifier and its attributes as a ((u, v), attr) tuple.

        """
        conditions = conditions or {}
        conditions.update(kwargs)

        for key in self.edges():
            is_match = True

            attr = self.edge_attributes(key)

            for name, value in conditions.items():
                method = getattr(self, name, None)

                if method and callable(method):
                    val = method(key)
                elif name in attr:
                    val = attr[name]
                else:
                    is_match = False
                    break

                if isinstance(val, list):
                    if value not in val:
                        is_match = False
                        break
                elif isinstance(value, (tuple, list)):
                    minval, maxval = value
                    if val < minval or val > maxval:
                        is_match = False
                        break
                else:
                    if value != val:
                        is_match = False
                        break

            if is_match:
                if data:
                    yield key, attr
                else:
                    yield key

    def edges_where_predicate(self, predicate, data=False):
        """Get edges for which a certain condition or set of conditions is true using a lambda function.

        Parameters
        ----------
        predicate : callable
            The condition you want to evaluate.
            The callable takes 2 parameters:
            an edge identifier (tuple of node identifiers) and edge attributes,
            and should return True or False.
        data : bool, optional
            If True, yield the edge attributes in addition to the edge attributes.

        Yields
        ------
        tuple[hashable, hashable] | tuple[tuple[hashable, hashable], dict[str, Any]]
            If `data` is False, the next edge identifier (u, v).
            If `data` is True, the next edge identifier and its attributes as a ((u, v), attr) tuple.

        Examples
        --------
        >>>

        """
        for key, attr in self.edges(True):
            if predicate(key, attr):
                if data:
                    yield key, attr
                else:
                    yield key

    # --------------------------------------------------------------------------
    # default attributes
    # --------------------------------------------------------------------------

    def update_default_node_attributes(self, attr_dict=None, **kwattr):
        """Update the default node attributes.

        Parameters
        ----------
        attr_dict : dict[str, Any], optional
            A dictionary of attributes with their default values.
        **kwattr : dict[str, Any], optional
            A dictionary of additional attributes compiled of remaining named arguments.

        Returns
        -------
        None

        """
        if not attr_dict:
            attr_dict = {}
        attr_dict.update(kwattr)
        self.default_node_attributes.update(attr_dict)

    def update_default_edge_attributes(self, attr_dict=None, **kwattr):
        """Update the default edge attributes.

        Parameters
        ----------
        attr_dict : dict[str, Any], optional
            A dictionary of attributes with their default values.
        **kwattr : dict[str, Any], optional
            A dictionary of additional attributes compiled of remaining named arguments.

        Returns
        -------
        None

        """
        if not attr_dict:
            attr_dict = {}
        attr_dict.update(kwattr)
        self.default_edge_attributes.update(attr_dict)

    update_dna = update_default_node_attributes
    update_dea = update_default_edge_attributes

    # --------------------------------------------------------------------------
    # node attributes
    # --------------------------------------------------------------------------

    def node_attribute(self, key, name, value=None):
        """Get or set an attribute of a node.

        Parameters
        ----------
        key : hashable
            The node identifier.
        name : str
            The name of the attribute
        value : obj, optional
            The value of the attribute.

        Returns
        -------
        obj or None
            The value of the attribute,
            or None when the function is used as a "setter".

        Raises
        ------
        KeyError
            If the node does not exist.

        """
        if key not in self.node:
            raise KeyError(key)
        if value is not None:
            self.node[key][name] = value
            return
        if name in self.node[key]:
            return self.node[key][name]
        else:
            if name in self.default_node_attributes:
                return self.default_node_attributes[name]

    def unset_node_attribute(self, key, name):
        """Unset the attribute of a node.

        Parameters
        ----------
        key : int
            The node identifier.
        name : str
            The name of the attribute.

        Raises
        ------
        KeyError
            If the node does not exist.

        Notes
        -----
        Unsetting the value of a node attribute implicitly sets it back to the value
        stored in the default node attribute dict.

        """
        if name in self.node[key]:
            del self.node[key][name]

    def node_attributes(self, key, names=None, values=None):
        """Get or set multiple attributes of a node.

        Parameters
        ----------
        key : hashable
            The identifier of the node.
        names : list[str], optional
            A list of attribute names.
        values : list[Any], optional
            A list of attribute values.

        Returns
        -------
        dict[str, Any] | list[Any] | None
            If the parameter `names` is empty,
            the function returns a dictionary of all attribute name-value pairs of the node.
            If the parameter `names` is not empty,
            the function returns a list of the values corresponding to the requested attribute names.
            The function returns None if it is used as a "setter".

        Raises
        ------
        KeyError
            If the node does not exist.

        """
        if key not in self.node:
            raise KeyError(key)
        if values is not None:
            # use it as a setter
            for name, value in zip(names, values):
                self.node[key][name] = value
            return
        # use it as a getter
        if not names:
            # return all node attributes as a dict
            return NodeAttributeView(self.default_node_attributes, self.node[key])
        values = []
        for name in names:
            if name in self.node[key]:
                values.append(self.node[key][name])
            elif name in self.default_node_attributes:
                values.append(self.default_node_attributes[name])
            else:
                values.append(None)
        return values

    def nodes_attribute(self, name, value=None, keys=None):
        """Get or set an attribute of multiple nodes.

        Parameters
        ----------
        name : str
            The name of the attribute.
        value : obj, optional
            The value of the attribute.
        keys : list[hashable], optional
            A list of node identifiers.

        Returns
        -------
        list[Any] | None
            The value of the attribute for each node,
            or None if the function is used as a "setter".

        Raises
        ------
        KeyError
            If any of the nodes does not exist.

        """
        if not keys:
            keys = self.nodes()
        if value is not None:
            for key in keys:
                self.node_attribute(key, name, value)
            return
        return [self.node_attribute(key, name) for key in keys]

    def nodes_attributes(self, names=None, values=None, keys=None):
        """Get or set multiple attributes of multiple nodes.

        Parameters
        ----------
        names : list[str], optional
            The names of the attribute.
        values : list[Any], optional
            The values of the attributes.
        keys : list[hashable], optional
            A list of node identifiers.

        Returns
        -------
        list[dict[str, Any]] | list[list[Any]] | None
            If the parameter `names` is None,
            the function returns a list containing an attribute dict per node.
            If the parameter `names` is not None,
            the function returns a list containing a list of attribute values per node corresponding to the provided attribute names.
            The function returns None if it is used as a "setter".

        Raises
        ------
        KeyError
            If any of the nodes does not exist.

        """
        if not keys:
            keys = self.nodes()
        if values:
            for key in keys:
                self.node_attributes(key, names, values)
            return
        return [self.node_attributes(key, names) for key in keys]

    # --------------------------------------------------------------------------
    # edge attributes
    # --------------------------------------------------------------------------

    def edge_attribute(self, key, name, value=None):
        """Get or set an attribute of an edge.

        Parameters
        ----------
        key : tuple[hashable, hashable]
            The identifier of the edge as a pair of node identifiers.
        name : str
            The name of the attribute.
        value : obj, optional
            The value of the attribute.

        Returns
        -------
        object | None
            The value of the attribute, or None when the function is used as a "setter".

        Raises
        ------
        KeyError
            If the edge does not exist.

        """
        u, v = key
        if u not in self.edge or v not in self.edge[u]:
            raise KeyError(key)
        attr = self.edge[u][v]
        if value is not None:
            attr[name] = value
            return
        if name in attr:
            return attr[name]
        if name in self.default_edge_attributes:
            return self.default_edge_attributes[name]

    def unset_edge_attribute(self, key, name):
        """Unset the attribute of an edge.

        Parameters
        ----------
        key : tuple[hashable, hashable]
            The edge identifier.
        name : str
            The name of the attribute.

        Returns
        -------
        None

        Raises
        ------
        KeyError
            If the edge does not exist.

        Notes
        -----
        Unsetting the value of an edge attribute implicitly sets it back to the value
        stored in the default edge attribute dict.

        """
        u, v = key
        if u not in self.edge or v not in self.edge[u]:
            raise KeyError(key)
        attr = self.edge[u][v]
        if name in attr:
            del attr[name]

    def edge_attributes(self, key, names=None, values=None):
        """Get or set multiple attributes of an edge.

        Parameters
        ----------
        key : tuple[hashable, hashable]
            The identifier of the edge.
        names : list[str], optional
            A list of attribute names.
        values : list[Any], optional
            A list of attribute values.

        Returns
        -------
        dict[str, Any] | list[Any] | None
            If the parameter `names` is empty, a dictionary of all attribute name-value pairs of the edge.
            If the parameter `names` is not empty, a list of the values corresponding to the provided names.
            None if the function is used as a "setter".

        Raises
        ------
        KeyError
            If the edge does not exist.

        """
        u, v = key
        if u not in self.edge or v not in self.edge[u]:
            raise KeyError(key)
        if values:
            # use it as a setter
            for name, value in zip(names, values):
                self.edge_attribute(key, name, value)
            return
        # use it as a getter
        if not names:
            # get the entire attribute dict
            return EdgeAttributeView(self.default_edge_attributes, self.edge[u][v])
        # get only the values of the named attributes
        values = []
        for name in names:
            value = self.edge_attribute(key, name)
            values.append(value)
        return values

    def edges_attribute(self, name, value=None, keys=None):
        """Get or set an attribute of multiple edges.

        Parameters
        ----------
        name : str
            The name of the attribute.
        value : obj, optional
            The value of the attribute.
        keys : list[tuple[hashable, hashable]], optional
            A list of edge identifiers.

        Returns
        -------
        list[Any] | None
            A list containing the value per edge of the requested attribute,
            or None if the function is used as a "setter".

        Raises
        ------
        KeyError
            If any of the edges does not exist.

        """
        if not keys:
            keys = self.edges()
        if value is not None:
            for key in keys:
                self.edge_attribute(key, name, value)
            return
        return [self.edge_attribute(key, name) for key in keys]

    def edges_attributes(self, names=None, values=None, keys=None):
        """Get or set multiple attributes of multiple edges.

        Parameters
        ----------
        names : list[str], optional
            The names of the attribute.
        values : list[Any], optional
            The values of the attributes.
        keys : list[tuple[hashable, hashable]], optional
            A list of edge identifiers.

        Returns
        -------
        list[dict[str, Any]] | list[list[Any]] | None
            If `names` is empty,
            a list containing per edge an attribute dict with all attributes of the edge.
            If `names` is not empty,
            a list containing per edge a list of attribute values corresponding to the requested names.
            None if the function is used as a "setter".

        Raises
        ------
        KeyError
            If any of the edges does not exist.

        """
        if not keys:
            keys = self.edges()
        if values:
            for key in keys:
                self.edge_attributes(key, names, values)
            return
        return [self.edge_attributes(key, names) for key in keys]

    # --------------------------------------------------------------------------
    # node topology
    # --------------------------------------------------------------------------

    def has_node(self, key):
        """Verify if a specific node is present in the network.

        Parameters
        ----------
        key : hashable
            The identifier of the node.

        Returns
        -------
        bool
            True or False.

        """
        return key in self.node

    def is_leaf(self, key):
        """Verify if a node is a leaf.

        Parameters
        ----------
        key : hashable
            The identifier of the node.

        Returns
        -------
        bool
            True or False.

        Notes
        -----
        A node is a *leaf* if it has only one neighbor.

        """
        return self.degree(key) == 1

    def leaves(self):
        """Return all leaves of the network.

        Returns
        -------
        list[hashable]
            A list of node identifiers.

        """
        return [key for key in self.nodes() if self.is_leaf(key)]

    def is_node_connected(self, key):
        """Verify if a specific node is connected.

        Parameters
        ----------
        key : hashable
            The identifier of the node.

        Returns
        -------
        bool
            True or False.

        """
        return self.degree(key) > 0

    def neighbors(self, key):
        """Return the neighbors of a node.

        Parameters
        ----------
        key : hashable
            The identifier of the node.

        Returns
        -------
        list[hashable]
            A list of node identifiers.

        """
        return list(self.adjacency[key])

    def neighborhood(self, key, ring=1):
        """Return the nodes in the neighborhood of a node.

        Parameters
        ----------
        key : hashable
            The identifier of the node.
        ring : int, optional
            The size of the neighborhood.

        Returns
        -------
        list[hashable]
            A list of node identifiers.

        """
        nbrs = set(self.neighbors(key))
        i = 1
        while True:
            if i == ring:
                break
            temp = []
            for nbr in nbrs:
                temp += self.neighbors(nbr)
            nbrs.update(temp)
            i += 1
        if key in nbrs:
            nbrs.remove(key)
        return list(nbrs)

    def neighbors_out(self, key):
        """Return the outgoing neighbors of a node.

        Parameters
        ----------
        key : hashable
            The identifier of the node.

        Returns
        -------
        list[hashable]
            A list of node identifiers.

        """
        return list(self.edge[key])

    def neighbors_in(self, key):
        """Return the incoming neighbors of a node.

        Parameters
        ----------
        key : hashable
            The identifier of the node.

        Returns
        -------
        list[hashable]
            A list of node identifiers.

        """
        return list(set(self.adjacency[key]) - set(self.edge[key]))

    def degree(self, key):
        """Return the number of neighbors of a node.

        Parameters
        ----------
        key : hashable
            The identifier of the node.

        Returns
        -------
        int
            The number of neighbors of the node.

        """
        return len(self.neighbors(key))

    def degree_out(self, key):
        """Return the number of outgoing neighbors of a node.

        Parameters
        ----------
        key : hashable
            The identifier of the node.

        Returns
        -------
        int
            The number of outgoing neighbors of the node.

        """
        return len(self.neighbors_out(key))

    def degree_in(self, key):
        """Return the numer of incoming neighbors of a node.

        Parameters
        ----------
        key : hashable
            The identifier of the node.

        Returns
        -------
        int
            The number of incoming neighbors of the node.

        """
        return len(self.neighbors_in(key))

    def connected_edges(self, key):
        """Return the edges connected to a node.

        Parameters
        ----------
        key : hashable
            The identifier of the node.

        Returns
        -------
        list[tuple[hashable, hashable]]
            The edges connected to the node.

        """
        edges = []
        for nbr in self.neighbors(key):
            if nbr in self.edge[key]:
                edges.append((key, nbr))
            else:
                edges.append((nbr, key))
        return edges

    # --------------------------------------------------------------------------
    # edge topology
    # --------------------------------------------------------------------------

    def has_edge(self, u, v, directed=True):
        """Verify if the network contains a specific edge.

        Parameters
        ----------
        u : hashable
            The identifier of the first node of the edge.
        v : hashable
            The identifier of the second node of the edge.
        directed : bool, optional
            If True, the direction of the edge is taken into account.

        Returns
        -------
        bool
            True if the edge is present, False otherwise.

        """
        if directed:
            return u in self.edge and v in self.edge[u]
        return (u in self.edge and v in self.edge[u]) or (v in self.edge and u in self.edge[v])
