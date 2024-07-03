from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import scriptcontext as sc  # type: ignore
from Rhino.Geometry import TextDot  # type: ignore

import compas_rhino.objects
from compas.geometry import Line
from compas.geometry import centroid_points
from compas.scene import VolMeshObject
from compas_rhino.conversions import line_to_rhino
from compas_rhino.conversions import point_to_rhino
from compas_rhino.conversions import vertices_and_faces_to_rhino

from .helpers import ngon
from .sceneobject import RhinoSceneObject


class RhinoVolMeshObject(RhinoSceneObject, VolMeshObject):
    """Scene object for drawing volmesh data structures.

    Parameters
    ----------
    disjoint : bool, optional
        Draw the faces of the mesh disjointed.
        Default is ``True``.
    vertexgroup : str, optional
        The name of the group for the vertices.
    edgegroup : str, optional
        The name of the group for the edges.
    facegroup : str, optional
        The name of the group for the faces.
    cellgroup : str, optional
        The name of the group for the cells.
    **kwargs : dict, optional
        Additional keyword arguments.

    Attributes
    ----------
    disjoint : bool
        Draw the faces of the mesh disjointed.
        Default is ``True``.
    vertexgroup : str
        The name of the group for the vertices.
    edgegroup : str
        The name of the group for the edges.
    facegroup : str
        The name of the group for the faces.
    cellgroup : str
        The name of the group for the cells.

    """

    def __init__(self, disjoint=True, vertexgroup=None, edgegroup=None, facegroup=None, cellgroup=None, **kwargs):
        super(RhinoVolMeshObject, self).__init__(**kwargs)
        self.disjoint = disjoint
        self._guids_vertices = None
        self._guids_edges = None
        self._guids_faces = None
        self._guids_cells = None
        self._guids_vertexlabels = None
        self._guids_edgelabels = None
        self._guids_facelabels = None
        self._guids_celllabels = None
        self.vertexgroup = vertexgroup
        self.edgegroup = edgegroup
        self.facegroup = facegroup
        self.cellgroup = cellgroup

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
            guids += self.draw_vertices()
        if self.show_edges:
            guids += self.draw_edges()
        if self.show_faces:
            guids += self.draw_faces()
        if self.show_cells:
            guids += self.draw_cells()

        self._guids = guids

        return self.guids

    def draw_vertices(self):
        """Draw a selection of vertices.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino point objects.

        """
        guids = []

        vertices = list(self.volmesh.vertices()) if self.show_vertices is True else self.show_vertices or []

        if vertices:
            for vertex in vertices:
                name = "{}.vertex.{}".format(self.volmesh.name, vertex)
                color = self.vertexcolor[vertex]
                attr = self.compile_attributes(name=name, color=color)

                point = self.vertex_xyz[vertex]

                guid = sc.doc.Objects.AddPoint(point_to_rhino(point), attr)
                guids.append(guid)

        if guids:
            if self.vertexgroup:
                self.add_to_group(self.vertexgroup, guids)
            elif self.group:
                self.add_to_group(self.group, guids)

        self._guids_vertices = guids
        return guids

    def draw_edges(self):
        """Draw a selection of edges.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino line objects.

        """
        guids = []

        edges = list(self.volmesh.edges()) if self.show_edges is True else self.show_edges or []

        if edges:
            for edge in edges:
                name = "{}.edge.{}-{}".format(self.volmesh.name, *edge)
                color = self.edgecolor[edge]
                attr = self.compile_attributes(name=name, color=color)

                line = Line(self.vertex_xyz[edge[0]], self.vertex_xyz[edge[1]])

                guid = sc.doc.Objects.AddLine(line_to_rhino(line), attr)
                guids.append(guid)

        if guids:
            if self.edgegroup:
                self.add_to_group(self.edgegroup, guids)
            elif self.group:
                self.add_to_group(self.group, guids)

        self._guids_edges = guids
        return guids

    def draw_faces(self):
        """Draw a selection of faces.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino objects.

        """
        guids = []

        faces = list(self.volmesh.faces()) if self.show_faces is True else self.show_faces or []

        if faces:
            for face in faces:
                name = "{}.face.{}".format(self.volmesh.name, face)
                color = self.facecolor[face]
                attr = self.compile_attributes(name=name, color=color)

                vertices = [self.vertex_xyz[vertex] for vertex in self.volmesh.face_vertices(face)]
                facet = ngon(len(vertices))

                if facet:
                    guid = sc.doc.Objects.AddMesh(vertices_and_faces_to_rhino(vertices, [facet]), attr)
                    guids.append(guid)

        if guids:
            if self.facegroup:
                self.add_to_group(self.facegroup, guids)
            elif self.group:
                self.add_to_group(self.group, guids)

        self._guids_faces = guids
        return guids

    def draw_cells(self):
        """Draw a selection of cells.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino objects.
            Every cell is drawn as an individual mesh.

        """
        guids = []

        cells = list(self.volmesh.cells()) if self.show_cells is True else self.show_cells or []

        if cells:
            for cell in cells:
                name = "{}.cell.{}".format(self.volmesh.name, cell)
                color = self.cellcolor[cell]
                attr = self.compile_attributes(name=name, color=color)

                vertices = self.volmesh.cell_vertices(cell)
                faces = self.volmesh.cell_faces(cell)
                vertex_index = dict((vertex, index) for index, vertex in enumerate(vertices))

                vertices = [self.vertex_xyz[vertex] for vertex in vertices]
                faces = [[vertex_index[vertex] for vertex in self.volmesh.halfface_vertices(face)] for face in faces]

                guid = sc.doc.Objects.AddMesh(vertices_and_faces_to_rhino(vertices, faces, disjoint=self.disjoint), attr)
                guids.append(guid)

        if guids:
            if self.cellgroup:
                self.add_to_group(self.cellgroup, guids)
            elif self.group:
                self.add_to_group(self.group, guids)

        self._guids_cells = guids
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
            color = self.vertexcolor[vertex]
            attr = self.compile_attributes(name=name, color=color)

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
            color = self.edgecolor[edge]
            attr = self.compile_attributes(name="{}.label".format(name), color=color)

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
            color = self.facecolor[face]
            attr = self.compile_attributes(name="{}.label".format(name), color=color)

            vertices = [self.vertex_xyz[vertex] for vertex in self.volmesh.face_vertices(face)]  # type: ignore
            point = point_to_rhino(centroid_points(vertices))

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
            color = self.cellcolor[cell]
            attr = self.compile_attributes(name="{}.label".format(name), color=color)

            vertices = [self.vertex_xyz[vertex] for vertex in self.volmesh.cell_vertices(cell)]  # type: ignore
            point = point_to_rhino(centroid_points(vertices))

            dot = TextDot(str(text[cell]), point)  # type: ignore
            dot.FontHeight = fontheight
            dot.FontFace = fontface

            guid = sc.doc.Objects.AddTextDot(dot, attr)
            guids.append(guid)

        if group:
            self.add_to_group(group, guids)

        return guids
