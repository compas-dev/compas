from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas.colors  # noqa: F401
import compas.datastructures  # noqa: F401
import compas.geometry  # noqa: F401
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

    def __init__(
        self,
        show_vertices=False,  # type: bool | list
        show_edges=True,  # type: bool | list
        show_faces=False,  # type: bool | list
        show_cells=True,  # type: bool | list
        vertexcolor=None,  # type: compas.colors.Color | dict | None
        edgecolor=None,  # type: compas.colors.Color | dict | None
        facecolor=None,  # type: compas.colors.Color | dict | None
        cellcolor=None,  # type: compas.colors.Color | dict | None
        vertexsize=1.0,  # type: float
        edgewidth=1.0,  # type: float
        **kwargs  # type: dict
    ):  # fmt: skip
        # type: (...) -> None
        super(VolMeshObject, self).__init__(**kwargs)  # type: ignore
        self._vertex_xyz = None
        self.show_vertices = show_vertices
        self.show_edges = show_edges
        self.show_faces = show_faces
        self.show_cells = show_cells
        self.vertexcolor = vertexcolor or self.color
        self.edgecolor = edgecolor or self.color
        self.facecolor = facecolor or self.color
        self.cellcolor = cellcolor or self.color
        self.vertexsize = vertexsize
        self.edgewidth = edgewidth

    @property
    def settings(self):
        # type: () -> dict
        settings = super(VolMeshObject, self).settings
        settings["show_vertices"] = self.show_vertices
        settings["show_edges"] = self.show_edges
        settings["show_faces"] = self.show_faces
        settings["show_cells"] = self.show_cells
        settings["vertexcolor"] = self.vertexcolor
        settings["edgecolor"] = self.edgecolor
        settings["facecolor"] = self.facecolor
        settings["cellcolor"] = self.cellcolor
        return settings

    @property
    def volmesh(self):
        # type: () -> compas.datastructures.VolMesh
        return self.item  # type: ignore

    @volmesh.setter
    def volmesh(self, volmesh):
        # type: (compas.datastructures.VolMesh) -> None
        self._item = volmesh
        self._transformation = None
        self._vertex_xyz = None

    @property
    def transformation(self):
        # type: () -> compas.geometry.Transformation | None
        return self._transformation

    @transformation.setter
    def transformation(self, transformation):
        # type: (compas.geometry.Transformation) -> None
        self._vertex_xyz = None
        self._transformation = transformation

    @property
    def vertex_xyz(self):
        # type: () -> dict[int, list[float]]
        if self._vertex_xyz is None:
            points = self.volmesh.vertices_attributes("xyz")  # type: ignore
            points = transform_points(points, self.worldtransformation)
            self._vertex_xyz = dict(zip(self.volmesh.vertices(), points))  # type: ignore
        return self._vertex_xyz  # type: ignore

    @vertex_xyz.setter
    def vertex_xyz(self, vertex_xyz):
        # type: (dict[int, list[float]]) -> None
        self._vertex_xyz = vertex_xyz

    def draw_vertices(self):
        """Draw the vertices of the mesh.

        The vertices are drawn based on the values of

        * `self.show_vertices`
        * `self.vertexcolor`
        * `self.vertexsize`

        Returns
        -------
        list
            The identifiers of the objects representing the vertices in the visualization context.

        """
        raise NotImplementedError

    def draw_edges(self):
        """Draw the edges of the mesh.

        The edges are drawn based on the values of

        * `self.show_edges`
        * `self.edgecolor`
        * `self.edgewidth`

        Returns
        -------
        list
            The identifiers of the objects representing the edges in the visualization context.

        """
        raise NotImplementedError

    def draw_faces(self):
        """Draw the faces of the mesh.

        The faces are drawn based on the values of

        * `self.show_faces`
        * `self.facecolor`

        Returns
        -------
        list
            The identifiers of the objects representing the faces in the visualization context.

        """
        raise NotImplementedError

    def draw_cells(self):
        """Draw the cells of the mesh.

        The cells are drawn based on the values of

        * `self.show_cells`
        * `self.cellcolor`

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
