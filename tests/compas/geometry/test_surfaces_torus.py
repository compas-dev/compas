import pytest
import json
import compas
from random import random

from compas.itertools import linspace
from compas.geometry import Point  # noqa: F401
from compas.geometry import Vector  # noqa: F401
from compas.geometry import Frame
from compas.geometry import ToroidalSurface
from compas.tolerance import TOL


@pytest.mark.parametrize(
    "radius_axis,radius_pipe",
    [
        (0, 0),
        (1, 0),
        (0, 1),
        (1, 1),
        (random(), random()),
    ],
)
def test_torus(radius_axis, radius_pipe):
    torus = ToroidalSurface(radius_axis=radius_axis, radius_pipe=radius_pipe)

    assert torus.radius_axis == radius_axis
    assert torus.radius_pipe == radius_pipe
    assert torus.frame == Frame.worldXY()

    for u in linspace(0.0, 1.0, num=100):
        for v in linspace(0.0, 1.0, num=100):
            assert torus.point_at(u, v) == torus.point_at(u, v, world=False)

    other = eval(repr(torus))

    assert TOL.is_close(torus.radius_axis, other.radius_axis, tol=1e-12)
    assert TOL.is_close(torus.radius_pipe, other.radius_pipe, tol=1e-12)
    assert torus.frame == other.frame


@pytest.mark.parametrize(
    "frame",
    [
        Frame.worldXY(),
        Frame.worldZX(),
        Frame.worldYZ(),
    ],
)
def test_torus_with_frame(frame):
    torus = ToroidalSurface(radius_axis=1.0, radius_pipe=1.0, frame=frame)

    assert torus.radius_axis == 1.0
    assert torus.radius_pipe == 1.0
    assert torus.frame == frame

    for u in linspace(0.0, 1.0, num=100):
        for v in linspace(0.0, 1.0, num=100):
            assert torus.point_at(u, v) == torus.point_at(u, v, world=False).transformed(torus.transformation)

    other = eval(repr(torus))

    assert TOL.is_close(torus.radius_axis, other.radius_axis, tol=1e-12)
    assert TOL.is_close(torus.radius_pipe, other.radius_pipe, tol=1e-12)
    assert torus.frame == other.frame


# =============================================================================
# Data
# =============================================================================


def test_torus_data():
    radius_axis = random()
    radius_pipe = random()
    frame = Frame.worldXY()

    torus = ToroidalSurface(radius_axis=radius_axis, radius_pipe=radius_pipe, frame=frame)
    other = ToroidalSurface.__from_data__(json.loads(json.dumps(torus.__data__)))

    assert torus.radius_axis == other.radius_axis
    assert torus.radius_pipe == other.radius_pipe
    assert torus.frame == frame

    if not compas.IPY:
        assert ToroidalSurface.validate_data(torus.__data__)
        assert ToroidalSurface.validate_data(other.__data__)


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
