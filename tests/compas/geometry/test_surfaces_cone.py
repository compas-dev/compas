import pytest
import json
import compas
from random import random

from compas.geometry import Point  # noqa: F401
from compas.geometry import Vector  # noqa: F401
from compas.geometry import Frame
from compas.geometry import ConicalSurface
from compas.tolerance import TOL
from compas.itertools import linspace


@pytest.mark.parametrize(
    "radius,height",
    [
        (0, 0),
        (1, 0),
        (0, 1),
        (1, 1),
        (random(), random()),
    ],
)
def test_cone(radius, height):
    cone = ConicalSurface(radius=radius, height=height)

    assert cone.radius == radius
    assert cone.height == height
    assert cone.frame == Frame.worldXY()

    for u in linspace(0.0, 1.0, num=100):
        for v in linspace(0.0, 1.0, num=100):
            assert cone.point_at(u, v) == cone.point_at(u, v, world=False)

    other = eval(repr(cone))

    assert TOL.is_close(cone.radius, other.radius, tol=1e-12)
    assert TOL.is_close(cone.height, other.height, tol=1e-12)
    assert cone.frame == other.frame


@pytest.mark.parametrize(
    "frame",
    [
        Frame.worldXY(),
        Frame.worldZX(),
        Frame.worldYZ(),
    ],
)
def test_cone_frame(frame):
    radius = random()
    height = random()
    cone = ConicalSurface(radius=radius, height=height, frame=frame)

    assert cone.radius == radius
    assert cone.height == height
    assert cone.frame == frame

    for u in linspace(0.0, 1.0, num=100):
        for v in linspace(0.0, 1.0, num=100):
            assert cone.point_at(u, v) == cone.point_at(u, v, world=False).transformed(cone.transformation)

    other = eval(repr(cone))

    assert TOL.is_close(cone.radius, other.radius, tol=1e-12)
    assert TOL.is_close(cone.height, other.height, tol=1e-12)
    assert cone.frame == other.frame


# =============================================================================
# Data
# =============================================================================


def test_cone_data():
    radius = random()
    height = random()
    cone = ConicalSurface(radius=radius, height=height)
    other = ConicalSurface.__from_data__(json.loads(json.dumps(cone.__data__)))

    assert cone.__data__ == other.__data__
    assert cone.radius == radius
    assert cone.height == height
    assert cone.frame == Frame.worldXY()

    if not compas.IPY:
        assert ConicalSurface.validate_data(cone.__data__)
        assert ConicalSurface.validate_data(other.__data__)


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
