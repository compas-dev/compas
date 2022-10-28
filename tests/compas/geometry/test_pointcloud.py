import random
import compas

from compas.geometry import Pointcloud


if not compas.IPY:

    def test_data():
        p = Pointcloud.from_bounds(10, 10, 10, 100)
        assert p.data == p.validate_data()
        o = Pointcloud.from_data(p.data)
        assert p == o
        assert not (p is o)
        assert o.data == o.validate_data()


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
