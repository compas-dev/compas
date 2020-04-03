from compas.geometry import allclose
from compas.geometry import tangent_points_to_circle_xy


def test_tangent_points_to_circle_xy():
    circle = (0, 0, 0), 1.
    point = (2, 4, 0)
    t1, t2 = tangent_points_to_circle_xy(circle, point)
    assert allclose(t1, (-0.772, 0.636, 0.000), tol=1e-3)
    assert allclose(t2, (0.972, -0.236, 0.000), tol=1e-3)