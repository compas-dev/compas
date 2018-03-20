from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import math

from copy import deepcopy

from compas.geometry.basic import scale_vector
from compas.geometry.basic import scale_vector_xy
from compas.geometry.basic import normalize_vector
from compas.geometry.basic import normalize_vector_xy
from compas.geometry.basic import add_vectors
from compas.geometry.basic import add_vectors_xy
from compas.geometry.basic import subtract_vectors
from compas.geometry.basic import subtract_vectors_xy
from compas.geometry.basic import cross_vectors
from compas.geometry.basic import dot_vectors
from compas.geometry.basic import multiply_matrix_vector
from compas.geometry.basic import vector_component
from compas.geometry.basic import vector_component_xy
from compas.geometry.basic import multiply_matrices
from compas.geometry.basic import transpose_matrix
from compas.geometry.basic import length_vector
from compas.geometry.basic import norm_vector


from compas.geometry.angles import angle_vectors
from compas.geometry.average import centroid_points

from compas.geometry.intersections import intersection_line_line
from compas.geometry.intersections import intersection_line_plane
from compas.geometry.intersections import intersection_line_triangle

from compas.geometry.orientation import normal_polygon
from compas.geometry.orientation import normal_triangle

from compas.geometry.distance import closest_point_on_plane


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


__all__ = [
    'transform',
    'homogenize',
    'dehomogenize',

    'transform_numpy',
    'homogenize_numpy',
    'dehomogenize_numpy',

    'local_axes',
    'local_coords_numpy',
    'global_coords_numpy',

    'determinant',
    'inverse',
    'identity_matrix',
    'matrix_from_frame',
    'matrix_from_euler_angles',
    'euler_angles_from_matrix',
    'matrix_from_axis_and_angle',
    'matrix_from_axis_angle_vector',
    'axis_and_angle_from_matrix',
    'axis_angle_vector_from_matrix',
    'matrix_from_quaternion',
    'quaternion_from_matrix',
    'matrix_from_basis_vectors',
    'basis_vectors_from_matrix',
    'matrix_from_translation',
    'translation_from_matrix',
    'matrix_from_orthogonal_projection',
    'matrix_from_parallel_projection',
    'matrix_from_perspective_projection',
    'matrix_from_perspective_entries',
    'matrix_from_shear_entries',
    'matrix_from_shear',
    'matrix_from_scale_factors',
    'compose_matrix',
    'decompose_matrix',

    'translate_points',
    'translate_points_xy',
    'translate_lines',
    'translate_lines_xy',
    'scale_points',
    'rotate_points',
    'rotate_points_xy',
    'offset_line',
    'offset_polyline',
    'offset_polygon',
    'orient_points',
    'mirror_point_point',
    'mirror_point_point_xy',
    'mirror_points_point',
    'mirror_points_point_xy',
    'mirror_point_line',
    'mirror_point_line_xy',
    'mirror_points_line',
    'mirror_points_line_xy',
    'mirror_point_plane',
    'mirror_points_plane',
    'mirror_vector_vector',
    'reflect_line_plane',
    'reflect_line_triangle',
    'project_point_plane',
    'project_points_plane',
    'project_point_line',
    'project_point_line_xy',
    'project_points_line',
    'project_points_line_xy',
]


# epsilon for testing whether a number is close to zero
_EPS = 1e-16

# used for Euler angles: to map rotation type and axes to tuples of inner
# axis, parity, repetition, frame
_SPEC2TUPLE = {
    'sxyz': (0, 0, 0, 0), 'sxyx': (0, 0, 1, 0), 'sxzy': (0, 1, 0, 0),
    'sxzx': (0, 1, 1, 0), 'syzx': (1, 0, 0, 0), 'syzy': (1, 0, 1, 0),
    'syxz': (1, 1, 0, 0), 'syxy': (1, 1, 1, 0), 'szxy': (2, 0, 0, 0),
    'szxz': (2, 0, 1, 0), 'szyx': (2, 1, 0, 0), 'szyz': (2, 1, 1, 0),
    'rzyx': (0, 0, 0, 1), 'rxyx': (0, 0, 1, 1), 'ryzx': (0, 1, 0, 1),
    'rxzx': (0, 1, 1, 1), 'rxzy': (1, 0, 0, 1), 'ryzy': (1, 0, 1, 1),
    'rzxy': (1, 1, 0, 1), 'ryxy': (1, 1, 1, 1), 'ryxz': (2, 0, 0, 1),
    'rzxz': (2, 0, 1, 1), 'rxyz': (2, 1, 0, 1), 'rzyz': (2, 1, 1, 1)}

_NEXT_SPEC = [1, 2, 0, 1]


# TODO: move somewhere else
def allclose(l1, l2, tol = 1e-05):
    """Returns True if two lists are element-wise equal within a tolerance.

    The function is similar to NumPy's *allclose* function.
    """
    for a, b in zip(l1, l2):
        if math.fabs(a - b) > tol:
            return False
    return True


def transform(points, T):
    points = homogenize(points)
    points = transpose_matrix(multiply_matrices(T, transpose_matrix(points)))
    return dehomogenize(points)


def transform_numpy(points, T):
    from numpy import asarray

    T = asarray(T)
    points = homogenize_numpy(points)
    points = T.dot(points.T).T
    return dehomogenize_numpy(points)


# ==============================================================================
# helpers
# ==============================================================================


def homogenize(vectors, w=1.0):
    """Homogenise a list of vectors.

    Parameters
    ----------
    vectors : list
        A list of vectors.
    w : float, optional
        Homogenisation parameter.
        Defaults to ``1.0``.

    Returns
    -------
    list
        Homogenised vectors.

    Notes
    -----
    Vectors described by XYZ components are homogenised by appending a homogenisation
    parameter to the components, and by dividing each component by that parameter.
    Homogenisatioon of vectors is often used in relation to transformations.

    Examples
    --------
    >>> vectors = [[1.0, 0.0, 0.0]]
    >>> homogenize(vectors)
    [[1.0, 0.0, 0.0, 1.0]]

    """
    return [[x / w, y / w, z / w, w] for x, y, z in vectors]


def dehomogenize(vectors):
    """Dehomogenise a list of vectors.

    Parameters
    ----------
    vectors : list
        A list of vectors.

    Returns
    -------
    list
        Dehomogenised vectors.

    Examples
    --------
    >>>

    """
    return [[x * w, y * w, z * w] for x, y, z, w in vectors]


def homogenize_numpy(points):
    from numpy import asarray
    from numpy import hstack
    from numpy import ones

    points = asarray(points)
    points = hstack((points, ones((points.shape[0], 1))))
    return points


def dehomogenize_numpy(points):
    from numpy import asarray

    points = asarray(points)
    return points[:, :-1] / points[:, -1].reshape((-1, 1))


def local_axes(a, b, c):
    u = b - a
    v = c - a
    w = cross_vectors(u, v)
    v = cross_vectors(w, u)
    return normalize_vector(u), normalize_vector(v), normalize_vector(w)


def local_coords_numpy(o, uvw, xyz):
    from numpy import asarray
    from scipy.linalg import solve

    uvw = asarray(uvw).T
    xyz = asarray(xyz).T - asarray(o).reshape((-1, 1))
    rst = solve(uvw, xyz)
    return rst.T


def global_coords_numpy(o, uvw, rst):
    from numpy import asarray

    uvw = asarray(uvw).T
    rst = asarray(rst).T
    xyz = uvw.dot(rst) + asarray(o).reshape((-1, 1))
    return xyz.T


# ==============================================================================
# xforms
# ==============================================================================


def determinant(M, check=True):
    """Calculates the determinant of a square matrix M.

    Args:
        M (:obj:`list` of :obj:`list` of :obj:`float`): The square matrix of \
            any dimension.
        check (bool): If true checks if matrix is squared. Defaults to True.

    Raises:
        ValueError: If matrix is not a square matrix.

    Returns:
        (:obj:`float`): The determinant.
    """

    dim = len(M)

    if check:
        for c in M:
            if len(c) != dim:
                raise ValueError("Not a square matrix")

    if (dim == 2):
        return M[0][0] * M[1][1] - M[0][1] * M[1][0]
    else:
        i = 1
        t = 0
        sum = 0
        for t in range(dim):
            d = {}
            for t1 in range(1, dim):
                m = 0
                d[t1] = []
                for m in range(dim):
                    if (m != t):
                        d[t1].append(M[t1][m])
            M1 = [d[x] for x in d]
            sum = sum + i * M[0][t] * determinant(M1, check=False)
            i = i * (-1)
        return sum


def inverse(M):
    """Calculates the inverse of a square matrix M.

    This method uses Gaussian elimination (elementary row operations) to
    calculate the inverse. The elementary row operations are a) swap 2 rows,
    b) multiply a row by a scalar, and c) add 2 rows.

    Args:
        M (:obj:`list` of :obj:`list` of :obj:`float`): The square
            matrix of any dimension.

    Raises:
        ValueError: If the matrix is not squared
        ValueError: If the matrix is singular.
        ValueError: If the matrix is not invertible.

    Returns:
        (:obj:`list` of :obj:`list` of :obj:`float`): The inverted matrix.

    Example:
        >>> from compas.geometry import Frame
        >>> f = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
        >>> T = matrix_from_frame(f)
        >>> I = multiply_matrices(T, inverse(T))
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

    detM = determinant(M)  # raises ValueError if matrix is not squared

    if detM == 0:
        ValueError("The matrix is singular.")

    dim = len(M)

    # create identity I and copy M into C
    I = identity_matrix(dim)
    C = [[float(M[j][i]) for i in range(dim)] for j in range(dim)]

    # Perform elementary row operations
    for i in range(dim):
        e = C[i][i]

        if e == 0:
            for ii in range(dim):
                if C[ii][i] != 0:
                    for j in range(dim):
                        e = C[i][j]
                        C[i][j] = C[ii][j]
                        C[ii][j] = e
                        e = I[i][j]
                        I[i][j] = I[ii][j]
                        I[ii][j] = e
                    break
            e = C[i][i]
            if e == 0:
                ValueError("Matrix not invertible")

        for j in range(dim):
            C[i][j] = C[i][j] / e
            I[i][j] = I[i][j] / e

        for ii in range(dim):
            if ii == i:
                continue
            e = C[ii][i]
            for j in range(dim):
                C[ii][j] -= e * C[i][j]
                I[ii][j] -= e * I[i][j]

    return I


def identity_matrix(dim):
    return [[1. if i == j else 0. for i in range(dim)] for j in range(dim)]


def matrix_from_frame(frame):
    """Computes a change of basis transformation from world XY to the frame.

    Args:
        frame (:class:`compas.geometry.Frame`): a frame describing the targeted Cartesian
            coordinate system

    Example:
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


def matrix_from_euler_angles(euler_angles, static=True, axes='xyz'):
    """Calculates a rotation matrix from Euler angles.

    In 3D space any orientation can be achieved by composing three elemental
    rotations, rotations about the axes (x,y,z) of a coordinate system. A
    triple of Euler angles can be interpreted in 24 ways, which depends on if
    the rotations are applied to a static (extrinsic) or rotating (intrinsic)
    frame and the order of axes.

    Args:
        euler_angles(:obj:`list` of :obj:`float`): Three numbers that represent
            the angles of rotations about the defined axes.
        static(:obj:`bool`, optional): If true the rotations are applied to a
            static frame. If not, to a rotational. Defaults to true.
        axes(:obj:`str`, optional): A 3 character string specifying order of
            the axes. Defaults to 'xyz'.

    Example:
        >>> ea1 = 1.4, 0.5, 2.3
        >>> args = True, 'xyz'
        >>> R = matrix_from_euler_angles(ea1, *args)
        >>> ea2 = euler_angles_from_matrix(R, *args)
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

    si, sj, sk = math.sin(ai), math.sin(aj), math.sin(ak)
    ci, cj, ck = math.cos(ai), math.cos(aj), math.cos(ak)
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

    Args:
        M (:obj:`list` of :obj:`list` of :obj:`float`): The 3x3 or 4x4 matrix
            in row-major order.
        static(:obj:`bool`, optional): If true the rotations are applied to a
            static frame. If not, to a rotational. Defaults to True.
        axes(:obj:`str`, optional): A 3 character string specifying order of
            the axes. Defaults to 'xyz'.

    Returns:
        (:obj:`list` of :obj:`float`): The 3 Euler angles.

    Example:
        >>> ea1 = 1.4, 0.5, 2.3
        >>> args = True, 'xyz'
        >>> R = matrix_from_euler_angles(ea1, *args)
        >>> ea2 = euler_angles_from_matrix(R, *args)
        >>> allclose(ea1, ea2)
        True
    """

    global _SPEC2TUPLE
    global _NEXT_SPEC
    global _EPS

    if static:
        firstaxis, parity, repetition, frame = _SPEC2TUPLE["s" + axes]
    else:
        firstaxis, parity, repetition, frame = _SPEC2TUPLE["r" + axes]

    i = firstaxis
    j = _NEXT_SPEC[i + parity]
    k = _NEXT_SPEC[i - parity + 1]

    if repetition:
        sy = math.sqrt(M[i][j] * M[i][j] + M[i][k] * M[i][k])
        if sy > _EPS:
            ax = math.atan2(M[i][j], M[i][k])
            ay = math.atan2(sy, M[i][i])
            az = math.atan2(M[j][i], -M[k][i])
        else:
            ax = math.atan2(-M[j][k], M[j][j])
            ay = math.atan2(sy, M[i][i])
            az = 0.0
    else:
        cy = math.sqrt(M[i][i] * M[i][i] + M[j][i] * M[j][i])
        if cy > _EPS:
            ax = math.atan2(M[k][j], M[k][k])
            ay = math.atan2(-M[k][i], cy)
            az = math.atan2(M[j][i], M[i][i])
        else:
            ax = math.atan2(-M[j][k], M[j][j])
            ay = math.atan2(-M[k][i], cy)
            az = 0.0

    if parity:
        ax, ay, az = -ax, -ay, -az
    if frame:
        ax, az = az, ax

    return [ax, ay, az]


def matrix_from_axis_and_angle(axis, angle, point=[0, 0, 0], rtype='list'):
    """Calculates a rotation matrix from an rotation axis, an angle and an
        optional point of rotation.

    Note:
        The rotation is based on the right hand rule, i.e. anti-clockwise
        if the axis of rotation points towards the observer.

    Args:
        axis (:obj:`list` of :obj:`float`): Three numbers that
            represent the axis of rotation
        angle (:obj:`float`): The rotation angle in radians.
        point (:obj:`list` of :obj:`float`, optional): A point to
            perform a rotation around an origin other than [0, 0, 0].

    Returns:
        (:obj:`list` of :obj:`list` of :obj:`float`): The matrix.

    Example:
        >>> axis1 = normalize_vector([-0.043, -0.254, 0.617])
        >>> angle1 = 0.1
        >>> R = matrix_from_axis_and_angle(axis1, angle1)
        >>> axis2, angle2 = axis_and_angle_from_matrix(R)
        >>> allclose(axis1, axis2)
        True
        >>> allclose([angle1], [angle2])
        True
    """

    axis = list(axis)
    if length_vector(axis):
        axis = normalize_vector(axis)

    sina = math.sin(angle)
    cosa = math.cos(angle)

    R = [[cosa, 0.0, 0.0], [0.0, cosa, 0.0], [0.0, 0.0, cosa]]

    outer_product = [[axis[i] * axis[j] *
                      (1.0 - cosa) for i in range(3)] for j in range(3)]
    R = [[R[i][j] + outer_product[i][j]
          for i in range(3)] for j in range(3)]

    axis = scale_vector(axis, sina)
    m = [[0.0, -axis[2], axis[1]],
         [axis[2], 0.0, -axis[0]],
         [-axis[1], axis[0], 0.0]]

    M = [[1. if x == y else 0. for x in range(4)] for y in range(4)]
    for i in range(3):
        for j in range(3):
            R[i][j] += m[i][j]
            M[i][j] = R[i][j]

    # rotation about axis, angle AND point includes also translation
    t = subtract_vectors(point, multiply_matrix_vector(R, point))
    M[0][3] = t[0]
    M[1][3] = t[1]
    M[2][3] = t[2]

    if rtype == 'list':
        return M
    if rtype == 'array':
        from numpy import asarray
        return asarray(M)

    raise NotImplementedError


def matrix_from_axis_angle_vector(axis_angle_vector, point=[0, 0, 0]):
    """Calculates a rotation matrix from an axis-angle vector.

    Args:
        axis_angle_vector (:obj:`list` of :obj:`float`): Three numbers
            that represent the axis of rotation and angle of rotation
            through the vector's magnitude.
        point (:obj:`list` of :obj:`float`, optional): A point to
            perform a rotation around an origin other than [0, 0, 0].

    Example:
        >>> aav1 = [-0.043, -0.254, 0.617]
        >>> R = matrix_from_axis_angle_vector(aav1)
        >>> aav2 = axis_and_angle_from_matrix(R)
        >>> allclose(aav1, aav2)
        True
    """
    axis = list(axis_angle_vector)
    angle = length_vector(axis_angle_vector)
    return matrix_from_axis_and_angle(axis, angle, point)


def axis_and_angle_from_matrix(M):
    """Returns the axis and the angle of the rotation matrix M.


    """
    epsilon = 0.01  # margin to allow for rounding errors
    epsilon2 = 0.1  # margin to distinguish between 0 and 180 degrees

    if ((math.fabs(M[0][1] - M[1][0]) < epsilon) and
        (math.fabs(M[0][2] - M[2][0]) < epsilon) and
            (math.fabs(M[1][2] - M[2][1]) < epsilon)):

        if ((math.fabs(M[0][1] + M[1][0]) < epsilon2) and
            (math.fabs(M[0][2] + M[2][0]) < epsilon2) and
            (math.fabs(M[1][2] + M[2][1]) < epsilon2) and
                (math.fabs(M[0][0] + M[1][1] + M[2][2] - 3) < epsilon2)):
            return [0, 0, 0], 0
        else:
            angle = math.pi
            xx = (M[0][0] + 1) / 2
            yy = (M[1][1] + 1) / 2
            zz = (M[2][2] + 1) / 2
            xy = (M[0][1] + M[1][0]) / 4
            xz = (M[0][2] + M[2][0]) / 4
            yz = (M[1][2] + M[2][1]) / 4
            root_half = math.sqrt(0.5)
            if ((xx > yy) and (xx > zz)):
                if (xx < epsilon):
                    axis = [0, root_half, root_half]
                else:
                    x = math.sqrt(xx)
                    axis = [x, xy / x, xz / x]
            elif (yy > zz):
                if (yy < epsilon):
                    axis = [root_half, 0, root_half]
                else:
                    y = math.sqrt(yy)
                    axis = [xy / y, y, yz / y]
            else:
                if (zz < epsilon):
                    axis = [root_half, root_half, 0]
                else:
                    z = math.sqrt(zz)
                    axis = [xz / z, yz / z, z]

            return axis, angle

    s = math.sqrt(
        (M[2][1] - M[1][2]) * (M[2][1] - M[1][2]) +
        (M[0][2] - M[2][0]) * (M[0][2] - M[2][0]) +
        (M[1][0] - M[0][1]) * (M[1][0] - M[0][1]))

    if (math.fabs(s) < 0.001):
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
    """Calculates a ``Rotation`` from quaternion coefficients.

    Args:
        quaternion (:obj:`list` of :obj:`float`): Four numbers that
            represents the four coefficient values of a quaternion.

    Raises:
        ValueError: If quaternion is invalid.

    Example:
        >>> q1 = [0.945, -0.021, -0.125, 0.303]
        >>> R = matrix_from_quaternion(q1)
        >>> q2 = quaternion_from_matrix(R)
        >>> allclose(q1, q2, tol=1e-03)
        True
    """
    q = quaternion
    n = q[0]**2 + q[1]**2 + q[2]**2 + q[3]**2  # dot product

    epsilon = 1.0e-15

    if n < epsilon:
        raise ValueError("Invalid quaternion, dot product must be != 0.")

    q = [v * math.sqrt(2.0 / n) for v in q]
    q = [[q[i] * q[j] for i in range(4)]
         for j in range(4)]  # outer_product

    rotation = [
        [1.0 - q[2][2] - q[3][3], q[1][2] - q[3][0], q[1][3] + q[2][0], 0.0],
        [q[1][2] + q[3][0], 1.0 - q[1][1] - q[3][3], q[2][3] - q[1][0], 0.0],
        [q[1][3] - q[2][0], q[2][3] + q[1][0], 1.0 - q[1][1] - q[2][2], 0.0],
        [0.0, 0.0, 0.0, 1.0]]
    return rotation


def quaternion_from_matrix(M):
    """Returns the 4 quaternion coefficients from a rotation matrix.

    Args:
        M (:obj:`list` of :obj:`list` of :obj:`float`): The rotation matrix.

    Returns:
        (:obj:`list` of :obj:`float`): The quaternion coefficients.

    Example:
        >>> q1 = [0.945, -0.021, -0.125, 0.303]
        >>> R = matrix_from_quaternion(q1)
        >>> q2 = quaternion_from_matrix(R)
        >>> allclose(q1, q2, tol=1e-03)
        True
    """

    qw, qx, qy, qz = 0, 0, 0, 0
    trace = M[0][0] + M[1][1] + M[2][2]

    if trace > 0.0:
        s = (0.5 / math.sqrt(trace + 1.0))
        qw = 0.25 / s
        qx = (M[2][1] - M[1][2]) * s
        qy = (M[0][2] - M[2][0]) * s
        qz = (M[1][0] - M[0][1]) * s

    elif ((M[0][0] > M[1][1]) and (M[0][0] > M[2][2])):
        s = 2.0 * math.sqrt(1.0 + M[0][0] - M[1][1] - M[2][2])
        qw = (M[2][1] - M[1][2]) / s
        qx = 0.25 * s
        qy = (M[0][1] + M[1][0]) / s
        qz = (M[0][2] + M[2][0]) / s

    elif (M[1][1] > M[2][2]):
        s = 2.0 * math.sqrt(1.0 + M[1][1] - M[0][0] - M[2][2])
        qw = (M[0][2] - M[2][0]) / s
        qx = (M[0][1] + M[1][0]) / s
        qy = 0.25 * s
        qz = (M[1][2] + M[2][1]) / s
    else:
        s = 2.0 * math.sqrt(1.0 + M[2][2] - M[0][0] - M[1][1])
        qw = (M[1][0] - M[0][1]) / s
        qx = (M[0][2] + M[2][0]) / s
        qy = (M[1][2] + M[2][1]) / s
        qz = 0.25 * s

    return [qw, qx, qy, qz]


def matrix_from_basis_vectors(xaxis, yaxis):
    """Creates a rotation matrix from basis vectors (= orthonormal vectors).

    Args:
        xaxis (:obj:`list` oof :obj:`float`): The x-axis of the frame.
        yaxis (:obj:`list` oof :obj:`float`): The y-axis of the frame.

    Example:
        >>> xaxis = [0.68, 0.68, 0.27]
        >>> yaxis = [-0.67, 0.73, -0.15]
        >>> R = matrix_from_basis_vectors(xaxis, yaxis)
    """
    xaxis = normalize_vector(list(xaxis))
    yaxis = normalize_vector(list(yaxis))
    zaxis = cross_vectors(xaxis, yaxis)
    yaxis = cross_vectors(zaxis, xaxis)  # correction

    R = identity_matrix(4)
    R[0][0], R[1][0], R[2][0] = xaxis
    R[0][1], R[1][1], R[2][1] = yaxis
    R[0][2], R[1][2], R[2][2] = zaxis
    return R


def basis_vectors_from_matrix(R):
    """Returns the basis vectors from the rotation matrix R.

    Raises:
        ValueError: If rotation matrix is invalid.

    Example:
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
    else:
        return [xaxis, yaxis]


def matrix_from_translation(translation, rtype='list'):
    """Returns a 4x4 translation matrix in row-major order.

    Args:
        translation (:obj:`list` of :obj:`float`): The x, y and z components
            of the translation.

    Example:
        >>> T = matrix_from_translation([1, 2, 3])
    """
    M = identity_matrix(4)
    M[0][3] = float(translation[0])
    M[1][3] = float(translation[1])
    M[2][3] = float(translation[2])

    if rtype == 'list':
        return M
    if rtype == 'array':
        from numpy import asarray
        return asarray(M)

    raise NotImplementedError


def translation_from_matrix(M):
    """Returns the 3 values of translation from the matrix M.
    """
    return [M[0][3], M[1][3], M[2][3]]

def matrix_from_orthogonal_projection(point, normal):
    """Returns an orthogonal projection matrix to project onto a plane \
        defined by point and normal.

    Args:
        point(:obj:`list` of :obj:`float`)
        normal(:obj:`list` of :obj:`float`)

    Example:
        >>> point = [0, 0, 0]
        >>> normal = [0, 0, 1]
        >>> P = matrix_from_orthogonal_projection(point, normal)
    """
    T = identity_matrix(4)
    normal = normalize_vector(normal)

    for j in range(3):
        for i in range(3):
            T[i][j] -= normal[i] * normal[j]  # outer_product

    T[0][3], T[1][3], T[2][3] = scale_vector(
        normal, dot_vectors(point, normal))
    return T

def matrix_from_parallel_projection(point, normal, direction):
    """Returns an parallel projection matrix to project onto a plane defined \
        by point, normal and direction.

    Args:
        point(:obj:`list` of :obj:`float`)
        normal(:obj:`list` of :obj:`float`)
        direction(:obj:`list` of :obj:`float`)

    Example:
        >>> point = [0, 0, 0]
        >>> normal = [0, 0, 1]
        >>> direction = [1, 1, 1]
        >>> P = matrix_from_parallel_projection(point, normal, direction)
    """
    T = identity_matrix(4)
    normal = normalize_vector(normal)

    scale = dot_vectors(direction, normal)
    for j in range(3):
        for i in range(3):
            T[i][j] -= direction[i] * normal[j] / scale

    T[0][3], T[1][3], T[2][3] = scale_vector(
        direction, dot_vectors(point, normal) / scale)
    return T

def matrix_from_perspective_projection(point, normal, perspective):
    """Returns an perspective projection matrix to project onto a plane \
        defined by point, normal and perspective.

    Args:
        point(:obj:`list` of :obj:`float`)
        normal(:obj:`list` of :obj:`float`)
        perspective(:obj:`list` of :obj:`float`)

    Example:
        >>> point = [0, 0, 0]
        >>> normal = [0, 0, 1]
        >>> perspective = [1, 1, 0]
        >>> P = matrix_from_perspective_projection(point, normal, perspective)
    """
    T = identity_matrix(4)
    normal = normalize_vector(normal)

    T[0][0] = T[1][1] = T[2][2] = dot_vectors(
        subtract_vectors(perspective, point), normal)

    for j in range(3):
        for i in range(3):
            T[i][j] -= perspective[i] * normal[j]

    T[0][3], T[1][3], T[2][3] = scale_vector(
        perspective, dot_vectors(point, normal))
    for i in range(3):
        T[3][i] -= normal[i]
    T[3][3] = dot_vectors(perspective, normal)
    return T

def matrix_from_perspective_entries(perspective):
    """Returns a matrix from perspective entries.

    Args:
        values(:obj:`list` of :obj:`float`): The 4 perspective entries of a
            matrix.
    """
    M = identity_matrix(4)
    M[3][0] = float(perspective[0])
    M[3][1] = float(perspective[1])
    M[3][2] = float(perspective[2])
    M[3][3] = float(perspective[3])
    return M


def matrix_from_shear_entries(shear_entries):
    """Returns a shear matrix from the 3 factors for x-y, x-z, and y-z axes.

    Args:
        shear_entries (:obj:`list` of :obj:`float`): The 3 shear factors for
            x-y, x-z, and y-z axes.

    Example:
        >>> Sh = matrix_from_shear_entries([1, 2, 3])
    """
    M = identity_matrix(4)
    M[0][1] = float(shear_entries[0])
    M[0][2] = float(shear_entries[1])
    M[1][2] = float(shear_entries[2])
    return M


def matrix_from_shear(angle, direction, point, normal):
    """Constructs a shear matrix by an angle along the direction vector on \
        the shear plane (defined by point and normal).

    A point P is transformed by the shear matrix into P" such that
    the vector P-P" is parallel to the direction vector and its extent is
    given by the angle of P-P'-P", where P' is the orthogonal projection
    of P onto the shear plane (defined by point and normal).

    Args:
        angle (:obj:`float`): The angle in radians.
        direction (:obj:`list` of :obj:`float`): The direction vector as
            list of 3 numbers. It must be orthogonal to the normal vector.
        point (:obj:`list` of :obj:`float`): The point of the shear plane
            as list of 3 numbers.
        normal (:obj:`list` of :obj:`float`): The normal of the shear plane
            as list of 3 numbers.

    Raises:
        ValueError: If direction and normal are not orthogonal.

    Example:
        >>> angle = 0.1
        >>> direction = [0.1, 0.2, 0.3]
        >>> point = [4, 3, 1]
        >>> normal = cross_vectors(direction, [1, 0.3, -0.1])
        >>> S = matrix_from_shear(angle, direction, point, normal)
    """

    normal = normalize_vector(normal)
    direction = normalize_vector(direction)

    if math.fabs(dot_vectors(normal, direction)) > _EPS:
        raise ValueError('Direction and normal vectors are not orthogonal')

    angle = math.tan(angle)
    M = [[1. if i == j else 0. for i in range(4)] for j in range(4)]

    for j in range(3):
        for i in range(3):
            M[i][j] += angle * direction[i] * normal[j]

    M[0][3], M[1][3], M[2][3] = scale_vector(
        direction, -angle * dot_vectors(point, normal))

    return M


def matrix_from_scale_factors(scale_factors, rtype='list'):
    """Returns a 4x4 scaling transformation.

    Args:
        scale_factors (:obj:`list` of :obj:`float`):  Three numbers defining
            the scaling factors in x, y, and z respectively.

    Example:
        >>> Sc = matrix_from_scale_factors([1, 2, 3])
    """
    M = identity_matrix(4)
    M[0][0] = float(scale_factors[0])
    M[1][1] = float(scale_factors[1])
    M[2][2] = float(scale_factors[2])

    if rtype == 'list':
        return M
    if rtype == 'array':
        from numpy import asarray
        return asarray(M)

    raise NotImplementedError


def decompose_matrix(M):
    """Calculates the components of rotation, translation, scale, shear, \
        and perspective of a given transformation matrix M.

    Returns:

        scale (:obj:`list` of :obj:`float`): The 3 scale factors in x-, y-, \
            and z-direction.

        shear (:obj:`list` of :obj:`float`): The 3 shear factors for x-y, \
            x-z, and y-z axes.

        angles (:obj:`list` of :obj:`float`): The rotation specified through \
            the 3 Euler angles about static x, y, z axes.

        translation (:obj:`list` of :obj:`float`): The 3 values of \
            translation

        perspective (:obj:`list` of :obj:`float`): The 4 perspective entries \
            of the matrix.

    Raises:
        ValueError: If matrix is singular or degenerative.

    Example:
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

    """

    detM = determinant(M)  # raises ValueError if matrix is not squared

    if detM == 0:
        ValueError("The matrix is singular.")

    Mt = transpose_matrix(M)

    if abs(Mt[3][3]) < _EPS:
        raise ValueError('The element [3,3] of the matrix is zero.')

    for i in range(4):
        for j in range(4):
            Mt[i][j] /= Mt[3][3]

    translation = [M[0][3], M[1][3], M[2][3]]

    # scale, shear, rotation
    # copy Mt[:3, :3] into row
    scale = [0.0, 0.0, 0.0]
    shear = [0.0, 0.0, 0.0]
    angles = [0.0, 0.0, 0.0]

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

    # use base vectors??
    angles[1] = math.asin(-row[0][2])
    if math.cos(angles[1]):
        angles[0] = math.atan2(row[1][2], row[2][2])
        angles[2] = math.atan2(row[0][1], row[0][0])
    else:
        angles[0] = math.atan2(-row[2][1], row[1][1])
        angles[2] = 0.0

    # perspective
    if math.fabs(Mt[0][3]) > _EPS and math.fabs(Mt[1][3]) > _EPS and \
            math.fabs(Mt[2][3]) > _EPS:
        P = deepcopy(Mt)
        P[0][3], P[1][3], P[2][3], P[3][3] = 0.0, 0.0, 0.0, 1.0
        Ptinv = inverse(transpose_matrix(P))
        perspective = multiply_matrix_vector(Ptinv, [Mt[0][3], Mt[1][3],
                                                     Mt[2][3], Mt[3][3]])
    else:
        perspective = [0.0, 0.0, 0.0, 1.0]

    return scale, shear, angles, translation, perspective


def compose_matrix(scale=None, shear=None, angles=None,
                   translation=None, perspective=None):
    """Calculates a matrix from the components of scale, shear, euler_angles, \
        translation and perspective.

    Args:
        scale (:obj:`list` of :obj:`float`): The 3 scale factors in x-, y-,
            and z-direction. Defaults to None.
        shear (:obj:`list` of :obj:`float`): The 3 shear factors for x-y,
            x-z, and y-z axes. Defaults to None.
        angles (:obj:`list` of :obj:`float`): The rotation specified
            through the 3 Euler angles about static x, y, z axes. Defaults to
            None.
        translation (:obj:`list` of :obj:`float`): The 3 values of
            translation. Defaults to None.
        perspective (:obj:`list` of :obj:`float`): The 4 perspective entries
            of the matrix. Defaults to None.

    Example:
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
        Sh = matrix_from_shear_entries(shear)
        M = multiply_matrices(M, Sh)
    if scale is not None:
        Sc = matrix_from_scale_factors(scale)
        M = multiply_matrices(M, Sc)
    for i in range(4):
        for j in range(4):
            M[i][j] /= M[3][3]
    return M



# ==============================================================================
# translate
# ==============================================================================


def translate_points(points, vector):
    return [add_vectors(point, vector) for point in points]


def translate_points_xy(points, vector):
    return [add_vectors_xy(point, vector) for point in points]


def translate_lines(lines, vector):
    sps, eps = zip(*lines)
    sps = translate_points(sps, vector)
    eps = translate_points(eps, vector)
    return zip(sps, eps)


def translate_lines_xy(lines, vector):
    sps, eps = zip(*lines)
    sps = translate_points_xy(sps, vector)
    eps = translate_points_xy(eps, vector)
    return zip(sps, eps)


# ==============================================================================
# scale
# ==============================================================================


def scale_points(points, scale):
    T = matrix_from_scale_factors([scale, scale, scale])
    return transform(points, T)


# ==============================================================================
# rotate
# ==============================================================================


def rotate_points(points, axis, angle, origin=None):
    """Rotates points around an arbitrary axis in 3D (radians).

    Parameters:
        points (sequence of sequence of float): XYZ coordinates of the points.
        axis (sequence of float): The rotation axis.
        angle (float): the angle of rotation in radians.
        origin (sequence of float): Optional. The origin of the rotation axis.
            Default is ``[0.0, 0.0, 0.0]``.

    Returns:
        list: the rotated points

    Notes:
        For more info, see [1]_.

    References:
        .. [1] Wikipedia. *Rotation matrix*.
               Available at: https://en.wikipedia.org/wiki/Rotation_matrix.

    """
    # rotation matrix
    R = matrix_from_axis_and_angle(angle, axis, origin)
    # apply rotation
    points = transform(points, R)
    return points


def rotate_points_xy(points, axis, angle, origin=None):
    """Rotates points around an arbitrary axis in 2D.

    Parameters:
        points (sequence of sequence of float): XY coordinates of the points.
        axis (sequence of float): The rotation axis.
        angle (float): the angle of rotation in radians.
        origin (sequence of float): Optional. The origin of the rotation axis.
            Default is ``[0.0, 0.0, 0.0]``.

    Returns:
        list: the rotated points

    Notes:
        For more info, see [1]_.

    References:
        .. [1] Wikipedia. *Rotation matrix*.
               Available at: https://en.wikipedia.org/wiki/Rotation_matrix.

    """
    if not origin:
        origin = [0.0, 0.0]
    # rotation matrix
    x, y = normalize_vector_xy(axis)
    cosa = math.cos(angle)
    sina = math.sin(angle)
    R = [[cosa, -sina], [sina, cosa]]
    # translate points
    points = translate_points_xy(points, scale_vector_xy(origin, -1.0))
    # rotate points
    points = [multiply_matrix_vector(R, point) for point in points]
    # translate points back
    points = translate_points_xy(points, origin)
    return points


# ==============================================================================
# offset
# ==============================================================================


def offset_line(line, distance, normal=[0., 0., 1.]):
    """Offset a line by a distance.

    Parameters:
        line (tuple): Two points defining the line.
        distances (float or tuples of floats): The offset distance as float.
            A single value determines a constant offset. Alternatively, two
            offset values for the start and end point of the line can be used to
            a create variable offset.
        normal (tuple): The normal of the offset plane.

    Returns:
        offset line (tuple): Two points defining the offset line.

    Examples:

        .. code-block:: python

            line = [(0.0, 0.0, 0.0), (3.0, 3.0, 0.0)]

            distance = 0.2 # constant offset
            line_offset = offset_line(line, distance)
            print(line_offset)

            distance = [0.2, 0.1] # variable offset
            line_offset = offset_line(line, distance)
            print(line_offset)

    """
    pt1, pt2 = line[0], line[1]
    vec = subtract_vectors(pt1, pt2)
    dir_vec = normalize_vector(cross_vectors(vec, normal))

    if isinstance(distance, list) or isinstance(distance, tuple):
        distances = distance
    else:
        distances = [distance, distance]

    vec_pt1 = scale_vector(dir_vec, distances[0])
    vec_pt2 = scale_vector(dir_vec, distances[1])
    pt1_new = add_vectors(pt1, vec_pt1)
    pt2_new = add_vectors(pt2, vec_pt2)
    return pt1_new, pt2_new


def offset_polygon(polygon, distance):
    """Offset a polygon (closed) by a distance.

    Parameters:
        polygon (sequence of sequence of floats): The XYZ coordinates of the
            corners of the polygon. The first and last coordinates must be identical.
        distance (float or list of tuples of floats): The offset distance as float.
            A single value determines a constant offset globally. Alternatively, pairs of local
            offset values per line segment can be used to create variable offsets.
            Distance > 0: offset to the outside, distance < 0: offset to the inside

    Returns:
        offset polygon (sequence of sequence of floats): The XYZ coordinates of the
            corners of the offset polygon. The first and last coordinates are identical.

    Notes:
        The offset direction is determined by the normal of the polygon. The
        algorithm works also for spatial polygons that do not perfectly fit a plane.

    Examples:

        .. code-block:: python

            polygon = [
                (0.0, 0.0, 0.0),
                (3.0, 0.0, 1.0),
                (3.0, 3.0, 2.0),
                (1.5, 1.5, 2.0),
                (0.0, 3.0, 1.0),
                (0.0, 0.0, 0.0)
                ]

            distance = 0.5 # constant offset
            polygon_offset = offset_polygon(polygon, distance)
            print(polygon_offset)

            distance = [
                (0.1, 0.2),
                (0.2, 0.3),
                (0.3, 0.4),
                (0.4, 0.3),
                (0.3, 0.1)
                ] # variable offset
            polygon_offset = offset_polygon(polygon, distance)
            print(polygon_offset)

    """
    normal = normal_polygon(polygon)

    if isinstance(distance, list) or isinstance(distance, tuple):
        distances = distance
        if len(distances) < len(polygon):
            distances = distances + [distances[-1]] * (len(polygon) - len(distances) - 1)
    else:
        distances = [[distance, distance]] * len(polygon)

    lines = [polygon[i:i + 2] for i in range(len(polygon[:-1]))]
    lines_offset = []
    for i, line in enumerate(lines):
        lines_offset.append(offset_line(line, distances[i], normal))

    polygon_offset = []

    for i in range(len(lines_offset)):
        intx_pt1, intx_pt2 = intersection_line_line(lines_offset[i - 1], lines_offset[i])

        if intx_pt1 and intx_pt2:
            polygon_offset.append(centroid_points([intx_pt1, intx_pt2]))
        else:
            polygon_offset.append(lines_offset[i][0])

    polygon_offset.append(polygon_offset[0])
    return polygon_offset


def offset_polyline(polyline, distance, normal=[0., 0., 1.]):
    """Offset a polyline by a distance.

    Parameters:
        polyline (sequence of sequence of floats): The XYZ coordinates of the
            vertices of a polyline.
        distance (float or list of tuples of floats): The offset distance as float.
            A single value determines a constant offset globally. Alternatively, pairs of local
            offset values per line segment can be used to create variable offsets.
            Distance > 0: offset to the "left", distance < 0: offset to the "right"
        normal (tuple): The normal of the offset plane.

    Returns:
        offset polyline (sequence of sequence of floats): The XYZ coordinates of the resulting polyline.

    """

    if isinstance(distance, list) or isinstance(distance, tuple):
        distances = distance
        if len(distances) < len(polyline):
            distances = distances + [distances[-1]] * (len(polyline) - len(distances) - 1)
    else:
        distances = [[distance, distance]] * len(polyline)

    lines = [polyline[i:i + 2] for i in range(len(polyline[:-1]))]
    lines_offset = []
    for i, line in enumerate(lines):
        lines_offset.append(offset_line(line, distances[i], normal))

    polyline_offset = []
    polyline_offset.append(lines_offset[0][0])
    for i in range(len(lines_offset[:-1])):
        intx_pt1, intx_pt2 = intersection_line_line(lines_offset[i], lines_offset[i + 1])

        if intx_pt1 and intx_pt2:
            polyline_offset.append(centroid_points([intx_pt1, intx_pt2]))
        else:
            polyline_offset.append(lines_offset[i][0])
    polyline_offset.append(lines_offset[-1][1])
    return polyline_offset


# ==============================================================================
# orientation
# ==============================================================================


def orient_points(points, reference_plane=None, target_plane=None):
    """Orient points from one plane to another.

    Parameters:
        points (sequence of sequence of float): XYZ coordinates of the points.
        reference_plane (tuple): Base point and normal defining a reference plane.
        target_plane (tuple): Base point and normal defining a target plane.

    Returns:
        points (sequence of sequence of float): XYZ coordinates of the oriented points.

    Notes:
        This function is useful to orient a planar problem in the xy-plane to simplify
        the calculation (see example).

    Examples:

        .. code-block:: python

            from compas.geometry import orient_points
            from compas.geometry import intersection_segment_segment_xy

            reference_plane = [(0.57735,0.57735,0.57735),(1.0, 1.0, 1.0)]

            line_a = [
                (0.288675,0.288675,1.1547),
                (0.866025,0.866025, 0.)
                ]

            line_b = [
                (1.07735,0.0773503,0.57735),
                (0.0773503,1.07735,0.57735)
                ]

            # orient lines to lie in the xy-plane
            line_a_xy = orient_points(line_a, reference_plane)
            line_b_xy = orient_points(line_b, reference_plane)

            # compute intersection in 2d in the xy-plane
            intx_point_xy = intersection_segment_segment_xy(line_a_xy, line_b_xy)

            # re-orient resulting intersection point to lie in the reference plane
            intx_point = orient_points([intx_point_xy], target_plane=reference_plane)[0]
            print(intx_point)

    """
    if not target_plane:
        target_plane = [(0., 0., 0.,), (0., 0., 1.)]

    if not reference_plane:
        reference_plane = [(0., 0., 0.,), (0., 0., 1.)]

    vec_rot = cross_vectors(reference_plane[1], target_plane[1])
    angle = angle_vectors(reference_plane[1], target_plane[1])
    if angle:
        points = rotate_points(points, vec_rot, angle, reference_plane[0])
    vec_trans = subtract_vectors(target_plane[0], reference_plane[0])
    points = translate_points(points, vec_trans)
    return points


# ==============================================================================
# mirror
# ==============================================================================


def mirror_point_point(point, mirror):
    """Mirror a point about a point.

    Parameters:
        point (sequence of float): XYZ coordinates of the point to mirror.
        mirror (sequence of float): XYZ coordinates of the mirror point.

    """
    return add_vectors(mirror, subtract_vectors(mirror, point))


def mirror_point_point_xy(point, mirror):
    """Mirror a point about a point.

    Parameters:
        point (sequence of float): XY coordinates of the point to mirror.
        mirror (sequence of float): XY coordinates of the mirror point.

    """
    return add_vectors_xy(mirror, subtract_vectors_xy(mirror, point))


def mirror_points_point(points, mirror):
    """Mirror multiple points about a point."""
    return [mirror_point_point(point, mirror) for point in points]


def mirror_points_point_xy(points, mirror):
    """Mirror multiple points about a point."""
    return [mirror_point_point_xy(point, mirror) for point in points]


def mirror_point_line(point, line):
    pass


def mirror_point_line_xy(point, line):
    pass


def mirror_points_line(points, line):
    pass


def mirror_points_line_xy(point, line):
    pass


def mirror_point_plane(point, plane):
    """Mirror a point about a plane."""
    p1 = closest_point_on_plane(point, plane)
    vec = subtract_vectors(p1, point)
    return add_vectors(p1, vec)


def mirror_points_plane(points, plane):
    """Mirror multiple points about a plane."""
    return [mirror_point_plane(point, plane) for point in points]


def mirror_vector_vector(v1, v2):
    """Mirrors vector about vector.

    Parameters:
        v1 (tuple, list, Vector): The vector.
        v2 (tuple, list, Vector): The normalized vector as mirror axis

    Returns:
        Tuple: mirrored vector

    Notes:
        For more info, see [1]_.

    References:
        .. [1] Math Stack Exchange. *How to get a reflection vector?*
               Available at: https://math.stackexchange.com/questions/13261/how-to-get-a-reflection-vector.

    """
    return subtract_vectors(v1, scale_vector(v2, 2 * dot_vectors(v1, v2)))


# ==============================================================================
# reflect
# ==============================================================================


def reflect_line_plane(line, plane, epsilon=1e-6):
    """Reflects a line at plane.

    Parameters:
        line (tuple): Two points defining the line.
        plane (tuple): The base point and normal (normalized) defining the plane.

    Returns:
        line (tuple): The reflected line starting at the reflection point on the plane,
        None otherwise.

    Notes:
        The directions of the line and plane are important! The line will only be
        reflected if it points (direction start -> end) in the direction of the plane
        and if the line intersects with the front face of the plane (normal direction
        of the plane).
        For more info, see [1]_.

    References:
        .. [1] Math Stack Exchange. *How to get a reflection vector?*
               Available at: https://math.stackexchange.com/questions/13261/how-to-get-a-reflection-vector.

    Examples:

        .. code-block:: python

            from math import pi, sin, cos, radians

            from compas.geometry import rotate_points
            from compas.geometry import intersection_line_plane
            from compas.geometry import reflect_line_plane

            # planes
            mirror_plane = [(0.0, 0.0, 0.0),(1.0, 0.0, 0.0)]
            projection_plane = [(40.0, 0.0, 0.0),(1.0, 0.0, 0.0)]

            # initial line (starting laser ray)
            line = [(30., 0.0, -10.0),(0.0, 0.0, 0.0)]

            dmax = 75 # steps (resolution)
            angle = radians(12)  # max rotation of mirror plane in degrees
            axis_z = [0.0, 0.0, 1.0] # rotation z-axis of mirror plane
            axis_y = [0.0, 1.0, 0.0] # rotation y-axis of mirror plane

            polyline_projection = []
            for i in range(dmax):
                plane_norm = rotate_points([mirror_plane[1]], axis_z, angle * math.sin(i / dmax * 2 * pi))[0]
                plane_norm = rotate_points([plane_norm], axis_y, angle * math.sin(i / dmax * 4 * pi))[0]
                reflected_line = reflect_line_plane(line, [mirror_plane[0],plane_norm])
                if not reflected_line:
                    continue
                intx_pt = intersection_line_plane(reflected_line,projection_plane)
                if intx_pt:
                    polyline_projection.append(intx_pt)

            print(polyline_projection)


    Notes:
        This example visualized in Rhino:


    .. image:: /_images/reflect_line_plane.*

    """
    intx_pt = intersection_line_plane(line, plane, epsilon)
    if not intx_pt:
        return None
    vec_line = subtract_vectors(line[1], line[0])
    vec_reflect = mirror_vector_vector(vec_line, plane[1])
    if angle_vectors(plane[1], vec_reflect) > 0.5 * math.pi:
        return None
    return [intx_pt, add_vectors(intx_pt, vec_reflect)]


def reflect_line_triangle(line, triangle, epsilon=1e-6):
    """Reflects a line at a triangle.

    Parameters:
        line (tuple): Two points defining the line.
        triangle (sequence of sequence of float): XYZ coordinates of the triangle corners.

    Returns:
        line (tuple): The reflected line starting at the reflection point on the plane,
        None otherwise.

    Notes:
        The directions of the line and triangular face are important! The line will only be
        reflected if it points (direction start -> end) in the direction of the triangular
        face and if the line intersects with the front face of the triangular face (normal
        direction of the face).

    Examples:

        .. code-block:: python

            # tetrahedron points
            pt1 = (0.0, 0.0, 0.0)
            pt2 = (6.0, 0.0, 0.0)
            pt3 = (3.0, 5.0, 0.0)
            pt4 = (3.0, 2.0, 4.0)

            # triangular tetrahedron faces
            tris = []
            tris.append([pt4,pt2,pt1])
            tris.append([pt4,pt3,pt2])
            tris.append([pt4,pt1,pt3])
            tris.append([pt1,pt2,pt3])

            # initial line (starting ray)
            line = [(1.0,1.0,0.0),(1.0,1.0,1.0)]

            # start reflection cycle inside the prism
            polyline = []
            polyline.append(line[0])
            for i in range(10):
                for tri in tris:
                    reflected_line = reflect_line_triangle(line, tri)
                    if reflected_line:
                        line = reflected_line
                        polyline.append(line[0])
                        break

            print(polyline)


    .. figure:: /_images/reflect_line_triangle.*
        :figclass: figure
        :class: figure-img img-fluid

    """
    intx_pt = intersection_line_triangle(line, triangle, epsilon)
    if not intx_pt:
        return None
    vec_line = subtract_vectors(line[1], line[0])
    vec_normal = normal_triangle(triangle, unitized=True)
    vec_reflect = mirror_vector_vector(vec_line, vec_normal)
    if angle_vectors(vec_normal, vec_reflect) > 0.5 * math.pi:
        return None
    return [intx_pt, add_vectors(intx_pt, vec_reflect)]


# ==============================================================================
# project
# ==============================================================================


def project_point_plane(point, plane):
    """Project a point onto a plane.

    Parameters:
        point (sequence of float): XYZ coordinates of the original point.
        plane (tuple): Base poin.t and normal vector defining the plane

    Returns:
        list: XYZ coordinates of the projected point.

    Notes:
        The projection is in the direction perpendicular to the plane.
        The projected point is thus the closest point on the plane to the original
        point [1]_.

    References:
        .. [1] Math Stack Exchange. *Project a point in 3D on a given plane*.
               Available at: https://math.stackexchange.com/questions/444968/project-a-point-in-3d-on-a-given-plane.

    Examples:

        >>> from compas.geometry import project_point_plane
        >>> point = [3.0, 3.0, 3.0]
        >>> plane = ([0.0, 0.0, 0.0], [0.0, 0.0, 1.0])  # the XY plane
        >>> project_point_plane(point, plane)
        [3.0, 3.0, 3.0]

    """
    base, normal = plane
    normal = normalize_vector(normal)
    vector = subtract_vectors(point, base)
    snormal = scale_vector(normal, dot_vectors(vector, normal))
    return subtract_vectors(point, snormal)


def project_points_plane(points, plane):
    """Project multiple points onto a plane.

    Parameters:
        points (sequence of sequence of float): Cloud of XYZ coordinates.
        plane (tuple): Base point and normal vector defining the projection plane.

    Returns:
        list of list: The XYZ coordinates of the projected points.

    See Also:
        :func:`project_point_plane`

    """
    return [project_point_plane(point, plane) for point in points]


def project_point_line(point, line):
    """Project a point onto a line.

    Parameters:
        point (sequence of float): XYZ coordinates.
        line (tuple): Two points defining a line.

    Returns:
        list: XYZ coordinates of the projected point.

    Notes:
        For more info, see [1]_.

    References:
        .. [1] Wiki Books. *Linear Algebra/Orthogonal Projection Onto a Line*.
               Available at: https://en.wikibooks.org/wiki/Linear_Algebra/Orthogonal_Projection_Onto_a_Line.

    """
    a, b = line
    ab = subtract_vectors(b, a)
    ap = subtract_vectors(point, a)
    c = vector_component(ap, ab)

    return add_vectors(a, c)


def project_point_line_xy(point, line):
    """Project a point onto a line.

    Parameters:
        point (sequence of float): XY coordinates.
        line (tuple): Two points defining a line.

    Returns:
        list: XY coordinates of the projected point.

    Notes:
        For more info, see [1]_.

    References:
        .. [1] Wiki Books. *Linear Algebra/Orthogonal Projection Onto a Line*.
               Available at: https://en.wikibooks.org/wiki/Linear_Algebra/Orthogonal_Projection_Onto_a_Line.

    """
    a, b = line
    ab = subtract_vectors_xy(b, a)
    ap = subtract_vectors_xy(point, a)
    c = vector_component_xy(ap, ab)
    return add_vectors_xy(a, c)


def project_points_line(points, line):
    """Project multiple points onto a line."""
    return [project_point_line(point, line) for point in points]


def project_points_line_xy(points, line):
    """Project multiple points onto a line."""
    return [project_point_line_xy(point, line) for point in points]


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    from numpy import array
    from numpy import vstack

    from numpy.random import randint

    import matplotlib.pyplot as plt

    n = 200

    points = randint(0, high=100, size=(n, 3)).astype(float)
    points = vstack((points, array([[0, 0, 0], [100, 0, 0]], dtype=float).reshape((-1, 3))))

    a = math.pi / randint(1, high=8)

    R = matrix_from_axis_and_angle([0, 0, 1], a, point=[0, 0, 0], rtype='array')

    points_ = transform_numpy(points, R)

    plt.plot(points[:, 0], points[:, 1], 'bo')
    plt.plot(points_[:, 0], points_[:, 1], 'ro')

    plt.plot(points[-2:, 0], points[-2:, 1], 'b-', label='before')
    plt.plot(points_[-2:, 0], points_[-2:, 1], 'r-', label='after')

    plt.legend(title='Rotation {0}'.format(180 * a / math.pi), fancybox=True)

    ax = plt.gca()
    ax.set_aspect('equal')

    plt.show()
