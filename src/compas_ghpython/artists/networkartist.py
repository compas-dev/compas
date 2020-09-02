from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_ghpython

from compas_ghpython.artists._artist import BaseArtist
from compas.utilities import color_to_colordict as colordict


__all__ = ['NetworkArtist']


class NetworkArtist(BaseArtist):
    """A network artist defines functionality for visualising COMPAS networks in GhPython.

    Parameters
    ----------
    network : compas.datastructures.Network
        A COMPAS network.

    Attributes
    ----------
    network : :class:`compas.datastructures.Network`
        The COMPAS network associated with the artist.
    settings : dict
        Default settings for color of network components.

    """

    def __init__(self, network):
        self._network = None
        self.network = network
        self.settings = {
            'color.nodes': (255, 255, 255),
            'color.edges': (0, 0, 0),
        }

    @property
    def network(self):
        """compas.datastructures.Network: The network that should be painted."""
        return self._network

    @network.setter
    def network(self, network):
        self._network = network

    def draw(self):
        """For networks (and data structures in general), a main draw function does not exist.
        Instead, you should use the drawing functions for the various components of the mesh:

        * ``draw_nodes``
        * ``draw_edges``
        """
        raise NotImplementedError

    # ==============================================================================
    # components
    # ==============================================================================

    def draw_nodes(self, nodes=None, color=None):
        """Draw a selection of nodes.

        Parameters
        ----------
        nodes: list, optional
            The selection of nodes that should be drawn.
            Default is ``None``, in which case all nodes are drawn.
        color: rgb-tuple or dict of rgb-tuple, optional
            The color specififcation for the nodes.
            The default is defined in the class settings.

        Returns
        -------
        list of :class:`Rhino.Geometry.Point3d`

        """
        nodes = nodes or list(self.network.nodes())
        node_color = colordict(color, nodes, default=self.settings['color.nodes'], colorformat='rgb', normalize=False)
        points = []
        for node in nodes:
            points.append({
                'pos': self.network.node_coordinates(node),
                'name': "{}.node.{}".format(self.network.name, node),
                'color': node_color[node]})
        return compas_ghpython.draw_points(points)

    def draw_edges(self, edges=None, color=None):
        """Draw a selection of edges.

        Parameters
        ----------
        edges : list, optional
            A list of edges to draw.
            The default is ``None``, in which case all edges are drawn.
        color : rgb-tuple or dict of rgb-tuple, optional
            The color specififcation for the edges.
            The default color is defined in the class settings.

        Returns
        -------
        list of :class:`Rhino.Geometry.Line`

        """
        edges = edges or list(self.network.edges())
        edge_color = colordict(color, edges, default=self.settings['color.edges'], colorformat='rgb', normalize=False)
        lines = []
        for edge in edges:
            start, end = self.network.edge_coordinates(*edge)
            lines.append({
                'start': start,
                'end': end,
                'color': edge_color[edge],
                'name': "{}.edge.{}-{}".format(self.network.name, *edge)})
        return compas_ghpython.draw_lines(lines)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
