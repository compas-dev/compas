from compas.geometry import Frame
from compas.geometry import Projection
from compas.geometry import Reflection
from compas.geometry import Rotation
from compas.geometry import Scale
from compas.geometry import Shear
from compas.geometry import Transformation
from compas.geometry import Translation
from compas.geometry import Vector
from compas.tolerance import TOL


def test_transformation():
    T = Transformation()
    assert T.matrix == [
        [1.0, 0.0, 0.0, 0.0],
        [0.0, 1.0, 0.0, 0.0],
        [0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 1.0],
    ]


def test_repr_can_reconstruct_base_transformation():
    transformation = Transformation.from_list(range(16))
    reconstructed = eval(repr(transformation), {"Transformation": Transformation})
    assert reconstructed == transformation


def test_alternative_constructors_preserve_subclasses():
    class CustomTransformation(Transformation):
        pass

    class CustomRotation(Rotation):
        pass

    class CustomTranslation(Translation):
        pass

    class CustomScale(Scale):
        pass

    class CustomShear(Shear):
        pass

    class CustomProjection(Projection):
        pass

    class CustomReflection(Reflection):
        pass

    assert type(CustomTransformation.from_list(range(16))) is CustomTransformation
    assert type(CustomRotation.from_axis_and_angle((0.0, 0.0, 1.0), 0.5)) is CustomRotation
    assert type(CustomRotation.from_euler_angles((0.1, 0.2, 0.3))) is CustomRotation
    assert type(CustomTranslation.from_vector((1.0, 2.0, 3.0))) is CustomTranslation
    assert type(CustomScale.from_factors((1.0, 2.0, 3.0))) is CustomScale
    assert type(CustomShear.from_entries((0.1, 0.2, 0.3))) is CustomShear
    assert type(CustomShear.from_angle_direction_plane(0.1, (1.0, 0.0, 0.0), ((0.0, 0.0, 0.0), (0.0, 0.0, 1.0)))) is CustomShear
    plane = (0.0, 0.0, 0.0), (0.0, 0.0, 1.0)
    assert type(CustomProjection.from_plane(plane)) is CustomProjection
    assert type(CustomProjection.from_plane_and_direction(plane, (0.0, 0.0, 1.0))) is CustomProjection
    assert type(CustomProjection.from_plane_and_point(plane, (0.0, 0.0, 1.0))) is CustomProjection
    assert type(CustomProjection.from_entries((0.1, 0.2, 0.3, 1.0))) is CustomProjection
    assert type(CustomReflection.from_plane(plane)) is CustomReflection
    assert type(CustomReflection.from_frame(Frame.worldXY())) is CustomReflection


def test_transformation_subpackage_exports_root_classes():
    from compas.geometry.transformations import Projection
    from compas.geometry.transformations import Reflection
    from compas.geometry.transformations import Rotation as PackagedRotation
    from compas.geometry.transformations import Scale as PackagedScale
    from compas.geometry.transformations import Shear
    from compas.geometry.transformations import Transformation as PackagedTransformation
    from compas.geometry.transformations import Translation as PackagedTranslation

    from compas.geometry import Projection as RootProjection
    from compas.geometry import Reflection as RootReflection
    from compas.geometry import Shear as RootShear

    assert PackagedTransformation is Transformation
    assert PackagedTranslation is Translation
    assert PackagedRotation is Rotation
    assert PackagedScale is Scale
    assert Projection is RootProjection
    assert Reflection is RootReflection
    assert Shear is RootShear


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
    assert T.matrix == [
        [1.0, 0.0, 0.0, 3.0],
        [0.0, 1.0, 0.0, 4.0],
        [0.0, 0.0, 1.0, 5.0],
        [0.0, 0.0, 0.0, 1.0],
    ]


def test_from_euler_angles():
    angle1 = [-2.142, 1.141, -0.142]
    R = Transformation.from_euler_angles(angle1, point=[0.25, -0.25, 0.25])
    matrix = [
        [0.41249169135312663, -0.8335562904208867, -0.3674704277413451, 0.25],
        [-0.05897071585157175, -0.4269749553355485, 0.9023385407861949, -0.25],
        [-0.9090506362335324, -0.35053715668381935, -0.22527903264048646, 0.25],
        [0.0, 0.0, 0.0, 1.0],
    ]
    assert TOL.is_allclose(R.matrix, matrix)


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
    matrix = [
        [0.41249169135312663, -0.8335562904208867, -0.3674704277413451, 0.0],
        [-0.05897071585157175, -0.4269749553355485, 0.9023385407861949, 0.0],
        [-0.9090506362335324, -0.35053715668381935, -0.22527903264048646, 0.0],
        [0.0, 0.0, 0.0, 1.0],
    ]
    assert TOL.is_allclose(R.matrix, matrix)


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
    assert TOL.is_allclose(x, Vector(0.41249169135312663, -0.05897071585157175, -0.9090506362335324))
    assert TOL.is_allclose(y, Vector(-0.8335562904208867, -0.4269749553355485, -0.35053715668381935))


def test_list():
    T = Transformation()
    assert T.list == [
        1.0,
        0.0,
        0.0,
        0.0,
        0.0,
        1.0,
        0.0,
        0.0,
        0.0,
        0.0,
        1.0,
        0.0,
        0.0,
        0.0,
        0.0,
        1.0,
    ]


def test_concatenated():
    trans1 = [1, 2, 3]
    angle1 = [-2.142, 1.141, -0.142]
    T1 = Translation.from_vector(trans1)
    R1 = Rotation.from_euler_angles(angle1)
    M1 = T1.concatenated(R1)
    assert TOL.is_allclose(M1, T1 * R1)


def test___repr__():
    point = [1, 2, 3]
    axis = [-2.142, 1.141, -0.142]
    angle = 0.7854
    R = Rotation.from_axis_and_angle(axis, angle, point=point)
    assert R == eval(repr(R))


def test___str__():
    s = (
        "[[    0.9345,   -0.0798,    0.3469,   -0.8157],\n"
        + " [   -0.1624,    0.7716,    0.6150,   -1.2258],\n"
        + " [   -0.3168,   -0.6311,    0.7081,    2.4546],\n"
        + " [    0.0000,    0.0000,    0.0000,    1.0000]]\n"
    )
    point = [1, 2, 3]
    axis = [-2.142, 1.141, -0.142]
    angle = 0.7854
    R = Rotation.from_axis_and_angle(axis, angle, point=point)
    assert s == str(R)


def test___eq__():
    i1 = Transformation()
    i2 = Transformation()
    t = Translation.from_vector([1, 0, 0])
    assert i1 == i2
    assert not (i1 != i2)
    assert i1 != t
    assert not (i1 == t)
