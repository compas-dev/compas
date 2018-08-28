from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import sys
import compas

try:
    from compas.numerical.alglib.core import Array
    from compas.numerical.alglib.core import Zeros
    from compas.numerical.alglib.core import xalglib

except ImportError:
    compas.raise_if_ironpython()


__all__ = ['solve', 'spsolve', 'splsqr']


class LinalgError(Exception):
    pass


# def multiply_matrix_matrix(A, B):
#     if not sparseiscrs(A):
#         sparseconverttocrs(A)
#     m = sparsegetnrows(A)
#     n = sparsegetncols(A)
#     o = 3
#     res = [[0] * o for i in range(m)]
#     res = sparsemm(A, B, n, res)
#     return res


# rmatrixsolvelu(m)(fast) => combine with rmatrixlu (does not use caching)
# rmatrixsolve(m)(fast)

def solve(A, b, fast=True):
    m, k = A.shape
    k, n = b.shape
    if m != k:
        raise LinalgError('Solver requires square matrix.')
    if not n:
        n = 1
    if n == 1:
        if fast:
            info, x = xalglib.rmatrixsolvefast(A.data, m, b.flatdata)
        else:
            info, rep, x = xalglib.rmatrixsolve(A.data, m, b.flatdata)
    else:
        if fast:
            x, info = xalglib.rmatrixsolvemfast(A.data, m, b.data, n)
        else:
            info, rep, x = xalglib.rmatrixsolvem(A.data, m, b.data, n, True)
    return Array(x, (m, n))


def spsolve(A, b):
    pass


def splsqr(A, b, x=None):
    m, n = A.shape
    n, k = b.shape
    if not k:
        k = 1
    problem = xalglib.linlsqrcreate(m, n)
    if k > 1:
        if not x:
            x = Zeros((m, k))
        M = A.matrix
        for dim in range(k):
            xalglib.linlsqrsolvesparse(problem, M, b[:, dim].data)
            result = xalglib.linlsqrresults(problem)
            x[:, dim] = result[0]
        return x
    if not x:
        x = Zeros((m, k))
    xalglib.linlsqrsolvesparse(problem, M, b.data)
    result = xalglib.linlsqrresults(problem)
    x[:, 0] = result[0]
    return x


def lu_solve():
    pass


def cho_solve():
    pass


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
