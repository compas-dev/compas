import compas
from compas.geometry import Point


if not compas.IPY:

    def test_data():
        p = Point(0, 0, "0")
        assert p.data == p.validate_data()
        o = Point.from_data(p.data)
        assert p == o
        assert not (p is o)
        assert o.data == o.validate_data()


def test_point():
    p = Point(1, 0, "0")
    assert p.x == 1.0 and p.y == 0.0 and p.z == 0.0
    assert p[0] == 1.0 and p[1] == 0.0 and p[2] == 0.0
    assert p == [1.0, 0.0, 0.0]
    assert repr(p) == "Point(1.000, 0.000, 0.000)"


def test_point_operators():
    pass


def test_point_equality():
    p1 = Point(1, 1, 1)
    p2 = Point(1, 1, 1)
    p3 = Point(0, 0, 0)
    assert p1 == p2
    assert not (p1 != p2)
    assert p1 != p3
    assert not (p1 == p3)


def test_point_inplace_operators():
    pass


def test_point_distance_to_point():
    pass


def test_point_distance_to_line():
    pass


def test_point_distance_to_plane():
    pass


def test_point_on_line():
    pass


def test_point_on_segment():
    pass


def test_point_on_polyline():
    pass


def test_point_on_circle():
    pass


def test_point_in_triangle():
    pass


def test_point_in_polygon():
    pass


def test_point_in_circle():
    pass


def test_point_in_polyhedron():
    pass
