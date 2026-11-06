"""Static consumer coverage for an installed COMPAS wheel."""

from typing import assert_type

import numpy as np

from compas.geometry import Point
from compas.geometry import Plane
from compas.geometry import Tessellation
from compas.geometry import closest_point_on_polygon_xy
from compas.geometry import closest_point_on_polyline_xy
from compas.geometry import orthonormalize_axes
from compas.geometry import trimesh_gaussian_curvature
from compas.typing import PointLike
from compas.typing import RealInput
from compas.typing import VerticesFaces


vertices = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]
triangles = [[0, 1, 2]]
tessellation = Tessellation(vertices, triangles)
numpy_point: PointLike = np.asarray([0.0, 0.0, 0.0], dtype=np.float32)
numpy_mesh: VerticesFaces = (
    np.asarray(vertices, dtype=np.float32),
    np.asarray(triangles, dtype=np.int32),
)
Plane(numpy_point, np.asarray([0, 0, 1], dtype=np.int64))

assert_type(Point(0.0, 0.0, 0.0).x, float)
assert_type(tessellation.number_of_triangles, int)
assert_type(tessellation.to_vertices_and_triangles(), tuple[list[list[float]], list[list[int]]])
assert_type(trimesh_gaussian_curvature((vertices, triangles)), list[float])
assert_type(trimesh_gaussian_curvature(numpy_mesh), list[float])
assert_type(closest_point_on_polyline_xy(numpy_point, vertices[:2]), list[RealInput])
assert_type(closest_point_on_polygon_xy(numpy_point, vertices), list[RealInput])
assert_type(orthonormalize_axes([1.0, 0.0, 0.0], [0.0, 1.0, 0.0]), tuple[list[RealInput], list[RealInput]])
