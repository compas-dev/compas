import pytest
import json
import compas

from compas.geometry import allclose
from compas.geometry import Frame
from compas.geometry import Bezier


def test_bezier_create():
    curve = Bezier([[-1, 0, 0], [0, 1, 0], [+1, 0, 0]])

    assert allclose(curve.points[0], [-1, 0, 0], tol=1e-12)
    assert allclose(curve.points[1], [0, 1, 0], tol=1e-12)
    assert allclose(curve.points[2], [+1, 0, 0], tol=1e-12)

    assert allclose(curve.point_at(0.0), [-1, 0, 0], tol=1e-12)
    assert allclose(curve.point_at(0.5), [0, 0.5, 0], tol=1e-12)
    assert allclose(curve.point_at(1.0), [+1, 0, 0], tol=1e-12)


def test_bezier_create_with_frame():
    with pytest.raises(Exception):
        Bezier([[-1, 0, 0], [0, 1, 0], [+1, 0, 0]], frame=Frame.worldXY())


# =============================================================================
# Data
# =============================================================================


def test_bezier_data():
    curve = Bezier([[-1, 0, 0], [0, 1, 0], [+1, 0, 0]])
    other = Bezier.__from_data__(json.loads(json.dumps(curve.__data__)))

    assert curve.points == other.points
    assert curve.frame.point == other.frame.point
    assert allclose(curve.frame.xaxis, other.frame.xaxis, tol=1e-12)
    assert allclose(curve.frame.yaxis, other.frame.yaxis, tol=1e-12)

    if not compas.IPY:
        assert Bezier.validate_data(curve.__data__)
        assert Bezier.validate_data(other.__data__)


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
