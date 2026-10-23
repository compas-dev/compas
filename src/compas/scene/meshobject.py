from collections.abc import Mapping
from typing import Any
from typing import cast

from compas.colors import Color
from compas.colors.color import ColorInput
from compas.datastructures import Mesh

from .descriptors.colordict import ColorDictAttribute
from .sceneobject import SceneObject


class MeshObject(SceneObject):
    """Base class for all mesh scene objects.

    See Also
    --------
    [`GraphObject`][compas.scene.GraphObject]
    [`VolMeshObject`][compas.scene.VolMeshObject]

    """

    vertexcolor = ColorDictAttribute()
    edgecolor = ColorDictAttribute()
    facecolor = ColorDictAttribute()

    # ==========================================================================
    # Dunder methods
    # ==========================================================================

    def __init__(
        self,
        show_vertices: bool | list[int] = False,
        show_edges: bool | list[tuple[int, int]] = False,
        show_faces: bool | list[int] = True,
        vertexcolor: Mapping[Any, ColorInput] | Color | None = None,
        edgecolor: Mapping[Any, ColorInput] | Color | None = None,
        facecolor: Mapping[Any, ColorInput] | Color | None = None,
        vertexsize: float = 1.0,
        edgewidth: float = 1.0,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.show_vertices = show_vertices
        self.show_edges = show_edges
        self.show_faces = show_faces
        self.vertexcolor = vertexcolor or self.contrastcolor
        self.edgecolor = edgecolor or self.contrastcolor
        self.facecolor = facecolor or self.color
        self.vertexsize = vertexsize
        self.edgewidth = edgewidth

    # ==========================================================================
    # Properties
    # ==========================================================================

    @property
    def settings(self) -> dict[str, object]:
        """The settings required to reconstruct the mesh scene object."""
        settings = super().settings
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
    def mesh(self) -> Mesh:
        """The mesh represented by this scene object.

        Setting the mesh clears the local transformation.

        """
        return cast(Mesh, self.item)

    @mesh.setter
    def mesh(self, mesh: Mesh) -> None:
        self._item = mesh
        self._transformation = None

    # ==========================================================================
    # Methods
    # ==========================================================================

    def draw_vertices(self) -> list[object]:
        """Draw the vertices of the mesh.

        Vertices are drawn based on the values of

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
        """Draw the edges of the mesh.

        Edges are drawn based on the values of

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
        """Draw the faces of the mesh.

        Faces are drawn based on the values of

        * `self.show_faces`
        * `self.facecolor`

        Returns
        -------
        list[object]
            The identifiers of the objects representing the faces in the visualization context.

        """
        raise NotImplementedError

    def clear_vertices(self) -> None:
        """Clear the vertices of the mesh."""
        raise NotImplementedError

    def clear_edges(self) -> None:
        """Clear the edges of the mesh."""
        raise NotImplementedError

    def clear_faces(self) -> None:
        """Clear the faces of the mesh."""
        raise NotImplementedError
