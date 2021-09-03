from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.data import Data
from compas.datastructures import Datastructure
from compas.datastructures.attributes import NodeAttributeView
from compas.datastructures.attributes import EdgeAttributeView


class StrictAttributesError(Exception):
    pass


class NodeError(Exception):
    pass


class EdgeError(Exception):
    pass


class Nodes(Data):

    def __init__(self, default_attributes=None, strict=False):
        super(Nodes, self).__init__()
        self._default_attributes = default_attributes or {}
        self._strict = strict
        self._nodes = {}
        self._max = -1

    def __str__(self):
        return "MultiGraph Nodes Object with {} items".format(len(self))

    def __len__(self):
        return len(self._nodes)

    def __iter__(self):
        for node in self._nodes:
            yield node

    def __getitem__(self, node):
        if node not in self._nodes:
            raise NodeError("The Nodes object doesn't contain {}".format(node))
        return NodeAttributeView(self._default_attributes, self._nodes[node])

    def __call__(self, data=False):
        for node in self._nodes:
            if not data:
                yield node
            else:
                yield node, NodeAttributeView(self._default_attributes, self._nodes[node])

    def add(self, key=None, **kwargs):
        """Add a node."""
        if key is None:
            key = self._max + 1
            self._max += 1
        elif isinstance(key, int):
            if key <= self._max:
                key += 1
            self._max = key
        if self._strict:
            attr = {kwargs[name] for name in self._default_attributes if name in kwargs}
        else:
            attr = kwargs
        self._nodes[key] = attr
        return key

    def attribute(self, name, nodes=None):
        """Retrieve a named data attribute from a (selection of) nodes in the container.

        Parameters
        ----------

        """
        if not nodes:
            nodes = self._nodes
        if self._strict:
            if name not in self._default_attributes:
                raise StrictAttributesError("Attribute {} does not have a default (strict mode).".format(name))
        return [self._nodes[node].get(name, self._default_attributes.get(name)) for node in nodes]

    def attributes(self, names, nodes=None):
        if not nodes:
            nodes = self._nodes
        if self._strict:
            if any(name not in self._default_attributes for name in names):
                raise StrictAttributesError("At least on of these attributes {} does not have a default (strict mode).".format(names))
        return [[self._nodes[node].get(name, self._default_attributes.get(name)) for name in names] for node in nodes]


class Edges(Data):

    def __init__(self, default_attributes=None, strict=False):
        super(Edges, self).__init__()
        self._default_attributes = default_attributes or {}
        self._strict = strict
        self._edges = {}

    def __str__(self):
        return "MultiGraph Edges Object with {} items".format(len(self))

    def __len__(self):
        return len(self._edges)

    def __getitem__(self, edge):
        u, v = edge
        if u not in self._edges:
            raise EdgeError("The Edges object doesn't contain node {} of edge {}".format(u, edge))
        if v not in self._edges[u]:
            raise EdgeError("The Edges object doesn't contain edge {}".format(edge))
        views = []
        for attr in self._edges[u][v]:
            view = EdgeAttributeView(self._default_attributes, attr)
            views.append(view)
        return views

    def __call__(self, data=False):
        for u in self._edges:
            for v in self._edges[u]:
                edge = u, v
                if not data:
                    yield edge
                else:
                    views = []
                    for attr in self._edges[u][v]:
                        view = EdgeAttributeView(self._default_attributes, attr)
                        views.append(view)
                    yield edge, views

    def add(self, u, v, **kwargs):
        if u not in self._edges:
            self._edges[u] = {}
        if v not in self._edges[u]:
            self._edges[u][v] = []
        if self._strict:
            attr = {kwargs[name] for name in self._default_attributes if name in kwargs}
        else:
            attr = kwargs
        index = len(self._edges[u][v])
        self._edges[u][v].append(attr)
        return index


class MultiGraph(Datastructure):
    """Data structure for graphs with multiple edges between pairs of nodes.

    Parameters
    ----------
    name: str, optional
        The name of the graph.
    default_node_attributes: dict, optional
        The default data attributes for the nodes of the graph.
    default_edge_attributes: dict, optional
        The default data attributes for the edges of the graph.
    strict: bool, optional
        Flag indicating that only data attributes with a default can be stored on the nodes and edges.
        Default is ``False``.

    Attributes
    ----------
    nodes: Nodes
        A container object for the nodes of the graph.
    edges: Edges
        A container object for the edges of the graph.

    Examples
    --------
    >>> graph = MultiGraph(default_node_attributes={'x': 0.0, 'y': 0.0})
    >>> a = graph.add_node()
    >>> b = graph.add_node(x=1.0)
    >>> graph.add_edge(a, b)

    Display general information.

    >>> graph
    "MultiGraph with 2 nodes and 1 edges"

    Access nodes and node data.

    >>> for node in graph.nodes:
    ...     print(graph.nodes[node])
    ...
    {'x': 0.0, 'y': 0.0}
    {'x': 1.0, 'y': 0.0}

    >>> graph.nodes.attribute('x')
    [0.0, 1.0]

    >>> graph.nodes[a]
    {'x': 0.0, 'y': 0.0}

    >>> graph.nodes[a]['x']
    0.0
    """

    def __init__(self, name=None, default_node_attributes=None, default_edge_attributes=None, strict=False):
        super(MultiGraph, self).__init__(name=name)
        self._nodes = Nodes(default_attributes=default_node_attributes, strict=strict)
        self._edges = Edges(default_attributes=default_edge_attributes, strict=strict)

    def __str__(self):
        return "MultiGraph with {} nodes and {} edges.".format(len(self.nodes), len(self.edges))

    @property
    def nodes(self):
        return self._nodes

    @property
    def edges(self):
        return self._edges

    def add_node(self, key=None, **kwargs):
        """Add a node."""
        return self.nodes.add(key=key, **kwargs)

    def add_edge(self, u, v, **kwargs):
        """Add a edge."""
        return self.edges.add(u, v, **kwargs)
