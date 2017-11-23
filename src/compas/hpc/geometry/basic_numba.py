from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from numba import f8
from numba import i8
from numba import jit

try:
    from numba import prange
except ImportError:
    prange = range

from numpy import array
from numpy import empty
from numpy import sqrt

import numpy as np

# Note: Numba experimental features parallel and prange are implementated but generally disabled.


__author__    = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__ = 'Copyright 2017, BLOCK Research Group - ETH Zurich'
__license__   = 'MIT License'
__email__     = 'liew@arch.ethz.ch'


__all__ = [
    'sum_vectors_numba',
    'norm_vector_numba',
    'norm_vectors_numba',
    'length_vector_numba',
    'length_vector_xy_numba',
    'length_vector_sqrd_numba',
    'length_vector_sqrd_xy_numba',
    'scale_vector_numba',
    'scale_vector_xy_numba',
    'scale_vectors_numba',
    'scale_vectors_xy_numba',
    'normalize_vector_numba',
    'normalize_vector_xy_numba',
    'normalize_vectors_numba',
    'normalize_vectors_xy_numba',
    'power_vector_numba',
    'power_vectors_numba',
    'square_vector_numba',
    'square_vectors_numba',
    'add_vectors_numba',
    'add_vectors_xy_numba',
    'subtract_vectors_numba',
    'subtract_vectors_xy_numba',
    'multiply_vectors_numba',
    'multiply_vectors_xy_numba',
    'divide_vectors_numba',
    'divide_vectors_xy_numba',
    'cross_vectors_numba',
    'cross_vectors_xy_numba',
    'dot_vectors_numba',
    'dot_vectors_xy_numba',
    'vector_component_numba',
    'vector_component_xy_numba',
    'multiply_matrices_numba',
    'multiply_matrix_vector_numba',
    'transpose_matrix_numba',
    'orthonormalise_vectors_numba',
    'plane_from_points_numba',
    'circle_from_points_numba',
    'circle_from_points_xy_numba',
]


# ==============================================================================

@jit(f8[:](f8[:, :], i8), nogil=True, nopython=True, parallel=False)
def sum_vectors_numba(a, axis=0):
    """ Calculate the sum of an array of vectors along the specified axis.

    Parameters
    ----------
        a (array): Array of vectors (m x 3).
        axis (int): Dimension to sum through.

    Returns
    -------
        array: The summed values according to the axis of choice.
    """
    m = a.shape[0]

    if axis == 0:
        b = array([0., 0., 0.])
        for i in prange(m):
            b[0] += a[i, 0]
            b[1] += a[i, 1]
            b[2] += a[i, 2]

    elif axis == 1:
        b = np.zeros(m)
        for i in prange(m):
            b[i] += a[i, 0] + a[i, 1] + a[i, 2]

    return b


@jit(f8(f8[:]), nogil=True, nopython=True, parallel=True)
def norm_vector_numba(a):
    """ Calculate the L2 norm or length of a vector.

    Parameters
    ----------
        a (array): XYZ components of the vector.

    Returns
    -------
        float: The L2 norm of the vector.
    """
    return sqrt(a[0]**2 + a[1]**2 + a[2]**2)


@jit(f8[:](f8[:, :]), nogil=True, nopython=True, parallel=False)
def norm_vectors_numba(a):
    """ Calculate the L2 norm or length of vectors.

    Parameters
    ----------
        a (array): XYZ components of the vectors (m x 3).

    Returns
    -------
        array: The L2 norm of the vectors.
    """
    m = a.shape[0]
    w = empty(m)
    for i in prange(m):
        w[i] = sqrt(a[i, 0]**2 + a[i, 1]**2 + a[i, 2]**2)
    return w


@jit(f8(f8[:]), nogil=True, nopython=True, parallel=True)
def length_vector_numba(a):
    """ Calculate the length of a vector.

    Parameters
    ----------
        a (array): XYZ components of the vector.

    Returns
    -------
        float: The length of the vector.
    """
    return sqrt(a[0]**2 + a[1]**2 + a[2]**2)


@jit(f8(f8[:]), nogil=True, nopython=True, parallel=True)
def length_vector_xy_numba(a):
    """ Calculate the length of the vector, assuming it lies in the XY plane.

    Parameters
    ----------
        a (array): XY(Z) components of the vector.

    Returns
    -------
        float: The length of the XY component of the vector
    """
    return sqrt(a[0]**2 + a[1]**2)


@jit(f8(f8[:]), nogil=True, nopython=True, parallel=True)
def length_vector_sqrd_numba(a):
    """ Calculate the squared length of the vector.

    Parameters
    ----------
        a (array): XYZ components of the vector.

    Returns
    -------
        float: The squared length of the XYZ components.
    """
    return a[0]**2 + a[1]**2 + a[2]**2


@jit(f8(f8[:]), nogil=True, nopython=True, parallel=True)
def length_vector_sqrd_xy_numba(a):
    """ Calculate the squared length of the vector, assuming it lies in the XY plane.

    Parameters
    ----------
        a (array): XY(Z) components of the vector.

    Returns
    -------
        float: The squared length of the XY components.
    """
    return a[0]**2 + a[1]**2


# ==============================================================================

@jit(f8[:](f8[:], f8), nogil=True, nopython=True, parallel=True)
def scale_vector_numba(a, factor):
    """ Scale a vector by a given factor.

    Parameters
    ----------
        a (array): XYZ components of the vector.
        factor (float): Scale factor.

    Returns
    -------
        array: The scaled vector, factor * a.
    """
    b = empty(3)
    b[0] = a[0] * factor
    b[1] = a[1] * factor
    b[2] = a[2] * factor
    return b


@jit(f8[:](f8[:], f8), nogil=True, nopython=True, parallel=True)
def scale_vector_xy_numba(a, factor):
    """ Scale a vector by a given factor, assuming it lies in the XY plane.

    Parameters
    ----------
        a (array): XY(Z) components of the vector.
        factor (float): Scale factor.

    Returns
    -------
        array: The scaled vector, factor * a (XY).
    """
    b = empty(3)
    b[0] = a[0] * factor
    b[1] = a[1] * factor
    b[2] = 0
    return b


@jit(f8[:, :](f8[:, :], f8), nogil=True, nopython=True, parallel=False)
def scale_vectors_numba(a, factor):
    """ Scale multiple vectors by a given factor.

    Parameters
    ----------
        a (array): XYZ components of the vectors.
        factor (float): Scale factor.

    Returns
    -------
        array: Scaled vectors.
    """
    m = a.shape[0]
    b = empty((m, 3))
    for i in prange(m):
        b[i, :] = scale_vector_numba(a[i, :], factor)
    return b


@jit(f8[:, :](f8[:, :], f8), nogil=True, nopython=True, parallel=False)
def scale_vectors_xy_numba(a, factor):
    """ Scale multiple vectors by a given factor, assuming they lie in the XY plane

    Parameters
    ----------
        a (array): XY(Z)components of the vectors.
        factor (float): Scale factor.

    Returns
    -------
        array: Scaled vectors (XY).
    """
    m = a.shape[0]
    b = empty((m, 3))
    for i in prange(m):
        b[i, :] = scale_vector_xy_numba(a[i, :], factor)
    return b


@jit(f8[:](f8[:]), nogil=True, nopython=True, parallel=True)
def normalize_vector_numba(a):
    """ Normalize a given vector.

    Parameters
    ----------
        a (array): XYZ components of the vector.

    Returns
    -------
        array: The normalised vector.
    """
    l = length_vector_numba(a)
    b = empty(3)
    b[0] = a[0] / l
    b[1] = a[1] / l
    b[2] = a[2] / l
    return b


@jit(f8[:](f8[:]), nogil=True, nopython=True, parallel=True)
def normalize_vector_xy_numba(a):
    """ Normalize a given vector, assuming it lies in the XY-plane.

    Parameters
    ----------
        a (array): XY(Z) components of the vector.

    Returns
    -------
        array: The normalised vector in the XY-plane (Z = 0.0).
    """
    l = length_vector_xy_numba(a)
    b = empty(3)
    b[0] = a[0] / l
    b[1] = a[1] / l
    b[2] = 0
    return b


@jit(f8[:, :](f8[:, :]), nogil=True, nopython=True, parallel=False)
def normalize_vectors_numba(a):
    """ Normalise multiple vectors.

    Parameters
    ----------
        a (array): XYZ components of vectors.

    Returns
    -------
        array: The normalised vectors.
    """
    m = a.shape[0]
    b = empty((m, 3))
    for i in prange(m):
        b[i, :] = normalize_vector_numba(a[i, :])
    return b


@jit(f8[:, :](f8[:, :]), nogil=True, nopython=True, parallel=False)
def normalize_vectors_xy_numba(a):
    """ Normalise multiple vectors, assuming they lie in the XY plane.

    Parameters
    ----------
        a (array): XY(Z) components of vectors.

    Returns
    -------
        array: The normalised vectors in the XY plane.
    """
    m = a.shape[0]
    b = empty((m, 3))
    for i in prange(m):
        b[i, :] = normalize_vector_xy_numba(a[i, :])
    return b


@jit(f8[:](f8[:], f8), nogil=True, nopython=True, parallel=True)
def power_vector_numba(a, power):
    """ Raise a vector to the given power.

    Parameters
    ----------
        a (array): XYZ components of the vector.
        power (float): Power to raise to.

    Returns
    -------
        array: a^power.
    """
    return array([a[0]**power, a[1]**power, a[2]**power])


@jit(f8[:, :](f8[:, :], f8), nogil=True, nopython=True, parallel=False)
def power_vectors_numba(a, power):
    """ Raise multiple vectors to the given power.

    Parameters
    ----------
        a (array): XYZ components of the vectors (m x 3).
        power (float): Power to raise to.

    Returns
    -------
        array: a^power.
    """
    m = a.shape[0]
    b = empty((m, 3))
    for i in prange(m):
        b[i, :] = power_vector_numba(a[i, :], power)
    return b


@jit(f8[:](f8[:]), nogil=True, nopython=True, parallel=True)
def square_vector_numba(a):
    """ Raise a single vector to the power 2.

    Parameters
    ----------
        a (array): XYZ components of the vector.

    Returns
    -------
        array: a^2.
    """
    return power_vector_numba(a, power=2.)


@jit(f8[:, :](f8[:, :]), nogil=True, nopython=True, parallel=True)
def square_vectors_numba(a):
    """ Raise multiple vectors to the power 2.

    Parameters
    ----------
        a (array): XYZ components of the vectors (m x 3).

    Returns
    -------
        array: a^2.
    """
    return power_vectors_numba(a, power=2.)


# ==============================================================================

@jit(f8[:](f8[:], f8[:]), nogil=True, nopython=True, parallel=True)
def add_vectors_numba(u, v):
    """ Add two vectors.

    Parameters
    ----------
        u (array): XYZ components of the first vector.
        v (array): XYZ components of the second vector.

    Returns
    -------
        array: u + v.
    """
    return array([u[0] + v[0], u[1] + v[1], u[2] + v[2]])


@jit(f8[:](f8[:], f8[:]), nogil=True, nopython=True, parallel=True)
def add_vectors_xy_numba(u, v):
    """ Add two vectors, assuming they lie in the XY-plane.

    Parameters
    ----------
        u (array): XYZ components of the first vector.
        v (array): XYZ components of the second vector.

    Returns
    -------
        array: u + v (Z = 0.0).
    """
    return array([u[0] + v[0], u[1] + v[1], 0.])


@jit(f8[:](f8[:], f8[:]), nogil=True, nopython=True, parallel=True)
def subtract_vectors_numba(u, v):
    """ Subtract one vector from another.

    Parameters
    ----------
        u (array): XYZ components of the first vector.
        v (array): XYZ components of the second vector.

    Returns
    -------
        array: u - v.
    """
    return array([u[0] - v[0], u[1] - v[1], u[2] - v[2]])


@jit(f8[:](f8[:], f8[:]), nogil=True, nopython=True, parallel=True)
def subtract_vectors_xy_numba(u, v):
    """ Subtract one vector from another, assuming they lie in the XY plane.

    Parameters
    ----------
        u (array): XY(Z) components of the first vector.
        v (array): XY(Z) components of the second vector.

    Returns
    -------
        array: u - v (Z = 0.0).
    """
    return array([u[0] - v[0], u[1] - v[1], 0.])


@jit(f8[:](f8[:], f8[:]), nogil=True, nopython=True, parallel=True)
def multiply_vectors_numba(u, v):
    """ Element-wise multiplication of two vectors.

    Parameters
    ----------
        u (array): XYZ components of the first vector.
        v (array): XYZ components of the second vector.

    Returns
    -------
        array: [ui * vi, uj * vj, uk * vk].
    """
    return array([u[0] * v[0], u[1] * v[1], u[2] * v[2]])


@jit(f8[:](f8[:], f8[:]), nogil=True, nopython=True, parallel=True)
def multiply_vectors_xy_numba(u, v):
    """ Element-wise multiplication of two vectors assumed to lie in the XY plane..

    Parameters
    ----------
        u (array): XY(Z) components of the first vector.
        v (array): XY(Z) components of the second vector.

    Returns
    -------
        array: [ui * vi, uj * vj, (Z = 0.0)].
    """
    return array([u[0] * v[0], u[1] * v[1], 0.])


@jit(f8[:](f8[:], f8[:]), nogil=True, nopython=True, parallel=True)
def divide_vectors_numba(u, v):
    """ Element-wise division of two vectors.

    Parameters
    ----------
        u (array): XYZ components of the first vector.
        v (array): XYZ components of the second vector.

    Returns
    -------
        array: [ui / vi, uj / vj, uk / vk].
    """
    return array([u[0] / v[0], u[1] / v[1], u[2] / v[2]])


@jit(f8[:](f8[:], f8[:]), nogil=True, nopython=True, parallel=True)
def divide_vectors_xy_numba(u, v):
    """ Element-wise division of two vectors assumed to lie in the XY plane.

    Parameters
    ----------
        u (array): XY(Z) components of the first vector.
        v (array): XY(Z) components of the second vector.

    Returns
    -------
        array: [ui / vi, uj / vj, (Z = 0.0)].
    """
    return array([u[0] / v[0], u[1] / v[1], 0.])


# ==============================================================================

@jit(f8[:](f8[:], f8[:]), nogil=True, nopython=True, parallel=True)
def cross_vectors_numba(u, v):
    """ Compute the cross product of two vectors.

    Parameters
    ----------
        u (array): XYZ components of the first vector.
        v (array): XYZ components of the second vector.

    Returns
    -------
        array: u X v.
    """
    w = empty(3)
    w[0] = u[1] * v[2] - u[2] * v[1]
    w[1] = u[2] * v[0] - u[0] * v[2]
    w[2] = u[0] * v[1] - u[1] * v[0]
    return w


@jit(f8[:](f8[:], f8[:]), nogil=True, nopython=True, parallel=True)
def cross_vectors_xy_numba(u, v):
    """ Compute the cross product of two vectors, assuming they lie in the XY-plane.

    Parameters
    ----------
        u (array): XY(Z) components of the first vector.
        v (array): XY(Z) components of the second vector.

    Returns
    -------
        array: u X v.
    """
    return array([0., 0., u[0] * v[1] - u[1] * v[0]])


@jit(f8(f8[:], f8[:]), nogil=True, nopython=True, parallel=True)
def dot_vectors_numba(u, v):
    """ Compute the dot product of two vectors.

    Parameters
    ----------
        u (array): XYZ components of the first vector.
        v (array): XYZ components of the second vector.

    Returns
    -------
        float: u . v.
    """
    return u[0] * v[0] + u[1] * v[1] + u[2] * v[2]


@jit(f8(f8[:], f8[:]), nogil=True, nopython=True, parallel=True)
def dot_vectors_xy_numba(u, v):
    """ Compute the dot product of two vectors, assuming they lie in the XY-plane.

    Parameters
    ----------
        u (array): XY(Z) components of the first vector.
        v (array): XY(Z) components of the second vector.

    Returns
    -------
        float: u . v (Z = 0.0).
    """
    return u[0] * v[0] + u[1] * v[1]


@jit(f8[:](f8[:], f8[:]), nogil=True, nopython=True, parallel=True)
def vector_component_numba(u, v):
    """Compute the component of u in the direction of v.

    Parameters
    ----------
        u (array): XYZ components of the vector.
        v (array): XYZ components of the direction.

    Returns
    -------
        float: The component of u in the direction of v.
    """
    factor = dot_vectors_numba(u, v) / length_vector_sqrd_numba(v)
    return scale_vector_numba(v, factor)


@jit(f8[:](f8[:], f8[:]), nogil=True, nopython=True, parallel=True)
def vector_component_xy_numba(u, v):
    """Compute the component of u in the direction of v, assuming they lie in the XY-plane.

    Parameters
    ----------
        u (array): XY(Z) components of the vector.
        v (array): XY(Z) components of the direction.

    Returns
    -------
        float: The component of u in the direction of v (Z = 0.0).
    """
    factor = dot_vectors_xy_numba(u, v) / length_vector_sqrd_xy_numba(v)
    return scale_vector_xy_numba(v, factor)


# ==============================================================================

@jit(f8[:, :](f8[:, :], f8[:, :]), nogil=True, nopython=True, parallel=False)
def multiply_matrices_numba(A, B):
    """ The multiplication of matrices.

    Parameters
    ----------
        A (array): The first matrix (m x n).
        B (array): The second matrix (n x p).

    Returns
    -------
        array: A * B of size (m x p).
    """
    m, n = A.shape
    p = B.shape[1]
    C = np.zeros((m, p))
    for i in prange(m):
        for j in prange(p):
            for k in prange(n):
                C[i, j] += A[i, k] * B[k, j]
    return C


@jit(f8[:](f8[:, :], f8[:]), nogil=True, nopython=True, parallel=False)
def multiply_matrix_vector_numba(A, b):
    """ The multiplication of a matrix with a vector.

    Parameters
    ----------
        A (array): The matrix (m x n).
        b (array): The vector (n,).

    Returns
    -------
        array: A * b of size (m,).
    """
    m, n = A.shape
    C = np.zeros(m)
    for i in prange(m):
        for j in prange(n):
            C[i] += A[i, j] * b[j]
    return C


@jit(f8[:, :](f8[:, :]), nogil=True, nopython=True, parallel=False)
def transpose_matrix_numba(A):
    """ Transpose an array.

    Parameters
    ----------
        A (array): The matrix (m x n).

    Returns
    -------
        array: A transposed (n x m).
    """
    m, n = A.shape
    B = empty((n, m))
    for i in prange(m):
        for j in prange(n):
            B[j, i] = A[i, j]
    return B


@jit(f8[:, :](f8[:, :]), nogil=True, nopython=True, parallel=False)
def orthonormalise_vectors_numba(a):
    """ Orthonomalise a set of vectors using the Gram-Schmidt process.

    Parameters
    ----------
        u (array): XYZ components of the vectors (m x 3).

    Returns
    -------
        array: Array of othonormal basis for the input vectors.
    """
    m = a.shape[0]
    b = empty((m, 3))
    b[0, :] = a[0, :]
    for i in prange(1, m):
        proj = empty((i, 3))
        for j in prange(i):
            proj[j, :] = vector_component_numba(a[i, :], b[j, :])
        b[i, :] = subtract_vectors_numba(a[i, :], sum_vectors_numba(proj, axis=0))
    return b


@jit(f8[:](f8[:], f8[:], f8[:]), nogil=True, nopython=True, parallel=True)
def plane_from_points_numba(u, v, w):
    """Construct a plane from three points.

    Parameters
    ----------
        u (array): XYZ components of the base point.
        v (array): XYZ components of the second point.
        w (array): XYZ components of the third point.

    Returns
    -------
        p : Normalised vector
    """
    uv = subtract_vectors_numba(v, u)
    uw = subtract_vectors_numba(w, u)
    p = normalize_vector_numba(cross_vectors_numba(uv, uw))
    return p


@jit(f8[:](f8[:], f8[:], f8[:]), nogil=True, nopython=True, parallel=True)
def circle_from_points_numba(a, b, c):
    """Construct a circle from three points.

    Parameters
    ----------
        a (array): XYZ components of the base point.
        b (array): XYZ components of the second point.
        c (array): XYZ components of the third point.

    Returns
    -------
        array: (xyz, r, normal) x, y, z centre, radius, nx, ny, nz normal.
    """
    ab = subtract_vectors_numba(b, a)
    cb = subtract_vectors_numba(b, c)
    ba = subtract_vectors_numba(a, b)
    ca = subtract_vectors_numba(a, c)
    ac = subtract_vectors_numba(c, a)
    bc = subtract_vectors_numba(c, b)
    normal = normalize_vector_numba(cross_vectors_numba(ab, ac))
    d = 2. * length_vector_sqrd_numba(cross_vectors_numba(ba, cb))
    A = length_vector_sqrd_numba(cb) * dot_vectors_numba(ba, ca) / d
    B = length_vector_sqrd_numba(ca) * dot_vectors_numba(ab, cb) / d
    C = length_vector_sqrd_numba(ba) * dot_vectors_numba(ac, bc) / d
    w = empty((3, 3))
    w[0, :] = scale_vector_numba(a, A)
    w[1, :] = scale_vector_numba(b, B)
    w[2, :] = scale_vector_numba(c, C)
    centre = sum_vectors_numba(w, axis=0)
    cr = array([
        centre[0],
        centre[1],
        centre[2],
        length_vector_numba(subtract_vectors_numba(a, centre)),
        normal[0],
        normal[1],
        normal[2]])
    return cr


@jit(f8[:](f8[:], f8[:], f8[:]), nogil=True, nopython=True, parallel=True)
def circle_from_points_xy_numba(u, v, w):
    """Construct a circle from three points assumed to be in the XY plane.

    Parameters
    ----------
         u (array): XY(Z) components of the base point.
         v (array): XY(Z) components of the second point.
         w (array): XY(Z) components of the third point.
    Returns
    -------
        array: (x, y, z, r) where x, y, z are coords of the centre point and r the radius.
   """
    ax, ay = u[0], u[1]
    bx, by = v[0], v[1]
    cx, cy = w[0], w[1]
    a = bx - ax
    b = by - ay
    c = cx - ax
    d = cy - ay
    e = a * (ax + bx) + b * (ay + by)
    f = c * (ax + cx) + d * (ay + cy)
    g = 2 * (a * (cy - by) - b * (cx - bx))
    centrex = (d * e - b * f) / g
    centrey = (a * f - c * e) / g
    radius = sqrt((ax - centrex)**2 + (ay - centrey)**2)
    return array([centrex, centrey, 0.0, radius])


# ==============================================================================
# Testing
# ==============================================================================

if __name__ == "__main__":

    from time import time

    u = array([1., 2., 3.])
    v = array([4., 5., 6.])
    w = array([5., 2., 10.])
    c = array([[1., 2., 3.], [4., 4., 4.]])
    d = array([4., 5.])
    e = array([[1., 2.], [0., 2.]])
    f = array([[4., 5.], [1., 2.]])

    tic = time()

    for i in range(10**5):

        # sum_vectors_numba(c, axis=0)
        # norm_vector_numba(u)
        # norm_vectors_numba(c)
        # length_vector_numba(u)
        # length_vector_xy_numba(u)
        # length_vector_sqrd_numba(u)
        # length_vector_sqrd_xy_numba(u)

        # scale_vector_numba(u, factor=4.)
        # scale_vector_xy_numba(u, factor=4.)
        # scale_vectors_numba(c, factor=4.)
        # scale_vectors_xy_numba(c, factor=4.)
        # normalize_vector_numba(u)
        # normalize_vector_xy_numba(u)
        # normalize_vectors_numba(c)
        # normalize_vectors_xy_numba(c)
        # power_vector_numba(u, 3.)
        # power_vectors_numba(c, 3.)
        # square_vector_numba(u)
        # square_vectors_numba(c)

        # add_vectors_numba(u, v)
        # add_vectors_xy_numba(u, v)
        # subtract_vectors_numba(u, v)
        # subtract_vectors_xy_numba(u, v)
        # multiply_vectors_numba(u, v)
        # multiply_vectors_xy_numba(u, v)
        # divide_vectors_numba(u, v)
        # divide_vectors_xy_numba(u, v)

        # cross_vectors_numba(u, v)
        # cross_vectors_xy_numba(u, v)
        # dot_vectors_numba(u, v)
        # dot_vectors_xy_numba(u, v)
        # vector_component_numba(u, v)
        # vector_component_xy_numba(u, v)

        # multiply_matrices_numba(e, f)
        # multiply_matrix_vector_numba(e, d)
        # transpose_matrix_numba(e)
        # orthonormalise_vectors_numba(c)
        # plane_from_points_numba(u, v, w)
        # circle_from_points_numba(u, v, w)
        circle_from_points_xy_numba(u, v, w)

    print(time() - tic)
