from compas.geometry import Circle
from compas.geometry import Plane  # noqa: F401
from compas.geometry import Point  # noqa: F401
from compas.geometry import Vector  # noqa: F401


def test_circle():
    point = [0, 0, 0]
    vector = [1, 0, 0]
    plane = (point, vector)
    c = Circle(plane, 1.0)
    assert c.radius == 1.0
    assert c.plane == plane
    assert c == (plane, 1.0)
    assert c == Circle(plane, 1.0)
    assert c != 1.0
    assert c != (plane, 2.0)
    assert c == eval(repr(c))
