
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


__author__    = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__ = 'Copyright 2018, BLOCK Research Group - ETH Zurich'
__license__   = 'MIT License'
__email__     = 'liew@arch.ethz.ch'


__all__ = [
    'diag_numba',
    'diag_fill_numba',
]


@jit(f8[:, :](f8[:, :], f8[:]), nogil=True, nopython=True, parallel=True, cache=False)
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


@jit(f8[:, :](f8[:, :], f8), nogil=True, nopython=True, parallel=True, cache=False)
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
