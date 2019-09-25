import pytest

from compas.geometry.transformations import transform_points
from compas.geometry.transformations import transform_vectors
from compas.geometry.transformations import homogenize
from compas.geometry.transformations import dehomogenize
from compas.geometry.transformations import determinant
from compas.geometry.transformations import inverse
from compas.geometry.transformations import decompose_matrix
from compas.geometry.transformations import compose_matrix

from compas.geometry.transformations import Translation
from compas.geometry.transformations import Rotation


@pytest.fixture
def T():
    return Translation([1, 2, 3])


@pytest.fixture
def R():
    return Rotation.from_euler_angles([90, 0, 0])


def test_transform_points(T):
    assert transform_points([[0, 0, 1], [1, 0, 0]], T) == [[1.0, 2.0, 4.0], [2.0, 2.0, 3.0]]


def test_transform_vectors(R):
    assert transform_vectors([[1, 2, 3], [5, 6, 7]], R) == [[1.0, -3.5781372230600135, 0.44377247881360526], [5.0, -8.946418341978926, 2.227464668699156]]


def test_homogenize():
    assert homogenize([[1, 2, 3]], 0.5) == [[0.5, 1.0, 1.5, 0.5]]


def test_dehomogenize():
    assert dehomogenize([[0.5, 1.0, 1.5, 0.5]]) == [[1, 2, 3]]


def test_local_axes():
    pass


def test_determinant(R, T):
    assert determinant(R.matrix) == 1
    assert determinant(T.matrix) == 1


def test_inverse(R, T):
    assert inverse(R.matrix) == [[1.0, -0.0, 0.0, -0.0], [-0.0, -0.4480736161291701, 0.8939966636005579, 0.0], [0.0, -0.8939966636005579, -0.4480736161291701, -0.0], [-0.0, 0.0, -0.0, 1.0]]
    assert inverse(T.matrix) == [[1.0, -0.0, 0.0, -1.0], [-0.0, 1.0, -0.0, -2.0], [0.0, -0.0, 1.0, -3.0], [-0.0, 0.0, -0.0, 1.0]]


def test_decompose_matrix(R, T):
    assert decompose_matrix(R.matrix) == ([1.0, 1.0, 1.0], [0.0, 0.0, 0.0], [2.035405699485789, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 1.0])
    assert decompose_matrix(T.matrix) == ([1.0, 1.0, 1.0], [0.0, 0.0, 0.0], [0.0, -0.0, 0.0], [1.0, 2.0, 3.0], [0.0, 0.0, 0.0, 1.0])


def test_compose_matrix():
    M = compose_matrix([1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12], [0, 1, 2, 3])
    assert M == [[0.0034886706291650366, -0.01961312282449104, -0.40764893516767803, 0.2631578947368421], [-0.0015779803562060576, -0.034677956457534555, -0.1506311173884861, 0.2894736842105263], [-0.02603574333219426, -0.2133170820431009, -0.44447632662352016, 0.3157894736842105], [-0.05364946702059457, -0.4613121205437364, -1.0395837706355264, 1.0]]