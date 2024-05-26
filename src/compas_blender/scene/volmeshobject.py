from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import bpy  # type: ignore

import compas_blender
from compas.colors import Color
from compas.geometry import Line
from compas.geometry import add_vectors
from compas.geometry import centroid_points
from compas.geometry import scale_vector
from compas.scene import VolMeshObject as BaseVolMeshObject
from compas_blender import conversions

from .sceneobject import BlenderSceneObject


class VolMeshObject(BlenderSceneObject, BaseVolMeshObject):
    """A scene object for drawing volumetric mesh data structures in Blender.

    Parameters
    ----------
    volmesh : :class:`compas.datastructures.VolMesh`
        The volmesh data structure.
    **kwargs : dict, optional
        Additional keyword arguments.

    """

    def __init__(self, volmesh, **kwargs: Any):
        super().__init__(volmesh=volmesh, **kwargs)
        self.vertexobjects = []
        self.edgeobjects = []
        self.faceobjects = []
        self.cellobjects = []

    # ==========================================================================
    # clear
    # ==========================================================================

    def clear(self):
        compas_blender.delete_objects(self.objects)

    def clear_vertices(self):
        """Clear the objects contained in the vertex collection (``self.vertexcollection``).

        Returns
        -------
        None

        """
        compas_blender.delete_objects(self.vertexobjects)

    def clear_edges(self):
        """Clear the objects contained in the edge collection (``self.edgecollection``).

        Returns
        -------
        None

        """
        compas_blender.delete_objects(self.edgeobjects)

    def clear_faces(self):
        """Clear the objects contained in the face collection (``self.facecollection``).

        Returns
        -------
        None

        """
        compas_blender.delete_objects(self.faceobjects)

    def clear_cells(self):
        """Clear the objects contained in the cell collection (``self.cellcollection``).

        Returns
        -------
        None

        """
        compas_blender.delete_objects(self.cellobjects)

    # ==========================================================================
    # draw
    # ==========================================================================

    def draw(self, cells: Optional[List[int]] = None, color: Optional[Color] = None, collection: Optional[str] = None) -> list[bpy.types.Object]:
        """Draw a selection of cells.

        Parameters
        ----------
        cells : list[int], optional
            A list of cells to draw.
            The default is None, in which case all cells are drawn.
        color : :class:`compas.colors.Color` | dict[int, :class:`compas.colors.Color`], optional
            The color of the cells.
            The default color is :attr:`VolMeshObject.default_cellcolor`.
        collection : str, optional
            The name of the Blender scene collection containing the created object(s).

        Returns
        -------
        list[:blender:`bpy.types.Object`]
            The objects created in Blender.

        """
        self._guids = self.draw_cells(cells=cells, color=color, collection=collection)
        return self.guids

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
        radius : float, optional
            The radius of the spheres representing the vertices.
        u : int, optional
            Number of faces in the "u" direction of the spheres representing the vertices.
        v : int, optional
            Number of faces in the "v" direction of the spheres representing the vertices.

        Returns
        -------
        list[:blender:`bpy.types.Object`]

        """
        objects = []

        self.vertexcolor = color

        for vertex in vertices or self.volmesh.vertices():  # type: ignore
            name = f"{self.volmesh.name}.vertex.{vertex}"  # type: ignore
            color = self.vertexcolor[vertex]  # type: ignore
            point = self.volmesh.vertices_attributes("xyz")[vertex]

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
        color: Optional[Union[Color, Dict[int, Color]]] = None,
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

        self.edgecolor = color

        for u, v in edges or self.volmesh.edges():  # type: ignore
            name = f"{self.volmesh.name}.edge.{u}-{v}"  # type: ignore
            color = self.edgecolor[u, v]  # type: ignore
            curve = conversions.line_to_blender_curve(Line(self.volmesh.vertices_attributes("xyz")[u], self.volmesh.vertices_attributes("xyz")[v]))

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

        self.facecolor = color

        for face in faces or self.volmesh.faces():  # type: ignore
            name = f"{self.volmesh.name}.face.{face}"  # type: ignore
            color = self.facecolor[face]  # type: ignore
            points = [self.volmesh.vertices_attributes("xyz")[vertex] for vertex in self.volmesh.face_vertices(face)]  # type: ignore
            mesh = conversions.polygon_to_blender_mesh(points, name=name)  # type: ignore

            obj = self.create_object(mesh, name=name)
            self.update_object(obj, color=color, collection=collection, show_wire=show_wire)  # type: ignore
            objects.append(obj)

        return objects

    def draw_cells(
        self,
        cells: Optional[List[int]] = None,
        color: Optional[Union[Color, Dict[int, Color]]] = None,
        collection: Optional[str] = None,
        show_wire: bool = True,
    ) -> List[bpy.types.Object]:
        """Draw a selection of cells.

        Parameters
        ----------
        cells : list[int], optional
            A list of cells to draw.
            The default is None, in which case all cells are drawn.
        color : :class:`compas.colors.Color` | dict[int, :class:`compas.colors.Color`], optional
            The color of the cells.
        collection : str, optional
            The name of the Blender scene collection containing the created object(s).
        show_wire : bool, optional
            Display the wireframe of the cells.

        Returns
        -------
        list[:blender:`bpy.types.Object`]

        """
        objects = []

        self.cellcolor = color

        for cell in cells or self.volmesh.cells():  # type: ignore
            name = f"{self.volmesh.name}.cell.{cell}"  # type: ignore
            color = self.cellcolor[cell]  # type: ignore

            vertices = self.volmesh.cell_vertices(cell)  # type: ignore
            faces = self.volmesh.cell_faces(cell)  # type: ignore
            vertex_index = dict((vertex, index) for index, vertex in enumerate(vertices))

            vertices = [self.volmesh.vertices_attributes("xyz")[vertex] for vertex in vertices]
            faces = [[vertex_index[vertex] for vertex in self.volmesh.halfface_vertices(face)] for face in faces]  # type: ignore

            mesh = conversions.vertices_and_faces_to_blender_mesh(vertices, faces, name=name)  # type: ignore

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

        for vertex in vertices or self.volmesh.vertices():  # type: ignore
            name = f"{self.volmesh.name}.vertex.{vertex}.normal"  # type: ignore

            a = self.volmesh.vertices_attributes("xyz")[vertex]
            n = self.volmesh.vertex_normal(vertex)  # type: ignore
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

        for face in faces or self.volmesh.faces():  # type: ignore
            name = f"{self.volmesh.name}.face.{face}.normal"  # type: ignore

            a = centroid_points([self.volmesh.vertices_attributes("xyz")[vertex] for vertex in self.volmesh.face_vertices(face)])  # type: ignore
            n = self.volmesh.face_normal(face)  # type: ignore
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
    #                 "pos": self.volmesh.vertices_attributes("xyz")[vertex],
    #                 "name": f"{self.volmesh.name}.vertexlabel.{vertex}",
    #                 "text": self.vertex_text[vertex],
    #                 "color": self.vertexcolor[vertex],
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
    #                 "pos": centroid_points([self.volmesh.vertices_attributes("xyz")[u], self.volmesh.vertices_attributes("xyz")[v]]),
    #                 "name": f"{self.volmesh.name}.edgelabel.{u}-{v}",
    #                 "text": self.edge_text[edge],
    #                 "color": self.edgecolor[edge],
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
    #                 "pos": centroid_points([self.volmesh.vertices_attributes("xyz")[vertex] for vertex in self.volmesh.face_vertices(face)]),
    #                 "name": "{}.facelabel.{}".format(self.volmesh.name, face),
    #                 "text": self.face_text[face],
    #                 "color": self.facecolor[face],
    #             }
    #         )
    #     return compas_blender.draw_texts(labels, collection=self.collection)
