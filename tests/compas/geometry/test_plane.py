import pytest
import json
import compas
from random import random
from compas.tolerance import TOL
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
    assert TOL.is_close(plane.normal.length, 1.0)

    other = eval(repr(plane))
    assert TOL.is_allclose(other.point, plane.point)
    assert TOL.is_allclose(other.normal, plane.normal)


def test_plane_data():
    point = Point(random(), random(), random())
    vector = Vector(random(), random(), random())
    plane = Plane(point, vector)
    other = Plane.__from_data__(json.loads(json.dumps(plane.__data__)))

    assert TOL.is_allclose(other.point, plane.point)
    assert TOL.is_allclose(other.normal, plane.normal)
    assert plane.guid != other.guid

    if not compas.IPY:
        assert Plane.validate_data(plane.__data__)
        assert Plane.validate_data(other.__data__)


def test_plane_predefined():
    plane = Plane.worldXY()
    assert plane.point == Point(0, 0, 0)
    assert plane.normal == Vector(0, 0, 1)

    plane = Plane.worldYZ()
    assert plane.point == Point(0, 0, 0)
    assert plane.normal == Vector(1, 0, 0)

    plane = Plane.worldZX()
    assert plane.point == Point(0, 0, 0)
    assert plane.normal == Vector(0, 1, 0)


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
    
def test_plane_is_parallel():
    plane1 = Plane.worldXY()
    plane2 = Plane([1.0, 1.0, 1.0], [0.0, 0.0, 1.0])
    assert plane1.is_parallel(plane2)
    
    plane1 = Plane.worldXY()
    plane2 = Plane([1.0, 1.0, 1.0], [0.0, 0.0, -1.0])
    assert plane1.is_parallel(plane2)
    
