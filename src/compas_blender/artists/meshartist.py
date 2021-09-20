# from __future__ import annotations
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import bpy

from functools import partial

import compas_blender
from compas.datastructures import Mesh
from compas.geometry import add_vectors
from compas.geometry import centroid_points
from compas.geometry import scale_vector

from compas.utilities import color_to_colordict
from .artist import BlenderArtist

colordict = partial(color_to_colordict, colorformat='rgb', normalize=True)
Color = Union[Tuple[int, int, int], Tuple[float, float, float]]


class MeshArtist(BlenderArtist):
    """A mesh artist defines functionality for visualising COMPAS meshes in Blender.

    Parameters
    ----------
    mesh : :class:`compas.datastructures.Mesh`
        A COMPAS mesh.

    Attributes
    ----------
    mesh : :class:`compas.datastructures.Mesh`
        The COMPAS mesh associated with the artist.

    Examples
    --------
    .. code-block:: python

        import compas
        from compas.datastructures import Mesh
        from compas_blender.artists import MeshArtist

        mesh = Mesh.from_obj(compas.get('faces.obj'))

        MeshArtist(mesh).draw()

    """

    def __init__(self, mesh: Mesh):
        super().__init__()
        self._collection = None
        self._vertexcollection = None
        self._edgecollection = None
        self._facecollection = None
        self._vertexnormalcollection = None
        self._facenormalcollection = None
        self._vertexlabelcollection = None
        self._edgelabelcollection = None
        self._facelabelcollection = None
        self._object_vertex = {}
        self._object_edge = {}
        self._object_face = {}
        self._object_vertexnormal = {}
        self._object_facenormal = {}
        self._object_vertexlabel = {}
        self._object_edgelabel = {}
        self._object_facelabel = {}
        self.color_vertices = (1.0, 1.0, 1.0)
        self.color_edges = (0.0, 0.0, 0.0)
        self.color_faces = (0.7, 0.7, 0.7)
        self.show_vertices = True
        self.show_edges = True
        self.show_faces = True
        self.mesh = mesh

    @property
    def collection(self) -> bpy.types.Collection:
        if not self._collection:
            self._collection = compas_blender.create_collection(self.mesh.name)
        return self._collection

    @property
    def vertexcollection(self) -> bpy.types.Collection:
        path = f"{self.mesh.name}::Vertices"
        if not self._vertexcollection:
            self._vertexcollection = compas_blender.create_collections_from_path(path)[1]
        return self._vertexcollection

    @property
    def edgecollection(self) -> bpy.types.Collection:
        path = f"{self.mesh.name}::Edges"
        if not self._edgecollection:
            self._edgecollection = compas_blender.create_collections_from_path(path)[1]
        return self._edgecollection

    @property
    def facecollection(self) -> bpy.types.Collection:
        path = f"{self.mesh.name}::Faces"
        if not self._facecollection:
            self._facecollection = compas_blender.create_collections_from_path(path)[1]
        return self._facecollection

    @property
    def vertexnormalcollection(self) -> bpy.types.Collection:
        path = f"{self.mesh.name}::VertexNormals"
        if not self._vertexnormalcollection:
            self._vertexnormalcollection = compas_blender.create_collections_from_path(path)[1]
        return self._vertexnormalcollection

    @property
    def facenormalcollection(self) -> bpy.types.Collection:
        path = f"{self.mesh.name}::FaceNormals"
        if not self._facenormalcollection:
            self._facenormalcollection = compas_blender.create_collections_from_path(path)[1]
        return self._facenormalcollection

    @property
    def vertexlabelcollection(self) -> bpy.types.Collection:
        path = f"{self.mesh.name}::VertexLabels"
        if not self._vertexlabelcollection:
            self._vertexlabelcollection = compas_blender.create_collections_from_path(path)[1]
        return self._vertexlabelcollection

    @property
    def edgelabelcollection(self) -> bpy.types.Collection:
        path = f"{self.mesh.name}::EdgeLabels"
        if not self._edgelabelcollection:
            self._edgelabelcollection = compas_blender.create_collections_from_path(path)[1]
        return self._edgelabelcollection

    @property
    def facelabelcollection(self) -> bpy.types.Collection:
        path = f"{self.mesh.name}::FaceLabels"
        if not self._facelabelcollection:
            self._facelabelcollection = compas_blender.create_collections_from_path(path)[1]
        return self._facelabelcollection

    @property
    def object_vertex(self) -> Dict[bpy.types.Object, int]:
        """Map between Blender object objects and mesh vertex identifiers."""
        return self._object_vertex

    @object_vertex.setter
    def object_vertex(self, values):
        self._object_vertex = dict(values)

    @property
    def object_edge(self) -> Dict[bpy.types.Object, Tuple[int, int]]:
        """Map between Blender object objects and mesh edge identifiers."""
        return self._object_edge

    @object_edge.setter
    def object_edge(self, values):
        self._object_edge = dict(values)

    @property
    def object_face(self) -> Dict[bpy.types.Object, int]:
        """Map between Blender object objects and mesh face identifiers."""
        return self._object_face

    @object_face.setter
    def object_face(self, values):
        self._object_face = dict(values)

    @property
    def object_vertexnormal(self) -> Dict[bpy.types.Object, int]:
        """Map between Blender object objects and mesh vertex normal identifiers."""
        return self._object_vertexnormal

    @object_vertexnormal.setter
    def object_vertexnormal(self, values):
        self._object_vertexnormal = dict(values)

    @property
    def object_facenormal(self) -> Dict[bpy.types.Object, int]:
        """Map between Blender object objects and mesh face normal identifiers."""
        return self._object_facenormal

    @object_facenormal.setter
    def object_facenormal(self, values):
        self._object_facenormal = dict(values)

    @property
    def object_vertexlabel(self) -> Dict[bpy.types.Object, int]:
        """Map between Blender object objects and mesh vertex label identifiers."""
        return self._object_vertexlabel

    @object_vertexlabel.setter
    def object_vertexlabel(self, values):
        self._object_vertexlabel = dict(values)

    @property
    def object_edgelabel(self) -> Dict[bpy.types.Object, Tuple[int, int]]:
        """Map between Blender object objects and mesh edge label identifiers."""
        return self._object_edgelabel

    @object_edgelabel.setter
    def object_edgelabel(self, values):
        self._object_edgelabel = dict(values)

    @property
    def object_facelabel(self) -> Dict[bpy.types.Object, int]:
        """Map between Blender object objects and mesh face label identifiers."""
        return self._object_facelabel

    @object_facelabel.setter
    def object_facelabel(self, values):
        self._object_facelabel = dict(values)

    # ==========================================================================
    # clear
    # ==========================================================================

    def clear(self) -> None:
        """Clear all objects previously drawn by this artist.
        """
        objects = []
        objects += list(self.object_vertex)
        objects += list(self.object_edge)
        objects += list(self.object_face)
        objects += list(self.object_vertexnormal)
        objects += list(self.object_facenormal)
        objects += list(self.object_vertexlabel)
        objects += list(self.object_edgelabel)
        objects += list(self.object_facelabel)
        compas_blender.delete_objects(objects, purge_data=True)
        self._object_vertex = {}
        self._object_edge = {}
        self._object_face = {}
        self._object_vertexnormal = {}
        self._object_facenormal = {}
        self._object_vertexlabel = {}
        self._object_edgelabel = {}
        self._object_facelabel = {}

    # ==========================================================================
    # components
    # ==========================================================================

    def draw(self) -> None:
        """Draw the mesh using the chosen visualisation settings.

        Parameters
        ----------
        settings : dict, optional
            Dictionary of visualisation settings that will be merged with the settings of the artist.

        """
        self.clear()
        if self.show_vertices:
            self.draw_vertices()
        if self.show_faces:
            self.draw_faces()
        if self.show_edges:
            self.draw_edges()

    def draw_mesh(self) -> List[bpy.types.Object]:
        """Draw the mesh."""
        vertices, faces = self.mesh.to_vertices_and_faces()
        obj = compas_blender.draw_mesh(vertices, faces, name=self.mesh.name, collection=self.collection)
        return [obj]

    def draw_vertices(self,
                      vertices: Optional[List[int]] = None,
                      color: Optional[Union[str, Color, List[Color], Dict[int, Color]]] = None) -> List[bpy.types.Object]:
        """Draw a selection of vertices.

        Parameters
        ----------
        vertices : list
            A list of vertex keys identifying which vertices to draw.
            Default is ``None``, in which case all vertices are drawn.
        color : rgb-tuple or dict of rgb-tuple
            The color specification for the vertices.

        Returns
        -------
        list of :class:`bpy.types.Object`

        """
        vertices = vertices or list(self.mesh.vertices())
        vertex_color = colordict(color, vertices, default=self.color_vertices)
        points = []
        for vertex in vertices:
            points.append({
                'pos': self.mesh.vertex_coordinates(vertex),
                'name': f"{self.mesh.name}.vertex.{vertex}",
                'color': vertex_color[vertex],
                'radius': 0.01
            })
        objects = compas_blender.draw_points(points, self.vertexcollection)
        self.object_vertex = zip(objects, vertices)
        return objects

    def draw_faces(self,
                   faces: Optional[List[int]] = None,
                   color: Optional[Union[str, Color, List[Color], Dict[int, Color]]] = None) -> List[bpy.types.Object]:
        """Draw a selection of faces.

        Parameters
        ----------
        faces : list
            A list of face keys identifying which faces to draw.
            The default is ``None``, in which case all faces are drawn.
        color : rgb-tuple or dict of rgb-tuple
            The color specification for the faces.

        Returns
        -------
        list of :class:`bpy.types.Object`

        """
        faces = faces or list(self.mesh.faces())
        face_color = colordict(color, faces, default=self.color_faces)
        facets = []
        for face in faces:
            facets.append({
                'points': self.mesh.face_coordinates(face),
                'name': f"{self.mesh.name}.face.{face}",
                'color': face_color[face]
            })
        objects = compas_blender.draw_faces(facets, self.facecollection)
        self.object_face = zip(objects, faces)
        return objects

    def draw_edges(self,
                   edges: Optional[List[Tuple[int, int]]] = None,
                   color: Optional[Union[str, Color, List[Color], Dict[int, Color]]] = None) -> List[bpy.types.Object]:
        """Draw a selection of edges.

        Parameters
        ----------
        edges : list
            A list of edge keys (as uv pairs) identifying which edges to draw.
            The default is ``None``, in which case all edges are drawn.
        color : rgb-tuple or dict of rgb-tuple
            The color specification for the edges.

        Returns
        -------
        list of :class:`bpy.types.Object`

        """
        edges = edges or list(self.mesh.edges())
        edge_color = colordict(color, edges, default=self.color_edges)
        lines = []
        for edge in edges:
            lines.append({
                'start': self.mesh.vertex_coordinates(edge[0]),
                'end': self.mesh.vertex_coordinates(edge[1]),
                'color': edge_color[edge],
                'name': f"{self.mesh.name}.edge.{edge[0]}-{edge[1]}"
            })
        objects = compas_blender.draw_lines(lines, self.edgecollection)
        self.object_edge = zip(objects, edges)
        return objects

    # ==========================================================================
    # draw normals
    # ==========================================================================

    def draw_vertexnormals(self,
                           vertices: Optional[List[int]] = None,
                           color: Optional[Union[str, Color, List[Color], Dict[int, Color]]] = None,
                           scale: float = 1.0) -> List[bpy.types.Object]:
        """Draw the normals at the vertices of the mesh.

        Parameters
        ----------
        vertices : list, optional
            A selection of vertex normals to draw.
            Default is to draw all vertex normals.
        color : rgb-tuple or dict of rgb-tuple
            The color specification of the normal vectors.
            The default color is green, ``(0., 1., 0.)``.
        scale : float, optional
            Scale factor for the vertex normals.
            Default is ``1.0``.

        Returns
        -------
        list of :class:`bpy.types.Object`
        """
        vertices = vertices or list(self.mesh.vertices())
        vertex_color = colordict(color, vertices, default=(0., 1., 0.))
        lines = []
        for vertex in vertices:
            a = self.mesh.vertex_coordinates(vertex)
            n = self.mesh.vertex_normal(vertex)
            b = add_vectors(a, scale_vector(n, scale))
            lines.append({
                'start': a,
                'end': b,
                'color': vertex_color[vertex],
                'name': "{}.vertexnormal.{}".format(self.mesh.name, vertex)
            })
        objects = compas_blender.draw_lines(lines, collection=self.vertexnormalcollection)
        self.object_vertexnormal = zip(objects, vertices)
        return objects

    def draw_facenormals(self,
                         faces: Optional[List[List[int]]] = None,
                         color: Optional[Union[str, Color, List[Color], Dict[int, Color]]] = None,
                         scale: float = 1.0) -> List[bpy.types.Object]:
        """Draw the normals of the faces.

        Parameters
        ----------
        faces : list, optional
            A selection of face normals to draw.
            Default is to draw all face normals.
        color : rgb-tuple or dict of rgb-tuple
            The color specification of the normal vectors.
            The default color is cyan, ``(0., 1., 1.)``.
        scale : float, optional
            Scale factor for the face normals.
            Default is ``1.0``.

        Returns
        -------
        list of :class:`bpy.types.Object`
        """
        faces = faces or list(self.mesh.faces())
        face_color = colordict(color, faces, default=(0., 1., 1.))
        lines = []
        for face in faces:
            a = centroid_points(
                [self.mesh.vertex_coordinates(vertex) for vertex in self.mesh.face_vertices(face)]
            )
            n = self.mesh.face_normal(face)
            b = add_vectors(a, scale_vector(n, scale))
            lines.append({
                'start': a,
                'end': b,
                'name': "{}.facenormal.{}".format(self.mesh.name, face),
                'color': face_color[face]
            })
        objects = compas_blender.draw_lines(lines, collection=self.facenormalcollection)
        self.object_facenormal = zip(objects, faces)
        return objects

    # ==========================================================================
    # draw labels
    # ==========================================================================

    def draw_vertexlabels(self,
                          text: Optional[Dict[int, str]] = None,
                          color: Optional[Union[str, Color, List[Color], Dict[int, Color]]] = None) -> List[bpy.types.Object]:
        """Draw labels for a selection vertices.

        Parameters
        ----------
        text : dict, optional
            A dictionary of vertex labels as vertex-text pairs.
            The default value is ``None``, in which case every vertex will be labeled with its key.
        color : rgb-tuple or dict of rgb-tuple
            The color specification of the labels.
            The default color is the same as the default vertex color.

        Returns
        -------
        list of :class:`bpy.types.Object`
        """
        if not text or text == 'key':
            vertex_text = {vertex: str(vertex) for vertex in self.mesh.vertices()}
        elif text == 'index':
            vertex_text = {vertex: str(index) for index, vertex in enumerate(self.mesh.vertices())}
        elif isinstance(text, dict):
            vertex_text = text
        else:
            raise NotImplementedError
        vertex_color = colordict(color, vertex_text, default=self.color_vertices)
        labels = []
        for vertex in vertex_text:
            labels.append({
                'pos': self.mesh.vertex_coordinates(vertex),
                'name': "{}.vertexlabel.{}".format(self.mesh.name, vertex),
                'text': vertex_text[vertex],
                'color': vertex_color[vertex]})
        objects = compas_blender.draw_texts(labels, collection=self.vertexlabelcollection)
        self.object_vertexlabel = zip(objects, vertex_text)
        return objects

    def draw_edgelabels(self,
                        text: Optional[Dict[Tuple[int, int], str]] = None,
                        color: Optional[Union[str, Color, List[Color], Dict[int, Color]]] = None) -> List[bpy.types.Object]:
        """Draw labels for a selection of edges.

        Parameters
        ----------
        text : dict, optional
            A dictionary of edge labels as edge-text pairs.
            The default value is ``None``, in which case every edge will be labeled with its key.
        color : rgb-tuple or dict of rgb-tuple
            The color specification of the labels.
            The default color is the same as the default color for edges.

        Returns
        -------
        list of :class:`bpy.types.Object`
        """
        if text is None:
            edge_text = {(u, v): "{}-{}".format(u, v) for u, v in self.mesh.edges()}
        elif isinstance(text, dict):
            edge_text = text
        else:
            raise NotImplementedError
        edge_color = colordict(color, edge_text, default=self.color_edges)
        labels = []
        for edge in edge_text:
            labels.append({
                'pos': centroid_points(
                    [self.mesh.vertex_coordinates(edge[0]), self.mesh.vertex_coordinates(edge[1])]
                ),
                'name': "{}.edgelabel.{}-{}".format(self.mesh.name, *edge),
                'text': edge_text[edge]})
        objects = compas_blender.draw_texts(labels, collection=self.edgelabelcollection, color=edge_color)
        self.object_edgelabel = zip(objects, edge_text)
        return objects

    def draw_facelabels(self,
                        text: Optional[Dict[int, str]] = None,
                        color: Optional[Union[str, Color, List[Color], Dict[int, Color]]] = None) -> List[bpy.types.Object]:
        """Draw labels for a selection of faces.

        Parameters
        ----------
        text : dict, optional
            A dictionary of face labels as face-text pairs.
            The default value is ``None``, in which case every face will be labeled with its key.
        color : rgb-tuple or dict of rgb-tuple
            The color specification of the labels.
            The default color is the same as the default face color.

        Returns
        -------
        list of :class:`bpy.types.Object`
        """
        if not text or text == 'key':
            face_text = {face: str(face) for face in self.mesh.faces()}
        elif text == 'index':
            face_text = {face: str(index) for index, face in enumerate(self.mesh.faces())}
        elif isinstance(text, dict):
            face_text = text
        else:
            raise NotImplementedError
        face_color = color or self.color_faces
        labels = []
        for face in face_text:
            labels.append({
                'pos': centroid_points(
                    [self.mesh.vertex_coordinates(vertex) for vertex in self.mesh.face_vertices(face)]
                ),
                'name': "{}.facelabel.{}".format(self.mesh.name, face),
                'text': face_text[face]})
        objects = compas_blender.draw_texts(labels, collection=self.collection, color=face_color)
        self.object_facelabel = zip(objects, face_text)
        return objects
