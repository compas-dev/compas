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
    return dehomogenize(multiply_matrices(homogenize(points, w=1.0), transpose_matrix(T)))


def transform_vectors(vectors, T):
    return dehomogenize(multiply_matrices(homogenize(vectors, w=0.0), transpose_matrix(T)))


def transform_points_numpy(points, T):
    from numpy import asarray
    T = asarray(T)
    points = homogenize_numpy(points, w=1.0)
    return dehomogenize_numpy(points.dot(T.T))


def transform_vectors_numpy(vectors, T):
    from numpy import asarray
    T = asarray(T)
    vectors = homogenize_numpy(vectors, w=0.0)
    return dehomogenize_numpy(vectors.dot(T.T))


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
    return [[x / w, y / w, z / w] if w else [x, y, z] for x, y, z, w in vectors]


def homogenize_numpy(points, w=1.0):
    from numpy import asarray
    from numpy import hstack
    from numpy import ones

    points = asarray(points)
    points = hstack((points, w * ones((points.shape[0], 1))))
    return points


def dehomogenize_numpy(points):
    from numpy import asarray

    points = asarray(points)
    return points[:, :-1] / points[:, -1].reshape((-1, 1))


# this function will not always work
# it is also a duplicate of stuff found in matrices and frame
def local_axes(a, b, c):
    u = b - a
    v = c - a
    w = cross_vectors(u, v)
    v = cross_vectors(w, u)
    return normalize_vector(u), normalize_vector(v), normalize_vector(w)


# this should be defined somewhere else
# and should have a python equivalent
# there is an implementation available in frame
def local_coords_numpy(o, uvw, xyz):
    from numpy import asarray
    from scipy.linalg import solve

    uvw = asarray(uvw).T
    xyz = asarray(xyz).T - asarray(o).reshape((-1, 1))
    rst = solve(uvw, xyz)
    return rst.T


# this should be defined somewhere else
# and should have a python equivalent
# there is an implementation available in frame
def global_coords_numpy(o, uvw, rst):
    from numpy import asarray

    uvw = asarray(uvw).T
    rst = asarray(rst).T
    xyz = uvw.dot(rst) + asarray(o).reshape((-1, 1))
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

    pass
