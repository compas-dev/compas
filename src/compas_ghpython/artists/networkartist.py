from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_ghpython
from compas.artists import NetworkArtist
from .artist import GHArtist


class NetworkArtist(GHArtist, NetworkArtist):
    """Artist for drawing network data structures.

    Parameters
    ----------
    network : :class:`~compas.datastructures.Network`
        A COMPAS network.
    **kwargs : dict, optional
        Additional keyword arguments.
        See :class:`~compas_ghpython.artists.GHArtist` and :class:`~compas.artists.NetworkArtist` for more info.

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
        color: :class:`~compas.colors.Color` | dict[hashable, :class:`~compas.colors.Color`], optional
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
            points.append(
                {
                    "pos": node_xyz[node],
                    "name": "{}.node.{}".format(self.network.name, node),
                    "color": self.node_color[node].rgb255,
                }
            )
        return compas_ghpython.draw_points(points)

    def draw_edges(self, edges=None, color=None):
        """Draw a selection of edges.

        Parameters
        ----------
        edges : list[tuple[hashable, hashable]], optional
            A list of edges to draw.
            The default is None, in which case all edges are drawn.
        color : :class:`~compas.colors.Color` | dict[tuple[hashable, hashable], :class:`~compas.colors.Color`], optional
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
            u, v = edge
            lines.append(
                {
                    "start": node_xyz[u],
                    "end": node_xyz[v],
                    "color": self.edge_color[edge].rgb255,
                    "name": "{}.edge.{}-{}".format(self.network.name, u, v),
                }
            )
        return compas_ghpython.draw_lines(lines)

    def clear_edges(self):
        """GH Artists are state-less. Therefore, clear does not have any effect."""
        pass

    def clear_nodes(self):
        """GH Artists are state-less. Therefore, clear does not have any effect."""
        pass
