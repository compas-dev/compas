import pytest

from compas.geometry import Point
from compas.geometry import Line
from compas.geometry import closest_point_on_segment_xy


@pytest.mark.parametrize("point,point_on_line", [[[0, 0, -10], [1, 1, 0]], [[5, 4, 80], [4.5, 4.5, 0]]])
def test_closest_point_segment_xy(point, point_on_line):
    line = Line([1, 1, -15], [10, 10, 20])
    ponl = closest_point_on_segment_xy(Point(*point), line)
    assert ponl == Point(*point_on_line)
