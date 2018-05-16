
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
from numba import f8
from numba import i8
from numba import c16
from numba import jit

try:
    from numba import prange
except ImportError:
    prange = range

from numpy import zeros


__author__    = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__ = 'Copyright 2018, BLOCK Research Group - ETH Zurich'
__license__   = 'MIT License'
__email__     = 'liew@arch.ethz.ch'


__all__ = [
    'diag_numba',
    'diag_complex_numba',
    'diag_fill_numba',
    'diag_fill_complex_numba',
    'ew_matrix_scalar_multiplication_numba',
    'ew_cmatrix_cscalar_multiplication_numba',
    'ew_cmatrix_scalar_multiplication_numba',
    'ew_matrix_cscalar_multiplication_numba',
    'ew_matrix_matrix_multiplication_numba',
    'ew_cmatrix_cmatrix_multiplication_numba',
    'ew_cmatrix_matrix_multiplication_numba',
    'ew_matrix_scalar_division_numba',
    'ew_cmatrix_cscalar_division_numba',
    'ew_cmatrix_scalar_division_numba',
    'ew_matrix_cscalar_division_numba',
    'ew_matrix_matrix_division_numba',
    'ew_cmatrix_cmatrix_division_numba',
    'ew_cmatrix_matrix_division_numba',
    'ew_matrix_cmatrix_division_numba',
    'dot_numba',
    'dotv_numba',
    'transpose_numba']


@jit(f8[:, :](f8[:, :], f8[:]), nogil=True, nopython=True, parallel=False, cache=True)
def diag_numba(A, b):

    """ Fill matrix A with a diagonal represented by vector b.

    Parameters
    ----------
    A : array
        Base matrix.
    b : array
        Diagonal vector to fill with.

    Returns
    -------
    array
        Matrix A with diagonal filled.

    """

    for i in range(b.shape[0]):
        A[i, i] = b[i]
    return A


@jit(c16[:, :](c16[:, :], c16[:]), nogil=True, nopython=True, parallel=False, cache=True)
def diag_complex_numba(A, b):

    """ Fill matrix A with a diagonal represented by vector b (complex).

    Parameters
    ----------
    A : array
        Base matrix.
    b : array
        Diagonal vector to fill with.

    Returns
    -------
    array
        Matrix A with diagonal filled (complex).

    """

    for i in range(b.shape[0]):
        A[i, i] = b[i]
    return A


@jit(f8[:, :](f8[:, :], f8), nogil=True, nopython=True, parallel=False, cache=True)
def diag_fill_numba(A, b):

    """ Fill matrix A with a diagonal represented by scalar b.

    Parameters
    ----------
    A : array
        Base matrix.
    b : float
        Diagonal scalar to fill with.

    Returns
    -------
    array
        Matrix A with diagonal filled.

    """

    if A.shape[0] < A.shape[1]:
        m = A.shape[0]
    else:
        m = A.shape[1]
    for i in range(m):
        A[i, i] = b
    return A


@jit(c16[:, :](c16[:, :], c16), nogil=True, nopython=True, parallel=False, cache=True)
def diag_fill_complex_numba(A, b):

    """ Fill matrix A with a diagonal represented by scalar b (complex).

    Parameters
    ----------
    A : array
        Base matrix.
    b : float
        Diagonal scalar to fill with.

    Returns
    -------
    array
        Matrix A with diagonal filled (complex).

    """

    if A.shape[0] < A.shape[1]:
        m = A.shape[0]
    else:
        m = A.shape[1]
    for i in range(m):
        A[i, i] = b
    return A


# elementwise matrix scalar multiplication -------------------------------------

@jit(f8[:, :](f8[:, :], f8), nogil=True, nopython=True, parallel=False, cache=True)
def ew_matrix_scalar_multiplication_numba(A, b):
    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            A[i, j] *= b
    return A


@jit(c16[:, :](c16[:, :], c16), nogil=True, nopython=True, parallel=False, cache=True)
def ew_cmatrix_cscalar_multiplication_numba(A, b):
    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            A[i, j] *= b
    return A


@jit(c16[:, :](c16[:, :], f8), nogil=True, nopython=True, parallel=False, cache=True)
def ew_cmatrix_scalar_multiplication_numba(A, b):
    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            A[i, j] *= b
    return A


@jit(c16[:, :](f8[:, :], c16), nogil=True, nopython=True, parallel=False, cache=True)
def ew_matrix_cscalar_multiplication_numba(A, b):
    C = np.zeros((A.shape[0], A.shape[1]), dtype=np.complex_)
    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            C[i, j] = A[i, j] * b
    return C


# elementwise matrix matrix multiplication -------------------------------------


@jit(f8[:, :](f8[:, :], f8[:, :]), nogil=True, nopython=True, parallel=False, cache=True)
def ew_matrix_matrix_multiplication_numba(A, B):
    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            A[i, j] *= B[i, j]
    return A


@jit(c16[:, :](c16[:, :], c16[:, :]), nogil=True, nopython=True, parallel=False, cache=True)
def ew_cmatrix_cmatrix_multiplication_numba(A, B):
    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            A[i, j] *= B[i, j]
    return A


@jit(c16[:, :](c16[:, :], f8[:, :]), nogil=True, nopython=True, parallel=False, cache=True)
def ew_cmatrix_matrix_multiplication_numba(A, B):
    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            A[i, j] *= B[i, j]
    return A


# elementwise matrix scalar division -------------------------------------------


@jit(f8[:, :](f8[:, :], f8), nogil=True, nopython=True, parallel=False, cache=True)
def ew_matrix_scalar_division_numba(A, b):
    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            A[i, j] /= b
    return A


@jit(c16[:, :](c16[:, :], c16), nogil=True, nopython=True, parallel=False, cache=True)
def ew_cmatrix_cscalar_division_numba(A, b):
    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            A[i, j] /= b
    return A


@jit(c16[:, :](c16[:, :], f8), nogil=True, nopython=True, parallel=False, cache=True)
def ew_cmatrix_scalar_division_numba(A, b):
    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            A[i, j] /= b
    return A


@jit(c16[:, :](f8[:, :], c16), nogil=True, nopython=True, parallel=False, cache=True)
def ew_matrix_cscalar_division_numba(A, b):
    C = np.zeros((A.shape[0], A.shape[1]), dtype=np.complex_)
    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            C[i, j] = A[i, j] / b
    return C

# elementwise matrix matrix division -------------------------------------------


@jit(f8[:, :](f8[:, :], f8[:, :]), nogil=True, nopython=True, parallel=False, cache=True)
def ew_matrix_matrix_division_numba(A, B):
    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            A[i, j] /= B[i, j]
    return A


@jit(c16[:, :](c16[:, :], c16[:, :]), nogil=True, nopython=True, parallel=False, cache=True)
def ew_cmatrix_cmatrix_division_numba(A, B):
    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            A[i, j] /= B[i, j]
    return A


@jit(c16[:, :](c16[:, :], f8[:, :]), nogil=True, nopython=True, parallel=False, cache=True)
def ew_cmatrix_matrix_division_numba(A, B):
    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            A[i, j] /= B[i, j]
    return A


@jit(c16[:, :](f8[:, :], c16[:, :]), nogil=True, nopython=True, parallel=False, cache=True)
def ew_matrix_cmatrix_division_numba(A, B):
    C = np.zeros((A.shape[0], A.shape[1]), dtype=np.complex_)
    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            C[i, j] = A[i, j] / B[i, j]
    return C


@jit(f8[:, :](f8[:, :], f8[:, :]), nogil=True, nopython=True, parallel=False, cache=True)
def dot_numba(A, B):

    """ The multiplication of matrices.

    Parameters
    ----------
    A : array
        The first matrix (m x n).
    B : array
        The second matrix (n x p).

    Returns
    -------
    array
        A * B of size (m x p).

    """

    m, n = A.shape
    p = B.shape[1]
    C = zeros((m, p))
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i, j] += A[i, k] * B[k, j]
    return C


@jit(f8[:](f8[:, :], f8[:]), nogil=True, nopython=True, parallel=False, cache=True)
def dotv_numba(A, b):

    """ The multiplication of a matrix with a vector.

    Parameters
    ----------
    A : array
        The matrix (m x n).
    b : array
        The vector (n,).

    Returns
    -------
    array
        A * b of size (m,).

    """

    m, n = A.shape
    C = zeros(m)
    for i in range(m):
        for j in range(n):
            C[i] += A[i, j] * b[j]
    return C


@jit(f8[:, :](f8[:, :]), nogil=True, nopython=True, parallel=False, cache=True)
def transpose_numba(A):

    """ Transpose an array.

    Parameters
    ----------
    A : array
        The matrix (m x n).

    Returns
    -------
    array
        A transposed (n x m).

    """

    m, n = A.shape
    B = zeros((n, m))
    for i in range(m):
        for j in range(n):
            B[j, i] = A[i, j]
    return B

# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    from numpy import array
    from numpy import float64
    from numpy import zeros

    A = zeros((3, 3))
    b = array(list(range(3)), dtype=float64)

    print(diag_numba(A, b))
    print(diag_fill_numba(A, 1.))

    d = array([4., 5.])
    e = array([[1., 2.], [0., 2.]])
    f = array([[4., 5.], [1., 2.]])

    # print(dot_numba(e, f))
    print(dotv_numba(e, d))
    print(transpose_numba(e))
