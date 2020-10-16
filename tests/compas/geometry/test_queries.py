from compas.geometry import Line
from compas.geometry import Point
from compas.geometry import is_colinear_line_line


def test_is_colinear_line_line():
    assert is_colinear_line_line(Line(Point(0, 0, 0), Point(1, 1, 1)), Line(Point(3, 3, 3), Point(2, 2, 2))) is True
    assert is_colinear_line_line(Line(Point(0, 0, 0), Point(1, 1, 1)), Line(Point(4, 1, 0), Point(5, 2, 1))) is False
