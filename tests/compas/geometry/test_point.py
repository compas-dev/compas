import pytest
import json
import compas
from random import random
from compas.geometry import Circle
from compas.geometry import Line
from compas.geometry import Plane
from compas.geometry import Point
from compas.geometry import Polygon
from compas.geometry import Polyhedron
from compas.geometry import Polyline
from compas.geometry import Translation
from compas.tolerance import TOL


@pytest.mark.parametrize(
    "x,y,z",
    [
        (1, 2, 3),
        (1.0, 2.0, 3.0),
        ("1.0", "2", 3.0),
        (random(), random(), random()),
    ],
)
def test_point(x, y, z):
    p = Point(x, y, z)
    x, y, z = float(x), float(y), float(z)
    assert p.x == x and p.y == y and p.z == z
    assert p[0] == x and p[1] == y and p[2] == z

    if not compas.IPY:
        assert eval(repr(p)) == p


@pytest.mark.parametrize(
    "x,y",
    [
        (1, 2),
        (1.0, 2.0),
        ("1.0", "2"),
        (random(), random()),
    ],
)
def test_point2(x, y):
    p = Point(x, y)
    x, y, z = float(x), float(y), 0.0
    assert p.x == x and p.y == y and p.z == z
    assert p[0] == x and p[1] == y and p[2] == z

    if not compas.IPY:
        assert eval(repr(p)) == p


def test_point_operators():
    a = Point(random(), random(), random())
    b = Point(random(), random(), random())
    assert a + b == [a.x + b.x, a.y + b.y, a.z + b.z]
    assert a - b == [a.x - b.x, a.y - b.y, a.z - b.z]
    assert a * 2 == [a.x * 2, a.y * 2, a.z * 2]
    assert a / 2 == [a.x / 2, a.y / 2, a.z / 2]
    assert a**3 == [a.x**3, a.y**3, a.z**3]


def test_point_equality():
    p1 = Point(1, 1, 1)
    p2 = Point(1, 1, 1)
    p3 = Point(0, 0, 0)
    assert p1 == p2
    assert not (p1 != p2)
    assert p1 != p3
    assert not (p1 == p3)
    assert p1 != [1, 1]
    assert p1 != [1, 1, 1, 1]
    assert p1 != object()
    assert p1 is not None


def test_geometry_copying_transform_helpers_preserve_subclass_and_original():
    point = Point(1.0, 0.0, 0.0)

    transformed = point.transformed(Translation.from_vector([1.0, 2.0, 3.0]))
    translated = point.translated([1.0, 2.0, 3.0])
    scaled = point.scaled(2.0, 3.0, 4.0)
    rotated = point.rotated(0.5 * 3.141592653589793, axis=[0.0, 0.0, 1.0])

    assert isinstance(transformed, Point)
    assert isinstance(translated, Point)
    assert isinstance(scaled, Point)
    assert isinstance(rotated, Point)
    assert point == Point(1.0, 0.0, 0.0)
    assert transformed == Point(2.0, 2.0, 3.0)
    assert translated == Point(2.0, 2.0, 3.0)
    assert scaled == Point(2.0, 0.0, 0.0)
    assert TOL.is_allclose(rotated, [0.0, 1.0, 0.0])


def test_point_comparison_relative():
    a = Point(random(), random(), random())
    b = Point(a.x + a.x * TOL.relative * 0.1, a.y + a.y * TOL.relative * 0.1, a.z + a.z * TOL.relative * 0.1)
    c = Point(a.x + a.x * TOL.relative, a.y + a.y * TOL.relative, a.z + a.z * TOL.relative)
    d = Point(a.x + a.x * TOL.relative * 10.0, a.y + a.y * TOL.relative * 10.0, a.z + a.z * TOL.relative * 10.0)
    assert a == b
    assert a == c
    assert a != d


def test_point_comparison_absolute():
    a = Point(0, 0, 0)
    b = Point(a.x + TOL.absolute * 0.1, a.y + TOL.absolute * 0.1, a.z + TOL.absolute * 0.1)
    c = Point(a.x + TOL.absolute, a.y + TOL.absolute, a.z + TOL.absolute)
    d = Point(a.x + TOL.absolute * 10.0, a.y + TOL.absolute * 10.0, a.z + TOL.absolute * 10.0)
    assert a == b
    assert a == c
    assert a != d


def test_point_inplace_operators():
    point = Point(2.0, 4.0, 6.0)
    identity = id(point)

    point += [1.0, 2.0, 3.0]
    point -= [1.0, 1.0, 1.0]
    point *= 2.0
    point /= 4.0
    point **= 2.0

    assert id(point) == identity
    assert point == [1.0, 6.25, 16.0]


def test_point_sequence_behaviour():
    point = Point(1.0, 2.0, 3.0)

    assert len(point) == 3
    assert list(point) == [1.0, 2.0, 3.0]
    assert point[:] == [1.0, 2.0, 3.0]
    assert point[-3] == 1.0
    assert point[-1] == 3.0

    point[0] = 4.0
    point[-2] = 5.0
    point[-1] = 6.0
    assert point == [4.0, 5.0, 6.0]

    with pytest.raises(IndexError):
        _ = point[3]
    with pytest.raises(IndexError):
        _ = point[-4]
    with pytest.raises(IndexError):
        point[3] = 7.0
    with pytest.raises(IndexError):
        point[-4] = 7.0


def test_point_data():
    point = Point(random(), random(), random())
    other = Point.__from_data__(json.loads(json.dumps(point.__data__)))

    assert point == other
    assert point.__data__ == other.__data__
    assert point.guid != other.guid


def test_point_distance_to_point():
    assert Point(1.0, 2.0, 3.0).distance_to_point([4.0, 6.0, 3.0]) == 5.0


def test_point_distance_to_line():
    line = Line([0.0, 0.0, 0.0], [0.0, 1.0, 0.0])
    assert Point(2.0, 0.0, 0.0).distance_to_line(line) == 2.0


def test_point_distance_to_plane():
    plane = Plane([0.0, 0.0, 2.0], [0.0, 0.0, 1.0])
    assert Point(0.0, 0.0, -1.0).distance_to_plane(plane) == 3.0


def test_point_on_line():
    line = Line([0.0, 0.0, 0.0], [1.0, 0.0, 0.0])
    assert Point(2.0, 0.0, 0.0).on_line(line)
    assert not Point(2.0, 1.0, 0.0).on_line(line)


def test_point_on_segment():
    segment = Line([0.0, 0.0, 0.0], [1.0, 0.0, 0.0])
    assert Point(0.5, 0.0, 0.0).on_segment(segment)
    assert not Point(2.0, 0.0, 0.0).on_segment(segment)


def test_point_on_polyline():
    polyline = Polyline([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0]])
    assert Point(1.0, 0.5, 0.0).on_polyline(polyline)
    assert not Point(0.5, 0.5, 0.0).on_polyline(polyline)


def test_point_on_circle():
    circle = Circle(1.0)
    assert Point(1.0, 0.0, 0.0).on_circle(circle)
    assert not Point(0.0, 0.0, 0.0).on_circle(circle)
    assert not Point(1.0, 0.0, 1.0).on_circle(circle)


def test_point_in_triangle():
    triangle = Polygon([[0.0, 0.0, 0.0], [2.0, 0.0, 0.0], [0.0, 2.0, 0.0]])
    assert Point(0.5, 0.5, 0.0).in_triangle(triangle)
    assert not Point(2.0, 2.0, 0.0).in_triangle(triangle)


def test_point_in_polygon():
    polygon = Polygon([[0.0, 0.0, 0.0], [2.0, 0.0, 0.0], [2.0, 2.0, 0.0], [0.0, 2.0, 0.0]])
    assert Point(1.0, 1.0, 0.0).in_polygon(polygon)
    assert Point(1.0, 1.0, 0.0).in_convex_polygon(polygon)
    assert not Point(3.0, 1.0, 0.0).in_polygon(polygon)


def test_point_in_circle():
    circle = Circle(2.0)
    assert Point(1.0, 0.0, 0.0).in_circle(circle)
    assert not Point(3.0, 0.0, 0.0).in_circle(circle)


def test_point_in_polyhedron():
    tetrahedron = Polyhedron.from_platonicsolid(4)
    tetrahedron.faces = [list(reversed(face)) for face in tetrahedron.faces]
    assert Point(0.0, 0.0, 0.0).in_polyhedron(tetrahedron)
    assert not Point(10.0, 10.0, 10.0).in_polyhedron(tetrahedron)
