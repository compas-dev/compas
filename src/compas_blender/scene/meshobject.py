from typing import Any
from typing import List
from typing import Optional

import bpy  # type: ignore

import compas_blender
import compas_blender.objects
from compas.colors import Color
from compas.datastructures import Mesh
from compas.geometry import Line
from compas.geometry import Sphere
from compas.geometry import add_vectors
from compas.geometry import centroid_points
from compas.geometry import scale_vector
from compas.scene import MeshObject as BaseMeshObject
from compas_blender import conversions

from .sceneobject import BlenderSceneObject


class MeshObject(BlenderSceneObject, BaseMeshObject):
    """Scene object for drawing mesh data structures in Blender.

    Parameters
    ----------
    mesh : :class:`compas.datastructures.Mesh`
        A COMPAS mesh.

    """

    def __init__(self, mesh: Mesh, vertex_u=16, vertex_v=16, **kwargs: Any):
        super().__init__(mesh=mesh, **kwargs)
        self.vertexobjects = []
        self.edgeobjects = []
        self.faceobjects = []
        self.vertex_u = vertex_u
        self.vertex_v = vertex_v

    # ==========================================================================
    # clear
    # ==========================================================================

    def clear(self):
        compas_blender.objects.delete_objects(self.objects)

    def clear_vertices(self):
        """Clear the vertex objects.

        Returns
        -------
        None

        """
        compas_blender.objects.delete_objects(self.vertexobjects)

    def clear_edges(self):
        """Clear the edge objects.

        Returns
        -------
        None

        """
        compas_blender.objects.delete_objects(self.edgeobjects)

    def clear_faces(self):
        """Clear the face objects.

        Returns
        -------
        None

        """
        compas_blender.objects.delete_objects(self.faceobjects)

    # ==========================================================================
    # draw
    # ==========================================================================

    def draw(self) -> list[bpy.types.Object]:
        """Draw the mesh.

        Returns
        -------
        list[:blender:`bpy.types.Object`]
            The objects created in Blender.

        """
        self._guids = []

        if self.show_faces is True:
            name = self.mesh.name  # type: ignore
            color = self.color
            mesh = conversions.mesh_to_blender(self.mesh)  # type: ignore

            obj = self.create_object(mesh, name=name)
            self.update_object(obj, color=color, collection=self.collection, show_wire=self.show_wire)

            self._guids.append(obj)

        elif self.show_faces:
            self._guids += self.draw_faces()

        if self.show_vertices:
            self._guids += self.draw_vertices()

        if self.show_edges:
            self._guids += self.draw_edges()

        return self.guids

    def draw_vertices(self) -> List[bpy.types.Object]:
        """Draw a selection of vertices.

        Returns
        -------
        list[:blender:`bpy.types.Object`]

        """
        objects = []

        vertices = list(self.mesh.vertices()) if self.show_vertices is True else self.show_vertices or []

        for vertex in vertices:
            name = f"{self.mesh.name}.vertex.{vertex}"
            color = self.vertexcolor[vertex]
            point = self.vertex_xyz[vertex]

            # # there is no such thing as a sphere data block
            # bpy.ops.mesh.primitive_uv_sphere_add(location=point, radius=radius, segments=u, ring_count=v)
            # obj = bpy.context.object
            # self.update_object(obj, name=name, color=color, collection=collection)  # type: ignore

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

        edges = list(self.mesh.edges()) if self.show_edges is True else self.show_edges or []

        for u, v in edges:
            name = f"{self.mesh.name}.edge.{u}-{v}"
            color = self.edgecolor[u, v]
            curve = conversions.line_to_blender_curve(Line(self.vertex_xyz[u], self.vertex_xyz[v]))

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

        faces = list(self.mesh.faces()) if self.show_faces is True else self.show_faces or []

        for face in faces:
            name = f"{self.mesh.name}.face.{face}"
            color = self.facecolor[face]
            points = [self.vertex_xyz[vertex] for vertex in self.mesh.face_vertices(face)]
            mesh = conversions.polygon_to_blender_mesh(points, name=name)

            obj = self.create_object(mesh, name=name)
            self.update_object(obj, color=color, collection=self.collection)
            objects.append(obj)

        self.faceobjects = objects
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

    #     for vertex in vertices or self.mesh.vertices():  # type: ignore
    #         name = f"{self.mesh.name}.vertex.{vertex}.normal"  # type: ignore

    #         a = self.vertex_xyz[vertex]
    #         n = self.mesh.vertex_normal(vertex)  # type: ignore
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

    #     for face in faces or self.mesh.faces():  # type: ignore
    #         name = f"{self.mesh.name}.face.{face}.normal"  # type: ignore

    #         a = centroid_points([self.vertex_xyz[vertex] for vertex in self.mesh.face_vertices(face)])  # type: ignore
    #         n = self.mesh.face_normal(face)  # type: ignore
    #         b = add_vectors(a, scale_vector(n, scale))

    #         curve = conversions.line_to_blender_curve(Line(a, b))

    #         obj = self.create_object(curve, name=name)
    #         self.update_object(obj, color=color, collection=collection)

    #         objects.append(obj)

    #     return objects
