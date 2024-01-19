import pytest
import json
import compas
from random import random

from compas.geometry import Point  # noqa: F401
from compas.geometry import Vector  # noqa: F401
from compas.geometry import Frame
from compas.geometry import PlanarSurface
from compas.geometry import close
from compas.utilities import linspace


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

    assert close(plane.xsize, other.xsize, tol=1e-12)
    assert close(plane.ysize, other.ysize, tol=1e-12)
    assert plane.frame == other.frame


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

    assert close(plane.xsize, other.xsize, tol=1e-12)
    assert close(plane.ysize, other.ysize, tol=1e-12)
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
