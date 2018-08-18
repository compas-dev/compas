
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
    has_pycuda = None


__author__    = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__ = 'Copyright 2018, Block Research Group - ETH Zurich'
__license__   = 'MIT License'
__email__     = 'liew@arch.ethz.ch'


__all__ = [
    'diag_cuda',
    'transpose_cuda',
    # 'det_cuda',
    'dot_cuda',
    # 'eig_cuda',
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


# def det_cuda(a):

#     """ GPUArray square matrix determinant.

#     Parameters
#     ----------
#     a : gpuarray
#         GPUArray matrix of size (m x m).

#     Returns
#     -------
#     float
#         Determinant of the square matrix.

#     Notes
#     -----
#     - Requires CULA.

#     Examples
#     --------
#     >>> a = det_cuda(give_cuda([[5, -2, 1], [0, 3, -1], [2, 0, 7]]))
#     103

#     """

#     return skcuda.linalg.det(a)


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
    o = b.shape[1]
    nx = int(ceil(o / dim))
    ny = int(ceil(m / dim))

    func = mod.get_function('dot_cuda')
    c = pycuda.gpuarray.empty((m, o), float32)
    func(uint32(m), uint32(n), uint32(o),  a, b, c, block=(dim, dim, 1), grid=(nx, ny, 1))

    return c


# def cuda_eig(a):
#     """ Matrix Eigenvectors and Eigenvalues of GPUArray.

#     Notes
#         - Requires CULA.
#         - Input GPUArray is a square matrix, either real or complex.

#     Parameters:
#         a (gpuarray): GPUArray of a square matrix (m x m).

#     Returns:
#         gpuarray: Normalised Eigenvectors (right)
#         gpuarray: Eigenvalues.

#     """
#     vr, w = skcuda.linalg.eig(a)
#     return vr, w


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



# from numpy import float64
# from numpy import ceil

# from compas.hpc.cuda.math_ import cuda_sqrt
# from compas.hpc.cuda.math_ import cuda_sum


# __all__ = [
#     'cuda_conj',
#     'cuda_cross',
#     'cuda_hermitian',
#     'cuda_inv',
#     'cuda_normrow',
#     'cuda_pinv',
#     'cuda_svd',
#     'cuda_trace',
#     'cuda_transpose'
# ]


# def cuda_conj(a):
#     """ Complex conjugate of GPUArray elements.

#     Parameters:
#         a (gpu): Complex GPUArray.

#     Returns:
#         gpu: The complex conjugate of the GPUArray.

#     Examples:
#         a = cuda_conj(cuda_give([1 + 2.j, 3 - 4.j], type='complex'))
#         array([ 1.-2.j,  3.+4.j], dtype=complex64)
#         >>> type(a)
#         <class 'pycuda.gpuarray.GPUArray'>
#     """
#     return skcuda.linalg.conj(a)


# try:
#     kernel_code_template = """
#     __global__ void cross_product(float *a, float *b, float *c)
#     {
#         int i = threadIdx.x + blockDim.x * blockIdx.x;
#         int n = 3;
#         float A1 = a[i * n + 0];
#         float A2 = a[i * n + 1];
#         float A3 = a[i * n + 2];
#         float B1 = b[i * n + 0];
#         float B2 = b[i * n + 1];
#         float B3 = b[i * n + 2];
#         c[i * n + 0] = A2 * B3 - A3 * B2;
#         c[i * n + 1] = A3 * B1 - A1 * B3;
#         c[i * n + 2] = A1 * B2 - A2 * B1;
#     }
#     """
#     kernel_code = kernel_code_template % {'m': 3}
#     mod = pycuda.compiler.SourceModule(kernel_code)
#     cross_product = mod.get_function("cross_product")
# except NameError as e:
#     pass


# def cuda_cross(a, b, bsize):
#     """ Cross-product of two GPUArrays (row by row).

#     Parameters:
#         a (gpu): GPUArray 1 of vectors (m x 3).
#         b (gpu): GPUArray 2 of vectors (m x 3).
#         bsize (int): < Blocksize divided by 3.

#     Returns:
#         gpu: Returns the m vectors from a x b
#     """
#     m = a.shape[0]
#     c = pycuda.gpuarray.empty((m, 3), float64)
#     grid = (int(ceil(m / bsize)), 1)
#     cross_product(a, b, c, block=(bsize, 3, 1), grid=grid)
#     return c


# def cuda_hermitian(a):
#     """ Hermitian conjugate transpose of GPUArray.

#     Parameters:
#         a (gpu): Complex GPUArray.

#     Returns:
#         gpu: The complex conjugate transpose of the GPUArray.

#     Examples:
#         >>> a = cuda_hermitian(cuda_give([[1 + 2.j, 3 - 4.j],[0 - 5.j, 6 - 1.j]], type='complex'))
#         array([[ 1.-2.j,  0.+5.j],
#                [ 3.+4.j,  6.+1.j]], dtype=complex64)
#         >>> type(a)
#         <class 'pycuda.gpuarray.GPUArray'>
#     """
#     return skcuda.linalg.hermitian(a)


# def cuda_inv(a):
#     """ Inverse of GPUArray matrix.

#     Notes
#         - Requires CULA.

#     Parameters:
#         a (gpu): Input square GPUArray (m x m).

#     Returns:
#         gpu: Matrix inverse as a GPUArray (m x m).

#     Examples:
#         >>> a = cuda_inv(cuda_give([[4, 7], [2, 6]]))
#         array([[ 0.6, -0.7],
#                [-0.2,  0.4]])
#         >>> type(a)
#         <class 'pycuda.gpuarray.GPUArray'>
#     """
#     return skcuda.linalg.inv(a)


# def cuda_normrow(a):
#     """ GPUArray of vectors norm.2 (row by row).

#     Parameters:
#         a (gpu): GPUArray of vectors (m x n).

#     Returns:
#         gpu: Vector lengths (m,).

#     Examples:
#         >>> a = cuda_normrow(cuda_give([[1, 2], [3, 4]]))
#         array([ 2.23606798,  5.])
#         >>> type(a)
#         <class 'pycuda.gpuarray.GPUArray'>
#     """
#     return cuda_sqrt(cuda_sum(a * a, axis=1))


# def cuda_pinv(a):
#     """ Moore-Penrose pseudo inverse of the GPUArray.

#     Notes:
#         - Singular values smaller than 10^-15 are set to zero.
#         - Requires CULA.

#     Parameters:
#         a (gpu): Input GPUArray (m x n).

#     Returns:
#         gpu: Pseudo inverse.

#     Examples:
#         >>> a = cuda_pinv(cuda_give([[1, 3, -1], [2, 0, 3]]))
#         array([[ 0.1056338 ,  0.16197183],
#                [ 0.27464789,  0.02112676],
#                [-0.07042254,  0.22535211]])
#         >>> type(a)
#         <class 'pycuda.gpuarray.GPUArray'>
#     """
#     return skcuda.linalg.pinv(a)


# def cuda_svd(a, jobu='S', jobvt='S'):
#     """ GPUArray Singular Value Decomposition.

#     Notes
#         - Requires CULA.

#     Parameters:
#         a (gpu): GPUArray (m x n) to decompose.

#     Returns:
#         gpu: Unitary matrix (m x k).
#         gpu: Singular values.
#         gpu: vh matrix (k x n).

#     """
#     return skcuda.linalg.svd(a)


# def cuda_trace(a):
#     """ GPUArray trace, the sum along the main diagonal.

#     Parameters:
#         a (gpu): Input GPUArray.

#     Returns:
#         float: tr(GPUArray).

#     Examples:
#         >>> a = cuda_trace(cuda_give([[0, 1], [2, 3]]))
#         3.0
#         >>> type(a)
#         <class 'numpy.float64'>
#     """
#     return skcuda.linalg.trace(a)
