from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from functools import partial
import compas_ghpython
from compas_ghpython.artists._artist import BaseArtist
from compas.utilities import color_to_colordict


colordict = partial(color_to_colordict, colorformat='rgb', normalize=False)


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
    color_nodes : 3-tuple
        Default color of the nodes.
    color_edges : 3-tuple
        Default color of the edges.

    """

    def __init__(self, network):
        self._network = None
        self.network = network
        self.color_nodes = (255, 255, 255)
        self.color_edges = (0, 0, 0)

    @property
    def network(self):
        """compas.datastructures.Network: The network that should be painted."""
        return self._network

    @network.setter
    def network(self, network):
        self._network = network

    def draw(self):
        """Draw the entire network with default color settings.

        Returns
        -------
        tuple
            list of :class:`Rhino.Geometry.Point3d` and list of :class:`Rhino.Geometry.Line`
        """
        return (self.draw_nodes(), self.draw_edges())

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
        color: 3-tuple or dict of 3-tuple, optional
            The color specififcation for the nodes.
            The default color is ``(255, 255, 255)``.

        Returns
        -------
        list of :class:`Rhino.Geometry.Point3d`

        """
        nodes = nodes or list(self.network.nodes())
        node_color = colordict(color, nodes, default=self.color_nodes)
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
        color : 3-tuple or dict of 3-tuple, optional
            The color specififcation for the edges.
            The default color is ``(0, 0, 0)``.

        Returns
        -------
        list of :class:`Rhino.Geometry.Line`

        """
        edges = edges or list(self.network.edges())
        edge_color = colordict(color, edges, default=self.color_edges)
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
