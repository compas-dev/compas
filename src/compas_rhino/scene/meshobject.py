from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import Rhino  # type: ignore
import scriptcontext as sc  # type: ignore

import compas_rhino.objects
from compas.colors import Color
from compas.geometry import Line
from compas.geometry import Point
from compas.geometry import centroid_points
from compas.scene import MeshObject
from compas_rhino.conversions import line_to_rhino
from compas_rhino.conversions import point_to_rhino

# from compas_rhino.conversions import transformation_to_rhino
from compas_rhino.conversions import vertices_and_faces_to_rhino

from .helpers import ngon
from .sceneobject import RhinoSceneObject


class RhinoMeshObject(RhinoSceneObject, MeshObject):
    """Scene object for drawing mesh data structures.

    Parameters
    ----------
    disjoint : bool, optional
        Draw the faces of the mesh disjointed.
    **kwargs : dict, optional
        Additional keyword arguments.

    Attributes
    ----------
    disjoint : bool, optional
        Draw the faces of the mesh disjointed.
        Default is ``False``.

    """

    def __init__(self, mesh, disjoint=False, vertexgroup=None, edgegroup=None, facegroup=None, **kwargs):
        super(RhinoMeshObject, self).__init__(**kwargs)
        self.disjoint = disjoint
        self._guid_mesh = None
        self._guids_faces = None
        self._guids_edges = None
        self._guids_vertices = None
        self._guids_vertexnormals = None
        self._guids_facenormals = None
        self._guids_vertexlabels = None
        self._guids_edgelabels = None
        self._guids_facelabels = None
        self._guids_spheres = None
        self._guids_pipes = None
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

    def clear_vertexnormals(self):
        """Delete all vertex normals drawn by this scene object.

        Returns
        -------
        None

        """
        compas_rhino.objects.delete_objects(self._guids_vertexnormals, purge=True)

    def clear_facenormals(self):
        """Delete all face normals drawn by this scene object.

        Returns
        -------
        None

        """
        compas_rhino.objects.delete_objects(self._guids_facenormals, purge=True)

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
            if len(self.vertexcolor):
                vertexcolors = [self.vertexcolor[vertex] for vertex in self.mesh.vertices()]

            facecolors = []
            if len(self.facecolor):
                facecolors = [self.facecolor[face] for face in self.mesh.faces()]

            vertex_index = self.mesh.vertex_index()
            vertex_xyz = self.vertex_xyz

            vertices = [vertex_xyz[vertex] for vertex in self.mesh.vertices()]
            faces = [[vertex_index[vertex] for vertex in self.mesh.face_vertices(face)] for face in self.mesh.faces()]

            geometry = vertices_and_faces_to_rhino(
                vertices,
                faces,
                color=self.color,
                vertexcolors=vertexcolors,
                facecolors=facecolors,
                disjoint=self.disjoint,
            )

            # geometry.Transform(transformation_to_rhino(self.worldtransformation))

            self._guid_mesh = sc.doc.Objects.AddMesh(geometry, attr)
            if self.group:
                self.add_to_group(self.group, [self._guid_mesh])

            self._guids.append(self._guid_mesh)

        elif self.show_faces:
            self._guids += self.draw_faces()

        if self.show_vertices:
            self._guids += self.draw_vertices()

        if self.show_edges:
            self._guids += self.draw_edges()

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

        if vertices:
            for vertex in vertices:
                name = "{}.vertex.{}".format(self.mesh.name, vertex)
                color = self.vertexcolor[vertex]
                attr = self.compile_attributes(name=name, color=color)

                point = point_to_rhino(self.vertex_xyz[vertex])

                guid = sc.doc.Objects.AddPoint(point, attr)
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

        edges = list(self.mesh.edges()) if self.show_edges is True else self.show_edges or []

        if edges:
            for edge in edges:
                name = "{}.edge.{}-{}".format(self.mesh.name, *edge)
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
            The GUIDs of the created Rhino mesh objects.

        """
        guids = []

        faces = list(self.mesh.faces()) if self.show_faces is True else self.show_faces or []

        if faces:
            for face in faces:
                name = "{}.face.{}".format(self.mesh.name, face)
                color = self.facecolor[face]
                attr = self.compile_attributes(name=name, color=color)

                vertices = [self.vertex_xyz[vertex] for vertex in self.mesh.face_vertices(face)]  # type: ignore
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

        for vertex in text:
            name = "{}.vertex.{}.label".format(self.mesh.name, vertex)  # type: ignore
            color = self.vertexcolor[vertex]
            attr = self.compile_attributes(name=name, color=color)

            point = point_to_rhino(self.vertex_xyz[vertex])

            dot = Rhino.Geometry.TextDot(str(text[vertex]), point)  # type: ignore
            dot.FontHeight = fontheight
            dot.FontFace = fontface

            guid = sc.doc.Objects.AddTextDot(dot, attr)
            guids.append(guid)

        if group:
            self.add_to_group(group, guids)

        self._guids_vertexlabels = guids

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

        for edge in text:
            name = "{}.edge.{}-{}".format(self.mesh.name, *edge)  # type: ignore
            color = self.edgecolor[edge]
            attr = self.compile_attributes(name="{}.label".format(name), color=color)

            line = Line(self.vertex_xyz[edge[0]], self.vertex_xyz[edge[1]])
            point = point_to_rhino(line.midpoint)

            dot = Rhino.Geometry.TextDot(str(text[edge]), point)  # type: ignore
            dot.FontHeight = fontheight
            dot.FontFace = fontface

            guid = sc.doc.Objects.AddTextDot(dot, attr)
            guids.append(guid)

        if group:
            self.add_to_group(group, guids)

        self._guids_edgelabels = guids

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

        for face in text:
            name = "{}.face.{}.label".format(self.mesh.name, face)  # type: ignore
            color = self.facecolor[face]
            attr = self.compile_attributes(name=name, color=color)

            points = [self.vertex_xyz[vertex] for vertex in self.mesh.face_vertices(face)]  # type: ignore
            point = point_to_rhino(centroid_points(points))

            dot = Rhino.Geometry.TextDot(str(text[face]), point)  # type: ignore
            dot.FontHeight = fontheight
            dot.FontFace = fontface

            guid = sc.doc.Objects.AddTextDot(dot, attr)
            guids.append(guid)

        if group:
            self.add_to_group(group, guids)

        self._guids_facelabels = guids

        return guids

    # ==========================================================================
    # draw normals
    # ==========================================================================

    def draw_vertexnormals(self, vertices=None, color=(0, 255, 0), scale=1.0, group=None):
        """Draw the normals at the vertices of the mesh.

        Parameters
        ----------
        vertices : list[int], optional
            A selection of vertex normals to draw.
            Default is to draw all vertex normals.
        color : tuple[int, int, int] | tuple[float, float, float] | :class:`compas.colors.Color`, optional
            The color specification of the normal vectors.
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

        color = Color.coerce(color)

        for vertex in vertices or self.mesh.vertices():  # type: ignore
            name = "{}.vertex.{}.normal".format(self.mesh.name, vertex)  # type: ignore
            attr = self.compile_attributes(name=name, color=color)

            point = Point(*self.vertex_xyz[vertex])
            normal = self.mesh.vertex_normal(vertex)  # type: ignore

            guid = sc.doc.Objects.AddLine(point_to_rhino(point), point_to_rhino(point + normal * scale), attr)
            guids.append(guid)

        if group:
            self.add_to_group(group, guids)

        self._guids_vertexnormals = guids

        return guids

    def draw_facenormals(self, faces=None, color=(0, 255, 255), scale=1.0, group=None):
        """Draw the normals of the faces.

        Parameters
        ----------
        faces : list[int], optional
            A selection of face normals to draw.
            Default is to draw all face normals.
        color : tuple[int, int, int] | tuple[float, float, float] | :class:`compas.colors.Color`, optional
            The color specification of the normal vectors.
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

        color = Color.coerce(color)

        for face in faces or self.mesh.faces():  # type: ignore
            name = "{}.face.{}.normal".format(self.mesh.name, face)  # type: ignore
            attr = self.compile_attributes(name=name, color=color)

            point = Point(*centroid_points([self.vertex_xyz[vertex] for vertex in self.mesh.face_vertices(face)]))  # type: ignore
            normal = self.mesh.face_normal(face)  # type: ignore

            guid = sc.doc.Objects.AddLine(point_to_rhino(point), point_to_rhino(point + normal * scale), attr)
            guids.append(guid)

        if group:
            self.add_to_group(group, guids)

        self._guids_facenormals = guids

        return guids
