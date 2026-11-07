from typing import Any
from typing import cast

from compas.colors import Color
from compas.geometry import Geometry

from .descriptors.color import ColorAttribute
from .sceneobject import SceneObject
from .sceneobject import SceneStateField


class GeometryObject(SceneObject):
    """Base class for scene objects for geometry objects."""

    pointcolor = ColorAttribute()
    linecolor = ColorAttribute()
    surfacecolor = ColorAttribute()
    __scene_state_namespace__ = "compas.scene.GeometryObject"
    __scene_state_fields__ = (
        SceneStateField("pointcolor", (Color, type(None)), default=None, required=False),
        SceneStateField("linecolor", (Color, type(None)), default=None, required=False),
        SceneStateField("surfacecolor", (Color, type(None)), default=None, required=False),
        SceneStateField("pointsize", (int, float), default=1.0, required=False),
        SceneStateField("linewidth", (int, float), default=1.0, required=False),
        SceneStateField("show_points", bool, default=False, required=False),
        SceneStateField("show_lines", bool, default=True, required=False),
        SceneStateField("show_surfaces", bool, default=True, required=False),
    )

    # ==========================================================================
    # Dunder methods
    # ==========================================================================

    def __init__(
        self,
        pointcolor: Color | None = None,
        linecolor: Color | None = None,
        surfacecolor: Color | None = None,
        pointsize: float = 1.0,
        linewidth: float = 1.0,
        show_points: bool = False,
        show_lines: bool = True,
        show_surfaces: bool = True,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.pointcolor = pointcolor or self.color
        self.linecolor = linecolor or self.color
        self.surfacecolor = surfacecolor or self.color
        self.pointsize = pointsize
        self.linewidth = linewidth
        self.show_points = show_points
        self.show_lines = show_lines
        self.show_surfaces = show_surfaces

    # ==========================================================================
    # Properties
    # ==========================================================================

    @property
    def geometry(self) -> Geometry:
        """The geometry represented by this scene object."""
        return cast(Geometry, self.item)
