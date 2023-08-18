from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from abc import abstractmethod

from compas.colors import Color
from .artist import Artist
from .descriptors.color import ColorAttribute
from .descriptors.colordict import ColorDictAttribute


class VolMeshArtist(Artist):
    """Artist for drawing volmesh data structures.

    Parameters
    ----------
    volmesh : :class:`~compas.datastructures.VolMesh`
        A COMPAS volmesh.

    Attributes
    ----------
    volmesh : :class:`~compas.datastructures.VolMesh`
        The COMPAS volmesh associated with the artist.
    vertex_xyz : dict[int, list[float]]
        The view coordinates of the vertices.
        By default, the actual vertex coordinates are used.
    vertex_color : dict[int, :class:`~compas.colors.Color`]
        Mapping between vertices and colors.
        Missing vertices get the default vertex color: :attr:`default_vertexcolor`.
    edge_color : dict[tuple[int, int], :class:`~compas.colors.Color`]
        Mapping between edges and colors.
        Missing edges get the default edge color: :attr:`default_edgecolor`.
    face_color : dict[int, :class:`~compas.colors.Color`]
        Mapping between faces and colors.
        Missing faces get the default face color: :attr:`default_facecolor`.
    cell_color : dict[int, :class:`~compas.colors.Color`]
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

    See Also
    --------
    :class:`compas.artists.NetworkArtist`
    :class:`compas.artists.MeshArtist`

    """

    color = ColorAttribute(default=Color.grey().lightened(50))

    vertex_color = ColorDictAttribute(default=Color.white())
    edge_color = ColorDictAttribute(default=Color.black())
    face_color = ColorDictAttribute(default=Color.grey().lightened(50))
    cell_color = ColorDictAttribute(default=Color.grey())

    def __init__(self, volmesh, **kwargs):
        super(VolMeshArtist, self).__init__(**kwargs)
        self._volmesh = None
        self._vertex_xyz = None
        self._vertex_text = None
        self._edge_text = None
        self._face_text = None
        self._cell_text = None
        self._vertexcollection = None
        self._edgecollection = None
        self._facecollection = None
        self._cellcollection = None
        self._vertexnormalcollection = None
        self._facenormalcollection = None
        self._vertexlabelcollection = None
        self._edgelabelcollection = None
        self._facelabelcollection = None
        self._celllabelcollection = None
        self.volmesh = volmesh

    @property
    def volmesh(self):
        return self._volmesh

    @volmesh.setter
    def volmesh(self, volmesh):
        self._volmesh = volmesh
        self._vertex_xyz = None

    @property
    def vertex_xyz(self):
        if not self._vertex_xyz:
            self._vertex_xyz = {vertex: self.volmesh.vertex_coordinates(vertex) for vertex in self.volmesh.vertices()}  # type: ignore
        return self._vertex_xyz

    @vertex_xyz.setter
    def vertex_xyz(self, vertex_xyz):
        self._vertex_xyz = vertex_xyz

    @property
    def vertex_text(self):
        if not self._vertex_text:
            self._vertex_text = {vertex: str(vertex) for vertex in self.volmesh.vertices()}  # type: ignore
        return self._vertex_text

    @vertex_text.setter
    def vertex_text(self, text):
        if text == "key":
            self._vertex_text = {vertex: str(vertex) for vertex in self.volmesh.vertices()}  # type: ignore
        elif text == "index":
            self._vertex_text = {vertex: str(index) for index, vertex in enumerate(self.volmesh.vertices())}  # type: ignore
        elif isinstance(text, dict):
            self._vertex_text = text

    @property
    def edge_text(self):
        if not self._edge_text:
            self._edge_text = {edge: "{}-{}".format(*edge) for edge in self.volmesh.edges()}  # type: ignore
        return self._edge_text

    @edge_text.setter
    def edge_text(self, text):
        if text == "key":
            self._edge_text = {edge: "{}-{}".format(*edge) for edge in self.volmesh.edges()}  # type: ignore
        elif text == "index":
            self._edge_text = {edge: str(index) for index, edge in enumerate(self.volmesh.edges())}  # type: ignore
        elif isinstance(text, dict):
            self._edge_text = text

    @property
    def face_text(self):
        if not self._face_text:
            self._face_text = {face: str(face) for face in self.volmesh.faces()}  # type: ignore
        return self._face_text

    @face_text.setter
    def face_text(self, text):
        if text == "key":
            self._face_text = {face: str(face) for face in self.volmesh.faces()}  # type: ignore
        elif text == "index":
            self._face_text = {face: str(index) for index, face in enumerate(self.volmesh.faces())}  # type: ignore
        elif isinstance(text, dict):
            self._face_text = text

    @property
    def cell_text(self):
        if not self._cell_text:
            self._cell_text = {cell: str(cell) for cell in self.volmesh.cells()}  # type: ignore
        return self._cell_text

    @cell_text.setter
    def cell_text(self, text):
        if text == "key":
            self._cell_text = {cell: str(cell) for cell in self.volmesh.cells()}  # type: ignore
        elif text == "index":
            self._cell_text = {cell: str(index) for index, cell in enumerate(self.volmesh.cells())}  # type: ignore
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
        color : tuple[float, float, float] | :class:`~compas.colors.Color` | dict[int, tuple[float, float, float] | :class:`~compas.colors.Color`], optional
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
        color : tuple[float, float, float] | :class:`~compas.colors.Color` | dict[tuple[int, int], tuple[float, float, float] | :class:`~compas.colors.Color`], optional
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
        color : tuple[float, float, float] | :class:`~compas.colors.Color` | dict[int, tuple[float, float, float] | :class:`~compas.colors.Color`], optional
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
        color : tuple[float, float, float] | :class:`~compas.colors.Color` | dict[int, tuple[float, float, float] | :class:`~compas.colors.Color`], optional
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
