from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rhino.artists.base import BaseArtist

from compas.utilities import color_to_colordict


__all__ = ['NetworkArtist']


class NetworkArtist(BaseArtist):
    """A network artist defines functionality for visualising COMPAS networks in Rhino.

    Parameters
    ----------
    network : :class:`compas.datastructures.Network`
        A COMPAS network.
    layer : str, optional
        The parent layer of the network.
    settings : dict, optional
        A dict with custom visualisation settings.

    Attributes
    ----------
    network : :class:`compas.datastructures.Network`
        The COMPAS network associated with the artist.
    layer : str
        The layer in which the network should be contained.
    settings : dict
        Default settings for color, scale, tolerance, ...

    """

    def __init__(self, network, layer=None, settings=None):
        super(NetworkArtist, self).__init__()
        self._guid_node = {}
        self._guid_edge = {}
        self.network = network
        self.layer = layer
        self.settings = {
            'color.nodes': (255, 255, 255),
            'color.edges': (0, 0, 0),
            'show.nodes': True,
            'show.edges': True,
            'show.nodelabels': False,
            'show.edgelabels': False
        }
        if settings:
            self.settings.update(settings)

    @property
    def guid_node(self):
        if not self._guid_node:
            self._guid_node = {}
        return self._guid_node

    @guid_node.setter
    def guid_node(self, values):
        self._guid_node = dict(values)

    @property
    def guid_edge(self):
        if not self._guid_edge:
            self._guid_edge = {}
        return self._guid_edge

    @guid_edge.setter
    def guid_edge(self, values):
        self._guid_edge = dict(values)

    # ==========================================================================
    # clear
    # ==========================================================================

    def clear(self):
        guids_nodes = list(self.guid_node.keys())
        guids_edges = list(self.guid_edge.keys())
        guids = guids_nodes + guids_edges
        compas_rhino.delete_objects(guids, purge=True)
        self._guid_node = {}
        self._guid_edge = {}

    def clear_layer(self):
        """Clear the main layer of the artist."""
        if self.layer:
            compas_rhino.clear_layer(self.layer)
        else:
            compas_rhino.clear_current_layer()

    # ==========================================================================
    # components
    # ==========================================================================

    def draw(self, settings=None):
        """Draw the network using the chosen visualisation settings.

        Parameters
        ----------
        settings : dict, optional
            Dictionary of visualisation settings that will be merged with the settings of the artist.

        Returns
        -------
        list
            The GUIDs of the created Rhino objects.

        Notes
        -----
        This method will attempt to clear all previously drawn elements by this artist.
        However, clearing the artist layer has to be done explicitly with a call to ``NetworkArtist.clear_layer``.

        """
        self.clear()
        if not settings:
            settings = {}
        self.settings.update(settings)
        if self.settings['show.nodes']:
            self.draw_nodes()
            if self.settings['show.nodelabels']:
                self.draw_nodelabels()
        if self.settings['show.edges']:
            self.draw_edges()
            if self.settings['show.edgelabels']:
                self.draw_edgelabels()
        return self.guids

    def draw_nodes(self, keys=None, color=None):
        """Draw a selection of nodes.

        Parameters
        ----------
        keys : list
            A list of node keys identifying which nodes to draw.
            Default is ``None``, in which case all nodes are drawn.
        color : str, tuple, dict
            The color specififcation for the nodes.
            Colors should be specified in the form of a string (hex colors) or as a tuple of RGB components.
            To apply the same color to all nodes, provide a single color specification.
            Individual colors can be assigned using a dictionary of key-color pairs.
            Missing keys will be assigned the default node color (``self.settings['color.nodes']``).
            The default is ``None``, in which case all nodes are assigned the default node color.

        Returns
        -------
        list
            The GUIDs of the created Rhino objects.

        """
        nodes = keys or list(self.network.nodes())
        node_color = color_to_colordict(color,
                                        nodes,
                                        default=self.settings['color.nodes'],
                                        colorformat='rgb',
                                        normalize=False)
        points = []
        for node in nodes:
            points.append({
                'pos': self.network.node_coordinates(node),
                'name': "{}.node.{}".format(self.network.name, node),
                'color': node_color[node]})

        guids = compas_rhino.draw_points(points, layer=self.layer, clear=False, redraw=False)
        self.guid_node = zip(guids, nodes)
        return guids

    def draw_edges(self, keys=None, color=None):
        """Draw a selection of edges.

        Parameters
        ----------
        keys : list
            A list of edge keys (as uv pairs) identifying which edges to draw.
            The default is ``None``, in which case all edges are drawn.
        color : str, tuple, dict
            The color specififcation for the edges.
            Colors should be specified in the form of a string (hex colors) or as a tuple of RGB components.
            To apply the same color to all edges, provide a single color specification.
            Individual colors can be assigned using a dictionary of key-color pairs.
            Missing keys will be assigned the default edge color (``self.settings['color.edges']``).
            The default is ``None``, in which case all edges are assigned the default edge color.

        Returns
        -------
        list
            The GUIDs of the created Rhino objects.

        """
        keys = keys or list(self.network.edges())
        colordict = color_to_colordict(color,
                                       keys,
                                       default=self.settings['color.edges'],
                                       colorformat='rgb',
                                       normalize=False)
        lines = []
        for u, v in keys:
            lines.append({
                'start': self.network.node_coordinates(u),
                'end': self.network.node_coordinates(v),
                'color': colordict[(u, v)],
                'name': "{}.edge.{}-{}".format(self.network.name, u, v)})

        guids = compas_rhino.draw_lines(lines, layer=self.layer, clear=False, redraw=False)
        self.guids += guids
        return guids

    # ==========================================================================
    # labels
    # ==========================================================================

    def draw_nodelabels(self, text=None, color=None):
        """Draw labels for a selection nodes.

        Parameters
        ----------
        text : dict
            A dictionary of node labels as key-text pairs.
            The default value is ``None``, in which case every node will be labelled with its key.
        color : str, tuple, dict
            The color sepcification of the labels.
            String values are interpreted as hex colors.
            Tuples are interpreted as RGB component specifications.
            If a dictionary of specififcations is provided,
            the keys of the should refer to node keys and the values should be color specifications in the form of strings or tuples.
            The default value is ``None``, in which case the labels are assigned the default node color (``self.settings['color.nodes']``).

        Returns
        -------
        list
            The GUIDs of the created Rhino objects.

        """
        if text is None:
            textdict = {key: str(key) for key in self.network.nodes()}
        elif isinstance(text, dict):
            textdict = text
        elif text == 'key':
            textdict = {key: str(key) for key in self.network.nodes()}
        elif text == 'index':
            textdict = {key: str(index) for index, key in enumerate(self.network.nodes())}
        else:
            raise NotImplementedError

        colordict = color_to_colordict(color,
                                       textdict.keys(),
                                       default=self.settings['color.nodes'],
                                       colorformat='rgb',
                                       normalize=False)
        labels = []
        for key, text in iter(textdict.items()):
            labels.append({
                'pos': self.network.node_coordinates(key),
                'name': "{}.nodelabel.{}".format(self.network.name, key),
                'color': colordict[key],
                'text': textdict[key]})

        guids = compas_rhino.draw_labels(labels, layer=self.layer, clear=False, redraw=False)
        self.guids += guids
        return guids

    def draw_edgelabels(self, text=None, color=None):
        """Draw labels for a selection of edges.

        Parameters
        ----------
        text : dict
            A dictionary of edge labels as key-text pairs.
            The default value is ``None``, in which case every edge will be labelled with its key.
        color : str, tuple, dict
            The color sepcification of the labels.
            String values are interpreted as hex colors.
            Tuples are interpreted as RGB component specifications.
            Individual colors can be assigned using a dictionary of key-color pairs.
            Missing keys will be assigned the default face color (``self.settings['color.edges']``).
            The default is ``None``, in which case all edges are assigned the default edge color.

        Returns
        -------
        list
            The GUIDs of the created Rhino objects.

        """
        if text is None:
            textdict = {(u, v): "{}-{}".format(u, v) for u, v in self.network.edges()}
        elif isinstance(text, dict):
            textdict = text
        else:
            raise NotImplementedError

        colordict = color_to_colordict(color,
                                       textdict.keys(),
                                       default=self.settings['color.edges'],
                                       colorformat='rgb',
                                       normalize=False)
        labels = []
        for (u, v), text in iter(textdict.items()):
            labels.append({
                'pos': self.network.edge_midpoint(u, v),
                'name': "{}.edgelabel.{}-{}".format(self.network.name, u, v),
                'color': colordict[(u, v)],
                'text': textdict[(u, v)]})

        guids = compas_rhino.draw_labels(labels, layer=self.layer, clear=False, redraw=False)
        self.guids += guids
        return guids


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
