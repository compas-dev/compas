
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

try:
    from numpy import diag
    from numpy import eye
    from numpy import float32
except:
    pass

try:
    from compas.hpc import give_cl
except:
    pass

try:
    import pyopencl as cl
    import pyopencl.array as cl_array
except:
    pass


__author__    = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__ = 'Copyright 2018, BLOCK Research Group - ETH Zurich'
__license__   = 'MIT License'
__email__     = 'liew@arch.ethz.ch'


__all__ = [
    'diag_cl',
    'transpose_cl',
#     # 'dot_cl',
    'eye_cl',
]


def transpose_cl(a):

    """ Return the transpose of a GPUArray.

    Parameters
    ----------
    a : GPUArray
        Array on GPU memory.

    Returns
    -------
    gpuarray
        Tranpose of the input GPUArray.

    """

    return a.transpose()


# def dot_cl(a, b):

#     """ Matrix multiplication of two GPUArrays.

#     Parameters
#     ----------
#     a : gpuarray
#         GPUArray matrix 1 (m x n).
#     b : gpuarray
#         GPUArray matrix 2 (n x o).

#     Returns
#     -------
#     gpuarray
#         [c] = [a][b] of size (m x o)

#     """

#     return cl_array.dot(a, b)


def diag_cl(queue, a):

    """ Construct GPUArray diagonal.

    Parameters
    ----------
    queue
        PyOpenCL queue.
    a : array, list
        Elements along diagonal.

    Returns
    -------
    gpuarray
        GPUArray with inserted diagonal.

    """

    return give_cl(queue, diag(a))


def eye_cl(queue, n):

    """ Create GPUArray identity matrix (ones on diagonal) of size (n x n).

    Parameters
    ----------
    queue
        PyOpenCL queue.
    n : int
        Size of identity matrix (n x n).

    Returns
    -------
    gpuarray
        Identity matrix (n x n) as GPUArray.

    """

    return give_cl(queue, eye(n, dtype=float32))


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    from compas.hpc import get_cl

    ctx = cl.create_some_context()
    queue = cl.CommandQueue(ctx)

    a_ = give_cl(queue, [[0, 1, 2]])

    print(get_cl(diag_cl(queue, [0, 1, 2])))
    print(get_cl(eye_cl(queue, 3)))
    print(get_cl(transpose_cl(a_)))

#     a = give_cl(queue, [[0, 1], [2, 3]])
#     b = give_cl(queue, [[0, 1], [1, 0]])
#     # c = get_cl(dot_cl(a, b))
