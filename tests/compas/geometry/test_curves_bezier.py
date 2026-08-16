import pytest
import json
from math import asinh
from math import sqrt

from compas.tolerance import TOL
from compas.geometry import Frame
from compas.geometry import Bezier


def test_bezier_create():
    curve = Bezier([[-1, 0, 0], [0, 1, 0], [+1, 0, 0]])

    assert TOL.is_allclose(curve.points[0], [-1, 0, 0])
    assert TOL.is_allclose(curve.points[1], [0, 1, 0])
    assert TOL.is_allclose(curve.points[2], [+1, 0, 0])

    assert TOL.is_allclose(curve.point_at(0.0), [-1, 0, 0])
    assert TOL.is_allclose(curve.point_at(0.5), [0, 0.5, 0])
    assert TOL.is_allclose(curve.point_at(1.0), [+1, 0, 0])


def test_bezier_create_with_frame():
    with pytest.raises(TypeError):
        Bezier([[-1, 0, 0], [0, 1, 0], [+1, 0, 0]], frame=Frame.worldXY())


# =============================================================================
# Data
# =============================================================================


def test_bezier_data():
    curve = Bezier([[-1, 0, 0], [0, 1, 0], [+1, 0, 0]])
    other = Bezier.__from_data__(json.loads(json.dumps(curve.__data__)))

    assert curve.points == other.points
    assert curve.frame.point == other.frame.point
    assert TOL.is_allclose(curve.frame.xaxis, other.frame.xaxis)
    assert TOL.is_allclose(curve.frame.yaxis, other.frame.yaxis)


# =============================================================================
# Constructors
# =============================================================================

# =============================================================================
# Properties and Geometry
# =============================================================================


def test_bezier_properties():
    curve = Bezier([[-1, 0, 0], [0, 1, 0], [+1, 0, 0]])

    assert curve.frame == Frame.worldXY()

    with pytest.raises(AttributeError):
        curve.frame = Frame.worldXY()

    assert not curve.is_closed
    assert not curve.is_periodic


def test_bezier_length():
    line = Bezier([[0.0, 0.0, 0.0], [3.0, 4.0, 0.0]])
    quadratic = Bezier([[-1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [1.0, 0.0, 0.0]])

    assert TOL.is_close(line.length, 5.0)
    assert TOL.is_close(quadratic.length, sqrt(2.0) + asinh(1.0))


def test_closed_bezier_is_not_periodic():
    curve = Bezier([[0.0, 0.0, 0.0], [1.0, 1.0, 0.0], [0.0, 0.0, 0.0]])

    assert curve.is_closed
    assert not curve.is_periodic


def test_bezier_geometry():
    curve = Bezier([[-1, 0, 0], [0, 1, 0], [+1, 0, 0]])

    assert TOL.is_allclose(curve.tangent_at(0.0), (curve.points[1] - curve.points[0]).unitized())
    assert TOL.is_allclose(curve.tangent_at(1.0), (curve.points[2] - curve.points[1]).unitized())

    assert TOL.is_allclose(curve.tangent_at(0.5), [1, 0, 0])
    assert TOL.is_allclose(curve.normal_at(0.5), [0, -1, 0])


def test_bezier_comparison():
    curve = Bezier([[-1, 0, 0], [0, 1, 0], [+1, 0, 0]])

    assert curve == Bezier([[-1, 0, 0], [0, 1, 0], [+1, 0, 0]])
    assert curve != Bezier([[-1, 0, 0], [0, 2, 0], [+1, 0, 0]])
    assert curve != object()


def test_bezier_control_points_are_independent_and_require_3d():
    points = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0]]
    curve = Bezier(points)
    points[0][0] = 2.0

    assert curve.points[0].x == 0.0
    with pytest.raises(ValueError):
        curve.points = []
    with pytest.raises(IndexError):
        Bezier([[0.0, 0.0], [1.0, 0.0, 0.0]])


def test_bezier_parameter_domain():
    curve = Bezier([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0]])

    with pytest.raises(ValueError):
        curve.point_at(-0.1)
    with pytest.raises(ValueError):
        curve.tangent_at(1.1)


def test_linear_bezier_has_no_normal():
    curve = Bezier([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0]])

    assert curve.normal_at(0.5) is None


# =============================================================================
# Accessors
# =============================================================================

# =============================================================================
# Comparison
# =============================================================================

# =============================================================================
# Other Methods
# =============================================================================
