
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from numpy import array
# from numpy import float64
# from numpy import complex64

try:
    from numba import cuda
except ImportError as e:
    pass


__author__    = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__ = 'Copyright 2018, Block Research Group - ETH Zurich'
__license__   = 'MIT License'
__email__     = 'liew@arch.ethz.ch'


__all__ = [
    'select_cuda',
    'current_cuda',
    'devices_cuda',
    'give_cuda',
    'get_cuda',
    # 'ones_cuda',
    # 'zeros_cuda',
    # 'rand_cuda',
    # 'tile_cuda',
]


def select_cuda(id):

    """ Select a CUDA device by its ID.

    Parameters
    ----------
    id : int
        Device integer identifier.

    Returns
    -------
    obj
        Device object.

    """

    dev = cuda.select_device(id)
    print('CUDA device selected : {0}'.format(dev))
    return dev


def current_cuda():

    """ Currently selected CUDA device.

    Parameters
    ----------
    None

    Returns
    -------
    obj
        Device object.

    """

    dev = cuda.gpus.current
    print('Current CUDA device : {0}'.format(dev))
    return dev


def devices_cuda():

    """ Display available CUDA devices.

    Parameters
    ----------
    None

    Returns
    -------
    obj
        Function of available devices.

    """

    return cuda.list_devices()


# def rand_cuda(shape):

#     """ Create random values in the range [0, 1] as GPUArray.

#     Parameters
#     ----------
#     shape : tuple
#         Size of the random array.

#     Returns
#     -------
#     gpuarray
#         Random floats from 0 to 1 in GPUArray.

#     Examples
#     --------
#     >>> a = rand_cuda((2, 2))
#     array([[ 0.80916596,  0.82687163],
#            [ 0.03921388,  0.44197764]])

#     >>> type(a)
#     <class 'pycuda.gpuarray.GPUArray'>

#     """

#     return pycuda.curandom.rand(shape, float64)


def give_cuda(a):

    """ Give an array to GPU memory.

    Parameters
    ----------
    a : array
        Array to send to the GPU memory.

    Returns
    -------
    gpuarray
        DeviceNDArray of the input array.

    Examples
    --------
    >>> a = give_cuda(array([[1., 2., 3.], [4., 5., 6.]]))
    <numba.cuda.cudadrv.devicearray.DeviceNDArray object at 0x0000022B3C7323C8>

    >>> a.shape
    (2, 3)

    >>> a.dtype
    float64

    """

    return cuda.to_device(array(a))


def get_cuda(a):

    """ Get back a GPUArray from GPU memory as an array.

    Parameters
    ----------
    a : gpuarray
        Data on the GPU memory to retrieve.

    Returns
    -------
    array
        The DeviceNDArray returned to RAM as an array.

    Examples
    --------
    >>> a = give_cuda(array([1., 2., 3.]))
    >>> b = get_cuda(a)
    array([ 1.,  2.,  3.])

    >>> type(b)
    <class 'numpy.ndarray'>

    """

    return a.copy_to_host()


# def ones_cuda(shape):

#     """ Create GPUArray of ones directly on GPU memory.

#     Parameters
#     ----------
#     shape : tuple
#         Dimensions of the GPUArray.

#     Returns
#     -------
#     gpuarray
#         GPUArray of ones.

#     Examples
#     --------
#     >>> a = ones_cuda((3, 2))
#     array([[ 1.,  1.],
#            [ 1.,  1.],
#            [ 1.,  1.]])

#     >>> type(a)
#     <class 'pycuda.gpuarray.GPUArray'>

#     """

#     return skcuda.misc.ones(shape, float64)


# def zeros_cuda(shape):

#     """ Create GPUArray of zeros directly on GPU memory.

#     Parameters
#     ----------
#     shape : tuple
#         Dimensions of the GPUArray.

#     Returns
#     -------
#     gpuarray
#         GPUArray of zeros.

#     Examples
#     --------
#     >>> a = zeros_cuda((3, 2))
#     array([[ 0.,  0.],
#            [ 0.,  0.],
#            [ 0.,  0.]])

#     >>> type(a)
#     <class 'pycuda.gpuarray.GPUArray'>

#     """

#     return pycuda.gpuarray.zeros(shape, dtype='float64')


# def tile_cuda(a, shape):

#     """ Horizontally and vertically tile a GPUArray.

#     Parameters
#     ----------
#     a : gpuarray
#         GPUArray to tile.
#     shape : tuple
#         Number of vertical and horizontal tiles.

#     Returns
#     -------
#     gpuarray
#         Tiled GPUArray.

#     Notes
#     -----
#     - A temporary function, to be made into a kernal.

#     Examples
#     --------
#     >>> a = tile_cuda(give_cuda([[1, 2], [3, 4]]), (2, 2))
#     array([[ 1.,  2.,  1.,  2.],
#            [ 3.,  4.,  3.,  4.],
#            [ 1.,  2.,  1.,  2.],
#            [ 3.,  4.,  3.,  4.]])

#     >>> type(a)
#     <class 'pycuda.gpuarray.GPUArray'>

#     """
#     m, n = a.shape

#     b = zeros_cuda((m * shape[0], n))
#     for i in range(shape[0]):
#         b[i * m:i * m + m, :] = a

#     c = zeros_cuda((m * shape[0], n * shape[1]))
#     for i in range(shape[1]):
#         c[:, i * n:i * n + n] = b

#     return c


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    from numpy import array

    select_cuda(0)
    current_cuda()
    print(devices_cuda)

    A = array([[1., 2.], [3., 4.]])

    A_ = give_cuda(A)
    B = get_cuda(A_)
    print(type(B))

#     c = ones_cuda((3, 3))
#     d = zeros_cuda((3, 3))
#     e = rand_cuda((2, 2))
#     f = tile_cuda(give_cuda([[1, 2], [3, 4]]), (2, 2))
