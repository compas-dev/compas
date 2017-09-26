""""""

try:
    from compas.numerical.alglib.xalglib import sparsegetnrows
    from compas.numerical.alglib.xalglib import sparsegetncols
    from compas.numerical.alglib.xalglib import sparseiscrs
    from compas.numerical.alglib.xalglib import sparseconverttocrs
    from compas.numerical.alglib.xalglib import sparsemm
except ImportError:
    import platform
    if platform.python_implementation() == 'IronPython':
        raise


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


__all__ = []


def multiply_matrix_matrix(A, B):
    if not sparseiscrs(A):
        sparseconverttocrs(A)
    m = sparsegetnrows(A)
    n = sparsegetncols(A)
    o = 3
    res = [[0] * o for i in range(m)]
    res = sparsemm(A, B, n, res)
    return res


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":
    pass
