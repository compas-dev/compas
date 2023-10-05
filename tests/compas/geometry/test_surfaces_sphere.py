import pytest
import json
import compas
from random import random

from compas.utilities import linspace
from compas.geometry import Point  # noqa: F401
from compas.geometry import Vector  # noqa: F401
from compas.geometry import Frame
from compas.geometry import SphericalSurface
from compas.geometry import close


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

    assert close(surf.radius, other.radius, tol=1e-12)
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

    assert close(surf.radius, other.radius, tol=1e-12)
    assert surf.frame == other.frame


# =============================================================================
# Data
# =============================================================================


def test_spherical_surface_data():
    radius = random()
    surf = SphericalSurface(radius=radius)
    other = SphericalSurface.from_data(json.loads(json.dumps(surf.data)))

    assert surf.data == other.data
    assert surf.radius == radius
    assert surf.frame == Frame.worldXY()

    if not compas.IPY:
        assert SphericalSurface.validate_data(surf.data)
        assert SphericalSurface.validate_data(other.data)


# =============================================================================
# Constructors
# =============================================================================


def test_create_sphere_from_plane_and_radius():
    pass


def test_create_sphere_from_three_points():
    pass


def test_create_sphere_from_points():
    pass


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
