import pytest
import json
import compas
from random import random
from compas.geometry import Point
from compas.geometry import Polygon
from compas.utilities import pairwise


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
def test_polygon(points):
    polygon = Polygon(points)
    assert polygon.points == points
    assert polygon.lines == [(a, b) for a, b in pairwise(points + points[:1])]
    assert polygon.points[-1] != polygon.points[0]
    assert polygon.lines[0][0] == polygon.points[0]
    assert polygon.lines[-1][1] == polygon.points[0]
    assert polygon.lines[-1][0] == polygon.points[-1]

    if not compas.IPY:
        assert polygon == eval(repr(polygon))


def test_polygon_constructor_does_not_modify_input_params():
    pts = [[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0], [0, 0, 0]]

    polygon = Polygon(pts)
    assert len(pts) == 5
    assert len(polygon.points) == 4, "The last point (matching the first) should have been removed"


def test_polygon_data():
    points = [[random(), random(), random()] for i in range(10)]
    polygon = Polygon(points)
    other = Polygon.from_data(json.loads(json.dumps(polygon.to_data())))

    assert polygon == other
    assert polygon.points == other.points
    assert polygon.data == other.data

    if not compas.IPY:
        assert Polygon.validate_data(polygon.data)
        assert Polygon.validate_data(other.data)


def test_polygon__eq__():
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


def test_polygon__getitem__():
    points = [[0, 0, x] for x in range(5)]
    polygon = Polygon(points)
    for x in range(5):
        assert polygon[x] == [0, 0, x]
    with pytest.raises(IndexError):
        polygon[6] = [0, 0, 6]


def test_polygon__setitem__():
    points = [[0, 0, x] for x in range(5)]
    polygon = Polygon(points)
    point = [1, 1, 4]
    polygon[4] = point
    assert polygon[4] == point
    assert isinstance(polygon[4], Point)
    assert polygon.lines[-2].end == point


def test_polygon_to_vertices_and_faces():

    points = [
        [332.639635, -3824, 1435.771272],
        [422.117559, -3301, 1563.558991],
        [642.370911, -3534, 1878.113376],
        [505.286143, -3908, 1682.336037],
        [477.180897, -3578, 1642.197587],
        [448.502075, -3634, 1601.239985],
        [441.619158, -3998, 1591.41016],
        [339.522553, -4195, 1445.601096],
        [189.245526, -3981, 1230.983261],
        [186.377644, -3672, 1226.887501],
        [278.149874, -3619, 1357.951828],
        [332.639635, -3414, 1435.771272],
        [192.686985, -3362, 1235.898173],
        [136.476494, -3688, 1155.621273],
        [63.05871, -4035, 1050.769811],
        [-51.083001, -3865, 887.758554],
        [-2.329003, -3686, 957.386478],
        [86.575344, -3695, 1084.355045],
        [69.368051, -3436, 1059.780484],
        [74.530239, -3315, 1067.152852],
        [219.071501, -3154, 1273.579167],
        [277.576297, -3227, 1357.132676],
        [336.081094, -3052, 1440.686184],
        [458.252875, -3120, 1615.16557],
        [718.083001, -3144, 1986.241446],
        [595.337643, -3295, 1810.942908],
        [459.973604, -3252, 1617.623026],
        [369.348527, -3265, 1488.197003],
        [377.952174, -3452, 1500.484283],
    ]

    polygon = Polygon(points)
    polygon.points.reverse()

    vertices, faces = polygon.to_vertices_and_faces(True)

    assert list(polygon) == vertices
    assert faces == [
        [2, 3, 4],
        [5, 6, 7],
        [7, 8, 9],
        [12, 13, 14],
        [14, 15, 16],
        [17, 18, 19],
        [19, 20, 21],
        [21, 22, 23],
        [23, 24, 25],
        [27, 28, 0],
        [1, 2, 4],
        [7, 9, 10],
        [14, 16, 17],
        [23, 25, 26],
        [0, 1, 4],
        [12, 14, 17],
        [21, 23, 26],
        [0, 4, 5],
        [12, 17, 19],
        [21, 26, 27],
        [0, 5, 7],
        [11, 12, 19],
        [19, 21, 27],
        [0, 7, 10],
        [11, 19, 27],
        [0, 10, 11],
        [11, 27, 0],
    ]

    # test polygon with self-coinciding vertices
    self_intersecting_polygon = Polygon(
        [
            [-1, -1, 0],
            [-1, 0, 0],
            [-1, 1, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]
    )

    with pytest.raises(IndexError):
        vertices,
        faces = self_intersecting_polygon.to_vertices_and_faces(True)
