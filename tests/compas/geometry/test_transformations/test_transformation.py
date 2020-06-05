from compas.geometry import Frame
from compas.geometry import Rotation
from compas.geometry import Scale
from compas.geometry import Transformation
from compas.geometry import Translation
from compas.geometry import Vector
from compas.geometry import allclose


def test_transformation():
    T = Transformation()
    assert T.matrix == [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]]


def test_copy():
    T = Transformation()
    assert T.matrix == T.copy().matrix


def test_from_matrix():
    T = Transformation()
    matrix = T.matrix
    assert Transformation.from_matrix(matrix).matrix == matrix


def test_from_list():
    numbers = [1, 0, 0, 3, 0, 1, 0, 4, 0, 0, 1, 5, 0, 0, 0, 1]
    T = Transformation.from_list(numbers)
    assert T.matrix == [[1.0, 0.0, 0.0, 3.0], [0.0, 1.0, 0.0, 4.0], [0.0, 0.0, 1.0, 5.0], [0.0, 0.0, 0.0, 1.0]]


def test_from_frame():
    f1 = Frame([2, 2, 2], [0.12, 0.58, 0.81], [-0.80, 0.53, -0.26])
    f2 = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
    T = Transformation.from_frame_to_frame(f1, f2)
    f1.transform(T)
    assert f1 == f2


def test_inverse():
    f = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
    T = Transformation.from_frame(f)
    identity = T * T.inverse()
    assert Transformation() == identity


def test_decomposed():
    trans1 = [1, 2, 3]
    angle1 = [-2.142, 1.141, -0.142]
    scale1 = [0.123, 2, 0.5]
    T1 = Translation.from_vector(trans1)
    R1 = Rotation.from_euler_angles(angle1)
    S1 = Scale.from_factors(scale1)
    M = (T1 * R1) * S1
    Sc, Sh, R, T, P = M.decomposed()
    assert S1 == Sc
    assert R1 == R
    assert T1 == T


def test_rotation():
    angle1 = [-2.142, 1.141, -0.142]
    R = Rotation.from_euler_angles(angle1)
    matrix = [[0.41249169135312663, -0.8335562904208867, -0.3674704277413451, 0.0],
              [-0.05897071585157175, -0.4269749553355485, 0.9023385407861949, 0.0],
              [-0.9090506362335324, -0.35053715668381935, -0.22527903264048646, 0.0],
              [0.0, 0.0, 0.0, 1.0]]
    assert allclose(R.matrix, matrix)


def test_rotation_property():
    T = Transformation()
    R = T.rotation
    assert R.matrix == [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]


def test_translation():
    trans1 = [1, 2, 3]
    T1 = Translation.from_vector(trans1)
    assert T1.translation_vector == trans1


def test_basis_vectors():
    trans1 = [1, 2, 3]
    angle1 = [-2.142, 1.141, -0.142]
    scale1 = [0.123, 2, 0.5]
    T1 = Translation.from_vector(trans1)
    R1 = Rotation.from_euler_angles(angle1)
    S1 = Scale.from_factors(scale1)
    M = (T1 * R1) * S1
    x, y = M.basis_vectors
    assert allclose(x, Vector(0.41249169135312663, -0.05897071585157175, -0.9090506362335324))
    assert allclose(y, Vector(-0.8335562904208867, -0.4269749553355485, -0.35053715668381935))


def test_list():
    T = Transformation()
    assert T.list == [1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0]


def concatenate():
    trans1 = [1, 2, 3]
    angle1 = [-2.142, 1.141, -0.142]
    T1 = Translation.from_vector(trans1)
    R1 = Rotation.from_euler_angles(angle1)
    M1 = T1.concatenate(R1)
    assert allclose(M1, T1 * R1)
