import pytest
import json

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

    assert not hyperbola.is_closed
    assert not hyperbola.is_periodic

    assert hyperbola.frame == Frame.worldXY()

    assert TOL.is_allclose(hyperbola.point_at(0.0), hyperbola.point_at(0.0, world=False))
    assert TOL.is_allclose(hyperbola.point_at(-1.0), hyperbola.point_at(-1.0, world=False))
    assert TOL.is_allclose(hyperbola.point_at(1.0), hyperbola.point_at(1.0, world=False))


def test_hyperbola_create_with_frame():
    hyperbola = Hyperbola(major=1.0, minor=0.5, frame=Frame.worldZX())

    assert TOL.is_close(hyperbola.major, 1.0)
    assert TOL.is_close(hyperbola.minor, 0.5)
    assert TOL.is_close(hyperbola.semifocal, 1.118033988749895)
    assert TOL.is_close(hyperbola.eccentricity, 1.118033988749895)
    assert TOL.is_close(hyperbola.focal, 2.23606797749979)

    assert not hyperbola.is_closed
    assert not hyperbola.is_periodic

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


def test_hyperbola_branches_and_derivatives():
    positive = Hyperbola(major=2.0, minor=1.0, branch=1)
    negative = Hyperbola(major=2.0, minor=1.0, branch=-1)

    assert TOL.is_allclose(positive.point_at(0.0), [2.0, 0.0, 0.0])
    assert TOL.is_allclose(negative.point_at(0.0), [-2.0, 0.0, 0.0])
    assert TOL.is_allclose(positive.tangent_at(0.0), [0.0, 1.0, 0.0])
    assert TOL.is_allclose(positive.normal_at(0.0), [-1.0, 0.0, 0.0])
    assert TOL.is_close(positive.tangent_at(1.0).dot(positive.normal_at(1.0)), 0.0)


def test_hyperbola_asymptotes():
    hyperbola = Hyperbola(major=2.0, minor=1.0)

    assert TOL.is_allclose(hyperbola.asymptote1.closest_point([2.0, 1.0, 0.0]), [2.0, 1.0, 0.0])
    assert TOL.is_allclose(hyperbola.asymptote2.closest_point([2.0, -1.0, 0.0]), [2.0, -1.0, 0.0])


def test_hyperbola_comparison():
    hyperbola = Hyperbola(major=2.0, minor=1.0)

    assert hyperbola == Hyperbola(major=2.0, minor=1.0)
    assert hyperbola != Hyperbola(major=2.0, minor=1.0, branch=-1)
    assert hyperbola != object()


def test_hyperbola_invalid_dimensions_and_branch():
    with pytest.raises(ValueError):
        Hyperbola(major=0.0, minor=1.0)
    with pytest.raises(ValueError):
        Hyperbola(major=1.0, minor=0.0)
    with pytest.raises(ValueError):
        Hyperbola(major=1.0, minor=1.0, branch=0)


# =============================================================================
# Accessors
# =============================================================================

# =============================================================================
# Comparison
# =============================================================================

# =============================================================================
# Other Methods
# =============================================================================
