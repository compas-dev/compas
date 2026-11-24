from typing import Any
from typing import cast

from compas.geometry import Plane

from .geometryobject import GeometryObject
from .sceneobject import SceneStateField


class PlaneObject(GeometryObject):
    """Scene object for a plane.

    Parameters
    ----------
    size
        Display size of the plane.

    """

    __scene_state_namespace__ = "compas.scene.PlaneObject"
    __scene_state_fields__ = (SceneStateField("size", (int, float), default=1.0, required=False),)

    def __init__(self, size: float = 1.0, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.size = size

    @property
    def plane(self) -> Plane:
        """The plane represented by this scene object."""
        return cast(Plane, self.item)
