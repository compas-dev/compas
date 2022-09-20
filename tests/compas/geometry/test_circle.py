from compas.geometry import Circle

# These imports are used to check __repr__.
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


def test_equality():
    point = [0, 0, 0]
    vector = [1, 0, 0]
    plane = (point, vector)
    c = Circle(plane, 1.0)
    assert c == (plane, 1.0)
    assert c == Circle(plane, 1.0)
    assert c != 1.0
    assert c != (plane, 2.0)


def test___repr__():
    point = [0, 0, 0]
    vector = [1, 0, 0]
    plane = (point, vector)
    c = Circle(plane, 1.0)
    assert c == eval(repr(c))


def test___getitem__():
    point = [0, 0, 0]
    vector = [1, 0, 0]
    plane = (point, vector)
    c = Circle(plane, 1.0)
    assert c[0] == plane
    assert c[1] == 1.0
