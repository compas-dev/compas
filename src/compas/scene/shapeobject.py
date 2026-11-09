from typing import Any
from typing import cast

from compas.geometry import Shape

from .geometryobject import GeometryObject
from .sceneobject import SceneStateField


class ShapeObject(GeometryObject):
    """Scene object for an analytic shape.

    Parameters
    ----------
    u
        Number of discretization intervals in the first parameter direction.
    v
        Number of discretization intervals in the second parameter direction.

    """

    __scene_state_namespace__ = "compas.scene.ShapeObject"
    __scene_state_fields__ = (
        SceneStateField("u", int, default=16, required=False),
        SceneStateField("v", int, default=16, required=False),
    )

    def __init__(self, u: int = 16, v: int = 16, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.u = u
        self.v = v

    @property
    def shape(self) -> Shape:
        """The analytic shape represented by this scene object."""
        return cast(Shape, self.item)
