import pytest

from compas.geometry import Circle
from compas.geometry import Line
from compas.geometry import Point
from compas.geometry import Sphere
from compas.tolerance import TOL
from compas.geometry import intersection_line_line
from compas.geometry import intersection_line_line_xy
from compas.geometry import intersection_line_box_xy
from compas.geometry import intersection_line_plane
from compas.geometry import intersection_line_segment
from compas.geometry import intersection_line_triangle
from compas.geometry import intersection_line_segment_xy
from compas.geometry import intersection_plane_plane
from compas.geometry import intersection_plane_plane_plane
from compas.geometry import intersection_polyline_plane
from compas.geometry import intersection_polyline_box_xy
from compas.geometry import intersection_segment_polyline
from compas.geometry import intersection_segment_segment
from compas.geometry import intersection_segment_polyline_xy
from compas.geometry import intersection_segment_segment_xy
from compas.geometry import intersection_sphere_line
from compas.geometry import intersection_sphere_sphere
from compas.geometry import intersection_plane_circle
from compas.geometry import intersection_circle_circle_xy
from compas.geometry import intersection_ellipse_line_xy


def test_intersection_line_line_rejects_parallel_and_degenerate_lines():
    assert intersection_line_line(([0, 0, 0], [1, 0, 0]), ([0, 1, 0], [1, 1, 0])).is_empty
    assert intersection_line_line(([0, 0, 0], [0, 0, 0]), ([0, 0, 0], [0, 1, 0])).is_empty


def test_intersection_line_line_returns_only_actual_intersection():
    intersecting = intersection_line_line(([0, 0, 0], [1, 0, 0]), ([0, -1, 0], [0, 1, 0]))
    skew = intersection_line_line(([0, 0, 0], [1, 0, 0]), ([0, -1, 1], [0, 1, 1]))

    assert intersecting.results == (Point(0, 0, 0),)
    assert skew.is_empty


def test_line_and_segment_intersections_return_only_actual_points():
    line = ([-1, 0, 0], [1, 0, 0])
    segment = ([0, -1, 0], [0, 1, 0])
    skew_segment = ([0, -1, 1], [0, 1, 1])

    assert intersection_line_segment(line, segment).results == (Point(0, 0, 0),)
    assert intersection_line_segment(line, skew_segment).is_empty
    assert intersection_segment_segment(line, segment).results == (Point(0, 0, 0),)
    assert intersection_segment_segment(line, skew_segment).is_empty


def test_intersection_line_plane_returns_origin_without_truthiness_ambiguity():
    result = intersection_line_plane(([0, 0, -1], [0, 0, 1]), ([0, 0, 0], [0, 0, 1]))

    assert result.is_unique
    assert result[0] == Point(0.0, 0.0, 0.0)


def test_intersection_polyline_plane_respects_zero_limit_and_rejects_negative_limit():
    polyline = [[0, 0, -1], [0, 0, 1], [1, 0, -1]]
    plane = [0, 0, 0], [0, 0, 1]

    assert intersection_polyline_plane(polyline, plane, expected_number_of_intersections=0).is_empty
    with pytest.raises(ValueError, match="cannot be negative"):
        intersection_polyline_plane(polyline, plane, expected_number_of_intersections=-1)


def test_intersection_polyline_plane_returns_multiple_points():
    polyline = [[0, 0, -1], [0, 0, 1], [1, 0, -1]]
    result = intersection_polyline_plane(polyline, ([0, 0, 0], [0, 0, 1]))

    assert result.is_multiple
    assert result.results == (Point(0.0, 0.0, 0.0), Point(0.5, 0.0, 0.0))


def test_intersection_line_triangle_returns_unified_result():
    triangle = ([0, 0, 0], [1, 0, 0], [0, 1, 0])

    result = intersection_line_triangle(([0.25, 0.25, -1], [0.25, 0.25, 1]), triangle)
    miss = intersection_line_triangle(([2, 2, -1], [2, 2, 1]), triangle)

    assert result.is_unique
    assert result[0] == Point(0.25, 0.25, 0.0)
    assert miss.is_empty


def test_intersection_plane_plane_accepts_nonunit_normals_and_detects_opposite_parallel_normals():
    result = intersection_plane_plane(([0, 0, 0], [0, 0, 2]), ([0, 0, 0], [0, 3, 0]))

    assert result.is_unique
    line = result[0]
    assert isinstance(line, Line)
    assert TOL.is_allclose(line[0], [0, 0, 0])
    assert intersection_plane_plane(([0, 0, 0], [0, 0, 2]), ([0, 0, 1], [0, 0, -3])).is_empty


def test_intersection_plane_plane_plane_returns_unique_point():
    result = intersection_plane_plane_plane(([1, 0, 0], [1, 0, 0]), ([0, 2, 0], [0, 1, 0]), ([0, 0, 3], [0, 0, 1]))

    assert result.is_unique
    assert result[0] == Point(1, 2, 3)


def test_intersection_sphere_line():
    sphere = (3.0, 7.0, 4.0), 10.0
    line = (1.0, 0, 0.5), (2.0, 1.0, 0.5)
    result = intersection_sphere_line(sphere, line)
    assert result.is_multiple
    ipt1, ipt2 = result
    assert TOL.is_allclose(ipt1, (11.634, 10.634, 0.500), atol=1e-3)
    assert TOL.is_allclose(ipt2, (-0.634, -1.634, 0.500), atol=1e-3)


def test_intersection_sphere_line_tangent_and_invalid_inputs():
    tangent = intersection_sphere_line(([0, 0, 0], 1.0), ([-1, 1, 0], [1, 1, 0]))

    assert tangent.is_unique
    assert tangent[0] == Point(0.0, 1.0, 0.0)
    assert intersection_sphere_line(([0, 0, 0], 1.0), ([-1, 2, 0], [1, 2, 0])).is_empty

    with pytest.raises(ValueError, match="distinct"):
        intersection_sphere_line(([0, 0, 0], 1.0), ([0, 0, 0], [0, 0, 0]))
    with pytest.raises(ValueError, match="radius"):
        intersection_sphere_line(([0, 0, 0], -1.0), ([-1, 0, 0], [1, 0, 0]))


def test_intersection_sphere_sphere_classifies_intersection_geometry():
    coincident = intersection_sphere_sphere(((0, 0, 0), 1.0), ((0, 0, 0), 1.0))
    tangent = intersection_sphere_sphere(((0, 0, 0), 1.0), ((2, 0, 0), 1.0))
    circle = intersection_sphere_sphere(((0, 0, 0), 2.0), ((2, 0, 0), 2.0))

    assert coincident.is_unique
    coincident_sphere = coincident[0]
    assert isinstance(coincident_sphere, Sphere)
    assert coincident_sphere.base == Point(0, 0, 0)
    assert coincident_sphere.radius == 1.0
    assert tangent.results == (Point(1.0, 0.0, 0.0),)
    assert circle.is_unique
    intersection_circle = circle[0]
    assert isinstance(intersection_circle, Circle)
    assert intersection_circle.center == Point(1.0, 0.0, 0.0)


def test_intersection_segment_polyline_skips_nonintersecting_segments():
    segment = ([0.0, -1.0, 0.0], [0.0, 1.0, 0.0])
    polyline = [[-2.0, 2.0, 0.0], [-1.0, 2.0, 0.0], [-1.0, 0.0, 0.0], [1.0, 0.0, 0.0]]

    result = intersection_segment_polyline(segment, polyline)

    assert result.results == (Point(0.0, 0.0, 0.0),)


def test_intersection_segment_polyline_returns_empty_result():
    result = intersection_segment_polyline(([0, 0, 0], [1, 0, 0]), [[0, 1, 0], [1, 1, 0]])

    assert result.is_empty


def test_intersection_line_line_xy_accepts_2d_coordinates_and_returns_3d_point():
    result = intersection_line_line_xy(([0, 0], [1, 1]), ([0, 1], [1, 0]))

    assert result.results == (Point(0.5, 0.5, 0.0),)


def test_intersection_line_segment_xy_distinguishes_line_from_segment():
    line = ([0, 0], [1, 0])

    assert intersection_line_segment_xy(line, ([0.5, -1], [0.5, 1])).results == (Point(0.5, 0.0, 0.0),)
    assert intersection_line_segment_xy(line, ([0.5, 1], [0.5, 2])).is_empty


def test_intersection_segment_segment_xy_requires_point_on_both_segments():
    assert intersection_segment_segment_xy(([0, 0], [1, 0]), ([0.5, -1], [0.5, 1])).results == (Point(0.5, 0.0, 0.0),)
    assert intersection_segment_segment_xy(([0, 0], [1, 0]), ([2, -1], [2, 1])).is_empty


def test_intersection_segment_polyline_xy_skips_nonintersecting_segments():
    segment = ([0, -1], [0, 1])
    polyline = [[-2, 2], [-1, 2], [-1, 0], [1, 0]]

    assert intersection_segment_polyline_xy(segment, polyline).results == (Point(0.0, 0.0, 0.0),)
    assert intersection_segment_polyline_xy(segment, [[1, 2], [2, 2]]).is_empty


def test_intersection_line_box_xy_returns_unique_points_consistently():
    box = [[0, 0], [1, 0], [1, 1], [0, 1]]

    assert intersection_line_box_xy(([-1, 0.5], [2, 0.5]), box).results == (Point(1.0, 0.5, 0.0), Point(0.0, 0.5, 0.0))
    assert intersection_line_box_xy(([-1, 1], [0, 0]), box).results == (Point(0.0, 0.0, 0.0),)
    assert intersection_line_box_xy(([-1, 2], [2, 2]), box).is_empty


def test_intersection_polyline_box_xy_deduplicates_corner_hits():
    box = [[0, 0], [1, 0], [1, 1], [0, 1]]
    polyline = [[-1, -1], [0, 0], [2, 2]]

    assert intersection_polyline_box_xy(polyline, box).results == (Point(0.0, 0.0, 0.0), Point(1.0, 1.0, 0.0))


@pytest.mark.parametrize("function", [intersection_line_box_xy, intersection_polyline_box_xy])
def test_xy_box_intersections_require_four_corners(function):
    with pytest.raises(ValueError, match="four corners"):
        function(([-1, 0], [2, 0]), [[0, 0], [1, 0], [1, 1]])


def test_intersection_plane_circle():
    plane = (0, 0, 0), (0, 0, 1)
    circle = ((3.0, 7.0, 4.0), (0, 1, 0)), 10.0
    result = intersection_plane_circle(plane, circle)
    assert result.is_multiple
    ipt1, ipt2 = result
    assert TOL.is_allclose(ipt1, (-6.165, 7.000, 0.000), atol=1e-3)
    assert TOL.is_allclose(ipt2, (12.165, 7.000, 0.000), atol=1e-3)


def test_intersection_circle_circle_xy():
    circle1 = ((0.0, 0.0, 0.0), (0, 0, 1)), 10.0
    circle2 = ((3.0, 7.0, 0.0), (0, 0, 1)), 10.0
    result = intersection_circle_circle_xy(circle1, circle2)
    assert result.is_multiple
    ipt1, ipt2 = result
    assert isinstance(ipt1, Point)
    assert isinstance(ipt2, Point)
    assert TOL.is_allclose(ipt1, (9.999, -0.142, 0.000), atol=1e-3)
    assert TOL.is_allclose(ipt2, (-6.999, 7.142, 0.000), atol=1e-3)


def test_intersection_circle_circle_xy_classifies_secant_tangent_and_disjoint_circles():
    circle1 = (([0, 0, 0], [0, 0, 1]), 1.0)

    secant = intersection_circle_circle_xy(circle1, (([1, 0, 0], [0, 0, 1]), 1.0))
    tangent = intersection_circle_circle_xy(circle1, (([2, 0, 0], [0, 0, 1]), 1.0))

    coincident = intersection_circle_circle_xy(circle1, (([0, 0, 0], [0, 0, 1]), 1.0))

    assert secant.is_multiple
    assert tangent.results == (Point(1.0, 0.0, 0.0),)
    assert intersection_circle_circle_xy(circle1, (([3, 0, 0], [0, 0, 1]), 1.0)).is_empty
    assert coincident.is_single
    assert isinstance(coincident[0], Circle)


@pytest.mark.parametrize("radius", [0.0, -1.0])
def test_intersection_circle_circle_xy_rejects_nonpositive_radius(radius):
    with pytest.raises(ValueError, match="positive"):
        intersection_circle_circle_xy((([0, 0, 0], [0, 0, 1]), radius), (([1, 0, 0], [0, 0, 1]), 1.0))


def test_intersection_ellipse_line_xy_classifies_secant_tangent_and_disjoint_lines():
    assert intersection_ellipse_line_xy((2.0, 1.0), ([-3, 0], [3, 0])).results == (
        Point(2.0, 0.0, 0.0),
        Point(-2.0, 0.0, 0.0),
    )
    assert intersection_ellipse_line_xy((2.0, 1.0), ([-3, 1], [3, 1])).results == (Point(0.0, 1.0, 0.0),)
    assert intersection_ellipse_line_xy((2.0, 1.0), ([-3, 2], [3, 2])).is_empty


@pytest.mark.parametrize("ellipse", [(0.0, 1.0), (2.0, 0.0), (-2.0, 1.0)])
def test_intersection_ellipse_line_xy_rejects_nonpositive_axes(ellipse):
    with pytest.raises(ValueError, match="positive"):
        intersection_ellipse_line_xy(ellipse, ([-3, 0], [3, 0]))


def test_intersection_ellipse_line_xy_rejects_degenerate_line():
    with pytest.raises(ValueError, match="distinct"):
        intersection_ellipse_line_xy((2.0, 1.0), ([0, 0], [0, 0]))
