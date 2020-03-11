import pytest

from compas.geometry import matrix_inverse
from compas.geometry import matrix_determinant
from compas.geometry import decompose_matrix
from compas.geometry import compose_matrix

from compas.geometry import identity_matrix
from compas.geometry import matrix_from_frame
from compas.geometry import matrix_from_euler_angles
from compas.geometry import matrix_from_axis_and_angle
from compas.geometry import matrix_from_axis_angle_vector
from compas.geometry import matrix_from_basis_vectors
from compas.geometry import matrix_from_translation
from compas.geometry import matrix_from_orthogonal_projection
from compas.geometry import matrix_from_parallel_projection
from compas.geometry import matrix_from_perspective_projection
from compas.geometry import matrix_from_perspective_entries
from compas.geometry import matrix_from_shear_entries
from compas.geometry import matrix_from_shear
from compas.geometry import matrix_from_scale_factors
from compas.geometry import matrix_from_quaternion
from compas.geometry import euler_angles_from_matrix
from compas.geometry import euler_angles_from_quaternion
from compas.geometry import axis_and_angle_from_matrix
from compas.geometry import axis_angle_vector_from_matrix
from compas.geometry import axis_angle_from_quaternion
from compas.geometry import quaternion_from_matrix
from compas.geometry import quaternion_from_euler_angles
from compas.geometry import quaternion_from_axis_angle
from compas.geometry import basis_vectors_from_matrix
from compas.geometry import translation_from_matrix

from compas.geometry import Translation
from compas.geometry import Rotation

import math

from compas.geometry import Frame
from compas.geometry import allclose
from compas.geometry import normalize_vector
from compas.geometry import cross_vectors
import numpy as np


@pytest.fixture
def T():
    return Translation([1, 2, 3])


@pytest.fixture
def R():
    return Rotation.from_euler_angles([90, 0, 0])


def test_matrix_determinant(R, T):
    assert matrix_determinant(R.matrix) == 1
    assert matrix_determinant(T.matrix) == 1


def test_matrix_inverse(R, T):
    assert matrix_inverse(R.matrix) == [
        [1.0, -0.0, 0.0, -0.0], [-0.0, -0.4480736161291701, 0.8939966636005579, 0.0], [0.0, -0.8939966636005579, -0.4480736161291701, -0.0], [-0.0, 0.0, -0.0, 1.0]]
    assert matrix_inverse(T.matrix) == [
        [1.0, -0.0, 0.0, -1.0], [-0.0, 1.0, -0.0, -2.0], [0.0, -0.0, 1.0, -3.0], [-0.0, 0.0, -0.0, 1.0]]


def test_decompose_matrix(R, T):
    assert decompose_matrix(R.matrix) == ([1.0, 1.0, 1.0], [0.0, 0.0, 0.0], [2.035405699485789, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 1.0])
    assert decompose_matrix(T.matrix) == ([1.0, 1.0, 1.0], [0.0, 0.0, 0.0], [0.0, -0.0, 0.0], [1.0, 2.0, 3.0], [0.0, 0.0, 0.0, 1.0])


def test_compose_matrix():
    M = compose_matrix([1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12], [0, 1, 2, 3])
    assert M == [
        [0.0034886706291650366, -0.01961312282449104, -0.40764893516767803, 0.2631578947368421],
        [-0.0015779803562060576, -0.034677956457534555, -0.1506311173884861, 0.2894736842105263],
        [-0.02603574333219426, -0.2133170820431009, -0.44447632662352016, 0.3157894736842105],
        [-0.05364946702059457, -0.4613121205437364, -1.0395837706355264, 1.0]]


def test_identity_matrix():
    assert identity_matrix(4) == [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]]


def test_matrix_from_frame():
    f = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
    T = matrix_from_frame(f)
    t = [[0.6807833515407016, -0.6687681911461376, -0.29880283595731283, 1.0],
         [0.6807833515407016, 0.7282315441900513, -0.0788216106888398, 1.0],
         [0.2703110366411609, -0.14975955581430114, 0.9510541619236438, 1.0],
         [0.0, 0.0, 0.0, 1.0]]
    assert np.allclose(T, t)


def test_matrix_from_euler_angles():
    ea1 = 1.4, 0.5, 2.3
    args = True, 'xyz'
    R = matrix_from_euler_angles(ea1, *args)
    r = [[-0.5847122176808724, -0.4415273357486694, 0.6805624396639868, 0.0],
         [0.6544178905170501, 0.23906322244658262, 0.7173464994301357, 0.0],
         [-0.479425538604203, 0.8648134986574489, 0.14916020070358058, 0.0],
         [0.0, 0.0, 0.0, 1.0]]
    assert np.allclose(R, r)


def test_euler_angles_from_matrix():
    ea1 = 1.4, 0.5, 2.3
    args = True, 'xyz'
    R = matrix_from_euler_angles(ea1, *args)
    ea2 = euler_angles_from_matrix(R, *args)
    assert np.allclose(ea1, ea2)


def test_matrix_from_axis_angle_vector():
    axis1 = normalize_vector([-0.043, -0.254, 0.617])
    angle1 = 0.1
    R = matrix_from_axis_and_angle(axis1, angle1)
    r = [[0.9950248278789664, -0.09200371122722178, -0.03822183963195913, 0.0],
         [0.09224781823368366, 0.9957251324831573, 0.004669108322156158, 0.0],
         [0.037628871037522216, -0.008171760019527692, 0.9992583701939277, 0.0],
         [0.0, 0.0, 0.0, 1.0]]
    assert np.allclose(R, r)


def test_matrix_from_basis_vectors():
    xaxis = [0.68, 0.68, 0.27]
    yaxis = [-0.67, 0.73, -0.15]
    R = matrix_from_basis_vectors(xaxis, yaxis)
    r = [[0.6807833515407016, -0.6687681611113407, -0.29880282253789103, 0.0],
         [0.6807833515407016, 0.7282315114847181, -0.07882160714891209, 0.0],
         [0.2703110366411609, -0.14975954908850603, 0.9510541192112079, 0.0],
         [0.0, 0.0, 0.0, 1.0]]
    assert np.allclose(R, r)


def test_matrix_from_translation():
    T = matrix_from_translation([1, 2, 3])
    t = [[1.0, 0.0, 0.0, 1.0], [0.0, 1.0, 0.0, 2.0], [0.0, 0.0, 1.0, 3.0], [0.0, 0.0, 0.0, 1.0]]
    assert np.allclose(T, t)


def test_matrix_from_orthogonal_projection():
    point = [0, 0, 0]
    normal = [0, 0, 1]
    P = matrix_from_orthogonal_projection(point, normal)
    p = [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 1.0]]
    assert np.allclose(P, p)


def test_matrix_from_parallel_projection():
    point = [0, 0, 0]
    normal = [0, 0, 1]
    direction = [1, 1, 1]
    P = matrix_from_parallel_projection(point, normal, direction)
    p = [[1.0, 0.0, -1.0, 0.0], [0.0, 1.0, -1.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 1.0]]
    assert np.allclose(P, p)


def test_matrix_from_perspective_projection():
    point = [0, 0, 0]
    normal = [0, 0, 1]
    perspective = [1, 1, 0]
    P = matrix_from_perspective_projection(point, normal, perspective)
    p = [[0.0, 0.0, -1.0, 0.0], [0.0, 0.0, -1.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, -1.0, 0.0]]
    assert np.allclose(P, p)


def test_matrix_from_perspective_entries():
    assert matrix_from_perspective_entries([2, 3, 4, 5]) == [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [2.0, 3.0, 4.0, 5.0]]


def test_matrix_from_shear_entries():
    assert matrix_from_shear_entries([2, 3, 4]) == [[1.0, 2.0, 3.0, 0.0], [0.0, 1.0, 4.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]]


def test_matrix_from_shear():
    angle = 0.1
    direction = [0.1, 0.2, 0.3]
    point = [4, 3, 1]
    normal = cross_vectors(direction, [1, 0.3, -0.1])
    S = matrix_from_shear(angle, direction, point, normal)
    s = [[0.992033620789569, 0.02245070504757821, -0.012311676961575148, -0.023174921339435575],
         [-0.015932758420861955, 1.0449014100951564, -0.024623353923150296, -0.04634984267887115],
         [-0.023899137631292932, 0.06735211514273462, 0.9630649691152746, -0.0695247640183067],
         [0.0, 0.0, 0.0, 1.0]]
    assert np.allclose(S, s)


def test_matrix_from_scale_factors():
    Sc = matrix_from_scale_factors([1, 2, 3])
    assert Sc == [[1.0, 0.0, 0.0, 0.0], [0.0, 2.0, 0.0, 0.0], [0.0, 0.0, 3.0, 0.0], [0.0, 0.0, 0.0, 1.0]]


def test_matrix_from_quaternion():
    q1 = [0.945, -0.021, -0.125, 0.303]
    R = matrix_from_quaternion(q1)
    r = [[0.7853252073134178, -0.5669097811969227, -0.2487521230892197, 0.0],
         [0.5774003396942752, 0.8156659006893796, -0.0360275751823359, 0.0],
         [0.22332300929163754, -0.11533619742231993, 0.9678968927964832, 0.0],
         [0.0, 0.0, 0.0, 1.0]]
    assert np.allclose(R, r)


def test_euler_angles_from_quaternion():
    axis = [1.0, 0.0, 0.0]
    angle = math.pi/2
    q = quaternion_from_axis_angle(axis, angle)
    assert np.allclose(euler_angles_from_quaternion(q), [math.pi/2, 0, 0])


def test_axis_and_angle_from_matrix():
    axis1 = normalize_vector([-0.043, -0.254, 0.617])
    angle1 = 0.1
    R = matrix_from_axis_and_angle(axis1, angle1)
    axis2, angle2 = axis_and_angle_from_matrix(R)
    assert allclose(axis1, axis2)
    assert allclose([angle1], [angle2])


def test_axis_angle_vector_from_matrix():
    aav1 = [-0.043, -0.254, 0.617]
    R = matrix_from_axis_angle_vector(aav1)
    aav2 = axis_angle_vector_from_matrix(R)
    assert allclose(aav1, aav2)


def test_axis_angle_from_quaternion():
    q = [1., 1., 0., 0.]
    axis, angle = axis_angle_from_quaternion(q)
    assert allclose(axis, [1., 0., 0.])
    assert allclose([angle], [math.pi/2], 1e-6)


def test_quaternion_from_matrix():
    q1 = [0.945, -0.021, -0.125, 0.303]
    R = matrix_from_quaternion(q1)
    q2 = quaternion_from_matrix(R)
    assert allclose(q1, q2, tol=1e-03)


def test_quaternion_from_euler_angles():
    axis = [1.0, 0.0, 0.0]
    angle = math.pi/2
    assert np.allclose(quaternion_from_axis_angle(axis, angle), quaternion_from_euler_angles([math.pi/2, 0, 0]))


def test_quaternion_from_axis_angle():
    axis = [1.0, 0.0, 0.0]
    angle = math.pi/2
    q = quaternion_from_axis_angle(axis, angle)
    assert allclose(q, [math.sqrt(2)/2, math.sqrt(2)/2, 0, 0])


def test_basis_vectors_from_matrix():
    f = Frame([0, 0, 0], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
    R = matrix_from_frame(f)
    xaxis, yaxis = basis_vectors_from_matrix(R)
    assert np.allclose(xaxis, [0.6807833515407016, 0.6807833515407016, 0.2703110366411609])
    assert np.allclose(yaxis, [-0.6687681911461376, 0.7282315441900513, -0.14975955581430114])


def test_translation_from_matrix():
    t = [1, 2, 3]
    T = matrix_from_translation(t)
    assert translation_from_matrix(T) == t
