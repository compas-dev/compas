import random
from compas.geometry import Pointcloud


def test_equality():
    a = Pointcloud.from_bounds(10, 10, 10, 10)
    points = a.points[:]
    random.shuffle(points)
    b = Pointcloud(points)
    assert a == b


def test_inequality():
    a = Pointcloud.from_bounds(10, 10, 10, 10)
    b = Pointcloud.from_bounds(10, 10, 10, 11)
    assert a != b
    b = Pointcloud.from_bounds(10, 10, 10, 9)
    assert a != b
    b = Pointcloud.from_bounds(10, 10, 10, 10)
    assert a != b
