from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from Rhino.Geometry import TextDot  # type: ignore
import scriptcontext as sc  # type: ignore

import compas_rhino
from compas.geometry import Point
from compas.geometry import Line
from compas.artists import NetworkArtist as BaseArtist
from compas_rhino.conversions import point_to_rhino
from compas_rhino.conversions import line_to_rhino
from .artist import RhinoArtist
from ._helpers import attributes


class NetworkArtist(RhinoArtist, BaseArtist):
    """Artist for drawing network data structures.

    Parameters
    ----------
    network : :class:`~compas.datastructures.Network`
        A COMPAS network.
    **kwargs : dict, optional
        Additional keyword arguments.
        For more info, see :class:`RhinoArtist` and :class:`NetworkArtist`.

    """

    def __init__(self, network, **kwargs):
        super(NetworkArtist, self).__init__(network=network, **kwargs)

    # ==========================================================================
    # clear
    # ==========================================================================

    def clear(self):
        """Delete all objects drawn by this artist.

        Returns
        -------
        None

        """
        guids = compas_rhino.get_objects(name="{}.*".format(self.network.name))  # type: ignore
        compas_rhino.delete_objects(guids, purge=True)

    def clear_nodes(self):
        """Delete all nodes drawn by this artist.

        Returns
        -------
        None

        """
        guids = compas_rhino.get_objects(name="{}.vertex.*".format(self.network.name))  # type: ignore
        compas_rhino.delete_objects(guids, purge=True)

    def clear_edges(self):
        """Delete all edges drawn by this artist.

        Returns
        -------
        None

        """
        guids = compas_rhino.get_objects(name="{}.edge.*".format(self.network.name))  # type: ignore
        compas_rhino.delete_objects(guids, purge=True)

    # ==========================================================================
    # draw
    # ==========================================================================

    def draw(
        self,
        nodes=None,
        edges=None,
        nodecolor=None,
        edgecolor=None,
        nodetext=None,
        edgetext=None,
    ):
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
        nodetext : dict[int, str], optional
            A dictionary of node labels as node-text pairs.
            The default value is None, in which case every node will be labelled with its key.
        edgetext : dict[tuple[int, int], str], optional
            A dictionary of edgelabels as edge-text pairs.
            The default value is None, in which case every edge will be labelled with its key.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino objects.

        """
        self.clear()
        guids = self.draw_nodes(nodes=nodes, color=nodecolor, text=nodetext)
        guids += self.draw_edges(edges=edges, color=edgecolor, text=edgetext)
        return guids

    def draw_nodes(self, nodes=None, color=None, text=None, fontheight=10, fontface="Arial Regular"):
        """Draw a selection of nodes.

        Parameters
        ----------
        nodes : list[int], optional
            A list of nodes to draw.
            Default is None, in which case all nodes are drawn.
        color : :class:`~compas.colors.Color` | dict[int, :class:`~compas.colors.Color`], optional
            Color of the nodes.
            The default color is :attr:`NetworkArtist.default_nodecolor`.
        text : dict[int, str], optional
            A dictionary of node labels as node-text pairs.
            The default value is None, in which case every node will be labelled with its key.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino point objects.

        """
        nodes = nodes or self.network.nodes()  # type: ignore

        self.node_color = color
        self.node_text = text
        node_xyz = self.node_xyz
        node_color = self.node_color
        node_text = self.node_text

        guids = []

        for node in nodes:
            point = point_to_rhino(Point(*node_xyz[node]))
            name = "{}.node.{}".format(self.network.name, node)  # type: ignore
            color = node_color[node]  # type: ignore
            attr = attributes(name=name, color=color, layer=self.layer)
            guid = sc.doc.Objects.AddPoint(point, attr)
            guids.append(guid)

            if text and node in node_text:
                name = "{}.label".format(name)
                attr = attributes(name=name, color=color, layer=self.layer)
                dot = TextDot(str(node_text[node]), point)  # type: ignore
                dot.FontHeight = fontheight
                dot.FontFace = fontface
                guid = sc.doc.Objects.AddTextDot(dot, attr)

        return guids

    def draw_edges(self, edges=None, color=None, text=None, fontheight=10, fontface="Arial Regular"):
        """Draw a selection of edges.

        Parameters
        ----------
        edges : list[tuple[int, int]], optional
            A list of edges to draw.
            The default is None, in which case all edges are drawn.
        color : :class:`~compas.colors.Color` | dict[tuple[int, int], :class:`~compas.colors.Color`], optional
            Color of the edges.
            The default color is :attr:`NetworkArtist.default_edgecolor`.
        text : dict[tuple[int, int], str], optional
            A dictionary of edgelabels as edge-text pairs.
            The default value is None, in which case every edge will be labelled with its key.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino objects.

        """
        edges = edges or self.network.edges()  # type: ignore

        self.edge_color = color
        self.edge_text = text
        node_xyz = self.node_xyz
        edge_color = self.edge_color
        edge_text = self.edge_text

        guids = []

        for edge in edges:
            u, v = edge
            line = Line(node_xyz[u], node_xyz[v])
            color = edge_color[edge]  # type: ignore
            name = "{}.edge.{}-{}".format(self.network.name, u, v)  # type: ignore
            attr = attributes(name=name, color=color, layer=self.layer)
            guid = sc.doc.Objects.AddLine(line_to_rhino(line), attr)
            guids.append(guid)

            if text and edge in edge_text:
                name = "{}.label".format(name)
                attr = attributes(name=name, color=color, layer=self.layer)
                dot = TextDot(str(edge_text[edge]), point_to_rhino(line.midpoint))  # type: ignore
                dot.FontHeight = fontheight
                dot.FontFace = fontface
                sc.doc.Objects.AddTextDot(dot, attr)

        return guids
