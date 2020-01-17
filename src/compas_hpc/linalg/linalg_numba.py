
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from numba import f8
from numba import c16
from numba import jit

from numpy import cos
from numpy import sin
from numpy import zeros


__all__ = [
    'rotate_x_numba',
    'rotate_y_numba',
    'rotate_z_numba',
    'trace_numba',
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
    'transpose_numba',
]


# ---------------------------------------------------------------------------------------------------
# Linear algebra
# ---------------------------------------------------------------------------------------------------

@jit(f8(f8[:, :]), nogil=True, nopython=True, parallel=False, cache=True)
def trace_numba(A):

    """ Trace of matrix A.

    Parameters
    ----------
    A : array
        Matrix.

    Returns
    -------
    array
        trace(A).

    """

    c = 0

    for i in range(A.shape[0]):
        c += A[i, i]

    return c


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

    """ Fill complex matrix A with a diagonal represented by vector b (complex).

    Parameters
    ----------
    A : array
        Base matrix (complex).
    b : array
        Diagonal vector to fill with (complex).

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

    """ Fill complex matrix A with a diagonal represented by complex number b.

    Parameters
    ----------
    A : array
        Base matrix (complex).
    b : float
        Complex number to fill with.

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
        AB of size (m x p).

    """

    m = A.shape[0]
    n = A.shape[1]
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
        Ab of size (m,).

    """

    m = A.shape[0]
    n = A.shape[1]
    C = zeros(m)

    for i in range(m):
        for j in range(n):
            C[i] += A[i, j] * b[j]

    return C


@jit(f8[:](f8[:], f8), nogil=True, nopython=True, parallel=False, cache=True)
def rotate_x_numba(a, theta):

    """ Rotate a vector about the x axis.

    Parameters
    ----------
    a : array
        Vector [x, y, z].
    theta : float
        Angle in radians to rotate by, anti-clockwise positive.

    Returns
    -------
    array
        Rotated vector.

    """

    c = cos(theta)
    s = sin(theta)

    T = zeros((3, 3))
    T[0, :] = [1,  0,  0]
    T[1, :] = [0,  c, -s]
    T[2, :] = [0,  s,  c]

    return dotv_numba(T, a)


@jit(f8[:](f8[:], f8), nogil=True, nopython=True, parallel=False, cache=True)
def rotate_y_numba(a, theta):

    """ Rotate a vector about the y axis.

    Parameters
    ----------
    a : array
        Vector [x, y, z].
    theta : float
        Angle in radians to rotate by, anti-clockwise positive.

    Returns
    -------
    array
        Rotated vector.

    """

    c = cos(theta)
    s = sin(theta)

    T = zeros((3, 3))
    T[0, :] = [c, 0, -s]
    T[1, :] = [0, 1,  0]
    T[2, :] = [s, 0,  c]

    return dotv_numba(T, a)


@jit(f8[:](f8[:], f8), nogil=True, nopython=True, parallel=False, cache=True)
def rotate_z_numba(a, theta):

    """ Rotate a vector about the z axis.

    Parameters
    ----------
    a : array
        Vector [x, y, z].
    theta : float
        Angle in radians to rotate by, anti-clockwise positive.

    Returns
    -------
    array
        Rotated vector.

    """

    c = cos(theta)
    s = sin(theta)

    T = zeros((3, 3))
    T[0, :] = [c, -s, 0]
    T[1, :] = [s,  c, 0]
    T[2, :] = [0,  0, 1]

    return dotv_numba(T, a)


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

    m = A.shape[0]
    n = A.shape[1]
    B = zeros((n, m))

    for i in range(m):
        for j in range(n):
            B[j, i] = A[i, j]

    return B


# ---------------------------------------------------------------------------------------------------
# Elementwise
# ---------------------------------------------------------------------------------------------------

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
        Complex matrix A scaled by b.

    """

    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            A[i, j] *= b

    return A


@jit(f8[:, :](f8[:, :], f8[:, :]), nogil=True, nopython=True, parallel=False, cache=True)
def multiply_matrices_numba(A, B):

    """ Multiply element-wise a matrix A with another matrix B.

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

    """ Multiply element-wise a complex matrix A with another complex matrix B.

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

    """ Divide element-wise a matrix A with another matrix B.

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

    """ Divide element-wise a complex matrix A with another complex matrix B.

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


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    from numpy import array
    from numpy import complex128
    from numpy import dot
    from numpy import pi
    from numpy import ones
    from numpy import zeros


    A = zeros((5, 5)) + 2
    B = zeros((5, 5), dtype=complex128) + (1 + 1j)
    C = zeros((5, 5)) + 4
    D = zeros((5, 5), dtype=complex128) + (1 - 2j)
    E = zeros((5, 2)) + 1
    b = ones(5)
    c = ones(5) + 3j
    d = ones(5) * 2
    e = ones(5) * 3
    # b = array(list(range(m)), dtype=float64)

    # print(diag_numba(A, b))
    # print(diag_complex_numba(B, c))
    # print(diag_fill_numba(A, 3.0))
    # print(diag_fill_complex_numba(B, 3.0 + 2j))
    # print(scale_matrix_numba(A, 3))
    # print(scale_matrix_complex_numba(B, 1 + 2j))
    # print(multiply_matrices_numba(A, C))
    # print(divide_matrices_numba(A, C))
    # print(multiply_matrices_complex_numba(B, D))
    # print(divide_matrices_complex_numba(B, D))
    # print(dot(A, C))
    # print(dot_numba(A, C))
    # print(dot(A, d[:, None]))
    # print(dotv_numba(A, d))
    # print(transpose_numba(E))
    # print(trace_numba(A))
    # print(rotate_z_numba(array([1., 0., 3.]), pi/2))
    # print(rotate_y_numba(array([1., 2., 0.]), pi/2))
    print(rotate_x_numba(array([3., 2., 0.]), pi/2))
