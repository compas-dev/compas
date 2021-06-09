from compas.geometry import Point
from compas.geometry import Line
from compas.geometry import closest_point_on_segment_xy


def test_closest_point_segment_xy():
    point = Point(0, 0, -10)
    line = Line([1, 1, -15], [10, 10, 20])
    ponl = closest_point_on_segment_xy(point, line)
    assert ponl == Point(1, 1, 0)
