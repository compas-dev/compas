from typing import Any

from .geometryobject import GeometryObject
from .sceneobject import SceneStateField


class FrameObject(GeometryObject):
    """Scene object for a frame.

    Parameters
    ----------
    size
        Display size of the frame axes.

    """

    __scene_state_namespace__ = "compas.scene.FrameObject"
    __scene_state_fields__ = (SceneStateField("size", (int, float), default=1.0, required=False),)

    def __init__(self, size: float = 1.0, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.size = size
