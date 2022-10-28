from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import bpy

import compas_blender
from compas.datastructures import Mesh
from compas.geometry import add_vectors
from compas.geometry import centroid_points
from compas.geometry import scale_vector

from compas.colors import Color
from compas.artists import MeshArtist
from .artist import BlenderArtist


class MeshArtist(BlenderArtist, MeshArtist):
    """Artist for drawing mesh data structures in Blender.

    Parameters
    ----------
    mesh : :class:`~compas.datastructures.Mesh`
        A COMPAS mesh.
    collection : str | :blender:`bpy.types.Collection`
        The Blender scene collection the object(s) created by this artist belong to.

    Attributes
    ----------
    vertexcollection : :blender:`bpy.types.Collection`
        The collection containing the vertices.
    edgecollection : :blender:`bpy.types.Collection`
        The collection containing the edges.
    facecollection : :blender:`bpy.types.Collection`
        The collection containing the faces.
    vertexlabelcollection : :blender:`bpy.types.Collection`
        The collection containing the vertex labels.
    edgelabelcollection : :blender:`bpy.types.Collection`
        The collection containing the edge labels.
    facelabelcollection : :blender:`bpy.types.Collection`
        The collection containing the face labels.

    Examples
    --------
    Use the Blender artist explicitly.

    .. code-block:: python

        from compas.datastructures import Mesh
        from compas_blender.artists import MeshArtist

        mesh = Mesh.from_meshgrid(10, 10)

        artist = MeshArtist(mesh)
        artist.draw()

    Or, use the artist through the plugin mechanism.

    .. code-block:: python

        from compas.datastructures import Mesh
        from compas.artists import Artist

        mesh = Mesh.from_meshgrid(10, 10)

        artist = Artist(mesh)
        artist.draw()

    """

    def __init__(
        self,
        mesh: Mesh,
        collection: Optional[Union[str, bpy.types.Collection]] = None,
        **kwargs: Any,
    ):

        super().__init__(mesh=mesh, collection=collection or mesh.name, **kwargs)

    @property
    def vertexcollection(self) -> bpy.types.Collection:
        if not self._vertexcollection:
            self._vertexcollection = compas_blender.create_collection("Vertices", parent=self.collection)
        return self._vertexcollection

    @property
    def edgecollection(self) -> bpy.types.Collection:
        if not self._edgecollection:
            self._edgecollection = compas_blender.create_collection("Edges", parent=self.collection)
        return self._edgecollection

    @property
    def facecollection(self) -> bpy.types.Collection:
        if not self._facecollection:
            self._facecollection = compas_blender.create_collection("Faces", parent=self.collection)
        return self._facecollection

    @property
    def vertexnormalcollection(self) -> bpy.types.Collection:
        if not self._vertexnormalcollection:
            self._vertexnormalcollection = compas_blender.create_collection("VertexNormals", parent=self.collection)
        return self._vertexnormalcollection

    @property
    def facenormalcollection(self) -> bpy.types.Collection:
        if not self._facenormalcollection:
            self._facenormalcollection = compas_blender.create_collection("FaceNormals", parent=self.collection)
        return self._facenormalcollection

    @property
    def vertexlabelcollection(self) -> bpy.types.Collection:
        if not self._vertexlabelcollection:
            self._vertexlabelcollection = compas_blender.create_collection("VertexLabels", parent=self.collection)
        return self._vertexlabelcollection

    @property
    def edgelabelcollection(self) -> bpy.types.Collection:
        if not self._edgelabelcollection:
            self._edgelabelcollection = compas_blender.create_collection("EdgeLabels", parent=self.collection)
        return self._edgelabelcollection

    @property
    def facelabelcollection(self) -> bpy.types.Collection:
        if not self._facelabelcollection:
            self._facelabelcollection = compas_blender.create_collection("FaceLabels", parent=self.collection)
        return self._facelabelcollection

    # ==========================================================================
    # clear
    # ==========================================================================

    def clear(self):
        compas_blender.delete_objects(self.collection.objects)

    def clear_vertices(self):
        """Clear the objects contained in the vertex collection (``self.vertexcollection``).

        Returns
        -------
        None

        """
        compas_blender.delete_objects(self.vertexcollection.objects)

    def clear_edges(self):
        """Clear the objects contained in the edge collection (``self.edgecollection``).

        Returns
        -------
        None

        """
        compas_blender.delete_objects(self.edgecollection.objects)

    def clear_faces(self):
        """Clear the objects contained in the face collection (``self.facecollection``).

        Returns
        -------
        None

        """
        compas_blender.delete_objects(self.facecollection.objects)

    # ==========================================================================
    # draw
    # ==========================================================================

    def draw(self, color: Optional[Color] = None) -> List[bpy.types.Object]:
        """Draw the mesh.

        Parameters
        ----------
        color : :class:`~compas.colors.Color`, optional
            The color of the mesh.
            The default value is :attr:`color`.

        Returns
        -------
        list[:blender:`bpy.types.Object`]

        """
        self.color = color
        vertices, faces = self.mesh.to_vertices_and_faces()
        obj = compas_blender.draw_mesh(
            vertices,
            faces,
            color=self.color,
            name=self.mesh.name,
            collection=self.collection,
        )
        return [obj]

    def draw_vertices(
        self,
        vertices: Optional[List[int]] = None,
        color: Optional[Union[Color, Dict[int, Color]]] = None,
    ) -> List[bpy.types.Object]:
        """Draw a selection of vertices.

        Parameters
        ----------
        vertices : list[int], optional
            A list of vertex keys identifying which vertices to draw.
            Default is None, in which case all vertices are drawn.
        color : :class:`~compas.colors.Color` | dict[int, :class:`~compas.colors.Color`], optional
            The color specification for the vertices.
            The default color of vertices is :attr:`default_vertexcolor`.

        Returns
        -------
        list[:blender:`bpy.types.Object`]

        """
        self.vertex_color = color
        vertices = vertices or self.vertices
        points = []
        for vertex in vertices:
            points.append(
                {
                    "pos": self.vertex_xyz[vertex],
                    "name": f"{self.mesh.name}.vertex.{vertex}",
                    "color": self.vertex_color[vertex],
                    "radius": 0.01,
                }
            )
        return compas_blender.draw_points(points, self.vertexcollection)

    def draw_edges(
        self,
        edges: Optional[List[Tuple[int, int]]] = None,
        color: Optional[Union[Color, Dict[int, Color]]] = None,
    ) -> List[bpy.types.Object]:
        """Draw a selection of edges.

        Parameters
        ----------
        edges : list[tuple[int, int]], optional
            A list of edge keys (as uv pairs) identifying which edges to draw.
            The default is None, in which case all edges are drawn.
        color : :class:`~compas.colors.Color` | dict[tuple[int, int], :class:`~compas.colors.Color`], optional
            The color specification for the edges.
            The default color of edges is :attr:`default_edgecolor`.

        Returns
        -------
        list[:blender:`bpy.types.Object`]

        """
        self.edge_color = color
        edges = edges or self.edges
        lines = []
        for edge in edges:
            u, v = edge
            lines.append(
                {
                    "start": self.vertex_xyz[u],
                    "end": self.vertex_xyz[v],
                    "color": self.edge_color[edge],
                    "name": f"{self.mesh.name}.edge.{u}-{v}",
                }
            )
        return compas_blender.draw_lines(lines, self.edgecollection)

    def draw_faces(
        self,
        faces: Optional[List[int]] = None,
        color: Optional[Union[Color, Dict[int, Color]]] = None,
    ) -> List[bpy.types.Object]:
        """Draw a selection of faces.

        Parameters
        ----------
        faces : list[int], optional
            A list of face keys identifying which faces to draw.
            The default is None, in which case all faces are drawn.
        color : :class:`~compas.colors.Color` | dict[int, :class:`~compas.colors.Color`], optional
            The color specification for the faces.
            Th default color of faces is :attr:`default_facecolor`.

        Returns
        -------
        list[:blender:`bpy.types.Object`]

        """
        self.face_color = color
        faces = faces or self.faces
        facets = []
        for face in faces:
            facets.append(
                {
                    "points": [self.vertex_xyz[vertex] for vertex in self.mesh.face_vertices(face)],
                    "name": f"{self.mesh.name}.face.{face}",
                    "color": self.face_color[face],
                }
            )
        return compas_blender.draw_faces(facets, self.facecollection)

    # ==========================================================================
    # draw normals
    # ==========================================================================

    def draw_vertexnormals(
        self,
        vertices: Optional[List[int]] = None,
        color: Color = Color.green(),
        scale: float = 1.0,
    ) -> List[bpy.types.Object]:
        """Draw the normals at the vertices of the mesh.

        Parameters
        ----------
        vertices : list[int], optional
            A selection of vertex normals to draw.
            Default is to draw all vertex normals.
        color : :class:`~compas.colors.Color`, optional
            The color specification of the normal vectors.
        scale : float, optional
            Scale factor for the vertex normals.

        Returns
        -------
        list[:blender:`bpy.types.Object`]

        """
        vertices = vertices or self.vertices
        lines = []
        for vertex in vertices:
            a = self.vertex_xyz[vertex]
            n = self.mesh.vertex_normal(vertex)
            b = add_vectors(a, scale_vector(n, scale))
            lines.append(
                {
                    "start": a,
                    "end": b,
                    "color": color,
                    "name": f"{self.mesh.name}.vertexnormal.{vertex}",
                }
            )
        return compas_blender.draw_lines(lines, collection=self.vertexnormalcollection)

    def draw_facenormals(
        self,
        faces: Optional[List[List[int]]] = None,
        color: Color = Color.cyan(),
        scale: float = 1.0,
    ) -> List[bpy.types.Object]:
        """Draw the normals of the faces.

        Parameters
        ----------
        faces : list[int], optional
            A selection of face normals to draw.
            Default is to draw all face normals.
        color : :class:`~compas.colors.Color`, optional
            The color specification of the normal vectors.
        scale : float, optional
            Scale factor for the face normals.

        Returns
        -------
        list[:blender:`bpy.types.Object`]

        """
        faces = faces or self.faces
        lines = []
        for face in faces:
            a = centroid_points([self.vertex_xyz[vertex] for vertex in self.mesh.face_vertices(face)])
            n = self.mesh.face_normal(face)
            b = add_vectors(a, scale_vector(n, scale))
            lines.append(
                {
                    "start": a,
                    "end": b,
                    "name": f"{self.mesh.name}.facenormal.{face}",
                    "color": color,
                }
            )
        return compas_blender.draw_lines(lines, collection=self.facenormalcollection)

    # ==========================================================================
    # draw labels
    # ==========================================================================

    def draw_vertexlabels(self, text: Optional[Dict[int, str]] = None) -> List[bpy.types.Object]:
        """Draw labels for a selection vertices.

        Parameters
        ----------
        text : dict[int, str], optional
            A dictionary of vertex labels as vertex-text pairs.
            The default value is None, in which case every vertex will be labeled with its identifier.

        Returns
        -------
        list[:blender:`bpy.types.Object`]

        """
        self.vertex_text = text
        labels = []
        for vertex in self.vertex_text:
            labels.append(
                {
                    "pos": self.vertex_xyz[vertex],
                    "name": f"{self.mesh.name}.vertexlabel.{vertex}",
                    "text": self.vertex_text[vertex],
                    "color": self.vertex_color[vertex],
                }
            )
        return compas_blender.draw_texts(labels, collection=self.vertexlabelcollection)

    def draw_edgelabels(self, text: Optional[Dict[Tuple[int, int], str]] = None) -> List[bpy.types.Object]:
        """Draw labels for a selection of edges.

        Parameters
        ----------
        text : dict[tuple[int, int], str], optional
            A dictionary of edge labels as edge-text pairs.
            The default value is None, in which case every edge will be labeled with its identifier.

        Returns
        -------
        list[:blender:`bpy.types.Object`]

        """
        self.edge_text = text
        labels = []
        for edge in self.edge_text:
            u, v = edge
            labels.append(
                {
                    "pos": centroid_points([self.vertex_xyz[u], self.vertex_xyz[v]]),
                    "name": f"{self.mesh.name}.edgelabel.{u}-{v}",
                    "text": self.edge_text[edge],
                    "color": self.edge_color[edge],
                }
            )
        return compas_blender.draw_texts(labels, collection=self.edgelabelcollection)

    def draw_facelabels(self, text: Optional[Dict[int, str]] = None) -> List[bpy.types.Object]:
        """Draw labels for a selection of faces.

        Parameters
        ----------
        text : dict[int, str], optional
            A dictionary of face labels as face-text pairs.
            The default value is None, in which case every face will be labeled with its identifier.

        Returns
        -------
        list[:blender:`bpy.types.Object`]

        """
        self.face_text = text
        labels = []
        for face in self.face_text:
            labels.append(
                {
                    "pos": centroid_points([self.vertex_xyz[vertex] for vertex in self.mesh.face_vertices(face)]),
                    "name": "{}.facelabel.{}".format(self.mesh.name, face),
                    "text": self.face_text[face],
                    "color": self.face_color[face],
                }
            )
        return compas_blender.draw_texts(labels, collection=self.collection)
