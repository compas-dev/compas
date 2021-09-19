from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from abc import abstractmethod

from compas.utilities import is_color_rgb
from .artist import Artist


class MeshArtist(Artist):
    """Base class for all mesh artists.

    Class Attributes
    ----------------
    default_color : tuple
        The default color of the mesh.
    default_vertexcolor : tuple
        The default color for vertices that do not have a specified color.
    default_edgecolor : tuple
        The default color for edges that do not have a specified color.
    default_facecolor : tuple
        The default color for faces that do not have a specified color.

    Attributes
    ----------
    mesh : :class:`compas.datastructures.Mesh`
        The mesh associated with the artist.
    vertices : list
        The vertices to include in the drawing.
        Default is all vertices.
    edges : list
        The edges to include in the drawing.
        Default is all edges.
    faces : list
        The faces to include in the drawing.
        Default is all faces.
    vertex_xyz : dict
        The view coordinates of the vertices.
        Default is to use the actual vertex coordinates.
    vertex_color : dict
        Mapping between vertices and colors.
        Default is to use the default color for vertices.
    edge_color : dict
        Mapping between edges and colors.
        Default is to use the default color for edges.
    face_color : dict
        Mapping between faces and colors.
        Default is to use the default color for faces.
    vertex_text : dict
        Mapping between vertices and text labels.
    edge_text : dict
        Mapping between edges and text labels.
    face_text : dict
        Mapping between faces and text labels.
    """

    default_color = (0, 0, 0)
    default_vertexcolor = (255, 255, 255)
    default_edgecolor = (0, 0, 0)
    default_facecolor = (0, 0, 0)

    def __init__(self, mesh):
        self._mesh = None
        self._vertices = None
        self._edges = None
        self._faces = None
        self._color = None
        self._vertex_xyz = None
        self._vertex_color = None
        self._edge_color = None
        self._face_color = None
        self._vertex_text = None
        self._edge_text = None
        self._face_text = None
        self.mesh = mesh
        self.join_faces = False

    @property
    def mesh(self):
        return self.item

    @mesh.setter
    def mesh(self, mesh):
        self.item = mesh
        self._vertex_xyz = None

    @property
    def vertices(self):
        if self._vertices is None:
            self._vertices = list(self.mesh.vertices())
        return self._vertices

    @vertices.setter
    def vertices(self, vertices):
        self._vertices = vertices

    @property
    def edges(self):
        if self._edges is None:
            self._edges = list(self.mesh.edges())
        return self._edges

    @edges.setter
    def edges(self, edges):
        self._edges = edges

    @property
    def faces(self):
        if self._faces is None:
            self._faces = list(self.mesh.faces())
        return self._faces

    @faces.setter
    def faces(self, faces):
        self._faces = faces

    @property
    def color(self):
        if not self._color:
            self._color = self.default_color
        return self._color

    @color.setter
    def color(self, color):
        if is_color_rgb(color):
            self._color = color

    @property
    def vertex_xyz(self):
        if not self._vertex_xyz:
            return {vertex: self.mesh.vertex_attributes(vertex, 'xyz') for vertex in self.mesh.vertices()}
        return self._vertex_xyz

    @vertex_xyz.setter
    def vertex_xyz(self, vertex_xyz):
        self._vertex_xyz = vertex_xyz

    @property
    def vertex_color(self):
        if not self._vertex_color:
            self._vertex_color = {vertex: self.default_vertexcolor for vertex in self.mesh.vertices()}
        return self._vertex_color

    @vertex_color.setter
    def vertex_color(self, vertex_color):
        if isinstance(vertex_color, dict):
            self._vertex_color = vertex_color
        elif is_color_rgb(vertex_color):
            self._vertex_color = {vertex: vertex_color for vertex in self.mesh.vertices()}

    @property
    def edge_color(self):
        if not self._edge_color:
            self._edge_color = {edge: self.default_edgecolor for edge in self.mesh.edges()}
        return self._edge_color

    @edge_color.setter
    def edge_color(self, edge_color):
        if isinstance(edge_color, dict):
            self._edge_color = edge_color
        elif is_color_rgb(edge_color):
            self._edge_color = {edge: edge_color for edge in self.mesh.edges()}

    @property
    def face_color(self):
        if not self._face_color:
            self._face_color = {face: self.default_facecolor for face in self.mesh.faces()}
        return self._face_color

    @face_color.setter
    def face_color(self, face_color):
        if isinstance(face_color, dict):
            self._face_color = face_color
        elif is_color_rgb(face_color):
            self._face_color = {face: face_color for face in self.mesh.faces()}

    @property
    def vertex_text(self):
        if not self._vertex_text:
            self._vertex_text = {vertex: str(vertex) for vertex in self.mesh.vertices()}
        return self._vertex_text

    @vertex_text.setter
    def vertex_text(self, text):
        if text == 'key':
            self._vertex_text = {vertex: str(vertex) for vertex in self.mesh.vertices()}
        elif text == 'index':
            self._vertex_text = {vertex: str(index) for index, vertex in enumerate(self.mesh.vertices())}
        elif isinstance(text, dict):
            self._vertex_text = text

    @property
    def edge_text(self):
        if not self._edge_text:
            self._edge_text = {edge: "{}-{}".format(*edge) for edge in self.mesh.edges()}
        return self._edge_text

    @edge_text.setter
    def edge_text(self, text):
        if text == 'key':
            self._edge_text = {edge: "{}-{}".format(*edge) for edge in self.mesh.edges()}
        elif text == 'index':
            self._edge_text = {edge: str(index) for index, edge in enumerate(self.mesh.edges())}
        elif isinstance(text, dict):
            self._edge_text = text

    @property
    def face_text(self):
        if not self._face_text:
            self._face_text = {face: str(face) for face in self.mesh.faces()}
        return self._face_text

    @face_text.setter
    def face_text(self, text):
        if text == 'key':
            self._face_text = {face: str(face) for face in self.mesh.faces()}
        elif text == 'index':
            self._face_text = {face: str(index) for index, face in enumerate(self.mesh.faces())}
        elif isinstance(text, dict):
            self._face_text = text

    @abstractmethod
    def draw_vertices(self, vertices=None, color=None, text=None):
        raise NotImplementedError

    @abstractmethod
    def draw_edges(self, edges=None, color=None, text=None):
        raise NotImplementedError

    @abstractmethod
    def draw_faces(self, faces=None, color=None, text=None):
        raise NotImplementedError
