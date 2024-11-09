from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import Rhino  # type: ignore
import scriptcontext as sc  # type: ignore

import compas_rhino.objects
from compas.colors import Color
from compas.geometry import Line
from compas.geometry import centroid_points
from compas.scene import MeshObject
from compas_rhino.conversions import line_to_rhino
from compas_rhino.conversions import point_to_rhino
from compas_rhino.conversions import transformation_to_rhino
from compas_rhino.conversions import vertices_and_faces_to_rhino

from .helpers import ngon
from .sceneobject import RhinoSceneObject


class RhinoMeshObject(RhinoSceneObject, MeshObject):
    """Scene object for drawing mesh data structures.

    Parameters
    ----------
    disjoint : bool, optional
        Draw the faces of the mesh disjointed.
        Default is ``False``.
    vertexgroup : str, optional
        The name of the group for the vertices.
    edgegroup : str, optional
        The name of the group for the edges.
    facegroup : str, optional
        The name of the group for the faces.
    **kwargs : dict, optional
        Additional keyword arguments.

    Attributes
    ----------
    disjoint : bool, optional
        Draw the faces of the mesh disjointed.
        Default is ``False``.
    vertexgroup : str, optional
        The name of the group for the vertices.
    edgegroup : str, optional
        The name of the group for the edges.
    facegroup : str, optional
        The name of the group for the faces.

    """

    def __init__(self, disjoint=False, vertexgroup=None, edgegroup=None, facegroup=None, **kwargs):
        super(RhinoMeshObject, self).__init__(**kwargs)
        self.disjoint = disjoint
        self._guid_mesh = None
        self._guid_face = {}
        self._guid_edge = {}
        self._guid_vertex = {}
        self.vertexgroup = vertexgroup
        self.edgegroup = edgegroup
        self.facegroup = facegroup

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
        self._guids = []

    def clear_vertices(self):
        """Delete all vertices drawn by this scene object.

        Returns
        -------
        None

        """
        compas_rhino.objects.delete_objects(self._guid_vertex, purge=True)
        self._guid_vertex = {}

    def clear_edges(self):
        """Delete all edges drawn by this scene object.

        Returns
        -------
        None

        """
        compas_rhino.objects.delete_objects(self._guid_edge, purge=True)
        self._guid_edge = {}

    def clear_faces(self):
        """Delete all faces drawn by this scene object.

        Returns
        -------
        None

        """
        compas_rhino.objects.delete_objects(self._guid_face, purge=True)
        self._guid_face = {}

    # ==========================================================================
    # draw
    # ==========================================================================

    def draw(self):
        """Draw the mesh or its components in Rhino.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino objects.

        Notes
        -----
        The mesh should be a valid Rhino Mesh object, which means it should have only triangular or quadrilateral faces.
        Faces with more than 4 vertices will be triangulated on-the-fly.

        """
        # when drawing the actual mesh
        # vertex colors or face colors have to be provided as lists with colors for all vertices or faces
        # when drawing the mesh as individual components (vertices, edges, faces)
        # colors have to be provided as dicts that map colors to specific components

        self._guids = []

        if self.show_faces is True:
            attr = self.compile_attributes()

            vertexcolors = []
            if len(self.vertexcolor):  # type: ignore
                vertexcolors = [self.vertexcolor[vertex] for vertex in self.mesh.vertices()]  # type: ignore

            facecolors = []
            if len(self.facecolor):  # type: ignore
                facecolors = [self.facecolor[face] for face in self.mesh.faces()]  # type: ignore

            vertex_index = self.mesh.vertex_index()

            vertices = [self.mesh.vertex_attributes(vertex, "xyz") for vertex in self.mesh.vertices()]
            faces = [[vertex_index[vertex] for vertex in self.mesh.face_vertices(face)] for face in self.mesh.faces()]

            geometry = vertices_and_faces_to_rhino(
                vertices,
                faces,
                color=self.color,
                vertexcolors=vertexcolors,
                facecolors=facecolors,
                disjoint=self.disjoint,
            )

            geometry.Transform(transformation_to_rhino(self.worldtransformation))

            self._guid_mesh = sc.doc.Objects.AddMesh(geometry, attr)
            if self.group:
                self.add_to_group(self.group, [self._guid_mesh])

            self._guids.append(self._guid_mesh)

        elif self.show_faces:
            self.draw_faces()

        self.draw_vertices()
        self.draw_edges()

        return self.guids

    def draw_vertices(self):
        """Draw a selection of vertices.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino point objects.

        """
        guids = []

        vertices = list(self.mesh.vertices()) if self.show_vertices is True else self.show_vertices or []

        transformation = transformation_to_rhino(self.worldtransformation)

        if vertices:
            for vertex in vertices:
                name = "{}.vertex.{}".format(self.mesh.name, vertex)
                color = self.vertexcolor[vertex]  # type: ignore
                attr = self.compile_attributes(name=name, color=color)

                geometry = point_to_rhino(self.mesh.vertex_attributes(vertex, "xyz"))
                geometry.Transform(transformation)

                guid = sc.doc.Objects.AddPoint(geometry, attr)
                guids.append(guid)

        if guids:
            if self.vertexgroup:
                self.add_to_group(self.vertexgroup, guids)
            elif self.group:
                self.add_to_group(self.group, guids)

        self._guid_vertex = dict(zip(guids, vertices))

        self._guids += guids
        return guids

    def draw_edges(self):
        """Draw a selection of edges.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino line objects.

        """
        guids = []

        edges = list(self.mesh.edges()) if self.show_edges is True else self.show_edges or []

        transformation = transformation_to_rhino(self.worldtransformation)

        if edges:
            for edge in edges:
                name = "{}.edge.{}-{}".format(self.mesh.name, *edge)
                color = self.edgecolor[edge]  # type: ignore
                attr = self.compile_attributes(name=name, color=color)

                line = self.mesh.edge_line(edge)

                geometry = line_to_rhino(line)
                geometry.Transform(transformation)

                guid = sc.doc.Objects.AddLine(geometry, attr)
                guids.append(guid)

        if guids:
            if self.edgegroup:
                self.add_to_group(self.edgegroup, guids)
            elif self.group:
                self.add_to_group(self.group, guids)

        self._guid_edge = dict(zip(guids, edges))

        self._guids += guids
        return guids

    def draw_faces(self):
        """Draw a selection of faces.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino mesh objects.

        """
        guids = []

        faces = list(self.mesh.faces()) if self.show_faces is True else self.show_faces or []

        transformation = transformation_to_rhino(self.worldtransformation)

        if faces:
            for face in faces:
                name = "{}.face.{}".format(self.mesh.name, face)
                color = self.facecolor[face]  # type: ignore
                attr = self.compile_attributes(name=name, color=color)

                vertices = [self.mesh.vertex_attributes(vertex, "xyz") for vertex in self.mesh.face_vertices(face)]  # type: ignore
                facet = ngon(len(vertices))

                if facet:
                    geometry = vertices_and_faces_to_rhino(vertices, [facet])
                    geometry.Transform(transformation)

                    guid = sc.doc.Objects.AddMesh(geometry, attr)
                    guids.append(guid)

        if guids:
            if self.facegroup:
                self.add_to_group(self.facegroup, guids)
            elif self.group:
                self.add_to_group(self.group, guids)

        self._guid_face = dict(zip(guids, faces))

        self._guids += guids
        return guids

    # ==========================================================================
    # draw labels
    # ==========================================================================

    def draw_vertexlabels(self, text, color=None, group=None, fontheight=10, fontface="Arial Regular"):
        """Draw labels for a selection of vertices.

        Parameters
        ----------
        text : dict[int, str]
            A dictionary of vertex labels as vertex-text pairs.
        color : :class:`compas.colors.Color` | dict[int, :class:`compas.colors.Color`], optional
            The color of the vertex labels.
        group : str, optional
            The name of a group to join the created Rhino objects in.
        fontheight : int, optional
            Font height of the vertex labels.
        fontface : str, optional
            Font face of the vertex labels.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino point objects.

        """
        guids = []

        self.vertexcolor = color

        transformation = transformation_to_rhino(self.worldtransformation)

        for vertex in text:
            name = "{}.vertex.{}.label".format(self.mesh.name, vertex)  # type: ignore
            color = self.vertexcolor[vertex]  # type: ignore
            attr = self.compile_attributes(name=name, color=color)

            location = point_to_rhino(self.mesh.vertex_attributes(vertex, "xyz"))
            location.Transform(transformation)

            dot = Rhino.Geometry.TextDot(str(text[vertex]), location)  # type: ignore
            dot.FontHeight = fontheight
            dot.FontFace = fontface

            guid = sc.doc.Objects.AddTextDot(dot, attr)
            guids.append(guid)

        if group:
            self.add_to_group(group, guids)

        self._guids_vertexlabels = guids
        self._guids += guids
        return guids

    def draw_edgelabels(self, text, color=None, group=None, fontheight=10, fontface="Arial Regular"):
        """Draw labels for a selection of edges.

        Parameters
        ----------
        text : dict[tuple[int, int], str]
            A dictionary of edge labels as edge-text pairs.
        color : :class:`compas.colors.Color` | dict[tuple[int, int], :class:`compas.colors.Color`], optional
            The color of the edge labels.
        group : str, optional
            The name of a group to join the created Rhino objects in.
        fontheight : int, optional
            Font height of the edge labels.
        fontface : str, optional
            Font face of the edge labels.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino point objects.

        """
        guids = []

        self.edgecolor = color

        transformation = transformation_to_rhino(self.worldtransformation)

        for edge in text:
            name = "{}.edge.{}-{}".format(self.mesh.name, *edge)  # type: ignore
            color = self.edgecolor[edge]  # type: ignore
            attr = self.compile_attributes(name="{}.label".format(name), color=color)

            line = self.mesh.edge_line(edge)
            location = point_to_rhino(line.midpoint)
            location.Transform(transformation)

            dot = Rhino.Geometry.TextDot(str(text[edge]), location)  # type: ignore
            dot.FontHeight = fontheight
            dot.FontFace = fontface

            guid = sc.doc.Objects.AddTextDot(dot, attr)
            guids.append(guid)

        if group:
            self.add_to_group(group, guids)

        self._guids_edgelabels = guids
        self._guids += guids
        return guids

    def draw_facelabels(self, text, color=None, group=None, fontheight=10, fontface="Arial Regular"):
        """Draw labels for a selection of faces.

        Parameters
        ----------
        text : dict[int, str]
            A dictionary of face labels as face-text pairs.
        color : :class:`compas.colors.Color` | dict[int, :class:`compas.colors.Color`], optional
            The color of the face labels.
        group : str, optional
            The name of a group to join the created Rhino objects in.
        fontheight : int, optional
            Font height of the face labels.
        fontface : str, optional
            Font face of the face labels.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino point objects.

        """
        guids = []

        transformation = transformation_to_rhino(self.worldtransformation)

        for face in text:
            name = "{}.face.{}.label".format(self.mesh.name, face)  # type: ignore
            color = self.facecolor[face]  # type: ignore
            attr = self.compile_attributes(name=name, color=color)

            points = [self.mesh.vertex_attributes(vertex, "xyz") for vertex in self.mesh.face_vertices(face)]  # type: ignore
            location = point_to_rhino(centroid_points(points))
            location.Transform(transformation)

            dot = Rhino.Geometry.TextDot(str(text[face]), location)  # type: ignore
            dot.FontHeight = fontheight
            dot.FontFace = fontface

            guid = sc.doc.Objects.AddTextDot(dot, attr)
            guids.append(guid)

        if group:
            self.add_to_group(group, guids)

        self._guids_facelabels = guids
        self._guids += guids
        return guids

    # ==========================================================================
    # draw normals
    # ==========================================================================

    def draw_vertexnormals(self, color=None, scale=1.0, group=None):
        """Draw the normals at the vertices of the mesh.

        Parameters
        ----------
        color : tuple[int, int, int] | tuple[float, float, float] | :class:`compas.colors.Color`, optional
            The color specification of the normal vectors.
            If no  color is specified, the color of the corresponding vertex is used.
        scale : float, optional
            Scale factor for the vertex normals.
        group : str, optional
            The name of a group to join the created Rhino objects in.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino objects.

        """
        guids = []

        vertices = list(self.mesh.vertices()) if self.show_vertices is True else self.show_vertices or []
        transformation = transformation_to_rhino(self.worldtransformation)

        color = Color.coerce(color)

        for vertex in vertices:
            name = "{}.vertex.{}.normal".format(self.mesh.name, vertex)  # type: ignore
            attr = self.compile_attributes(name=name, color=color or self.vertexcolor[vertex])  # type: ignore

            point = self.mesh.vertex_point(vertex)
            normal = self.mesh.vertex_normal(vertex)  # type: ignore
            line = Line.from_point_and_vector(point, normal * scale)

            geometry = line_to_rhino(line)
            geometry.Transform(transformation)

            guid = sc.doc.Objects.AddLine(geometry, attr)
            guids.append(guid)

        if group:
            self.add_to_group(group, guids)

        self._guids_vertexnormals = guids
        self._guids += guids
        return guids

    def draw_facenormals(self, color=None, scale=1.0, group=None):
        """Draw the normals of the faces.

        Parameters
        ----------
        color : tuple[int, int, int] | tuple[float, float, float] | :class:`compas.colors.Color`, optional
            The color specification of the normal vectors.
            If no color is specified, the color of the corresponding face is used.
        scale : float, optional
            Scale factor for the face normals.
        group : str, optional
            The name of a group to join the created Rhino objects in.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino objects.

        """
        guids = []

        faces = list(self.mesh.faces()) if self.show_faces is True else self.show_faces or []
        transformation = transformation_to_rhino(self.worldtransformation)

        color = Color.coerce(color)

        for face in faces:
            name = "{}.face.{}.normal".format(self.mesh.name, face)  # type: ignore
            attr = self.compile_attributes(name=name, color=color or self.facecolor[face])  # type: ignore

            point = self.mesh.face_centroid(face)
            normal = self.mesh.face_normal(face)
            line = Line.from_point_and_vector(point, normal * scale)

            geometry = line_to_rhino(line)
            geometry.Transform(transformation)

            guid = sc.doc.Objects.AddLine(geometry, attr)
            guids.append(guid)

        if group:
            self.add_to_group(group, guids)

        self._guids_facenormals = guids

        return guids
