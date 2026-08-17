import pytest

from compas.tolerance import TOL
from compas.geometry import intersection_line_line
from compas.geometry import intersection_line_line_xy
from compas.geometry import intersection_line_box_xy
from compas.geometry import intersection_line_plane
from compas.geometry import intersection_line_segment_xy
from compas.geometry import intersection_plane_plane
from compas.geometry import intersection_plane_plane_plane
from compas.geometry import intersection_polyline_plane
from compas.geometry import intersection_polyline_box_xy
from compas.geometry import intersection_segment_polyline
from compas.geometry import intersection_segment_polyline_xy
from compas.geometry import intersection_segment_segment_xy
from compas.geometry import intersection_sphere_line
from compas.geometry import intersection_sphere_sphere
from compas.geometry import intersection_plane_circle
from compas.geometry import intersection_circle_circle_xy


def test_intersection_line_line_rejects_parallel_and_degenerate_lines():
    assert intersection_line_line(([0, 0, 0], [1, 0, 0]), ([0, 1, 0], [1, 1, 0])) == (None, None)
    assert intersection_line_line(([0, 0, 0], [0, 0, 0]), ([0, 0, 0], [0, 1, 0])) == (None, None)


def test_intersection_line_plane_returns_origin_without_truthiness_ambiguity():
    assert intersection_line_plane(([0, 0, -1], [0, 0, 1]), ([0, 0, 0], [0, 0, 1])) == [0.0, 0.0, 0.0]


def test_intersection_polyline_plane_respects_zero_limit_and_rejects_negative_limit():
    polyline = [[0, 0, -1], [0, 0, 1], [1, 0, -1]]
    plane = [0, 0, 0], [0, 0, 1]

    assert intersection_polyline_plane(polyline, plane, expected_number_of_intersections=0) == []
    with pytest.raises(ValueError, match="cannot be negative"):
        intersection_polyline_plane(polyline, plane, expected_number_of_intersections=-1)


def test_intersection_plane_plane_accepts_nonunit_normals_and_detects_opposite_parallel_normals():
    line = intersection_plane_plane(([0, 0, 0], [0, 0, 2]), ([0, 0, 0], [0, 3, 0]))

    assert line is not None
    assert TOL.is_allclose(line[0], [0, 0, 0])
    assert intersection_plane_plane(([0, 0, 0], [0, 0, 2]), ([0, 0, 1], [0, 0, -3])) is None


def test_intersection_plane_plane_plane_returns_unique_point():
    point = intersection_plane_plane_plane(([1, 0, 0], [1, 0, 0]), ([0, 2, 0], [0, 1, 0]), ([0, 0, 3], [0, 0, 1]))

    assert point is not None
    assert TOL.is_allclose(point, [1, 2, 3])


def test_intersection_sphere_line():
    sphere = (3.0, 7.0, 4.0), 10.0
    line = (1.0, 0, 0.5), (2.0, 1.0, 0.5)
    ipt1, ipt2 = intersection_sphere_line(sphere, line)
    assert TOL.is_allclose(ipt1, (11.634, 10.634, 0.500), atol=1e-3)
    assert TOL.is_allclose(ipt2, (-0.634, -1.634, 0.500), atol=1e-3)


def test_intersection_sphere_line_tangent_and_invalid_inputs():
    assert intersection_sphere_line(([0, 0, 0], 1.0), ([-1, 1, 0], [1, 1, 0])) == (0.0, 1.0, 0.0)

    with pytest.raises(ValueError, match="distinct"):
        intersection_sphere_line(([0, 0, 0], 1.0), ([0, 0, 0], [0, 0, 0]))
    with pytest.raises(ValueError, match="radius"):
        intersection_sphere_line(([0, 0, 0], -1.0), ([-1, 0, 0], [1, 0, 0]))


def test_intersection_sphere_sphere_classifies_intersection_geometry():
    coincident = intersection_sphere_sphere(((0, 0, 0), 1.0), ((0, 0, 0), 1.0))
    tangent = intersection_sphere_sphere(((0, 0, 0), 1.0), ((2, 0, 0), 1.0))
    circle = intersection_sphere_sphere(((0, 0, 0), 2.0), ((2, 0, 0), 2.0))

    assert coincident == ("sphere", ([0, 0, 0], 1.0))
    assert tangent == ("point", [1.0, 0.0, 0.0])
    assert circle is not None and circle[0] == "circle"


def test_intersection_segment_polyline_skips_nonintersecting_segments():
    segment = ([0.0, -1.0, 0.0], [0.0, 1.0, 0.0])
    polyline = [[-2.0, 2.0, 0.0], [-1.0, 2.0, 0.0], [-1.0, 0.0, 0.0], [1.0, 0.0, 0.0]]

    point1, point2 = intersection_segment_polyline(segment, polyline)

    assert point1 == [0.0, 0.0, 0.0]
    assert point2 == [0.0, 0.0, 0.0]


def test_intersection_segment_polyline_returns_consistent_empty_pair():
    result = intersection_segment_polyline(([0, 0, 0], [1, 0, 0]), [[0, 1, 0], [1, 1, 0]])

    assert result == (None, None)


def test_intersection_line_line_xy_accepts_2d_coordinates_and_returns_3d_point():
    point = intersection_line_line_xy(([0, 0], [1, 1]), ([0, 1], [1, 0]))

    assert point == [0.5, 0.5, 0.0]


def test_intersection_line_segment_xy_distinguishes_line_from_segment():
    line = ([0, 0], [1, 0])

    assert intersection_line_segment_xy(line, ([0.5, -1], [0.5, 1])) == [0.5, 0.0, 0.0]
    assert intersection_line_segment_xy(line, ([0.5, 1], [0.5, 2])) is None


def test_intersection_segment_segment_xy_requires_point_on_both_segments():
    assert intersection_segment_segment_xy(([0, 0], [1, 0]), ([0.5, -1], [0.5, 1])) == [0.5, 0.0, 0.0]
    assert intersection_segment_segment_xy(([0, 0], [1, 0]), ([2, -1], [2, 1])) is None


def test_intersection_segment_polyline_xy_skips_nonintersecting_segments():
    segment = ([0, -1], [0, 1])
    polyline = [[-2, 2], [-1, 2], [-1, 0], [1, 0]]

    assert intersection_segment_polyline_xy(segment, polyline) == [0.0, 0.0, 0.0]
    assert intersection_segment_polyline_xy(segment, [[1, 2], [2, 2]]) is None


def test_intersection_line_box_xy_returns_unique_points_consistently():
    box = [[0, 0], [1, 0], [1, 1], [0, 1]]

    assert intersection_line_box_xy(([-1, 0.5], [2, 0.5]), box) == [[1.0, 0.5, 0.0], [0.0, 0.5, 0.0]]
    assert intersection_line_box_xy(([-1, 1], [0, 0]), box) == [[0.0, 0.0, 0.0]]
    assert intersection_line_box_xy(([-1, 2], [2, 2]), box) == []


def test_intersection_polyline_box_xy_deduplicates_corner_hits():
    box = [[0, 0], [1, 0], [1, 1], [0, 1]]
    polyline = [[-1, -1], [0, 0], [2, 2]]

    assert intersection_polyline_box_xy(polyline, box) == [[0.0, 0.0, 0.0], [1.0, 1.0, 0.0]]


@pytest.mark.parametrize("function", [intersection_line_box_xy, intersection_polyline_box_xy])
def test_xy_box_intersections_require_four_corners(function):
    with pytest.raises(ValueError, match="four corners"):
        function(([-1, 0], [2, 0]), [[0, 0], [1, 0], [1, 1]])


def test_intersection_plane_circle():
    plane = (0, 0, 0), (0, 0, 1)
    circle = ((3.0, 7.0, 4.0), (0, 1, 0)), 10.0
    ipt1, ipt2 = intersection_plane_circle(plane, circle)
    assert TOL.is_allclose(ipt1, (-6.165, 7.000, 0.000), atol=1e-3)
    assert TOL.is_allclose(ipt2, (12.165, 7.000, 0.000), atol=1e-3)


def test_intersection_circle_circle_xy():
    circle1 = ((0.0, 0.0, 0.0), (0, 0, 1)), 10.0
    circle2 = ((3.0, 7.0, 0.0), (0, 0, 1)), 10.0
    ipt1, ipt2 = intersection_circle_circle_xy(circle1, circle2)
    assert TOL.is_allclose(ipt1, (9.999, -0.142, 0.000), atol=1e-3)
    assert TOL.is_allclose(ipt2, (-6.999, 7.142, 0.000), atol=1e-3)
