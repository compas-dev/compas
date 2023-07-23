import pytest

from compas.geometry import Point
from compas.geometry import Polyline
from compas.utilities import pairwise


def test_polyline():
    points = [[0, 0, x] for x in range(5)]
    polyline = Polyline(points)
    assert polyline.points == points
    assert polyline.lines == [(a, b) for a, b in pairwise(points)]


def test_equality():
    points1 = [[0, 0, x] for x in range(5)]
    polyline1 = Polyline(points1)
    points2 = [[0, 0, x] for x in range(6)]
    polyline2 = Polyline(points2)
    assert polyline1 == polyline1
    assert polyline1 == points1
    assert points1 == polyline1
    assert polyline1 != polyline2
    assert polyline2 != polyline1
    assert polyline1 != points2
    assert points2 != polyline1
    assert polyline1 != 1


def test___repr__():
    points = [[0, 0, x] for x in range(5)]
    polyline = Polyline(points)
    assert polyline == eval(repr(polyline))


def test___getitem__():
    points = [[0, 0, x] for x in range(5)]
    polyline = Polyline(points)
    for x in range(5):
        assert polyline[x] == [0, 0, x]
    with pytest.raises(IndexError):
        polyline[6] = [0, 0, 6]


def test___setitem__():
    points = [[0, 0, x] for x in range(5)]
    polyline = Polyline(points)
    point = [1, 1, 4]
    polyline[4] = point
    assert polyline[4] == point
    assert isinstance(polyline[4], Point)
    assert polyline.lines[-1].end == point
