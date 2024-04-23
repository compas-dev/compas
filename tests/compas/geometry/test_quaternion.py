import pytest
import json
import compas
from random import random

from compas.geometry import Quaternion
from compas.geometry import close
from compas.geometry import Frame


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
# Properties and Geometry
# =============================================================================


def test_quaternion_properties():
    w = 1.0
    x = 2.0
    y = 3.0
    z = 4.0

    quaternion = Quaternion(w, x, y, z)

    assert quaternion.wxyz == [w, x, y, z]
    assert quaternion.xyzw == [x, y, z, w]
    assert close(quaternion.norm, 5.4772255)
    assert quaternion.is_unit is False

    quaternion = Quaternion(0.0, 0.0, 0.0, 1.0)
    assert quaternion.norm == 1.0


# =============================================================================
# Accessors
# =============================================================================


def test_quaternion_accessors():
    w = 1.0
    x = 2.0
    y = 3.0
    z = 4.0

    quaternion = Quaternion(w, x, y, z)

    assert quaternion[0] == w
    assert quaternion[1] == x
    assert quaternion[2] == y
    assert quaternion[3] == z

    quaternion[0] = 5.0
    quaternion[1] = 6.0
    quaternion[2] = 7.0
    quaternion[3] = 8.0

    assert quaternion.w == 5.0
    assert quaternion.x == 6.0
    assert quaternion.y == 7.0
    assert quaternion.z == 8.0


# =============================================================================
# Comparison
# =============================================================================


def test_quaternion_comparison():
    quaternion1 = Quaternion(1.0, 2.0, 3.0, 4.0)
    quaternion2 = Quaternion(1.0, 2.0, 3.0, 4.0)
    quaternion3 = Quaternion(5.0, 6.0, 7.0, 8.0)

    assert quaternion1 == quaternion2
    assert quaternion1 != quaternion3


# =============================================================================
# Methods
# =============================================================================


def test_quaternion_other_methods():
    quaternion = Quaternion(1.0, 2.0, 3.0, 4.0)

    conjugate = quaternion.conjugated()
    assert conjugate.w == 1.0
    assert conjugate.x == -2.0
    assert conjugate.y == -3.0
    assert conjugate.z == -4.0

    unitized = quaternion.unitized()
    assert unitized.is_unit

    quaternion = Quaternion.from_frame(Frame.worldZX())
    canonized = quaternion.canonized()

    assert str(canonized) == str("Quaternion(0.5, -0.5, -0.5, -0.5)")
