import pytest
import json
from math import pi
from random import random

from compas.itertools import linspace
from compas.geometry import Arc
from compas.geometry import Circle
from compas.geometry import Point  # noqa: F401
from compas.geometry import Vector  # noqa: F401
from compas.geometry import Frame
from compas.geometry import Plane
from compas.geometry import SphericalSurface
from compas.tolerance import TOL


@pytest.mark.parametrize(
    "radius",
    [
        0,
        1,
        random(),
    ],
)
def test_spherical_surface(radius):
    surf = SphericalSurface(radius)

    assert surf.radius == radius
    assert surf.frame == Frame.worldXY()

    for u in linspace(0.0, 1.0, num=100):
        for v in linspace(0.0, 1.0, num=100):
            assert surf.point_at(u, v) == surf.point_at(u, v, world=False)

    other = eval(repr(surf))

    assert TOL.is_close(surf.radius, other.radius)
    assert surf.frame == other.frame


@pytest.mark.parametrize(
    "frame",
    [
        Frame.worldXY(),
        Frame.worldZX(),
        Frame.worldYZ(),
    ],
)
def test_spherical_surface_with_frame(frame):
    surf = SphericalSurface(radius=1.0, frame=frame)

    assert surf.radius == 1.0
    assert surf.frame == frame

    for u in linspace(0.0, 1.0, num=100):
        for v in linspace(0.0, 1.0, num=100):
            assert surf.point_at(u, v) == surf.point_at(u, v, world=False).transformed(surf.transformation)

    other = eval(repr(surf))

    assert TOL.is_close(surf.radius, other.radius)
    assert surf.frame == other.frame


# =============================================================================
# Data
# =============================================================================


def test_spherical_surface_data():
    radius = random()
    surf = SphericalSurface(radius=radius)
    other = SphericalSurface.__from_data__(json.loads(json.dumps(surf.__data__)))

    assert surf.__data__ == other.__data__
    assert surf.radius == radius
    assert surf.frame == Frame.worldXY()


# =============================================================================
# Constructors
# =============================================================================


def test_create_sphere_from_plane_and_radius():
    class CustomSphericalSurface(SphericalSurface):
        pass

    sphere = CustomSphericalSurface.from_plane_and_radius(Plane.worldYZ(), 2.0)

    assert isinstance(sphere, CustomSphericalSurface)
    assert sphere.radius == 2.0
    assert sphere.frame == Frame.worldYZ()


def test_create_sphere_from_three_points():
    sphere = SphericalSurface.from_three_points([1, 0, 0], [0, 1, 0], [-1, 0, 0])

    assert TOL.is_close(sphere.radius, 1.0)
    assert sphere.center == [0, 0, 0]


def test_create_sphere_from_points():
    sphere = SphericalSurface.from_points([[1, 0, 0], [0, 1, 0], [-1, 0, 0]])

    assert TOL.is_close(sphere.radius, 1.0)
    assert sphere.center == [0, 0, 0]


# =============================================================================
# Properties and Geometry
# =============================================================================


def test_spherical_surface_area_and_volume():
    sphere = SphericalSurface(2.0)

    assert TOL.is_close(sphere.area, 16.0 * pi)
    assert TOL.is_close(sphere.volume, 32.0 / 3.0 * pi)


def test_spherical_surface_center_assignment_creates_independent_point():
    source = Point(1, 2, 3)
    sphere = SphericalSurface(1.0)

    sphere.center = source
    source.x = 10

    assert sphere.center == [1, 2, 3]

# =============================================================================
# Accessors
# =============================================================================

# =============================================================================
# Comparison
# =============================================================================

# =============================================================================
# Other Methods
# =============================================================================


def test_spherical_surface_isocurves_match_surface_parameterization():
    sphere = SphericalSurface(2.0, frame=Frame.worldYZ())
    meridian = sphere.isocurve_u(0.25)
    latitude = sphere.isocurve_v(0.25)

    assert isinstance(meridian, Arc)
    assert isinstance(latitude, Circle)
    for parameter in (0.0, 0.25, 0.5, 0.75, 1.0):
        assert TOL.is_allclose(meridian.point_at(parameter), sphere.point_at(0.25, parameter))
        assert TOL.is_allclose(latitude.point_at(parameter), sphere.point_at(parameter, 0.25))
