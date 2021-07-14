from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas.geometry import centroid_points
from compas.utilities import is_color_rgb

from ._artist import Artist


__all__ = ['NetworkArtist']


class NetworkArtist(Artist):
    """Artist for drawing network data structures.

    Parameters
    ----------
    network : :class:`compas.datastructures.Network`
        A COMPAS network.
    layer : str, optional
        The parent layer of the network.

    Attributes
    ----------
    network : :class:`compas.datastructures.Network`
        The COMPAS network associated with the artist.
    layer : str
        The layer in which the network should be contained.
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

    default_nodecolor = (255, 255, 255)
    default_edgecolor = (0, 0, 0)

    def __init__(self, network, layer=None):
        super(NetworkArtist, self).__init__(network, layer=layer)
        self._node_xyz = None
        self._node_color = None
        self._edge_color = None
        self._node_text = None
        self._edge_text = None

    @property
    def network(self):
        return self.item

    @network.setter
    def network(self, network):
        self.item = network
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
            self._node_color = {node: self.artist.default_nodecolor for node in self.network.nodes()}
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
            self._edge_color = {edge: self.artist.default_edgecolor for edge in self.network.edges()}
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

    # ==========================================================================
    # clear
    # ==========================================================================

    def clear_by_name(self):
        """Clear all objects in the "namespace" of the associated network."""
        guids = compas_rhino.get_objects(name="{}.*".format(self.network.name))
        compas_rhino.delete_objects(guids, purge=True)

    # ==========================================================================
    # draw
    # ==========================================================================

    def draw(self):
        """Draw the network using the chosen visualisation settings.

        Returns
        -------
        list
            The GUIDs of the created Rhino objects.
        """
        guids = self.draw_nodes()
        guids += self.draw_edges()
        return guids

    def draw_nodes(self):
        """Draw a selection of nodes.

        Returns
        -------
        list
            The GUIDs of the created Rhino objects.
        """
        node_xyz = self.node_xyz
        node_color = self.node_color
        points = []
        for node in self.nodes:
            points.append({
                'pos': node_xyz[node],
                'name': "{}.node.{}".format(self.network.name, node),
                'color': node_color.get(node, self.default_nodecolor)
            })
        return compas_rhino.draw_points(points, layer=self.layer, clear=False, redraw=False)

    def draw_edges(self):
        """Draw a selection of edges.

        Returns
        -------
        list
            The GUIDs of the created Rhino objects.
        """
        node_xyz = self.node_xyz
        edge_color = self.edge_color
        lines = []
        for edge in self.edges:
            lines.append({
                'start': node_xyz[edge[0]],
                'end': node_xyz[edge[1]],
                'color': edge_color.get(edge, self.default_edgecolor),
                'name': "{}.edge.{}-{}".format(self.network.name, *edge)
            })
        return compas_rhino.draw_lines(lines, layer=self.layer, clear=False, redraw=False)

    # ==========================================================================
    # draw labels
    # ==========================================================================

    def draw_nodelabels(self):
        """Draw labels for a selection nodes.

        Returns
        -------
        list
            The GUIDs of the created Rhino objects.
        """
        node_xyz = self.node_xyz
        node_text = self.node_text
        node_color = self.node_color
        labels = []
        for node in node_text:
            labels.append({
                'pos': node_xyz[node],
                'name': "{}.nodelabel.{}".format(self.network.name, node),
                'color': node_color.get(node, self.default_nodecolor),
                'text': node_text[node]
            })
        return compas_rhino.draw_labels(labels, layer=self.layer, clear=False, redraw=False)

    def draw_edgelabels(self):
        """Draw labels for a selection of edges.

        Returns
        -------
        list
            The GUIDs of the created Rhino objects.
        """
        node_xyz = self.node_xyz
        edge_text = self.edge_text
        edge_color = self.edge_color
        labels = []
        for edge in edge_text:
            labels.append({
                'pos': centroid_points([node_xyz[edge[0]], node_xyz[edge[1]]]),
                'name': "{}.edgelabel.{}-{}".format(self.network.name, *edge),
                'color': edge_color.get(edge, self.default_edgecolor),
                'text': edge_text[edge]
            })
        return compas_rhino.draw_labels(labels, layer=self.layer, clear=False, redraw=False)
