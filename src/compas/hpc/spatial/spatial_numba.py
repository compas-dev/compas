
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from numba import f8
from numba import jit

try:
    from numba import prange
except ImportError:
    prange = range

from numpy import sqrt
from numpy import zeros


__author__    = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__ = 'Copyright 2018, BLOCK Research Group - ETH Zurich'
__license__   = 'MIT License'
__email__     = 'liew@arch.ethz.ch'


__all__ = [
    'distance_matrix_numba',
]


@jit(f8[:, :](f8[:, :], f8[:, :]), nogil=True, nopython=True, parallel=False, cache=True)
def distance_matrix_numba(A, B):

    """ Distance matrix between two point clouds.

    Parameters
    ----------
    A : array
        Point cloud 1 (m x 3).
    B : array
        Point cloud 2 (n x 3).

    Returns
    -------
    array
        Distance matrix (m x n).

    """

    m = A.shape[0]
    n = B.shape[0]
    o = zeros((m, n))

    for i in range(m):
        u = A[i, :]
        for j in range(n):
            v = B[j, :]
            dx = u[0] - v[0]
            dy = u[1] - v[1]
            dz = u[2] - v[2]
            o[i, j] = sqrt(dx**2 + dy**2 + dz**2)

    return o


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    from numpy import allclose
    from numpy.random import rand

    from scipy.spatial import distance_matrix

    from time import time

    m = 10000

    A = rand(m, 3)
    B = rand(m, 3)

    tic1 = time()
    C = distance_matrix_numba(A, B)
    print(time() - tic1)

    tic2 = time()
    D = distance_matrix(A, B)
    print(time() - tic2)

    print(allclose(C, D))
