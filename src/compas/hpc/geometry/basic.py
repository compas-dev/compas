from __future__ import division
from __future__ import print_function

from numba import float64
from numba import int64
from numba import jit

from numpy import array
from numpy import sqrt
from numpy import sum
from numpy import zeros


__author__     = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2017, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'liew@arch.ethz.ch'


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
    # 'vector_component_numba',
    # 'vector_component_xy_numba',
    # 'transpose_matrix_numba',
    'multiply_matrices_numba',
    'multiply_matrix_vector_numba',
    # 'orthonormalise_vectors',
    # 'homogenise_vectors_numba',
    # 'dehomogenise_vectors_numba',
    # 'vector_from_points',
    # 'vector_from_points_xy',
    # 'plane_from_points',
    # 'circle_from_points',
    # 'circle_from_points_xy',
    # 'pointcloud',
    # 'pointcloud_xy',
]


# ==============================================================================

@jit(float64[:](float64[:, :], int64), nogil=True, nopython=True)
def sum_vectors_numba(a, axis=0):
    """ Calculate the sum of an array of vectors along the specified axis.

    Parameters:
        a (array): Array of vectors (m x 3).
        axis (int): Dimension to sum through.

    Returns:
        array: The summed values according to the axis of choice.
    """
    return sum(a, axis=axis)


@jit(float64(float64[:]), nogil=True, nopython=True)
def norm_vector_numba(a):
    """ Calculate the L2 norm or length of a vector.

    Parameters:
        a (array): XYZ components of the vector.

    Returns:
        float: The L2 norm of the vector.
    """
    return sqrt(a[0]**2 + a[1]**2 + a[2]**2)


@jit(float64[:](float64[:, :]), nogil=True, nopython=True)
def norm_vectors_numba(a):
    """ Calculate the L2 norm or length of vectors.

    Parameters:
        a (array): XYZ components of the vectors (m x 3).

    Returns:
        array: The L2 norm of the vectors (m x 1).
    """
    m = a.shape[0]
    w = zeros(m)
    for i in range(m):
        w[i] = sqrt(a[i, 0]**2 + a[i, 1]**2 + a[i, 2]**2)
    return w


@jit(float64(float64[:]), nogil=True, nopython=True)
def length_vector_numba(a):
    """ Calculate the length of a vector.

    Parameters:
        a (array): XYZ components of the vector.

    Returns:
        float: The length of the vector.
    """
    return sqrt(a[0]**2 + a[1]**2 + a[2]**2)


@jit(float64(float64[:]), nogil=True, nopython=True)
def length_vector_xy_numba(a):
    """ Calculate the length of the vector, assuming it lies in the XY plane.

    Parameters:
        a (array): XY(Z) components of the vector.

    Returns:
        float: The length of the XY component of the vector
    """
    return sqrt(a[0]**2 + a[1]**2)


@jit(float64(float64[:]), nogil=True, nopython=True)
def length_vector_sqrd_numba(a):
    """ Calculate the squared length of the vector.

    Parameters:
        a (array): XYZ components of the vector.

    Returns:
        float: The squared length of the XYZ components.
    """
    return a[0]**2 + a[1]**2 + a[2]**2


@jit(float64(float64[:]), nogil=True, nopython=True)
def length_vector_sqrd_xy_numba(a):
    """ Calculate the squared length of the vector, assuming it lies in the XY plane.

    Parameters:
        a (array): XY(Z) components of the vector.

    Returns:
        float: The squared length of the XY components.
    """
    return a[0]**2 + a[1]**2


# ==============================================================================

@jit(float64[:](float64[:], float64), nogil=True, nopython=True)
def scale_vector_numba(a, factor):
    """ Scale a vector by a given factor.

    Parameters:
        a (array): XYZ components of the vector.
        factor (float): Scale factor.

    Returns:
        array: The scaled vector, factor * a.
    """
    return a * factor


@jit(float64[:](float64[:], float64), nogil=True, nopython=True)
def scale_vector_xy_numba(a, factor):
    """ Scale a vector by a given factor, assuming it lies in the XY plane.

    Parameters:
        a (array): XY(Z) components of the vector.
        factor (float): Scale factor.

    Returns:
        array: The scaled vector, factor * a (XY).
    """
    b = a * factor
    b[2] = 0
    return b


@jit(float64[:, :](float64[:, :], float64), nogil=True, nopython=True)
def scale_vectors_numba(a, factor):
    """ Scale multiple vectors by a given factor.

    Parameters:
        a (array): XYZ components of the vectors.
        factor (float): Scale factor.

    Returns:
        array: Scaled vectors.
    """
    return a * factor


@jit(float64[:, :](float64[:, :], float64), nogil=True, nopython=True)
def scale_vectors_xy_numba(a, factor):
    """ Scale multiple vectors by a given factor, assuming they lie in the XY plane

    Parameters:
        a (array): XY(Z)components of the vectors.
        factor (float): Scale factor.

    Returns:
        array: Scaled vectors (XY).
    """
    b = a * factor
    for i in range(b.shape[0]):
        b[i, 2] = 0.
    return b


@jit(float64[:](float64[:]), nogil=True, nopython=True)
def normalize_vector_numba(a):
    """ Normalize a given vector.

    Parameters:
        a (array): XYZ components of the vector.

    Returns:
        array: The normalised vector.
    """
    l = length_vector_numba(a)
    return a / l


@jit(float64[:](float64[:]), nogil=True, nopython=True)
def normalize_vector_xy_numba(a):
    """ Normalize a given vector, assuming it lies in the XY-plane.

    Parameters:
        a (array): XY(Z) components of the vector.

    Returns:
        array: The normalised vector in the XY-plane (Z = 0.0).
    """
    l = length_vector_xy_numba(a)
    b = a / l
    b[2] = 0.
    return b


@jit(float64[:, :](float64[:, :]), nogil=True, nopython=True)
def normalize_vectors_numba(a):
    """ Normalise multiple vectors.

    Parameters:
        a (array): XYZ components of vectors.

    Returns:
        array: The normalised vectors.
    """
    m = a.shape[0]
    b = zeros((m, 3))
    for i in range(m):
        b[i, :] = normalize_vector_numba(a[i, :])
    return b


@jit(float64[:, :](float64[:, :]), nogil=True, nopython=True)
def normalize_vectors_xy_numba(a):
    """ Normalise multiple vectors, assuming they lie in the XY plane.

    Parameters:
        a (array): XY(Z) components of vectors.

    Returns:
        array: The normalised vectors in the XY plane.
    """
    m = a.shape[0]
    b = zeros((m, 3))
    for i in range(m):
        l = length_vector_xy_numba(a[i, :])
        b[i, 0] = a[i, 0] / l
        b[i, 1] = a[i, 1] / l
    return b


@jit(float64[:](float64[:], float64), nogil=True, nopython=True)
def power_vector_numba(a, power):
    """ Raise a vector to the given power.

    Parameters:
        a (array): XYZ components of the vector.
        power (float): Power to raise to.

    Returns:
        array: a^power.
    """
    return array([a[0]**power, a[1]**power, a[2]**power])


@jit(float64[:, :](float64[:, :], float64), nogil=True, nopython=True)
def power_vectors_numba(a, power):
    """ Raise multiple vectors to the given power.

    Parameters:
        a (array): XYZ components of the vectors (m x 3).
        power (float): Power to raise to.

    Returns:
        array: a^power.
    """
    m = a.shape[0]
    b = zeros((m, 3))
    for i in range(m):
        b[i, 0] = a[i, 0]**power
        b[i, 1] = a[i, 1]**power
        b[i, 2] = a[i, 2]**power
    return b


@jit(float64[:](float64[:]), nogil=True, nopython=True)
def square_vector_numba(a):
    """ Raise a single vector to the power 2.

    Parameters:
        a (array): XYZ components of the vector.

    Returns:
        array: a^2.
    """
    return power_vector_numba(a, power=2.)


@jit(float64[:, :](float64[:, :]), nogil=True, nopython=True)
def square_vectors_numba(a):
    """ Raise multiple vectors to the power 2.

    Parameters:
        a (array): XYZ components of the vectors (m x 3).

    Returns:
        array: a^2.
    """
    return power_vectors_numba(a, power=2.)


# ==============================================================================

@jit(float64[:](float64[:], float64[:]), nogil=True, nopython=True)
def add_vectors_numba(u, v):
    """ Add two vectors.

    Parameters:
        u (array): XYZ components of the first vector.
        v (array): XYZ components of the second vector.

    Returns:
        array: u + v.
    """
    return array([u[0] + v[0], u[1] + v[1], u[2] + v[2]])


@jit(float64[:](float64[:], float64[:]), nogil=True, nopython=True)
def add_vectors_xy_numba(u, v):
    """ Add two vectors, assuming they lie in the XY-plane.

    Parameters:
        u (array): XYZ components of the first vector.
        v (array): XYZ components of the second vector.

    Returns:
        array: u + v (Z = 0.0).
    """
    return array([u[0] + v[0], u[1] + v[1], 0.])


@jit(float64[:](float64[:], float64[:]), nogil=True, nopython=True)
def subtract_vectors_numba(u, v):
    """ Subtract one vector from another.

    Parameters:
        u (array): XYZ components of the first vector.
        v (array): XYZ components of the second vector.

    Returns:
        array: u - v.
    """
    return array([u[0] - v[0], u[1] - v[1], u[2] - v[2]])


@jit(float64[:](float64[:], float64[:]), nogil=True, nopython=True)
def subtract_vectors_xy_numba(u, v):
    """ Subtract one vector from another, assuming they lie in the XY plane.

    Parameters:
        u (array): XY(Z) components of the first vector.
        v (array): XY(Z) components of the second vector.

    Returns:
        array: u - v (Z = 0.0).
    """
    return array([u[0] - v[0], u[1] - v[1], 0.])


@jit(float64[:](float64[:], float64[:]), nogil=True, nopython=True)
def multiply_vectors_numba(u, v):
    """ Element-wise multiplication of two vectors.

    Parameters:
        u (array): XYZ components of the first vector.
        v (array): XYZ components of the second vector.

    Returns:
        array: [ui * vi, uj * vj, uk * vk].
    """
    return array([u[0] * v[0], u[1] * v[1], u[2] * v[2]])


@jit(float64[:](float64[:], float64[:]), nogil=True, nopython=True)
def multiply_vectors_xy_numba(u, v):
    """ Element-wise multiplication of two vectors assumed to lie in the XY plane..

    Parameters:
        u (array): XY(Z) components of the first vector.
        v (array): XY(Z) components of the second vector.

    Returns:
        array: [ui * vi, uj * vj, (Z = 0.0)].
    """
    return array([u[0] * v[0], u[1] * v[1], 0.])


@jit(float64[:](float64[:], float64[:]), nogil=True, nopython=True)
def divide_vectors_numba(u, v):
    """ Element-wise division of two vectors.

    Parameters:
        u (array): XYZ components of the first vector.
        v (array): XYZ components of the second vector.

    Returns:
        array: [ui / vi, uj / vj, uk / vk].
    """
    return array([u[0] / v[0], u[1] / v[1], u[2] / v[2]])


@jit(float64[:](float64[:], float64[:]), nogil=True, nopython=True)
def divide_vectors_xy_numba(u, v):
    """ Element-wise division of two vectors assumed to lie in the XY plane.

    Parameters:
        u (array): XY(Z) components of the first vector.
        v (array): XY(Z) components of the second vector.

    Returns:
        array: [ui / vi, uj / vj, (Z = 0.0)].
    """
    return array([u[0] / v[0], u[1] / v[1], 0.])


# ==============================================================================

@jit(float64[:](float64[:], float64[:]), nogil=True, nopython=True)
def cross_vectors_numba(u, v):
    """ Compute the cross product of two vectors.

    Parameters:
        u (array): XYZ components of the first vector.
        v (array): XYZ components of the second vector.

    Returns:
        array: u X v.
    """
    w = zeros(3)
    w[0] = u[1] * v[2] - u[2] * v[1]
    w[1] = u[2] * v[0] - u[0] * v[2]
    w[2] = u[0] * v[1] - u[1] * v[0]
    return w


@jit(float64[:](float64[:], float64[:]), nogil=True, nopython=True)
def cross_vectors_xy_numba(u, v):
    """ Compute the cross product of two vectors, assuming they lie in the XY-plane.

    Parameters:
        u (array): XY(Z) components of the first vector.
        v (array): XY(Z) components of the second vector.

    Returns:
        array: u X v.
    """
    return array([0., 0., u[0] * v[1] - u[1] * v[0]])


@jit(float64(float64[:], float64[:]), nogil=True, nopython=True)
def dot_vectors_numba(u, v):
    """ Compute the dot product of two vectors.

    Parameters:
        u (array): XYZ components of the first vector.
        v (array): XYZ components of the second vector.

    Returns:
        float: u . v.
    """
    return u[0] * v[0] + u[1] * v[1] + u[2] * v[2]


@jit(float64(float64[:], float64[:]), nogil=True, nopython=True)
def dot_vectors_xy_numba(u, v):
    """ Compute the dot product of two vectors, assuming they lie in the XY-plane.

    Parameters:
        u (array): XY(Z) components of the first vector.
        v (array): XY(Z) components of the second vector.

    Returns:
        float: u . v (Z = 0.0).
    """
    return u[0] * v[0] + u[1] * v[1]


# ==============================================================================

@jit(float64[:, :](float64[:, :], float64[:, :]), nogil=True, nopython=True)
def multiply_matrices_numba(A, B):
    """ The multiplication of matrices.

    Parameters:
        A (array): The first matrix (m x n).
        B (array): The second matrix (n x p).

    Returns:
        array: A * B of size (m x p).
    """
    m, n = A.shape
    p = B.shape[1]
    C = zeros((m, p))
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i, j] += A[i, k] * B[k, j]
    return C


@jit(float64[:](float64[:, :], float64[:]), nogil=True, nopython=True)
def multiply_matrix_vector_numba(A, b):
    """ The multiplication of a matrix with a vector.

    Parameters:
        A (array): The matrix (m x n).
        b (array): The vector (n,).

    Returns:
        array: A * b of size (m,).
    """
    m, n = A.shape
    C = zeros(m)
    for i in range(m):
        for j in range(n):
            C[i] += A[i, j] * b[j]
    return C


# ==============================================================================
# Testing
# ==============================================================================

if __name__ == "__main__":

    u = array([1., 2., 3.])
    v = array([4., 5., 6.])
    c = array([[1., 2., 3.], [1., 1., 1.]])
    d = array([4., 5.])
    e = array([[1., 2.], [0., 2.]])
    f = array([[4., 5.], [1., 2.]])

    print(sum_vectors_numba(c, axis=1))
    print(norm_vector_numba(u))
    print(norm_vectors_numba(c))
    print(length_vector_numba(u))
    print(length_vector_xy_numba(u))
    print(length_vector_sqrd_numba(u))
    print(length_vector_sqrd_xy_numba(u))

    print(scale_vector_numba(u, factor=4.))
    print(scale_vector_xy_numba(u, factor=4.))
    print(scale_vectors_numba(c, factor=4.))
    print(scale_vectors_xy_numba(c, factor=4.))
    print(normalize_vector_numba(u))
    print(normalize_vector_xy_numba(u))
    print(normalize_vectors_numba(c))
    print(normalize_vectors_xy_numba(c))
    print(power_vector_numba(u, 3.))
    print(power_vectors_numba(c, 3.))
    print(square_vector_numba(u))
    print(square_vectors_numba(c))

    print(add_vectors_numba(u, v))
    print(add_vectors_xy_numba(u, v))
    print(subtract_vectors_numba(u, v))
    print(subtract_vectors_xy_numba(u, v))
    print(multiply_vectors_numba(u, v))
    print(multiply_vectors_xy_numba(u, v))
    print(divide_vectors_numba(u, v))
    print(divide_vectors_xy_numba(u, v))

    print(cross_vectors_numba(u, v))
    print(cross_vectors_xy_numba(u, v))
    print(dot_vectors_numba(u, v))
    print(dot_vectors_xy_numba(u, v))

    print(multiply_matrices_numba(e, f))
    print(multiply_matrix_vector_numba(e, d))

#     print(vector_component_numba(u, v))
#     print(vector_component_xy_numba(u, v))
#     print(homogenise_vectors_numba(d,3))
#     print(dehomogenise_vectors_numba(d,3))
#     print(transpose_matrix_numba(d))
