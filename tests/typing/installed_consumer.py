"""Static consumer coverage for an installed COMPAS wheel."""

from typing import assert_type

from compas.geometry import Point
from compas.geometry import Tessellation
from compas.geometry import trimesh_gaussian_curvature


vertices = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]
triangles = [[0, 1, 2]]
tessellation = Tessellation(vertices, triangles)

assert_type(Point(0.0, 0.0, 0.0).x, float)
assert_type(tessellation.number_of_triangles, int)
assert_type(tessellation.to_vertices_and_triangles(), tuple[list[list[float]], list[list[int]]])
assert_type(trimesh_gaussian_curvature((vertices, triangles)), list[float])
