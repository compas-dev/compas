from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from abc import abstractmethod

from compas.colors import Color
from compas.geometry import transform_points
from .artist import Artist
from .descriptors.color import ColorAttribute
from .descriptors.colordict import ColorDictAttribute


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
    vertex_xyz : dict[int, list[float]]
        The view coordinates of the vertices.
        By default, the actual vertex coordinates are used.
    vertex_color : dict[int, :class:`compas.colors.Color`]
        Mapping between vertices and colors.
        Missing vertices get the default vertex color: :attr:`default_vertexcolor`.
    edge_color : dict[tuple[int, int], :class:`compas.colors.Color`]
        Mapping between edges and colors.
        Missing edges get the default edge color: :attr:`default_edgecolor`.
    face_color : dict[int, :class:`compas.colors.Color`]
        Mapping between faces and colors.
        Missing faces get the default face color: :attr:`default_facecolor`.
    cell_color : dict[int, :class:`compas.colors.Color`]
        Mapping between cells and colors.
        Missing cells get the default cell color: :attr:`default_facecolor`.

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
        super(VolMeshArtist, self).__init__(item=volmesh, **kwargs)
        self._volmesh = None
        self._vertex_xyz = None
        self.volmesh = volmesh

    @property
    def volmesh(self):
        return self._volmesh

    @volmesh.setter
    def volmesh(self, volmesh):
        self._volmesh = volmesh
        self._transformation = None
        self._vertex_xyz = None

    @property
    def transformation(self):
        return self._transformation

    @transformation.setter
    def transformation(self, transformation):
        self._vertex_xyz = None
        self._transformation = transformation

    @property
    def vertex_xyz(self):
        if self._vertex_xyz is None:
            points = self.volmesh.vertices_attributes("xyz")  # type: ignore
            if self.transformation:
                points = transform_points(points, self.transformation)
            self._vertex_xyz = dict(zip(self.volmesh.vertices(), points))  # type: ignore
        return self._vertex_xyz

    @vertex_xyz.setter
    def vertex_xyz(self, vertex_xyz):
        self._vertex_xyz = vertex_xyz

    @abstractmethod
    def draw_vertices(self, vertices=None, color=None, text=None):
        """Draw the vertices of the mesh.

        Parameters
        ----------
        vertices : list[int], optional
            The vertices to include in the drawing.
            Default is all vertices.
        color : tuple[float, float, float] | :class:`compas.colors.Color` | dict[int, tuple[float, float, float] | :class:`compas.colors.Color`], optional
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
        color : tuple[float, float, float] | :class:`compas.colors.Color` | dict[tuple[int, int], tuple[float, float, float] | :class:`compas.colors.Color`], optional
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
        color : tuple[float, float, float] | :class:`compas.colors.Color` | dict[int, tuple[float, float, float] | :class:`compas.colors.Color`], optional
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
        color : tuple[float, float, float] | :class:`compas.colors.Color` | dict[int, tuple[float, float, float] | :class:`compas.colors.Color`], optional
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

    def clear_vertices(self):
        """Clear the vertices of the mesh.

        Returns
        -------
        None

        """
        raise NotImplementedError

    def clear_edges(self):
        """Clear the edges of the mesh.

        Returns
        -------
        None

        """
        raise NotImplementedError

    def clear_faces(self):
        """Clear the faces of the mesh.

        Returns
        -------
        None

        """
        raise NotImplementedError

    def clear_cells(self):
        """Clear the cells of the mesh.

        Returns
        -------
        None

        """
        raise NotImplementedError
