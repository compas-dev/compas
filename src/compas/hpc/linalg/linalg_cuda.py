
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from numpy import array
from numpy import float64
from numpy import complex64

try:
    import pycuda
    import pycuda.autoinit
except ImportError as e:
    pass

try:
    import skcuda
    import skcuda.autoinit
    import skcuda.linalg
except ImportError as e:
    pass


__author__    = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__ = 'Copyright 2018, Block Research Group - ETH Zurich'
__license__   = 'MIT License'
__email__     = 'liew@arch.ethz.ch'


__all__ = [
    'diag_cuda',
]


def diag_cuda(a):

    """ Construct or extract GPUArray diagonal.

    Parameters
    ----------
    a : gpuarray
        GPUArray (1D or 2D).

    Returns
    -------
    gpuarray
        GPUArray with inserted diagonal, or vector of diagonal.

    Notes
    -----
    - If input is 1D, a GPUArray is constructed, if 2D, the diagonal is extracted.

    Examples
    --------
    >>> a = diag_cuda(cuda_give([1, 2, 3]))
    array([[ 1.,  0.,  0.],
           [ 0.,  2.,  0.],
           [ 0.,  0.,  3.]])

    >>> b = diag_cuda(a)
    array([ 1.,  2.,  3.])

    >>> type(b)
    <class 'pycuda.gpuarray.GPUArray'>

    """

    return skcuda.linalg.diag(a)


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

    return skcuda.linalg.eye(n, dtype=float64)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    from compas.hpc.core.cuda import cuda_give

    print(diag_cuda(cuda_give([1., 2., 3.])))
    print(eye_cuda(3))
