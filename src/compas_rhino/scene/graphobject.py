from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from Rhino.Geometry import TextDot  # type: ignore
import scriptcontext as sc  # type: ignore

import compas_rhino
from compas.geometry import Line
from compas.geometry import Cylinder
from compas.geometry import Sphere
from compas.scene import GraphObject as BaseGraphObject
from compas_rhino.conversions import point_to_rhino
from compas_rhino.conversions import line_to_rhino
from compas_rhino.conversions import sphere_to_rhino
from compas_rhino.conversions import cylinder_to_rhino_brep
from .sceneobject import RhinoSceneObject
from .helpers import attributes


class GraphObject(RhinoSceneObject, BaseGraphObject):
    """Scene object for drawing graph data structures.

    Parameters
    ----------
    graph : :class:`compas.datastructures.Graph`
        A COMPAS graph.
    **kwargs : dict, optional
        Additional keyword arguments.

    """

    def __init__(self, graph, **kwargs):
        super(GraphObject, self).__init__(graph=graph, **kwargs)
        self._guids_nodes = None
        self._guids_edges = None
        self._guids_nodelabels = None
        self._guids_edgelabels = None
        self._guids_spheres = None
        self._guids_pipes = None

    # ==========================================================================
    # clear
    # ==========================================================================

    def clear(self):
        """Delete all objects drawn by this scene object.

        Returns
        -------
        None

        """
        compas_rhino.objects.delete_objects(self.guids, purge=True)

    def clear_nodes(self):
        """Delete all nodes drawn by this scene object.

        Returns
        -------
        None

        """
        compas_rhino.objects.delete_objects(self._guids_nodes, purge=True)

    def clear_edges(self):
        """Delete all edges drawn by this scene object.

        Returns
        -------
        None

        """
        compas_rhino.objects.delete_objects(self._guids_edges, purge=True)

    # ==========================================================================
    # draw
    # ==========================================================================

    def draw(self):
        """Draw the graph using the chosen visualisation settings.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino objects.

        """
        self.clear()
        guids = self.draw_nodes(nodes=self.show_nodes, color=self.nodecolor, group=self.group)
        guids += self.draw_edges(edges=self.show_edges, color=self.edgecolor, group=self.group)
        self._guids = guids
        return self.guids

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

        self.nodecolor = color

        if nodes is True:
            nodes = list(self.graph.nodes())

        for node in nodes or self.graph.nodes():  # type: ignore
            name = "{}.node.{}".format(self.graph.name, node)  # type: ignore
            attr = attributes(name=name, color=self.nodecolor[node], layer=self.layer)  # type: ignore

            point = point_to_rhino(self.node_xyz[node])

            guid = sc.doc.Objects.AddPoint(point, attr)
            guids.append(guid)

        if group:
            self.add_to_group(group, guids)

        self._guids_nodes = guids

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
        self.edgecolor = color

        if edges is True:
            edges = list(self.graph.edges())

        for edge in edges or self.graph.edges():  # type: ignore
            u, v = edge

            color = self.edgecolor[edge]  # type: ignore
            name = "{}.edge.{}-{}".format(self.graph.name, u, v)  # type: ignore
            attr = attributes(name=name, color=color, layer=self.layer, arrow=arrow)  # type: ignore

            line = Line(self.node_xyz[u], self.node_xyz[v])

            guid = sc.doc.Objects.AddLine(line_to_rhino(line), attr)
            guids.append(guid)

        if group:
            self.add_to_group(group, guids)

        self._guids_edges = guids

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

        self.nodecolor = color

        for node in text:
            name = "{}.node.{}.label".format(self.graph.name, node)  # type: ignore
            attr = attributes(name=name, color=self.nodecolor[node], layer=self.layer)  # type: ignore

            point = point_to_rhino(self.node_xyz[node])

            dot = TextDot(str(text[node]), point)  # type: ignore
            dot.FontHeight = fontheight
            dot.FontFace = fontface

            guid = sc.doc.Objects.AddTextDot(dot, attr)
            guids.append(guid)

        if group:
            self.add_to_group(group, guids)

        self._guids_nodelabels = guids

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

        self.edgecolor = color

        for edge in text:
            u, v = edge

            color = self.edgecolor[edge]  # type: ignore
            name = "{}.edge.{}-{}.label".format(self.graph.name, u, v)  # type: ignore
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

        self._guids_edgelabels = guids

        return guids

    # =============================================================================
    # draw miscellaneous
    # =============================================================================

    def draw_spheres(self, radius, color=None, group=None):
        """Draw spheres at the vertices of the graph.

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

        self.nodecolor = color

        for node in radius:
            name = "{}.node.{}.sphere".format(self.graph.name, node)  # type: ignore
            color = self.nodecolor[node]  # type: ignore
            attr = attributes(name=name, color=color, layer=self.layer)

            sphere = Sphere.from_point_and_radius(self.node_xyz[node], radius[node])
            geometry = sphere_to_rhino(sphere)

            guid = sc.doc.Objects.AddSphere(geometry, attr)
            guids.append(guid)

        if group:
            self.add_to_group(group, guids)

        self._guids_spheres = guids

        return guids

    def draw_pipes(self, radius, color=None, group=None):
        """Draw pipes around the edges of the graph.

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

        self.edgecolor = color

        for edge in radius:
            name = "{}.edge.{}-{}.pipe".format(self.graph.name, *edge)  # type: ignore
            color = self.edgecolor[edge]  # type: ignore
            attr = attributes(name=name, color=color, layer=self.layer)

            line = Line(self.node_xyz[edge[0]], self.node_xyz[edge[1]])
            cylinder = Cylinder.from_line_and_radius(line, radius[edge])
            geometry = cylinder_to_rhino_brep(cylinder)

            guid = sc.doc.Objects.AddBrep(geometry, attr)
            guids.append(guid)

        if group:
            self.add_to_group(group, guids)

        self._guids_pipes = guids

        return guids
