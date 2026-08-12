from __future__ import division
import pytest
import json
import compas
from random import random
from compas.geometry import Point
from compas.tolerance import TOL


@pytest.mark.parametrize(
    "x,y,z",
    [
        (1, 2, 3),
        (1.0, 2.0, 3.0),
        ("1.0", "2", 3.0),
        (random(), random(), random()),
    ],
)
def test_point(x, y, z):
    p = Point(x, y, z)
    x, y, z = float(x), float(y), float(z)
    assert p.x == x and p.y == y and p.z == z
    assert p[0] == x and p[1] == y and p[2] == z

    if not compas.IPY:
        assert eval(repr(p)) == p


@pytest.mark.parametrize(
    "x,y",
    [
        (1, 2),
        (1.0, 2.0),
        ("1.0", "2"),
        (random(), random()),
    ],
)
def test_point2(x, y):
    p = Point(x, y)
    x, y, z = float(x), float(y), 0.0
    assert p.x == x and p.y == y and p.z == z
    assert p[0] == x and p[1] == y and p[2] == z

    if not compas.IPY:
        assert eval(repr(p)) == p


def test_point_operators():
    a = Point(random(), random(), random())
    b = Point(random(), random(), random())
    assert a + b == [a.x + b.x, a.y + b.y, a.z + b.z]
    assert a - b == [a.x - b.x, a.y - b.y, a.z - b.z]
    assert a * 2 == [a.x * 2, a.y * 2, a.z * 2]
    assert a / 2 == [a.x / 2, a.y / 2, a.z / 2]
    assert a**3 == [a.x**3, a.y**3, a.z**3]


def test_point_equality():
    p1 = Point(1, 1, 1)
    p2 = Point(1, 1, 1)
    p3 = Point(0, 0, 0)
    assert p1 == p2
    assert not (p1 != p2)
    assert p1 != p3
    assert not (p1 == p3)


def test_point_comparison_relative():
    a = Point(random(), random(), random())
    b = Point(a.x + a.x * TOL.relative * 0.1, a.y + a.y * TOL.relative * 0.1, a.z + a.z * TOL.relative * 0.1)
    c = Point(a.x + a.x * TOL.relative, a.y + a.y * TOL.relative, a.z + a.z * TOL.relative)
    d = Point(a.x + a.x * TOL.relative * 10.0, a.y + a.y * TOL.relative * 10.0, a.z + a.z * TOL.relative * 10.0)
    assert a == b
    assert a == c
    assert a != d


def test_point_comparison_absolute():
    a = Point(0, 0, 0)
    b = Point(a.x + TOL.absolute * 0.1, a.y + TOL.absolute * 0.1, a.z + TOL.absolute * 0.1)
    c = Point(a.x + TOL.absolute, a.y + TOL.absolute, a.z + TOL.absolute)
    d = Point(a.x + TOL.absolute * 10.0, a.y + TOL.absolute * 10.0, a.z + TOL.absolute * 10.0)
    assert a == b
    assert a == c
    assert a != d


def test_point_inplace_operators():
    pass


def test_point_data():
    point = Point(random(), random(), random())
    other = Point.__from_data__(json.loads(json.dumps(point.__data__)))

    assert point == other
    assert point.__data__ == other.__data__
    assert point.guid != other.guid

    if not compas.IPY:
        assert Point.validate_data(point.__data__)
        assert Point.validate_data(other.__data__)


def test_point_distance_to_point():
    pass


def test_point_distance_to_line():
    pass


def test_point_distance_to_plane():
    pass


def test_point_on_line():
    pass


def test_point_on_segment():
    pass


def test_point_on_polyline():
    pass


def test_point_on_circle():
    pass


def test_point_in_triangle():
    pass


def test_point_in_polygon():
    pass


def test_point_in_circle():
    pass


def test_point_in_polyhedron():
    pass
