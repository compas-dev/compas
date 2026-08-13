import pytest

from compas.tolerance import TOL
from compas.geometry import tangent_points_to_circle_xy


def test_tangent_points_to_circle_xy():
    circle = ((0.0, 0.0, 0.0), (0.0, 0.0, 1.0)), 1.0
    point = (2.0, 4.0, 0.0)
    t1, t2 = tangent_points_to_circle_xy(circle, point)
    assert TOL.is_allclose(t1, (-0.772, 0.636, 0.000), atol=1e-3)
    assert TOL.is_allclose(t2, (0.972, -0.236, 0.000), atol=1e-3)


def test_tangent_points_accepts_two_coordinates_and_translated_circle():
    circle = ((1.0, 2.0, 0.0), (0.0, 0.0, 1.0)), 1.0
    t1, t2 = tangent_points_to_circle_xy(circle, (3.0, 2.0))
    assert TOL.is_allclose(t1, (1.5, 2.8660254, 0.0))
    assert TOL.is_allclose(t2, (1.5, 1.1339746, 0.0))


def test_tangent_point_on_circle_returns_same_point_twice():
    circle = ((0.0, 0.0, 0.0), (0.0, 0.0, 1.0)), 1.0
    t1, t2 = tangent_points_to_circle_xy(circle, (1.0, 0.0))
    assert TOL.is_allclose(t1, (1.0, 0.0, 0.0))
    assert TOL.is_allclose(t2, (1.0, 0.0, 0.0))


def test_tangent_points_rejects_point_inside_circle():
    circle = ((0.0, 0.0, 0.0), (0.0, 0.0, 1.0)), 1.0
    with pytest.raises(ValueError, match="math domain error"):
        tangent_points_to_circle_xy(circle, (0.5, 0.0))


def test_tangent_points_rejects_circle_center():
    circle = ((0.0, 0.0, 0.0), (0.0, 0.0, 1.0)), 1.0
    with pytest.raises(ZeroDivisionError):
        tangent_points_to_circle_xy(circle, (0.0, 0.0))
