
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

try:
    from numpy import ceil
    from numpy import diag
    from numpy import eye
    from numpy import float32
    from numpy import uint32
except:
    pass

try:
    from compas.hpc import give_cuda
except:
    pass

try:
    import pycuda
    import pycuda.autoinit
    has_pycuda = True
except:
    has_pycuda = False


__all__ = [
    'diag_cuda',
    'transpose_cuda',
    'dot_cuda',
    'eye_cuda',
]


kernel = """

__global__ void dot_cuda(int m, int n, int o, float *a, float *b, float *c) {

    // int nx  = blockDim.x * gridDim.x;
    int idx = threadIdx.x + blockDim.x*blockIdx.x;
    int idy = threadIdx.y + blockDim.y*blockIdx.y;

    if (idx < o && idy < m) {

        int id  = idy * o + idx;
        float p = 0.;

        for (int i = 0; i < n; i++) {
            float ai = a[idy * n + i];
            float bi = b[i * o + idx];
            p += ai * bi;
        }

        c[id] = p;
    }
}
"""
if has_pycuda:
    mod = pycuda.compiler.SourceModule(kernel)


def transpose_cuda(a):

    """ Return the transpose of a GPUArray.

     Parameters
    ----------
    a : GPUArray
        Array on GPU memory.

    Returns
    -------
    gpuarray
        Tranpose of the input GPUArray.

    Examples
    --------
    >>> a = transpose_cuda(give_cuda([[0, 1], [2, 3]]))
    array([[ 0.,  2.],
           [ 1.,  3.]])

    >>> type(a)
    <class 'pycuda.gpuarray.GPUArray'>

    """

    return a.transpose()


def dot_cuda(a, b, dim=2):

    """ Matrix multiplication of two GPUArrays.

    Parameters
    ----------
    a : gpuarray
        GPUArray matrix 1 (m x n).
    b : gpuarray
        GPUArray matrix 2 (n x o).
    dim : int
        Dimension of square CUDA block.

    Returns
    -------
    gpuarray
        [c] = [a][b] of size (m x o)

    Examples
    --------
    >>> a = give_cuda([[0, 1], [2, 3]])
    >>> b = give_cuda([[0, 1], [1, 0]])
    >>> c = dot_cuda(a, b)
    array([[ 1.,  0.],
           [ 3.,  2.]])

    >>> type(c)
    <class 'pycuda.gpuarray.GPUArray'>

    """

    m, n = a.shape
    o  = b.shape[1]
    nx = int(ceil(o / dim))
    ny = int(ceil(m / dim))

    func = mod.get_function('dot_cuda')
    c = pycuda.gpuarray.empty((m, o), dtype=float32)
    func(uint32(m), uint32(n), uint32(o),  a, b, c, block=(dim, dim, 1), grid=(nx, ny, 1))

    return c


def diag_cuda(a):

    """ Construct GPUArray diagonal.

    Parameters
    ----------
    a : array, list
        Elements along diagonal.

    Returns
    -------
    gpuarray
        GPUArray with inserted diagonal.

    Examples
    --------
    >>> a = diag_cuda([1, 2, 3])
    array([[ 1.,  0.,  0.],
           [ 0.,  2.,  0.],
           [ 0.,  0.,  3.]])

    >>> type(a)
    <class 'pycuda.gpuarray.GPUArray'>

    """

    return give_cuda(diag(a))


def eye_cuda(n):

    """ Create GPUArray identity matrix (ones on diagonal) of size (n x n).

    Parameters
    ----------
    n : int
        Size of identity matrix (n x n).

    Returns
    -------
    gpuarray
        Identity matrix (n x n) as GPUArray.

    Examples
    --------
    >>> a = eye_cuda(3)
    array([[ 1.,  0.,  0.],
           [ 0.,  1.,  0.],
           [ 0.,  0.,  1.]])

    >>> type(a)
    <class 'pycuda.gpuarray.GPUArray'>

    """

    return give_cuda(eye(n, dtype=float32))


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    from compas.hpc import get_cuda

    from numpy import allclose
    from numpy import dot
    from numpy.random import rand

    from time import time

    a = diag_cuda([1., 2., 3.])
    a = eye_cuda(3)
    b = give_cuda([[5, -2, 1], [0, 3, -1], [2, 0, 7]])
    c = transpose_cuda(b)

    a = rand(200, 3)
    b = rand(3, 500)
    c = dot(a, b)

    a_ = give_cuda(a)
    b_ = give_cuda(b)
    c_ = dot_cuda(a_, b_)

    tic = time()
    print(1000 * (time() - tic))
    print(allclose(c, get_cuda(c_)))
