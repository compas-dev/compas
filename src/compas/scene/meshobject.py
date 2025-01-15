from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas.colors  # noqa: F401
import compas.datastructures  # noqa: F401
import compas.geometry  # noqa: F401

from .descriptors.colordict import ColorDictAttribute
from .sceneobject import SceneObject


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
    show_vertices : Union[bool, sequence[float]]
        Flag for showing or hiding the vertices, or a list of keys for the vertices to show.
        Default is ``False``.
    show_edges : Union[bool, sequence[tuple[int, int]]]
        Flag for showing or hiding the edges, or a list of keys for the edges to show.
        Default is ``True``.
    show_faces : Union[bool, sequence[int]]
        Flag for showing or hiding the faces, or a list of keys for the faces to show.
        Default is ``True``.
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

    See Also
    --------
    :class:`compas.scene.GraphObject`
    :class:`compas.scene.VolMeshObject`

    """

    vertexcolor = ColorDictAttribute()
    edgecolor = ColorDictAttribute()
    facecolor = ColorDictAttribute()

    def __init__(
        self,
        show_vertices=False,  # type: bool | list
        show_edges=False,  # type: bool | list
        show_faces=True,  # type: bool | list
        vertexcolor=None,  # type: dict | compas.colors.Color | None
        edgecolor=None,  # type: dict | compas.colors.Color | None
        facecolor=None,  # type: dict | compas.colors.Color | None
        vertexsize=1.0,  # type: float
        edgewidth=1.0,  # type: float
        **kwargs  # dict
    ):  # fmt: skip
        # type: (...) -> None
        super(MeshObject, self).__init__(**kwargs)  # type: ignore
        self.show_vertices = show_vertices
        self.show_edges = show_edges
        self.show_faces = show_faces
        self.vertexcolor = vertexcolor or self.contrastcolor
        self.edgecolor = edgecolor or self.contrastcolor
        self.facecolor = facecolor or self.color
        self.vertexsize = vertexsize
        self.edgewidth = edgewidth

    @property
    def settings(self):
        # type: () -> dict
        settings = super(MeshObject, self).settings
        # perhaps this should be renamed to just "vertices", "edges", "faces"
        settings["show_vertices"] = self.show_vertices
        settings["show_edges"] = self.show_edges
        settings["show_faces"] = self.show_faces
        # end of perhaps
        settings["vertexcolor"] = self.vertexcolor
        settings["edgecolor"] = self.edgecolor
        settings["facecolor"] = self.facecolor
        settings["vertexsize"] = self.vertexsize
        settings["edgewidth"] = self.edgewidth
        return settings

    @property
    def mesh(self):
        # type: () -> compas.datastructures.Mesh
        return self.item  # type: ignore

    @mesh.setter
    def mesh(self, mesh):
        # type: (compas.datastructures.Mesh) -> None
        self._item = mesh
        self._transformation = None

    def draw_vertices(self):
        """Draw the vertices of the mesh.

        Vertices are drawn based on the values of

        * `self.show_vertices`
        * `self.vertexcolor`
        * `self.vertextext`
        * `self.vertexsize`

        Returns
        -------
        list
            The identifiers of the objects representing the vertices in the visualization context.

        """
        raise NotImplementedError

    def draw_edges(self):
        """Draw the edges of the mesh.

        Edges are drawn based on the values of

        * `self.show_edges`
        * `self.edgecolor`
        * `self.edgetext`
        * `self.edgewidth`

        Returns
        -------
        list
            The identifiers of the objects representing the edges in the visualization context.

        """
        raise NotImplementedError

    def draw_faces(self):
        """Draw the faces of the mesh.

        Faces are drawn based on the values of

        * `self.show_faces`
        * `self.facecolor`
        * `self.facetext`

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
