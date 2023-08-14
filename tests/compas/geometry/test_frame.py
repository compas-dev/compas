from __future__ import division
import pytest
import json
import compas
from random import random
from compas.geometry import allclose
from compas.geometry import close
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
    assert close(frame.zaxis.dot(xaxis), 0, tol=1e-12)
    assert close(frame.zaxis.dot(yaxis), 0, tol=1e-12)
    assert close(frame.xaxis.length, 1, tol=1e-12)
    assert close(frame.yaxis.length, 1, tol=1e-12)
    assert close(frame.zaxis.length, 1, tol=1e-12)

    other = eval(repr(frame))
    assert allclose(frame.point, other.point, tol=1e-12)
    assert allclose(frame.xaxis, other.xaxis, tol=1e-12)
    assert allclose(frame.yaxis, other.yaxis, tol=1e-12)


def test_frame_data():
    point = [random(), random(), random()]
    xaxis = [random(), random(), random()]
    yaxis = [random(), random(), random()]
    frame = Frame(point, xaxis, yaxis)
    other = Frame.from_data(json.loads(json.dumps(frame.data)))

    assert allclose(frame.point, other.point, tol=1e-12)
    assert allclose(frame.xaxis, other.xaxis, tol=1e-12)
    assert allclose(frame.yaxis, other.yaxis, tol=1e-12)
    assert frame.guid != other.guid

    if not compas.IPY:
        assert Frame.validate_data(frame.data)
        assert Frame.validate_data(other.data)


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
