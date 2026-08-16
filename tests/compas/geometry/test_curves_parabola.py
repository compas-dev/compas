import pytest
import json

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


def test_parabola_geometry():
    parabola = Parabola(focal=1.0)

    assert parabola.domain == (-float("inf"), float("inf"))
    assert parabola.latus == 4.0
    assert parabola.eccentricity == 1.0
    assert TOL.is_allclose(parabola.focus, [0.0, 1.0, 0.0])
    assert TOL.is_allclose(parabola.vertex, [0.0, 0.0, 0.0])
    assert TOL.is_allclose(parabola.directix.closest_point([2.0, -1.0, 0.0]), [2.0, -1.0, 0.0])
    assert not parabola.is_closed
    assert not parabola.is_periodic


def test_parabola_derivatives():
    parabola = Parabola(focal=1.0)

    assert TOL.is_allclose(parabola.tangent_at(0.0), [1.0, 0.0, 0.0])
    assert TOL.is_allclose(parabola.normal_at(0.0), [0.0, 1.0, 0.0])
    assert parabola.tangent_at(-1.0).x > 0.0
    assert TOL.is_close(parabola.tangent_at(2.0).dot(parabola.normal_at(2.0)), 0.0)


def test_parabola_invalid_focal_and_coefficient():
    with pytest.raises(ValueError):
        Parabola(focal=0.0)
    with pytest.raises(ValueError):
        Parabola(focal=-1.0)

    parabola = Parabola(focal=1.0)
    with pytest.raises(ValueError):
        parabola.a = 0.0


def test_parabola_comparison():
    parabola = Parabola(focal=1.0)

    assert parabola == Parabola(focal=1.0)
    assert parabola != Parabola(focal=2.0)
    assert parabola != object()


def test_parabola_from_data_preserves_subclass():
    class CustomParabola(Parabola):
        pass

    parabola = CustomParabola.__from_data__(Parabola(focal=1.0).__data__)
    assert isinstance(parabola, CustomParabola)


# =============================================================================
# Accessors
# =============================================================================

# =============================================================================
# Comparison
# =============================================================================

# =============================================================================
# Other Methods
# =============================================================================
