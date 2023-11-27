from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from Rhino.Geometry import TextDot  # type: ignore
import scriptcontext as sc  # type: ignore

import compas_rhino
from compas.geometry import Line
from compas.geometry import Cylinder
from compas.geometry import Sphere
from compas.scene import NetworkObject as BaseNetworkObject
from compas_rhino.conversions import point_to_rhino
from compas_rhino.conversions import line_to_rhino
from compas_rhino.conversions import sphere_to_rhino
from compas_rhino.conversions import cylinder_to_rhino_brep
from .sceneobject import RhinoSceneObject
from ._helpers import attributes


class NetworkObject(RhinoSceneObject, BaseNetworkObject):
    """Sceneobject for drawing network data structures.

    Parameters
    ----------
    network : :class:`compas.datastructures.Network`
        A COMPAS network.
    **kwargs : dict, optional
        Additional keyword arguments.

    """

    def __init__(self, network, **kwargs):
        super(NetworkObject, self).__init__(network=network, **kwargs)

    # ==========================================================================
    # clear
    # ==========================================================================

    def clear(self):
        """Delete all objects drawn by this sceneobject.

        Returns
        -------
        None

        """
        guids = compas_rhino.get_objects(name="{}.*".format(self.network.name))  # type: ignore
        compas_rhino.delete_objects(guids, purge=True)

    def clear_nodes(self):
        """Delete all nodes drawn by this sceneobject.

        Returns
        -------
        None

        """
        guids = compas_rhino.get_objects(name="{}.node.*".format(self.network.name))  # type: ignore
        compas_rhino.delete_objects(guids, purge=True)

    def clear_edges(self):
        """Delete all edges drawn by this sceneobject.

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
        nodecolor : :class:`compas.colors.Color` | dict[int, :class:`compas.colors.Color`], optional
            The color of the nodes.
        edgecolor : :class:`compas.colors.Color` | dict[tuple[int, int], :class:`compas.colors.Color`], optional
            The color of the edges.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino objects.

        """
        self.clear()
        guids = self.draw_nodes(nodes=nodes, color=nodecolor)
        guids += self.draw_edges(edges=edges, color=edgecolor)
        return guids

    def draw_nodes(self, nodes=None, color=None, group=None):
        """Draw a selection of nodes.

        Parameters
        ----------
        nodes : list[int], optional
            A list of nodes to draw.
            Default is None, in which case all nodes are drawn.
        color : :class:`compas.colors.Color` | dict[int, :class:`compas.colors.Color`], optional
            Color of the nodes.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino point objects.

        """
        guids = []

        self.node_color = color

        for node in nodes or self.network.nodes():  # type: ignore
            name = "{}.node.{}".format(self.network.name, node)  # type: ignore
            attr = attributes(name=name, color=self.node_color[node], layer=self.layer)  # type: ignore

            point = point_to_rhino(self.node_xyz[node])

            guid = sc.doc.Objects.AddPoint(point, attr)
            guids.append(guid)

        if group:
            self.add_to_group(group, guids)

        return guids

    def draw_edges(self, edges=None, color=None, group=None, show_direction=False):
        """Draw a selection of edges.

        Parameters
        ----------
        edges : list[tuple[int, int]], optional
            A list of edges to draw.
            The default is None, in which case all edges are drawn.
        color : :class:`compas.colors.Color` | dict[tuple[int, int], :class:`compas.colors.Color`], optional
            Color of the edges.
        group : str, optional
            The name of a group to add the edges to.
        show_direction : bool, optional
            Show the direction of the edges.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino objects.

        """
        guids = []

        arrow = "end" if show_direction else None
        self.edge_color = color

        for edge in edges or self.network.edges():  # type: ignore
            u, v = edge

            color = self.edge_color[edge]  # type: ignore
            name = "{}.edge.{}-{}".format(self.network.name, u, v)  # type: ignore
            attr = attributes(name=name, color=color, layer=self.layer, arrow=arrow)  # type: ignore

            line = Line(self.node_xyz[u], self.node_xyz[v])

            guid = sc.doc.Objects.AddLine(line_to_rhino(line), attr)
            guids.append(guid)

        if group:
            self.add_to_group(group, guids)

        return guids

    # =============================================================================
    # draw labels
    # =============================================================================

    def draw_nodelabels(self, text, color=None, group=None, fontheight=10, fontface="Arial Regular"):
        """Draw labels for a selection of nodes.

        Parameters
        ----------
        text : dict[int, str]
            A dictionary of node labels as node-text pairs.
        color : :class:`compas.colors.Color` | dict[int, :class:`compas.colors.Color`], optional
            Color of the labels.
        group : str, optional
            The name of a group to add the labels to.
        fontheight : float, optional
            Font height of the labels.
        fontface : str, optional
            Font face of the labels.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino text objects.

        """
        guids = []

        self.node_color = color

        for node in text:
            name = "{}.node.{}.label".format(self.network.name, node)  # type: ignore
            attr = attributes(name=name, color=self.node_color[node], layer=self.layer)  # type: ignore

            point = point_to_rhino(self.node_xyz[node])

            dot = TextDot(str(text[node]), point)  # type: ignore
            dot.FontHeight = fontheight
            dot.FontFace = fontface

            guid = sc.doc.Objects.AddTextDot(dot, attr)
            guids.append(guid)

        if group:
            self.add_to_group(group, guids)

        return guids

    def draw_edgelabels(self, text, color=None, group=None, fontheight=10, fontface="Arial Regular"):
        """Draw labels for a selection of edges.

        Parameters
        ----------
        text : dict[tuple[int, int], str]
            A dictionary of edge labels as edge-text pairs.
        color : :class:`compas.colors.Color` | dict[tuple[int, int], :class:`compas.colors.Color`], optional
            Color of the labels.
        group : str, optional
            The name of a group to add the labels to.
        fontheight : float, optional
            Font height of the labels.
        fontface : str, optional
            Font face of the labels.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino text objects.

        """
        guids = []

        self.edge_color = color

        for edge in text:
            u, v = edge

            color = self.edge_color[edge]  # type: ignore
            name = "{}.edge.{}-{}.label".format(self.network.name, u, v)  # type: ignore
            attr = attributes(name=name, color=color, layer=self.layer)

            line = Line(self.node_xyz[u], self.node_xyz[v])
            point = point_to_rhino(line.midpoint)

            dot = TextDot(str(text[edge]), point)
            dot.FontHeight = fontheight
            dot.FontFace = fontface

            guid = sc.doc.Objects.AddTextDot(dot, attr)
            guids.append(guid)

        if group:
            self.add_to_group(group, guids)

        return guids

    # =============================================================================
    # draw miscellaneous
    # =============================================================================

    def draw_spheres(self, radius, color=None, group=None):
        """Draw spheres at the vertices of the network.

        Parameters
        ----------
        radius : dict[int, float], optional
            The radius of the spheres.
        color : :class:`compas.colors.Color` | dict[int, :class:`compas.colors.Color`], optional
            The color of the spheres.
        group : str, optional
            The name of a group to join the created Rhino objects in.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino objects.

        """
        guids = []

        self.node_color = color

        for node in radius:
            name = "{}.node.{}.sphere".format(self.network.name, node)  # type: ignore
            color = self.node_color[node]  # type: ignore
            attr = attributes(name=name, color=color, layer=self.layer)

            sphere = Sphere.from_point_and_radius(self.node_xyz[node], radius[node])
            geometry = sphere_to_rhino(sphere)

            guid = sc.doc.Objects.AddSphere(geometry, attr)
            guids.append(guid)

        if group:
            self.add_to_group(group, guids)

        return guids

    def draw_pipes(self, radius, color=None, group=None):
        """Draw pipes around the edges of the network.

        Parameters
        ----------
        radius : dict[tuple[int, int], float]
            The radius per edge.
        color : :class:`compas.colors.Color` | dict[tuple[int, int], :class:`compas.colors.Color`], optional
            The color of the pipes.
        group : str, optional
            The name of a group to join the created Rhino objects in.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino objects.

        """
        guids = []

        self.edge_color = color

        for edge in radius:
            name = "{}.edge.{}-{}.pipe".format(self.network.name, *edge)  # type: ignore
            color = self.edge_color[edge]  # type: ignore
            attr = attributes(name=name, color=color, layer=self.layer)

            line = Line(self.node_xyz[edge[0]], self.node_xyz[edge[1]])
            cylinder = Cylinder.from_line_and_radius(line, radius[edge])
            geometry = cylinder_to_rhino_brep(cylinder)

            guid = sc.doc.Objects.AddBrep(geometry, attr)
            guids.append(guid)

        if group:
            self.add_to_group(group, guids)

        return guids
