from compas.geometry.transformations import translate_points
from compas.geometry.transformations import translate_points_xy
from compas.geometry.transformations import scale_points
from compas.geometry.transformations import scale_points_xy
from compas.geometry.transformations import rotate_points
from compas.geometry.transformations import rotate_points_xy
from compas.geometry.transformations import mirror_vector_vector
from compas.geometry.transformations import mirror_points_point
from compas.geometry.transformations import mirror_points_point_xy
from compas.geometry.transformations import mirror_points_line
from compas.geometry.transformations import mirror_points_line_xy
from compas.geometry.transformations import mirror_points_plane
from compas.geometry.transformations import project_point_plane
from compas.geometry.transformations import project_points_plane
from compas.geometry.transformations import project_point_line
from compas.geometry.transformations import project_point_line_xy
from compas.geometry.transformations import project_points_line
from compas.geometry.transformations import project_points_line_xy
from compas.geometry.transformations import reflect_line_plane
from compas.geometry.transformations import reflect_line_triangle
from compas.geometry.transformations import orient_points

from compas.geometry import intersection_segment_segment_xy
import numpy as np


def test_translate_points():
    assert translate_points([[0, 1, 2]], [3, 4, 5]) == [[3, 5, 7]]


def test_translate_points_xy():
    assert translate_points_xy([[0, 1, 2]], [3, 4, 5]) == [[3, 5, 0.0]]


def test_scale_points():
    assert scale_points([[0, 1, 2]], 5) == [[0, 5, 10]]


def test_scale_points_xy():
    assert scale_points_xy([[0, 1, 2]], 5) == [[0.0, 5.0, 0.0]]


def test_rotate_points():
    assert np.allclose(rotate_points([[0, 1, 2]], 1), [[-0.8414709848078965, 0.5403023058681398, 2.0]])


def test_rotate_points_xy():
    assert np.allclose(rotate_points_xy([[0, 1, 2]], 1), [[-0.8414709848078965, 0.5403023058681398, 0.0]])


def test_mirror_vector_vector():
    assert mirror_vector_vector([0, 1, 2], [3, 4, 5]) == [-84, -111, -138]
    # TODO: is this correct?


def test_mirror_points_point():
    assert mirror_points_point([[0, 1, 2]], [3, 4, 5]) == [[6, 7, 8]]


def test_mirror_points_point_xy():
    assert mirror_points_point_xy([[0, 1, 2]], [3, 4, 5]) == [[6, 7, 0.0]]


def test_mirror_points_line():
    assert np.allclose(mirror_points_line([[0, 1, 2]], ([3, 4, 5], [6, 7, 8.8])), [[0.281134401972873, 1.281134401972873, 1.5561035758323052]])


def test_mirror_points_line_xy():
    assert mirror_points_line_xy([[0, 2.5, 2]], ([3, 4, 5], [6, 7, 8.8])) == [[0.75, 1.75, 0.0]]


def test_mirror_points_plane():
    assert np.allclose(mirror_points_plane([[0, 2.5, 2]], ([3, 4, 5], [6, 7, 8.8])), [[4.055651317409505, 7.231593203644422, 7.948288598867276]])


def test_project_point_plane():
    assert np.allclose(project_point_plane([0, 2.5, 2], ([3, 4, 5], [6, 7, 8.8])), [2.0278256587047525, 4.865796601822211, 4.974144299433638])


def test_project_points_plane():
    assert np.allclose(project_points_plane([[0, 2.5, 2]], ([3, 4, 5], [6, 7, 8.8])), [[2.0278256587047525, 4.865796601822211, 4.974144299433638]])


def test_project_point_line():
    assert np.allclose(project_point_line([0, 1, 2], ([3, 4, 5], [6, 7, 8.8])), [0.281134401972873, 1.281134401972873, 1.5561035758323052])


def test_project_point_line_xy():
    assert project_point_line_xy([0, 1, 2], ([3, 4, 5], [6, 7, 8.8])) == [0.0, 1.0, 0.0]
    # TODO: is this correct?


def test_project_points_line():
    assert np.allclose(project_points_line([[0, 1, 2]], ([3, 4, 5], [6, 7, 8.8])), [[0.281134401972873, 1.281134401972873, 1.5561035758323052]])


def test_project_points_line_xy():
    assert project_points_line_xy([[0, 1, 2]], ([3, 4, 5], [6, 7, 8.8])) == [[0.0, 1.0, 0.0]]
    # TODO: is this correct?


def test_reflect_line_plane():
    plane = [0, 0, 0], [0, 1, 0]
    line = [-1, 1, 0], [-0.5, 0.5, 0]
    assert reflect_line_plane(line, plane) == ([0.0, 0.0, 0.0], [1.0, 1.0, 0.0])


def test_reflect_line_triangle():
    triangle = [1.0, 0, 0], [-1.0, 0, 0], [0, 0, 1.0]
    line = [-1, 1, 0], [-0.5, 0.5, 0]
    assert reflect_line_triangle(line, triangle) == ([0.0, 0.0, 0], [1.0, 1.0, 0])


def test_orient_points():
    refplane = ([0.57735, 0.57735, 0.57735], [1.0, 1.0, 1.0])
    tarplane = ([0.0, 0.0, 0.0], [0.0, 0.0, 1.0])

    points = [
        [0.288675, 0.288675, 1.1547],
        [0.866025, 0.866025, 0.0],
        [1.077350, 0.077350, 0.57735],
        [0.077350, 1.077350, 0.57735]
    ]

    points = orient_points(points, refplane, tarplane)

    ab = points[0], points[1]
    cd = points[2], points[3]

    point = intersection_segment_segment_xy(ab, cd)

    points = orient_points([point], tarplane, refplane)

    assert points[0] == [0.57735, 0.57735, 0.57735]
