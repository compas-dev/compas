import pytest
import json
import compas
from random import random, shuffle
from compas.geometry import Box
from compas.geometry import Point  # noqa: F401
from compas.geometry import Pointcloud


@pytest.mark.parametrize(
    "points",
    [
        [[0, 0, 0], [1, 0, 0]],
        [[0, 0, 0], [1, 0, 0], [1, 1, 0]],
        [[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]],
        [[0, 0, x] for x in range(5)],
        [[random(), random(), random()] for i in range(10)],
    ],
)
def test_pointcloud(points):
    pointcloud = Pointcloud(points)
    assert pointcloud.points == points

    if not compas.IPY:
        assert pointcloud == eval(repr(pointcloud))


def test_pointcloud_data():
    points = [[random(), random(), random()] for i in range(10)]
    pointcloud = Pointcloud(points)
    other = Pointcloud.__from_data__(json.loads(json.dumps(pointcloud.__data__)))

    assert pointcloud == other
    assert pointcloud.points == other.points
    assert pointcloud.__data__ == other.__data__

    if not compas.IPY:
        assert Pointcloud.validate_data(pointcloud.__data__)
        assert Pointcloud.validate_data(other.__data__)


def test_pointcloud__eq__():
    a = Pointcloud.from_bounds(10, 10, 10, 10)
    points = a.points[:]
    shuffle(points)
    b = Pointcloud(points)
    assert a == b


def test_pointcloud__neq__():
    a = Pointcloud.from_bounds(10, 10, 10, 10)
    b = Pointcloud.from_bounds(10, 10, 10, 11)
    assert a != b
    b = Pointcloud.from_bounds(10, 10, 10, 9)
    assert a != b
    b = Pointcloud.from_bounds(10, 10, 10, 10)
    assert a != b


def test_pointcloud_from_box():
    x_size = 10
    y_size = 5
    z_size = 3
    box = Box.from_width_height_depth(x_size, z_size, y_size)
    pointcloud = Pointcloud.from_box(box, 100)
    assert len(pointcloud.points) == 100
    assert all((-x_size / 2 < x < x_size / 2) and (-y_size / 2 < y < y_size / 2) and (-z_size / 2 < z < z_size) for x, y, z in pointcloud.points)
