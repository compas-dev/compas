from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from Rhino.Geometry import TextDot  # type: ignore
import scriptcontext as sc  # type: ignore

from compas.geometry import centroid_points
from compas.geometry import Line
from compas.scene import VolMeshObject as BaseVolMeshObject

import compas_rhino.objects
from compas_rhino.conversions import point_to_rhino
from compas_rhino.conversions import line_to_rhino
from compas_rhino.conversions import vertices_and_faces_to_rhino

from .sceneobject import RhinoSceneObject
from ._helpers import attributes
from ._helpers import ngon


class VolMeshObject(RhinoSceneObject, BaseVolMeshObject):
    """Scene object for drawing volmesh data structures.

    Parameters
    ----------
    volmesh : :class:`compas.datastructures.VolMesh`
        A COMPAS volmesh.
    disjoint : bool, optional
        Draw the faces of the mesh disjointed.
        Default is ``True``.
    **kwargs : dict, optional
        Additional keyword arguments.

    """

    def __init__(self, volmesh, disjoint=True, **kwargs):
        super(VolMeshObject, self).__init__(volmesh=volmesh, **kwargs)
        self.disjoint = disjoint
        self._guids_vertices = None
        self._guids_edges = None
        self._guids_faces = None
        self._guids_cells = None
        self._guids_vertexlabels = None
        self._guids_edgelabels = None
        self._guids_facelabels = None
        self._guids_celllabels = None

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

    def clear_vertices(self):
        """Delete all vertices drawn by this scene object.

        Returns
        -------
        None

        """
        compas_rhino.objects.delete_objects(self._guids_vertices, purge=True)

    def clear_edges(self):
        """Delete all edges drawn by this scene object.

        Returns
        -------
        None

        """
        compas_rhino.objects.delete_objects(self._guids_edges, purge=True)

    def clear_faces(self):
        """Delete all faces drawn by this scene object.

        Returns
        -------
        None

        """
        compas_rhino.objects.delete_objects(self._guids_faces, purge=True)

    def clear_cells(self):
        """Delete all cells drawn by this scene object.

        Returns
        -------
        None

        """
        compas_rhino.objects.delete_objects(self._guids_cells, purge=True)

    def clear_vertexlabels(self):
        """Delete all vertex labels drawn by this scene object.

        Returns
        -------
        None

        """
        compas_rhino.objects.delete_objects(self._guids_vertexlabels, purge=True)

    def clear_edgelabels(self):
        """Delete all edge labels drawn by this scene object.

        Returns
        -------
        None

        """
        compas_rhino.objects.delete_objects(self._guids_edgelabels, purge=True)

    def clear_facelabels(self):
        """Delete all face labels drawn by this scene object.

        Returns
        -------
        None

        """
        compas_rhino.objects.delete_objects(self._guids_facelabels, purge=True)

    # ==========================================================================
    # draw
    # ==========================================================================

    def draw(self):
        """Draw a selection of cells.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino objects.
            Every cell is drawn as an individual mesh.

        """
        guids = []

        if self.show_vertices:
            guids += self.draw_vertices(vertices=self.show_vertices, color=self.vertexcolor, group=self.group)
        if self.show_edges:
            guids += self.draw_edges(edges=self.show_edges, color=self.edgecolor, group=self.group)
        if self.show_faces:
            guids += self.draw_faces(faces=self.show_faces, color=self.facecolor, group=self.group)
        if self.show_cells:
            guids += self.draw_cells(cells=self.show_cells, color=self.cellcolor, group=self.group)
    
        self._guids = guids

        return self.guids

    def draw_vertices(self, vertices=None, color=None, group=None):
        """Draw a selection of vertices.

        Parameters
        ----------
        vertices : list[int], optional
            A list of vertices to draw.
            Default is None, in which case all vertices are drawn.
        color : :class:`compas.colors.Color` | dict[int, :class:`compas.colors.Color`], optional
            The color of the vertices.
        group : str, optional
            The name of the group in which the vertices are combined.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino point objects.

        """
        self.vertexcolor = color

        guids = []

        if vertices is True:
            vertices = list(self.volmesh.vertices())

        for vertex in vertices or self.volmesh.vertices():  # type: ignore
            name = "{}.vertex.{}".format(self.volmesh.name, vertex)  # type: ignore
            color = self.vertexcolor[vertex]  # type: ignore
            attr = attributes(name=name, color=color, layer=self.layer)

            point = self.vertex_xyz[vertex]

            guid = sc.doc.Objects.AddPoint(point_to_rhino(point), attr)
            guids.append(guid)

        return guids

    def draw_edges(self, edges=None, color=None, group=None):
        """Draw a selection of edges.

        Parameters
        ----------
        edges : list[tuple[int, int]], optional
            A list of edges to draw.
            The default is None, in which case all edges are drawn.
        color : :class:`compas.colors.Color` | dict[tuple[int, int], :class:`compas.colors.Color`], optional
            The color of the edges.
        group : str, optional
            The name of the group in which the edges are combined.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino line objects.

        """
        self.edgecolor = color

        guids = []

        if edges is True:
            edges = list(self.volmesh.edges())

        for edge in edges or self.volmesh.edges():  # type: ignore
            name = "{}.edge.{}-{}".format(self.volmesh.name, *edge)  # type: ignore
            color = self.edgecolor[edge]  # type: ignore
            attr = attributes(name=name, color=color, layer=self.layer)

            line = Line(self.vertex_xyz[edge[0]], self.vertex_xyz[edge[1]])

            guid = sc.doc.Objects.AddLine(line_to_rhino(line), attr)
            guids.append(guid)

        if group:
            self.add_to_group(group, guids)

        return guids

    def draw_faces(self, faces=None, color=None, group=None):
        """Draw a selection of faces.

        Parameters
        ----------
        faces : list[int], optional
            A list of faces to draw.
            The default is None, in which case all faces are drawn.
        color : :class:`compas.colors.Color` | dict[int, :class:`compas.colors.Color`], optional
            The color of the faces.
        group : str, optional
            The name of the group in which the faces are combined.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino objects.

        """
        self.facecolor = color

        guids = []

        if faces is True:
            faces = list(self.volmesh.faces())

        for face in faces or self.volmesh.faces():  # type: ignore
            name = "{}.face.{}".format(self.volmesh.name, face)  # type: ignore
            color = self.facecolor[face]  # type: ignore
            attr = attributes(name=name, color=color, layer=self.layer)

            vertices = [self.vertex_xyz[vertex] for vertex in self.volmesh.face_vertices(face)]  # type: ignore
            facet = ngon(len(vertices))

            if facet:
                guid = sc.doc.Objects.AddMesh(vertices_and_faces_to_rhino(vertices, [facet]), attr)
                guids.append(guid)

        if group:
            self.add_to_group(group, guids)

        return guids

    def draw_cells(self, cells=None, color=None, group=None):
        """Draw a selection of cells.

        Parameters
        ----------
        cells : list[int], optional
            A list of cells to draw.
            The default is None, in which case all cells are drawn.
        color : :class:`compas.colors.Color` | dict[int, :class:`compas.colors.Color`], optional
            The color of the cells.
        group : str, optional
            The name of the group in which the cells are combined.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino objects.
            Every cell is drawn as an individual mesh.

        """
        self.cellcolor = color

        guids = []

        if cells is True:
            cells = list(self.volmesh.cells())

        for cell in cells or self.volmesh.cells():  # type: ignore
            name = "{}.cell.{}".format(self.volmesh.name, cell)  # type: ignore
            color = self.cellcolor[cell]  # type: ignore
            attr = attributes(name=name, color=color, layer=self.layer)

            vertices = self.volmesh.cell_vertices(cell)  # type: ignore
            faces = self.volmesh.cell_faces(cell)  # type: ignore
            vertex_index = dict((vertex, index) for index, vertex in enumerate(vertices))
            vertices = [self.vertex_xyz[vertex] for vertex in vertices]
            faces = [[vertex_index[vertex] for vertex in self.volmesh.halfface_vertices(face)] for face in faces]  # type: ignore

            guid = sc.doc.Objects.AddMesh(vertices_and_faces_to_rhino(vertices, faces, disjoint=self.disjoint), attr)
            guids.append(guid)

        return guids

    # =============================================================================
    # draw labels
    # =============================================================================

    def draw_vertexlabels(self, text, color=None, group=None, fontheight=10, fontface="Arial Regular"):
        """Draw a selection of vertex labels.

        Parameters
        ----------
        text : dict[int, str]
            A dictionary of vertex labels as vertex-text pairs.
        color : :class:`compas.colors.Color` | dict[int, :class:`compas.colors.Color`], optional
            The color of the vertices.
        group : str, optional
            The name of the group in which the labels are combined.
        fontheight : int, optional
            Font height of the vertex labels.
        fontface : str, optional
            Font face of the vertex labels.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino objects.

        """
        self.vertexcolor = color

        guids = []

        for vertex in text:
            name = "{}.vertex.{}.label".format(self.volmesh.name, vertex)  # type: ignore
            color = self.vertexcolor[vertex]  # type: ignore
            attr = attributes(name=name, color=color, layer=self.layer)

            point = self.vertex_xyz[vertex]

            dot = TextDot(str(text[vertex]), point)  # type: ignore
            dot.FontHeight = fontheight
            dot.FontFace = fontface

            guid = sc.doc.Objects.AddTextDot(dot, attr)
            guids.append(guid)

        if group:
            self.add_to_group(group, guids)

        return guids

    def draw_edgelabels(self, text, color=None, group=None, fontheight=10, fontface="Arial Regular"):
        """Draw a selection of edge labels.

        Parameters
        ----------
        text : dict[tuple[int, int], str], optional
            A dictionary of edge labels as edge-text pairs.
        color : :class:`compas.colors.Color` | dict[tuple[int, int], :class:`compas.colors.Color`], optional
            The color of the edges.
        group : str, optional
            The name of the group in which the labels are combined.
        fontheight : int, optional
            Font height of the edge labels.
        fontface : str, optional
            Font face of the edge labels.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino objects.

        """
        self.edgecolor = color

        guids = []

        for edge in text:
            name = "{}.edge.{}-{}.label".format(self.volmesh.name, *edge)  # type: ignore
            color = self.edgecolor[edge]  # type: ignore
            attr = attributes(name="{}.label".format(name), color=color, layer=self.layer)

            line = Line(self.vertex_xyz[edge[0]], self.vertex_xyz[edge[1]])
            point = point_to_rhino(line.midpoint)

            dot = TextDot(str(text[edge]), point)  # type: ignore
            dot.FontHeight = fontheight
            dot.FontFace = fontface

            guid = sc.doc.Objects.AddTextDot(dot, attr)
            guids.append(guid)

        if group:
            self.add_to_group(group, guids)

        return guids

    def draw_facelabels(self, text, color=None, group=None, fontheight=10, fontface="Arial Regular"):
        """Draw a selection of face labels.

        Parameters
        ----------
        text : dict[int, str]
            A dictionary of face labels as face-text pairs.
        color : :class:`compas.colors.Color` | dict[int, :class:`compas.colors.Color`], optional
            The color of the faces.
        group : str, optional
            The name of the group in which the labels are combined.
        fontheight : int, optional
            Font height of the face labels.
        fontface : str, optional
            Font face of the face labels.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino objects.

        """
        self.facecolor = color

        guids = []

        for face in text:
            name = "{}.face.{}.label".format(self.volmesh.name, face)  # type: ignore
            color = self.facecolor[face]  # type: ignore
            attr = attributes(name="{}.label".format(name), color=color, layer=self.layer)

            vertices = [self.vertex_xyz[vertex] for vertex in self.volmesh.face_vertices(face)]  # type: ignore
            point = point_to_rhino(centroid_points(vertices))  # type: ignore

            dot = TextDot(str(text[face]), point)  # type: ignore
            dot.FontHeight = fontheight
            dot.FontFace = fontface

            guid = sc.doc.Objects.AddTextDot(dot, attr)
            guids.append(guid)

        if group:
            self.add_to_group(group, guids)

        return guids

    def draw_celllabels(self, text, color=None, group=None, fontheight=10, fontface="Arial Regular"):
        """Draw a selection of cells.

        Parameters
        ----------
        text : dict[int, str], optional
            A dictionary of face labels as cell-text pairs.
        color : :class:`compas.colors.Color` | dict[int, :class:`compas.colors.Color`], optional
            The color of the cells.
        group : str, optional
            The name of the group in which the labels are combined.
        fontheight : int, optional
            Font height of the cell labels.
        fontface : str, optional
            Font face of the cell labels.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino objects.

        """
        self.cellcolor = color

        guids = []

        for cell in text:
            name = "{}.cell.{}.label".format(self.volmesh.name, cell)  # type: ignore
            color = self.cellcolor[cell]  # type: ignore
            attr = attributes(name="{}.label".format(name), color=color, layer=self.layer)

            vertices = [self.vertex_xyz[vertex] for vertex in self.volmesh.cell_vertices(cell)]  # type: ignore
            point = point_to_rhino(centroid_points(vertices))  # type: ignore

            dot = TextDot(str(text[cell]), point)  # type: ignore
            dot.FontHeight = fontheight
            dot.FontFace = fontface

            guid = sc.doc.Objects.AddTextDot(dot, attr)
            guids.append(guid)

        if group:
            self.add_to_group(group, guids)

        return guids

    # =============================================================================
    # draw normals
    # =============================================================================

    # =============================================================================
    # draw miscellaneous
    # =============================================================================
