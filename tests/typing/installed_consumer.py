"""Static consumer coverage for an installed COMPAS wheel."""

from typing import assert_type

import numpy as np

from compas.datastructures import Mesh
from compas.geometry import Box
from compas.geometry import Brep
from compas.geometry import PlanarRegion
from compas.geometry import Point
from compas.geometry import Plane
from compas.geometry import Polygon
from compas.geometry import PolygonalSurface
from compas.geometry import Polyhedron
from compas.geometry import Tessellation
from compas.geometry import closest_point_on_polygon_xy
from compas.geometry import closest_point_on_polyline_xy
from compas.geometry import orthonormalize_axes
from compas.geometry import triangulate_polygon
from compas.geometry import triangulate_polygon_earclip
from compas.geometry import triangulate_polygon_minimum_area
from compas.geometry import triangulate_polygon_projected
from compas.geometry import triangulate_quadrilateral
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
polygon = Polygon(vertices)
polygonal_surface = PolygonalSurface(vertices, [triangles[0]])
polyhedron = Polyhedron(
    [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]],
    [[0, 2, 1], [0, 1, 3], [1, 2, 3], [2, 0, 3]],
)
planar_region = PlanarRegion(vertices)
mesh = Mesh.from_vertices_and_faces(vertices, triangles)


class CustomMesh(Mesh):
    pass


custom_mesh = CustomMesh.from_vertices_and_faces(vertices, triangles)

assert_type(Point(0.0, 0.0, 0.0).x, float)
assert_type(tessellation.number_of_triangles, int)
assert_type(tessellation.to_vertices_and_triangles(), tuple[list[list[float]], list[list[int]]])
assert_type(Box(1.0).to_polygonal_surface(), PolygonalSurface)
assert_type(Box(1.0).to_tessellation(), Tessellation)
assert_type(Brep().to_tessellation(), Tessellation)
assert_type(polygon.triangulated(), Tessellation)
assert_type(polygonal_surface.triangulated(), Tessellation)
assert_type(polyhedron.triangulated(), Tessellation)
assert_type(planar_region.triangulated(), Tessellation)
assert_type(mesh.triangulated(), Mesh)
assert_type(custom_mesh.triangulated(), CustomMesh)
assert_type(triangulate_polygon(vertices), list[list[int]])
assert_type(triangulate_polygon_earclip(vertices), list[list[int]])
assert_type(triangulate_polygon_minimum_area(vertices), list[list[int]])
assert_type(triangulate_polygon_projected(vertices, max_deviation=0.01), list[list[int]])
assert_type(triangulate_quadrilateral([*vertices, [1.0, 1.0, 0.0]]), list[list[int]])
assert_type(trimesh_gaussian_curvature((vertices, triangles)), list[float])
assert_type(trimesh_gaussian_curvature(numpy_mesh), list[float])
assert_type(closest_point_on_polyline_xy(numpy_point, vertices[:2]), list[RealInput])
assert_type(closest_point_on_polygon_xy(numpy_point, vertices), list[RealInput])
assert_type(orthonormalize_axes([1.0, 0.0, 0.0], [0.0, 1.0, 0.0]), tuple[list[RealInput], list[RealInput]])
