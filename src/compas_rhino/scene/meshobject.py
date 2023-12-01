from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from Rhino.Geometry import TextDot  # type: ignore
import scriptcontext as sc  # type: ignore

from compas.geometry import centroid_points
from compas.geometry import Point
from compas.geometry import Line
from compas.geometry import Cylinder
from compas.geometry import Sphere

import compas_rhino
from compas.scene import MeshObject as BaseMeshObject
from compas.colors import Color
from compas_rhino.conversions import vertices_and_faces_to_rhino
from compas_rhino.conversions import mesh_to_rhino
from compas_rhino.conversions import point_to_rhino
from compas_rhino.conversions import line_to_rhino
from compas_rhino.conversions import cylinder_to_rhino_brep
from compas_rhino.conversions import sphere_to_rhino
from compas_rhino.conversions import transformation_to_rhino
from .sceneobject import RhinoSceneObject
from ._helpers import attributes
from ._helpers import ngon


class MeshObject(RhinoSceneObject, BaseMeshObject):
    """Scene object for drawing mesh data structures.

    Parameters
    ----------
    mesh : :class:`compas.datastructures.Mesh`
        A COMPAS mesh.
    **kwargs : dict, optional
        Additional keyword arguments.

    """

    def __init__(self, mesh, **kwargs):
        super(MeshObject, self).__init__(mesh=mesh, **kwargs)

    # ==========================================================================
    # clear
    # ==========================================================================

    def clear(self):
        """Delete all objects drawn by this scene object.

        Returns
        -------
        None

        """
        guids = compas_rhino.get_objects(name="{}.*".format(self.mesh.name))  # type: ignore
        compas_rhino.delete_objects(guids, purge=True)

    def clear_vertices(self):
        """Delete all vertices drawn by this scene object.

        Returns
        -------
        None

        """
        guids = compas_rhino.get_objects(name="{}.vertex.*".format(self.mesh.name))  # type: ignore
        compas_rhino.delete_objects(guids, purge=True)

    def clear_edges(self):
        """Delete all edges drawn by this scene object.

        Returns
        -------
        None

        """
        guids = compas_rhino.get_objects(name="{}.edge.*".format(self.mesh.name))  # type: ignore
        compas_rhino.delete_objects(guids, purge=True)

    def clear_faces(self):
        """Delete all faces drawn by this scene object.

        Returns
        -------
        None

        """
        guids = compas_rhino.get_objects(name="{}.face.*".format(self.mesh.name))  # type: ignore
        compas_rhino.delete_objects(guids, purge=True)

    def clear_vertexnormals(self):
        """Delete all vertex normals drawn by this scene object.

        Returns
        -------
        None

        """
        guids = compas_rhino.get_objects(name="{}.vertex.*.normal".format(self.mesh.name))  # type: ignore
        compas_rhino.delete_objects(guids, purge=True)

    def clear_facenormals(self):
        """Delete all face normals drawn by this scene object.

        Returns
        -------
        None

        """
        guids = compas_rhino.get_objects(name="{}.face.*.normal".format(self.mesh.name))  # type: ignore
        compas_rhino.delete_objects(guids, purge=True)

    def clear_vertexlabels(self):
        """Delete all vertex labels drawn by this scene object.

        Returns
        -------
        None

        """
        guids = compas_rhino.get_objects(name="{}.vertex.*.label".format(self.mesh.name))  # type: ignore
        compas_rhino.delete_objects(guids, purge=True)

    def clear_edgelabels(self):
        """Delete all edge labels drawn by this scene object.

        Returns
        -------
        None

        """
        guids = compas_rhino.get_objects(name="{}.edge.*.label".format(self.mesh.name))  # type: ignore
        compas_rhino.delete_objects(guids, purge=True)

    def clear_facelabels(self):
        """Delete all face labels drawn by this scene object.

        Returns
        -------
        None

        """
        guids = compas_rhino.get_objects(name="{}.face.*.label".format(self.mesh.name))  # type: ignore
        compas_rhino.delete_objects(guids, purge=True)

    # ==========================================================================
    # draw
    # ==========================================================================

    def draw(self, color=None, vertexcolors=None, facecolors=None, disjoint=False):
        """Draw the mesh as a consolidated RhinoMesh.

        Parameters
        ----------
        color : tuple[int, int, int], optional
            The color of the mesh.
            Default is the value of :attr:`MeshObject.default_color`.
        disjoint : bool, optional
            If True, draw the faces of the mesh with disjoint vertices.

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

        color = Color.coerce(color) or self.color
        attr = attributes(name=self.mesh.name, color=color, layer=self.layer)  # type: ignore

        geometry = mesh_to_rhino(
            self.mesh,
            color=color,
            vertexcolors=vertexcolors,
            facecolors=facecolors,
            disjoint=disjoint,
        )

        if self.transformation:
            geometry.Transform(transformation_to_rhino(self.transformation))

        guid = sc.doc.Objects.AddMesh(geometry, attr)
        return [guid]

    def draw_vertices(self, vertices=None, color=None, group=None):
        """Draw a selection of vertices.

        Parameters
        ----------
        vertices : list[int], optional
            A selection of vertices to draw.
            Default is None, in which case all vertices are drawn.
        color : :class:`compas.colors.Color` | dict[int, :class:`compas.colors.Color`], optional
            The color of the vertices.
        group : str, optional
            The name of a group to join the created Rhino objects in.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino point objects.

        """
        guids = []

        self.vertex_color = color

        for vertex in vertices or self.mesh.vertices():  # type: ignore
            name = "{}.vertex.{}".format(self.mesh.name, vertex)  # type: ignore
            color = self.vertex_color[vertex]  # type: ignore
            attr = attributes(name=name, color=color, layer=self.layer)

            point = point_to_rhino(self.vertex_xyz[vertex])

            guid = sc.doc.Objects.AddPoint(point, attr)
            guids.append(guid)

        if group:
            self.add_to_group(group, guids)

        return guids

    def draw_edges(self, edges=None, color=None, text=None, fontheight=10, fontface="Arial Regular", group=None):
        """Draw a selection of edges.

        Parameters
        ----------
        edges : list[tuple[int, int]], optional
            A selection of edges to draw.
            The default is None, in which case all edges are drawn.
        color : :class:`compas.colors.Color` | dict[tuple[int, int], :class:`compas.colors.Color`], optional
            The color of the edges.
        text : dict[tuple[int, int], str], optional
            A dictionary of edge labels as edge-text pairs.
        fontheight : int, optional
            Font height of the edge labels.
        fontface : str, optional
            Font face of the edge labels.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino line objects.

        """
        guids = []

        self.edge_color = color

        for edge in edges or self.mesh.edges():  # type: ignore
            name = "{}.edge.{}-{}".format(self.mesh.name, *edge)  # type: ignore
            color = self.edge_color[edge]  # type: ignore
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
            A selection of faces to draw.
            The default is None, in which case all faces are drawn.
        color : :class:`compas.colors.Color` | dict[int, :class:`compas.colors.Color`], optional
            The color of the faces.
        text : dict[int, str], optional
            A dictionary of face labels as face-text pairs.
        fontheight : int, optional
            Font height of the face labels.
        fontface : str, optional
            Font face of the face labels.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino mesh objects.

        """
        guids = []

        self.face_color = color

        for face in faces or self.mesh.faces():  # type: ignore
            name = "{}.face.{}".format(self.mesh.name, face)  # type: ignore
            color = self.face_color[face]  # type: ignore
            attr = attributes(name=name, color=color, layer=self.layer)

            vertices = [self.vertex_xyz[vertex] for vertex in self.mesh.face_vertices(face)]  # type: ignore
            facet = ngon(len(vertices))

            if facet:
                guid = sc.doc.Objects.AddMesh(vertices_and_faces_to_rhino(vertices, [facet]), attr)
                guids.append(guid)

        if group:
            self.add_to_group(group, guids)

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

        self.vertex_color = color

        for vertex in text:
            name = "{}.vertex.{}.label".format(self.mesh.name, vertex)  # type: ignore
            color = self.vertex_color[vertex]  # type: ignore
            attr = attributes(name=name, color=color, layer=self.layer)

            point = point_to_rhino(self.vertex_xyz[vertex])

            dot = TextDot(str(text[vertex]), point)  # type: ignore
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

        self.edge_color = color

        for edge in text:
            name = "{}.edge.{}-{}".format(self.mesh.name, *edge)  # type: ignore
            color = self.edge_color[edge]  # type: ignore
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
            color = self.face_color[face]  # type: ignore
            attr = attributes(name=name, color=color, layer=self.layer)

            points = [self.vertex_xyz[vertex] for vertex in self.mesh.face_vertices(face)]  # type: ignore
            point = point_to_rhino(centroid_points(points))  # type: ignore

            dot = TextDot(str(text[face]), point)  # type: ignore
            dot.FontHeight = fontheight
            dot.FontFace = fontface

            guid = sc.doc.Objects.AddTextDot(dot, attr)
            guids.append(guid)

        if group:
            self.add_to_group(group, guids)

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
            attr = attributes(name=name, color=color, layer=self.layer)

            point = Point(*self.vertex_xyz[vertex])
            normal = self.mesh.vertex_normal(vertex)  # type: ignore

            guid = sc.doc.Objects.AddLine(point_to_rhino(point), point_to_rhino(point + normal * scale), attr)
            guids.append(guid)

        if group:
            self.add_to_group(group, guids)

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
            attr = attributes(name=name, color=color, layer=self.layer)

            point = Point(*centroid_points([self.vertex_xyz[vertex] for vertex in self.mesh.face_vertices(face)]))  # type: ignore
            normal = self.mesh.face_normal(face)  # type: ignore

            guid = sc.doc.Objects.AddLine(point_to_rhino(point), point_to_rhino(point + normal * scale), attr)
            guids.append(guid)

        if group:
            self.add_to_group(group, guids)

        return guids

    # ==========================================================================
    # draw miscellaneous
    # ==========================================================================

    def draw_spheres(self, radius, color=None, group=None):
        """Draw spheres at the vertices of the mesh.

        Parameters
        ----------
        radius : dict[int, float], optional
            The radius of the spheres.
        color : tuple[int, int, int] | tuple[float, float, float] | :class:`compas.colors.Color` | dict[int, :class:`compas.colors.Color`], optional
            The color of the spheres.
        group : str, optional
            The name of a group to join the created Rhino objects in.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino objects.

        """
        guids = []

        self.vertex_color = color

        for vertex in radius:
            name = "{}.vertex.{}.sphere".format(self.mesh.name, vertex)  # type: ignore
            color = self.vertex_color[vertex]  # type: ignore
            attr = attributes(name=name, color=color, layer=self.layer)

            sphere = Sphere.from_point_and_radius(self.vertex_xyz[vertex], radius[vertex])
            geometry = sphere_to_rhino(sphere)

            guid = sc.doc.Objects.AddSphere(geometry, attr)
            guids.append(guid)

        if group:
            self.add_to_group(group, guids)

        return guids

    def draw_pipes(self, radius, color=None, group=None):
        """Draw pipes around the edges of the mesh.

        Parameters
        ----------
        radius : dict[tuple[int, int], float]
            The radius per edge.
        color : tuple[int, int, int] | tuple[float, float, float] | :class:`compas.colors.Color` | dict[tuple[int, int], :class:`compas.colors.Color`], optional
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
            name = "{}.edge.{}-{}.pipe".format(self.mesh.name, *edge)  # type: ignore
            color = self.edge_color[edge]  # type: ignore
            attr = attributes(name=name, color=color, layer=self.layer)

            line = Line(self.vertex_xyz[edge[0]], self.vertex_xyz[edge[1]])
            cylinder = Cylinder.from_line_and_radius(line, radius[edge])
            brep = cylinder_to_rhino_brep(cylinder)

            guid = sc.doc.Objects.AddBrep(brep, attr)
            guids.append(guid)

        if group:
            self.add_to_group(group, guids)

        return guids
