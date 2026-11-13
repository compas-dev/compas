from __future__ import annotations

from numbers import Integral
from typing import Any
from typing import cast

from compas.geometry import Capsule
from compas.geometry import Cone
from compas.geometry import Cylinder
from compas.geometry import Shape
from compas.geometry import Sphere
from compas.geometry import Torus

from .geometryobject import GeometryObject
from .sceneobject import SceneStateField


def _validate_resolution(value: object, name: str, minimum: int) -> int:
    if not isinstance(value, Integral) or isinstance(value, bool):
        raise TypeError(f"Shape-object {name} resolution should be an integer.")
    value = int(value)
    if value < minimum:
        raise ValueError(f"Shape-object {name} resolution should be at least {minimum}.")
    return value


def _update_u_resolution(sceneobject: ShapeObject, value: object) -> None:
    if not isinstance(sceneobject.item, (Cone, Cylinder, Sphere, Torus, Capsule)):
        raise ValueError("The represented shape does not use U resolution.")
    sceneobject.u = _validate_resolution(value, "U", 3)


def _update_v_resolution(sceneobject: ShapeObject, value: object) -> None:
    if not isinstance(sceneobject.item, (Sphere, Torus, Capsule)):
        raise ValueError("The represented shape does not use V resolution.")
    minimum = 4 if isinstance(sceneobject.item, Capsule) else 3
    resolution = _validate_resolution(value, "V", minimum)
    if isinstance(sceneobject.item, Capsule) and resolution % 2:
        raise ValueError("Capsule V resolution should be even.")
    sceneobject.v = resolution


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
        SceneStateField("u", int, default=16, required=False, editable=True, update=_update_u_resolution),
        SceneStateField("v", int, default=16, required=False, editable=True, update=_update_v_resolution),
    )

    def __init__(self, u: int = 16, v: int = 16, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.u = u
        self.v = v

    @property
    def shape(self) -> Shape:
        """The analytic shape represented by this scene object."""
        return cast(Shape, self.item)
