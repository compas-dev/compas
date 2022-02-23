from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from functools import partial
import compas_ghpython

from compas.utilities import color_to_colordict

from compas.artists import NetworkArtist
from .artist import GHArtist

colordict = partial(color_to_colordict, colorformat='rgb', normalize=False)


class NetworkArtist(GHArtist, NetworkArtist):
    """Artist for drawing network data structures.

    Parameters
    ----------
    network : :class:`compas.datastructures.Network`
        A COMPAS network.
    **kwargs : dict, optional
        Additional keyword arguments.
        See :class:`compas_ghpython.artists.GHArtist` and :class:`compas.artists.NetworkArtist` for more info.

    """

    def __init__(self, network, **kwargs):
        super(NetworkArtist, self).__init__(network=network, **kwargs)

    def draw(self):
        """Draw the entire network with default color settings.

        Returns
        -------
        list[:rhino:`Rhino.Geometry.Point3d`]
            The objects representing the nodes of the network.
        list[:rhino:`Rhino.Geometry.Line`]
            The objects representing the edges of the network.

        """
        return self.draw_nodes(), self.draw_edges()

    def draw_nodes(self, nodes=None, color=None):
        """Draw a selection of nodes.

        Parameters
        ----------
        nodes: list[hashable], optional
            The selection of nodes that should be drawn.
            Default is None, in which case all nodes are drawn.
        color: tuple[int, int, int] or dict[hashable, tuple[int, int, int]], optional
            The color specification for the nodes.
            The default color is :attr:`NetworkArtist.default_nodecolor`.

        Returns
        -------
        list[:rhino:`Rhino.Geometry.Point3d`]

        """
        self.node_color = color
        node_xyz = self.node_xyz
        nodes = nodes or list(self.network.nodes())
        points = []
        for node in nodes:
            points.append({
                'pos': node_xyz[node],
                'name': "{}.node.{}".format(self.network.name, node),
                'color': self.node_color.get(node, self.default_nodecolor)
            })
        return compas_ghpython.draw_points(points)

    def draw_edges(self, edges=None, color=None):
        """Draw a selection of edges.

        Parameters
        ----------
        edges : list[tuple[hashable, hashable]], optional
            A list of edges to draw.
            The default is None, in which case all edges are drawn.
        color : tuple[int, int, int] or dict[tuple[hashable, hashable], tuple[int, int, int]], optional
            The color specification for the edges.
            The default color is the value of :attr:`NetworkArtist.default_edgecolor`.

        Returns
        -------
        list[:rhino:`Rhino.Geometry.Line`]

        """
        self.edge_color = color
        node_xyz = self.node_xyz
        edges = edges or list(self.network.edges())
        lines = []
        for edge in edges:
            lines.append({
                'start': node_xyz[edge[0]],
                'end': node_xyz[edge[1]],
                'color': self.edge_color.get(edge, self.default_edgecolor),
                'name': "{}.edge.{}-{}".format(self.network.name, *edge)
            })
        return compas_ghpython.draw_lines(lines)
