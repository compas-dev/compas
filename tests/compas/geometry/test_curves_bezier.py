import pytest
from compas.geometry import allclose
from compas.geometry import Frame
from compas.geometry import Bezier


def test_create_bezier():
    curve = Bezier([[-1, 0, 0], [0, 1, 0], [+1, 0, 0]])

    assert allclose(curve.points[0], [-1, 0, 0], tol=1e-12)
    assert allclose(curve.points[1], [0, 1, 0], tol=1e-12)
    assert allclose(curve.points[2], [+1, 0, 0], tol=1e-12)

    assert allclose(curve.point_at(0.0), [-1, 0, 0], tol=1e-12)
    assert allclose(curve.point_at(0.5), [0, 0.5, 0], tol=1e-12)
    assert allclose(curve.point_at(1.0), [+1, 0, 0], tol=1e-12)


def test_create_bezier_frame():
    with pytest.raises(Exception):
        Bezier([[-1, 0, 0], [0, 1, 0], [+1, 0, 0]], frame=Frame.worldXY())


# =============================================================================
# Constructors
# =============================================================================

# =============================================================================
# Properties and Geometry
# =============================================================================


def test_bezier_properties():
    curve = Bezier([[-1, 0, 0], [0, 1, 0], [+1, 0, 0]])

    assert curve.frame == Frame.worldXY()

    with pytest.raises(Exception):
        curve.frame = Frame.worldXY()


def test_bezier_geometry():
    curve = Bezier([[-1, 0, 0], [0, 1, 0], [+1, 0, 0]])

    assert allclose(curve.tangent_at(0.0), (curve.points[1] - curve.points[0]).unitized(), tol=1e-12)
    assert allclose(curve.tangent_at(1.0), (curve.points[2] - curve.points[1]).unitized(), tol=1e-12)

    assert allclose(curve.tangent_at(0.5), [1, 0, 0], tol=1e-12)
    assert allclose(curve.normal_at(0.5), [0, -1, 0], tol=1e-12)


# =============================================================================
# Accessors
# =============================================================================

# =============================================================================
# Comparison
# =============================================================================

# =============================================================================
# Other Methods
# =============================================================================
