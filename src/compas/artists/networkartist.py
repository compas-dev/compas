from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from abc import abstractmethod

from compas.utilities import is_color_rgb
from .artist import Artist


class NetworkArtist(Artist):
    """Artist for drawing network data structures.

    Parameters
    ----------
    network : :class:`compas.datastructures.Network`
        A COMPAS network.

    Class Attributes
    ----------------
    default_nodecolor : tuple
        The default color for nodes that do not have a specified color.
    default_edgecolor : tuple
        The default color for edges that do not have a specified color.

    Attributes
    ----------
    network : :class:`compas.datastructures.Network`
        The COMPAS network associated with the artist.
    nodes : list
        The list of nodes to draw.
        Default is a list of all nodes of the network.
    edges : list
        The list of edges to draw.
        Default is a list of all edges of the network.
    node_xyz : dict[int, tuple(float, float, float)]
        Mapping between nodes and their view coordinates.
        The default view coordinates are the actual coordinates of the nodes of the network.
    node_color : dict[int, tuple(int, int, int)]
        Mapping between nodes and RGB color values.
        The colors have to be integer tuples with values in the range ``0-255``.
        Missing nodes get the default node color (``MeshArtist.default_nodecolor``).
    node_text : dict[int, str]
        Mapping between nodes and text labels.
        Missing nodes are labelled with the corresponding node identifiers.
    edge_color : dict[tuple(int, int), tuple(int, int, int)]
        Mapping between edges and RGB color values.
        The colors have to be integer tuples with values in the range ``0-255``.
        Missing edges get the default edge color (``MeshArtist.default_edgecolor``).
    edge_text : dict[tuple(int, int), str]
        Mapping between edges and text labels.
        Missing edges are labelled with the corresponding edge identifiers.

    """

    default_nodecolor = (1, 1, 1)
    default_edgecolor = (0, 0, 0)

    def __init__(self, network, **kwargs):
        super(NetworkArtist, self).__init__(**kwargs)
        self._network = None
        self._nodes = None
        self._edges = None
        self._node_xyz = None
        self._node_color = None
        self._edge_color = None
        self._node_text = None
        self._edge_text = None
        self.network = network

    @property
    def network(self):
        return self._network

    @network.setter
    def network(self, network):
        self._network = network
        self._node_xyz = None

    @property
    def nodes(self):
        if self._nodes is None:
            self._nodes = list(self.network.nodes())
        return self._nodes

    @nodes.setter
    def nodes(self, nodes):
        self._nodes = nodes

    @property
    def edges(self):
        if self._edges is None:
            self._edges = list(self.network.edges())
        return self._edges

    @edges.setter
    def edges(self, edges):
        self._edges = edges

    @property
    def node_xyz(self):
        if not self._node_xyz:
            return {node: self.network.node_attributes(node, 'xyz') for node in self.network.nodes()}
        return self._node_xyz

    @node_xyz.setter
    def node_xyz(self, node_xyz):
        self._node_xyz = node_xyz

    @property
    def node_color(self):
        if not self._node_color:
            self._node_color = {node: self.default_nodecolor for node in self.network.nodes()}
        return self._node_color

    @node_color.setter
    def node_color(self, node_color):
        if isinstance(node_color, dict):
            self._node_color = node_color
        elif is_color_rgb(node_color):
            self._node_color = {node: node_color for node in self.network.nodes()}

    @property
    def edge_color(self):
        if not self._edge_color:
            self._edge_color = {edge: self.default_edgecolor for edge in self.network.edges()}
        return self._edge_color

    @edge_color.setter
    def edge_color(self, edge_color):
        if isinstance(edge_color, dict):
            self._edge_color = edge_color
        elif is_color_rgb(edge_color):
            self._edge_color = {edge: edge_color for edge in self.network.edges()}

    @property
    def node_text(self):
        if not self._node_text:
            self._node_text = {node: str(node) for node in self.network.nodes()}
        return self._node_text

    @node_text.setter
    def node_text(self, text):
        if text == 'key':
            self._node_text = {node: str(node) for node in self.network.nodes()}
        elif text == 'index':
            self._node_text = {node: str(index) for index, node in enumerate(self.network.nodes())}
        elif isinstance(text, dict):
            self._node_text = text

    @property
    def edge_text(self):
        if not self._edge_text:
            self._edge_text = {edge: "{}-{}".format(*edge) for edge in self.network.edges()}
        return self._edge_text

    @edge_text.setter
    def edge_text(self, text):
        if text == 'key':
            self._edge_text = {edge: "{}-{}".format(*edge) for edge in self.network.edges()}
        elif text == 'index':
            self._edge_text = {edge: str(index) for index, edge in enumerate(self.network.edges())}
        elif isinstance(text, dict):
            self._edge_text = text

    @abstractmethod
    def draw_nodes(self, nodes=None, color=None, text=None):
        """Draw the nodes of the network.

        Parameters
        ----------
        nodes : list, optional
            The nodes to include in the drawing.
            Default is all nodes.
        color : tuple or dict, optional
            The color of the nodes,
            as either a single color to be applied to all nodes,
            or a color dict, mapping specific nodes to specific colors.
        text : dict, optional
            The text labels for the nodes
            as a text dict, mapping specific nodes to specific text labels.
        """
        raise NotImplementedError

    @abstractmethod
    def draw_edges(self, edges=None, color=None, text=None):
        """Draw the edges of the mesh.

        Parameters
        ----------
        edges : list, optional
            The edges to include in the drawing.
            Default is all edges.
        color : tuple or dict, optional
            The color of the edges,
            as either a single color to be applied to all edges,
            or a color dict, mapping specific edges to specific colors.
        text : dict, optional
            The text labels for the edges
            as a text dict, mapping specific edges to specific text labels.
        """
        raise NotImplementedError

    @abstractmethod
    def clear_nodes(self):
        raise NotImplementedError

    @abstractmethod
    def clear_edges(self):
        raise NotImplementedError
