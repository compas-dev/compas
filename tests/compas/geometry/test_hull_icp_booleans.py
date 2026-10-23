import pytest

from compas.geometry import Polygon
from compas.geometry import Polyhedron
from compas.geometry import boolean_difference_polygon_polygon
from compas.geometry import boolean_intersection_polygon_polygon
from compas.geometry import boolean_symmetric_difference_polygon_polygon
from compas.geometry import boolean_union_polygon_polygon
from compas.geometry import convex_hull
from compas.geometry import convex_hull_xy
from compas.geometry import icp
from compas.tolerance import TOL


def test_convex_hull():
    points = [[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1], [0.1, 0.1, 0.1]]
    vertices, faces = convex_hull(points)

    assert set(vertices) == {0, 1, 2, 3}
    assert faces.shape == (4, 3)


def test_convex_hull_xy():
    points = [[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0], [0.5, 0.5, 0]]
    vertices, edges = convex_hull_xy(points)

    assert set(vertices) == {0, 1, 2, 3}
    assert edges.shape == (4, 2)


def test_polyhedron_from_convex_hull_omits_interior_points():
    points = [[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1], [0.1, 0.1, 0.1]]
    polyhedron = Polyhedron.from_convex_hull(points)

    assert len(polyhedron.vertices) == 4
    assert len(polyhedron.faces) == 4


def test_icp_always_returns_points_and_transformation():
    source = [[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]]
    target = [[2, 3, 4], [3, 3, 4], [2, 4, 4], [2, 3, 5]]
    points, transformation = icp(source, target)

    assert TOL.is_allclose(points, target)
    assert transformation.shape == (4, 4)


def test_polygon_boolean_default_uses_shapely():
    a = Polygon([[0, 0, 0], [2, 0, 0], [2, 2, 0], [0, 2, 0]])
    b = Polygon([[1, 1, 0], [3, 1, 0], [3, 3, 0], [1, 3, 0]])

    regions = boolean_intersection_polygon_polygon(a, b)

    assert len(regions) == 1
    assert regions[0].area() == pytest.approx(1.0)


def test_polygon_boolean_preserves_holes():
    outer = Polygon([[0, 0, 0], [4, 0, 0], [4, 4, 0], [0, 4, 0]])
    inner = Polygon([[1, 1, 0], [3, 1, 0], [3, 3, 0], [1, 3, 0]])

    regions = boolean_difference_polygon_polygon(outer, inner)

    assert len(regions) == 1
    assert len(regions[0].holes) == 1
    assert regions[0].area() == pytest.approx(12.0)


def test_polygon_boolean_preserves_disconnected_components():
    a = Polygon([[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]])
    b = Polygon([[2, 0, 0], [3, 0, 0], [3, 1, 0], [2, 1, 0]])

    union = boolean_union_polygon_polygon(a, b)
    symmetric_difference = boolean_symmetric_difference_polygon_polygon(a, b)

    assert len(union) == 2
    assert len(symmetric_difference) == 2
    assert sum(region.area() for region in union) == pytest.approx(2.0)


def test_polygon_boolean_empty_result():
    a = Polygon([[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]])
    b = Polygon([[2, 0, 0], [3, 0, 0], [3, 1, 0], [2, 1, 0]])

    assert boolean_intersection_polygon_polygon(a, b) == []


def test_polygon_boolean_accepts_planar_regions():
    outer = Polygon([[0, 0, 0], [4, 0, 0], [4, 4, 0], [0, 4, 0]])
    inner = Polygon([[1, 1, 0], [3, 1, 0], [3, 3, 0], [1, 3, 0]])
    region = boolean_difference_polygon_polygon(outer, inner)[0]

    result = boolean_intersection_polygon_polygon(region, inner)

    assert result == []
