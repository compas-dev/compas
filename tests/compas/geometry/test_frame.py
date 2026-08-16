import math

import pytest
import json
from random import random
from compas.tolerance import TOL
from compas.geometry import Point
from compas.geometry import Vector
from compas.geometry import Frame
from compas.geometry import Plane
from compas.geometry import Quaternion
from compas.geometry import Rotation
from compas.geometry import Transformation


@pytest.mark.parametrize(
    "point,xaxis,yaxis",
    [
        ([0, 0, 0], [1, 0, 0], [0, 1, 0]),
        ([0, 0, 0], [1, 0, 0], [1, 1, 0]),
        ([0, 0, 0], [1, 0, 0], [0, 1, 1]),
        ([0, 0, 0], [1, 0, 0], [1, 1, 1]),
        ([random(), random(), random()], [random(), random(), random()], [random(), random(), random()]),
    ],
)
def test_frame(point, xaxis, yaxis):
    frame = Frame(point, xaxis, yaxis)
    assert frame.point == Point(*point)
    assert frame.xaxis == Vector(*xaxis).unitized()
    assert TOL.is_close(frame.zaxis.dot(xaxis), 0)
    assert TOL.is_close(frame.zaxis.dot(yaxis), 0)
    assert TOL.is_close(frame.xaxis.length, 1)
    assert TOL.is_close(frame.yaxis.length, 1)
    assert TOL.is_close(frame.zaxis.length, 1)

    other = eval(repr(frame))
    assert TOL.is_allclose(frame.point, other.point)
    assert TOL.is_allclose(frame.xaxis, other.xaxis)
    assert TOL.is_allclose(frame.yaxis, other.yaxis)


def test_frame_rejects_2d_coordinates():
    with pytest.raises(IndexError):
        Frame([0, 0], [1, 0, 0], [0, 1, 0])

    with pytest.raises(IndexError):
        Frame([0, 0, 0], [1, 0], [0, 1, 0])

    with pytest.raises(IndexError):
        Frame([0, 0, 0], [1, 0, 0], [0, 1])


def test_frame_data():
    point = [random(), random(), random()]
    xaxis = [random(), random(), random()]
    yaxis = [random(), random(), random()]
    frame = Frame(point, xaxis, yaxis)
    other = Frame.__from_data__(json.loads(json.dumps(frame.__data__)))

    assert TOL.is_allclose(frame.point, other.point)
    assert TOL.is_allclose(frame.xaxis, other.xaxis)
    assert TOL.is_allclose(frame.yaxis, other.yaxis)
    assert frame.guid != other.guid


def test_frame_predefined():
    frame = Frame.worldXY()
    assert frame.point == Point(0, 0, 0)
    assert frame.xaxis == Vector(1, 0, 0)
    assert frame.yaxis == Vector(0, 1, 0)

    frame = Frame.worldYZ()
    assert frame.point == Point(0, 0, 0)
    assert frame.xaxis == Vector(0, 1, 0)
    assert frame.yaxis == Vector(0, 0, 1)

    frame = Frame.worldZX()
    assert frame.point == Point(0, 0, 0)
    assert frame.xaxis == Vector(0, 0, 1)
    assert frame.yaxis == Vector(1, 0, 0)


def test_frame_sequence_behaviour():
    frame = Frame.worldXY()

    assert len(frame) == 3
    assert list(frame) == [frame.point, frame.xaxis, frame.yaxis]
    assert frame[0] is frame.point
    assert frame[1] is frame.xaxis
    assert frame[2] is frame.yaxis
    assert frame != object()
    assert frame != [frame.point, frame.xaxis]

    frame[0] = [1.0, 2.0, 3.0]
    frame[1] = [0.0, 1.0, 0.0]
    frame[2] = [0.0, 0.0, 1.0]
    assert frame == [[1.0, 2.0, 3.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]

    with pytest.raises(KeyError):
        _ = frame[3]
    with pytest.raises(KeyError):
        frame[3] = [1.0, 0.0, 0.0]


def test_frame_constructors():
    expected = Frame.worldXY()
    point = [0.0, 0.0, 0.0]

    assert Frame.from_points(point, [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]) == expected

    rotation = Rotation.from_axis_and_angle([0.0, 0.0, 1.0], 0.0)
    assert Frame.from_rotation(rotation) == expected

    transformation = Transformation.from_frame(expected)
    assert Frame.from_transformation(transformation) == expected
    assert Frame.from_matrix(transformation.matrix) == expected

    values = [value for row in transformation.matrix for value in row]
    assert Frame.from_list(values) == expected
    values12 = values[:12]
    assert Frame.from_list(values12) == expected
    assert len(values12) == 16

    assert Frame.from_quaternion(Quaternion(1.0, 0.0, 0.0, 0.0), point) == expected
    assert Frame.from_axis_angle_vector([0.0, 0.0, 0.0], point) == expected
    assert Frame.from_euler_angles([0.0, 0.0, 0.0], point=point) == expected
    from_plane = Frame.from_plane(Plane(point, [0.0, 0.0, 1.0]))
    assert from_plane.point == point
    assert from_plane.normal == [0.0, 0.0, 1.0]

    with pytest.raises(ValueError):
        Frame.from_list([0.0] * 11)


def test_frame_conversions_and_transformations():
    frame = Frame([1.0, 2.0, 3.0])
    transformation = frame.to_transformation()

    assert Frame.from_transformation(transformation) == frame
    assert frame.to_local_coordinates([1.0, 2.0, 3.0]) == Point(0.0, 0.0, 0.0)
    assert frame.to_local_coordinates((2.0, 4.0, 6.0)) == Point(1.0, 2.0, 3.0)
    assert frame.to_world_coordinates([0.0, 0.0, 0.0]) == Point(1.0, 2.0, 3.0)
    assert frame.to_world_coordinates((1.0, 2.0, 3.0)) == Point(2.0, 4.0, 6.0)

    point = Point(2.0, 4.0, 6.0)
    local = frame.to_local_coordinates(point)
    assert isinstance(local, Point)
    assert frame.to_world_coordinates(local) == point

    transformed = Frame.worldXY()
    transformed.transform(transformation.matrix)
    assert transformed == frame


def test_frame_interpolate_frames_and_euler_angles():
    frame1 = Frame.worldXY()
    frame2 = Frame([1.0, 1.0, 1.0], [0.0, 1.0, 0.0], [-1.0, 0.0, 0.0])

    frames = frame1.interpolate_frames(frame2, 3)
    assert len(frames) == 3
    assert frames[0] == frame1
    assert frames[-1] == frame2
    assert TOL.is_allclose(Frame.from_euler_angles(frame2.euler_angles()).xaxis, frame2.xaxis)


def test_interpolate_frame_start_end():
    frame1 = Frame(Point(0, 0, 0), Vector(1, 0, 0), Vector(0, 1, 0))
    frame2 = Frame(Point(1, 1, 1), Vector(0, 0, 1), Vector(0, 1, 0))

    # Test interpolation at the start
    start_frame = frame1.interpolate_frame(frame2, 0)
    assert start_frame.point == frame1.point and start_frame.xaxis == frame1.xaxis and start_frame.yaxis == frame1.yaxis, "Failed at t=0"

    # Test interpolation at the end
    end_frame = frame1.interpolate_frame(frame2, 1)
    assert end_frame.point == frame2.point and end_frame.xaxis == frame2.xaxis and end_frame.yaxis == frame2.yaxis, "Failed at t=1"

    quarter_frame = frame1.interpolate_frame(frame2, 0.25)
    assert TOL.is_allclose([math.degrees(quarter_frame.axis_angle_vector.y)], [-22.5], atol=TOL.angular)

    half_frame = frame1.interpolate_frame(frame2, 0.5)
    assert TOL.is_allclose([math.degrees(half_frame.axis_angle_vector.y)], [-45.0], atol=TOL.angular)

    three_quarter_frame = frame1.interpolate_frame(frame2, 0.75)
    assert TOL.is_allclose([math.degrees(three_quarter_frame.axis_angle_vector.y)], [-67.5], atol=TOL.angular)


def test_frame_invert():
    frame = Frame([0, 0, 0])

    assert TOL.is_close(frame.xaxis.dot([1, 0, 0]), 1.0)
    assert TOL.is_close(frame.yaxis.dot([0, 1, 0]), 1.0)
    assert TOL.is_close(frame.zaxis.dot([0, 0, 1]), 1.0)

    frame.invert()

    assert TOL.is_close(frame.xaxis.dot([1, 0, 0]), 1.0)
    assert TOL.is_close(frame.yaxis.dot([0, -1, 0]), 1.0)
    assert TOL.is_close(frame.zaxis.dot([0, 0, -1]), 1.0)


def test_frame_inverted():
    frame = Frame([0, 0, 0])

    assert TOL.is_close(frame.xaxis.dot([1, 0, 0]), 1.0)
    assert TOL.is_close(frame.yaxis.dot([0, 1, 0]), 1.0)
    assert TOL.is_close(frame.zaxis.dot([0, 0, 1]), 1.0)

    other = frame.inverted()

    assert TOL.is_close(frame.xaxis.dot([1, 0, 0]), 1.0)
    assert TOL.is_close(frame.yaxis.dot([0, 1, 0]), 1.0)
    assert TOL.is_close(frame.zaxis.dot([0, 0, 1]), 1.0)

    assert TOL.is_close(other.xaxis.dot([1, 0, 0]), 1.0)
    assert TOL.is_close(other.yaxis.dot([0, -1, 0]), 1.0)
    assert TOL.is_close(other.zaxis.dot([0, 0, -1]), 1.0)


def test_frame_comparison_relative():
    a = Frame(Point(random(), random(), random()))

    b = a.copy()
    b.point.x += 0.1 * TOL.relative * b.point.x
    assert a == b

    c = a.copy()
    c.point.x += TOL.relative * c.point.x
    assert a == c

    d = a.copy()
    d.point.x += 10.0 * TOL.relative * d.point.x
    assert a != d


def test_frame_comparison_absolute():
    a = Frame(Point(0, 0, 0))

    b = a.copy()
    b.point.x += 0.1 * TOL.absolute
    assert a == b

    c = a.copy()
    c.point.x += TOL.absolute
    assert a == c

    d = a.copy()
    d.point.x += 10.0 * TOL.absolute
    assert a != d
