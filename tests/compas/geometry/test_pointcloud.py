import pytest
import json
from random import random, shuffle
from compas.geometry import Box
from compas.geometry import Frame
from compas.geometry import Point  # noqa: F401
from compas.geometry import Pointcloud
from compas.geometry import Translation


class PointcloudSubclass(Pointcloud):
    pass


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

    assert pointcloud == eval(repr(pointcloud))


def test_pointcloud_data():
    points = [[random(), random(), random()] for i in range(10)]
    pointcloud = Pointcloud(points)
    other = Pointcloud.__from_data__(json.loads(json.dumps(pointcloud.__data__)))

    assert pointcloud == other
    assert pointcloud.points == other.points
    assert pointcloud.__data__ == other.__data__


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
    x_size = 10.0
    y_size = 5.0
    z_size = 3.0
    box = Box.from_width_height_depth(x_size, z_size, y_size)
    pointcloud = Pointcloud.from_box(box, 100)
    assert len(pointcloud.points) == 100
    assert all((-x_size / 2 < x < x_size / 2) and (-y_size / 2 < y < y_size / 2) and (-z_size / 2 < z < z_size / 2) for x, y, z in pointcloud.points)


def test_pointcloud_from_rotated_box():
    frame = Frame([2.0, 3.0, 4.0], [0.0, 1.0, 0.0], [-1.0, 0.0, 0.0])
    box = Box(2.0, 4.0, 6.0, frame=frame)
    pointcloud = Pointcloud.from_box(box, 100)
    local = [box.frame.to_local_coordinates(point) for point in pointcloud.points]

    assert all(-1.0 <= x <= 1.0 and -2.0 <= y <= 2.0 and -3.0 <= z <= 3.0 for x, y, z in local)


def test_pointcloud_set_operations_with_empty_clouds():
    points = Pointcloud([[0, 0, 0], [1, 0, 0]])
    empty = Pointcloud([])

    assert empty.union(points) == points
    assert points.difference(empty) == points

    empty.add(points)
    assert empty == points

    points.subtract(Pointcloud([]))
    assert len(points) == 2


def test_pointcloud_spatial_index_is_invalidated_after_mutation():
    cloud = Pointcloud([[0, 0, 0], [1, 0, 0]])
    original_tree = cloud.tree

    cloud[0] = [2, 0, 0]
    assert cloud.tree is not original_tree

    replaced_tree = cloud.tree
    cloud.transform(Translation.from_vector([1, 0, 0]))
    assert cloud.tree is not replaced_tree


def test_pointcloud_set_operations_preserve_subclasses():
    cloud = PointcloudSubclass([[0, 0, 0]])

    assert isinstance(cloud.union(Pointcloud([])), PointcloudSubclass)
    assert isinstance(cloud.difference(Pointcloud([])), PointcloudSubclass)
