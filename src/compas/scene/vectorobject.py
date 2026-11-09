from typing import Any
from typing import cast

from compas.geometry import Point
from compas.geometry import Vector

from .geometryobject import GeometryObject
from .sceneobject import SceneStateField


class VectorObject(GeometryObject):
    """Scene object for a vector.

    Parameters
    ----------
    anchor
        Point at which the vector is displayed.

    """

    __scene_state_namespace__ = "compas.scene.VectorObject"
    __scene_state_fields__ = (SceneStateField("anchor", Point),)

    def __init__(self, anchor: Point | None = None, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.anchor = anchor if anchor is not None else Point(0.0, 0.0, 0.0)

    @property
    def vector(self) -> Vector:
        """The vector represented by this scene object."""
        return cast(Vector, self.item)
