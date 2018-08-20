
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from numba import f8
from numba import c16
from numba import jit

try:
    from numba import prange
except ImportError:
    prange = range

from numpy import zeros


__author__    = ['Andrew Liew <liew@arch.ethz.ch>', 'Tomas Mendez Echenagucia <mtomas@ethz.ch>']
__copyright__ = 'Copyright 2018, BLOCK Research Group - ETH Zurich'
__license__   = 'MIT License'
__email__     = 'liew@arch.ethz.ch'


__all__ = [
    'diag_numba',
    'diag_complex_numba',
    'diag_fill_numba',
    'diag_fill_complex_numba',
    'scale_matrix_numba',
    'scale_matrix_complex_numba',
    'multiply_matrices_numba',
    'multiply_matrices_complex_numba',
    'divide_matrices_numba',
    'divide_matrices_complex_numba',
    'dot_numba',
    'dotv_numba',
    'transpose_numba'
]


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


# Elementwise operations -------------------------------------

@jit(f8[:, :](f8[:, :], f8), nogil=True, nopython=True, parallel=False, cache=True)
def scale_matrix_numba(A, b):

    """ Scale a matrix A with a float.

    Parameters
    ----------
    A : array
        Base matrix.
    b : float
        Scalar value.

    Returns
    -------
    array
        Matrix A scaled by b.

    """

    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            A[i, j] *= b
    return A


@jit(c16[:, :](c16[:, :], c16), nogil=True, nopython=True, parallel=False, cache=True)
def scale_matrix_complex_numba(A, b):

    """ Scale a complex matrix A with a complex number.

    Parameters
    ----------
    A : array
        Base complex matrix.
    b : float
        Complex number.

    Returns
    -------
    array
        Matrix A scaled by b.

    """

    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            A[i, j] *= b
    return A


@jit(f8[:, :](f8[:, :], f8[:, :]), nogil=True, nopython=True, parallel=False, cache=True)
def multiply_matrices_numba(A, B):

    """ Multiply a matrix A with another matrix B.

    Parameters
    ----------
    A : array
        First matrix.
    b : array
        Second matrix.

    Returns
    -------
    array
        Element-wise A * B.

    """

    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            A[i, j] *= B[i, j]
    return A


@jit(c16[:, :](c16[:, :], c16[:, :]), nogil=True, nopython=True, parallel=False, cache=True)
def multiply_matrices_complex_numba(A, B):

    """ Multiply a complex matrix A with another complex matrix B.

    Parameters
    ----------
    A : array
        First complex matrix.
    b : array
        Second complex matrix.

    Returns
    -------
    array
        Element-wise A * B (complex).

    """

    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            A[i, j] *= B[i, j]
    return A


@jit(f8[:, :](f8[:, :], f8[:, :]), nogil=True, nopython=True, parallel=False, cache=True)
def divide_matrices_numba(A, B):

    """ Divide a matrix A with another matrix B.

    Parameters
    ----------
    A : array
        First matrix.
    b : array
        Second matrix.

    Returns
    -------
    array
        Element-wise A / B.

    """

    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            A[i, j] /= B[i, j]
    return A


@jit(c16[:, :](c16[:, :], c16[:, :]), nogil=True, nopython=True, parallel=False, cache=True)
def divide_matrices_complex_numba(A, B):

    """ Divide a complex matrix A with another complex matrix B.

    Parameters
    ----------
    A : array
        First complex matrix.
    b : array
        Second complex matrix.

    Returns
    -------
    array
        Element-wise A / B (complex).

    """

    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            A[i, j] /= B[i, j]
    return A


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
    from numpy import complex128
    from numpy import zeros
    from numpy.random import rand

    from time import time

    m = 10**3

    A = zeros((m, m)) + 3
    b = array(list(range(m)), dtype=float64)

    tic1 = time()
    # diag_numba(A, b)
    # diag_complex_numba(array(A, dtype=complex128), array(b, dtype=complex128))
    # diag_fill_numba(A, 1.0)
    # diag_fill_complex_numba(array(A, dtype=complex128), 1.0 + 1.0j)
    # scale_matrix_numba(A, 2.0)
    # scale_matrix_complex_numba(array(A, dtype=complex128), 1.+1j)
    print(1000 * (time() - tic1))

    # tic2 = time()
    # B = array(A, dtype=complex128) * 1.+1j
    # print(1000 * (time() - tic2))
