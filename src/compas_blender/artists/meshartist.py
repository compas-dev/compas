from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union
from typing import Any

import bpy

from functools import partial

import compas_blender
from compas.datastructures import Mesh
from compas.geometry import add_vectors
from compas.geometry import centroid_points
from compas.geometry import scale_vector

from compas.utilities import color_to_colordict
from compas.artists import MeshArtist
from .artist import BlenderArtist

colordict = partial(color_to_colordict, colorformat='rgb', normalize=True)
Color = Union[Tuple[int, int, int], Tuple[float, float, float]]


class MeshArtist(BlenderArtist, MeshArtist):
    """A mesh artist defines functionality for visualising COMPAS meshes in Blender.

    Parameters
    ----------
    mesh : :class:`compas.datastructures.Mesh`
        A COMPAS mesh.
    collection: str or :class:`bpy.types.Collection`
        The name of the collection the object belongs to.
    vertices : list of int, optional
        A list of vertex identifiers.
        Default is ``None``, in which case all vertices are drawn.
    edges : list, optional
        A list of edge keys (as uv pairs) identifying which edges to draw.
        The default is ``None``, in which case all edges are drawn.
    faces : list, optional
        A list of face identifiers.
        The default is ``None``, in which case all faces are drawn.
    vertexcolor : rgb-tuple or dict of rgb-tuples, optional
        The color specification for the vertices.
    edgecolor : rgb-tuple or dict of rgb-tuples, optional
        The color specification for the edges.
    facecolor : rgb-tuple or dict of rgb-tuples, optional
        The color specification for the faces.
    show_mesh : bool, optional
    show_vertices : bool, optional
    show_edges : bool, optional
    show_faces : bool, optional

    Attributes
    ----------
    vertexcollection : :class:`bpy.types.Collection`
        The collection containing the vertices.
    edgecollection : :class:`bpy.types.Collection`
        The collection containing the edges.
    facecollection : :class:`bpy.types.Collection`
        The collection containing the faces.
    vertexlabelcollection : :class:`bpy.types.Collection`
        The collection containing the vertex labels.
    edgelabelcollection : :class:`bpy.types.Collection`
        The collection containing the edge labels.
    facelabelcollection : :class:`bpy.types.Collection`
        The collection containing the face labels.

    """

    def __init__(self,
                 mesh: Mesh,
                 collection: Optional[Union[str, bpy.types.Collection]] = None,
                 vertices: Optional[List[int]] = None,
                 edges: Optional[List[int]] = None,
                 faces: Optional[List[int]] = None,
                 vertexcolor: Optional[Color] = None,
                 edgecolor: Optional[Color] = None,
                 facecolor: Optional[Color] = None,
                 show_mesh: bool = False,
                 show_vertices: bool = True,
                 show_edges: bool = True,
                 show_faces: bool = True,
                 **kwargs: Any):

        super().__init__(mesh=mesh, collection=collection or mesh.name, **kwargs)

        self.vertices = vertices
        self.edges = edges
        self.faces = faces
        self.vertex_color = vertexcolor
        self.edge_color = edgecolor
        self.face_color = facecolor
        self.show_mesh = show_mesh
        self.show_vertices = show_vertices
        self.show_edges = show_edges
        self.show_faces = show_faces

    @property
    def vertexcollection(self) -> bpy.types.Collection:
        if not self._vertexcollection:
            self._vertexcollection = compas_blender.create_collection('Vertices', parent=self.collection)
        return self._vertexcollection

    @property
    def edgecollection(self) -> bpy.types.Collection:
        if not self._edgecollection:
            self._edgecollection = compas_blender.create_collection('Edges', parent=self.collection)
        return self._edgecollection

    @property
    def facecollection(self) -> bpy.types.Collection:
        if not self._facecollection:
            self._facecollection = compas_blender.create_collection('Faces', parent=self.collection)
        return self._facecollection

    @property
    def vertexnormalcollection(self) -> bpy.types.Collection:
        if not self._vertexnormalcollection:
            self._vertexnormalcollection = compas_blender.create_collection('VertexNormals', parent=self.collection)
        return self._vertexnormalcollection

    @property
    def facenormalcollection(self) -> bpy.types.Collection:
        if not self._facenormalcollection:
            self._facenormalcollection = compas_blender.create_collection('FaceNormals', parent=self.collection)
        return self._facenormalcollection

    @property
    def vertexlabelcollection(self) -> bpy.types.Collection:
        if not self._vertexlabelcollection:
            self._vertexlabelcollection = compas_blender.create_collection('VertexLabels', parent=self.collection)
        return self._vertexlabelcollection

    @property
    def edgelabelcollection(self) -> bpy.types.Collection:
        if not self._edgelabelcollection:
            self._edgelabelcollection = compas_blender.create_collection('EdgeLabels', parent=self.collection)
        return self._edgelabelcollection

    @property
    def facelabelcollection(self) -> bpy.types.Collection:
        if not self._facelabelcollection:
            self._facelabelcollection = compas_blender.create_collection('FaceLabels', parent=self.collection)
        return self._facelabelcollection

    # ==========================================================================
    # clear
    # ==========================================================================

    def clear_vertices(self):
        compas_blender.delete_objects(self.vertexcollection.objects)

    def clear_edges(self):
        compas_blender.delete_objects(self.edgecollection.objects)

    def clear_faces(self):
        compas_blender.delete_objects(self.facecollection.objects)

    # ==========================================================================
    # draw
    # ==========================================================================

    def draw(self,
             vertices: Optional[List[int]] = None,
             edges: Optional[List[Tuple[int, int]]] = None,
             faces: Optional[List[int]] = None,
             vertexcolor: Optional[Union[str, Color, List[Color], Dict[int, Color]]] = None,
             edgecolor: Optional[Union[str, Color, List[Color], Dict[int, Color]]] = None,
             facecolor: Optional[Union[str, Color, List[Color], Dict[int, Color]]] = None
             ) -> None:
        """Draw the mesh using the chosen visualisation settings.

        Parameters
        ----------
        settings : dict, optional
            Dictionary of visualisation settings that will be merged with the settings of the artist.

        """
        self.clear()
        if self.show_mesh:
            self.draw_mesh()
        if self.show_vertices:
            self.draw_vertices(vertices=vertices, color=vertexcolor)
        if self.show_edges:
            self.draw_edges(edges=edges, color=edgecolor)
        if self.show_faces:
            self.draw_faces(faces=faces, color=facecolor)

    def draw_mesh(self) -> List[bpy.types.Object]:
        """Draw the mesh."""
        vertices, faces = self.mesh.to_vertices_and_faces()
        obj = compas_blender.draw_mesh(vertices, faces, name=self.mesh.name, collection=self.collection)
        return [obj]

    def draw_vertices(self,
                      vertices: Optional[List[int]] = None,
                      color: Optional[Union[str, Color, List[Color], Dict[int, Color]]] = None
                      ) -> List[bpy.types.Object]:
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
        self.vertex_color = color
        vertices = vertices or self.vertices
        points = []
        for vertex in vertices:
            points.append({
                'pos': self.vertex_xyz[vertex],
                'name': f"{self.mesh.name}.vertex.{vertex}",
                'color': self.vertex_color.get(vertex, self.default_vertexcolor),
                'radius': 0.01
            })
        return compas_blender.draw_points(points, self.vertexcollection)

    def draw_edges(self,
                   edges: Optional[List[Tuple[int, int]]] = None,
                   color: Optional[Union[str, Color, List[Color], Dict[int, Color]]] = None
                   ) -> List[bpy.types.Object]:
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
        self.edge_color = color
        edges = edges or self.edges
        lines = []
        for edge in edges:
            lines.append({
                'start': self.vertex_xyz[edge[0]],
                'end': self.vertex_xyz[edge[1]],
                'color': self.edge_color.get(edge, self.default_edgecolor),
                'name': f"{self.mesh.name}.edge.{edge[0]}-{edge[1]}"
            })
        return compas_blender.draw_lines(lines, self.edgecollection)

    def draw_faces(self,
                   faces: Optional[List[int]] = None,
                   color: Optional[Union[str, Color, List[Color], Dict[int, Color]]] = None
                   ) -> List[bpy.types.Object]:
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
        self.face_color = color
        faces = faces or self.faces
        facets = []
        for face in faces:
            facets.append({
                'points': [self.vertex_xyz[vertex] for vertex in self.mesh.face_vertices(face)],
                'name': f"{self.mesh.name}.face.{face}",
                'color': self.face_color.get(face, self.default_facecolor)
            })
        return compas_blender.draw_faces(facets, self.facecollection)

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
        vertices = vertices or self.vertices
        vertex_color = colordict(color, vertices, default=(0., 1., 0.))
        lines = []
        for vertex in vertices:
            a = self.vertex_xyz[vertex]
            n = self.mesh.vertex_normal(vertex)
            b = add_vectors(a, scale_vector(n, scale))
            lines.append({
                'start': a,
                'end': b,
                'color': vertex_color[vertex],
                'name': "{}.vertexnormal.{}".format(self.mesh.name, vertex)
            })
        return compas_blender.draw_lines(lines, collection=self.vertexnormalcollection)

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
        faces = faces or self.faces
        face_color = colordict(color, faces, default=(0., 1., 1.))
        lines = []
        for face in faces:
            a = centroid_points([self.vertex_xyz[vertex] for vertex in self.mesh.face_vertices(face)])
            n = self.mesh.face_normal(face)
            b = add_vectors(a, scale_vector(n, scale))
            lines.append({
                'start': a,
                'end': b,
                'name': "{}.facenormal.{}".format(self.mesh.name, face),
                'color': face_color[face]
            })
        return compas_blender.draw_lines(lines, collection=self.facenormalcollection)

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
            vertex_text = {vertex: str(vertex) for vertex in self.vertices}
        elif text == 'index':
            vertex_text = {vertex: str(index) for index, vertex in enumerate(self.vertices)}
        elif isinstance(text, dict):
            vertex_text = text
        else:
            raise NotImplementedError
        vertex_color = colordict(color, vertex_text, default=self.default_vertexcolor)
        labels = []
        for vertex in vertex_text:
            labels.append({
                'pos': self.vertex_xyz[vertex],
                'name': "{}.vertexlabel.{}".format(self.mesh.name, vertex),
                'text': vertex_text[vertex],
                'color': vertex_color[vertex]
            })
        return compas_blender.draw_texts(labels, collection=self.vertexlabelcollection)

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
            edge_text = {(u, v): "{}-{}".format(u, v) for u, v in self.edges}
        elif isinstance(text, dict):
            edge_text = text
        else:
            raise NotImplementedError
        edge_color = colordict(color, edge_text, default=self.default_edgecolor)
        labels = []
        for edge in edge_text:
            labels.append({
                'pos': centroid_points([self.vertex_xyz[edge[0]], self.vertex_xyz[edge[1]]]),
                'name': "{}.edgelabel.{}-{}".format(self.mesh.name, *edge),
                'text': edge_text[edge]
            })
        return compas_blender.draw_texts(labels, collection=self.edgelabelcollection, color=edge_color)

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
            face_text = {face: str(face) for face in self.faces}
        elif text == 'index':
            face_text = {face: str(index) for index, face in enumerate(self.faces)}
        elif isinstance(text, dict):
            face_text = text
        else:
            raise NotImplementedError
        face_color = color or self.default_facecolor
        labels = []
        for face in face_text:
            labels.append({
                'pos': centroid_points([self.vertex_xyz[vertex] for vertex in self.mesh.face_vertices(face)]),
                'name': "{}.facelabel.{}".format(self.mesh.name, face),
                'text': face_text[face]
            })
        return compas_blender.draw_texts(labels, collection=self.collection, color=face_color)
