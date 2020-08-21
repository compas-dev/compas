from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_ghpython

from compas_ghpython.artists._artist import BaseArtist
from compas.utilities import color_to_colordict


__all__ = ['NetworkArtist']


class NetworkArtist(BaseArtist):
    """A network artist defines functionality for visualising COMPAS networks in GhPython.

    Parameters
    ----------
    network : compas.datastructures.Network
        A COMPAS network.
    settings : dict, optional
        A dict with custom visualisation settings.

    Attributes
    ----------
    network : :class:`compas.datastructures.Network`
        The COMPAS network associated with the artist.
    settings : dict
        Default settings for color, scale, tolerance, ...

    """

    def __init__(self, network, settings=None):
        self._network = None
        self.network = network
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
    def network(self):
        """compas.datastructures.Network: The network that should be painted."""
        return self._network

    @network.setter
    def network(self, network):
        self._network = network

    def draw(self):
        """Draws the network using the current settings.

        Returns
        -------
        geometry : list

            * geometry[0]: list of :class:`Rhino.Geometry.Point3d` or `None`, if `self.settings['show.nodes']` is False.
            * geometry[1]: list of :class:`Rhino.Geometry.TextDot` or `None`, if `self.settings['show.nodelabels']` is False.
            * geometry[2]: list of :class:`Rhino.Geometry.Line` or `None`, if `self.settings['show.edges']` is False.
            * geometry[3]: list of :class:`Rhino.Geometry.TextDot` or `None`, if `self.settings['show.edgelabels']` is False.

        """
        geometry = [None, None, None, None]

        if self.settings['show.nodes']:
            geometry[0] = self.draw_nodes()
            if self.settings['show.nodelabels']:
                geometry[1] = self.draw_nodelabels()

        if self.settings['show.edges']:
            geometry[2] = self.draw_edges()
            if self.settings['show.edgelabels']:
                geometry[3] = self.draw_edgelabels()

        return geometry

    # ==============================================================================
    # components
    # ==============================================================================

    def draw_nodes(self, keys=None, color=None):
        """Draw a selection of nodes.

        Parameters
        ----------
        keys : list
            A list of node keys identifying which nodes to draw.
            Default is ``None``, in which case all nodes are drawn.
        color : str, tuple, dict
            The color specififcation for the nodes.
            Colors should be specified in the form of a string (hex colors) or
            as a tuple of RGB components.
            To apply the same color to all nodes, provide a single color
            specification. Individual colors can be assigned using a dictionary
            of key-color pairs. Missing keys will be assigned the default node
            color (``self.settings['color.nodes']``).
            The default is ``None``, in which case all nodes are assigned the
            default node color.

        Returns
        -------
        list of :class:`Rhino.Geometry.Point3d`

        """
        nodes = keys or list(self.network.nodes())
        colordict = color_to_colordict(color,
                                       nodes,
                                       default=self.settings['color.nodes'],
                                       colorformat='rgb',
                                       normalize=False)
        points = []
        for node in nodes:
            points.append({
                'pos': self.network.node_coordinates(node),
                'name': "{}.node.{}".format(self.network.name, node),
                'color': colordict[node]
            })
        return compas_ghpython.draw_points(points)

    def draw_edges(self, keys=None, color=None):
        """Draw a selection of edges.

        Parameters
        ----------
        keys : list
            A list of edge keys (as uv pairs) identifying which edges to draw.
            The default is ``None``, in which case all edges are drawn.
        color : str, tuple, dict
            The color specififcation for the edges.
            Colors should be specified in the form of a string (hex colors) or
            as a tuple of RGB components.
            To apply the same color to all edges, provide a single color
            specification. Individual colors can be assigned using a dictionary
            of key-color pairs. Missing keys will be assigned the default face
            color (``self.settings['edge.color']``).
            The default is ``None``, in which case all edges are assigned the
            default edge color.

        Returns
        -------
        list of :class:`Rhino.Geometry.Line`

        """
        edges = keys or list(self.network.edges())
        colordict = color_to_colordict(color,
                                       edges,
                                       default=self.settings['color.edges'],
                                       colorformat='rgb',
                                       normalize=False)
        lines = []
        for edge in edges:
            start, end = self.network.edge_coordinates(*edge)
            lines.append({
                'start': start,
                'end': end,
                'color': colordict[edge],
                'name': "{}.edge.{}-{}".format(self.network.name, *edge)
            })
        return compas_ghpython.draw_lines(lines)

    # ==============================================================================
    # labels
    # ==============================================================================

    def draw_nodelabels(self, text=None, color=None):
        """Draw labels for a selection nodes.

        Parameters
        ----------
        text : dict
            A dictionary of node labels as key-text pairs.
            The default value is ``None``, in which case every node will be labelled with its key.
        color : str, tuple, dict
            The color sepcification of the labels.
            String values are interpreted as hex colors (e.g. ``'#ff0000'`` for red).
            Tuples are interpreted as RGB component specifications (e.g. ``(255, 0, 0) for red``.
            If a dictionary of specififcations is provided, the keys of the
            should refer to node keys and the values should be color
            specifications in the form of strings or tuples.
            The default value is ``None``, in which case the labels are assigned
            the default node color (``self.settings['color.nodes']``).

        Returns
        -------
        list of :class:`Rhino.Geometry.Point3d`

        """
        if text is None:
            textdict = {key: str(key) for key in self.network.nodes()}
        elif isinstance(text, dict):
            textdict = text
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
                'text': textdict[key]
            })

        return compas_ghpython.draw_labels(labels)

    def draw_edgelabels(self, text=None, color=None):
        """Draw labels for a selection of edges.

        Parameters
        ----------
        text : dict
            A dictionary of edge labels as key-text pairs.
            The default value is ``None``, in which case every edge will be labelled with its key.
        color : str, tuple, dict
            The color sepcification of the labels.
            String values are interpreted as hex colors (e.g. ``'#ff0000'`` for red).
            Tuples are interpreted as RGB component specifications (e.g. ``(255, 0, 0) for red``.
            Individual colors can be assigned using a dictionary
            of key-color pairs. Missing keys will be assigned the default face
            color (``self.settings['edge.color']``).
            The default is ``None``, in which case all edges are assigned the
            default edge color.

        Returns
        -------
        list of :class:`Rhino.Geometry.Point3d`

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
                'text': textdict[(u, v)]
            })

        return compas_ghpython.draw_labels(labels)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
