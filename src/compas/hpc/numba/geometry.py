from __future__ import print_function
from __future__ import absolute_import

from numba import jit
from numba import int64
from numba import float64
from numba import guvectorize

from numpy import sqrt
from numpy import zeros


__author__     = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2017, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'liew@arch.ethz.ch'


__all__ = [
    'numba_cross',
    'numba_vdot',
    'numba_dot',
    'numba_length',
    'numba_subtract'
]


@jit(nogil=True, nopython=True)
def numba_cross(a, b):
    """ The cross-product of vectors.

    Parameters:
        a (array): The first vector.
        b (array): The second vector.

    Returns:
        array: a X b.
    """
    c = zeros(3)
    c[0] = a[1] * b[2] - a[2] * b[1]
    c[1] = a[2] * b[0] - a[0] * b[2]
    c[2] = a[0] * b[1] - a[1] * b[0]
    return c


@jit(nogil=True, nopython=True)
def numba_dot(A, B):
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


@jit(nogil=True, nopython=True)
def numba_vdot(a, b):
    """ The dot-product of vectors.

    Parameters:
        a (array): The first vector.
        b (array): The second vector.

    Returns:
        float: a . b.
    """
    c = a[0] * b[0] + a[1] * b[1] + a[2] * b[2]
    return c


@jit(nogil=True, nopython=True)
def numba_length(a):
    """ The length of vector.

    Parameters:
        a (array): The input vector.

    Returns:
        float: Length of input vector.
    """
    c = sqrt(a[0]**2 + a[1]**2 + a[2]**2)
    return c


@jit(nogil=True, nopython=True)
def numba_subtract(a, b):
    """ Subtract two vectors.

    Parameters:
        a (array): The first vector to subtract from.
        b (array): The second vector to subtract with.

    Returns:
        array: a - b.
    """
    c = zeros(3)
    c[0] = a[0] - b[0]
    c[1] = a[1] - b[1]
    c[2] = a[2] - b[2]
    return c


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    from numpy import array

    a = array([1, 2, 3])
    b = array([4, 5, 6])
    c = array([[1, 2, 3], [1, 1, 1]])
    d = array([[4, 5, 6], [1, 2, 3]])

    print(numba_cross(a, b))
    print(numba_vdot(a, b))
    print(numba_length(a))
    print(numba_dot(c, d.transpose()))
