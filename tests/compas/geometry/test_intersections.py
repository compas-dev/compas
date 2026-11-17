from compas.tolerance import TOL
from compas.geometry import distance_point_point
from compas.geometry import intersection_line_line_xy
from compas.geometry import intersection_sphere_line
from compas.geometry import intersection_plane_circle
from compas.geometry import intersection_circle_circle_xy


def test_intersection_line_line_xy_large_coordinates():
    line_a = ((2687071.524742563, 1221749.0753872169, 0.0), (2687069.1419153824, 1221750.3200979184, 0.0))
    line_b = ((2687069.1328718644, 1221750.3261498366, 0.0), (2687069.006655604, 1221750.4317925072, 0.0))

    intersection = intersection_line_line_xy(line_a, line_b, tol=1e-7)

    assert distance_point_point(intersection, (2687069.137092316, 1221750.32261733, 0.0)) < 1e-7


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
