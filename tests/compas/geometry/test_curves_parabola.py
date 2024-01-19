import pytest
import json
import compas

from compas.geometry import allclose
from compas.geometry import Frame
from compas.geometry import Parabola


def test_parabola_create():
    parabola = Parabola(focal=1)

    assert parabola.focal == 1
    assert parabola.frame == Frame.worldXY()

    assert allclose(parabola.point_at(0.0), parabola.point_at(0.0, world=False), tol=1e-12)
    assert allclose(parabola.point_at(0.5), parabola.point_at(0.5, world=False), tol=1e-12)
    assert allclose(parabola.point_at(1.0), parabola.point_at(1.0, world=False), tol=1e-12)


def test_parabola_create_with_frame():
    frame = Frame.worldZX()
    parabola = Parabola(focal=1, frame=frame)

    assert parabola.focal == 1
    assert parabola.frame == frame

    assert allclose(parabola.point_at(0.0), parabola.point_at(0.0, world=False), tol=1e-12)
    assert not allclose(parabola.point_at(0.5), parabola.point_at(0.5, world=False), tol=1e-12)
    assert not allclose(parabola.point_at(1.0), parabola.point_at(1.0, world=False), tol=1e-12)

    assert allclose(
        parabola.point_at(0.0),
        parabola.point_at(0.0, world=False).transformed(parabola.transformation),
        tol=1e-12,
    )
    assert allclose(
        parabola.point_at(0.5),
        parabola.point_at(0.5, world=False).transformed(parabola.transformation),
        tol=1e-12,
    )
    assert allclose(
        parabola.point_at(1.0),
        parabola.point_at(1.0, world=False).transformed(parabola.transformation),
        tol=1e-12,
    )


# =============================================================================
# Data
# =============================================================================


def test_parabola_data():
    parabola = Parabola(focal=1)
    other = Parabola.__from_data__(json.loads(json.dumps(parabola.__data__)))

    assert parabola.focal == other.focal
    assert parabola.frame.point == other.frame.point
    assert allclose(parabola.frame.xaxis, other.frame.xaxis, tol=1e-12)
    assert allclose(parabola.frame.yaxis, other.frame.yaxis, tol=1e-12)

    if not compas.IPY:
        assert Parabola.validate_data(parabola.__data__)
        assert Parabola.validate_data(other.__data__)


# =============================================================================
# Constructors
# =============================================================================

# =============================================================================
# Properties and Geometry
# =============================================================================


def test_parabola_properties():
    parabola = Parabola(focal=1.0)

    assert parabola.focal == 1.0

    parabola._focal = None
    with pytest.raises(ValueError):
        parabola.focal


# =============================================================================
# Accessors
# =============================================================================

# =============================================================================
# Comparison
# =============================================================================

# =============================================================================
# Other Methods
# =============================================================================
