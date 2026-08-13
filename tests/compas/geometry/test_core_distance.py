import pytest

from compas.geometry import Line
from compas.geometry import Point
from compas.geometry import closest_point_in_cloud
from compas.geometry import closest_point_on_plane
from compas.geometry import closest_point_on_segment
from compas.geometry import closest_point_on_segment_xy
from compas.geometry import distance_line_line
from compas.geometry import distance_point_line
from compas.geometry import distance_point_line_sqrd
from compas.geometry import distance_point_line_sqrd_xy
from compas.geometry import distance_point_line_xy
from compas.geometry import distance_point_plane
from compas.geometry import distance_point_plane_signed
from compas.geometry import distance_point_point
from compas.geometry import distance_point_point_sqrd
from compas.geometry import distance_point_point_sqrd_xy
from compas.geometry import distance_point_point_xy
from compas.geometry import sort_points
from compas.tolerance import TOL


@pytest.mark.parametrize("point,point_on_line", [[[0, 0, -10], [1, 1, 0]], [[5, 4, 80], [4.5, 4.5, 0]]])
def test_closest_point_segment_xy(point, point_on_line):
    line = Line([1, 1, -15], [10, 10, 20])
    ponl = closest_point_on_segment_xy(Point(*point), line)
    assert ponl == Point(*point_on_line)


def test_point_point_distances_accept_raw_sequences_and_are_symmetric():
    a = (1.0, 2.0, 3.0)
    b = [4.0, 6.0, 3.0]

    assert distance_point_point(a, b) == distance_point_point(b, a) == 5.0
    assert distance_point_point_sqrd(a, b) == distance_point_point_sqrd(b, a) == 25.0


def test_xy_point_distances_ignore_z_coordinates():
    a = (1.0, 2.0, -100.0)
    b = (4.0, 6.0, 100.0)

    assert distance_point_point_xy(a, b) == 5.0
    assert distance_point_point_sqrd_xy(a, b) == 25.0


@pytest.mark.parametrize(
    ("distance", "expected"),
    [
        (distance_point_line, 73.0**0.5),
        (distance_point_line_sqrd, 73.0),
        (distance_point_line_xy, 3.0),
        (distance_point_line_sqrd_xy, 9.0),
    ],
)
def test_point_line_distances(distance, expected):
    assert distance((2.0, 3.0, 8.0), ((0.0, 0.0, 0.0), (4.0, 0.0, 0.0))) == expected


@pytest.mark.parametrize(
    "distance",
    [distance_point_line, distance_point_line_sqrd, distance_point_line_xy, distance_point_line_sqrd_xy],
)
def test_point_line_distances_preserve_degenerate_line_error(distance):
    with pytest.raises(ZeroDivisionError):
        distance((1.0, 2.0, 3.0), ((0.0, 0.0, 0.0), (0.0, 0.0, 0.0)))


def test_signed_and_unsigned_point_plane_distances():
    plane = ((0.0, 0.0, 1.0), (0.0, 0.0, 1.0))

    assert distance_point_plane_signed((0.0, 0.0, 4.0), plane) == 3.0
    assert distance_point_plane_signed((0.0, 0.0, -2.0), plane) == -3.0
    assert distance_point_plane((0.0, 0.0, -2.0), plane) == 3.0


def test_line_line_distance_handles_skew_and_parallel_lines():
    x_axis = ((0.0, 0.0, 0.0), (1.0, 0.0, 0.0))
    skew = ((0.0, 1.0, 2.0), (0.0, 2.0, 2.0))
    parallel = ((0.0, 3.0, 0.0), (1.0, 3.0, 0.0))

    assert TOL.is_close(distance_line_line(x_axis, skew), 2.0)
    assert TOL.is_close(distance_line_line(x_axis, parallel), 3.0)


def test_sort_points_preserves_cloud_order_for_equal_distances():
    cloud = ((-1.0, 0.0, 0.0), (1.0, 0.0, 0.0))

    assert [item[2] for item in sort_points((0.0, 0.0, 0.0), cloud)] == [0, 1]


def test_closest_point_in_empty_cloud_preserves_index_error():
    with pytest.raises(IndexError):
        closest_point_in_cloud((0.0, 0.0, 0.0), ())


def test_closest_point_on_segment_preserves_endpoint_container():
    segment = ((0.0, 0.0, 0.0), (1.0, 0.0, 0.0))

    assert closest_point_on_segment((-1.0, 1.0, 0.0), segment) is segment[0]


def test_closest_point_on_plane_normalizes_the_plane_normal():
    result = closest_point_on_plane((1.0, 2.0, 5.0), ((0.0, 0.0, 1.0), (0.0, 0.0, 4.0)))

    assert TOL.is_allclose(result, (1.0, 2.0, 1.0))
