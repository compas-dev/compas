from collections.abc import Mapping
from typing import Any
from typing import cast

from compas.colors import Color
from compas.colors.color import ColorInput
from compas.datastructures import VolMesh
from compas.geometry import transform_points

from .descriptors.colordict import ColorDictAttribute
from .sceneobject import SceneObject


class VolMeshObject(SceneObject):
    """Scene object for drawing volmesh data structures.

    See Also
    --------
    [`GraphObject`][compas.scene.GraphObject]
    [`MeshObject`][compas.scene.MeshObject]

    """

    vertexcolor = ColorDictAttribute()
    edgecolor = ColorDictAttribute()
    facecolor = ColorDictAttribute()
    cellcolor = ColorDictAttribute()

    # ==========================================================================
    # Dunder methods
    # ==========================================================================

    def __init__(
        self,
        show_vertices: bool | list[int] = False,
        show_edges: bool | list[tuple[int, int]] = True,
        show_faces: bool | list[int] = False,
        show_cells: bool | list[int] = True,
        vertexcolor: Mapping[Any, ColorInput] | Color | None = None,
        edgecolor: Mapping[Any, ColorInput] | Color | None = None,
        facecolor: Mapping[Any, ColorInput] | Color | None = None,
        cellcolor: Mapping[Any, ColorInput] | Color | None = None,
        vertexsize: float = 1.0,
        edgewidth: float = 1.0,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self._vertex_xyz: dict[int, list[float]] | None = None
        self._vertex_xyz_revision: tuple[int, ...] | None = None
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

    # ==========================================================================
    # Properties
    # ==========================================================================

    @property
    def settings(self) -> dict[str, object]:
        """The settings required to reconstruct the volmesh scene object."""
        settings = super().settings
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
    def volmesh(self) -> VolMesh:
        """The volmesh represented by this scene object.

        Setting the volmesh clears the local transformation and cached vertex
        coordinates.

        """
        return cast(VolMesh, self.item)

    @volmesh.setter
    def volmesh(self, volmesh: VolMesh) -> None:
        if self.scene is None:
            self._item_guid = volmesh.guid
            self._detached_item = volmesh
        else:
            self.scene.replace_item(self, volmesh)
        self._transformation = None
        self._vertex_xyz = None
        self._vertex_xyz_revision = None

    @property
    def vertex_xyz(self) -> dict[int, list[float]]:
        """The vertex coordinates in the scene object's world coordinate system.

        Notes
        -----
        Coordinates computed from the volmesh are cached until the local or an
        ancestor transformation changes. Explicitly assigned coordinates are
        used as-is until the local transformation or volmesh changes.

        """
        revision = self._worldtransformation_revision()
        if self._vertex_xyz is None or (self._vertex_xyz_revision is not None and self._vertex_xyz_revision != revision):
            points = self.volmesh.vertices_attributes("xyz")
            points = transform_points(points, self.worldtransformation)
            self._vertex_xyz = dict(zip(self.volmesh.vertices(), points))
            self._vertex_xyz_revision = revision
        return self._vertex_xyz

    @vertex_xyz.setter
    def vertex_xyz(self, vertex_xyz: dict[int, list[float]]) -> None:
        self._vertex_xyz = vertex_xyz
        self._vertex_xyz_revision = None

    # ==========================================================================
    # Methods
    # ==========================================================================

    def draw_vertices(self) -> list[object]:
        """Draw the vertices of the volmesh.

        The vertices are drawn based on the values of

        * `self.show_vertices`
        * `self.vertexcolor`
        * `self.vertexsize`

        Returns
        -------
        list[object]
            The identifiers of the objects representing the vertices in the visualization context.

        """
        raise NotImplementedError

    def draw_edges(self) -> list[object]:
        """Draw the edges of the volmesh.

        The edges are drawn based on the values of

        * `self.show_edges`
        * `self.edgecolor`
        * `self.edgewidth`

        Returns
        -------
        list[object]
            The identifiers of the objects representing the edges in the visualization context.

        """
        raise NotImplementedError

    def draw_faces(self) -> list[object]:
        """Draw the faces of the volmesh.

        The faces are drawn based on the values of

        * `self.show_faces`
        * `self.facecolor`

        Returns
        -------
        list[object]
            The identifiers of the objects representing the faces in the visualization context.

        """
        raise NotImplementedError

    def draw_cells(self) -> list[object]:
        """Draw the cells of the volmesh.

        The cells are drawn based on the values of

        * `self.show_cells`
        * `self.cellcolor`

        Returns
        -------
        list[object]
            The identifiers of the objects representing the cells in the visualization context.

        """
        raise NotImplementedError

    def clear_vertices(self) -> None:
        """Clear the vertices of the volmesh."""
        raise NotImplementedError

    def clear_edges(self) -> None:
        """Clear the edges of the volmesh."""
        raise NotImplementedError

    def clear_faces(self) -> None:
        """Clear the faces of the volmesh."""
        raise NotImplementedError

    def clear_cells(self) -> None:
        """Clear the cells of the volmesh."""
        raise NotImplementedError

    # ==========================================================================
    # Private helpers
    # ==========================================================================

    def _invalidate_transformation_cache(self) -> None:
        self._vertex_xyz = None
        self._vertex_xyz_revision = None
