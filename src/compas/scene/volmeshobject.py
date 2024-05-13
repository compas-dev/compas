from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.geometry import transform_points

from .descriptors.colordict import ColorDictAttribute
from .sceneobject import SceneObject


class VolMeshObject(SceneObject):
    """Scene object for drawing volmesh data structures.

    Parameters
    ----------
    volmesh : :class:`compas.datastructures.VolMesh`
        A COMPAS volmesh.

    Attributes
    ----------
    volmesh : :class:`compas.datastructures.VolMesh`
        The COMPAS volmesh associated with the scene object.
    vertex_xyz : dict[int, list[float]]
        The view coordinates of the vertices.
        By default, the actual vertex coordinates are used.
    vertexcolor : :class:`compas.colors.ColorDict`
        Mapping between vertices and colors.
        Missing vertices get the default vertex color: :attr:`default_vertexcolor`.
    edgecolor : :class:`compas.colors.ColorDict`
        Mapping between edges and colors.
        Missing edges get the default edge color: :attr:`default_edgecolor`.
    facecolor : :class:`compas.colors.ColorDict`
        Mapping between faces and colors.
        Missing faces get the default face color: :attr:`default_facecolor`.
    cellcolor : :class:`compas.colors.ColorDict`
        Mapping between cells and colors.
        Missing cells get the default cell color: :attr:`default_facecolor`.
    vertexsize : float
        The size of the vertices. Default is ``1.0``.
    edgewidth : float
        The width of the edges. Default is ``1.0``.
    show_vertices : Union[bool, sequence[float]]
        Flag for showing or hiding the vertices, or a list of keys for the vertices to show.
        Default is ``False``.
    show_edges : Union[bool, sequence[tuple[int, int]]]
        Flag for showing or hiding the edges, or a list of keys for the edges to show.
        Default is ``True``.
    show_faces : Union[bool, sequence[int]]
        Flag for showing or hiding the faces, or a list of keys for the faces to show.
        Default is ``False``.
    show_cells : bool
        Flag for showing or hiding the cells, or a list of keys for the cells to show.
        Default is ``True``.

    See Also
    --------
    :class:`compas.scene.GraphObject`
    :class:`compas.scene.MeshObject`

    """

    vertexcolor = ColorDictAttribute()
    edgecolor = ColorDictAttribute()
    facecolor = ColorDictAttribute()
    cellcolor = ColorDictAttribute()

    def __init__(self, volmesh, **kwargs):
        super(VolMeshObject, self).__init__(item=volmesh, **kwargs)
        self._volmesh = None
        self._vertex_xyz = None
        self.volmesh = volmesh
        self.vertexcolor = kwargs.get("vertexcolor", self.color)
        self.edgecolor = kwargs.get("edgecolor", self.color)
        self.facecolor = kwargs.get("facecolor", self.color)
        self.cellcolor = kwargs.get("cellcolor", self.color)
        self.vertexsize = kwargs.get("vertexsize", 1.0)
        self.edgewidth = kwargs.get("edgewidth", 1.0)
        self.show_vertices = kwargs.get("show_vertices", False)
        self.show_edges = kwargs.get("show_edges", True)
        self.show_faces = kwargs.get("show_faces", False)
        self.show_cells = kwargs.get("show_cells", True)

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
            points = transform_points(points, self.worldtransformation)
            self._vertex_xyz = dict(zip(self.volmesh.vertices(), points))  # type: ignore
        return self._vertex_xyz

    @vertex_xyz.setter
    def vertex_xyz(self, vertex_xyz):
        self._vertex_xyz = vertex_xyz

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

    def draw(self):
        """Draw the volmesh."""
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
