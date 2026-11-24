from __future__ import annotations

from numbers import Integral
from typing import Any
from typing import cast

from compas.geometry import Surface

from .geometryobject import GeometryObject
from .sceneobject import SceneStateField


def _validate_resolution(value: object, name: str) -> int:
    if not isinstance(value, Integral) or isinstance(value, bool):
        raise TypeError(f"Surface-object {name} resolution should be an integer.")
    value = int(value)
    if value < 1:
        raise ValueError(f"Surface-object {name} resolution should be at least 1.")
    return value


def _update_u_resolution(sceneobject: SurfaceObject, value: object) -> None:
    sceneobject.u = _validate_resolution(value, "U")


def _update_v_resolution(sceneobject: SurfaceObject, value: object) -> None:
    sceneobject.v = _validate_resolution(value, "V")


class SurfaceObject(GeometryObject):
    """Scene object for a parametric surface.

    Parameters
    ----------
    u
        Number of discretization intervals in the first parameter direction.
    v
        Number of discretization intervals in the second parameter direction.

    """

    __scene_state_namespace__ = "compas.scene.SurfaceObject"
    __scene_state_fields__ = (
        SceneStateField("u", int, default=16, required=False, editable=True, update=_update_u_resolution),
        SceneStateField("v", int, default=16, required=False, editable=True, update=_update_v_resolution),
    )

    def __init__(self, u: int = 16, v: int = 16, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.u = u
        self.v = v

    @property
    def surface(self) -> Surface:
        """The parametric surface represented by this scene object."""
        return cast(Surface, self.item)
