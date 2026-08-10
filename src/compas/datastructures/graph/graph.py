from ast import literal_eval
from collections.abc import Mapping
from itertools import combinations
from random import sample
from random import shuffle
from typing import Any
from typing import Callable
from typing import Iterable
from typing import Iterator
from typing import Literal
from typing import Optional
from typing import Sequence
from typing import Union
from typing import overload

from typing_extensions import Self

from compas.datastructures.attributes import EdgeAttributeView
from compas.datastructures.attributes import NodeAttributeView
from compas.datastructures.datastructure import Datastructure
from compas.files import obj_data
from compas.files import read_obj
from compas.geometry import Box
from compas.geometry import Line
from compas.geometry import Point
from compas.geometry import Vector
from compas.geometry import add_vectors
from compas.geometry import bounding_box
from compas.geometry import centroid_points
from compas.geometry import distance_point_point
from compas.geometry import midpoint_line
from compas.geometry import normalize_vector
from compas.geometry import oriented_bounding_box
from compas.geometry import scale_vector
from compas.geometry import subtract_vectors
from compas.geometry import transform_points
from compas.tolerance import TOL
from compas.topology import astar_shortest_path
from compas.topology import breadth_first_traverse
from compas.topology import connected_components

from .duality import graph_find_cycles
from .operations.join import graph_join_edges
from .operations.split import graph_split_edge
from .planarity import graph_count_crossings
from .planarity import graph_embed_in_plane
from .planarity import graph_find_crossings
from .planarity import graph_is_crossed
from .planarity import graph_is_planar
from .planarity import graph_is_planar_embedding
from .planarity import graph_is_xy
from .smoothing import graph_smooth_centroid
from .types import AttributeDict
from .types import Edge
from .types import Node

_MISSING = object()


class Graph(Datastructure):
    """Data structure for describing the relationships between nodes connected by edges.

    Parameters
    ----------
    default_node_attributes
        Default values for node attributes.
    default_edge_attributes
        Default values for edge attributes.
    name
        The name of the graph.
    **kwargs
        Additional keyword arguments, which are stored in the attributes dict.

    Attributes
    ----------
    default_node_attributes
        dictionary containing default values for the attributes of nodes.
        It is recommended to add a default to this dictionary using update_default_node_attributes
        for every node attribute used in the data structure.
    default_edge_attributes
        dictionary containing default values for the attributes of edges.
        It is recommended to add a default to this dictionary using update_default_edge_attributes
        for every edge attribute used in the data structure.

    """

    split_edge = graph_split_edge
    join_edges = graph_join_edges
    smooth = graph_smooth_centroid
    is_crossed = graph_is_crossed
    is_planar = graph_is_planar
    is_planar_embedding = graph_is_planar_embedding
    is_xy = graph_is_xy
    count_crossings = graph_count_crossings
    find_crossings = graph_find_crossings
    embed_in_plane = graph_embed_in_plane
    find_cycles = graph_find_cycles

    @property
    def __data__(self) -> dict[str, Any]:
        return self.__before_json_dump__(
            {
                "attributes": self.attributes,
                "default_node_attributes": self.default_node_attributes,
                "default_edge_attributes": self.default_edge_attributes,
                "node": self.node,
                "edge": self.edge,
                "max_node": self._max_node,
            }
        )

    def __before_json_dump__(self, data: dict[str, Any]) -> dict[str, Any]:
        data["node"] = {repr(key): attr for key, attr in data["node"].items()}
        data["edge"] = {repr(u): {repr(v): attr for v, attr in nbrs.items()} for u, nbrs in data["edge"].items()}
        return data

    def __after_json_load__(self, data: dict[str, Any]) -> dict[str, Any]:
        l_e = literal_eval
        nodes = data["node"] or {}
        edges = data["edge"] or {}
        data["node"] = {l_e(node): attr for node, attr in nodes.items()}
        data["edge"] = {l_e(u): {l_e(v): attr for v, attr in nbrs.items()} for u, nbrs in edges.items()}
        return data

    @classmethod
    def __from_data__(cls, data: dict[str, Any]) -> Self:
        graph = cls(
            default_node_attributes=data.get("default_node_attributes"),
            default_edge_attributes=data.get("default_edge_attributes"),
        )
        graph.attributes.update(data["attributes"] or {})
        data = graph.__after_json_load__(data)
        for node, attr in iter(data["node"].items()):
            graph.add_node(key=node, attr_dict=attr)
        for u, nbrs in iter(data["edge"].items()):
            for v, attr in iter(nbrs.items()):
                graph.add_edge(u, v, attr_dict=attr)
        graph._max_node = data.get("max_node", graph._max_node)
        return graph

    def __init__(
        self,
        default_node_attributes: Optional[AttributeDict] = None,
        default_edge_attributes: Optional[AttributeDict] = None,
        name: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(kwargs, name=name)
        self._max_node = -1
        self.node = {}
        self.edge = {}
        self.adjacency = {}
        self.default_node_attributes = {"x": 0.0, "y": 0.0, "z": 0.0}
        self.default_edge_attributes = {}
        if default_node_attributes:
            self.default_node_attributes.update(default_node_attributes)
        if default_edge_attributes:
            self.default_edge_attributes.update(default_edge_attributes)

    def __str__(self) -> str:
        tpl = "<Graph with {} nodes, {} edges>"
        return tpl.format(self.number_of_nodes(), self.number_of_edges())

    # --------------------------------------------------------------------------
    # Constructors
    # --------------------------------------------------------------------------

    @classmethod
    def from_edges(cls, edges: Iterable[Edge]) -> Self:
        """Create a new graph instance from information about the edges.

        Parameters
        ----------
        edges
            The edges of the graph as pairs of node identifiers.

        Returns
        -------
        Graph

        See Also
        --------
        from_networkx

        """
        graph = cls()
        for u, v in edges:
            if u not in graph.node:
                graph.add_node(u)
            if v not in graph.node:
                graph.add_node(v)
            graph.add_edge(u, v)
        return graph

    @classmethod
    def from_networkx(cls, graph: Any) -> Self:
        """Create a new graph instance from a NetworkX DiGraph instance.

        Parameters
        ----------
        graph
            NetworkX instance of a directed graph.

        Returns
        -------
        Graph

        See Also
        --------
        to_networkx
        from_edges

        """
        g = cls()
        g.name = graph.graph.get("name")

        for node in graph.nodes():
            g.add_node(node, **graph.nodes[node])

        for edge in graph.edges():
            g.add_edge(*edge, **graph.edges[edge])

        return g

    @classmethod
    def from_obj(cls, filepath: Any, precision: Optional[int] = None) -> Self:
        """Construct a graph from the data contained in an OBJ file.

        Parameters
        ----------
        filepath
            A path, a file-like object or a URL pointing to a file.
        precision
            The precision of the geometric map that is used to connect the lines.

        Returns
        -------
        Graph
            A graph object.

        See Also
        --------
        to_obj
        from_lines, from_nodes_and_edges, from_pointcloud
        OBJ

        """
        data = obj_data(read_obj(filepath))
        lines = [(data.vertices[u], data.vertices[v]) for u, v in data.lines]
        return cls.from_lines(lines, precision=precision)

    @classmethod
    def from_lines(cls, lines: Iterable[Sequence[Any]], precision: Optional[int] = None) -> Self:
        """Construct a graph from a set of lines represented by their start and end point coordinates.

        Parameters
        ----------
        lines
            A list of pairs of point coordinates.
        precision
            Precision for converting numbers to strings.
            Default is TOL.precision.

        Returns
        -------
        Graph
            A graph object.

        See Also
        --------
        to_lines
        from_obj, from_nodes_and_edges, from_pointcloud

        """
        graph = cls()
        edges = []
        node = {}
        for line in lines:
            sp = line[0]
            ep = line[1]
            a = TOL.geometric_key(sp, precision)
            b = TOL.geometric_key(ep, precision)
            node[a] = sp
            node[b] = ep
            edges.append((a, b))
        key_index = dict((k, i) for i, k in enumerate(iter(node)))
        for key, xyz in iter(node.items()):
            i = key_index[key]
            graph.add_node(i, x=xyz[0], y=xyz[1], z=xyz[2])
        for u, v in edges:
            i = key_index[u]
            j = key_index[v]
            graph.add_edge(i, j)
        return graph

    @classmethod
    def from_nodes_and_edges(
        cls,
        nodes: Union[Sequence[Sequence[float]], dict[Node, Sequence[float]]],
        edges: Iterable[Edge],
    ) -> Self:
        """Construct a graph from nodes and edges.

        Parameters
        ----------
        nodes
            A list of node coordinates or a dictionary of keys pointing to node coordinates to specify keys.
        edges

        Returns
        -------
        Graph
            A graph object.

        See Also
        --------
        to_nodes_and_edges
        from_obj, from_lines, from_pointcloud

        """
        graph = cls()

        if isinstance(nodes, Mapping):
            for key, (x, y, z) in nodes.items():
                graph.add_node(key, x=x, y=y, z=z)
        else:
            for i, (x, y, z) in enumerate(nodes):
                graph.add_node(i, x=x, y=y, z=z)

        for u, v in edges:
            graph.add_edge(u, v)

        return graph

    @classmethod
    def from_pointcloud(cls, cloud: Iterable[Sequence[float]], degree: int = 3) -> Self:
        """Construct a graph from random connections between the points of a pointcloud.

        Parameters
        ----------
        cloud
            A pointcloud object.
        degree
            The number of connections per node.

        Returns
        -------
        Graph
            A graph object.

        See Also
        --------
        to_points
        from_obj, from_lines, from_nodes_and_edges

        """
        graph = cls()
        for x, y, z in cloud:
            graph.add_node(x=x, y=y, z=z)
        nodes = list(graph.nodes())
        for u in graph.nodes():
            shuffle(nodes)
            for v in nodes:
                if v == u:
                    continue
                if graph.degree(v) == degree:
                    continue
                if graph.degree(u) == degree:
                    break
                graph.add_edge(u, v)
        return graph

    # --------------------------------------------------------------------------
    # Converters
    # --------------------------------------------------------------------------

    def to_obj(self) -> None:
        """Write the graph to an OBJ file.

        Parameters
        ----------
        filepath
            A path or a file-like object pointing to a file.

        Returns
        -------
        None

        See Also
        --------
        from_obj
        to_lines, to_nodes_and_edges, to_points

        """
        raise NotImplementedError

    def to_points(self) -> list[list[float]]:
        """Return the coordinates of the graph.

        Returns
        -------
        list[list[float]]
            A list with the coordinates of the vertices of the graph.

        See Also
        --------
        from_pointcloud
        to_lines, to_nodes_and_edges, to_obj

        """
        return [self.node_coordinates(key) for key in self.nodes()]

    def to_lines(self) -> list[tuple[list[float], list[float]]]:
        """Return the lines of the graph as pairs of start and end point coordinates.

        Returns
        -------
        list[tuple[list[float], list[float]]]
            A list of lines each defined by a pair of point coordinates.

        See Also
        --------
        from_lines
        to_nodes_and_edges, to_obj, to_points

        """
        return [self.edge_coordinates(edge) for edge in self.edges()]

    def to_nodes_and_edges(self) -> tuple[list[list[float]], list[tuple[int, int]]]:
        """Return the nodes and edges of a graph.

        Returns
        -------
        tuple[list[list[float]], list[tuple[int, int]]]
            A list of nodes, represented by their XYZ coordinates, and
            a list of edges, with each edge represented by a pair of indices in the node list.

        See Also
        --------
        from_nodes_and_edges
        to_lines, to_obj, to_points

        """
        key_index = dict((key, index) for index, key in enumerate(self.nodes()))
        nodes = [self.node_coordinates(key) for key in self.nodes()]
        edges = [(key_index[u], key_index[v]) for u, v in self.edges()]
        return nodes, edges

    def to_networkx(self) -> Any:
        """Create a new NetworkX graph instance from a graph.

        Returns
        -------
        networkx.DiGraph
            A newly created NetworkX DiGraph.

        See Also
        --------
        from_networkx

        """
        import networkx as nx

        G = nx.DiGraph()
        G.graph["name"] = self.name  # type: ignore

        for node, attr in self.nodes(data=True):
            G.add_node(node, **attr)  # type: ignore

        for edge, attr in self.edges(data=True):
            G.add_edge(*edge, **attr)

        return G

    # --------------------------------------------------------------------------
    # Helpers
    # --------------------------------------------------------------------------

    def clear(self) -> None:
        """Clear all the graph data.

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

    def node_sample(self, size: int = 1) -> list[Node]:
        """Get a list of identifiers of a random set of n nodes.

        Parameters
        ----------
        size
            The size of the sample.

        Returns
        -------
        list[hashable]
            The identifiers of the nodes.

        See Also
        --------
        edge_sample

        """
        return sample(list(self.nodes()), size)

    def edge_sample(self, size: int = 1) -> list[Edge]:
        """Get the identifiers of a set of random edges.

        Parameters
        ----------
        size
            The size of the sample.

        Returns
        -------
        list[tuple[hashable, hashable]]
            The identifiers of the random edges.

        See Also
        --------
        node_sample

        """
        return sample(list(self.edges()), size)

    def node_index(self) -> dict[Node, int]:
        """Returns a dictionary that maps node identifiers to their corresponding index in a node list or array.

        Returns
        -------
        dict[hashable, int]
            A dictionary of node-index pairs.

        See Also
        --------
        index_node
        edge_index

        """
        return {key: index for index, key in enumerate(self.nodes())}

    def index_node(self) -> dict[int, Node]:
        """Returns a dictionary that maps the indices of a node list to keys in a node dictionary.

        Returns
        -------
        dict[int, hashable]
            A dictionary of index-node pairs.

        See Also
        --------
        node_index
        index_edge

        """
        return dict(enumerate(self.nodes()))

    def edge_index(self) -> dict[Edge, int]:
        """Returns a dictionary that maps edge identifiers (i.e. pairs of vertex identifiers)
        to the corresponding edge index in a list or array of edges.

        Returns
        -------
        dict[tuple[hashable, hashable], int]
            A dictionary of uv-index pairs.

        See Also
        --------
        index_edge
        node_index

        """
        return {(u, v): index for index, (u, v) in enumerate(self.edges())}

    def index_edge(self) -> dict[int, Edge]:
        """Returns a dictionary that maps edges in a list to the corresponding
        vertex identifier pairs.

        Returns
        -------
        dict[int, tuple[hashable, hashable]]
            A dictionary of index-uv pairs.

        See Also
        --------
        edge_index
        index_node

        """
        return dict(enumerate(self.edges()))

    def node_gkey(self, precision: Optional[int] = None) -> dict[Node, str]:
        """Returns a dictionary that maps node identifiers to the corresponding
        *geometric key* up to a certain precision.

        Parameters
        ----------
        precision
            Precision for converting numbers to strings.
            Default is TOL.precision.

        Returns
        -------
        dict[hashable, str]
            A dictionary of (node, geometric key) pairs.

        See Also
        --------
        gkey_node
        TOL.geometric_key

        """
        gkey = TOL.geometric_key
        xyz = self.node_coordinates
        return {key: gkey(xyz(key), precision) for key in self.nodes()}

    def gkey_node(self, precision: Optional[int] = None) -> dict[str, Node]:
        """Returns a dictionary that maps *geometric keys* of a certain precision
        to the identifiers of the corresponding nodes.

        Parameters
        ----------
        precision
            Precision for converting numbers to strings.
            Default is TOL.precision.

        Returns
        -------
        dict[str, hashable]
            A dictionary of (geometric key, node) pairs.

        See Also
        --------
        node_gkey
        TOL.geometric_key

        """
        gkey = TOL.geometric_key
        xyz = self.node_coordinates
        return {gkey(xyz(key), precision): key for key in self.nodes()}

    # --------------------------------------------------------------------------
    # Builders
    # --------------------------------------------------------------------------

    def add_node(
        self,
        key: Optional[Node] = None,
        attr_dict: Optional[AttributeDict] = None,
        **kwattr: Any,
    ) -> Node:
        """Add a node and specify its attributes (optional).

        Parameters
        ----------
        key
            An identifier for the node.
            Defaults to None, in which case an identifier of type int is automatically generated.
        attr_dict
            A dictionary of vertex attributes.
        **kwattr
            A dictionary of additional attributes compiled of remaining named arguments.

        Returns
        -------
        hashable
            The identifier of the node.

        See Also
        --------
        add_edge
        delete_node

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
        elif isinstance(key, int) and key > self._max_node:
            self._max_node = key

        if key not in self.node:
            self.node[key] = {}
            self.edge[key] = {}
            self.adjacency[key] = {}
        attr = attr_dict or {}
        attr.update(kwattr)
        self.node[key].update(attr)
        return key

    def add_edge(
        self,
        u: Node,
        v: Node,
        attr_dict: Optional[AttributeDict] = None,
        **kwattr: Any,
    ) -> Edge:
        """Add an edge and specify its attributes.

        Parameters
        ----------
        u
            The identifier of the first node of the edge.
        v
            The identifier of the second node of the edge.
        attr_dict
            A dictionary of edge attributes.
        **kwattr
            A dictionary of additional attributes compiled of remaining named arguments.

        Returns
        -------
        tuple[hashable, hashable]
            The identifier of the edge.

        See Also
        --------
        add_node
        delete_edge

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
    # Modifiers
    # --------------------------------------------------------------------------

    def delete_node(self, key: Node) -> None:
        """Delete a node from the graph.

        Parameters
        ----------
        key
            The identifier of the node.

        Returns
        -------
        None

        See Also
        --------
        delete_edge
        add_node

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

    def delete_edge(self, edge: Edge) -> None:
        """Delete an edge from the graph.

        Parameters
        ----------
        edge
            The identifier of the edge as a pair of node identifiers.

        Returns
        -------
        None

        See Also
        --------
        delete_node
        add_edge

        Examples
        --------
        >>>

        """
        u, v = edge

        if u in self.edge and v in self.edge[u]:
            del self.edge[u][v]

        if u == v:  # invalid edge
            del self.adjacency[u][v]
        elif v not in self.edge or u not in self.edge[v]:
            del self.adjacency[u][v]
            del self.adjacency[v][u]
        # else: an edge in an opposite direction exists, we don't want to delete the adjacency

    # --------------------------------------------------------------------------
    # Info
    # --------------------------------------------------------------------------

    def summary(self) -> str:
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

    def number_of_nodes(self) -> int:
        """Compute the number of nodes of the graph.

        Returns
        -------
        int
            The number of nodes.

        See Also
        --------
        number_of_edges

        """
        return len(list(self.nodes()))

    def number_of_edges(self) -> int:
        """Compute the number of edges of the graph.

        Returns
        -------
        int
            The number of edges.

        See Also
        --------
        number_of_nodes

        """
        return len(list(self.edges()))

    def is_connected(self) -> bool:
        """Verify that the graph is connected.


        Returns
        -------
        bool
            True, if the graph is connected.
            False, otherwise.

        Notes
        -----
        A graph is connected if for every two vertices a path exists connecting them.

        Examples
        --------
        >>> import compas
        >>> from compas.datastructures import Graph
        >>> graph = Graph.from_obj(compas.get("lines.obj"))
        >>> graph.is_connected()
        True

        """
        if self.number_of_nodes() == 0:
            return False
        nodes = breadth_first_traverse(self.adjacency, self.node_sample(size=1)[0])
        return len(nodes) == self.number_of_nodes()

    # --------------------------------------------------------------------------
    # Accessors
    # --------------------------------------------------------------------------

    @overload
    def nodes(self, data: Literal[False] = False) -> Iterator[Node]: ...

    @overload
    def nodes(self, data: Literal[True]) -> Iterator[tuple[Node, NodeAttributeView]]: ...

    @overload
    def nodes(self, data: bool) -> Iterator[Union[Node, tuple[Node, NodeAttributeView]]]: ...

    def nodes(self, data: bool = False) -> Iterator[Any]:
        """Iterate over the nodes of the graph.

        Parameters
        ----------
        data
            If True, yield the node attributes in addition to the node identifiers.

        Yields
        ------
        hashable
            The node identifier if `data` is `False`.
        tuple[hashable, NodeAttributeView]
            The node identifier and its attributes if `data` is `True`.

        See Also
        --------
        nodes_where, nodes_where_predicate
        edges, edges_where, edges_where_predicate

        """
        for key in self.node:
            if not data:
                yield key
            else:
                yield key, self.node_attributes(key)

    @overload
    def nodes_where(
        self,
        conditions: Optional[AttributeDict] = None,
        data: Literal[False] = False,
        **kwargs: Any,
    ) -> Iterator[Node]: ...

    @overload
    def nodes_where(
        self,
        conditions: Optional[AttributeDict],
        data: Literal[True],
        **kwargs: Any,
    ) -> Iterator[tuple[Node, NodeAttributeView]]: ...

    @overload
    def nodes_where(
        self,
        conditions: Optional[AttributeDict] = None,
        data: bool = False,
        **kwargs: Any,
    ) -> Iterator[Union[Node, tuple[Node, NodeAttributeView]]]: ...

    def nodes_where(
        self,
        conditions: Optional[AttributeDict] = None,
        data: bool = False,
        **kwargs: Any,
    ) -> Iterator[Any]:
        """Get nodes for which a certain condition or set of conditions is true.

        Parameters
        ----------
        conditions
            A set of conditions in the form of key-value pairs.
            The keys should be attribute names. The values can be attribute
            values or ranges of attribute values in the form of min/max pairs.
        data
            If True, yield the node attributes in addition to the node identifiers.

        Yields
        ------
        hashable
            A matching node identifier if `data` is `False`.
        tuple[hashable, NodeAttributeView]
            A matching node identifier and its attributes if `data` is `True`.

        See Also
        --------
        nodes, nodes_where_predicate
        edges, edges_where, edges_where_predicate

        """
        conditions = conditions or {}
        conditions.update(kwargs)

        for key, attr in self.nodes(True):
            is_match = True
            attr = attr or {}

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

    @overload
    def nodes_where_predicate(
        self,
        predicate: Callable[[Node, NodeAttributeView], bool],
        data: Literal[False] = False,
    ) -> Iterator[Node]: ...

    @overload
    def nodes_where_predicate(
        self,
        predicate: Callable[[Node, NodeAttributeView], bool],
        data: Literal[True],
    ) -> Iterator[tuple[Node, NodeAttributeView]]: ...

    @overload
    def nodes_where_predicate(
        self,
        predicate: Callable[[Node, NodeAttributeView], bool],
        data: bool,
    ) -> Iterator[Union[Node, tuple[Node, NodeAttributeView]]]: ...

    def nodes_where_predicate(
        self,
        predicate: Callable[[Node, NodeAttributeView], bool],
        data: bool = False,
    ) -> Iterator[Any]:
        """Get nodes for which a certain condition or set of conditions is true using a lambda function.

        Parameters
        ----------
        predicate
            The condition you want to evaluate.
            The callable takes 2 parameters
        data
            If True, yield the node attributes in addition to the node identifiers.

        Yields
        ------
        hashable
            A matching node identifier if `data` is `False`.
        tuple[hashable, NodeAttributeView]
            A matching node identifier and its attributes if `data` is `True`.

        See Also
        --------
        nodes, nodes_where
        edges, edges_where, edges_where_predicate

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

    @overload
    def edges(self, data: Literal[False] = False) -> Iterator[Edge]: ...

    @overload
    def edges(self, data: Literal[True]) -> Iterator[tuple[Edge, EdgeAttributeView]]: ...

    @overload
    def edges(self, data: bool) -> Iterator[Union[Edge, tuple[Edge, EdgeAttributeView]]]: ...

    def edges(self, data: bool = False) -> Iterator[Any]:
        """Iterate over the edges of the graph.

        Parameters
        ----------
        data
            If True, yield the edge attributes in addition to the edge identifiers.

        Yields
        ------
        tuple[hashable, hashable]
            The edge identifier if `data` is `False`.
        tuple[tuple[hashable, hashable], EdgeAttributeView]
            The edge identifier and its attributes if `data` is `True`.

        See Also
        --------
        edges_where, edges_where_predicate
        nodes, nodes_where, nodes_where_predicate

        """
        for u, nbrs in iter(self.edge.items()):
            for v, attr in iter(nbrs.items()):
                if data:
                    yield (u, v), attr
                else:
                    yield u, v

    @overload
    def edges_where(
        self,
        conditions: Optional[AttributeDict] = None,
        data: Literal[False] = False,
        **kwargs: Any,
    ) -> Iterator[Edge]: ...

    @overload
    def edges_where(
        self,
        conditions: Optional[AttributeDict],
        data: Literal[True],
        **kwargs: Any,
    ) -> Iterator[tuple[Edge, EdgeAttributeView]]: ...

    @overload
    def edges_where(
        self,
        conditions: Optional[AttributeDict] = None,
        data: bool = False,
        **kwargs: Any,
    ) -> Iterator[Union[Edge, tuple[Edge, EdgeAttributeView]]]: ...

    def edges_where(
        self,
        conditions: Optional[AttributeDict] = None,
        data: bool = False,
        **kwargs: Any,
    ) -> Iterator[Any]:
        """Get edges for which a certain condition or set of conditions is true.

        Parameters
        ----------
        conditions
            A set of conditions in the form of key-value pairs.
            The keys should be attribute names. The values can be attribute
            values or ranges of attribute values in the form of min/max pairs.
        data
            If True, yield the edge attributes in addition to the edge identifiers.
        **kwargs
            Additional conditions provided as named function arguments.

        Yields
        ------
        tuple[hashable, hashable]
            A matching edge identifier if `data` is `False`.
        tuple[tuple[hashable, hashable], EdgeAttributeView]
            A matching edge identifier and its attributes if `data` is `True`.

        See Also
        --------
        edges, edges_where_predicate
        nodes, nodes_where, nodes_where_predicate

        """
        conditions = conditions or {}
        conditions.update(kwargs)

        for key in self.edges():
            is_match = True

            attr = self.edge_attributes(key) or {}

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

    @overload
    def edges_where_predicate(
        self,
        predicate: Callable[[Edge, EdgeAttributeView], bool],
        data: Literal[False] = False,
    ) -> Iterator[Edge]: ...

    @overload
    def edges_where_predicate(
        self,
        predicate: Callable[[Edge, EdgeAttributeView], bool],
        data: Literal[True],
    ) -> Iterator[tuple[Edge, EdgeAttributeView]]: ...

    @overload
    def edges_where_predicate(
        self,
        predicate: Callable[[Edge, EdgeAttributeView], bool],
        data: bool,
    ) -> Iterator[Union[Edge, tuple[Edge, EdgeAttributeView]]]: ...

    def edges_where_predicate(
        self,
        predicate: Callable[[Edge, EdgeAttributeView], bool],
        data: bool = False,
    ) -> Iterator[Any]:
        """Get edges for which a certain condition or set of conditions is true using a lambda function.

        Parameters
        ----------
        predicate
            The condition you want to evaluate.
            The callable takes 2 parameters:
            an edge identifier (tuple of node identifiers) and edge attributes,
            and should return True or False.
        data
            If True, yield the edge attributes in addition to the edge attributes.

        Yields
        ------
        tuple[hashable, hashable]
            A matching edge identifier if `data` is `False`.
        tuple[tuple[hashable, hashable], EdgeAttributeView]
            A matching edge identifier and its attributes if `data` is `True`.

        See Also
        --------
        edges, edges_where
        nodes, nodes_where, nodes_where_predicate

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

    def shortest_path(self, u: Node, v: Node) -> Optional[list[Node]]:
        """Find the shortest path between two nodes using the A* algorithm.

        Parameters
        ----------
        u
            The identifier of the start node.
        v
            The identifier of the end node.

        Returns
        -------
        list[hashable] | None
            The path from root to goal, or None, if no path exists between the vertices.

        See Also
        --------
        astar_shortest_path

        """
        return astar_shortest_path(self, u, v)

    # --------------------------------------------------------------------------
    # Default attributes
    # --------------------------------------------------------------------------

    def update_default_node_attributes(self, attr_dict: Optional[AttributeDict] = None, **kwattr: Any) -> None:
        """Update the default node attributes.

        Parameters
        ----------
        attr_dict
            A dictionary of attributes with their default values.
        **kwattr
            A dictionary of additional attributes compiled of remaining named arguments.

        Returns
        -------
        None

        See Also
        --------
        update_default_edge_attributes

        """
        if not attr_dict:
            attr_dict = {}
        attr_dict.update(kwattr)
        self.default_node_attributes.update(attr_dict)

    def update_default_edge_attributes(self, attr_dict: Optional[AttributeDict] = None, **kwattr: Any) -> None:
        """Update the default edge attributes.

        Parameters
        ----------
        attr_dict
            A dictionary of attributes with their default values.
        **kwattr
            A dictionary of additional attributes compiled of remaining named arguments.

        Returns
        -------
        None

        See Also
        --------
        update_default_node_attributes

        """
        if not attr_dict:
            attr_dict = {}
        attr_dict.update(kwattr)
        self.default_edge_attributes.update(attr_dict)

    # --------------------------------------------------------------------------
    # Node attributes
    # --------------------------------------------------------------------------

    @overload
    def node_attribute(self, key: Node, name: str) -> Any: ...

    @overload
    def node_attribute(self, key: Node, name: str, value: Any) -> None: ...

    def node_attribute(self, key: Node, name: str, value: Any = _MISSING) -> Any:
        """Get or set an attribute of a node.

        Parameters
        ----------
        key
            The node identifier.
        name
            The name of the attribute
        value
            The value of the attribute. If omitted, the current value is returned.

        Returns
        -------
        Any
            The attribute value when `value` is not provided.
        None
            When `value` is provided.

        Raises
        ------
        KeyError
            If the node does not exist.

        See Also
        --------
        unset_node_attribute
        node_attributes, nodes_attribute, nodes_attributes
        edge_attribute, edge_attributes, edges_attribute, edges_attributes

        """
        if key not in self.node:
            raise KeyError(key)
        if value is not _MISSING:
            self.node[key][name] = value
            return
        if name in self.node[key]:
            return self.node[key][name]
        else:
            if name in self.default_node_attributes:
                return self.default_node_attributes[name]

    def unset_node_attribute(self, key: Node, name: str) -> None:
        """Unset the attribute of a node.

        Parameters
        ----------
        key
            The node identifier.
        name
            The name of the attribute.

        Raises
        ------
        KeyError
            If the node does not exist.

        See Also
        --------
        node_attribute

        Notes
        -----
        Unsetting the value of a node attribute implicitly sets it back to the value
        stored in the default node attribute dict.

        """
        if name in self.node[key]:
            del self.node[key][name]

    def node_attributes(
        self,
        key: Node,
        names: Optional[Sequence[str]] = None,
        values: Optional[list[Any]] = None,
    ) -> Any:
        """Get or set multiple attributes of a node.

        Parameters
        ----------
        key
            The identifier of the node.
        names
            A list of attribute names.
        values
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

        See Also
        --------
        node_attribute, nodes_attribute, nodes_attributes
        edge_attribute, edge_attributes, edges_attribute, edges_attributes

        """
        if key not in self.node:
            raise KeyError(key)
        if names and values is not None:
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

    @overload
    def nodes_attribute(
        self,
        name: str,
        *,
        keys: Optional[Iterable[Node]] = None,
    ) -> list[Any]: ...

    @overload
    def nodes_attribute(
        self,
        name: str,
        value: Any,
        keys: Optional[Iterable[Node]] = None,
    ) -> None: ...

    def nodes_attribute(
        self,
        name: str,
        value: Any = _MISSING,
        keys: Optional[Iterable[Node]] = None,
    ) -> Optional[list[Any]]:
        """Get or set an attribute of multiple nodes.

        Parameters
        ----------
        name
            The name of the attribute.
        value
            The value of the attribute. If omitted, the current values are returned.
        keys
            A list of node identifiers.

        Returns
        -------
        list[Any]
            The attribute values when `value` is not provided.
        None
            When `value` is provided.

        Raises
        ------
        KeyError
            If any of the nodes does not exist.

        See Also
        --------
        node_attribute, node_attributes, nodes_attributes
        edge_attribute, edge_attributes, edges_attribute, edges_attributes

        """
        if not keys:
            keys = self.nodes()
        if value is not _MISSING:
            for key in keys:
                self.node_attribute(key, name, value)
            return
        return [self.node_attribute(key, name) for key in keys]

    def nodes_attributes(
        self,
        names: Optional[Sequence[str]] = None,
        values: Optional[list[Any]] = None,
        keys: Optional[Iterable[Node]] = None,
    ) -> Any:
        """Get or set multiple attributes of multiple nodes.

        Parameters
        ----------
        names
            The names of the attribute.
        values
            The values of the attributes.
        keys
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

        See Also
        --------
        node_attribute, node_attributes, nodes_attribute
        edge_attribute, edge_attributes, edges_attribute, edges_attributes

        """
        if not keys:
            keys = self.nodes()
        if values:
            for key in keys:
                self.node_attributes(key, names, values)
            return
        return [self.node_attributes(key, names) for key in keys]

    # --------------------------------------------------------------------------
    # Edge attributes
    # --------------------------------------------------------------------------

    @overload
    def edge_attribute(self, key: Edge, name: str) -> Any: ...

    @overload
    def edge_attribute(self, key: Edge, name: str, value: Any) -> None: ...

    def edge_attribute(self, key: Edge, name: str, value: Any = _MISSING) -> Any:
        """Get or set an attribute of an edge.

        Parameters
        ----------
        key
            The identifier of the edge as a pair of node identifiers.
        name
            The name of the attribute.
        value
            The value of the attribute. If omitted, the current value is returned.

        Returns
        -------
        Any
            The attribute value when `value` is not provided.
        None
            When `value` is provided.

        Raises
        ------
        KeyError
            If the edge does not exist.

        See Also
        --------
        unset_edge_attribute
        edge_attributes, edges_attribute, edges_attributes
        node_attribute, node_attributes, nodes_attribute, nodes_attributes

        """
        u, v = key
        if u not in self.edge or v not in self.edge[u]:
            raise KeyError(key)
        attr = self.edge[u][v]
        if value is not _MISSING:
            attr[name] = value
            return
        if name in attr:
            return attr[name]
        if name in self.default_edge_attributes:
            return self.default_edge_attributes[name]

    def unset_edge_attribute(self, key: Edge, name: str) -> None:
        """Unset the attribute of an edge.

        Parameters
        ----------
        key
            The edge identifier.
        name
            The name of the attribute.

        Returns
        -------
        None

        Raises
        ------
        KeyError
            If the edge does not exist.

        See Also
        --------
        edge_attribute

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

    def edge_attributes(
        self,
        key: Edge,
        names: Optional[Sequence[str]] = None,
        values: Optional[list[Any]] = None,
    ) -> Any:
        """Get or set multiple attributes of an edge.

        Parameters
        ----------
        key
            The identifier of the edge.
        names
            A list of attribute names.
        values
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

        See Also
        --------
        edge_attribute, edges_attribute, edges_attributes
        node_attribute, node_attributes, nodes_attribute, nodes_attributes

        """
        u, v = key
        if u not in self.edge or v not in self.edge[u]:
            raise KeyError(key)
        if names and values:
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

    @overload
    def edges_attribute(
        self,
        name: str,
        *,
        keys: Optional[Iterable[Edge]] = None,
    ) -> list[Any]: ...

    @overload
    def edges_attribute(
        self,
        name: str,
        value: Any,
        keys: Optional[Iterable[Edge]] = None,
    ) -> None: ...

    def edges_attribute(
        self,
        name: str,
        value: Any = _MISSING,
        keys: Optional[Iterable[Edge]] = None,
    ) -> Optional[list[Any]]:
        """Get or set an attribute of multiple edges.

        Parameters
        ----------
        name
            The name of the attribute.
        value
            The value of the attribute. If omitted, the current values are returned.
        keys
            A list of edge identifiers.

        Returns
        -------
        list[Any]
            The attribute values when `value` is not provided.
        None
            When `value` is provided.

        Raises
        ------
        KeyError
            If any of the edges does not exist.

        See Also
        --------
        edge_attribute, edge_attributes, edges_attributes
        node_attribute, node_attributes, nodes_attribute, nodes_attributes

        """
        if not keys:
            keys = self.edges()
        if value is not _MISSING:
            for key in keys:
                self.edge_attribute(key, name, value)
            return
        return [self.edge_attribute(key, name) for key in keys]

    def edges_attributes(
        self,
        names: Optional[Sequence[str]] = None,
        values: Optional[list[Any]] = None,
        keys: Optional[Iterable[Edge]] = None,
    ) -> Any:
        """Get or set multiple attributes of multiple edges.

        Parameters
        ----------
        names
            The names of the attribute.
        values
            The values of the attributes.
        keys
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

        See Also
        --------
        edge_attribute, edge_attributes, edges_attribute
        node_attribute, node_attributes, nodes_attribute, nodes_attributes

        """
        if not keys:
            keys = self.edges()
        if values:
            for key in keys:
                self.edge_attributes(key, names, values)
            return
        return [self.edge_attributes(key, names) for key in keys]

    # --------------------------------------------------------------------------
    # Node topology
    # --------------------------------------------------------------------------

    def has_node(self, key: Node) -> bool:
        """Verify if a specific node is present in the graph.

        Parameters
        ----------
        key
            The identifier of the node.

        Returns
        -------
        bool
            True or False.

        See Also
        --------
        has_edge

        """
        return key in self.node

    def is_leaf(self, key: Node) -> bool:
        """Verify if a node is a leaf.

        Parameters
        ----------
        key
            The identifier of the node.

        Returns
        -------
        bool
            True or False.

        See Also
        --------
        leaves
        is_node_connected

        Notes
        -----
        A node is a *leaf* if it has only one neighbor.

        """
        return self.degree(key) == 1

    def leaves(self) -> list[Node]:
        """Return all leaves of the graph.

        Returns
        -------
        list[hashable]
            A list of node identifiers.

        """
        return [key for key in self.nodes() if self.is_leaf(key)]

    def is_node_connected(self, key: Node) -> bool:
        """Verify if a specific node is connected.

        Parameters
        ----------
        key
            The identifier of the node.

        Returns
        -------
        bool
            True or False.

        See Also
        --------
        is_leaf

        """
        return self.degree(key) > 0

    def neighbors(self, key: Node) -> list[Node]:
        """Return the neighbors of a node.

        Parameters
        ----------
        key
            The identifier of the node.

        Returns
        -------
        list[hashable]
            A list of node identifiers.

        See Also
        --------
        neighbors_out, neighbors_in
        neighborhood

        """
        return list(self.adjacency[key])

    def neighborhood(self, key: Node, ring: int = 1) -> list[Node]:
        """Return the nodes in the neighborhood of a node.

        Parameters
        ----------
        key
            The identifier of the node.
        ring
            The size of the neighborhood.

        Returns
        -------
        list[hashable]
            A list of node identifiers.

        See Also
        --------
        neighbors

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

    def neighbors_out(self, key: Node) -> list[Node]:
        """Return the outgoing neighbors of a node.

        Parameters
        ----------
        key
            The identifier of the node.

        Returns
        -------
        list[hashable]
            A list of node identifiers.

        See Also
        --------
        neighbors, neighbors_in

        """
        return list(self.edge[key])

    def neighbors_in(self, key: Node) -> list[Node]:
        """Return the incoming neighbors of a node.

        Parameters
        ----------
        key
            The identifier of the node.

        Returns
        -------
        list[hashable]
            A list of node identifiers.

        See Also
        --------
        neighbors, neighbors_out

        """
        return list(set(self.adjacency[key]) - set(self.edge[key]))

    def degree(self, key: Node) -> int:
        """Return the number of neighbors of a node.

        Parameters
        ----------
        key
            The identifier of the node.

        Returns
        -------
        int
            The number of neighbors of the node.

        See Also
        --------
        degree_out, degree_in

        """
        return len(self.neighbors(key))

    def degree_out(self, key: Node) -> int:
        """Return the number of outgoing neighbors of a node.

        Parameters
        ----------
        key
            The identifier of the node.

        Returns
        -------
        int
            The number of outgoing neighbors of the node.

        See Also
        --------
        degree, degree_in

        """
        return len(self.neighbors_out(key))

    def degree_in(self, key: Node) -> int:
        """Return the numer of incoming neighbors of a node.

        Parameters
        ----------
        key
            The identifier of the node.

        Returns
        -------
        int
            The number of incoming neighbors of the node.

        See Also
        --------
        degree, degree_out

        """
        return len(self.neighbors_in(key))

    def node_edges(self, key: Node) -> list[Edge]:
        """Return the edges connected to a node.

        Parameters
        ----------
        key
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
    # Edge topology
    # --------------------------------------------------------------------------

    def has_edge(self, edge: Edge, directed: bool = True) -> bool:
        """Verify if the graph contains a specific edge.

        Parameters
        ----------
        edge
            The identifier of the edge as a pair of node identifiers.
        directed
            If True, the direction of the edge is taken into account.

        Returns
        -------
        bool
            True if the edge is present, False otherwise.

        See Also
        --------
        has_node

        """
        u, v = edge
        if directed:
            return u in self.edge and v in self.edge[u]
        return (u in self.edge and v in self.edge[u]) or (v in self.edge and u in self.edge[v])

    # --------------------------------------------------------------------------
    # Node geometry
    # --------------------------------------------------------------------------

    def node_coordinates(self, key: Node, axes: str = "xyz") -> list[float]:
        """Return the coordinates of a node.

        Parameters
        ----------
        key
            The identifier of the node.
        axes
            The components of the node coordinates to return.

        Returns
        -------
        list[float]
            The coordinates of the node.

        See Also
        --------
        node_point, node_laplacian, node_neighborhood_centroid

        """
        return [self.node[key][axis] for axis in axes]

    def node_point(self, node: Node) -> Point:
        """Return the point of a node.

        Parameters
        ----------
        node
            The identifier of the node.

        Returns
        -------
        Point
            The point of the node.

        See Also
        --------
        node_coordinates, node_laplacian, node_neighborhood_centroid

        """
        return Point(*self.node_coordinates(node))

    def node_laplacian(self, key: Node) -> Vector:
        """Return the vector from the node to the centroid of its 1-ring neighborhood.

        Parameters
        ----------
        key
            The identifier of the node.

        Returns
        -------
        Vector
            The laplacian vector.

        See Also
        --------
        node_coordinates, node_point, node_neighborhood_centroid

        """
        c = centroid_points([self.node_coordinates(nbr) for nbr in self.neighbors(key)])
        p = self.node_coordinates(key)
        return Vector(*subtract_vectors(c, p))

    def node_neighborhood_centroid(self, key: Node) -> Point:
        """Return the computed centroid of the neighboring nodes.

        Parameters
        ----------
        key
            The identifier of the node.

        Returns
        -------
        Point
            The point at the centroid.

        See Also
        --------
        node_coordinates, node_point, node_laplacian

        """
        return Point(*centroid_points([self.node_coordinates(nbr) for nbr in self.neighbors(key)]))

    # --------------------------------------------------------------------------
    # Edge geometry
    # --------------------------------------------------------------------------

    def edge_coordinates(self, edge: Edge, axes: str = "xyz") -> tuple[list[float], list[float]]:
        """Return the coordinates of the start and end point of an edge.

        Parameters
        ----------
        edge
            The identifier of the edge.
        axes
            The axes along which the coordinates should be included.

        Returns
        -------
        tuple[list[float], list[float]]
            The coordinates of the start point.
            The coordinates of the end point.

        See Also
        --------
        edge_point, edge_start, edge_end, edge_midpoint

        """
        u, v = edge
        return self.node_coordinates(u, axes=axes), self.node_coordinates(v, axes=axes)

    def edge_start(self, edge: Edge) -> Point:
        """Return the start point of an edge.

        Parameters
        ----------
        edge
            The identifier of the edge.

        Returns
        -------
        Point
            The start point of the edge.

        See Also
        --------
        edge_point, edge_end, edge_midpoint

        """
        return self.node_point(edge[0])

    def edge_end(self, edge: Edge) -> Point:
        """Return the end point of an edge.

        Parameters
        ----------
        edge
            The identifier of the edge.

        Returns
        -------
        Point
            The end point of the edge.

        See Also
        --------
        edge_point, edge_start, edge_midpoint

        """
        return self.node_point(edge[1])

    def edge_point(self, edge: Edge, t: float = 0.5) -> Point:
        """Return the point at a parametric location along an edge.

        Parameters
        ----------
        edge
            The identifier of the edge.
        t
            The location of the point on the edge.
            If the value of `t` is outside the range 0-1, the point will
            lie in the direction of the edge, but not on the edge vector.

        Returns
        -------
        Point
            The point at the specified location.

        See Also
        --------
        edge_start, edge_end, edge_midpoint

        """
        if t == 0.0:
            return self.edge_start(edge)
        if t == 1.0:
            return self.edge_end(edge)
        if t == 0.5:
            return self.edge_midpoint(edge)

        a, b = self.edge_coordinates(edge)
        ab = subtract_vectors(b, a)
        return Point(*add_vectors(a, scale_vector(ab, t)))

    def edge_midpoint(self, edge: Edge) -> Point:
        """Return the location of the midpoint of an edge.

        Parameters
        ----------
        edge
            The identifier of the edge.

        Returns
        -------
        Point
            The midpoint of the edge.

        See Also
        --------
        edge_start, edge_end, edge_point

        """
        a, b = self.edge_coordinates(edge)
        return Point(*midpoint_line((a, b)))

    def edge_vector(self, edge: Edge) -> Vector:
        """Return the vector of an edge.

        Parameters
        ----------
        edge
            The identifier of the edge.

        Returns
        -------
        Vector
            The vector from start to end.

        See Also
        --------
        edge_direction, edge_line, edge_length

        """
        a, b = self.edge_coordinates(edge)
        return Vector.from_start_end(a, b)

    def edge_direction(self, edge: Edge) -> Vector:
        """Return the direction vector of an edge.

        Parameters
        ----------
        edge
            The identifier of the edge.

        Returns
        -------
        Vector
            The direction vector of the edge.

        See Also
        --------
        edge_vector, edge_line, edge_length

        """
        return Vector(*normalize_vector(self.edge_vector(edge)))

    def edge_line(self, edge: Edge) -> Line:
        """Return the line of an edge.

        Parameters
        ----------
        edge
            The identifier of the edge.

        Returns
        -------
        Line
            The line of the edge.

        See Also
        --------
        edge_vector, edge_direction, edge_length

        """
        return Line(*self.edge_coordinates(edge))

    def edge_length(self, edge: Edge) -> float:
        """Return the length of an edge.

        Parameters
        ----------
        edge
            The identifier of the edge.

        Returns
        -------
        float
            The length of the edge.

        See Also
        --------
        edge_vector, edge_direction, edge_line

        """
        a, b = self.edge_coordinates(edge)
        return distance_point_point(a, b)

    # --------------------------------------------------------------------------
    # Transformations and BBox
    # --------------------------------------------------------------------------

    def transform(self, transformation: Any) -> None:
        """Transform all nodes of the graph.

        Parameters
        ----------
        transformation
            The transformation used to transform the nodes.

        Returns
        -------
        None

        """
        nodes = self.nodes_attributes("xyz")
        points = transform_points(nodes, transformation)
        for point, node in zip(points, self.nodes()):
            self.node_attributes(node, "xyz", point)

    def aabb(self) -> Box:  # type: ignore[override]
        """Calculate the axis aligned bounding box of the graph.

        Returns
        -------
        Box

        """
        nodes = self.nodes_attributes("xyz")
        return Box.from_bounding_box(bounding_box(nodes))

    def obb(self) -> Box:  # type: ignore[override]
        """Calculate the oriented bounding box of the graph.

        Returns
        -------
        Box

        """
        nodes = self.nodes_attributes("xyz")
        return Box.from_bounding_box(oriented_bounding_box(nodes))

    # --------------------------------------------------------------------------
    # Other Methods
    # --------------------------------------------------------------------------

    def connected_nodes(self) -> list[list[Node]]:
        """Get groups of connected nodes.

        Returns
        -------
        list[list[hashable]]

        See Also
        --------
        connected_edges

        """
        return connected_components(self.adjacency)

    def connected_edges(self) -> list[list[Edge]]:
        """Get groups of connected edges.

        Returns
        -------
        list[list[tuple[hashable, hashable]]]

        See Also
        --------
        connected_nodes

        """
        return self._group_edges_by_component(self.connected_nodes())

    def _group_edges_by_component(self, components: Sequence[Sequence[Node]]) -> list[list[Edge]]:
        node_component = {node: index for index, nodes in enumerate(components) for node in nodes}
        edges_by_component: list[list[Edge]] = [[] for _ in components]
        for edge in self.edges():
            edges_by_component[node_component[edge[0]]].append(edge)
        return edges_by_component

    def exploded(self) -> list[Self]:
        """Explode the graph into its connected components.

        Returns
        -------
        list[Graph]

        """
        cls = type(self)
        graphs = []
        components = self.connected_nodes()
        edges_by_component = self._group_edges_by_component(components)
        for nodes, edges in zip(components, edges_by_component):
            graph = cls(
                default_node_attributes=self.default_node_attributes,
                default_edge_attributes=self.default_edge_attributes,
            )
            for node in nodes:
                graph.add_node(node, attr_dict=self.node_attributes(node))
            for u, v in edges:
                graph.add_edge(u, v, attr_dict=self.edge_attributes((u, v)))
            graphs.append(graph)
        return graphs

    def complement(self) -> Self:
        """Generate the complement of a graph.

        The complement of a graph G is the graph H with the same vertices
        but whose edges consists of the edges not present in the graph G [1]_.

        Returns
        -------
        Graph
            The complement graph.

        References
        ----------
        .. [1] Wolfram MathWorld. *Graph complement*.
            Available at: http://mathworld.wolfram.com/GraphComplement.html.

        Examples
        --------
        >>> import compas
        >>> from compas.datastructures import Graph
        >>> graph = Graph.from_obj(compas.get("lines.obj"))
        >>> complement = graph.complement()
        >>> any(complement.has_edge((u, v), directed=False) for u, v in graph.edges())
        False

        """
        cls = type(self)

        graph = cls(
            default_node_attributes=self.default_node_attributes,
            default_edge_attributes=self.default_edge_attributes,
        )
        for node in self.nodes():
            graph.add_node(node, attr_dict=self.node_attributes(node))

        for u, v in combinations(self.nodes(), 2):
            if not self.has_edge((u, v), directed=False):
                graph.add_edge(u, v)

        return graph

    # --------------------------------------------------------------------------
    # Matrices
    # --------------------------------------------------------------------------

    def adjacency_matrix(self, rtype: str = "array") -> Any:
        """Creates a node adjacency matrix from a Graph datastructure.

        Parameters
        ----------
        rtype
            Format of the result.

        Returns
        -------
        array_like
            Constructed adjacency matrix.

        """
        from compas.matrices import adjacency_matrix

        node_index = self.node_index()
        adjacency = [[node_index[nbr] for nbr in self.neighbors(key)] for key in self.nodes()]
        return adjacency_matrix(adjacency, rtype=rtype)

    def connectivity_matrix(self, rtype: str = "array") -> Any:
        """Creates a connectivity matrix from a Graph datastructure.

        Parameters
        ----------
        rtype
            Format of the result.

        Returns
        -------
        array_like
            Constructed connectivity matrix.

        """
        from compas.matrices import connectivity_matrix

        node_index = self.node_index()
        edges = [(node_index[u], node_index[v]) for u, v in self.edges()]
        return connectivity_matrix(edges, rtype=rtype)

    def degree_matrix(self, rtype: str = "array") -> Any:
        """Creates a degree matrix from a Graph datastructure.

        Parameters
        ----------
        rtype
            Format of the result.

        Returns
        -------
        array_like
            Constructed degree matrix.

        """
        from compas.matrices import degree_matrix

        node_index = self.node_index()
        adjacency = [[node_index[nbr] for nbr in self.neighbors(key)] for key in self.nodes()]
        return degree_matrix(adjacency, rtype=rtype)

    def laplacian_matrix(self, normalize: bool = False, rtype: str = "array") -> Any:
        """Creates a Laplacian matrix from a Graph datastructure.

        Parameters
        ----------
        normalize
            If True, normalize the entries such that the value on the diagonal is 1.
        rtype
            Format of the result.

        Returns
        -------
        array_like
            Constructed Laplacian matrix.

        Notes
        -----
        ``d = L.dot(xyz)`` is currently a vector that points from the centroid to the node.
        Therefore ``c = xyz - d``. By changing the signs in the laplacian, the dsiplacement
        vectors could be used in a more natural way ``c = xyz + d``.

        """
        from compas.matrices import laplacian_matrix

        node_index = self.node_index()
        edges = [(node_index[u], node_index[v]) for u, v in self.edges()]
        return laplacian_matrix(edges, normalize=normalize, rtype=rtype)
