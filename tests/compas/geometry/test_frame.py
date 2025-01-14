from __future__ import division

import math

import pytest
import json
import compas
from random import random
from compas.tolerance import TOL
from compas.geometry import Point
from compas.geometry import Vector
from compas.geometry import Frame


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

    if not compas.IPY:
        assert Frame.validate_data(frame.__data__)
        assert Frame.validate_data(other.__data__)


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
