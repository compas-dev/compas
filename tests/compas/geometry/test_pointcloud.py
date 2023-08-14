import pytest
import json
import compas
from random import random, shuffle
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
    other = Pointcloud.from_data(json.loads(json.dumps(pointcloud.to_data())))

    assert pointcloud == other
    assert pointcloud.points == other.points
    assert pointcloud.data == other.data

    if not compas.IPY:
        assert Pointcloud.validate_data(pointcloud.data)
        assert Pointcloud.validate_data(other.data)


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
