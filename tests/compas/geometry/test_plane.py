import json
from random import random

import pytest

from compas.geometry import Frame
from compas.geometry import Plane
from compas.geometry import Point
from compas.geometry import Translation
from compas.geometry import Vector
from compas.tolerance import TOL


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


def test_plane_rejects_2d_coordinates():
    with pytest.raises(IndexError):
        Plane([0, 0], [0, 0, 1])

    with pytest.raises(IndexError):
        Plane([0, 0, 0], [0, 1])


def test_plane_data():
    point = Point(random(), random(), random())
    vector = Vector(random(), random(), random())
    plane = Plane(point, vector)
    other = Plane.__from_data__(json.loads(json.dumps(plane.__data__)))

    assert TOL.is_allclose(other.point, plane.point)
    assert TOL.is_allclose(other.normal, plane.normal)
    assert plane.guid != other.guid


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


def test_plane_sequence_behavior():
    plane = Plane.worldXY()

    assert len(plane) == 2
    assert list(plane) == [plane.point, plane.normal]
    assert plane[0] is plane.point
    assert plane[1] is plane.normal

    plane[0] = [1, 2, 3]
    plane[1] = [0, 2, 0]

    assert plane.point == [1, 2, 3]
    assert plane.normal == [0, 1, 0]
    assert plane == [[1, 2, 3], [0, 1, 0]]

    with pytest.raises(KeyError):
        _ = plane[2]

    with pytest.raises(KeyError):
        plane[2] = [0, 0, 1]


def test_plane_equation_coefficients():
    plane = Plane([0, 0, 2], [0, 0, 1])

    assert plane.d == -2
    assert plane.abcd == (0, 0, 1, -2)


def test_plane_from_abcd():
    plane = Plane.from_abcd([0, 0, 2, -4])

    assert plane.point == [0, 0, 2]
    assert plane.normal == [0, 0, 1]
    assert TOL.is_zero(sum(coefficient * coordinate for coefficient, coordinate in zip(plane.abcd[:3], plane.point)) + plane.abcd[3])


def test_plane_additional_constructors():
    frame = Frame([1, 2, 3], [1, 0, 0], [0, 1, 0])
    from_frame = Plane.from_frame(frame)
    from_points = Plane.from_points([[0, 0, 0], [1, 0, 0], [0, 1, 0], [1, 1, 0]])

    assert from_frame.point == frame.point
    assert from_frame.normal == frame.normal
    assert from_points.contains_point([0, 0, 0])
    assert from_points.normal == [0, 0, 1]


def test_plane_transform():
    plane = Plane.worldXY()
    plane.transform(Translation.from_vector([1, 2, 3]))

    assert plane.point == [1, 2, 3]
    assert plane.normal == [0, 0, 1]


def test_plane_point_relationships():
    plane = Plane.worldXY()

    assert plane.contains_point([1, 2, 0])
    assert not plane.contains_point([1, 2, 1])
    assert plane.distance_to_point([1, 2, 3]) == 3
    assert plane.closest_point([1, 2, 3]) == [1, 2, 0]
    assert plane.projected_point([1, 2, 3]) == [1, 2, 0]
    assert plane.projected_point([1, 2, 3], [0, 0, -1]) == [1, 2, 0]
    assert plane.projected_point([1, 2, 3], [1, 0, 0]) is None
    assert plane.mirrored_point([1, 2, 3]) == [1, 2, -3]


def test_plane_relationships():
    plane = Plane.worldXY()

    assert plane.is_parallel(Plane([0, 0, 1], [0, 0, -1]))
    assert plane.is_perpendicular(Plane.worldYZ())
    assert not plane.is_perpendicular(Plane.worldXY())


def test_plane_offset_preserves_subclass():
    class CustomPlane(Plane):
        pass

    plane = CustomPlane.worldXY()
    offset = plane.offset(2)

    assert isinstance(offset, CustomPlane)
    assert offset.point == [0, 0, 2]
    assert offset.normal == plane.normal
