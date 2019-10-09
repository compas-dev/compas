from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import math

from copy import deepcopy

from compas.geometry.basic import normalize_vector
from compas.geometry.basic import cross_vectors
from compas.geometry.basic import dot_vectors
from compas.geometry.basic import multiply_matrix_vector
from compas.geometry.basic import multiply_matrices
from compas.geometry.basic import transpose_matrix
from compas.geometry.basic import norm_vector

from compas.geometry.transformations import _EPS

from compas.geometry.transformations.matrices import matrix_from_perspective_entries
from compas.geometry.transformations.matrices import matrix_from_translation
from compas.geometry.transformations.matrices import matrix_from_euler_angles
from compas.geometry.transformations.matrices import matrix_from_shear_entries
from compas.geometry.transformations.matrices import matrix_from_scale_factors


__all__ = [
    'transform_points',
    'transform_points_numpy',

    'transform_vectors',
    'transform_vectors_numpy',

    'homogenize',
    'dehomogenize',
    'homogenize_numpy',
    'dehomogenize_numpy',

    'local_axes',
    'local_coords_numpy',
    'global_coords_numpy',

    'determinant',
    'inverse',

    'compose_matrix',
    'decompose_matrix',
]


def transform_points(points, T):
    """Transform multiple points with one Transformation.

    Parameters
    ----------
    points : list of :class:`Point`
        A list of points to be transformed.
    T : :class:`Transformation`
        The transformation to apply.

    Examples
    --------
    >>> points = [Point(1,0,0), (1,2,4), [4,7,1]]
    >>> T = Rotation.from_axis_and_angle((0,2,0), math.radians(45), point=(4,5,6))
    >>> points_transformed = transform_points(points, T)
    """
    return dehomogenize(multiply_matrices(homogenize(points, w=1.0), transpose_matrix(T)))


def transform_vectors(vectors, T):
    """Transform multiple vectors with one Transformation.

    Parameters
    ----------
    vectors : list of :class:`Vector`
        A list of vectors to be transformed.
    T : :class:`Transformation`
        The transformation to apply.

    Examples
    --------
    >>> vectors = [Vector(1,0,0), (1,2,4), [4,7,1]]
    >>> T = Rotation.from_axis_and_angle((0,2,0), math.radians(45), point=(4,5,6))
    >>> vectors_transformed = transform_vectors(vectors, T)
    """
    return dehomogenize(multiply_matrices(homogenize(vectors, w=0.0), transpose_matrix(T)))


def transform_frames(frames, T):
    """Transform multiple frames with one Transformation.

    Parameters
    ----------
    frames : list of :class:`Frame`
        A list of frames to be transformed.
    T : :class:`Transformation`
        The transformation to apply on the frames.

    Examples
    --------
    >>> frames = [Frame([1,0,0], [1,2,4], [4,7,1]), [[0,2,0], [5,2,1], [0,2,1]]]
    >>> T = Rotation.from_axis_and_angle((0,2,0), math.radians(45), point=(4,5,6))
    >>> transformed_frames = transform_frames(frames, T)
    """
    points_and_vectors = homogenize_and_flatten_frames(frames)
    return dehomogenize_and_unflatten_frames(multiply_matrices(points_and_vectors, transpose_matrix(T)))


def transform_points_numpy(points, T):
    """Transform multiple points with one Transformation using numpy.

    Parameters
    ----------
    points : list of :class:`Point`
        A list of points to be transformed.
    T : :class:`Transformation`
        The transformation to apply.

    Examples
    --------
    >>> points = [Point(1,0,0), (1,2,4), [4,7,1]]
    >>> T = Rotation.from_axis_and_angle((0,2,0), math.radians(45), point=(4,5,6))
    >>> points_transformed = transform_points_numpy(points, T)
    """
    from numpy import asarray
    T = asarray(T)
    points = homogenize_numpy(points, w=1.0)
    return dehomogenize_numpy(points.dot(T.T))


def transform_vectors_numpy(vectors, T):
    """Transform multiple vectors with one Transformation using numpy.

    Parameters
    ----------
    vectors : list of :class:`Vector`
        A list of vectors to be transformed.
    T : :class:`Transformation`
        The transformation to apply.

    Examples
    --------
    >>> vectors = [Vector(1,0,0), (1,2,4), [4,7,1]]
    >>> T = Rotation.from_axis_and_angle((0,2,0), math.radians(45), point=(4,5,6))
    >>> vectors_transformed = transform_vectors_numpy(vectors, T)
    """
    from numpy import asarray
    T = asarray(T)
    vectors = homogenize_numpy(vectors, w=0.0)
    return dehomogenize_numpy(vectors.dot(T.T))


def transform_frames_numpy(frames, T):
    """Transform multiple frames with one Transformation usig numpy.

    Parameters
    ----------
    frames : list of :class:`Frame`
        A list of frames to be transformed.
    T : :class:`Transformation`
        The transformation to apply on the frames.

    Examples
    --------
    >>> frames = [Frame([1,0,0], [1,2,4], [4,7,1]), [[0,2,0], [5,2,1], [0,2,1]]]
    >>> T = Rotation.from_axis_and_angle((0,2,0), math.radians(45), point=(4,5,6))
    >>> transformed_frames = transform_frames_numpy(frames, T)
    """
    from numpy import asarray
    T = asarray(T)
    points_and_vectors = homogenize_and_flatten_frames_numpy(frames)
    return dehomogenize_and_unflatten_frames_numpy(points_and_vectors.dot(T.T))


# ==============================================================================
# helping helpers
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
    return [[x * w, y * w, z * w, w] if w else [x, y, z, 0.0] for x, y, z in vectors]


def dehomogenize(vectors):
    """Dehomogenise a list of vectors.

    Parameters
    ----------
    vectors : list of float
        A list of vectors.

    Returns
    -------
    list of float
        Dehomogenised vectors.

    Examples
    --------
    >>>

    """
    return [[x / w, y / w, z / w] if w else [x, y, z] for x, y, z, w in vectors]


def homogenize_and_flatten_frames(frames):
    """Homogenize a list of frames and flatten the 3D list into a 2D list.

    Parameters
    ----------
    frames: list of :class:`Frame`

    Returns
    -------
    list of list of float

    Examples
    --------
    >>> frames = [Frame((1, 1, 1), (0, 1, 0), (1, 0, 0))]
    >>> homogenize_and_flatten_frames(frames)
    [[1.0, 1.0, 1.0, 1.0], [0.0, 1.0, 0.0, 0.0], [1.0, -0.0, 0.0, 0.0]]
    """
    def homogenize_frame(frame):
        return homogenize([frame[0]], w=1.0) + homogenize([frame[1], frame[2]], w=0.0)
    return [v for frame in frames for v in homogenize_frame(frame)]


def dehomogenize_and_unflatten_frames(points_and_vectors):
    """Dehomogenize a list of vectors and unflatten the 2D list into a 3D list.

    Parameters
    ----------
    points_and_vectors: list of list of float
        Homogenized points and vectors.

    Returns
    -------
    list of list of list of float
        The frames.

    Examples
    --------
    >>> points_and_vectors = [(1., 1., 1., 1.), (0., 1., 0., 0.), (1., 0., 0., 0.)]
    >>> dehomogenize_and_unflatten_frames(points_and_vectors)
    [[[1.0, 1.0, 1.0], [0.0, 1.0, 0.0], [1.0, 0.0, 0.0]]]
    """
    frames = dehomogenize(points_and_vectors)
    return [frames[i:i+3] for i in range(0, len(frames), 3)]


def homogenize_and_flatten_frames_numpy(frames):
    """Homogenize a list of frames and flatten the 3D list into a 2D list using numpy.

    The frame consists of a point and 2 orthonormal vectors.

    Parameters
    ----------
    frames: list of :class:`Frame`

    Returns
    -------
    :class:`numpy.ndarray`
        An array of points and vectors.

    Examples
    --------
    >>> import numpy as np
    >>> frames = [Frame((1, 1, 1), (0, 1, 0), (1, 0, 0))]
    >>> res = homogenize_and_flatten_frames_numpy(frames)
    >>> np.allclose(res, [[1.0, 1.0, 1.0, 1.0], [0.0, 1.0, 0.0, 0.0], [1.0, -0.0, 0.0, 0.0]])
    True
    """
    from numpy import asarray
    from numpy import tile
    from numpy import hstack
    n = len(frames)
    frames = asarray(frames).reshape(n * 3, 3)
    extend = tile(asarray([1, 0, 0]).reshape(3, 1), (n, 1))
    return hstack((frames, extend))


def dehomogenize_and_unflatten_frames_numpy(points_and_vectors):
    """Dehomogenize a list of vectors and unflatten the 2D list into a 3D list.

    Parameters
    ----------
    points_and_vectors: list of list of float
        Homogenized points and vectors.

    Returns
    -------
    :class:`numpy.ndarray`
        The frames.

    Examples
    --------
    >>> import numpy as np
    >>> points_and_vectors = [(1., 1., 1., 1.), (0., 1., 0., 0.), (1., 0., 0., 0.)]
    >>> res = dehomogenize_and_unflatten_frames_numpy(points_and_vectors)
    >>> np.allclose(res, [[1.0, 1.0, 1.0], [0.0, 1.0, 0.0], [1.0, 0.0, 0.0]])
    True
    """
    frames = dehomogenize_numpy(points_and_vectors)
    return frames.reshape((int(frames.shape[0]/3.), 3, 3))


def homogenize_numpy(points, w=1.0):
    """Dehomogenizes points or vectors.

    Parameters
    ----------
    points: list of :class:`Points` or list of :class:`Vectors`

    Returns
    -------
    :class:`numpy.ndarray`
    """
    from numpy import asarray
    from numpy import hstack
    from numpy import ones

    points = asarray(points)
    points = hstack((points, w * ones((points.shape[0], 1))))
    return points


def dehomogenize_numpy(points):
    """Dehomogenizes points or vectors.

    Parameters
    ----------
    points: list of :class:`Points` or list of :class:`Vectors`

    Returns
    -------
    :class:`numpy.ndarray`
    """
    from numpy import asarray
    from numpy import vectorize

    def func(a):
        return a if a else 1.
    func = vectorize(func)

    points = asarray(points)
    return points[:, :-1] / func(points[:, -1]).reshape((-1, 1))


# this function will not always work
# it is also a duplicate of stuff found in matrices and frame
def local_axes(a, b, c):
    u = b - a
    v = c - a
    w = cross_vectors(u, v)
    v = cross_vectors(w, u)
    return normalize_vector(u), normalize_vector(v), normalize_vector(w)


def correct_axis_vectors(xaxis, yaxis):
    """Corrects xaxis and yaxis to be unit vectors and orthonormal.

    Parameters
    ----------
    xaxis: :class:`Vector` or list of float
    yaxis: :class:`Vector` or list of float

    Returns
    -------
    tuple: (xaxis, yaxis)
        The corrected axes.
    
    Examples
    --------
    >>> xaxis = [1, 4, 5]
    >>> yaxis = [1, 0, -2]
    >>> xaxis, yaxis = correct_axis_vectors(xaxis, yaxis)
    >>> allclose(xaxis, [0.1543, 0.6172, 0.7715], tol=0.001)
    True
    >>> allclose(yaxis, [0.6929, 0.4891, -0.5298], tol=0.001)
    True
    """
    # TODO use this in Frame
    xaxis = normalize_vector(xaxis)
    yaxis = normalize_vector(yaxis)
    zaxis = normalize_vector(cross_vectors(xaxis, yaxis))
    yaxis = cross_vectors(zaxis, xaxis)
    return xaxis, yaxis

# this should be defined somewhere else
# and should have a python equivalent
# there is an implementation available in frame
def local_coords_numpy(origin, uvw, xyz):
    """Convert global coordinates to local coordinates.

    Parameters
    ----------
    origin : array-like
        The global (XYZ) coordinates of the origin of the local coordinate system.
    uvw : array-like
        The global coordinate difference vectors of the axes of the local coordinate system.
    xyz : array-like
        The global coordinates of the points to convert.

    Returns
    -------
    array
        The coordinates of the given points in the local coordinate system.

    Notes
    -----
    ``origin`` and ``uvw`` together form the frame of local coordinates.

    Examples
    --------
    >>> import numpy as np
    >>> f = Frame([0, 1, 0], [3, 4, 1], [1, 5, 9])
    >>> origin, uvw = f.point, [f.xaxis, f.yaxis, f.zaxis]
    >>> xyz = [Point(2, 3, 5)]
    >>> rst = local_coords_numpy(origin, uvw, xyz)
    >>> np.allclose(rst, [[3.72620657, 4.08804176, 1.55025779]])
    True
    >>> f.represent_point_in_local_coordinates(xyz[0])
    Point(3.726, 4.088, 1.550)
    """
    from numpy import asarray
    from scipy.linalg import solve

    uvw = asarray(uvw).T
    xyz = asarray(xyz).T - asarray(origin).reshape((-1, 1))
    rst = solve(uvw, xyz)
    return rst.T


# this should be defined somewhere else
# and should have a python equivalent
# there is an implementation available in frame
def global_coords_numpy(origin, uvw, rst):
    """Convert local coordinates to global (world) coordinates.

    Parameters
    ----------
    origin : array-like
        The origin of the local coordinate system.
    uvw : array-like
        The coordinate axes of the local coordinate system.
    rst : array-like
        The coordinates of the points wrt the local coordinate system.

    Returns
    -------
    array
        The world coordinates of the given points.

    Notes
    -----
    ``origin`` and ``uvw`` together form the frame of local coordinates.

    Examples
    --------
    >>> f = Frame([0, 1, 0], [3, 4, 1], [1, 5, 9])
    >>> origin, uvw = f.point, [f.xaxis, f.yaxis, f.zaxis]
    >>> xyz = [Point(2, 3, 5)]
    >>> rst = local_coords_numpy(origin, uvw, xyz)
    >>> xyz2 = global_coords_numpy(origin, uvw, rst)
    >>> numpy.allclose(xyz, xyz2)
    True
    """
    from numpy import asarray

    uvw = asarray(uvw).T
    rst = asarray(rst).T
    xyz = uvw.dot(rst) + asarray(origin).reshape((-1, 1))
    return xyz.T


def determinant(M, check=True):
    """Calculates the determinant of a square matrix M.

    Parameters
    ----------
    M : :obj:`list` of :obj:`list` of :obj:`float`
        The square matrix of any dimension.
    check : bool
        If true checks if matrix is squared. Defaults to True.

    Raises
    ------
    ValueError
        If matrix is not a square matrix.

    Returns
    -------
    float
        The determinant.

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

    Parameters
    ----------
    M : :obj:`list` of :obj:`list` of :obj:`float`
        The square matrix of any dimension.

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
    def matrix_minor(m, i, j):
        return [row[:j] + row[j + 1:] for row in (m[:i] + m[i + 1:])]

    detM = determinant(M)  # raises ValueError if matrix is not squared

    if detM == 0:
        ValueError("The matrix is singular.")

    if len(M) == 2:
        return [[M[1][1] / detM, -1 * M[0][1] / detM],
                [-1 * M[1][0] / detM, M[0][0] / detM]]
    else:
        cofactors = []
        for r in range(len(M)):
            cofactor_row = []
            for c in range(len(M)):
                minor = matrix_minor(M, r, c)
                cofactor_row.append(((-1) ** (r + c)) * determinant(minor))
            cofactors.append(cofactor_row)
        cofactors = transpose_matrix(cofactors)
        for r in range(len(cofactors)):
            for c in range(len(cofactors)):
                cofactors[r][c] = cofactors[r][c] / detM
        return cofactors


def decompose_matrix(M):
    """Calculates the components of rotation, translation, scale, shear, and
    perspective of a given transformation matrix M.

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

    # angles
    if row[0][2] != -1. and row[0][2] != 1.:

        beta1 = math.asin(-row[0][2])
        beta2 = math.pi - beta1

        alpha1 = math.atan2(row[1][2] / math.cos(beta1), row[2][2] / math.cos(beta1))
        alpha2 = math.atan2(row[1][2] / math.cos(beta2), row[2][2] / math.cos(beta2))

        gamma1 = math.atan2(row[0][1] / math.cos(beta1), row[0][0] / math.cos(beta1))
        gamma2 = math.atan2(row[0][1] / math.cos(beta2), row[0][0] / math.cos(beta2))

        angles = [alpha1, beta1, gamma1]
        # TODO: check for alpha2, beta2, gamma2 needed?
    else:
        gamma = 0.
        if row[0][2] == -1.:
            beta = math.pi / 2.
            alpha = gamma + math.atan2(row[1][0], row[2][0])
        else:  # row[0][2] == 1
            beta = -math.pi / 2.
            alpha = -gamma + math.atan2(-row[1][0], -row[2][0])
        angles = [alpha, beta, gamma]

    # perspective
    if math.fabs(Mt[0][3]) > _EPS and math.fabs(Mt[1][3]) > _EPS and math.fabs(Mt[2][3]) > _EPS:
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
# Main
# ==============================================================================

if __name__ == "__main__":
    import math
    import doctest
    import numpy
    from compas.geometry import allclose
    from compas.geometry import matrix_from_frame
    from compas.geometry import identity_matrix
    from compas.geometry import Point
    from compas.geometry import Vector
    from compas.geometry import Frame
    from compas.geometry import Transformation
    from compas.geometry import Rotation
    doctest.testmod(globs=globals())
