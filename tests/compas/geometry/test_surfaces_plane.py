import pytest
import json
import compas
from random import random

from compas.geometry import Point  # noqa: F401
from compas.geometry import Vector  # noqa: F401
from compas.geometry import Frame
from compas.geometry import PlanarSurface
from compas.tolerance import TOL
from compas.itertools import linspace


@pytest.mark.parametrize(
    "xsize,ysize",
    [
        (0, 0),
        (1, 0),
        (0, 1),
        (1, 1),
        (random(), random()),
    ],
)
def test_plane(xsize, ysize):
    plane = PlanarSurface(xsize=xsize, ysize=ysize)

    assert plane.xsize == xsize
    assert plane.ysize == ysize
    assert plane.frame == Frame.worldXY()

    for u in linspace(0.0, 1.0, num=100):
        for v in linspace(0.0, 1.0, num=100):
            assert plane.point_at(u, v) == plane.point_at(u, v, world=False)

    other = eval(repr(plane))

    assert TOL.is_close(plane.xsize, other.xsize)
    assert TOL.is_close(plane.ysize, other.ysize)
    assert plane.frame == other.frame


@pytest.mark.parametrize(
    "xsize,ysize",
    [
        (0, 0),
        (1, 0),
        (0, 1),
        (1, 1),
        (10, 1),
        (1, 10),
        (2, 3),
        (3, 2),
        (random(), random()),
    ],
)
def test_plane_size(xsize, ysize):
    plane = PlanarSurface(xsize=xsize, ysize=ysize)

    assert plane.point_at(1, 0) == Point(xsize, 0, 0)
    assert plane.point_at(0, 1) == Point(0, ysize, 0)
    assert plane.point_at(1, 1) == Point(xsize, ysize, 0)

    assert plane.point_at(0.5, 0) == Point(0.5 * xsize, 0, 0)
    assert plane.point_at(0, 0.5) == Point(0, 0.5 * ysize, 0)
    assert plane.point_at(0.5, 0.5) == Point(0.5 * xsize, 0.5 * ysize, 0)


@pytest.mark.parametrize(
    "frame",
    [
        Frame.worldXY(),
        Frame.worldZX(),
        Frame.worldYZ(),
    ],
)
def test_plane_frame(frame):
    xsize = random()
    ysize = random()
    plane = PlanarSurface(xsize=xsize, ysize=ysize, frame=frame)

    assert plane.xsize == xsize
    assert plane.ysize == ysize
    assert plane.frame == frame

    for u in linspace(0.0, 1.0, num=100):
        for v in linspace(0.0, 1.0, num=100):
            assert plane.point_at(u, v) == plane.point_at(u, v, world=False).transformed(plane.transformation)

    other = eval(repr(plane))

    assert TOL.is_close(plane.xsize, other.xsize)
    assert TOL.is_close(plane.ysize, other.ysize)
    assert plane.frame == other.frame


# =============================================================================
# Data
# =============================================================================


def test_plane_data():
    xsize = random()
    ysize = random()
    plane = PlanarSurface(xsize=xsize, ysize=ysize)
    other = PlanarSurface.__from_data__(json.loads(json.dumps(plane.__data__)))

    assert plane.__data__ == other.__data__
    assert plane.xsize == xsize
    assert plane.ysize == ysize
    assert plane.frame == Frame.worldXY()

    if not compas.IPY:
        assert PlanarSurface.validate_data(plane.__data__)
        assert PlanarSurface.validate_data(other.__data__)


# =============================================================================
# Constructors
# =============================================================================

# =============================================================================
# Properties and Geometry
# =============================================================================

# =============================================================================
# Accessors
# =============================================================================

# =============================================================================
# Comparison
# =============================================================================

# =============================================================================
# Other Methods
# =============================================================================

# =============================================================================
# Conversions
# =============================================================================


@pytest.mark.parametrize(
    "xsize,ysize",
    [
        (0, 0),
        (1, 0),
        (0, 1),
        (1, 1),
        (10, 1),
        (1, 10),
        (2, 3),
        (3, 2),
        (random(), random()),
    ],
)
def test_plane_conversion_to_mesh(xsize, ysize):
    plane = PlanarSurface(xsize=xsize, ysize=ysize)

    area = plane.xsize * plane.ysize

    mesh = plane.to_mesh(1, 1)
    assert mesh.number_of_vertices() == 4
    assert mesh.number_of_faces() == 1
    assert TOL.is_close(mesh.area(), area)

    mesh = plane.to_mesh(10, 10)
    assert mesh.number_of_vertices() == 121
    assert mesh.number_of_faces() == 100
    assert TOL.is_close(mesh.area(), area)
