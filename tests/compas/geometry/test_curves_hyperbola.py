import pytest
import json
import compas

from compas.geometry import close
from compas.geometry import allclose
from compas.geometry import Frame
from compas.geometry import Hyperbola


def test_hyperbola_create():
    hyperbola = Hyperbola(major=1.0, minor=0.5)

    assert close(hyperbola.major, 1.0, tol=1e-12)
    assert close(hyperbola.minor, 0.5, tol=1e-12)
    assert close(hyperbola.semifocal, 1.118033988749895, tol=1e-12)
    assert close(hyperbola.eccentricity, 1.118033988749895, tol=1e-12)
    assert close(hyperbola.focal, 2.23606797749979, tol=1e-12)

    assert hyperbola.is_closed
    assert hyperbola.is_periodic

    assert hyperbola.frame == Frame.worldXY()

    assert allclose(hyperbola.point_at(0.0), hyperbola.point_at(0.0, world=False), tol=1e-12)
    assert allclose(hyperbola.point_at(0.25), hyperbola.point_at(0.25, world=False), tol=1e-12)
    assert allclose(hyperbola.point_at(0.5), hyperbola.point_at(0.5, world=False), tol=1e-12)
    assert allclose(hyperbola.point_at(0.75), hyperbola.point_at(0.75, world=False), tol=1e-12)
    assert allclose(hyperbola.point_at(1.0), hyperbola.point_at(1.0, world=False), tol=1e-12)


def test_hyperbola_create_with_frame():
    hyperbola = Hyperbola(major=1.0, minor=0.5, frame=Frame.worldZX())

    assert close(hyperbola.major, 1.0, tol=1e-12)
    assert close(hyperbola.minor, 0.5, tol=1e-12)
    assert close(hyperbola.semifocal, 1.118033988749895, tol=1e-12)
    assert close(hyperbola.eccentricity, 1.118033988749895, tol=1e-12)
    assert close(hyperbola.focal, 2.23606797749979, tol=1e-12)

    assert hyperbola.is_closed
    assert hyperbola.is_periodic

    assert hyperbola.frame == Frame.worldZX()

    assert allclose(
        hyperbola.point_at(0.0),
        hyperbola.point_at(0.0, world=False).transformed(hyperbola.transformation),
        tol=1e-12,
    )
    assert allclose(
        hyperbola.point_at(0.25),
        hyperbola.point_at(0.25, world=False).transformed(hyperbola.transformation),
        tol=1e-12,
    )
    assert allclose(
        hyperbola.point_at(0.50),
        hyperbola.point_at(0.50, world=False).transformed(hyperbola.transformation),
        tol=1e-12,
    )
    assert allclose(
        hyperbola.point_at(0.75),
        hyperbola.point_at(0.75, world=False).transformed(hyperbola.transformation),
        tol=1e-12,
    )
    assert allclose(
        hyperbola.point_at(1.00),
        hyperbola.point_at(1.00, world=False).transformed(hyperbola.transformation),
        tol=1e-12,
    )


# =============================================================================
# Data
# =============================================================================


def test_hyperbola_data():
    hyperbola = Hyperbola(major=1.0, minor=0.5)
    other = Hyperbola.from_data(json.loads(json.dumps(hyperbola.data)))

    assert hyperbola.major == other.major
    assert hyperbola.minor == other.minor
    assert hyperbola.frame.point == other.frame.point
    assert allclose(hyperbola.frame.xaxis, other.frame.xaxis, tol=1e-12)
    assert allclose(hyperbola.frame.yaxis, other.frame.yaxis, tol=1e-12)

    if not compas.IPY:
        assert Hyperbola.validate_data(hyperbola.data)
        assert Hyperbola.validate_data(other.data)


# =============================================================================
# Constructors
# =============================================================================

# =============================================================================
# Properties and Geometry
# =============================================================================


def test_hyperbola_major():
    hyperbola = Hyperbola(major=1.0, minor=0.5)

    assert close(hyperbola.major, 1.0, tol=1e-12)

    hyperbola._major = None
    with pytest.raises(ValueError):
        hyperbola.major

    with pytest.raises(ValueError):
        hyperbola.major = -1.0


def test_hyperbola_minor():
    hyperbola = Hyperbola(major=1.0, minor=0.5)

    assert close(hyperbola.minor, 0.5, tol=1e-12)

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
