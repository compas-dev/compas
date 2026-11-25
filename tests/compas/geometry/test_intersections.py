from compas.tolerance import TOL
from compas.geometry import intersection_segment_segment
from compas.geometry import intersection_sphere_line
from compas.geometry import intersection_plane_circle
from compas.geometry import intersection_circle_circle_xy


def test_intersection_sphere_line():
    sphere = (3.0, 7.0, 4.0), 10.0
    line = (1.0, 0, 0.5), (2.0, 1.0, 0.5)
    ipt1, ipt2 = intersection_sphere_line(sphere, line)
    assert TOL.is_allclose(ipt1, (11.634, 10.634, 0.500), atol=1e-3)
    assert TOL.is_allclose(ipt2, (-0.634, -1.634, 0.500), atol=1e-3)


def test_intersection_plane_circle():
    plane = (0, 0, 0), (0, 0, 1)
    circle = ((3.0, 7.0, 4.0), (0, 1, 0)), 10.0
    ipt1, ipt2 = intersection_plane_circle(plane, circle)
    assert TOL.is_allclose(ipt1, (-6.165, 7.000, 0.000), atol=1e-3)
    assert TOL.is_allclose(ipt2, (12.165, 7.000, 0.000), atol=1e-3)


def test_intersection_circle_circle_xy():
    circle1 = ((0.0, 0.0, 0.0), (0, 0, 1)), 10.0
    circle2 = ((3.0, 7.0, 0.0), (0, 0, 1)), 10.0
    ipt1, ipt2 = intersection_circle_circle_xy(circle1, circle2)
    assert TOL.is_allclose(ipt1, (9.999, -0.142, 0.000), atol=1e-3)
    assert TOL.is_allclose(ipt2, (-6.999, 7.142, 0.000), atol=1e-3)


def test_intersection_segment_segment_large_coordinates_small_tolerance():
    s1 = (2687403.6546, 1169130.8538, 0.0), (2687403.6428, 1169130.8540, 0.0)
    s2 = (2687403.6408, 1169130.8538, 0.0), (2687403.6509, 1169130.8544, 0.0)

    x1, x2 = intersection_segment_segment(s1, s2, tol=1e-3)

    assert x1 is not None
    assert x2 is not None
    assert TOL.is_allclose(x1, (2687403.64386, 1169130.85398, 0.0), atol=1e-5)
    assert TOL.is_allclose(x2, (2687403.64386, 1169130.85398, 0.0), atol=1e-5)
