from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import bpy  # type: ignore

import compas_blender
from compas.datastructures import Mesh
from compas.geometry import Line
from compas.geometry import Sphere
from compas.geometry import Cylinder
from compas.geometry import add_vectors
from compas.geometry import centroid_points
from compas.geometry import scale_vector
from compas.colors import Color

from compas.scene import MeshObject as BaseMeshObject
from .artist import BlenderArtist

from compas_blender import conversions


class MeshArtist(BlenderArtist, BaseMeshObject):
    """Artist for drawing mesh data structures in Blender.

    Parameters
    ----------
    mesh : :class:`compas.datastructures.Mesh`
        A COMPAS mesh.

    """

    def __init__(self, mesh: Mesh, **kwargs: Any):
        super().__init__(mesh=mesh, **kwargs)
        self.vertexobjects = []
        self.edgeobjects = []
        self.faceobjects = []

    # ==========================================================================
    # clear
    # ==========================================================================

    def clear(self):
        compas_blender.delete_objects(self.objects)

    def clear_vertices(self):
        """Clear the vertex objects.

        Returns
        -------
        None

        """
        compas_blender.delete_objects(self.vertexobjects)

    def clear_edges(self):
        """Clear the edge objects.

        Returns
        -------
        None

        """
        compas_blender.delete_objects(self.edgeobjects)

    def clear_faces(self):
        """Clear the face objects.

        Returns
        -------
        None

        """
        compas_blender.delete_objects(self.faceobjects)

    # ==========================================================================
    # draw
    # ==========================================================================

    def draw(
        self, color: Optional[Color] = None, collection: Optional[str] = None, show_wire: bool = True
    ) -> bpy.types.Object:
        """Draw the mesh.

        Parameters
        ----------
        color : :class:`compas.colors.Color`, optional
            The color of the mesh.
        collection : str, optional
            The name of the collection that should contain the mesh.
        show_wire : bool, optional
            Display the wireframe of the mesh.

        Returns
        -------
        list[:blender:`bpy.types.Object`]

        """
        name = self.mesh.name  # type: ignore
        color = Color.coerce(color) or self.color
        mesh = conversions.mesh_to_blender(self.mesh)  # type: ignore

        obj = self.create_object(mesh, name=name)
        self.update_object(obj, color=color, collection=collection, show_wire=show_wire)

        return obj

    def draw_vertices(
        self,
        vertices: Optional[List[int]] = None,
        color: Optional[Union[Color, Dict[int, Color]]] = None,
        collection: Optional[str] = None,
        radius: float = 0.01,
        u: int = 16,
        v: int = 16,
    ) -> List[bpy.types.Object]:
        """Draw a selection of vertices.

        Parameters
        ----------
        vertices : list[int], optional
            A list of vertex keys identifying which vertices to draw.
            Default is None, in which case all vertices are drawn.
        color : :class:`compas.colors.Color` | dict[int, :class:`compas.colors.Color`], optional
            The color specification for the vertices.
        collection : str, optional
            The name of the Blender scene collection containing the created object(s).

        Other Parameters
        ----------------
        radius : float, optional
            The radius of the vertex spheres.
        u : int, optional
            Number of faces in the "u" direction of the vertex spheres.
        v : int, optional
            Number of faces in the "v" direction of the vertex spheres.

        Returns
        -------
        list[:blender:`bpy.types.Object`]

        """
        objects = []

        self.vertex_color = color

        for vertex in vertices or self.mesh.vertices():  # type: ignore
            name = f"{self.mesh.name}.vertex.{vertex}"  # type: ignore
            color = self.vertex_color[vertex]  # type: ignore
            point = self.vertex_xyz[vertex]

            # there is no such thing as a sphere data block
            bpy.ops.mesh.primitive_uv_sphere_add(location=point, radius=radius, segments=u, ring_count=v)
            obj = bpy.context.object
            self.objects.append(obj)
            self.update_object(obj, name=name, color=color, collection=collection)  # type: ignore
            objects.append(obj)

        return objects

    def draw_edges(
        self,
        edges: Optional[List[Tuple[int, int]]] = None,
        color: Optional[Union[Color, Dict[Tuple[int, int], Color]]] = None,
        collection: Optional[str] = None,
    ) -> List[bpy.types.Object]:
        """Draw a selection of edges.

        Parameters
        ----------
        edges : list[tuple[int, int]], optional
            A list of edge keys (as uv pairs) identifying which edges to draw.
            The default is None, in which case all edges are drawn.
        color : :class:`compas.colors.Color` | dict[tuple[int, int], :class:`compas.colors.Color`], optional
            The color specification for the edges.
        collection : str, optional
            The name of the Blender scene collection containing the created object(s).

        Returns
        -------
        list[:blender:`bpy.types.Object`]

        """
        objects = []

        self.edge_color = color

        for u, v in edges or self.mesh.edges():  # type: ignore
            name = f"{self.mesh.name}.edge.{u}-{v}"  # type: ignore
            color = self.edge_color[u, v]  # type: ignore
            curve = conversions.line_to_blender_curve(Line(self.vertex_xyz[u], self.vertex_xyz[v]))

            obj = self.create_object(curve, name=name)
            self.update_object(obj, color=color, collection=collection)  # type: ignore
            objects.append(obj)

        return objects

    def draw_faces(
        self,
        faces: Optional[List[int]] = None,
        color: Optional[Union[Color, Dict[int, Color]]] = None,
        collection: Optional[str] = None,
        show_wire: bool = True,
    ) -> List[bpy.types.Object]:
        """Draw a selection of faces.

        Parameters
        ----------
        faces : list[int], optional
            A list of face keys identifying which faces to draw.
            The default is None, in which case all faces are drawn.
        color : :class:`compas.colors.Color` | dict[int, :class:`compas.colors.Color`], optional
            The color specification for the faces.
        collection : str, optional
            The name of the Blender scene collection containing the created object(s).
        show_wire : bool, optional
            Display the wireframe of the faces.

        Returns
        -------
        list[:blender:`bpy.types.Object`]

        """
        objects = []

        self.face_color = color

        for face in faces or self.mesh.faces():  # type: ignore
            name = f"{self.mesh.name}.face.{face}"  # type: ignore
            color = self.face_color[face]  # type: ignore
            points = [self.vertex_xyz[vertex] for vertex in self.mesh.face_vertices(face)]  # type: ignore
            mesh = conversions.polygon_to_blender_mesh(points, name=name)  # type: ignore

            obj = self.create_object(mesh, name=name)
            self.update_object(obj, color=color, collection=collection, show_wire=show_wire)  # type: ignore
            objects.append(obj)

        return objects

    # ==========================================================================
    # draw normals
    # ==========================================================================

    def draw_vertexnormals(
        self,
        vertices: Optional[List[int]] = None,
        color: Color = Color.green(),
        scale: float = 1.0,
        collection: Optional[str] = None,
    ) -> List[bpy.types.Object]:
        """Draw the normals at the vertices of the mesh.

        Parameters
        ----------
        vertices : list[int], optional
            A selection of vertex normals to draw.
            Default is to draw all vertex normals.
        color : :class:`compas.colors.Color`, optional
            The color specification of the normal vectors.
        scale : float, optional
            Scale factor for the vertex normals.
        collection : str, optional
            The name of the Blender scene collection containing the created object(s).

        Returns
        -------
        list[:blender:`bpy.types.Object`]

        """
        objects = []

        color = Color.coerce(color)  # type: ignore

        for vertex in vertices or self.mesh.vertices():  # type: ignore
            name = f"{self.mesh.name}.vertex.{vertex}.normal"  # type: ignore

            a = self.vertex_xyz[vertex]
            n = self.mesh.vertex_normal(vertex)  # type: ignore
            b = add_vectors(a, scale_vector(n, scale))

            curve = conversions.line_to_blender_curve(Line(a, b))

            obj = self.create_object(curve, name=name)
            self.update_object(obj, color=color, collection=collection)

            objects.append(obj)

        return objects

    def draw_facenormals(
        self,
        faces: Optional[List[List[int]]] = None,
        color: Color = Color.cyan(),
        scale: float = 1.0,
        collection: Optional[str] = None,
    ) -> List[bpy.types.Object]:
        """Draw the normals of the faces.

        Parameters
        ----------
        faces : list[int], optional
            A selection of face normals to draw.
            Default is to draw all face normals.
        color : :class:`compas.colors.Color`, optional
            The color specification of the normal vectors.
        scale : float, optional
            Scale factor for the face normals.
        collection : str, optional
            The name of the Blender scene collection containing the created object(s).

        Returns
        -------
        list[:blender:`bpy.types.Object`]

        """
        objects = []

        color = Color.coerce(color)  # type: ignore

        for face in faces or self.mesh.faces():  # type: ignore
            name = f"{self.mesh.name}.face.{face}.normal"  # type: ignore

            a = centroid_points([self.vertex_xyz[vertex] for vertex in self.mesh.face_vertices(face)])  # type: ignore
            n = self.mesh.face_normal(face)  # type: ignore
            b = add_vectors(a, scale_vector(n, scale))

            curve = conversions.line_to_blender_curve(Line(a, b))

            obj = self.create_object(curve, name=name)
            self.update_object(obj, color=color, collection=collection)

            objects.append(obj)

        return objects

    # ==========================================================================
    # draw labels
    # ==========================================================================

    # def draw_vertexlabels(self, text: Optional[Dict[int, str]] = None) -> List[bpy.types.Object]:
    #     """Draw labels for a selection vertices.

    #     Parameters
    #     ----------
    #     text : dict[int, str], optional
    #         A dictionary of vertex labels as vertex-text pairs.
    #         The default value is None, in which case every vertex will be labeled with its identifier.

    #     Returns
    #     -------
    #     list[:blender:`bpy.types.Object`]

    #     """
    #     self.vertex_text = text
    #     labels = []
    #     for vertex in self.vertex_text:
    #         labels.append(
    #             {
    #                 "pos": self.vertex_xyz[vertex],
    #                 "name": f"{self.mesh.name}.vertexlabel.{vertex}",
    #                 "text": self.vertex_text[vertex],
    #                 "color": self.vertex_color[vertex],
    #             }
    #         )
    #     return compas_blender.draw_texts(labels, collection=self.vertexlabelcollection)

    # def draw_edgelabels(self, text: Optional[Dict[Tuple[int, int], str]] = None) -> List[bpy.types.Object]:
    #     """Draw labels for a selection of edges.

    #     Parameters
    #     ----------
    #     text : dict[tuple[int, int], str], optional
    #         A dictionary of edge labels as edge-text pairs.
    #         The default value is None, in which case every edge will be labeled with its identifier.

    #     Returns
    #     -------
    #     list[:blender:`bpy.types.Object`]

    #     """
    #     self.edge_text = text
    #     labels = []
    #     for edge in self.edge_text:
    #         u, v = edge
    #         labels.append(
    #             {
    #                 "pos": centroid_points([self.vertex_xyz[u], self.vertex_xyz[v]]),
    #                 "name": f"{self.mesh.name}.edgelabel.{u}-{v}",
    #                 "text": self.edge_text[edge],
    #                 "color": self.edge_color[edge],
    #             }
    #         )
    #     return compas_blender.draw_texts(labels, collection=self.edgelabelcollection)

    # def draw_facelabels(self, text: Optional[Dict[int, str]] = None) -> List[bpy.types.Object]:
    #     """Draw labels for a selection of faces.

    #     Parameters
    #     ----------
    #     text : dict[int, str], optional
    #         A dictionary of face labels as face-text pairs.
    #         The default value is None, in which case every face will be labeled with its identifier.

    #     Returns
    #     -------
    #     list[:blender:`bpy.types.Object`]

    #     """
    #     self.face_text = text
    #     labels = []
    #     for face in self.face_text:
    #         labels.append(
    #             {
    #                 "pos": centroid_points([self.vertex_xyz[vertex] for vertex in self.mesh.face_vertices(face)]),
    #                 "name": "{}.facelabel.{}".format(self.mesh.name, face),
    #                 "text": self.face_text[face],
    #                 "color": self.face_color[face],
    #             }
    #         )
    #     return compas_blender.draw_texts(labels, collection=self.collection)

    # =============================================================================
    # draw miscellaneous
    # =============================================================================

    def draw_spheres(
        self,
        radius: Dict[int, float],
        color: Optional[Union[Color, Dict[int, Color]]] = None,
        collection: Optional[str] = None,
    ) -> list[bpy.types.Object]:
        """Draw spheres at the vertices of the mesh.

        Parameters
        ----------
        radius : dict[int, float], optional
            The radius of the spheres.
        color : tuple[int, int, int] | tuple[float, float, float] | :class:`compas.colors.Color` | dict[int, :class:`compas.colors.Color`], optional
            The color of the spheres.
        collection : str, optional
            The name of the Blender scene collection containing the created object(s).

        Returns
        -------
        list[:blender:`bpy.types.Object`]

        """
        objects = []

        self.vertex_color = color

        for vertex in radius:
            name = "{}.vertex.{}.sphere".format(self.mesh.name, vertex)  # type: ignore
            color = self.vertex_color[vertex]  # type: ignore

            sphere = Sphere.from_point_and_radius(self.vertex_xyz[vertex], radius[vertex])
            geometry = conversions.sphere_to_blender_mesh(sphere, name=name)

            obj = self.create_object(geometry, name=name)
            self.update_object(obj, color=color, collection=collection)  # type: ignore

            objects.append(obj)

        return objects

    def draw_pipes(
        self,
        radius: Dict[Tuple[int, int], float],
        color: Optional[Union[Color, Dict[int, Color]]] = None,
        collection: Optional[str] = None,
    ) -> list[bpy.types.Object]:
        """Draw pipes around the edges of the mesh.

        Parameters
        ----------
        radius : dict[tuple[int, int], float]
            The radius per edge.
        color : tuple[int, int, int] | tuple[float, float, float] | :class:`compas.colors.Color` | dict[tuple[int, int], :class:`compas.colors.Color`], optional
            The color of the pipes.
        collection : str, optional
            The name of the Blender scene collection containing the created object(s).

        Returns
        -------
        list[:blender:`bpy.types.Object`]

        """
        objects = []

        self.edge_color = color

        for u, v in radius:
            name = "{}.edge.{}-{}.pipe".format(self.mesh.name, u, v)  # type: ignore
            color = self.edge_color[u, v]  # type: ignore

            line = Line(self.vertex_xyz[u], self.vertex_xyz[v])
            cylinder = Cylinder.from_line_and_radius(line, radius[u, v])  # type: ignore
            geometry = conversions.cylinder_to_blender_mesh(cylinder)

            obj = self.create_object(geometry, name=name)
            self.update_object(obj, color=color, collection=collection)  # type: ignore

            objects.append(obj)

        return objects
