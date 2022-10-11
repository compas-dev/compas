import math
import pytest
import random
import compas

from compas.geometry import Point
from compas.geometry import Polyline
from compas.utilities import pairwise


if not compas.IPY:

    def test_data():
        p = Polyline([Point(random.random(), random.random(), random.random()) for i in range(10)])
        assert p.data == p.validate_data()
        o = Polyline.from_data(p.data)
        assert p == o
        assert not (p is o)
        assert o.data == o.validate_data()


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


@pytest.mark.parametrize(
    "coords,expected",
    [
        (
            [[0.0, 0.0, 0.0], [100.0, 0.0, 0.0]],
            [
                [0.0, 0.0, 0.0],
                [20.0, 0.0, 0.0],
                [40.0, 0.0, 0.0],
                [60.0, 0.0, 0.0],
                [80.0, 0.0, 0.0],
                [100.0, 0.0, 0.0],
            ],
        ),
        (
            [[0.0, 0.0, 0.0], [100.0, 0.0, 0.0], [300.0, 0.0, 0.0]],
            [
                [0.0, 0.0, 0.0],
                [60.0, 0.0, 0.0],
                [120.0, 0.0, 0.0],
                [180.0, 0.0, 0.0],
                [240.0, 0.0, 0.0],
                [300.0, 0.0, 0.0],
            ],
        ),
        (
            [
                [0.0, 0.0, 0.0],
                [200.0, 0.0, 0.0],
                [200.0, 200.0, 0.0],
                [0.0, 200.0, 0.0],
                [0.0, 0.0, 0.0],
            ],
            [
                [0.0, 0.0, 0.0],
                [160.0, 0.0, 0.0],
                [200.0, 120.0, 0.0],
                [120.0, 200.0, 0.0],
                [0.0, 160.0, 0.0],
                [0.0, 0.0, 0.0],
            ],
        ),
    ],
)
def test_polyline_divide(coords, expected):
    assert expected == Polyline(coords).divide_polyline(5)


@pytest.mark.parametrize(
    "coords,expected",
    [
        ([[0.0, 0.0, 0.0], [100.0, 0.0, 0.0]], [[0.0, 0.0, 0.0], [100.0, 0.0, 0.0]]),
        (
            [[0.0, 0.0, 0.0], [100.0, 0.0, 0.0], [300.0, 0.0, 0.0]],
            [[0, 0, 0], [100, 0, 0], [200, 0, 0], [300, 0, 0]],
        ),
        (
            [
                [0.0, 0.0, 0.0],
                [200.0, 0.0, 0.0],
                [200.0, 200.0, 0.0],
                [0.0, 200.0, 0.0],
                [0.0, 0.0, 0.0],
            ],
            [
                [0, 0, 0],
                [100, 0, 0],
                [200, 0, 0],
                [200, 100, 0],
                [200, 200, 0],
                [100.0, 200, 0],
                [0, 200, 0],
                [0, 100.0, 0],
                [0, 0, 0],
            ],
        ),
    ],
)
def test_polyline_divide_length(coords, expected):
    assert expected == Polyline(coords).divide_polyline_by_length(100)


@pytest.mark.parametrize(
    "coords,expected",
    [
        ([[0.0, 0.0, 0.0], [100.0, 0.0, 0.0]], [[0.0, 0.0, 0.0], [80.0, 0.0, 0.0]]),
    ],
)
def test_polyline_divide_length_strict1(coords, expected):
    assert expected == Polyline(coords).divide_polyline_by_length(80)


@pytest.mark.parametrize(
    "coords,expected",
    [
        (
            [[0.0, 0.0, 0.0], [100.0, 0.0, 0.0]],
            [[0.0, 0.0, 0.0], [80.0, 0.0, 0.0], [100.0, 0.0, 0.0]],
        ),
    ],
)
def test_polyline_divide_length_strict2(coords, expected):
    assert expected == Polyline(coords).divide_polyline_by_length(80, False)


@pytest.mark.parametrize(
    "coords,input,expected",
    [
        (
            [
                [0.0, 0.0, 0.0],
                [1.0, 0.0, 0.0],
                [1.0, 1.0, 0.0],
                [0.0, 1.0, 0.0],
                [0.0, 0.0, 0.0],
            ],
            math.pi / 2,
            [
                Polyline([[0.0, 0.0, 0.0], [1, 0.0, 0.0]]),
                Polyline([[1, 0.0, 0.0], [1, 1, 0.0]]),
                Polyline([[1, 1, 0.0], [0.0, 1, 0.0]]),
                Polyline([[0.0, 1, 0.0], [0.0, 0.0, 0.0]]),
            ],
        ),
    ],
)
def test_polyline_split_at_corners(coords, input, expected):
    assert expected == Polyline(coords).split_at_corners(input)


@pytest.mark.parametrize(
    "coords,input,expected",
    [
        ([[0.0, 0.0, 0.0], [100.0, 0.0, 0.0]], [50, 0, 0], [1.0, 0.0, 0.0]),
        (
            [[0.0, 0.0, 0.0], [50.0, 0.0, 0.0], [100.0, 100.0, 0.0]],
            [50, 0, 0],
            [1.0, 0.0, 0.0],
        ),
    ],
)
def test_polyline_tangent_at_point(coords, input, expected):
    assert expected == Polyline(coords).tangent_at_point_on_polyline(input)


@pytest.mark.parametrize(
    "coords,input,expected",
    [
        (
            [[0, 0, 0], [1, 0, 0], [2, 0, 0], [2, 2, 0]],
            1.5,
            [[0, 0, 0], [1, 0, 0], [2, 0, 0], [2, 3.5, 0]],
        ),
        (
            [[0, 0, 0], [1, 0, 0], [2, 0, 0], [2, 2, 0]],
            -2.5,
            [[0, 0, 0], [1, 0, 0], [2, 0, 0], [2, -0.5, 0]],
        ),
        (
            [[0, 0, 0], [1, 0, 0], [2, 0, 0], [2, 2, 0]],
            (2, 2),
            [[-2, 0, 0], [1, 0, 0], [2, 0, 0], [2, 4, 0]],
        ),
        (
            [[0, 0, 0], [1, 0, 0], [2, 0, 0], [2, 2, 0]],
            (2, 0),
            [[-2, 0, 0], [1, 0, 0], [2, 0, 0], [2, 2, 0]],
        ),
    ],
)
def test_polyline_extend(coords, input, expected):
    assert expected == Polyline(coords).extended(input)


@pytest.mark.parametrize(
    "coords,input,expected",
    [
        (
            [[0, 0, 0], [1, 0, 0], [2, 0, 0], [2, 2, 0]],
            0.5,
            [[0, 0, 0], [1, 0, 0], [2, 0, 0], [2, 1.5, 0]],
        ),
        (
            [[0, 0, 0], [1, 0, 0], [2, 0, 0], [2, 2, 0]],
            2,
            [[0, 0, 0], [1, 0, 0], [2, 0, 0]],
        ),
        (
            [[0, 0, 0], [1, 0, 0], [2, 0, 0], [2, 2, 0]],
            (0.5, 2.5),
            [[0.5, 0, 0], [1, 0, 0], [1.5, 0, 0]],
        ),
        ([[0, 0, 0], [1, 0, 0], [2, 0, 0], [2, 2, 0]], (1, 2), [[1, 0, 0], [2, 0, 0]]),
    ],
)
def test_polyline_shortened(coords, input, expected):
    assert expected == Polyline(coords).shortened(input)
