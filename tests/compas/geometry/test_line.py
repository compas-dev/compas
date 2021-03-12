from compas.geometry import Line
from compas.geometry import Point  # noqa: F401


def test_line():
    p1 = [0, 0, 0]
    p2 = [1, 0, 0]
    line = Line(p1, p2)
    assert line.start == p1
    assert line.end == p2
    assert (p1, p2) == line
    assert line == Line(p1, p2)
    assert line != (p2, p1)
    assert line != 1
    assert line == eval(repr(line))
