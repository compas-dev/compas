import pytest
import json
import compas
from random import random
from compas.geometry import close
from compas.geometry import allclose
from compas.geometry import Point
from compas.geometry import Vector
from compas.geometry import Plane


@pytest.mark.parametrize(
    "point,vector",
    [
        ([1, 2, 3], [0, 0, 1]),
        (Point(1.0, 2.0, 3.0), [0.0, 0.0, 1.0]),
        (Point(1.0, 2.0, 3.0), Vector(0.0, 0.0, 1.0)),
        ([1.0, 2.0, 3.0], Vector(0.0, 0.0, 1.0)),
        ([random(), random(), random()], [random(), random(), random()]),
    ],
)
def test_plane(point, vector):
    plane = Plane(point, vector)
    assert plane.point == Point(*point)
    assert plane.normal == Vector(*vector).unitized()
    assert isinstance(plane.point, Point)
    assert isinstance(plane.normal, Vector)
    assert close(plane.normal.length, 1.0, tol=1e-12)

    if not compas.IPY:
        other = eval(repr(plane))
        assert allclose(other.point, plane.point, tol=1e-12)
        assert allclose(other.normal, plane.normal, tol=1e-12)


def test_plane_data():
    point = Point(random(), random(), random())
    vector = Vector(random(), random(), random())
    plane = Plane(point, vector)
    other = Plane.from_data(json.loads(json.dumps(plane.data)))

    assert plane == other
    assert plane.data == other.data
    assert plane.guid != other.guid

    if not compas.IPY:
        assert Plane.validate_data(plane.data)
        assert Plane.validate_data(other.data)


def test_plane_from_point_and_two_vectors():
    pt = [1, 2, 3]
    vec1 = [1, 0, 0]
    vec2 = [0, 1, 0]

    result = Plane.from_point_and_two_vectors(pt, vec1, vec2)
    assert result == [[1, 2, 3], [0, 0, 1]]


def test_plane_from_three_points():
    pt1 = [0, 0, 0]
    pt2 = [1, 0, 0]
    pt3 = [0, 1, 0]

    result = Plane.from_three_points(pt1, pt2, pt3)
    assert result == ([0, 0, 0], [0, 0, 1])
