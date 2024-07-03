import pytest
import json
import compas

from compas.tolerance import TOL
from compas.geometry import Frame
from compas.geometry import Hyperbola


def test_hyperbola_create():
    hyperbola = Hyperbola(major=1.0, minor=0.5)

    assert TOL.is_close(hyperbola.major, 1.0)
    assert TOL.is_close(hyperbola.minor, 0.5)
    assert TOL.is_close(hyperbola.semifocal, 1.118033988749895)
    assert TOL.is_close(hyperbola.eccentricity, 1.118033988749895)
    assert TOL.is_close(hyperbola.focal, 2.23606797749979)

    assert hyperbola.is_closed
    assert hyperbola.is_periodic

    assert hyperbola.frame == Frame.worldXY()

    assert TOL.is_allclose(hyperbola.point_at(0.0), hyperbola.point_at(0.0, world=False))
    assert TOL.is_allclose(hyperbola.point_at(0.25), hyperbola.point_at(0.25, world=False))
    assert TOL.is_allclose(hyperbola.point_at(0.5), hyperbola.point_at(0.5, world=False))
    assert TOL.is_allclose(hyperbola.point_at(0.75), hyperbola.point_at(0.75, world=False))
    assert TOL.is_allclose(hyperbola.point_at(1.0), hyperbola.point_at(1.0, world=False))


def test_hyperbola_create_with_frame():
    hyperbola = Hyperbola(major=1.0, minor=0.5, frame=Frame.worldZX())

    assert TOL.is_close(hyperbola.major, 1.0)
    assert TOL.is_close(hyperbola.minor, 0.5)
    assert TOL.is_close(hyperbola.semifocal, 1.118033988749895)
    assert TOL.is_close(hyperbola.eccentricity, 1.118033988749895)
    assert TOL.is_close(hyperbola.focal, 2.23606797749979)

    assert hyperbola.is_closed
    assert hyperbola.is_periodic

    assert hyperbola.frame == Frame.worldZX()

    assert TOL.is_allclose(
        hyperbola.point_at(0.0),
        hyperbola.point_at(0.0, world=False).transformed(hyperbola.transformation),
    )
    assert TOL.is_allclose(
        hyperbola.point_at(0.25),
        hyperbola.point_at(0.25, world=False).transformed(hyperbola.transformation),
    )
    assert TOL.is_allclose(
        hyperbola.point_at(0.50),
        hyperbola.point_at(0.50, world=False).transformed(hyperbola.transformation),
    )
    assert TOL.is_allclose(
        hyperbola.point_at(0.75),
        hyperbola.point_at(0.75, world=False).transformed(hyperbola.transformation),
    )
    assert TOL.is_allclose(
        hyperbola.point_at(1.00),
        hyperbola.point_at(1.00, world=False).transformed(hyperbola.transformation),
    )


# =============================================================================
# Data
# =============================================================================


def test_hyperbola_data():
    hyperbola = Hyperbola(major=1.0, minor=0.5)
    other = Hyperbola.__from_data__(json.loads(json.dumps(hyperbola.__data__)))

    assert hyperbola.major == other.major
    assert hyperbola.minor == other.minor
    assert hyperbola.frame.point == other.frame.point
    assert TOL.is_allclose(hyperbola.frame.xaxis, other.frame.xaxis)
    assert TOL.is_allclose(hyperbola.frame.yaxis, other.frame.yaxis)

    if not compas.IPY:
        assert Hyperbola.validate_data(hyperbola.__data__)
        assert Hyperbola.validate_data(other.__data__)


# =============================================================================
# Constructors
# =============================================================================

# =============================================================================
# Properties and Geometry
# =============================================================================


def test_hyperbola_major():
    hyperbola = Hyperbola(major=1.0, minor=0.5)

    assert TOL.is_close(hyperbola.major, 1.0)

    hyperbola._major = None
    with pytest.raises(ValueError):
        hyperbola.major

    with pytest.raises(ValueError):
        hyperbola.major = -1.0


def test_hyperbola_minor():
    hyperbola = Hyperbola(major=1.0, minor=0.5)

    assert TOL.is_close(hyperbola.minor, 0.5)

    hyperbola._minor = None
    with pytest.raises(ValueError):
        hyperbola.minor

    with pytest.raises(ValueError):
        hyperbola.minor = -1.0


# =============================================================================
# Accessors
# =============================================================================

# =============================================================================
# Comparison
# =============================================================================

# =============================================================================
# Other Methods
# =============================================================================
