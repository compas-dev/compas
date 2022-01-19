from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from abc import abstractmethod

from compas.utilities import is_color_rgb
from .artist import Artist


class VolMeshArtist(Artist):
    """Artist for drawing volmesh data structures.

    Parameters
    ----------
    volmesh : :class:`compas.datastructures.VolMesh`
        A COMPAS volmesh.

    Attributes
    ----------
    volmesh : :class:`compas.datastructures.VolMesh`
        The COMPAS volmesh associated with the artist.
    vertices : list[int]
        The list of vertices to draw.
        Default is a list of all vertices of the volmesh.
    edges : list[tuple[int, int]]
        The list of edges to draw.
        Default is a list of all edges of the volmesh.
    faces : list[int]
        The list of faces to draw.
        Default is a list of all faces of the volmesh.
    cells : list[int]
        The list of cells to draw.
        Default is a list of all cells of the volmesh.
    vertex_xyz : dict[int, list[float]]
        The view coordinates of the vertices.
        By default, the actual vertex coordinates are used.
    vertex_color : dict[int, tuple[float, float, float]]
        Mapping between vertices and colors.
        Missing vertices get the default vertex color: :attr:`default_vertexcolor`.
    edge_color : dict[tuple[int, int], tuple[float, float, float]]
        Mapping between edges and colors.
        Missing edges get the default edge color: :attr:`default_edgecolor`.
    face_color : dict[int, tuple[float, float, float]]
        Mapping between faces and colors.
        Missing faces get the default face color: :attr:`default_facecolor`.
    cell_color : dict[int, tuple[float, float, float]]
        Mapping between cells and colors.
        Missing cells get the default cell color: :attr:`default_facecolor`.
    vertex_text : dict[int, str]
        Mapping between vertices and text labels.
    edge_text : dict[tuple[int, int], str]
        Mapping between edges and text labels.
    face_text : dict[int, str]
        Mapping between faces and text lables.
    cell_text : dict[int, str]
        Mapping between cells and text lables.

    Class Attributes
    ----------------
    default_vertexcolor : tuple[float, float, float]
        The default color of the vertices of the mesh that don't have a specified color.
    default_edgecolor : tuple[float, float, float]
        The default color of the edges of the mesh that don't have a specified color.
    default_facecolor : tuple[float, float, float]
        The default color of the faces of the mesh that don't have a specified color.
    default_cellcolor : tuple[float, float, float]
        The default color of the cells of the mesh that don't have a specified color.

    """

    default_vertexcolor = (1, 1, 1)
    default_edgecolor = (0, 0, 0)
    default_facecolor = (0.8, 0.8, 0.8)
    default_cellcolor = (1, 0, 0)

    def __init__(self, volmesh, **kwargs):
        super(VolMeshArtist, self).__init__()
        self._volmesh = None
        self._vertices = None
        self._edges = None
        self._faces = None
        self._cells = None
        self._vertex_xyz = None
        self._vertex_color = None
        self._edge_color = None
        self._face_color = None
        self._cell_color = None
        self._vertex_text = None
        self._edge_text = None
        self._face_text = None
        self._cell_text = None
        self.volmesh = volmesh

    @property
    def volmesh(self):
        return self._volmesh

    @volmesh.setter
    def volmesh(self, volmesh):
        self._volmesh = volmesh
        self._vertex_xyz = None

    @property
    def vertices(self):
        if self._vertices is None:
            self._vertices = list(self.volmesh.vertices())
        return self._vertices

    @vertices.setter
    def vertices(self, vertices):
        self._vertices = vertices

    @property
    def edges(self):
        if self._edges is None:
            self._edges = list(self.volmesh.edges())
        return self._edges

    @edges.setter
    def edges(self, edges):
        self._edges = edges

    @property
    def faces(self):
        if self._faces is None:
            self._faces = list(self.volmesh.faces())
        return self._faces

    @faces.setter
    def faces(self, faces):
        self._faces = faces

    @property
    def cells(self):
        if self._cells is None:
            self._cells = list(self.volmesh.cells())
        return self._cells

    @cells.setter
    def cells(self, cells):
        self._cells = cells

    @property
    def vertex_xyz(self):
        if not self._vertex_xyz:
            self._vertex_xyz = {vertex: self.volmesh.vertex_attributes(vertex, 'xyz') for vertex in self.volmesh.vertices()}
        return self._vertex_xyz

    @vertex_xyz.setter
    def vertex_xyz(self, vertex_xyz):
        self._vertex_xyz = vertex_xyz

    @property
    def vertex_color(self):
        if not self._vertex_color:
            self._vertex_color = {vertex: self.artist.default_vertexcolor for vertex in self.volmesh.vertices()}
        return self._vertex_color

    @vertex_color.setter
    def vertex_color(self, vertex_color):
        if isinstance(vertex_color, dict):
            self._vertex_color = vertex_color
        elif is_color_rgb(vertex_color):
            self._vertex_color = {vertex: vertex_color for vertex in self.volmesh.vertices()}

    @property
    def edge_color(self):
        if not self._edge_color:
            self._edge_color = {edge: self.artist.default_edgecolor for edge in self.volmesh.edges()}
        return self._edge_color

    @edge_color.setter
    def edge_color(self, edge_color):
        if isinstance(edge_color, dict):
            self._edge_color = edge_color
        elif is_color_rgb(edge_color):
            self._edge_color = {edge: edge_color for edge in self.volmesh.edges()}

    @property
    def face_color(self):
        if not self._face_color:
            self._face_color = {face: self.artist.default_facecolor for face in self.volmesh.faces()}
        return self._face_color

    @face_color.setter
    def face_color(self, face_color):
        if isinstance(face_color, dict):
            self._face_color = face_color
        elif is_color_rgb(face_color):
            self._face_color = {face: face_color for face in self.volmesh.faces()}

    @property
    def cell_color(self):
        if not self._cell_color:
            self._cell_color = {cell: self.artist.default_cellcolor for cell in self.volmesh.cells()}
        return self._cell_color

    @cell_color.setter
    def cell_color(self, cell_color):
        if isinstance(cell_color, dict):
            self._cell_color = cell_color
        elif is_color_rgb(cell_color):
            self._cell_color = {cell: cell_color for cell in self.volmesh.cells()}

    @property
    def vertex_text(self):
        if not self._vertex_text:
            self._vertex_text = {vertex: str(vertex) for vertex in self.volmesh.vertices()}
        return self._vertex_text

    @vertex_text.setter
    def vertex_text(self, text):
        if text == 'key':
            self._vertex_text = {vertex: str(vertex) for vertex in self.volmesh.vertices()}
        elif text == 'index':
            self._vertex_text = {vertex: str(index) for index, vertex in enumerate(self.volmesh.vertices())}
        elif isinstance(text, dict):
            self._vertex_text = text

    @property
    def edge_text(self):
        if not self._edge_text:
            self._edge_text = {edge: "{}-{}".format(*edge) for edge in self.volmesh.edges()}
        return self._edge_text

    @edge_text.setter
    def edge_text(self, text):
        if text == 'key':
            self._edge_text = {edge: "{}-{}".format(*edge) for edge in self.volmesh.edges()}
        elif text == 'index':
            self._edge_text = {edge: str(index) for index, edge in enumerate(self.volmesh.edges())}
        elif isinstance(text, dict):
            self._edge_text = text

    @property
    def face_text(self):
        if not self._face_text:
            self._face_text = {face: str(face) for face in self.volmesh.faces()}
        return self._face_text

    @face_text.setter
    def face_text(self, text):
        if text == 'key':
            self._face_text = {face: str(face) for face in self.volmesh.faces()}
        elif text == 'index':
            self._face_text = {face: str(index) for index, face in enumerate(self.volmesh.faces())}
        elif isinstance(text, dict):
            self._face_text = text

    @property
    def cell_text(self):
        if not self._cell_text:
            self._cell_text = {cell: str(cell) for cell in self.volmesh.cells()}
        return self._cell_text

    @cell_text.setter
    def cell_text(self, text):
        if text == 'key':
            self._cell_text = {cell: str(cell) for cell in self.volmesh.cells()}
        elif text == 'index':
            self._cell_text = {cell: str(index) for index, cell in enumerate(self.volmesh.cells())}
        elif isinstance(text, dict):
            self._cell_text = text

    @abstractmethod
    def draw_vertices(self, vertices=None, color=None, text=None):
        """Draw the vertices of the mesh.

        Parameters
        ----------
        vertices : list[int], optional
            The vertices to include in the drawing.
            Default is all vertices.
        color : tuple[float, float, float] | dict[int, tuple[float, float, float]], optional
            The color of the vertices,
            as either a single color to be applied to all vertices,
            or a color dict, mapping specific vertices to specific colors.
        text : dict[int, str], optional
            The text labels for the vertices as a text dict,
            mapping specific vertices to specific text labels.

        Returns
        -------
        list
            The identifiers of the objects representing the vertices in the visualization context.

        """
        raise NotImplementedError

    @abstractmethod
    def draw_edges(self, edges=None, color=None, text=None):
        """Draw the edges of the mesh.

        Parameters
        ----------
        edges : list[tuple[int, int]], optional
            The edges to include in the drawing.
            Default is all edges.
        color : tuple[float, float, float] | dict[tuple[int, int], tuple[float, float, float]], optional
            The color of the edges,
            as either a single color to be applied to all edges,
            or a color dict, mapping specific edges to specific colors.
        text : dict[tuple[int, int], str], optional
            The text labels for the edges as a text dict,
            mapping specific edges to specific text labels.

        Returns
        -------
        list
            The identifiers of the objects representing the edges in the visualization context.

        """
        raise NotImplementedError

    @abstractmethod
    def draw_faces(self, faces=None, color=None, text=None):
        """Draw the faces of the mesh.

        Parameters
        ----------
        faces : list[int], optional
            The faces to include in the drawing.
            Default is all faces.
        color : tuple[float, float, float] or dict[int, tuple[float, float, float]], optional
            The color of the faces,
            as either a single color to be applied to all faces,
            or a color dict, mapping specific faces to specific colors.
        text : dict[int, str], optional
            The text labels for the faces as a text dict,
            mapping specific faces to specific text labels.

        Returns
        -------
        list
            The identifiers of the objects representing the faces in the visualization context.

        """
        raise NotImplementedError

    @abstractmethod
    def draw_cells(self, cells=None, color=None, text=None):
        """Draw the cells of the mesh.

        Parameters
        ----------
        cells : list[int], optional
            The cells to include in the drawing.
            Default is all cells.
        color : tuple[float, float, float] | dict[int, tuple[float, float, float]], optional
            The color of the cells,
            as either a single color to be applied to all cells,
            or a color dict, mapping specific cells to specific colors.
        text : dict[int, str], optional
            The text labels for the cells as a text dict,
            mapping specific cells to specific text labels.

        Returns
        -------
        list
            The identifiers of the objects representing the cells in the visualization context.

        """
        raise NotImplementedError

    @abstractmethod
    def clear_vertices(self):
        """Clear the vertices of the mesh.

        Returns
        -------
        None

        """
        raise NotImplementedError

    @abstractmethod
    def clear_edges(self):
        """Clear the edges of the mesh.

        Returns
        -------
        None

        """
        raise NotImplementedError

    @abstractmethod
    def clear_faces(self):
        """Clear the faces of the mesh.

        Returns
        -------
        None

        """
        raise NotImplementedError

    @abstractmethod
    def clear_cells(self):
        """Clear the cells of the mesh.

        Returns
        -------
        None

        """
        raise NotImplementedError
