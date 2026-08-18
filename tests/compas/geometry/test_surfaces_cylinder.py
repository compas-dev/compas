import pytest
import json
from math import pi
from random import random

from compas.geometry import Circle
from compas.geometry import Point  # noqa: F401
from compas.geometry import Vector  # noqa: F401
from compas.geometry import Frame
from compas.geometry import Line
from compas.geometry import Plane
from compas.geometry import CylindricalSurface
from compas.tolerance import TOL
from compas.itertools import linspace


@pytest.mark.parametrize(
    "radius",
    [
        1,
        random(),
    ],
)
def test_cylinder(radius):
    cylinder = CylindricalSurface(radius)

    assert cylinder.radius == radius
    assert cylinder.frame == Frame.worldXY()

    other = eval(repr(cylinder))

    for u in linspace(0.0, 1.0, num=100):
        for v in linspace(0.0, 1.0, num=100):
            assert cylinder.point_at(u, v) == cylinder.point_at(u, v, world=False)

    assert TOL.is_close(cylinder.radius, other.radius)
    assert cylinder.frame == other.frame


@pytest.mark.parametrize(
    "frame",
    [
        Frame.worldXY(),
        Frame.worldZX(),
        Frame.worldYZ(),
    ],
)
def test_cylinder_frame(frame):
    radius = random()
    cylinder = CylindricalSurface(radius, frame)

    assert cylinder.radius == radius
    assert cylinder.frame == frame

    other = eval(repr(cylinder))

    for u in linspace(0.0, 1.0, num=100):
        for v in linspace(0.0, 1.0, num=100):
            assert cylinder.point_at(u, v) == cylinder.point_at(u, v, world=False).transformed(cylinder.transformation)

    assert TOL.is_close(cylinder.radius, other.radius)
    assert cylinder.frame == other.frame


# =============================================================================
# Data
# =============================================================================


def test_cylinder_data():
    radius = random()
    cylinder = CylindricalSurface(radius=radius)
    other = CylindricalSurface.__from_data__(json.loads(json.dumps(cylinder.__data__)))

    assert cylinder.__data__ == other.__data__
    assert cylinder.radius == radius
    assert cylinder.frame == Frame.worldXY()


# =============================================================================
# Constructors
# =============================================================================


def test_cylinder_requires_positive_radius():
    with pytest.raises(ValueError, match="larger than zero"):
        CylindricalSurface(0.0)


def test_create_cylinder_from_plane_and_radius_preserves_subclass():
    class CustomCylindricalSurface(CylindricalSurface):
        pass

    cylinder = CustomCylindricalSurface.from_plane_and_radius(Plane.worldYZ(), 2.0)

    assert isinstance(cylinder, CustomCylindricalSurface)
    assert cylinder.radius == 2.0
    assert cylinder.frame == Frame.worldYZ()

# =============================================================================
# Properties and Geometry
# =============================================================================


def test_cylinder_area_and_volume_over_v_domain():
    cylinder = CylindricalSurface(2.0)

    assert TOL.is_close(cylinder.area, 4.0 * pi)
    assert TOL.is_close(cylinder.volume, 4.0 * pi)

# =============================================================================
# Accessors
# =============================================================================

# =============================================================================
# Comparison
# =============================================================================

# =============================================================================
# Other Methods
# =============================================================================


def test_cylinder_isocurves_match_surface_parameterization():
    cylinder = CylindricalSurface(2.0, frame=Frame.worldYZ())
    generator = cylinder.isocurve_u(0.25)
    circle = cylinder.isocurve_v(0.25)

    assert isinstance(generator, Line)
    assert isinstance(circle, Circle)
    for parameter in (0.0, 0.25, 0.5, 0.75, 1.0):
        assert TOL.is_allclose(generator.point_at(parameter), cylinder.point_at(0.25, parameter))
        assert TOL.is_allclose(circle.point_at(parameter), cylinder.point_at(parameter, 0.25))


def test_cylinder_frame_matches_point_and_normal_in_rotated_coordinates():
    cylinder = CylindricalSurface(2.0, frame=Frame.worldZX())
    frame = cylinder.frame_at(0.25, 0.75)

    assert TOL.is_allclose(frame.point, cylinder.point_at(0.25, 0.75))
    assert TOL.is_allclose(frame.zaxis, cylinder.normal_at(0.25, 0.75))
