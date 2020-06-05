import pytest

# from compas.geometry import homogenize
# from compas.geometry import dehomogenize
from compas.geometry import Rotation
from compas.geometry import Translation
from compas.geometry import allclose
from compas.geometry import intersection_segment_segment_xy
from compas.geometry import mirror_points_line
from compas.geometry import mirror_points_line_xy
from compas.geometry import mirror_points_plane
from compas.geometry import mirror_points_point
from compas.geometry import mirror_points_point_xy
from compas.geometry import mirror_vector_vector
from compas.geometry import orient_points
from compas.geometry import project_point_line
from compas.geometry import project_point_line_xy
from compas.geometry import project_point_plane
from compas.geometry import project_points_line
from compas.geometry import project_points_line_xy
from compas.geometry import project_points_plane
from compas.geometry import reflect_line_plane
from compas.geometry import reflect_line_triangle
from compas.geometry import rotate_points
from compas.geometry import rotate_points_xy
from compas.geometry import scale_points
from compas.geometry import scale_points_xy
from compas.geometry import transform_points
from compas.geometry import transform_vectors
from compas.geometry import translate_points
from compas.geometry import translate_points_xy


@pytest.fixture
def T():
    return Translation.from_vector([1, 2, 3])


@pytest.fixture
def R():
    return Rotation.from_euler_angles([90, 0, 0])


def test_transform_points(T):
    assert transform_points([[0, 0, 1], [1, 0, 0]], T) == [[1.0, 2.0, 4.0], [2.0, 2.0, 3.0]]


def test_transform_vectors(R):
    assert transform_vectors([[1, 2, 3], [5, 6, 7]], R) == [[1.0, -3.5781372230600135, 0.44377247881360526], [5.0, -8.946418341978926, 2.227464668699156]]


# def test_homogenize():
#     assert homogenize([[1, 2, 3]], 0.5) == [[0.5, 1.0, 1.5, 0.5]]


# def test_dehomogenize():
#     assert dehomogenize([[0.5, 1.0, 1.5, 0.5]]) == [[1, 2, 3]]


# def test_local_axes():
#     pass


def test_translate_points():
    assert translate_points([[0, 1, 2]], [3, 4, 5]) == [[3, 5, 7]]


def test_translate_points_xy():
    assert translate_points_xy([[0, 1, 2]], [3, 4, 5]) == [[3, 5, 0.0]]


def test_scale_points():
    assert scale_points([[0, 1, 2]], 5) == [[0, 5, 10]]


def test_scale_points_xy():
    assert scale_points_xy([[0, 1, 2]], 5) == [[0.0, 5.0, 0.0]]


def test_rotate_points():
    assert allclose(rotate_points([[0, 1, 2]], 1), [[-0.8414709848078965, 0.5403023058681398, 2.0]])


def test_rotate_points_xy():
    assert allclose(rotate_points_xy([[0, 1, 2]], 1), [[-0.8414709848078965, 0.5403023058681398, 0.0]])


def test_mirror_vector_vector():
    assert mirror_vector_vector([0, 1, 2], [3, 4, 5]) == [-84, -111, -138]
    # TODO: is this correct?


def test_mirror_points_point():
    assert mirror_points_point([[0, 1, 2]], [3, 4, 5]) == [[6, 7, 8]]


def test_mirror_points_point_xy():
    assert mirror_points_point_xy([[0, 1, 2]], [3, 4, 5]) == [[6, 7, 0.0]]


def test_mirror_points_line():
    assert allclose(mirror_points_line([[1.0, 0.0, 0.0]], ([0.0, 0.0, 0.0], [0.0, 1.0, 0.0])), [[-1.0, 0.0, 0.0]])


def test_mirror_points_line_xy():
    assert allclose(mirror_points_line_xy([[1.0, 0.0, 0.0]], ([0.0, 0.0, 0.0], [0.0, 1.0, 0.0])), [[-1.0, 0.0, 0.0]])


def test_mirror_points_plane():
    assert allclose(mirror_points_plane([[0, 2.5, 2]], ([3, 4, 5], [6, 7, 8.8])), [[4.055651317409505, 7.231593203644422, 7.948288598867276]])


def test_project_point_plane():
    assert allclose(project_point_plane([0, 2.5, 2], ([3, 4, 5], [6, 7, 8.8])), [2.0278256587047525, 4.865796601822211, 4.974144299433638])


def test_project_points_plane():
    assert allclose(project_points_plane([[0, 2.5, 2]], ([3, 4, 5], [6, 7, 8.8])), [[2.0278256587047525, 4.865796601822211, 4.974144299433638]])


def test_project_point_line():
    assert allclose(project_point_line([0, 1, 2], ([3, 4, 5], [6, 7, 8.8])), [0.281134401972873, 1.281134401972873, 1.5561035758323052])


def test_project_point_line_xy():
    assert project_point_line_xy([0, 1, 2], ([3, 4, 5], [6, 7, 8.8])) == [0.0, 1.0, 0.0]
    # TODO: is this correct?


def test_project_points_line():
    assert allclose(project_points_line([[0, 1, 2]], ([3, 4, 5], [6, 7, 8.8])), [[0.281134401972873, 1.281134401972873, 1.5561035758323052]])


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

    assert allclose(points[0], [0.57735, 0.57735, 0.57735])
