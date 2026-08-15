from copy import deepcopy
from math import acos
from math import asin
from math import atan2
from math import cos
from math import fabs
from math import pi
from math import sin
from math import sqrt
from math import tan
from typing import Optional
from typing import Sequence

from compas._typing import CoordinatesType
from compas._typing import CoordinateType
from compas._typing import FloatSequenceType
from compas.tolerance import TOL

from .matrices import matrix_determinant
from .matrices import matrix_inverse
from .matrices import multiply_matrices
from .matrices import multiply_matrix_vector
from .matrices import transpose_matrix
from .vectors import allclose
from .vectors import cross_vectors
from .vectors import dot_vectors
from .vectors import length_vector
from .vectors import norm_vector
from .vectors import normalize_vector
from .vectors import scale_vector
from .vectors import subtract_vectors

_SPEC2TUPLE = {
    "sxyz": (0, 0, 0, 0),
    "sxyx": (0, 0, 1, 0),
    "sxzy": (0, 1, 0, 0),
    "sxzx": (0, 1, 1, 0),
    "syzx": (1, 0, 0, 0),
    "syzy": (1, 0, 1, 0),
    "syxz": (1, 1, 0, 0),
    "syxy": (1, 1, 1, 0),
    "szxy": (2, 0, 0, 0),
    "szxz": (2, 0, 1, 0),
    "szyx": (2, 1, 0, 0),
    "szyz": (2, 1, 1, 0),
    "rzyx": (0, 0, 0, 1),
    "rxyx": (0, 0, 1, 1),
    "ryzx": (0, 1, 0, 1),
    "rxzx": (0, 1, 1, 1),
    "rxzy": (1, 0, 0, 1),
    "ryzy": (1, 0, 1, 1),
    "rzxy": (1, 1, 0, 1),
    "ryxy": (1, 1, 1, 1),
    "ryxz": (2, 0, 0, 1),
    "rzxz": (2, 0, 1, 1),
    "rxyz": (2, 1, 0, 1),
    "rzyz": (2, 1, 1, 1),
}
"""used for Euler angles: to map rotation type and axes to tuples of inner axis, parity, repetition, frame"""

_NEXT_SPEC = [1, 2, 0, 1]
# =============================================================================
# 4x4 matrices
# =============================================================================


def decompose_matrix(
    M: CoordinatesType,
) -> tuple[list[float], list[float], list[float], list[float], list[float]]:
    """Calculates the components of rotation, translation, scale, shear, and
    perspective of a given transformation matrix `M`.[^decompose-matrix-slabaugh]

    Parameters
    ----------
    M
        The square matrix of any dimension.

    Raises
    ------
    ValueError
        If matrix is singular or degenerative.

    Returns
    -------
    tuple[list[float], list[float], list[float], list[float], list[float]]
        The scale factors, shear factors, Euler angles, translation values,
        and perspective entries, in that order.

    See Also
    --------
    [`compose_matrix`][compas.linalg.compose_matrix]

    Examples
    --------
    >>> trans1 = [1, 2, 3]
    >>> angle1 = [-2.142, 1.141, -0.142]
    >>> scale1 = [0.123, 2, 0.5]
    >>> T = matrix_from_translation(trans1)
    >>> R = matrix_from_euler_angles(angle1)
    >>> S = matrix_from_scale_factors(scale1)
    >>> M = multiply_matrices(multiply_matrices(T, R), S)
    >>> # M = compose_matrix(scale1, None, angle1, trans1, None)
    >>> scale2, shear2, angle2, trans2, persp2 = decompose_matrix(M)
    >>> allclose(scale1, scale2)
    True
    >>> allclose(angle1, angle2)
    True
    >>> allclose(trans1, trans2)
    True

    References
    ----------
    [^decompose-matrix-slabaugh]: Slabaugh, G. [*Computing Euler Angles from a Rotation Matrix*](http://www.gregslabaugh.net/publications/euler.pdf), 1999.

    """
    detM = matrix_determinant(M)  # raises ValueError if matrix is not squared
    if detM == 0:
        raise ValueError("The matrix is singular.")

    Mt = transpose_matrix(M)
    if TOL.is_zero(Mt[3][3]):
        raise ValueError("The element [3,3] of the matrix is zero.")

    for i in range(4):
        for j in range(4):
            Mt[i][j] /= Mt[3][3]

    # copy Mt[:3, :3] into row
    row = [
        [0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0],
    ]
    for i in range(3):
        for j in range(3):
            row[i][j] = Mt[i][j]

    # translation
    translation = [M[0][3], M[1][3], M[2][3]]

    # scale, shear, angles
    scale = [0.0, 0.0, 0.0]
    shear = [0.0, 0.0, 0.0]
    angles = [0.0, 0.0, 0.0]

    scale[0] = norm_vector(row[0])
    for i in range(3):
        row[0][i] /= scale[0]

    shear[0] = dot_vectors(row[0], row[1])
    for i in range(3):
        row[1][i] -= row[0][i] * shear[0]

    scale[1] = norm_vector(row[1])
    for i in range(3):
        row[1][i] /= scale[1]

    shear[1] = dot_vectors(row[0], row[2])
    for i in range(3):
        row[2][i] -= row[0][i] * shear[1]

    # why is the order different here?
    # it certainly influences the result

    shear[2] = dot_vectors(row[1], row[2])
    for i in range(3):
        row[2][i] -= row[0][i] * shear[2]

    scale[2] = norm_vector(row[2])
    for i in range(3):
        row[2][i] /= scale[2]

    shear[0] /= scale[1]
    shear[1] /= scale[2]
    shear[2] /= scale[2]

    if dot_vectors(row[0], cross_vectors(row[1], row[2])) < 0:
        scale = [-x for x in scale]
        row = [[-x for x in y] for y in row]

    # angles
    if row[0][2] != -1.0 and row[0][2] != 1.0:
        beta1 = asin(-row[0][2])
        # beta2 = pi - beta1
        alpha1 = atan2(row[1][2] / cos(beta1), row[2][2] / cos(beta1))
        # alpha2 = atan2(row[1][2] / cos(beta2), row[2][2] / cos(beta2))
        gamma1 = atan2(row[0][1] / cos(beta1), row[0][0] / cos(beta1))
        # gamma2 = atan2(row[0][1] / cos(beta2), row[0][0] / cos(beta2))
        angles = [alpha1, beta1, gamma1]

    else:
        gamma = 0.0
        if row[0][2] == -1.0:
            beta = pi / 2.0
            alpha = gamma + atan2(row[1][0], row[2][0])
        else:  # row[0][2] == 1
            beta = -pi / 2.0
            alpha = -gamma + atan2(-row[1][0], -row[2][0])
        angles = [alpha, beta, gamma]

    # perspective
    if not TOL.is_zero(Mt[0][3]) and not TOL.is_zero(Mt[1][3]) and not TOL.is_zero(Mt[2][3]):
        P = deepcopy(Mt)
        P[0][3], P[1][3], P[2][3], P[3][3] = 0.0, 0.0, 0.0, 1.0
        Ptinv = matrix_inverse(transpose_matrix(P))
        perspective = multiply_matrix_vector(Ptinv, [Mt[0][3], Mt[1][3], Mt[2][3], Mt[3][3]])
    else:
        perspective = [0.0, 0.0, 0.0, 1.0]

    return scale, shear, angles, translation, perspective


def compose_matrix(
    scale: Optional[Sequence[float]] = None,
    shear: Optional[Sequence[float]] = None,
    angles: Optional[Sequence[float]] = None,
    translation: Optional[Sequence[float]] = None,
    perspective: Optional[Sequence[float]] = None,
) -> list[list[float]]:
    """Calculates a matrix from the components of scale, shear, euler_angles, translation and perspective.

    Parameters
    ----------
    scale
        The 3 scale factors in x-, y-, and z-direction.
    shear
        The 3 shear factors for x-y, x-z, and y-z axes.
    angles
        The rotation specified through the 3 Euler angles about static x, y, z axes.
    translation
        The 3 values of translation.
    perspective
        The 4 perspective entries of the matrix.

    Returns
    -------
    list[list[float]]
        The 4x4 matrix that combines the provided transformation components.

    See Also
    --------
    [`decompose_matrix`][compas.linalg.decompose_matrix]

    Examples
    --------
    >>> trans1 = [1, 2, 3]
    >>> angle1 = [-2.142, 1.141, -0.142]
    >>> scale1 = [0.123, 2, 0.5]
    >>> M = compose_matrix(scale1, None, angle1, trans1, None)
    >>> scale2, shear2, angle2, trans2, persp2 = decompose_matrix(M)
    >>> allclose(scale1, scale2)
    True
    >>> allclose(angle1, angle2)
    True
    >>> allclose(trans1, trans2)
    True

    """
    M = [[1.0 if i == j else 0.0 for i in range(4)] for j in range(4)]
    if perspective is not None:
        P = matrix_from_perspective_entries(perspective)
        M = multiply_matrices(M, P)
    if translation is not None:
        T = matrix_from_translation(translation)
        M = multiply_matrices(M, T)
    if angles is not None:
        R = matrix_from_euler_angles(angles, static=True, axes="xyz")
        M = multiply_matrices(M, R)
    if shear is not None:
        H = matrix_from_shear_entries(shear)
        M = multiply_matrices(M, H)
    if scale is not None:
        S = matrix_from_scale_factors(scale)
        M = multiply_matrices(M, S)
    for i in range(4):
        for j in range(4):
            M[i][j] /= M[3][3]
    return M


def identity_matrix(dim: int) -> list[list[float]]:
    """Construct an identity matrix.

    Parameters
    ----------
    dim
        The number of rows and/or columns of the matrix.

    Returns
    -------
    list[list[float]]
        A list of `dim` lists, with each list containing `dim` elements.
        The items on the "diagonal" are one.
        All other items are zero.

    See Also
    --------
    [`matrix_from_frame`][compas.linalg.matrix_from_frame]
    [`matrix_from_frame_to_frame`][compas.linalg.matrix_from_frame_to_frame]
    [`matrix_from_euler_angles`][compas.linalg.matrix_from_euler_angles]
    [`matrix_from_axis_and_angle`][compas.linalg.matrix_from_axis_and_angle]
    [`matrix_from_basis_vectors`][compas.linalg.matrix_from_basis_vectors]
    [`matrix_from_translation`][compas.linalg.matrix_from_translation]
    [`matrix_from_scale_factors`][compas.linalg.matrix_from_scale_factors]
    [`matrix_from_shear_entries`][compas.linalg.matrix_from_shear_entries]
    [`matrix_from_perspective_entries`][compas.linalg.matrix_from_perspective_entries]

    Examples
    --------
    >>> identity_matrix(4)
    [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]]

    """
    return [[1.0 if i == j else 0.0 for i in range(dim)] for j in range(dim)]


def matrix_from_frame(frame: Sequence[Sequence[float]]) -> list[list[float]]:
    """Computes a change of basis transformation from world XY to the frame.

    Parameters
    ----------
    frame
        A frame describing the targeted Cartesian coordinate system

    Returns
    -------
    list[list[float]]
        A 4x4 transformation matrix representing the transformation from
        world coordinates to frame coordinates.

    Examples
    --------
    >>> from compas.geometry import Frame
    >>> f = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
    >>> T = matrix_from_frame(f)

    """
    # Core frame data contains an origin and two axes; derive the third axis.
    point, xaxis, yaxis = frame
    zaxis = cross_vectors(xaxis, yaxis)
    M = identity_matrix(4)
    M[0][0], M[1][0], M[2][0] = xaxis
    M[0][1], M[1][1], M[2][1] = yaxis
    M[0][2], M[1][2], M[2][2] = zaxis
    M[0][3], M[1][3], M[2][3] = point
    return M


def matrix_from_frame_to_frame(frame_from: Sequence[Sequence[float]], frame_to: Sequence[Sequence[float]]) -> list[list[float]]:
    """Computes a transformation between two frames.

    This transformation allows to transform geometry from one Cartesian
    coordinate system defined by `frame_from` to another Cartesian
    coordinate system defined by `frame_to`.

    Parameters
    ----------
    frame_from
        A frame defining the original Cartesian coordinate system
    frame_to
        A frame defining the targeted Cartesian coordinate system

    Returns
    -------
    list[list[float]]
        A 4x4 transformation matrix representing the transformation
        from one frame to another.

    Examples
    --------
    >>> from compas.geometry import Frame
    >>> f1 = Frame([2, 2, 2], [0.12, 0.58, 0.81], [-0.80, 0.53, -0.26])
    >>> f2 = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
    >>> T = matrix_from_frame_to_frame(f1, f2)

    """
    T1 = matrix_from_frame(frame_from)
    T2 = matrix_from_frame(frame_to)
    return multiply_matrices(T2, matrix_inverse(T1))


def matrix_from_change_of_basis(frame_from: Sequence[Sequence[float]], frame_to: Sequence[Sequence[float]]) -> list[list[float]]:
    """Computes a change of basis transformation between two frames.

    A basis change is essentially a remapping of geometry from one
    coordinate system to another.

    Parameters
    ----------
    frame_from
        A frame defining the original Cartesian coordinate system
    frame_to
        A frame defining the targeted Cartesian coordinate system

    Returns
    -------
    list[list[float]]
        A 4x4 transformation matrix representing a change of basis.

    Examples
    --------
    >>> from compas.geometry import Point, Frame
    >>> f1 = Frame([2, 2, 2], [0.12, 0.58, 0.81], [-0.80, 0.53, -0.26])
    >>> f2 = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
    >>> T = matrix_from_change_of_basis(f1, f2)

    """
    T1 = matrix_from_frame(frame_from)
    T2 = matrix_from_frame(frame_to)
    return multiply_matrices(matrix_inverse(T2), T1)


def matrix_from_euler_angles(euler_angles: Sequence[float], static: bool = True, axes: str = "xyz") -> list[list[float]]:
    """Calculates a rotation matrix from Euler angles.

    In 3D space any orientation can be achieved by composing three elemental
    rotations, rotations about the axes (x, y, z) of a coordinate system. A
    triple of Euler angles can be interpreted in 24 ways, which depends on if
    the rotations are applied to a static (extrinsic) or rotating (intrinsic)
    frame and the order of axes.

    Parameters
    ----------
    euler_angles
        Three numbers that represent the angles of rotations about the defined axes.
    static
        If True the rotations are applied to a static frame.
        If False, to a rotational.
    axes
        A 3 character string specifying order of the axes.

    Returns
    -------
    list[list[float]]
        A 4x4 transformation matrix representing a rotation.

    Examples
    --------
    >>> ea1 = 1.4, 0.5, 2.3
    >>> R = matrix_from_euler_angles(ea1)
    >>> ea2 = euler_angles_from_matrix(R)
    >>> allclose(ea1, ea2)
    True

    """
    global _SPEC2TUPLE
    global _NEXT_SPEC

    ai, aj, ak = euler_angles

    if static:
        firstaxis, parity, repetition, frame = _SPEC2TUPLE["s" + axes]
    else:
        firstaxis, parity, repetition, frame = _SPEC2TUPLE["r" + axes]

    i = firstaxis
    j = _NEXT_SPEC[i + parity]
    k = _NEXT_SPEC[i - parity + 1]

    if frame:
        ai, ak = ak, ai
    if parity:
        ai, aj, ak = -ai, -aj, -ak

    si, sj, sk = sin(ai), sin(aj), sin(ak)
    ci, cj, ck = cos(ai), cos(aj), cos(ak)
    cc, cs = ci * ck, ci * sk
    sc, ss = si * ck, si * sk

    M = [[1.0 if x == y else 0.0 for x in range(4)] for y in range(4)]

    if repetition:
        M[i][i] = cj
        M[i][j] = sj * si
        M[i][k] = sj * ci
        M[j][i] = sj * sk
        M[j][j] = -cj * ss + cc
        M[j][k] = -cj * cs - sc
        M[k][i] = -sj * ck
        M[k][j] = cj * sc + cs
        M[k][k] = cj * cc - ss
    else:
        M[i][i] = cj * ck
        M[i][j] = sj * sc - cs
        M[i][k] = sj * cc + ss
        M[j][i] = cj * sk
        M[j][j] = sj * ss + cc
        M[j][k] = sj * cs - sc
        M[k][i] = -sj
        M[k][j] = cj * si
        M[k][k] = cj * ci

    return M


def euler_angles_from_matrix(M: Sequence[Sequence[float]], static: bool = True, axes: str = "xyz") -> list[float]:
    """Returns Euler angles from the rotation matrix M according to specified
    axis sequence and type of rotation.

    Parameters
    ----------
    M
        The 3x3 or 4x4 matrix in row-major order.
    static
        If True the rotations are applied to a static frame.
        If False, to a rotational.
    axes
        A 3 character string specifying order of the axes.

    Returns
    -------
    list[float]
        The 3 Euler angles.

    Examples
    --------
    >>> ea1 = 1.4, 0.5, 2.3
    >>> R = matrix_from_euler_angles(ea1)
    >>> ea2 = euler_angles_from_matrix(R)
    >>> allclose(ea1, ea2)
    True

    """
    global _SPEC2TUPLE
    global _NEXT_SPEC

    if static:
        firstaxis, parity, repetition, frame = _SPEC2TUPLE["s" + axes]
    else:
        firstaxis, parity, repetition, frame = _SPEC2TUPLE["r" + axes]

    i = firstaxis
    j = _NEXT_SPEC[i + parity]
    k = _NEXT_SPEC[i - parity + 1]

    if repetition:
        sy = sqrt(M[i][j] * M[i][j] + M[i][k] * M[i][k])
        if TOL.is_positive(sy):
            ax = atan2(M[i][j], M[i][k])
            ay = atan2(sy, M[i][i])
            az = atan2(M[j][i], -M[k][i])
        else:
            ax = atan2(-M[j][k], M[j][j])
            ay = atan2(sy, M[i][i])
            az = 0.0
    else:
        cy = sqrt(M[i][i] * M[i][i] + M[j][i] * M[j][i])
        if TOL.is_positive(cy):
            ax = atan2(M[k][j], M[k][k])
            ay = atan2(-M[k][i], cy)
            az = atan2(M[j][i], M[i][i])
        else:
            ax = atan2(-M[j][k], M[j][j])
            ay = atan2(-M[k][i], cy)
            az = 0.0

    if parity:
        ax, ay, az = -ax, -ay, -az
    if frame:
        ax, az = az, ax

    return [ax, ay, az]


def matrix_from_axis_and_angle(axis: Sequence[float], angle: float, point: Optional[Sequence[float]] = None) -> list[list[float]]:
    """Calculates a rotation matrix from an rotation axis, an angle and an optional
    point of rotation.

    Parameters
    ----------
    axis
        Three numbers that represent the axis of rotation.
    angle
        The rotation angle in radians.
    point
        A point to perform a rotation around an origin other than [0, 0, 0].

    Returns
    -------
    list[list[float]]
        A 4x4 transformation matrix representing a rotation.

    Notes
    -----
    The rotation is based on the right hand rule, i.e. anti-clockwise if the
    axis of rotation points towards the observer.

    Examples
    --------
    >>> axis1 = normalize_vector([-0.043, -0.254, 0.617])
    >>> angle1 = 0.1
    >>> R = matrix_from_axis_and_angle(axis1, angle1)
    >>> axis2, angle2 = axis_and_angle_from_matrix(R)
    >>> allclose(axis1, axis2)
    True
    >>> allclose([angle1], [angle2])
    True

    """
    if not point:
        point = [0.0, 0.0, 0.0]

    axis = list(axis)
    if length_vector(axis):
        axis = normalize_vector(axis)

    sina = sin(angle)
    cosa = cos(angle)

    R = [[cosa, 0.0, 0.0], [0.0, cosa, 0.0], [0.0, 0.0, cosa]]

    outer_product = [[axis[i] * axis[j] * (1.0 - cosa) for i in range(3)] for j in range(3)]
    R = [[R[i][j] + outer_product[i][j] for i in range(3)] for j in range(3)]

    axis = scale_vector(axis, sina)
    m = [[0.0, -axis[2], axis[1]], [axis[2], 0.0, -axis[0]], [-axis[1], axis[0], 0.0]]

    M = identity_matrix(4)

    for i in range(3):
        for j in range(3):
            R[i][j] += m[i][j]
            M[i][j] = R[i][j]

    # rotation about axis, angle AND point includes also translation
    t = subtract_vectors(point, multiply_matrix_vector(R, point))
    M[0][3] = t[0]
    M[1][3] = t[1]
    M[2][3] = t[2]

    return M


def matrix_from_axis_angle_vector(axis_angle_vector: CoordinateType, point: CoordinateType = (0, 0, 0)) -> list[list[float]]:
    """Calculates a rotation matrix from an axis-angle vector.

    Parameters
    ----------
    axis_angle_vector
        Three numbers that represent the axis of rotation and angle of rotation
        through the vector's magnitude.
    point
        A point to perform a rotation around an origin other than [0, 0, 0].

    Returns
    -------
    list[list[float]]
        The 4x4 transformation matrix representing a rotation.

    Examples
    --------
    >>> aav1 = [-0.043, -0.254, 0.617]
    >>> R = matrix_from_axis_angle_vector(aav1)
    >>> aav2 = axis_angle_vector_from_matrix(R)
    >>> allclose(aav1, aav2)
    True

    """
    axis = list(axis_angle_vector)
    angle = length_vector(axis_angle_vector)
    return matrix_from_axis_and_angle(axis, angle, point)


def axis_and_angle_from_matrix(M: Sequence[Sequence[float]]) -> tuple[list[float], float]:
    """Returns the axis and the angle of the rotation matrix M.

    Parameters
    ----------
    M
        The 4-by-4 transformation matrix.

    Returns
    -------
    tuple[list[float], float]
        The rotation axis and rotation angle in radians.

    """
    eps = 0.01  # margin to allow for rounding errors
    eps2 = 0.1  # margin to distinguish between 0 and 180 degrees

    if all(fabs(M[i][j] - M[j][i]) < eps for i, j in [(0, 1), (0, 2), (1, 2)]):
        if all(fabs(M[i][j] - M[j][i]) < eps2 for i, j in [(0, 1), (0, 2), (1, 2)]) and fabs(M[0][0] + M[1][1] + M[2][2] - 3) < eps2:
            return [0, 0, 0], 0

        angle = pi
        xx = (M[0][0] + 1) / 2
        yy = (M[1][1] + 1) / 2
        zz = (M[2][2] + 1) / 2
        xy = (M[0][1] + M[1][0]) / 4
        xz = (M[0][2] + M[2][0]) / 4
        yz = (M[1][2] + M[2][1]) / 4
        root_half = sqrt(0.5)
        if (xx > yy) and (xx > zz):
            if xx < eps:
                axis = [0, root_half, root_half]
            else:
                x = sqrt(xx)
                axis = [x, xy / x, xz / x]
        elif yy > zz:
            if yy < eps:
                axis = [root_half, 0, root_half]
            else:
                y = sqrt(yy)
                axis = [xy / y, y, yz / y]
        else:
            if zz < eps:
                axis = [root_half, root_half, 0]
            else:
                z = sqrt(zz)
                axis = [xz / z, yz / z, z]

        return axis, angle

    s = sqrt((M[2][1] - M[1][2]) * (M[2][1] - M[1][2]) + (M[0][2] - M[2][0]) * (M[0][2] - M[2][0]) + (M[1][0] - M[0][1]) * (M[1][0] - M[0][1]))

    # should this also be an eps?
    if fabs(s) < 0.001:
        s = 1

    angle = acos((M[0][0] + M[1][1] + M[2][2] - 1) / 2)

    x = (M[2][1] - M[1][2]) / s
    y = (M[0][2] - M[2][0]) / s
    z = (M[1][0] - M[0][1]) / s

    return [x, y, z], angle


def axis_angle_vector_from_matrix(M: Sequence[Sequence[float]]) -> list[float]:
    """Returns the axis-angle vector of the rotation matrix M.

    Parameters
    ----------
    M
        The 4-by-4 transformation matrix.

    Returns
    -------
    list[float]
        The axis-angle vector.

    """
    axis, angle = axis_and_angle_from_matrix(M)
    return scale_vector(axis, angle)


def matrix_from_quaternion(quaternion: FloatSequenceType) -> list[list[float]]:
    """Calculates a rotation matrix from quaternion coefficients.

    Parameters
    ----------
    quaternion
        Four numbers that represents the four coefficient values of a quaternion.

    Returns
    -------
    list[list[float]]
        The 4x4 transformation matrix representing a rotation.

    Raises
    ------
    ValueError
        If quaternion is invalid.

    Examples
    --------
    >>> q1 = [0.945, -0.021, -0.125, 0.303]
    >>> R = matrix_from_quaternion(q1)
    >>> q2 = quaternion_from_matrix(R)
    >>> allclose(q1, q2, tol=1e-03)
    True

    """
    q = quaternion
    n = q[0] ** 2 + q[1] ** 2 + q[2] ** 2 + q[3] ** 2  # dot product

    # perhaps this should not be hard-coded?
    eps = 1.0e-15

    if n < eps:
        raise ValueError("Invalid quaternion, dot product must be != 0.")

    q = [v * sqrt(2.0 / n) for v in q]
    q = [[q[i] * q[j] for i in range(4)] for j in range(4)]  # outer_product

    rotation = [
        [1.0 - q[2][2] - q[3][3], q[1][2] - q[3][0], q[1][3] + q[2][0], 0.0],
        [q[1][2] + q[3][0], 1.0 - q[1][1] - q[3][3], q[2][3] - q[1][0], 0.0],
        [q[1][3] - q[2][0], q[2][3] + q[1][0], 1.0 - q[1][1] - q[2][2], 0.0],
        [0.0, 0.0, 0.0, 1.0],
    ]
    return rotation


def quaternion_from_matrix(M: Sequence[Sequence[float]]) -> list[float]:
    """Returns the 4 quaternion coefficients from a rotation matrix.

    Parameters
    ----------
    M
        The coefficients of the rotation matrix, row per row.

    Returns
    -------
    list[float]
        The quaternion coefficients.

    Examples
    --------
    >>> q1 = [0.945, -0.021, -0.125, 0.303]
    >>> R = matrix_from_quaternion(q1)
    >>> q2 = quaternion_from_matrix(R)
    >>> allclose(q1, q2, tol=1e-03)
    True

    """
    qw, qx, qy, qz = 0, 0, 0, 0
    trace = M[0][0] + M[1][1] + M[2][2]

    if trace > 0.0:
        s = 0.5 / sqrt(trace + 1.0)
        qw = 0.25 / s
        qx = (M[2][1] - M[1][2]) * s
        qy = (M[0][2] - M[2][0]) * s
        qz = (M[1][0] - M[0][1]) * s

    elif (M[0][0] > M[1][1]) and (M[0][0] > M[2][2]):
        s = 2.0 * sqrt(1.0 + M[0][0] - M[1][1] - M[2][2])
        qw = (M[2][1] - M[1][2]) / s
        qx = 0.25 * s
        qy = (M[0][1] + M[1][0]) / s
        qz = (M[0][2] + M[2][0]) / s

    elif M[1][1] > M[2][2]:
        s = 2.0 * sqrt(1.0 + M[1][1] - M[0][0] - M[2][2])
        qw = (M[0][2] - M[2][0]) / s
        qx = (M[0][1] + M[1][0]) / s
        qy = 0.25 * s
        qz = (M[1][2] + M[2][1]) / s
    else:
        s = 2.0 * sqrt(1.0 + M[2][2] - M[0][0] - M[1][1])
        qw = (M[1][0] - M[0][1]) / s
        qx = (M[0][2] + M[2][0]) / s
        qy = (M[1][2] + M[2][1]) / s
        qz = 0.25 * s

    return [qw, qx, qy, qz]


def matrix_from_basis_vectors(xaxis: CoordinateType, yaxis: CoordinateType) -> list[list[float]]:
    """Creates a rotation matrix from basis vectors (= orthonormal vectors).

    Parameters
    ----------
    xaxis
        The x-axis of the frame.
    yaxis
        The y-axis of the frame.

    Returns
    -------
    list[list[float]]
        A 4x4 transformation matrix representing a rotation.

    Notes
    -----
    ```text
        [ x0  y0  z0  0 ]
        [ x1  y1  z1  0 ]
        [ x2  y2  z2  0 ]
        [  0   0   0  1 ]
    ```

    Examples
    --------
    >>> xaxis = [0.68, 0.68, 0.27]
    >>> yaxis = [-0.67, 0.73, -0.15]
    >>> R = matrix_from_basis_vectors(xaxis, yaxis)

    """
    xaxis = normalize_vector(list(xaxis))
    yaxis = normalize_vector(list(yaxis))
    zaxis = cross_vectors(xaxis, yaxis)
    yaxis = cross_vectors(zaxis, xaxis)

    R = identity_matrix(4)
    R[0][0], R[1][0], R[2][0] = xaxis
    R[0][1], R[1][1], R[2][1] = yaxis
    R[0][2], R[1][2], R[2][2] = zaxis
    return R


def basis_vectors_from_matrix(R: Sequence[Sequence[float]]) -> tuple[list[float], list[float]]:
    """Returns the basis vectors from the rotation matrix R.

    Parameters
    ----------
    R
        A 4-by-4 transformation matrix, or a 3-by-3 rotation matrix.

    Returns
    -------
    tuple[list[float], list[float]]
        The first and second basis vectors of the rotation.

    Raises
    ------
    ValueError
        If rotation matrix is invalid.

    Examples
    --------
    >>> from compas.geometry import Frame
    >>> f = Frame([0, 0, 0], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
    >>> R = matrix_from_frame(f)
    >>> xaxis, yaxis = basis_vectors_from_matrix(R)

    """
    xaxis = [R[0][0], R[1][0], R[2][0]]
    yaxis = [R[0][1], R[1][1], R[2][1]]
    zaxis = [R[0][2], R[1][2], R[2][2]]

    if not allclose(zaxis, cross_vectors(xaxis, yaxis)):
        raise ValueError("Matrix is invalid rotation matrix.")

    return xaxis, yaxis


def matrix_from_translation(translation: Sequence[float]) -> list[list[float]]:
    """Returns a 4x4 translation matrix in row-major order.

    Parameters
    ----------
    translation
        The x, y and z components of the translation.

    Returns
    -------
    list[list[float]]
        The 4x4 transformation matrix representing a translation.

    Notes
    -----
    ```text
        [ .  .  .  0 ]
        [ .  .  .  1 ]
        [ .  .  .  2 ]
        [ .  .  .  . ]
    ```

    Examples
    --------
    >>> T = matrix_from_translation([1, 2, 3])

    """
    M = identity_matrix(4)
    M[0][3] = float(translation[0])
    M[1][3] = float(translation[1])
    M[2][3] = float(translation[2])

    return M


def translation_from_matrix(M: Sequence[Sequence[float]]) -> list[float]:
    """Returns the 3 values of translation from the matrix M.

    Parameters
    ----------
    M
        A 4-by-4 transformation matrix.

    Returns
    -------
    list[float]
        The translation vector.

    """
    return [M[0][3], M[1][3], M[2][3]]


def matrix_from_orthogonal_projection(
    plane: tuple[Sequence[float], Sequence[float]],
) -> list[list[float]]:
    """Returns an orthogonal projection matrix to project onto a plane.

    Parameters
    ----------
    plane
        The plane to project onto.

    Returns
    -------
    list[list[float]]
        The 4x4 transformation matrix representing an orthogonal projection.

    Examples
    --------
    >>> point = [0, 0, 0]
    >>> normal = [0, 0, 1]
    >>> plane = (point, normal)
    >>> P = matrix_from_orthogonal_projection(plane)

    """
    point, normal = plane
    T = identity_matrix(4)
    normal = normalize_vector(normal)

    for j in range(3):
        for i in range(3):
            T[i][j] -= normal[i] * normal[j]  # outer_product

    T[0][3], T[1][3], T[2][3] = scale_vector(normal, dot_vectors(point, normal))
    return T


def matrix_from_parallel_projection(plane: tuple[Sequence[float], Sequence[float]], direction: Sequence[float]) -> list[list[float]]:
    """Returns an parallel projection matrix to project onto a plane.

    Parameters
    ----------
    plane
        The plane to project onto.
    direction
        Direction of the projection.

    Returns
    -------
    list[list[float]]
        A 4-by-4 transformation matrix.

    Examples
    --------
    >>> point = [0, 0, 0]
    >>> normal = [0, 0, 1]
    >>> plane = (point, normal)
    >>> direction = [1, 1, 1]
    >>> P = matrix_from_parallel_projection(plane, direction)

    """
    point, normal = plane
    T = identity_matrix(4)
    normal = normalize_vector(normal)

    scale = dot_vectors(direction, normal)
    for j in range(3):
        for i in range(3):
            T[i][j] -= direction[i] * normal[j] / scale

    T[0][3], T[1][3], T[2][3] = scale_vector(direction, dot_vectors(point, normal) / scale)
    return T


def matrix_from_perspective_projection(plane: tuple[Sequence[float], Sequence[float]], center_of_projection: Sequence[float]) -> list[list[float]]:
    """Returns a perspective projection matrix to project onto a plane along lines that emanate from a single point, called the center of projection.

    Parameters
    ----------
    plane
        The plane to project onto.
    center_of_projection
        The camera view point.

    Returns
    -------
    list[list[float]]
        A 4-by-4 transformation matrix.

    Examples
    --------
    >>> point = [0, 0, 0]
    >>> normal = [0, 0, 1]
    >>> plane = (point, normal)
    >>> center_of_projection = [1, 1, 0]
    >>> P = matrix_from_perspective_projection(plane, center_of_projection)

    """
    point, normal = plane
    T = identity_matrix(4)
    normal = normalize_vector(normal)

    T[0][0] = T[1][1] = T[2][2] = dot_vectors(subtract_vectors(center_of_projection, point), normal)

    for j in range(3):
        for i in range(3):
            T[i][j] -= center_of_projection[i] * normal[j]

    T[0][3], T[1][3], T[2][3] = scale_vector(center_of_projection, dot_vectors(point, normal))

    for i in range(3):
        T[3][i] -= normal[i]

    T[3][3] = dot_vectors(center_of_projection, normal)

    return T


def matrix_from_perspective_entries(perspective: Sequence[float]) -> list[list[float]]:
    """Returns a matrix from perspective entries.

    Parameters
    ----------
    perspective
        The 4 perspective entries of a matrix.

    Returns
    -------
    list[list[float]]
        A 4-by-4 transformation matrix.

    Notes
    -----
    ```text
        [ .  .  .  . ]
        [ .  .  .  . ]
        [ .  .  .  . ]
        [ 0  1  2  3 ]
    ```
    """
    M = identity_matrix(4)
    M[3][0] = float(perspective[0])
    M[3][1] = float(perspective[1])
    M[3][2] = float(perspective[2])
    M[3][3] = float(perspective[3])
    return M


def matrix_from_shear_entries(shear_entries: Sequence[float]) -> list[list[float]]:
    """Returns a shear matrix from the 3 factors for x-y, x-z, and y-z axes.

    Parameters
    ----------
    shear_entries
        The 3 shear factors for x-y, x-z, and y-z axes.

    Returns
    -------
    list[list[float]]
        A 4-by-4 transformation matrix.

    Notes
    -----
    ```text
        [ .  0  1  . ]
        [ .  .  2  . ]
        [ .  .  .  . ]
        [ .  .  .  . ]
    ```

    Examples
    --------
    >>> Sh = matrix_from_shear_entries([1, 2, 3])

    """
    M = identity_matrix(4)
    M[0][1] = float(shear_entries[0])
    M[0][2] = float(shear_entries[1])
    M[1][2] = float(shear_entries[2])
    return M


def matrix_from_shear(angle: float, direction: Sequence[float], point: Sequence[float], normal: Sequence[float]) -> list[list[float]]:
    """Constructs a shear matrix by an angle along the direction vector on the
    shear plane (defined by point and normal).

    Parameters
    ----------
    angle
        The angle in radians.
    direction
        The direction vector as list of 3 numbers.
        It must be orthogonal to the normal vector.
    point
        The point of the shear plane as list of 3 numbers.
    normal
        The normal of the shear plane as list of 3 numbers.

    Returns
    -------
    list[list[float]]
        A 4-by-4 transformation matrix.

    Raises
    ------
    ValueError
        If direction and normal are not orthogonal.

    Notes
    -----
    A point P is transformed by the shear matrix into P" such that
    the vector P-P" is parallel to the direction vector and its extent is
    given by the angle of P-P'-P", where P' is the orthogonal projection
    of P onto the shear plane (defined by point and normal).

    Examples
    --------
    >>> angle = 0.1
    >>> direction = [0.1, 0.2, 0.3]
    >>> point = [4, 3, 1]
    >>> normal = cross_vectors(direction, [1, 0.3, -0.1])
    >>> S = matrix_from_shear(angle, direction, point, normal)

    """
    normal = normalize_vector(normal)
    direction = normalize_vector(direction)

    if not TOL.is_zero(dot_vectors(normal, direction)):
        raise ValueError("Direction and normal vectors are not orthogonal")

    angle = tan(angle)
    M = identity_matrix(4)

    for j in range(3):
        for i in range(3):
            M[i][j] += angle * direction[i] * normal[j]

    M[0][3], M[1][3], M[2][3] = scale_vector(direction, -angle * dot_vectors(point, normal))

    return M


def matrix_from_scale_factors(scale_factors: Sequence[float]) -> list[list[float]]:
    """Returns a 4x4 scaling transformation.

    Parameters
    ----------
    scale_factors
        Three numbers defining the scaling factors in x, y, and z respectively.

    Returns
    -------
    list[list[float]]
        A 4-by-4 transformation matrix.

    Notes
    -----
    ```text
        [ 0  .  .  . ]
        [ .  1  .  . ]
        [ .  .  2  . ]
        [ .  .  .  . ]
    ```

    Examples
    --------
    >>> Sc = matrix_from_scale_factors([1, 2, 3])

    """
    M = identity_matrix(4)
    M[0][0] = float(scale_factors[0])
    M[1][1] = float(scale_factors[1])
    M[2][2] = float(scale_factors[2])

    return M
