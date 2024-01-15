from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from abc import abstractmethod

from compas.geometry import transform_points
from .sceneobject import SceneObject
from .descriptors.colordict import ColorDictAttribute


class MeshObject(SceneObject):
    """Base class for all mesh scene objects.

    Parameters
    ----------
    mesh : :class:`compas.datastructures.Mesh`
        A COMPAS mesh.

    Attributes
    ----------
    mesh : :class:`compas.datastructures.Mesh`
        The mesh data structure.
    vertex_xyz : dict[int, list[float]]
        View coordinates of the vertices.
        Defaults to the real coordinates.
    color : :class:`compas.colors.Color`
        The base RGB color of the mesh.
    vertexcolor : :class:`compas.colors.ColorDict`
        Vertex colors.
    edgecolor : :class:`compas.colors.ColorDict`
        Edge colors.
    facecolor : :class:`compas.colors.ColorDict`
        Face colors.
    vertexsize : float
        The size of the vertices. Default is ``1.0``.
    edgewidth : float
        The width of the edges. Default is ``1.0``.
    show_vertices : bool
        Flag for showing or hiding the vertices. Default is ``False``.
    show_edges : bool
        Flag for showing or hiding the edges. Default is ``True``.
    show_faces : bool
        Flag for showing or hiding the faces. Default is ``True``.

    See Also
    --------
    :class:`compas.scene.GraphObject`
    :class:`compas.scene.VolMeshObject`

    """

    vertexcolor = ColorDictAttribute()
    edgecolor = ColorDictAttribute()
    facecolor = ColorDictAttribute()

    def __init__(self, mesh, **kwargs):
        super(MeshObject, self).__init__(item=mesh, **kwargs)
        self._mesh = None
        self._vertex_xyz = None
        self.mesh = mesh
        self.vertexcolor = kwargs.get("vertexcolor", self.color)
        self.edgecolor = kwargs.get("edgecolor", self.color)
        self.facecolor = kwargs.get("facecolor", self.color)
        self.vertexsize = kwargs.get("vertexsize", 1.0)
        self.edgewidth = kwargs.get("edgewidth", 1.0)
        self.show_vertices = kwargs.get("show_vertices", False)
        self.show_edges = kwargs.get("show_edges", True)
        self.show_faces = kwargs.get("show_faces", True)

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
            points = transform_points(points, self.worldtransformation)
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
        color : tuple[float, float, float] | :class:`compas.colors.Color` | dict[int, tuple[float, float, float] | :class:`compas.colors.Color`], optional
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
        color : tuple[float, float, float] | :class:`compas.colors.Color` | dict[tuple[int, int], tuple[float, float, float] | :class:`compas.colors.Color`], optional
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
        color : tuple[float, float, float] | :class:`compas.colors.Color` | dict[int, tuple[float, float, float] | :class:`compas.colors.Color`], optional
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
            Use :meth:`~MeshObject.draw` instead.

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
