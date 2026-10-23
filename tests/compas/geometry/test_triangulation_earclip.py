import pytest

from compas.geometry import Polygon
from compas.geometry import PolygonalSurface
from compas.geometry import normal_triangle
from compas.geometry.triangulation_earclip import earclip_polygon


def assert_valid_triangulation(polygon, triangles):
    assert len(triangles) == len(polygon) - 2
    assert all(len(triangle) == 3 for triangle in triangles)
    assert all(0 <= index < len(polygon) for triangle in triangles for index in triangle)
    assert all(polygon.normal().dot(normal_triangle([polygon[index] for index in triangle])) > 0 for triangle in triangles)
    surface = PolygonalSurface(polygon.points, triangles)
    assert surface.area() == pytest.approx(polygon.area())


def test_earclip_polygon_triangle():
    points = [
        [0, 0, 0],
        [1, 0, 0],
        [1, 1, 0],
    ]

    polygon = Polygon(points)
    faces = earclip_polygon(polygon)
    assert_valid_triangulation(polygon, faces)


def test_earclip_polygon_square():
    points = [
        [0, 0, 0],
        [1, 0, 0],
        [1, 1, 0],
        [0, 1, 0],
    ]

    polygon = Polygon(points)
    faces = earclip_polygon(polygon)
    assert_valid_triangulation(polygon, faces)


def test_earclip_polygon_wrong_winding():
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

    faces = earclip_polygon(polygon)

    assert len(faces) == len(polygon) - 2
    assert all(0 <= index < len(polygon) for triangle in faces for index in triangle)


def test_earclip_polygon_coincident_points():
    self_intersecting_polygon = Polygon(
        [
            [-1, -1, 0],
            [-1, 0, 0],
            [-1, 1, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]
    )

    earclip_polygon(self_intersecting_polygon)


def test_earclip_polygon_when_reversed():
    polygon = Polygon(
        points=[
            [0, 0, 0],
            [5, 0, 0],
            [5, 5, 0],
            [10, 5, 0],
            [10, 15, 0],
            [0, 10, 0],
        ]
    )

    triangles = earclip_polygon(polygon)
    assert_valid_triangulation(polygon, triangles)

    polygon.points.reverse()
    triangles = earclip_polygon(polygon)
    assert_valid_triangulation(polygon, triangles)
