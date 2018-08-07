from compas.geometry import Point


def test_point():
    p = Point(1, 0, 0)
    assert p.x == 1.0 and p.y == 0.0 and p.z == 0.0
    assert p[0] == 1.0 and p[1] == 0.0 and p[2] == 0.0
    assert p == [1.0, 0.0, 0.0]
    assert repr(p) == 'Point(1.000, 0.000, 0.000)'


def test_point_operators():
    pass


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
