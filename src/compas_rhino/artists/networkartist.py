from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from functools import partial
import compas_rhino
from compas_rhino.artists._artist import BaseArtist
from compas.geometry import centroid_points
from compas.utilities import color_to_colordict


colordict = partial(color_to_colordict, colorformat='rgb', normalize=False)


__all__ = ['NetworkArtist']


class NetworkArtist(BaseArtist):
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
    color_nodes : 3-tuple
        Default color of the nodes.
    color_edges : 3-tuple
        Default color of the edges.

    """

    def __init__(self, network, layer=None):
        super(NetworkArtist, self).__init__()
        self._network = None
        self._node_xyz = None
        self.network = network
        self.layer = layer
        self.color_nodes = (255, 255, 255)
        self.color_edges = (0, 0, 0)

    @property
    def network(self):
        return self._network

    @network.setter
    def network(self, network):
        self._network = network
        self._node_xyz = None

    @property
    def node_xyz(self):
        """dict:
        The view coordinates of the network nodes.
        The view coordinates default to the actual node coordinates.
        """
        if not self._node_xyz:
            return {node: self.network.node_attributes(node, 'xyz') for node in self.network.nodes()}
        return self._node_xyz

    @node_xyz.setter
    def node_xyz(self, node_xyz):
        self._node_xyz = node_xyz

    # ==========================================================================
    # clear
    # ==========================================================================

    def clear_by_name(self):
        """Clear all objects in the "namespace" of the associated network."""
        guids = compas_rhino.get_objects(name="{}.*".format(self.network.name))
        compas_rhino.delete_objects(guids, purge=True)

    def clear_layer(self):
        """Clear the main layer of the artist."""
        if self.layer:
            compas_rhino.clear_layer(self.layer)

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

    def draw_nodes(self, nodes=None, color=None):
        """Draw a selection of nodes.

        Parameters
        ----------
        nodes : list, optional
            A list of nodes to draw.
            Default is ``None``, in which case all nodes are drawn.
        color : 3-tuple or dict of 3-tuples, optional
            The color specififcation for the nodes.
            The default color is ``(255, 255, 255)``.

        Returns
        -------
        list
            The GUIDs of the created Rhino objects.

        """
        node_xyz = self.node_xyz
        nodes = nodes or list(self.network.nodes())
        node_color = colordict(color, nodes, default=self.color_nodes)
        points = []
        for node in nodes:
            points.append({
                'pos': node_xyz[node],
                'name': "{}.node.{}".format(self.network.name, node),
                'color': node_color[node]})
        return compas_rhino.draw_points(points, layer=self.layer, clear=False, redraw=False)

    def draw_edges(self, edges=None, color=None):
        """Draw a selection of edges.

        Parameters
        ----------
        edges : list, optional
            A list of edges to draw.
            The default is ``None``, in which case all edges are drawn.
        color : 3-tuple or dict of 3-tuple, optional
            The color specififcation for the edges.
            The default color is ``(0, 0, 0)``.

        Returns
        -------
        list
            The GUIDs of the created Rhino objects.

        """
        node_xyz = self.node_xyz
        edges = edges or list(self.network.edges())
        edge_color = colordict(color, edges, default=self.color_edges)
        lines = []
        for edge in edges:
            lines.append({
                'start': node_xyz[edge[0]],
                'end': node_xyz[edge[1]],
                'color': edge_color[edge],
                'name': "{}.edge.{}-{}".format(self.network.name, *edge)})
        return compas_rhino.draw_lines(lines, layer=self.layer, clear=False, redraw=False)

    # ==========================================================================
    # draw labels
    # ==========================================================================

    def draw_nodelabels(self, text=None, color=None):
        """Draw labels for a selection nodes.

        Parameters
        ----------
        text : dict, optional
            A dictionary of node labels as node-text pairs.
            The default value is ``None``, in which case every node will be labelled with its key.
        color : 3-tuple or dict of 3-tuple, optional
            The color sepcification of the labels.
            The default color is the same as the default color of the nodes.

        Returns
        -------
        list
            The GUIDs of the created Rhino objects.

        """
        if not text or text == 'key':
            node_text = {node: str(node) for node in self.network.nodes()}
        elif text == 'index':
            node_text = {node: str(index) for index, node in enumerate(self.network.nodes())}
        elif isinstance(text, dict):
            node_text = text
        else:
            raise NotImplementedError
        node_xyz = self.node_xyz
        node_color = colordict(color, node_text.keys(), default=self.color_nodes)
        labels = []
        for node in node_text:
            labels.append({
                'pos': node_xyz[node],
                'name': "{}.nodelabel.{}".format(self.network.name, node),
                'color': node_color[node],
                'text': node_text[node]})
        return compas_rhino.draw_labels(labels, layer=self.layer, clear=False, redraw=False)

    def draw_edgelabels(self, text=None, color=None):
        """Draw labels for a selection of edges.

        Parameters
        ----------
        text : dict, optional
            A dictionary of edgelabels as edge-text pairs.
            The default value is ``None``, in which case every edge will be labelled with its key.
        color : 3-tuple or dict of 3-tuple, optional
            The color sepcification of the labels.
            The default color is the same as the default color of the edges.

        Returns
        -------
        list
            The GUIDs of the created Rhino objects.

        """
        if text is None:
            edge_text = {edge: "{}-{}".format(*edge) for edge in self.network.edges()}
        elif isinstance(text, dict):
            edge_text = text
        else:
            raise NotImplementedError
        node_xyz = self.node_xyz
        edge_color = colordict(color, edge_text.keys(), default=self.color_edges)
        labels = []
        for edge in edge_text:
            labels.append({
                'pos': centroid_points([node_xyz[edge[0]], node_xyz[edge[1]]]),
                'name': "{}.edgelabel.{}-{}".format(self.network.name, *edge),
                'color': edge_color[edge],
                'text': edge_text[edge]})
        return compas_rhino.draw_labels(labels, layer=self.layer, clear=False, redraw=False)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
