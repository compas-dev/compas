import pytest
import json
import compas
from random import random

from compas.geometry import Quaternion
from compas.geometry import close


@pytest.mark.parametrize(
    "x,y,z,w",
    [
        (0.0, 0.0, 0.0, 0.0),
        (0.0, 0.0, 0.0, 1.0),
        (1.0, 0.0, 0.0, 0.0),
        (1.0, 0.0, 0.0, 1.0),
        (0.0, 1.0, 0.0, 0.0),
        (0.0, 1.0, 0.0, 1.0),
        (0.0, 0.0, 1.0, 0.0),
        (0.0, 0.0, 1.0, 1.0),
        (1.0, 1.0, 1.0, 0.0),
        (1.0, 1.0, 1.0, 1.0),
        (random(), random(), random(), random()),
    ],
)
def test_quaternion(w, x, y, z):
    quaternion = Quaternion(w, x, y, z)

    assert quaternion.w == w
    assert quaternion.x == x
    assert quaternion.y == y
    assert quaternion.z == z

    other = eval(repr(quaternion))

    assert close(quaternion.w, other.w, tol=1e-12)
    assert close(quaternion.x, other.x, tol=1e-12)
    assert close(quaternion.y, other.y, tol=1e-12)
    assert close(quaternion.z, other.z, tol=1e-12)


# =============================================================================
# Data
# =============================================================================


def test_quaternion_data():
    x = random()
    y = random()
    z = random()
    w = random()

    quaternion = Quaternion(w, x, y, z)
    other = Quaternion.__from_data__(json.loads(json.dumps(quaternion.__data__)))

    assert quaternion.w == other.w
    assert quaternion.x == other.x
    assert quaternion.y == other.y
    assert quaternion.z == other.z

    if not compas.IPY:
        assert Quaternion.validate_data(quaternion.__data__)
        assert Quaternion.validate_data(other.__data__)


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
