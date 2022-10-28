from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas.geometry import centroid_points
from compas.artists import NetworkArtist
from .artist import RhinoArtist


class NetworkArtist(RhinoArtist, NetworkArtist):
    """Artist for drawing network data structures.

    Parameters
    ----------
    network : :class:`~compas.datastructures.Network`
        A COMPAS network.
    layer : str, optional
        The parent layer of the network.
    **kwargs : dict, optional
        Additional keyword arguments.
        For more info, see :class:`RhinoArtist` and :class:`NetworkArtist`.

    """

    def __init__(self, network, layer=None, **kwargs):

        super(NetworkArtist, self).__init__(network=network, layer=layer, **kwargs)

    # ==========================================================================
    # clear
    # ==========================================================================

    def clear(self):
        """Delete all objects drawn by this artist.

        Returns
        -------
        None

        """
        guids = compas_rhino.get_objects(name="{}.*".format(self.network.name))
        compas_rhino.delete_objects(guids, purge=True)

    def clear_nodes(self):
        """Delete all nodes drawn by this artist.

        Returns
        -------
        None

        """
        guids = compas_rhino.get_objects(name="{}.vertex.*".format(self.network.name))
        compas_rhino.delete_objects(guids, purge=True)

    def clear_edges(self):
        """Delete all edges drawn by this artist.

        Returns
        -------
        None

        """
        guids = compas_rhino.get_objects(name="{}.edge.*".format(self.network.name))
        compas_rhino.delete_objects(guids, purge=True)

    def clear_nodelabels(self):
        """Delete all node labels drawn by this artist.

        Returns
        -------
        None

        """
        guids = compas_rhino.get_objects(name="{}.nodexlabel.*".format(self.network.name))
        compas_rhino.delete_objects(guids, purge=True)

    def clear_edgelabels(self):
        """Delete all edge labels drawn by this artist.

        Returns
        -------
        None

        """
        guids = compas_rhino.get_objects(name="{}.edgelabel.*".format(self.network.name))
        compas_rhino.delete_objects(guids, purge=True)

    # ==========================================================================
    # draw
    # ==========================================================================

    def draw(self, nodes=None, edges=None, nodecolor=None, edgecolor=None):
        """Draw the network using the chosen visualisation settings.

        Parameters
        ----------
        nodes : list[int], optional
            A list of nodes to draw.
            Default is None, in which case all nodes are drawn.
        edges : list[tuple[int, int]], optional
            A list of edges to draw.
            The default is None, in which case all edges are drawn.
        nodecolor : :class:`~compas.colors.Color` | dict[int, :class:`~compas.colors.Color`], optional
            The color of the nodes.
            The default color is :attr:`NetworkArtist.default_nodecolor`.
        edgecolor : :class:`~compas.colors.Color` | dict[tuple[int, int], :class:`~compas.colors.Color`], optional
            The color of the edges.
            The default color is :attr:`NetworkArtist.default_edgecolor`.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino objects.

        """
        self.clear()
        guids = self.draw_nodes(nodes=nodes, color=nodecolor)
        guids += self.draw_edges(edges=edges, color=edgecolor)
        return guids

    def draw_nodes(self, nodes=None, color=None):
        """Draw a selection of nodes.

        Parameters
        ----------
        nodes : list[int], optional
            A list of nodes to draw.
            Default is None, in which case all nodes are drawn.
        color : :class:`~compas.colors.Color` | dict[int, :class:`~compas.colors.Color`], optional
            Color of the nodes.
            The default color is :attr:`NetworkArtist.default_nodecolor`.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino objects.

        """
        self.node_color = color
        nodes = nodes or self.nodes
        node_xyz = self.node_xyz
        points = []
        for node in nodes:
            points.append(
                {
                    "pos": node_xyz[node],
                    "name": "{}.node.{}".format(self.network.name, node),
                    "color": self.node_color[node].rgb255,
                }
            )
        return compas_rhino.draw_points(points, layer=self.layer, clear=False, redraw=False)

    def draw_edges(self, edges=None, color=None):
        """Draw a selection of edges.

        Parameters
        ----------
        edges : list[tuple[int, int]], optional
            A list of edges to draw.
            The default is None, in which case all edges are drawn.
        color : :class:`~compas.colors.Color` | dict[tuple[int, int], :class:`~compas.colors.Color`], optional
            Color of the edges.
            The default color is :attr:`NetworkArtist.default_edgecolor`.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino objects.

        """
        self.edge_color = color
        edges = edges or self.edges
        node_xyz = self.node_xyz
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
        return compas_rhino.draw_lines(lines, layer=self.layer, clear=False, redraw=False)

    # ==========================================================================
    # draw labels
    # ==========================================================================

    def draw_nodelabels(self, text=None):
        """Draw labels for a selection nodes.

        Parameters
        ----------
        text : dict[int, str], optional
            A dictionary of node labels as node-text pairs.
            The default value is None, in which case every node will be labelled with its key.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino objects.

        """
        self.node_text = text
        node_xyz = self.node_xyz
        labels = []
        for node in self.node_text:
            labels.append(
                {
                    "pos": node_xyz[node],
                    "name": "{}.nodelabel.{}".format(self.network.name, node),
                    "color": self.node_color[node].rgb255,
                    "text": self.node_text[node],
                }
            )
        return compas_rhino.draw_labels(labels, layer=self.layer, clear=False, redraw=False)

    def draw_edgelabels(self, text=None):
        """Draw labels for a selection of edges.

        Parameters
        ----------
        text : dict[tuple[int, int], str], optional
            A dictionary of edgelabels as edge-text pairs.
            The default value is None, in which case every edge will be labelled with its key.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino objects.

        """
        self.edge_text = text
        node_xyz = self.node_xyz
        labels = []
        for edge in self.edge_text:
            u, v = edge
            labels.append(
                {
                    "pos": centroid_points([node_xyz[u], node_xyz[v]]),
                    "name": "{}.edgelabel.{}-{}".format(self.network.name, u, v),
                    "color": self.edge_color[edge].rgb255,
                    "text": self.edge_text[edge],
                }
            )
        return compas_rhino.draw_labels(labels, layer=self.layer, clear=False, redraw=False)
