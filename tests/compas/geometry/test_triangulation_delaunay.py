import numpy as np

from compas.geometry import Point
from compas.geometry import delaunay_triangulation


def test_delaunay_triangulation_returns_triangle_indices():
    points = [[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]]

    triangles = delaunay_triangulation(points)

    assert isinstance(triangles, np.ndarray)
    assert triangles.shape == (2, 3)
    assert set(triangles.flat) == {0, 1, 2, 3}


def test_delaunay_triangulation_accepts_point_objects_and_ignores_z():
    planar = [Point(0, 0, 0), Point(2, 0, 0), Point(2, 1, 0), Point(0, 1, 0)]
    nonplanar = [Point(point.x, point.y, index) for index, point in enumerate(planar)]

    planar_triangles = delaunay_triangulation(planar)
    nonplanar_triangles = delaunay_triangulation(nonplanar)

    assert np.array_equal(planar_triangles, nonplanar_triangles)
