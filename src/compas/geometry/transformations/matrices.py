from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import math

from copy import deepcopy

from compas.geometry import scale_vector
from compas.geometry import normalize_vector
from compas.geometry import subtract_vectors
from compas.geometry import cross_vectors
from compas.geometry import dot_vectors
from compas.geometry import multiply_matrix_vector
from compas.geometry import length_vector
from compas.geometry import allclose
from compas.geometry import multiply_matrices
from compas.geometry import transpose_matrix
from compas.geometry import norm_vector


_EPS = 1e-16
"""eps for testing whether a number is close to zero"""

_SPEC2TUPLE = {
    'sxyz': (0, 0, 0, 0), 'sxyx': (0, 0, 1, 0), 'sxzy': (0, 1, 0, 0),
    'sxzx': (0, 1, 1, 0), 'syzx': (1, 0, 0, 0), 'syzy': (1, 0, 1, 0),
    'syxz': (1, 1, 0, 0), 'syxy': (1, 1, 1, 0), 'szxy': (2, 0, 0, 0),
    'szxz': (2, 0, 1, 0), 'szyx': (2, 1, 0, 0), 'szyz': (2, 1, 1, 0),
    'rzyx': (0, 0, 0, 1), 'rxyx': (0, 0, 1, 1), 'ryzx': (0, 1, 0, 1),
    'rxzx': (0, 1, 1, 1), 'rxzy': (1, 0, 0, 1), 'ryzy': (1, 0, 1, 1),
    'rzxy': (1, 1, 0, 1), 'ryxy': (1, 1, 1, 1), 'ryxz': (2, 0, 0, 1),
    'rzxz': (2, 0, 1, 1), 'rxyz': (2, 1, 0, 1), 'rzyz': (2, 1, 1, 1)}
"""used for Euler angles: to map rotation type and axes to tuples of inner axis, parity, repetition, frame"""

_NEXT_SPEC = [1, 2, 0, 1]


__all__ = [
    'matrix_determinant',
    'matrix_inverse',
    'decompose_matrix',
    'compose_matrix',

    'identity_matrix',

    'matrix_from_frame',
    'matrix_from_frame_to_frame',
    'matrix_from_change_of_basis',
    'matrix_from_euler_angles',
    'matrix_from_axis_and_angle',
    'matrix_from_axis_angle_vector',
    'matrix_from_basis_vectors',
    'matrix_from_translation',
    'matrix_from_orthogonal_projection',
    'matrix_from_parallel_projection',
    'matrix_from_perspective_projection',
    'matrix_from_perspective_entries',
    'matrix_from_shear_entries',
    'matrix_from_shear',
    'matrix_from_scale_factors',
    'matrix_from_quaternion',

    'euler_angles_from_matrix',
    'euler_angles_from_quaternion',

    'axis_and_angle_from_matrix',
    'axis_angle_vector_from_matrix',
    'axis_angle_from_quaternion',

    'quaternion_from_matrix',
    'quaternion_from_euler_angles',
    'quaternion_from_axis_angle',

    'basis_vectors_from_matrix',
    'translation_from_matrix',
]


def is_matrix_square(M):
    """Verify that a matrix is square.

    Parameters
    ----------
    M : list of list
        The matrix.

    Returns
    -------
    bool
        True if the length of every row is equal to the number of rows.
        False otherwise.

    Examples
    --------
    >>> M = identity_matrix(4)
    >>> is_matrix_square(M)
    True
    """
    number_of_rows = len(M)
    for row in M:
        if len(row) != number_of_rows:
            return False
    return True


def matrix_minor(M, i, j):
    return [row[:j] + row[j + 1:] for row in (M[:i] + M[i + 1:])]


def matrix_determinant(M, check=True):
    """Calculates the determinant of a square matrix M.

    Parameters
    ----------
    M : list of list of float
        A square matrix of any dimension.
    check : bool
        If ``True``, checks if matrix is squared.
        Default is ``True``.

    Raises
    ------
    ValueError
        If the matrix is not square.

    Returns
    -------
    float
        The determinant.

    Examples
    --------
    >>> M = identity_matrix(4)
    >>> matrix_determinant(M)
    1.0
    """
    dim = len(M)

    if check:
        if not is_matrix_square(M):
            raise ValueError("Not a square matrix")

    if dim == 2:
        return M[0][0] * M[1][1] - M[0][1] * M[1][0]

    D = 0
    for c in range(dim):
        D += (-1) ** c * M[0][c] * matrix_determinant(matrix_minor(M, 0, c), check=False)
    return D


def matrix_inverse(M):
    """Calculates the inverse of a square matrix M.

    Parameters
    ----------
    M : list of list of float
        A square matrix of any dimension.

    Raises
    ------
    ValueError
        If the matrix is not squared
    ValueError
        If the matrix is singular.
    ValueError
        If the matrix is not invertible.

    Returns
    -------
    list of list of float
        The inverted matrix.

    Examples
    --------
    >>> from compas.geometry import Frame
    >>> f = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
    >>> T = matrix_from_frame(f)
    >>> I = multiply_matrices(T, matrix_inverse(T))
    >>> I2 = identity_matrix(4)
    >>> allclose(I[0], I2[0])
    True
    >>> allclose(I[1], I2[1])
    True
    >>> allclose(I[2], I2[2])
    True
    >>> allclose(I[3], I2[3])
    True

    """
    D = matrix_determinant(M)

    if D == 0:
        ValueError("The matrix is singular.")

    if len(M) == 2:
        return [[M[1][1] / D, -1 * M[0][1] / D],
                [-1 * M[1][0] / D, M[0][0] / D]]

    cofactors = []
    for r in range(len(M)):
        cofactor_row = []
        for c in range(len(M)):
            cofactor_row.append((-1) ** (r + c) * matrix_determinant(matrix_minor(M, r, c)))
        cofactors.append(cofactor_row)

    cofactors = transpose_matrix(cofactors)

    for r in range(len(cofactors)):
        for c in range(len(cofactors)):
            cofactors[r][c] = cofactors[r][c] / D

    return cofactors


def decompose_matrix(M):
    """Calculates the components of rotation, translation, scale, shear, and
    perspective of a given transformation matrix M. [1]_

    Parameters
    ----------
    M : :obj:`list` of :obj:`list` of :obj:`float`
        The square matrix of any dimension.

    Raises
    ------
    ValueError
        If matrix is singular or degenerative.

    Returns
    -------
    tuple (scale, shear, angles, translation, perspective)
        * scale (:obj:`list` of :obj:`float`)
          - The 3 scale factors in x-, y-, and z-direction.
        * shear (:obj:`list` of :obj:`float`)
          - The 3 shear factors for x-y, x-z, and y-z axes.
        * angles (:obj:`list` of :obj:`float`)
          - The rotation specified through the 3 Euler angles about static x, y, z axes.
        * translation (:obj:`list` of :obj:`float`)
          - The 3 values of translation.
        * perspective (:obj:`list` of :obj:`float`)
          - The 4 perspective entries of the matrix.

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
    .. [1] Slabaugh, 1999. *Computing Euler angles from a rotation matrix*.
           Available at: http://www.gregslabaugh.net/publications/euler.pdf
    """
    fabs = math.fabs
    cos = math.cos
    atan2 = math.atan2
    asin = math.asin
    pi = math.pi

    detM = matrix_determinant(M)  # raises ValueError if matrix is not squared
    if detM == 0:
        ValueError("The matrix is singular.")

    Mt = transpose_matrix(M)
    if abs(Mt[3][3]) < _EPS:
        raise ValueError('The element [3,3] of the matrix is zero.')

    for i in range(4):
        for j in range(4):
            Mt[i][j] /= Mt[3][3]

    translation = [M[0][3], M[1][3], M[2][3]]

    # scale, shear, angles
    scale = [0.0, 0.0, 0.0]
    shear = [0.0, 0.0, 0.0]
    angles = [0.0, 0.0, 0.0]

    # copy Mt[:3, :3] into row
    row = [[0, 0, 0] for i in range(3)]
    for i in range(3):
        for j in range(3):
            row[i][j] = Mt[i][j]

    scale[0] = norm_vector(row[0])
    for i in range(3):
        row[0][i] /= scale[0]

    shear[0] = dot_vectors(row[0], row[1])
    for i in range(3):
        row[1][i] -= row[0][i] * shear[0]

    scale[1] = norm_vector(row[1])
    for i in range(3):
        row[1][i] /= scale[1]
    shear[0] /= scale[1]

    shear[1] = dot_vectors(row[0], row[2])
    for i in range(3):
        row[2][i] -= row[0][i] * shear[1]

    shear[2] = dot_vectors(row[1], row[2])
    for i in range(3):
        row[2][i] -= row[0][i] * shear[2]

    scale[2] = norm_vector(row[2])
    for i in range(3):
        row[2][i] /= scale[2]

    shear[1] /= scale[2]
    shear[2] /= scale[2]

    if dot_vectors(row[0], cross_vectors(row[1], row[2])) < 0:
        scale = [-x for x in scale]
        row = [[-x for x in y] for y in row]

    # angles
    if row[0][2] != -1. and row[0][2] != 1.:
        beta1 = asin(-row[0][2])
        # beta2 = pi - beta1
        alpha1 = atan2(row[1][2] / cos(beta1), row[2][2] / cos(beta1))
        # alpha2 = atan2(row[1][2] / cos(beta2), row[2][2] / cos(beta2))
        gamma1 = atan2(row[0][1] / cos(beta1), row[0][0] / cos(beta1))
        # gamma2 = atan2(row[0][1] / cos(beta2), row[0][0] / cos(beta2))
        angles = [alpha1, beta1, gamma1]
    else:
        gamma = 0.
        if row[0][2] == -1.:
            beta = pi / 2.
            alpha = gamma + atan2(row[1][0], row[2][0])
        else:  # row[0][2] == 1
            beta = -pi / 2.
            alpha = -gamma + atan2(-row[1][0], -row[2][0])
        angles = [alpha, beta, gamma]

    # perspective
    if fabs(Mt[0][3]) > _EPS and fabs(Mt[1][3]) > _EPS and fabs(Mt[2][3]) > _EPS:
        P = deepcopy(Mt)
        P[0][3], P[1][3], P[2][3], P[3][3] = 0.0, 0.0, 0.0, 1.0
        Ptinv = matrix_inverse(transpose_matrix(P))
        perspective = multiply_matrix_vector(Ptinv, [Mt[0][3], Mt[1][3], Mt[2][3], Mt[3][3]])
    else:
        perspective = [0.0, 0.0, 0.0, 1.0]

    return scale, shear, angles, translation, perspective


def compose_matrix(scale=None, shear=None, angles=None,
                   translation=None, perspective=None):
    """Calculates a matrix from the components of scale, shear, euler_angles,
    translation and perspective.

    Parameters
    ----------
    scale : :obj:`list` of :obj:`float`
        The 3 scale factors in x-, y-, and z-direction.
    shear : :obj:`list` of :obj:`float`
        The 3 shear factors for x-y, x-z, and y-z axes.
    angles : :obj:`list` of :obj:`float`
        The rotation specified through the 3 Euler angles about static x, y, z axes.
    translation : :obj:`list` of :obj:`float`
        The 3 values of translation.
    perspective : :obj:`list` of :obj:`float`
        The 4 perspective entries of the matrix.

    Returns
    -------
    list of list of float
        The 4x4 matrix that combines the provided transformation components.

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
    M = [[1. if i == j else 0. for i in range(4)] for j in range(4)]
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


def identity_matrix(dim):
    """Construct an identity matrix.

    Parameters
    ----------
    dim : int
        The number of rows and/or columns of the matrix.

    Returns
    -------
    list of list
        A list of ``dim`` lists, with each list containing ``dim`` elements.
        The items on the "diagonal" are one.
        All other items are zero.

    Examples
    --------
    >>> identity_matrix(4)
    [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]]
    """
    return [[1. if i == j else 0. for i in range(dim)] for j in range(dim)]


def matrix_from_frame(frame):
    """Computes a change of basis transformation from world XY to the frame.

    Parameters
    ----------
    frame : :class:`compas.geometry.Frame`
        A frame describing the targeted Cartesian coordinate system

    Returns
    -------
    list of list of float
        A 4x4 transformation matrix representing the transformation from
        world coordinates to frame coordinates.

    Examples
    --------
    >>> from compas.geometry import Frame
    >>> f = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
    >>> T = matrix_from_frame(f)

    """
    M = identity_matrix(4)
    M[0][0], M[1][0], M[2][0] = frame.xaxis
    M[0][1], M[1][1], M[2][1] = frame.yaxis
    M[0][2], M[1][2], M[2][2] = frame.zaxis
    M[0][3], M[1][3], M[2][3] = frame.point
    return M


def matrix_from_frame_to_frame(frame_from, frame_to):
    """Computes a transformation between two frames.

    This transformation allows to transform geometry from one Cartesian
    coordinate system defined by "frame_from" to another Cartesian
    coordinate system defined by "frame_to".

    Parameters
    ----------
    frame_from : :class:`Frame`
        A frame defining the original Cartesian coordinate system
    frame_to : :class:`Frame`
        A frame defining the targeted Cartesian coordinate system

    Returns
    -------
    list of list of float
        A 4x4 transformation matrix representing the transformation
        from one frame to another.

    Examples
    --------
    >>> f1 = Frame([2, 2, 2], [0.12, 0.58, 0.81], [-0.80, 0.53, -0.26])
    >>> f2 = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
    >>> T = matrix_from_frame_to_frame(f1, f2)
    """
    T1 = matrix_from_frame(frame_from)
    T2 = matrix_from_frame(frame_to)
    return multiply_matrices(T2, matrix_inverse(T1))


def matrix_from_change_of_basis(frame_from, frame_to):
    """Computes a change of basis transformation between two frames.

    A basis change is essentially a remapping of geometry from one
    coordinate system to another.

    Parameters
    ----------
    frame_from : :class:`Frame`
        A frame defining the original Cartesian coordinate system
    frame_to : :class:`Frame`
        A frame defining the targeted Cartesian coordinate system

    Returns
    -------
    list of list of float
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


def matrix_from_euler_angles(euler_angles, static=True, axes='xyz'):
    """Calculates a rotation matrix from Euler angles.

    In 3D space any orientation can be achieved by composing three elemental
    rotations, rotations about the axes (x,y,z) of a coordinate system. A
    triple of Euler angles can be interpreted in 24 ways, which depends on if
    the rotations are applied to a static (extrinsic) or rotating (intrinsic)
    frame and the order of axes.

    Parameters
    ----------
    euler_angles : list of float
        Three numbers that represent the angles of rotations about the defined axes.
    static : bool, optional
        If true the rotations are applied to a static frame.
        If not, to a rotational.
        Default is ``True``.
    axes : {'xyz', 'yzx', 'zxy'}, optional
        A 3 character string specifying order of the axes.
        Default is ``'xyz'``.

    Returns
    -------
    list of list of float
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

    sin = math.sin
    cos = math.cos

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

    M = [[1. if x == y else 0. for x in range(4)] for y in range(4)]

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


def euler_angles_from_matrix(M, static=True, axes='xyz'):
    """Returns Euler angles from the rotation matrix M according to specified
    axis sequence and type of rotation.

    Parameters
    ----------
    M : list of list of float
        The 3x3 or 4x4 matrix in row-major order.
    static : bool, optional
        If true the rotations are applied to a static frame.
        If not, to a rotational.
        Defaults to True.
    axes : str, optional
        A 3 character string specifying order of the axes.
        Defaults to 'xyz'.

    Returns
    -------
    list of float
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
    global _EPS

    atan2 = math.atan2
    sqrt = math.sqrt

    if static:
        firstaxis, parity, repetition, frame = _SPEC2TUPLE["s" + axes]
    else:
        firstaxis, parity, repetition, frame = _SPEC2TUPLE["r" + axes]

    i = firstaxis
    j = _NEXT_SPEC[i + parity]
    k = _NEXT_SPEC[i - parity + 1]

    if repetition:
        sy = sqrt(M[i][j] * M[i][j] + M[i][k] * M[i][k])
        if sy > _EPS:
            ax = atan2(M[i][j], M[i][k])
            ay = atan2(sy, M[i][i])
            az = atan2(M[j][i], -M[k][i])
        else:
            ax = atan2(-M[j][k], M[j][j])
            ay = atan2(sy, M[i][i])
            az = 0.0
    else:
        cy = sqrt(M[i][i] * M[i][i] + M[j][i] * M[j][i])
        if cy > _EPS:
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


def matrix_from_axis_and_angle(axis, angle, point=None):
    """Calculates a rotation matrix from an rotation axis, an angle and an optional
    point of rotation.

    Parameters
    ----------
    axis : list of float
        Three numbers that represent the axis of rotation.
    angle : float
        The rotation angle in radians.
    point : list of float, optional
        A point to perform a rotation around an origin other than [0, 0, 0].

    Returns
    -------
    list of list of float
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

    sina = math.sin(angle)
    cosa = math.cos(angle)

    R = [[cosa, 0.0, 0.0], [0.0, cosa, 0.0], [0.0, 0.0, cosa]]

    outer_product = [[axis[i] * axis[j] * (1.0 - cosa) for i in range(3)] for j in range(3)]
    R = [[R[i][j] + outer_product[i][j] for i in range(3)] for j in range(3)]

    axis = scale_vector(axis, sina)
    m = [[0.0, -axis[2], axis[1]],
         [axis[2], 0.0, -axis[0]],
         [-axis[1], axis[0], 0.0]]

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


def matrix_from_axis_angle_vector(axis_angle_vector, point=[0, 0, 0]):
    """Calculates a rotation matrix from an axis-angle vector.

    Parameters
    ----------
    axis_angle_vector : list of float
        Three numbers that represent the axis of rotation and angle of rotation
        through the vector's magnitude.
    point : list of float, optional
        A point to perform a rotation around an origin other than [0, 0, 0].

    Returns
    -------
    list of list of float
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


def axis_and_angle_from_matrix(M):
    """Returns the axis and the angle of the rotation matrix M.
    """
    fabs = math.fabs
    sqrt = math.sqrt

    eps = 0.01  # margin to allow for rounding errors
    eps2 = 0.1  # margin to distinguish between 0 and 180 degrees

    if all(fabs(M[i][j] - M[j][i]) < eps for i, j in [(0, 1), (0,  2), (1, 2)]):

        if (all(fabs(M[i][j] - M[j][i]) < eps2 for i, j in [(0, 1), (0,  2), (1, 2)]) and
                fabs(M[0][0] + M[1][1] + M[2][2] - 3) < eps2):
            return [0, 0, 0], 0

        angle = math.pi
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

    s = sqrt(
        (M[2][1] - M[1][2]) * (M[2][1] - M[1][2]) +
        (M[0][2] - M[2][0]) * (M[0][2] - M[2][0]) +
        (M[1][0] - M[0][1]) * (M[1][0] - M[0][1]))

    # should this also be an eps?
    if fabs(s) < 0.001:
        s = 1

    angle = math.acos((M[0][0] + M[1][1] + M[2][2] - 1) / 2)

    x = (M[2][1] - M[1][2]) / s
    y = (M[0][2] - M[2][0]) / s
    z = (M[1][0] - M[0][1]) / s

    return [x, y, z], angle


def axis_angle_vector_from_matrix(M):
    """Returns the axis-angle vector of the rotation matrix M.
    """
    axis, angle = axis_and_angle_from_matrix(M)
    return scale_vector(axis, angle)


def matrix_from_quaternion(quaternion):
    """Calculates a rotation matrix from quaternion coefficients.

    Parameters
    ----------
    quaternion : list of float
        Four numbers that represents the four coefficient values of a quaternion.

    Returns
    -------
    list of list of float
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
    sqrt = math.sqrt

    q = quaternion
    n = q[0]**2 + q[1]**2 + q[2]**2 + q[3]**2  # dot product

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
        [0.0, 0.0, 0.0, 1.0]]
    return rotation


def quaternion_from_matrix(M):
    """Returns the 4 quaternion coefficients from a rotation matrix.

    Parameters
    ----------
    M : list of list of float
        The coefficients of the rotation matrix, row per row.

    Returns
    -------
    list of float
        The quaternion coefficients.

    Examples
    --------
    >>> q1 = [0.945, -0.021, -0.125, 0.303]
    >>> R = matrix_from_quaternion(q1)
    >>> q2 = quaternion_from_matrix(R)
    >>> allclose(q1, q2, tol=1e-03)
    True

    """
    sqrt = math.sqrt

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


def matrix_from_basis_vectors(xaxis, yaxis):
    """Creates a rotation matrix from basis vectors (= orthonormal vectors).

    Parameters
    ----------
    xaxis : list of float
        The x-axis of the frame.
    yaxis : list of float
        The y-axis of the frame.

    Returns
    -------
    list of list of float
        A 4x4 transformation matrix representing a rotation.

    Examples
    --------
    >>> xaxis = [0.68, 0.68, 0.27]
    >>> yaxis = [-0.67, 0.73, -0.15]
    >>> R = matrix_from_basis_vectors(xaxis, yaxis)

    Notes
    -----
    .. code-block:: none

        [ x0  y0  z0  0 ]
        [ x1  y1  z1  0 ]
        [ x2  y2  z2  0 ]
        [  0   0   0  1 ]

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


def basis_vectors_from_matrix(R):
    """Returns the basis vectors from the rotation matrix R.

    Raises
    ------
    ValueError
        If rotation matrix is invalid.

    Returns
    -------
    list of two vectors
        The X and Y basis vectors of the rotation.

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

    return [xaxis, yaxis]


def matrix_from_translation(translation):
    """Returns a 4x4 translation matrix in row-major order.

    Parameters
    ----------
    translation : list of float
        The x, y and z components of the translation.

    Returns
    -------
    list of list of float
        The 4x4 transformation matrix representing a translation.

    Examples
    --------
    >>> T = matrix_from_translation([1, 2, 3])

    Notes
    -----
    .. code-block:: none

        [ .  .  .  0 ]
        [ .  .  .  1 ]
        [ .  .  .  2 ]
        [ .  .  .  . ]

    """
    M = identity_matrix(4)
    M[0][3] = float(translation[0])
    M[1][3] = float(translation[1])
    M[2][3] = float(translation[2])

    return M


def translation_from_matrix(M):
    """Returns the 3 values of translation from the matrix M.
    """
    return [M[0][3], M[1][3], M[2][3]]


def matrix_from_orthogonal_projection(plane):
    """Returns an orthogonal projection matrix to project onto a plane.

    Parameters
    ----------
    plane : compas.geometry.Plane or (point, normal)
        The plane to project onto.

    Returns
    -------
    list of list of float
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


def matrix_from_parallel_projection(plane, direction):
    """Returns an parallel projection matrix to project onto a plane.

    Parameters
    ----------
    plane : compas.geometry.Plane or (point, normal)
        The plane to project onto.
    direction : list of float
        Direction of the projection.

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


def matrix_from_perspective_projection(plane, center_of_projection):
    """Returns a perspective projection matrix to project onto a plane along lines that emanate from a single point, called the center of projection.

    Parameters
    ----------
    plane : compas.geometry.Plane or (point, normal)
        The plane to project onto.
    center_of_projection : compas.geometry.Point or list of float
        The camera view point.

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


def matrix_from_perspective_entries(perspective):
    """Returns a matrix from perspective entries.

    Parameters
    ----------
    values : list of float
        The 4 perspective entries of a matrix.

    Notes
    -----
    .. code-block:: none

        [ .  .  .  . ]
        [ .  .  .  . ]
        [ .  .  .  . ]
        [ 0  1  2  3 ]

    """
    M = identity_matrix(4)
    M[3][0] = float(perspective[0])
    M[3][1] = float(perspective[1])
    M[3][2] = float(perspective[2])
    M[3][3] = float(perspective[3])
    return M


def matrix_from_shear_entries(shear_entries):
    """Returns a shear matrix from the 3 factors for x-y, x-z, and y-z axes.

    Parameters
    ----------
    shear_entries : list of float
        The 3 shear factors for x-y, x-z, and y-z axes.

    Examples
    --------
    >>> Sh = matrix_from_shear_entries([1, 2, 3])

    Notes
    -----
    .. code-block:: none

        [ .  0  1  . ]
        [ .  .  2  . ]
        [ .  .  .  . ]
        [ .  .  .  . ]

    """
    M = identity_matrix(4)
    M[0][1] = float(shear_entries[0])
    M[0][2] = float(shear_entries[1])
    M[1][2] = float(shear_entries[2])
    return M


def matrix_from_shear(angle, direction, point, normal):
    """Constructs a shear matrix by an angle along the direction vector on the
    shear plane (defined by point and normal).

    Parameters
    ----------
    angle : float
        The angle in radians.
    direction : list of float
        The direction vector as list of 3 numbers.
        It must be orthogonal to the normal vector.
    point : list of float
        The point of the shear plane as list of 3 numbers.
    normal : list of float
        The normal of the shear plane as list of 3 numbers.

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
    fabs = math.fabs

    normal = normalize_vector(normal)
    direction = normalize_vector(direction)

    if fabs(dot_vectors(normal, direction)) > _EPS:
        raise ValueError('Direction and normal vectors are not orthogonal')

    angle = math.tan(angle)
    M = identity_matrix(4)

    for j in range(3):
        for i in range(3):
            M[i][j] += angle * direction[i] * normal[j]

    M[0][3], M[1][3], M[2][3] = scale_vector(direction, -angle * dot_vectors(point, normal))

    return M


def matrix_from_scale_factors(scale_factors):
    """Returns a 4x4 scaling transformation.

    Parameters
    ----------
    scale_factors : list of float
        Three numbers defining the scaling factors in x, y, and z respectively.

    Examples
    --------
    >>> Sc = matrix_from_scale_factors([1, 2, 3])

    Notes
    -----
    .. code-block:: python

        [ 0  .  .  . ]
        [ .  1  .  . ]
        [ .  .  2  . ]
        [ .  .  .  . ]

    """
    M = identity_matrix(4)
    M[0][0] = float(scale_factors[0])
    M[1][1] = float(scale_factors[1])
    M[2][2] = float(scale_factors[2])

    return M


def quaternion_from_euler_angles(e, static=True, axes='xyz'):
    """Returns a quaternion from Euler angles.

    Parameters
    ----------
    euler_angles : list
        Three numbers that represent the angles of rotations about the specified axes.
    static : bool, optional
        If ``True``, the rotations are applied to a static frame.
        If ``False``, the rotations are applied to a rotational frame.
        Defaults to ``True``.
    axes : str, optional
        A three-character string specifying the order of the axes.
        Defaults to ``'xyz'``.

    Returns
    -------
    list
        Quaternion as a list of four real values ``[w, x, y, z]``.
    """

    m = matrix_from_euler_angles(e, static, axes)
    q = quaternion_from_matrix(m)
    return q


def euler_angles_from_quaternion(q, static=True, axes='xyz'):
    """Returns Euler angles from a quaternion.

    Parameters
    ----------
    quaternion : list
        Quaternion as a list of four real values ``[w, x, y, z]``.
    static : bool, optional
        If ``True``, the rotations are applied to a static frame.
        If ``False``, the rotations are applied to a rotational frame.
        Defaults to ``True``.
    axes : str, optional
        A three-character string specifying the order of the axes.
        Defaults to ``'xyz'``.

    Returns
    -------
    list
        Euler angles as a list of three real values ``[a, b, c]``.
    """
    m = matrix_from_quaternion(q)
    e = euler_angles_from_matrix(m, static, axes)
    return e


def quaternion_from_axis_angle(axis, angle):
    """Returns a quaternion describing a rotation around the given axis by the given angle.

    Parameters
    ----------
    axis : list
        Coordinates ``[x, y, z]`` of the rotation axis vector.
    angle : float
        Angle of rotation in radians.

    Returns
    -------
    list
        Quaternion as a list of four real values ``[qw, qx, qy, qz]``.

    Examples
    --------
    >>> axis =  [1.0, 0.0, 0.0]
    >>> angle = math.pi/2
    >>> q = quaternion_from_axis_angle(axis, angle)
    >>> allclose(q, [math.sqrt(2)/2, math.sqrt(2)/2, 0, 0])
    True
    """
    m = matrix_from_axis_and_angle(axis, angle, None)
    q = quaternion_from_matrix(m)
    return q


def axis_angle_from_quaternion(q):
    """Returns an axis and an angle of rotation from the given quaternion.

    Parameters
    ----------
    q : list
        Quaternion as a list of four real values ``[qw, qx, qy, qz]``.

    Returns
    -------
    axis : list
        Coordinates ``[x, y, z]`` of the rotation axis vector.
    angle : float
        Angle of rotation in radians.

    Examples
    --------
    >>> q = [1., 1., 0., 0.]
    >>> axis, angle = axis_angle_from_quaternion(q)
    >>> allclose(axis, [1., 0., 0.])
    True
    >>> allclose([angle], [math.pi/2], 1e-6)
    True
    """

    m = matrix_from_quaternion(q)
    axis, angle = axis_and_angle_from_matrix(m)
    return axis, angle


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import doctest

    from compas.geometry import Frame  # noqa: F401
    from compas.geometry import Transformation  # noqa: F401

    doctest.testmod(globs=globals())
