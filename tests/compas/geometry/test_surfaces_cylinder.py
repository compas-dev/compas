import pytest
import json
import compas
from random import random

from compas.geometry import Point  # noqa: F401
from compas.geometry import Vector  # noqa: F401
from compas.geometry import Frame
from compas.geometry import CylindricalSurface
from compas.geometry import close


# =============================================================================
# Constructors
# =============================================================================


@pytest.mark.parametrize("radius", [0, 1, random()])
def test_cylinder(radius):
    cylinder = CylindricalSurface(radius)

    assert cylinder.radius == radius
    assert cylinder.frame == Frame.worldXY()

    other = eval(repr(cylinder))

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
