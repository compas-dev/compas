import pytest

from compas.geometry import allclose
from compas.geometry import Frame
from compas.geometry import Parabola


def test_create_parabola():
    parabola = Parabola(focal=1)

    assert parabola.focal == 1
    assert parabola.frame == Frame.worldXY()

    assert allclose(parabola.point_at(0.0), parabola.point_at(0.0, world=False), tol=1e-12)
    assert allclose(parabola.point_at(0.5), parabola.point_at(0.5, world=False), tol=1e-12)
    assert allclose(parabola.point_at(1.0), parabola.point_at(1.0, world=False), tol=1e-12)


def test_create_parabola_frame():
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
