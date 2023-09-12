from typing import Optional
from typing import Union
from typing import Any
from typing import List
from typing import Dict
from typing import Tuple

import bpy

import compas_blender

from compas.geometry import add_vectors
from compas.geometry import scale_vector
from compas.geometry import centroid_points

from compas.artists import VolMeshArtist
from compas.colors import Color
from .artist import BlenderArtist


class VolMeshArtist(BlenderArtist, VolMeshArtist):
    """An artist for drawing volumetric mesh data structures in Blender.

    Parameters
    ----------
    volmesh : :class:`~compas.datastructures.VolMesh`
        The volmesh data structure.
    collection : str | :blender:`bpy.types.Collection`
        The Blender scene collection the object(s) created by this artist belong to.
    **kwargs : dict, optional
        Additional keyword arguments.
        For more info,
        see :class:`~compas_blender.artists.BlenderArtist` and :class:`~compas.artists.MeshArtist`.

    """

    def __init__(
        self,
        volmesh,
        collection: Optional[Union[str, bpy.types.Collection]] = None,
        **kwargs: Any,
    ):

        super().__init__(volmesh=volmesh, collection=collection or volmesh.name, **kwargs)

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
    def cellcollection(self) -> bpy.types.Collection:
        if not self._cellcollection:
            self._cellcollection = compas_blender.create_collection("Cells", parent=self.collection)
        return self._cellcollection

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

    @property
    def celllabelcollection(self) -> bpy.types.Collection:
        if not self._celllabelcollection:
            self._celllabelcollection = compas_blender.create_collection("CellLabels", parent=self.collection)
        return self._celllabelcollection

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

    def clear_cells(self):
        """Clear the objects contained in the cell collection (``self.cellcollection``).

        Returns
        -------
        None

        """
        compas_blender.delete_objects(self.facecollection.objects)

    # clear the labels

    # ==========================================================================
    # draw
    # ==========================================================================

    def draw(self, cells: Optional[List[int]] = None, color: Optional[Color] = None) -> List[bpy.types.Object]:
        """Draw a selection of cells.

        Parameters
        ----------
        cells : list[int], optional
            A list of cells to draw.
            The default is None, in which case all cells are drawn.
        color : :class:`~compas.colors.Color` | dict[int, :class:`~compas.colors.Color`], optional
            The color of the cells.
            The default color is :attr:`VolMeshArtist.default_cellcolor`.

        Returns
        -------
        list[:blender:`bpy.types.Object`]

        """
        return self.draw_cells(cells=cells, color=color)

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
                    "points": [self.vertex_xyz[vertex] for vertex in self.volmesh.face_vertices(face)],
                    "name": f"{self.volmesh.name}.face.{face}",
                    "color": self.face_color[face],
                }
            )
        return compas_blender.draw_faces(facets, self.facecollection)

    def draw_cells(
        self,
        cells: Optional[List[int]] = None,
        color: Optional[Union[Color, Dict[int, Color]]] = None,
    ) -> List[bpy.types.Object]:
        """Draw a selection of cells.

        Parameters
        ----------
        cells : list[int], optional
            A list of cells to draw.
            The default is None, in which case all cells are drawn.
        color : :class:`~compas.colors.Color` | dict[int, :class:`~compas.colors.Color`], optional
            The color of the cells.
            The default color is :attr:`VolMeshArtist.default_cellcolor`.

        Returns
        -------
        list[:blender:`bpy.types.Object`]

        """
        self.cell_color = color
        cells = cells or self.cells
        vertex_xyz = self.vertex_xyz
        meshes = []
        for cell in cells:
            vertices = self.volmesh.cell_vertices(cell)
            faces = self.volmesh.cell_faces(cell)
            vertex_index = dict((vertex, index) for index, vertex in enumerate(vertices))
            vertices = [vertex_xyz[vertex] for vertex in vertices]
            faces = [[vertex_index[vertex] for vertex in self.volmesh.halfface_vertices(face)] for face in faces]
            obj = compas_blender.draw_mesh(
                vertices,
                faces,
                name=f"{self.volmesh.name}.cell.{cell}",
                color=self.cell_color[cell],
                collection=self.cellcollection,
            )
            meshes.append(obj)
        return meshes

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
