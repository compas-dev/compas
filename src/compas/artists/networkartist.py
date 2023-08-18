from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from abc import abstractmethod

from compas.colors import Color
from .artist import Artist
from .descriptors.colordict import ColorDictAttribute


class NetworkArtist(Artist):
    """Artist for drawing network data structures.

    Parameters
    ----------
    network : :class:`~compas.datastructures.Network`
        A COMPAS network.

    Attributes
    ----------
    network : :class:`~compas.datastructures.Network`
        The COMPAS network associated with the artist.
    default_nodesize : float
        The default size for nodes that do not have a specified size.
    default_edgewidth : float
        The default width for edges that do not have a specified width.
    node_xyz : dict[hashable, list[float]]
        Mapping between nodes and their view coordinates.
        The default view coordinates are the actual coordinates of the nodes of the network.
    node_color : :class:`~compas.colors.ColorDict`
        Mapping between nodes and RGB color values.
    edge_color : :class:`~compas.colors.ColorDict`
        Mapping between edges and colors.
    node_text : dict[hashable, str]
        Mapping between nodes and text labels.
    edge_text : dict[tuple[hashable, hashable], str]
        Mapping between edges and text labels.
    node_size : dict[hashable, float]
        Mapping between nodes and sizes.
        Missing nodes get assigned the default node size :attr:`default_nodesize`.
    edge_width : dict[tuple[hashable, hashable], float]
        Mapping between edges and line widths.
        Missing edges get assigned the default edge width :attr:`default_edgewidth`.

    See Also
    --------
    :class:`compas.artists.MeshArtist`
    :class:`compas.artists.VolMeshArtist`

    """

    node_color = ColorDictAttribute(default=Color.white())
    edge_color = ColorDictAttribute(default=Color.black())

    default_nodesize = 5
    default_edgewidth = 1.0

    def __init__(self, network, **kwargs):
        super(NetworkArtist, self).__init__(**kwargs)
        self._network = None
        self._node_xyz = None
        self._node_text = None
        self._edge_text = None
        self._edge_width = None
        # collect items that have been drawn?
        self._nodecollection = None
        self._edgecollection = None
        self._nodelabelcollection = None
        self._edgelabelcollection = None
        # the network of the artist
        self.network = network

    @property
    def network(self):
        return self._network

    @network.setter
    def network(self, network):
        self._network = network
        self._node_xyz = None

    @property
    def node_xyz(self):
        if not self._node_xyz:
            return {node: self.network.node_coordinates(node) for node in self.network.nodes()}  # type: ignore
        return self._node_xyz

    @node_xyz.setter
    def node_xyz(self, node_xyz):
        self._node_xyz = node_xyz

    @property
    def node_size(self):
        if not self._node_size:
            self._node_size = {node: self.default_nodesize for node in self.network.nodes()}  # type: ignore
        return self._node_size

    @node_size.setter
    def node_size(self, nodesize):
        if isinstance(nodesize, dict):
            self._node_size = nodesize
        elif isinstance(nodesize, (int, float)):
            self._node_size = {node: nodesize for node in self.network.nodes()}  # type: ignore

    @property
    def node_text(self):
        if not self._node_text:
            self._node_text = {node: str(node) for node in self.network.nodes()}  # type: ignore
        return self._node_text

    @node_text.setter
    def node_text(self, text):
        if text == "key":
            self._node_text = {node: str(node) for node in self.network.nodes()}  # type: ignore
        elif text == "index":
            self._node_text = {node: str(index) for index, node in enumerate(self.network.nodes())}  # type: ignore
        elif isinstance(text, dict):
            self._node_text = text

    @property
    def edge_text(self):
        if not self._edge_text:
            self._edge_text = {edge: "{}-{}".format(*edge) for edge in self.network.edges()}  # type: ignore
        return self._edge_text

    @edge_text.setter
    def edge_text(self, text):
        if text == "key":
            self._edge_text = {edge: "{}-{}".format(*edge) for edge in self.network.edges()}  # type: ignore
        elif text == "index":
            self._edge_text = {edge: str(index) for index, edge in enumerate(self.network.edges())}  # type: ignore
        elif isinstance(text, dict):
            self._edge_text = text

    @property
    def edge_width(self):
        if not self._edge_width:
            self._edge_width = {edge: self.default_edgewidth for edge in self.network.edges()}  # type: ignore
        return self._edge_width

    @edge_width.setter
    def edge_width(self, edgewidth):
        if isinstance(edgewidth, dict):
            self._edge_width = edgewidth
        elif isinstance(edgewidth, (int, float)):
            self._edge_width = {edge: edgewidth for edge in self.network.edges()}  # type: ignore

    @abstractmethod
    def draw_nodes(self, nodes=None, color=None, text=None):
        """Draw the nodes of the network.

        Parameters
        ----------
        nodes : list[int], optional
            The nodes to include in the drawing.
            Default is all nodes.
        color : tuple[float, float, float] | :class:`~compas.colors.Color` | dict[int, tuple[float, float, float] | :class:`~compas.colors.Color`], optional
            The color of the nodes,
            as either a single color to be applied to all nodes,
            or a color dict, mapping specific nodes to specific colors.
        text : dict[int, str], optional
            The text labels for the nodes
            as a text dict, mapping specific nodes to specific text labels.

        Returns
        -------
        list
            The identifiers of the objects representing the nodes in the visualization context.

        """
        raise NotImplementedError

    @abstractmethod
    def draw_edges(self, edges=None, color=None, text=None):
        """Draw the edges of the network.

        Parameters
        ----------
        edges : list[tuple[int, int]], optional
            The edges to include in the drawing.
            Default is all edges.
        color : tuple[float, float, float] | :class:`~compas.colors.Color` | dict[tuple[int, int], tuple[float, float, float] | :class:`~compas.colors.Color`], optional
            The color of the edges,
            as either a single color to be applied to all edges,
            or a color dict, mapping specific edges to specific colors.
        text : dict[tuple[int, int]], optional
            The text labels for the edges
            as a text dict, mapping specific edges to specific text labels.

        Returns
        -------
        list
            The identifiers of the objects representing the edges in the visualization context.

        """
        raise NotImplementedError

    @abstractmethod
    def clear_nodes(self):
        """Clear the nodes of the network.

        Returns
        -------
        None

        """
        raise NotImplementedError

    @abstractmethod
    def clear_edges(self):
        """Clear the edges of the network.

        Returns
        -------
        None

        """
        raise NotImplementedError

    def clear(self):
        """Clear the nodes and the edges of the network.

        Returns
        -------
        None

        """
        self.clear_nodes()
        self.clear_edges()
