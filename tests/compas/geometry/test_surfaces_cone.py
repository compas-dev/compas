import pytest
import json
from math import pi
from math import sqrt
from random import random

from compas.geometry import Circle
from compas.geometry import Point  # noqa: F401
from compas.geometry import Vector  # noqa: F401
from compas.geometry import Frame
from compas.geometry import Line
from compas.geometry import Plane
from compas.geometry import ConicalSurface
from compas.tolerance import TOL
from compas.itertools import linspace


@pytest.mark.parametrize(
    "radius,height",
    [
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

    assert TOL.is_close(cone.radius, other.radius)
    assert TOL.is_close(cone.height, other.height)
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

    assert TOL.is_close(cone.radius, other.radius)
    assert TOL.is_close(cone.height, other.height)
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


# =============================================================================
# Constructors
# =============================================================================


@pytest.mark.parametrize("radius, height", [(0.0, 1.0), (1.0, 0.0), (-1.0, 1.0), (1.0, -1.0)])
def test_cone_requires_positive_radius_and_height(radius, height):
    with pytest.raises(ValueError, match="larger than zero"):
        ConicalSurface(radius, height)


def test_cone_from_plane_preserves_subclass():
    class CustomConicalSurface(ConicalSurface):
        pass

    cone = CustomConicalSurface.from_plane_and_radius_height(Plane.worldYZ(), 2.0, 3.0)

    assert isinstance(cone, CustomConicalSurface)
    assert cone.radius == 2.0
    assert cone.height == 3.0
    assert cone.frame == Frame.worldYZ()

# =============================================================================
# Properties and Geometry
# =============================================================================


def test_cone_area_and_volume():
    cone = ConicalSurface(2.0, 3.0)

    assert TOL.is_close(cone.area, 2.0 * pi * sqrt(13.0))
    assert TOL.is_close(cone.volume, 4.0 * pi)

# =============================================================================
# Accessors
# =============================================================================

# =============================================================================
# Comparison
# =============================================================================

# =============================================================================
# Other Methods
# =============================================================================


def test_cone_isocurves_match_surface_parameterization():
    cone = ConicalSurface(2.0, 3.0, frame=Frame.worldYZ())
    generator = cone.isocurve_u(0.25)
    circle = cone.isocurve_v(0.25)

    assert isinstance(generator, Line)
    assert isinstance(circle, Circle)
    for parameter in (0.0, 0.25, 0.5, 0.75, 1.0):
        assert TOL.is_allclose(generator.point_at(parameter), cone.point_at(0.25, parameter))
        assert TOL.is_allclose(circle.point_at(parameter), cone.point_at(parameter, 0.25))


def test_cone_isocurve_at_apex_is_degenerate():
    with pytest.raises(ValueError, match="degenerate"):
        ConicalSurface(2.0, 3.0).isocurve_v(1.0)


def test_cone_frame_matches_point_and_normal_in_rotated_coordinates():
    cone = ConicalSurface(2.0, 3.0, frame=Frame.worldZX())
    frame = cone.frame_at(0.25, 0.75)

    assert TOL.is_allclose(frame.point, cone.point_at(0.25, 0.75))
    assert TOL.is_allclose(frame.zaxis, cone.normal_at(0.25, 0.75))
