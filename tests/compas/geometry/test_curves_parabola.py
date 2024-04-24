import pytest
import json
import compas

from compas.tolerance import TOL
from compas.geometry import Frame
from compas.geometry import Parabola


def test_parabola_create():
    parabola = Parabola(focal=1)

    assert parabola.focal == 1
    assert parabola.frame == Frame.worldXY()

    assert TOL.is_allclose(parabola.point_at(0.0), parabola.point_at(0.0, world=False))
    assert TOL.is_allclose(parabola.point_at(0.5), parabola.point_at(0.5, world=False))
    assert TOL.is_allclose(parabola.point_at(1.0), parabola.point_at(1.0, world=False))


def test_parabola_create_with_frame():
    frame = Frame.worldZX()
    parabola = Parabola(focal=1, frame=frame)

    assert parabola.focal == 1
    assert parabola.frame == frame

    assert TOL.is_allclose(parabola.point_at(0.0), parabola.point_at(0.0, world=False))
    assert not TOL.is_allclose(parabola.point_at(0.5), parabola.point_at(0.5, world=False))
    assert not TOL.is_allclose(parabola.point_at(1.0), parabola.point_at(1.0, world=False))

    assert TOL.is_allclose(
        parabola.point_at(0.0),
        parabola.point_at(0.0, world=False).transformed(parabola.transformation),
    )
    assert TOL.is_allclose(
        parabola.point_at(0.5),
        parabola.point_at(0.5, world=False).transformed(parabola.transformation),
    )
    assert TOL.is_allclose(
        parabola.point_at(1.0),
        parabola.point_at(1.0, world=False).transformed(parabola.transformation),
    )


# =============================================================================
# Data
# =============================================================================


def test_parabola_data():
    parabola = Parabola(focal=1)
    other = Parabola.__from_data__(json.loads(json.dumps(parabola.__data__)))

    assert parabola.focal == other.focal
    assert parabola.frame.point == other.frame.point
    assert TOL.is_allclose(parabola.frame.xaxis, other.frame.xaxis)
    assert TOL.is_allclose(parabola.frame.yaxis, other.frame.yaxis)

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
