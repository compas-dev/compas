import pytest
import json
from math import pi
from random import random

from compas.itertools import linspace
from compas.geometry import Circle
from compas.geometry import Point  # noqa: F401
from compas.geometry import Vector  # noqa: F401
from compas.geometry import Frame
from compas.geometry import Plane
from compas.geometry import ToroidalSurface
from compas.tolerance import TOL


@pytest.mark.parametrize(
    "radius_axis,radius_pipe",
    [
        (2.0, 1.0),
        (1.0 + random(), 0.5),
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

    assert TOL.is_close(torus.radius_axis, other.radius_axis)
    assert TOL.is_close(torus.radius_pipe, other.radius_pipe)
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
    torus = ToroidalSurface(radius_axis=2.0, radius_pipe=0.5, frame=frame)

    assert torus.radius_axis == 2.0
    assert torus.radius_pipe == 0.5
    assert torus.frame == frame

    for u in linspace(0.0, 1.0, num=100):
        for v in linspace(0.0, 1.0, num=100):
            assert torus.point_at(u, v) == torus.point_at(u, v, world=False).transformed(torus.transformation)

    other = eval(repr(torus))

    assert TOL.is_close(torus.radius_axis, other.radius_axis)
    assert TOL.is_close(torus.radius_pipe, other.radius_pipe)
    assert torus.frame == other.frame


# =============================================================================
# Data
# =============================================================================


def test_torus_data():
    radius_axis = 1.0 + random()
    radius_pipe = 0.5
    frame = Frame.worldXY()

    torus = ToroidalSurface(radius_axis=radius_axis, radius_pipe=radius_pipe, frame=frame)
    other = ToroidalSurface.__from_data__(json.loads(json.dumps(torus.__data__)))

    assert torus.radius_axis == other.radius_axis
    assert torus.radius_pipe == other.radius_pipe
    assert torus.frame == frame


# =============================================================================
# Constructors
# =============================================================================


@pytest.mark.parametrize("radius_axis, radius_pipe", [(0.0, 0.5), (2.0, 0.0), (1.0, 1.0), (1.0, 2.0)])
def test_torus_requires_regular_ring_radii(radius_axis, radius_pipe):
    with pytest.raises(ValueError):
        ToroidalSurface(radius_axis, radius_pipe)


def test_torus_from_plane_preserves_subclass():
    class CustomToroidalSurface(ToroidalSurface):
        pass

    torus = CustomToroidalSurface.from_plane_and_radii(Plane.worldYZ(), 2.0, 0.5)

    assert isinstance(torus, CustomToroidalSurface)
    assert torus.frame == Frame.worldYZ()

# =============================================================================
# Properties and Geometry
# =============================================================================


def test_torus_area_and_volume():
    torus = ToroidalSurface(2.0, 0.5)

    assert TOL.is_close(torus.area, 4.0 * pi**2)
    assert TOL.is_close(torus.volume, pi**2)

# =============================================================================
# Accessors
# =============================================================================

# =============================================================================
# Comparison
# =============================================================================

# =============================================================================
# Other Methods
# =============================================================================


def test_torus_isocurves_match_surface_parameterization():
    torus = ToroidalSurface(2.0, 0.5, frame=Frame.worldYZ())
    pipe = torus.isocurve_u(0.25)
    ring = torus.isocurve_v(0.25)

    assert isinstance(pipe, Circle)
    assert isinstance(ring, Circle)
    for parameter in (0.0, 0.25, 0.5, 0.75, 1.0):
        assert TOL.is_allclose(pipe.point_at(parameter), torus.point_at(0.25, parameter))
        assert TOL.is_allclose(ring.point_at(parameter), torus.point_at(parameter, 0.25))


def test_torus_frame_matches_point_and_normal_in_rotated_coordinates():
    torus = ToroidalSurface(2.0, 0.5, frame=Frame.worldZX())
    frame = torus.frame_at(0.25, 0.75)

    assert TOL.is_allclose(frame.point, torus.point_at(0.25, 0.75))
    assert TOL.is_allclose(frame.zaxis, torus.normal_at(0.25, 0.75))
