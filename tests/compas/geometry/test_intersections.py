from compas.geometry import allclose
from compas.geometry import intersection_sphere_line
from compas.geometry import intersection_plane_circle


def test_intersection_sphere_line():
    sphere = (3.0, 7.0, 4.0), 10.0
    line = (1.0, 0, 0.5), (2.0, 1.0, 0.5)
    ipt1, ipt2 = intersection_sphere_line(sphere, line)
    assert allclose(ipt1, (11.634, 10.634, 0.500), tol=1e-3)
    assert allclose(ipt2, (-0.634, -1.634, 0.500), tol=1e-3)


def test_intersection_plane_circle():
    plane = (0, 0, 0), (0, 0, 1)
    circle = ((3.0, 7.0, 4.0), (0, 1, 0)), 10.0
    ipt1, ipt2 = intersection_plane_circle(plane, circle)
    assert allclose(ipt1, (-6.165, 7.000, 0.000), tol=1e-3)
    assert allclose(ipt2, (12.165, 7.000, 0.000), tol=1e-3)
