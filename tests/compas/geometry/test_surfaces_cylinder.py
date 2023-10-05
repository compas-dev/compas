import pytest
import json
import compas
from random import random

from compas.geometry import Point  # noqa: F401
from compas.geometry import Vector  # noqa: F401
from compas.geometry import Frame
from compas.geometry import CylindricalSurface
from compas.geometry import close
from compas.utilities import linspace


@pytest.mark.parametrize(
    "radius",
    [
        0,
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

    assert close(cylinder.radius, other.radius, tol=1e-12)
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

    assert close(cylinder.radius, other.radius, tol=1e-12)
    assert cylinder.frame == other.frame


# =============================================================================
# Data
# =============================================================================


def test_cylinder_data():
    radius = random()
    cylinder = CylindricalSurface(radius=radius)
    other = CylindricalSurface.from_data(json.loads(json.dumps(cylinder.data)))

    assert cylinder.data == other.data
    assert cylinder.radius == radius
    assert cylinder.frame == Frame.worldXY()

    if not compas.IPY:
        assert CylindricalSurface.validate_data(cylinder.data)
        assert CylindricalSurface.validate_data(other.data)


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
