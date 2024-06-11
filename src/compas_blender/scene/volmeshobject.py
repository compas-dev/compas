from typing import Any
from typing import List

import bpy  # type: ignore

import compas_blender
import compas_blender.objects
from compas.geometry import Line
from compas.geometry import Sphere
from compas.scene import VolMeshObject as BaseVolMeshObject
from compas_blender import conversions

from .sceneobject import BlenderSceneObject


class VolMeshObject(BlenderSceneObject, BaseVolMeshObject):
    """A scene object for drawing volumetric mesh data structures in Blender.

    Parameters
    ----------
    vertex_u : int, optional
        Number of segments in the U direction of the vertex spheres.
        Default is ``16``.
    vertex_v : int, optional
        Number of segments in the V direction of the vertex spheres.
        Default is ``16``.
    **kwargs : dict, optional
        Additional keyword arguments.

    Attributes
    ----------
    vertex_u : int
        Number of segments in the U direction of the vertex spheres.
    vertex_v : int
        Number of segments in the V direction of the vertex spheres.
    vertexobjects : list[:class:`bpy.types.Object`]
        The Blender objects representing the vertices.
    edgeobjects : list[:class:`bpy.types.Object`]
        The Blender objects representing the edges.
    faceobjects : list[:class:`bpy.types.Object`]
        The Blender objects representing the faces.
    cellobjects : list[:class:`bpy.types.Object`]
        The Blender objects representing the cells.

    """

    def __init__(self, vertex_u=16, vertex_v=16, **kwargs: Any):
        super().__init__(**kwargs)
        self.vertexobjects = []
        self.edgeobjects = []
        self.faceobjects = []
        self.cellobjects = []
        self.vertex_u = vertex_u
        self.vertex_v = vertex_v

    # ==========================================================================
    # clear
    # ==========================================================================

    def clear(self):
        compas_blender.objects.delete_objects(self.objects)

    def clear_vertices(self):
        """Clear the objects contained in the vertex collection (``self.vertexcollection``).

        Returns
        -------
        None

        """
        compas_blender.objects.delete_objects(self.vertexobjects)

    def clear_edges(self):
        """Clear the objects contained in the edge collection (``self.edgecollection``).

        Returns
        -------
        None

        """
        compas_blender.objects.delete_objects(self.edgeobjects)

    def clear_faces(self):
        """Clear the objects contained in the face collection (``self.facecollection``).

        Returns
        -------
        None

        """
        compas_blender.objects.delete_objects(self.faceobjects)

    def clear_cells(self):
        """Clear the objects contained in the cell collection (``self.cellcollection``).

        Returns
        -------
        None

        """
        compas_blender.objects.delete_objects(self.cellobjects)

    # ==========================================================================
    # draw
    # ==========================================================================

    def draw(self) -> list[bpy.types.Object]:
        """Draw a selection of cells.

        Returns
        -------
        list[:blender:`bpy.types.Object`]
            The objects created in Blender.

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

    def draw_vertices(self) -> List[bpy.types.Object]:
        """Draw a selection of vertices.

        Returns
        -------
        list[:blender:`bpy.types.Object`]

        """
        objects = []

        vertices = list(self.volmesh.vertices()) if self.show_vertices is True else self.show_vertices or []

        for vertex in vertices:
            name = f"{self.volmesh.name}.vertex.{vertex}"
            color = self.vertexcolor[vertex]
            point = self.volmesh.vertex_coordinates(vertex)

            sphere = Sphere(radius=self.vertexsize, point=point)
            sphere.resolution_u = self.vertex_u
            sphere.resolution_v = self.vertex_v
            mesh = conversions.vertices_and_faces_to_blender_mesh(sphere.vertices, sphere.faces, name=name)
            obj = self.create_object(mesh, name=name)
            self.update_object(obj, color=color, collection=self.collection)
            objects.append(obj)

        self.vertexobjects = objects
        return objects

    def draw_edges(self) -> List[bpy.types.Object]:
        """Draw a selection of edges.

        Returns
        -------
        list[:blender:`bpy.types.Object`]

        """
        objects = []

        edges = list(self.volmesh.edges()) if self.show_edges is True else self.show_edges or []

        for u, v in edges:
            name = f"{self.volmesh.name}.edge.{u}-{v}"
            color = self.edgecolor[u, v]
            curve = conversions.line_to_blender_curve(Line(self.volmesh.vertex_coordinates(u), self.volmesh.vertex_coordinates(v)))

            obj = self.create_object(curve, name=name)
            self.update_object(obj, color=color, collection=self.collection)
            objects.append(obj)

        self.edgeobjects = objects
        return objects

    def draw_faces(self) -> List[bpy.types.Object]:
        """Draw a selection of faces.

        Returns
        -------
        list[:blender:`bpy.types.Object`]

        """
        objects = []

        faces = list(self.volmesh.faces()) if self.show_faces is True else self.show_faces or []

        for face in faces:
            name = f"{self.volmesh.name}.face.{face}"
            color = self.facecolor[face]
            points = [self.volmesh.vertex_coordinates(vertex) for vertex in self.volmesh.face_vertices(face)]
            mesh = conversions.polygon_to_blender_mesh(points, name=name)

            obj = self.create_object(mesh, name=name)
            self.update_object(obj, color=color, collection=self.collection)
            objects.append(obj)

        self.faceobjects = objects
        return objects

    def draw_cells(self) -> List[bpy.types.Object]:
        """Draw a selection of cells.

        Returns
        -------
        list[:blender:`bpy.types.Object`]

        """
        objects = []

        cells = list(self.volmesh.cells()) if self.show_cells is True else self.show_cells or []

        for cell in cells:
            name = "{}.cell.{}".format(self.volmesh.name, cell)
            color = self.cellcolor[cell]

            vertices = self.volmesh.cell_vertices(cell)
            faces = self.volmesh.cell_faces(cell)
            vertex_index = dict((vertex, index) for index, vertex in enumerate(vertices))

            vertices = [self.volmesh.vertex_coordinates(vertex) for vertex in vertices]
            faces = [[vertex_index[vertex] for vertex in self.volmesh.halfface_vertices(face)] for face in faces]

            mesh = conversions.vertices_and_faces_to_blender_mesh(vertices, faces, name=name)

            obj = self.create_object(mesh, name=name)
            self.update_object(obj, color=color, collection=self.collection, show_wire=self.show_wire)

            objects.append(obj)

        return objects

    # ==========================================================================
    # draw normals
    # ==========================================================================

    # def draw_vertexnormals(
    #     self,
    #     vertices: Optional[List[int]] = None,
    #     color: Color = Color.green(),
    #     scale: float = 1.0,
    #     collection: Optional[str] = None,
    # ) -> List[bpy.types.Object]:
    #     """Draw the normals at the vertices of the mesh.

    #     Parameters
    #     ----------
    #     vertices : list[int], optional
    #         A selection of vertex normals to draw.
    #         Default is to draw all vertex normals.
    #     color : :class:`compas.colors.Color`, optional
    #         The color specification of the normal vectors.
    #     scale : float, optional
    #         Scale factor for the vertex normals.
    #     collection : str, optional
    #         The name of the Blender scene collection containing the created object(s).

    #     Returns
    #     -------
    #     list[:blender:`bpy.types.Object`]

    #     """
    #     objects = []

    #     color = Color.coerce(color)  # type: ignore

    #     for vertex in vertices or self.volmesh.vertices():  # type: ignore
    #         name = f"{self.volmesh.name}.vertex.{vertex}.normal"  # type: ignore

    #         a = self.volmesh.vertices_attributes("xyz")[vertex]
    #         n = self.volmesh.vertex_normal(vertex)  # type: ignore
    #         b = add_vectors(a, scale_vector(n, scale))

    #         curve = conversions.line_to_blender_curve(Line(a, b))

    #         obj = self.create_object(curve, name=name)
    #         self.update_object(obj, color=color, collection=collection)

    #         objects.append(obj)

    #     return objects

    # def draw_facenormals(
    #     self,
    #     faces: Optional[List[List[int]]] = None,
    #     color: Color = Color.cyan(),
    #     scale: float = 1.0,
    #     collection: Optional[str] = None,
    # ) -> List[bpy.types.Object]:
    #     """Draw the normals of the faces.

    #     Parameters
    #     ----------
    #     faces : list[int], optional
    #         A selection of face normals to draw.
    #         Default is to draw all face normals.
    #     color : :class:`compas.colors.Color`, optional
    #         The color specification of the normal vectors.
    #     scale : float, optional
    #         Scale factor for the face normals.
    #     collection : str, optional
    #         The name of the Blender scene collection containing the created object(s).

    #     Returns
    #     -------
    #     list[:blender:`bpy.types.Object`]

    #     """
    #     objects = []

    #     color = Color.coerce(color)  # type: ignore

    #     for face in faces or self.volmesh.faces():  # type: ignore
    #         name = f"{self.volmesh.name}.face.{face}.normal"  # type: ignore

    #         a = centroid_points([self.volmesh.vertices_attributes("xyz")[vertex] for vertex in self.volmesh.face_vertices(face)])  # type: ignore
    #         n = self.volmesh.face_normal(face)  # type: ignore
    #         b = add_vectors(a, scale_vector(n, scale))

    #         curve = conversions.line_to_blender_curve(Line(a, b))

    #         obj = self.create_object(curve, name=name)
    #         self.update_object(obj, color=color, collection=collection)

    #         objects.append(obj)

    #     return objects
