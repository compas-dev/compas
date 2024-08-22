from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import Rhino  # type: ignore
import scriptcontext as sc  # type: ignore

import compas_rhino
import compas_rhino.objects
from compas.geometry import Line
from compas.scene import GraphObject
from compas_rhino.conversions import line_to_rhino
from compas_rhino.conversions import point_to_rhino

from .sceneobject import RhinoSceneObject


class RhinoGraphObject(RhinoSceneObject, GraphObject):
    """Scene object for drawing graph data structures.

    Parameters
    ----------
    nodegroup : str, optional
        The name of the group for the nodes.
    edgegroup : str, optional
        The name of the group for the edges.
    edgedirection : bool, optional
        Flag for drawing the edges with an arrow indicating the direction.
    **kwargs : dict, optional
        Additional keyword arguments.

    """

    def __init__(self, nodegroup=None, edgegroup=None, edgedirection=False, **kwargs):
        super(RhinoGraphObject, self).__init__(**kwargs)
        self._guids_nodes = None
        self._guids_edges = None
        self._guids_nodelabels = None
        self._guids_edgelabels = None
        self._guids_spheres = None
        self._guids_pipes = None
        self.nodegroup = nodegroup
        self.edgegroup = edgegroup
        self.edgedirection = edgedirection

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
        guids = self.draw_nodes()
        guids += self.draw_edges()

        self._guids = guids
        return self.guids

    def draw_nodes(self):
        """Draw a selection of nodes.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino point objects.

        """
        guids = []

        nodes = list(self.graph.nodes()) if self.show_nodes is True else self.show_nodes or []

        if nodes:
            for node in nodes:
                name = "{}.node.{}".format(self.graph.name, node)
                attr = self.compile_attributes(name=name, color=self.nodecolor[node])
                geometry = point_to_rhino(self.node_xyz[node])

                guid = sc.doc.Objects.AddPoint(geometry, attr)
                guids.append(guid)

        if guids:
            if self.nodegroup:
                self.add_to_group(self.nodegroup, guids)
            elif self.group:
                self.add_to_group(self.group, guids)

        self._guids_nodes = guids
        return guids

    def draw_edges(self):
        """Draw a selection of edges.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino objects.

        """
        guids = []

        edges = list(self.graph.edges()) if self.show_edges is True else self.show_edges or []
        edgedirection = "end" if self.edgedirection else False

        if edges:
            for edge in edges:
                u, v = edge

                color = self.edgecolor[edge]
                name = "{}.edge.{}-{}".format(self.graph.name, u, v)
                attr = self.compile_attributes(name=name, color=color, arrow=edgedirection)
                geometry = line_to_rhino((self.node_xyz[u], self.node_xyz[v]))

                guid = sc.doc.Objects.AddLine(geometry, attr)
                guids.append(guid)

        if guids:
            if self.edgegroup:
                self.add_to_group(self.edgegroup, guids)
            elif self.group:
                self.add_to_group(self.group, guids)

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
            attr = self.compile_attributes(name=name, color=self.nodecolor[node])

            point = point_to_rhino(self.node_xyz[node])

            dot = Rhino.Geometry.TextDot(str(text[node]), point)
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

            color = self.edgecolor[edge]
            name = "{}.edge.{}-{}.label".format(self.graph.name, u, v)  # type: ignore
            attr = self.compile_attributes(name=name, color=color)

            line = Line(self.node_xyz[u], self.node_xyz[v])
            point = point_to_rhino(line.midpoint)

            dot = Rhino.Geometry.TextDot(str(text[edge]), point)
            dot.FontHeight = fontheight
            dot.FontFace = fontface

            guid = sc.doc.Objects.AddTextDot(dot, attr)
            guids.append(guid)

        if group:
            self.add_to_group(group, guids)

        self._guids_edgelabels = guids

        return guids
