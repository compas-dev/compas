import pytest

from compas.geometry import Point
from compas.geometry import Polygon
from compas.utilities import pairwise


def test_polygon():
    points = [[0, 0, x] for x in range(5)]
    polygon = Polygon(points)
    assert polygon.points == points
    assert polygon.lines == [(a, b) for a, b in pairwise(points + points[:1])]


def test_equality():
    points1 = [[0, 0, x] for x in range(5)]
    polygon1 = Polygon(points1)
    points2 = [[0, 0, x] for x in range(6)]
    polygon2 = Polygon(points2)
    points3 = [[0, 0, x] for x in range(5)] + [[0, 0, 0]]
    polygon3 = Polygon(points3)
    assert polygon1 == polygon1
    assert polygon1 == points1
    assert points1 == polygon1
    assert polygon1 != polygon2
    assert polygon2 != polygon1
    assert polygon1 != points2
    assert points2 != polygon1
    assert polygon1 != 1
    assert polygon1 == polygon3


def test___repr__():
    points = [[0, 0, x] for x in range(5)]
    polygon = Polygon(points)
    assert polygon == eval(repr(polygon))


def test___getitem__():
    points = [[0, 0, x] for x in range(5)]
    polygon = Polygon(points)
    for x in range(5):
        assert polygon[x] == [0, 0, x]
    with pytest.raises(IndexError):
        polygon[6] = [0, 0, 6]


def test___setitem__():
    points = [[0, 0, x] for x in range(5)]
    polygon = Polygon(points)
    point = [1, 1, 4]
    polygon[4] = point
    assert polygon[4] == point
    assert isinstance(polygon[4], Point)
    assert polygon.lines[-2].end == point
