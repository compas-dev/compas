
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
from numpy import sqrt
from numpy import zeros


__author__    = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__ = 'Copyright 2018, BLOCK Research Group - ETH Zurich'
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
    'orthonormalize_vectors_numba',
    'plane_from_points_numba',
    'circle_from_points_numba',
    'circle_from_points_xy_numba',
]


# ==============================================================================

@jit(f8[:](f8[:, :], i8), nogil=True, nopython=True, parallel=False, cache=True)
def sum_vectors_numba(a, axis=0):

    """ Calculate the sum of an array of vectors along the specified axis.

    Parameters
    ----------
    a : array
        Array of vectors (m x 3).
    axis : int
        Dimension to sum through.

    Returns
    -------
    array: The summed values according to the axis of choice.

    """

    m = a.shape[0]

    if axis == 0:
        b = array([0., 0., 0.])
        for i in range(m):
            b[0] += a[i, 0]
            b[1] += a[i, 1]
            b[2] += a[i, 2]

    elif axis == 1:
        b = zeros(m)
        for i in range(m):
            b[i] += a[i, 0] + a[i, 1] + a[i, 2]

    return b


@jit(f8(f8[:]), nogil=True, nopython=True, parallel=False, cache=True)
def norm_vector_numba(a):

    """ Calculate the L2 norm or length of a vector.

    Parameters
    ----------
    a : array
        XYZ components of the vector.

    Returns
    -------
    float: The L2 norm of the vector.

    """

    return sqrt(a[0]**2 + a[1]**2 + a[2]**2)


@jit(f8[:](f8[:, :]), nogil=True, nopython=True, parallel=False, cache=True)
def norm_vectors_numba(a):

    """ Calculate the L2 norm or length of vectors.

    Parameters
    ----------
    a : array
        XYZ components of the vectors (m x 3).

    Returns
    -------
    array: The L2 norm of the vectors.

    """

    m = a.shape[0]
    w = zeros(m)
    for i in range(m):
        w[i] = sqrt(a[i, 0]**2 + a[i, 1]**2 + a[i, 2]**2)
    return w


@jit(f8(f8[:]), nogil=True, nopython=True, parallel=False, cache=True)
def length_vector_numba(a):

    """ Calculate the length of a vector.

    Parameters
    ----------
    a : array
        XYZ components of the vector.

    Returns
    -------
    float: The length of the vector.

    """

    return sqrt(a[0]**2 + a[1]**2 + a[2]**2)


@jit(f8(f8[:]), nogil=True, nopython=True, parallel=False, cache=True)
def length_vector_xy_numba(a):

    """ Calculate the length of the vector, assuming it lies in the XY plane.

    Parameters
    ----------
    a : array
        XY(Z) components of the vector.

    Returns
    -------
    float: The length of the XY component of the vector

    """

    return sqrt(a[0]**2 + a[1]**2)


@jit(f8(f8[:]), nogil=True, nopython=True, parallel=False, cache=True)
def length_vector_sqrd_numba(a):

    """ Calculate the squared length of the vector.

    Parameters
    ----------
    a : array
        XYZ components of the vector.

    Returns
    -------
    float: The squared length of the XYZ components.

    """

    return a[0]**2 + a[1]**2 + a[2]**2


@jit(f8(f8[:]), nogil=True, nopython=True, parallel=False, cache=True)
def length_vector_sqrd_xy_numba(a):

    """ Calculate the squared length of the vector, assuming it lies in the XY plane.

    Parameters
    ----------
    a : array
        XY(Z) components of the vector.

    Returns
    -------
    float: The squared length of the XY components.

    """

    return a[0]**2 + a[1]**2


# ==============================================================================

@jit(f8[:](f8[:], f8), nogil=True, nopython=True, parallel=False, cache=True)
def scale_vector_numba(a, factor):

    """ Scale a vector by a given factor.

    Parameters
    ----------
    a : array
        XYZ components of the vector.
    factor : float
        Scale factor.

    Returns
    -------
    array: The scaled vector, factor * a.

    """

    b = zeros(3)
    b[0] = a[0] * factor
    b[1] = a[1] * factor
    b[2] = a[2] * factor
    return b


@jit(f8[:](f8[:], f8), nogil=True, nopython=True, parallel=False, cache=True)
def scale_vector_xy_numba(a, factor):

    """ Scale a vector by a given factor, assuming it lies in the XY plane.

    Parameters
    ----------
    a : array
        XY(Z) components of the vector.
    factor : float
        Scale factor.

    Returns
    -------
    array
        The scaled vector, factor * a (XY).

    """

    b = zeros(3)
    b[0] = a[0] * factor
    b[1] = a[1] * factor
    return b


@jit(f8[:, :](f8[:, :], f8), nogil=True, nopython=True, parallel=False, cache=True)
def scale_vectors_numba(a, factor):

    """ Scale multiple vectors by a given factor.

    Parameters
    ----------
    a : array
        XYZ components of the vectors.
    factor : float
        Scale factor.

    Returns
    -------
    array: Scaled vectors.

    """

    m = a.shape[0]
    b = zeros((m, 3))
    for i in range(m):
        b[i, :] = scale_vector_numba(a[i, :], factor)
    return b


@jit(f8[:, :](f8[:, :], f8), nogil=True, nopython=True, parallel=False, cache=True)
def scale_vectors_xy_numba(a, factor):

    """ Scale multiple vectors by a given factor, assuming they lie in the XY plane

    Parameters
    ----------
    a : array
        XY(Z) components of the vectors.
    factor : float
        Scale factor.

    Returns
    -------
    array
        Scaled vectors (XY).

    """

    m = a.shape[0]
    b = zeros((m, 3))
    for i in range(m):
        b[i, :] = scale_vector_xy_numba(a[i, :], factor)
    return b


@jit(f8[:](f8[:]), nogil=True, nopython=True, parallel=False, cache=True)
def normalize_vector_numba(a):

    """ Normalize a given vector.

    Parameters
    ----------
    a : array
        XYZ components of the vector.

    Returns
    -------
    array
        The normalized vector.

    """

    l = length_vector_numba(a)
    b = zeros(3)
    b[0] = a[0] / l
    b[1] = a[1] / l
    b[2] = a[2] / l
    return b


@jit(f8[:](f8[:]), nogil=True, nopython=True, parallel=False, cache=True)
def normalize_vector_xy_numba(a):

    """ Normalize a given vector, assuming it lies in the XY-plane.

    Parameters
    ----------
    a : array
        XY(Z) components of the vector.

    Returns
    -------
    array
        The normalized vector in the XY-plane (Z = 0.0).

    """

    l = length_vector_xy_numba(a)
    b = zeros(3)
    b[0] = a[0] / l
    b[1] = a[1] / l
    return b


@jit(f8[:, :](f8[:, :]), nogil=True, nopython=True, parallel=False, cache=True)
def normalize_vectors_numba(a):

    """ Normalise multiple vectors.

    Parameters
    ----------
    a : array
        XYZ components of vectors.

    Returns
    -------
    array
        The normalized vectors.

    """

    m = a.shape[0]
    b = zeros((m, 3))
    for i in range(m):
        b[i, :] = normalize_vector_numba(a[i, :])
    return b


@jit(f8[:, :](f8[:, :]), nogil=True, nopython=True, parallel=False, cache=True)
def normalize_vectors_xy_numba(a):

    """ Normalise multiple vectors, assuming they lie in the XY plane.

    Parameters
    ----------
    a : array
        XY(Z) components of vectors.

    Returns
    -------
    array
        The normalized vectors in the XY plane.

    """

    m = a.shape[0]
    b = zeros((m, 3))
    for i in range(m):
        b[i, :] = normalize_vector_xy_numba(a[i, :])
    return b


@jit(f8[:](f8[:], f8), nogil=True, nopython=True, parallel=False, cache=True)
def power_vector_numba(a, power):

    """ Raise a vector to the given power.

    Parameters
    ----------
    a : array
        XYZ components of the vector.
    power : float
        Power to raise to.

    Returns
    -------
    array
        a^power.

    """

    return array([a[0]**power, a[1]**power, a[2]**power])


@jit(f8[:, :](f8[:, :], f8), nogil=True, nopython=True, parallel=False, cache=True)
def power_vectors_numba(a, power):

    """ Raise multiple vectors to the given power.

    Parameters
    ----------
    a : array
        XYZ components of the vectors (m x 3).
    power : float
        Power to raise to.

    Returns
    -------
    array
        a^power.

    """

    m = a.shape[0]
    b = zeros((m, 3))
    for i in range(m):
        b[i, :] = power_vector_numba(a[i, :], power)
    return b


@jit(f8[:](f8[:]), nogil=True, nopython=True, parallel=False, cache=True)
def square_vector_numba(a):

    """ Raise a single vector to the power 2.

    Parameters
    ----------
    a : array
        XYZ components of the vector.

    Returns
    -------
    array
        a^2.

    """

    return power_vector_numba(a, power=2.)


@jit(f8[:, :](f8[:, :]), nogil=True, nopython=True, parallel=False, cache=True)
def square_vectors_numba(a):

    """ Raise multiple vectors to the power 2.

    Parameters
    ----------
    a : array
        XYZ components of the vectors (m x 3).

    Returns
    -------
    array
        a^2.

    """

    return power_vectors_numba(a, power=2.)


# ==============================================================================

@jit(f8[:](f8[:], f8[:]), nogil=True, nopython=True, parallel=False, cache=True)
def add_vectors_numba(u, v):

    """ Add two vectors.

    Parameters
    ----------
    u : array
        XYZ components of the first vector.
    v : array
        XYZ components of the second vector.

    Returns
    -------
    array
        u + v.

    """

    return array([u[0] + v[0], u[1] + v[1], u[2] + v[2]])


@jit(f8[:](f8[:], f8[:]), nogil=True, nopython=True, parallel=False, cache=True)
def add_vectors_xy_numba(u, v):

    """ Add two vectors, assuming they lie in the XY-plane.

    Parameters
    ----------
    u : array
        XYZ components of the first vector.
    v : array
        XYZ components of the second vector.

    Returns
    -------
    array
        u + v (Z = 0.0).

    """

    return array([u[0] + v[0], u[1] + v[1], 0.])


@jit(f8[:](f8[:], f8[:]), nogil=True, nopython=True, parallel=False, cache=True)
def subtract_vectors_numba(u, v):

    """ Subtract one vector from another.

    Parameters
    ----------
    u : array
        XYZ components of the first vector.
    v : array
        XYZ components of the second vector.

    Returns
    -------
    array
        u - v.

    """

    return array([u[0] - v[0], u[1] - v[1], u[2] - v[2]])


@jit(f8[:](f8[:], f8[:]), nogil=True, nopython=True, parallel=False, cache=True)
def subtract_vectors_xy_numba(u, v):

    """ Subtract one vector from another, assuming they lie in the XY plane.

    Parameters
    ----------
    u : array
        XY(Z) components of the first vector.
    v : array
        XY(Z) components of the second vector.

    Returns
    -------
    array
        u - v (Z = 0.0).

    """

    return array([u[0] - v[0], u[1] - v[1], 0.])


@jit(f8[:](f8[:], f8[:]), nogil=True, nopython=True, parallel=False, cache=True)
def multiply_vectors_numba(u, v):

    """ Element-wise multiplication of two vectors.

    Parameters
    ----------
    u : array
        XYZ components of the first vector.
    v : array
        XYZ components of the second vector.

    Returns
    -------
    array
        [ui * vi, uj * vj, uk * vk].

    """

    return array([u[0] * v[0], u[1] * v[1], u[2] * v[2]])


@jit(f8[:](f8[:], f8[:]), nogil=True, nopython=True, parallel=False, cache=True)
def multiply_vectors_xy_numba(u, v):

    """ Element-wise multiplication of two vectors assumed to lie in the XY plane..

    Parameters
    ----------
    u : array
        XY(Z) components of the first vector.
    v : array
        XY(Z) components of the second vector.

    Returns
    -------
    array
        [ui * vi, uj * vj, (Z = 0.0)].

    """

    return array([u[0] * v[0], u[1] * v[1], 0.])


@jit(f8[:](f8[:], f8[:]), nogil=True, nopython=True, parallel=False, cache=True)
def divide_vectors_numba(u, v):

    """ Element-wise division of two vectors.

    Parameters
    ----------
    u : array
        XYZ components of the first vector.
    v : array
        XYZ components of the second vector.

    Returns
    -------
    array
        [ui / vi, uj / vj, uk / vk].

    """

    return array([u[0] / v[0], u[1] / v[1], u[2] / v[2]])


@jit(f8[:](f8[:], f8[:]), nogil=True, nopython=True, parallel=False, cache=True)
def divide_vectors_xy_numba(u, v):

    """ Element-wise division of two vectors assumed to lie in the XY plane.

    Parameters
    ----------
    u : array
        XY(Z) components of the first vector.
    v : array
        XY(Z) components of the second vector.

    Returns
    -------
    array
        [ui / vi, uj / vj, (Z = 0.0)].

    """

    return array([u[0] / v[0], u[1] / v[1], 0.])


# ==============================================================================

@jit(f8[:](f8[:], f8[:]), nogil=True, nopython=True, parallel=False, cache=True)
def cross_vectors_numba(u, v):

    """ Compute the cross product of two vectors.

    Parameters
    ----------
    u : array
        XYZ components of the first vector.
    v : array
        XYZ components of the second vector.

    Returns
    -------
    array
        u X v.

    """

    w = zeros(3)
    w[0] = u[1] * v[2] - u[2] * v[1]
    w[1] = u[2] * v[0] - u[0] * v[2]
    w[2] = u[0] * v[1] - u[1] * v[0]
    return w


@jit(f8[:](f8[:], f8[:]), nogil=True, nopython=True, parallel=False, cache=True)
def cross_vectors_xy_numba(u, v):

    """ Compute the cross product of two vectors, assuming they lie in the XY-plane.

    Parameters
    ----------
    u : array
        XY(Z) components of the first vector.
    v : array
        XY(Z) components of the second vector.

    Returns
    -------
    array
        u X v.

    """

    return array([0., 0., u[0] * v[1] - u[1] * v[0]])


@jit(f8(f8[:], f8[:]), nogil=True, nopython=True, parallel=False, cache=True)
def dot_vectors_numba(u, v):

    """ Compute the dot product of two vectors.

    Parameters
    ----------
    u : array
        XYZ components of the first vector.
    v : array
        XYZ components of the second vector.

    Returns
    -------
    float
        u . v.

    """

    return u[0] * v[0] + u[1] * v[1] + u[2] * v[2]


@jit(f8(f8[:], f8[:]), nogil=True, nopython=True, parallel=False, cache=True)
def dot_vectors_xy_numba(u, v):

    """ Compute the dot product of two vectors, assuming they lie in the XY-plane.

    Parameters
    ----------
    u : array
        XY(Z) components of the first vector.
    v : array
        XY(Z) components of the second vector.

    Returns
    -------
    float
        u . v (Z = 0.0).

    """

    return u[0] * v[0] + u[1] * v[1]


@jit(f8[:](f8[:], f8[:]), nogil=True, nopython=True, parallel=False, cache=True)
def vector_component_numba(u, v):

    """ Compute the component of u in the direction of v.

    Parameters
    ----------
    u : array
        XYZ components of the vector.
    v : array
        XYZ components of the direction.

    Returns
    -------
    float
        The component of u in the direction of v.

    """

    factor = dot_vectors_numba(u, v) / length_vector_sqrd_numba(v)
    return scale_vector_numba(v, factor)


@jit(f8[:](f8[:], f8[:]), nogil=True, nopython=True, parallel=False, cache=True)
def vector_component_xy_numba(u, v):

    """Compute the component of u in the direction of v, assuming they lie in the XY-plane.

    Parameters
    ----------
    u : array
        XY(Z) components of the vector.
    v : array
        XY(Z) components of the direction.

    Returns
    -------
    float
        The component of u in the direction of v (Z = 0.0).

    """

    factor = dot_vectors_xy_numba(u, v) / length_vector_sqrd_xy_numba(v)
    return scale_vector_xy_numba(v, factor)


# ==============================================================================

@jit(f8[:, :](f8[:, :]), nogil=True, nopython=True, parallel=False, cache=True)
def orthonormalize_vectors_numba(a):

    """ Orthonomalise a set of vectors using the Gram-Schmidt process.

    Parameters
    ----------
    u : array
        XYZ components of the vectors (m x 3).

    Returns
    -------
    array
        Array of othonormal basis for the input vectors.

    """

    m = a.shape[0]
    b = zeros((m, 3))
    b[0, :] = a[0, :]
    for i in range(1, m):
        proj = zeros((i, 3))
        for j in range(i):
            proj[j, :] = vector_component_numba(a[i, :], b[j, :])
        b[i, :] = subtract_vectors_numba(a[i, :], sum_vectors_numba(proj, axis=0))
    return b


@jit(f8[:](f8[:], f8[:], f8[:]), nogil=True, nopython=True, parallel=False, cache=True)
def plane_from_points_numba(u, v, w):

    """ Construct a plane from three points.

    Parameters
    ----------
    u : array
        XYZ components of the base point.
    v : array
        XYZ components of the second point.
    w : array
        XYZ components of the third point.

    Returns
    -------
    array
        Normalised vector

    """

    uv = subtract_vectors_numba(v, u)
    uw = subtract_vectors_numba(w, u)
    p = normalize_vector_numba(cross_vectors_numba(uv, uw))
    return p


@jit(f8[:](f8[:], f8[:], f8[:]), nogil=True, nopython=True, parallel=False, cache=True)
def circle_from_points_numba(a, b, c):

    """ Construct a circle from three points.

    Parameters
    ----------
    a : array
        XYZ components of the base point.
    b : array
        XYZ components of the second point.
    c : array
        XYZ components of the third point.

    Returns
    -------
    array
        (xyz, r, normal) x, y, z center, radius, nx, ny, nz normal.

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
    w = zeros((3, 3))
    w[0, :] = scale_vector_numba(a, A)
    w[1, :] = scale_vector_numba(b, B)
    w[2, :] = scale_vector_numba(c, C)
    center = sum_vectors_numba(w, axis=0)
    cr = array([
        center[0],
        center[1],
        center[2],
        length_vector_numba(subtract_vectors_numba(a, center)),
        normal[0],
        normal[1],
        normal[2]])
    return cr


@jit(f8[:](f8[:], f8[:], f8[:]), nogil=True, nopython=True, parallel=False, cache=True)
def circle_from_points_xy_numba(u, v, w):

    """ Construct a circle from three points assumed to be in the XY plane.

    Parameters
    ----------
     u : array
         XY(Z) components of the base point.
     v : array
         XY(Z) components of the second point.
     w : array
         XY(Z) components of the third point.

    Returns
    -------
    array
        (x, y, z, r) where x, y, z are coords of the center point and r the radius.

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
    centerx = (d * e - b * f) / g
    centery = (a * f - c * e) / g
    radius = sqrt((ax - centerx)**2 + (ay - centery)**2)
    return array([centerx, centery, 0.0, radius])


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    from numpy.random import rand

    from time import time

    u = array([1., 2., 3.])
    v = array([4., 5., 6.])
    w = array([5., 2., 10.])
    c = array([[1., 2., 3.], [4., 4., 4.]])
    d = array([4., 5.])
    e = array([[1., 2.], [0., 2.]])
    f = array([[4., 5.], [1., 2.]])

    tic = time()

    for i in range(10**6):

        # a = sum_vectors_numba(c, axis=0)
        # a = norm_vector_numba(u)
        # a = norm_vectors_numba(c)
        # a = length_vector_numba(u)
        # a = length_vector_xy_numba(u)
        # a = length_vector_sqrd_numba(u)
        # a = length_vector_sqrd_xy_numba(u)

        a = scale_vector_numba(u, factor=4.)
        # a = scale_vector_xy_numba(u, factor=4.)
        # a = scale_vectors_numba(c, factor=4.)
        # a = scale_vectors_xy_numba(c, factor=4.)
        # a = normalize_vector_numba(u)
        # a = normalize_vector_xy_numba(u)
        # a = normalize_vectors_numba(c)
        # a = normalize_vectors_xy_numba(c)
        # a = power_vector_numba(u, 3.)
        # a = power_vectors_numba(c, 3.)
        # a = square_vector_numba(u)
        # a = square_vectors_numba(c)

        # a = add_vectors_numba(u, v)
        # a = add_vectors_xy_numba(u, v)
        # a = subtract_vectors_numba(u, v)
        # a = subtract_vectors_xy_numba(u, v)
        # a = multiply_vectors_numba(u, v)
        # a = multiply_vectors_xy_numba(u, v)
        # a = divide_vectors_numba(u, v)
        # a = divide_vectors_xy_numba(u, v)

        # a = cross_vectors_numba(u, v)
        # a = cross_vectors_xy_numba(u, v)
        # a = dot_vectors_numba(u, v)
        # a = dot_vectors_xy_numba(u, v)
        # a = vector_component_numba(u, v)
        # a = vector_component_xy_numba(u, v)


        # a = orthonormalize_vectors_numba(c)
        # a = plane_from_points_numba(u, v, w)
        # a = circle_from_points_numba(u, v, w)
        # a = circle_from_points_xy_numba(u, v, w)

    # a = rand(10**7, 3)

    # sum_vectors_numba(a, 1)

    print(time() - tic)
    # print(a)
