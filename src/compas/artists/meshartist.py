from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from abc import abstractmethod

from compas.geometry import transform_points
from .artist import Artist
from .descriptors.color import ColorAttribute
from .descriptors.colordict import ColorDictAttribute


class MeshArtist(Artist):
    """Base class for all mesh artists.

    Parameters
    ----------
    mesh : :class:`~compas.datastructures.Mesh`
        A COMPAS mesh.

    Attributes
    ----------
    mesh : :class:`~compas.datastructures.Mesh`
        The mesh data structure.
    default_vertexsize : float
        The default size of the vertices of the mesh.
    default_edgewidth : float
        The default width of the edges of the mesh.
    vertex_xyz : dict[int, list[float]]
        View coordinates of the vertices.
        Defaults to the real coordinates.
    color : :class:`~compas.colors.Color`
        The base RGB color of the mesh.
    vertex_color : :class:`~compas.colors.ColorDict`]
        Vertex colors.
    edge_color : :class:`~compas.colors.ColorDict`
        Edge colors.
    face_color : :class:`~compas.colors.ColorDict`
        Face colors.
    vertex_text : dict[int, str]
        Vertex labels.
        Defaults to the vertex identifiers.
    edge_text : dict[tuple[int, int], str]
        Edge labels.
        Defaults to the edge identifiers.
    face_text : dict[int, str]
        Face labels.
        Defaults to the face identifiers.
    vertex_size : dict[int, float]
        Vertex sizes.
        Defaults to 1.
        Visualization of vertices with variable size is not available for all visualization contexts.
    edge_width : dict[tuple[int, int], float]
        Edge widths.
        Defaults to 1.
        Visualization of edges with variable width is not available for all visualization contexts.

    See Also
    --------
    :class:`compas.artists.NetworkArtist`
    :class:`compas.artists.VolMeshArtist`

    """

    color = ColorAttribute(default=None)

    vertex_color = ColorDictAttribute(default=None)
    edge_color = ColorDictAttribute(default=None)
    face_color = ColorDictAttribute(default=None)

    def __init__(self, mesh, **kwargs):
        super(MeshArtist, self).__init__(item=mesh, **kwargs)
        self._mesh = None
        self._vertex_xyz = None
        self.mesh = mesh

    @property
    def mesh(self):
        return self._mesh

    @mesh.setter
    def mesh(self, mesh):
        self._mesh = mesh
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
            points = self.mesh.vertices_attributes("xyz")  # type: ignore
            if self.transformation:
                points = transform_points(points, self.transformation)
            self._vertex_xyz = dict(zip(self.mesh.vertices(), points))  # type: ignore
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
        color : tuple[float, float, float] | :class:`~compas.colors.Color` | dict[int, tuple[float, float, float] | :class:`~compas.colors.Color`], optional
            The color of the vertices,
            as either a single color to be applied to all vertices,
            or a color dict, mapping specific vertices to specific colors.
        text : dict[int, str], optional
            The text labels for the vertices
            as a text dict, mapping specific vertices to specific text labels.

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
            The text labels for the edges
            as a text dict, mapping specific edges to specific text labels.

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
            The text labels for the faces
            as a text dict, mapping specific faces to specific text labels.

        Returns
        -------
        list
            The identifiers of the objects representing the faces in the visualization context.

        """
        raise NotImplementedError

    def draw_mesh(self, *args, **kwargs):
        """Draw the mesh of the mesh.

        .. deprecated:: 1.14.1
            Use :meth:`~MeshArtist.draw` instead.

        Returns
        -------
        list
            The identifiers of the objects representing the mesh in the visualization context.

        """
        return self.draw(*args, **kwargs)

    def clear(self):
        """Clear all components of the mesh.

        Returns
        -------
        None

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
