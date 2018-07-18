
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

try:
    from numpy import array
    from numpy import float32
    from numpy import complex64
except:
    pass

try:
    import pycuda
    import pycuda.gpuarray as cuda_array
    import pycuda.autoinit
    import pycuda.curandom
except:
    pass


__author__    = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__ = 'Copyright 2018, Block Research Group - ETH Zurich'
__license__   = 'MIT License'
__email__     = 'liew@arch.ethz.ch'


__all__ = [
    'rand_cuda',
    'device_cuda',
    'give_cuda',
    'get_cuda',
    'ones_cuda',
    'zeros_cuda',
    'tile_cuda',
    # 'hstack_cuda',
    # 'vstack_cuda',
]


def rand_cuda(shape):

    """ Create random values in the range [0, 1] as GPUArray.

    Parameters
    ----------
    shape : tuple
        Size of the random array.

    Returns
    -------
    gpuarray
        Random floats from 0 to 1 in GPUArray.

    Examples
    --------
    >>> a = rand_cuda((2, 2))
    array([[ 0.80916596,  0.82687163],
           [ 0.03921388,  0.44197764]])

    >>> type(a)
    <class 'pycuda.gpuarray.GPUArray'>

    """

    return pycuda.curandom.rand(shape, float32)


def device_cuda():

    """ Displays the CUDA GPU device details.

    Parameters
    ----------
    None

    Returns
    -------
    None

    Examples
    --------
    >>> device_cuda()
    Device: GeForce GTX 1060 6GB
    Compute Capability: 6.1
    Total Memory: 6291 MB
    CLOCK_RATE: 1746500
    ...
    MAX_BLOCK_DIM_X: 1024
    MAX_BLOCK_DIM_Y: 1024
    MAX_BLOCK_DIM_Z: 64
    ...etc

    """

    pycuda.driver.init()
    dev = pycuda.driver.Device(0)
    print('Device: ' + dev.name())
    print('Compute Capability: %d.%d' % dev.compute_capability())
    print('Total Memory: %s MB' % (dev.total_memory() // (1024000)))
    atts = [(str(att), value) for att, value in dev.get_attributes().items()]
    atts.sort()
    for att, value in atts:
        print('%s: %s' % (att, value))


def give_cuda(a, type='real'):

    """ Give a list or an array to GPU memory.

    Parameters
    ----------
    a : array, list
        Data to send to the GPU memory.
    type : str
        'real' or 'complex'.

    Returns
    -------
    gpuarray
        GPUArray of the input array.

    Examples
    --------
    >>> a = give_cuda([[1., 2., 3.], [4., 5., 6.]])
    array([[ 1.,  2.,  3.],
           [ 4.,  5.,  6.]])

    >>> type(a)
    <class 'pycuda.gpuarray.GPUArray'>

    >>> a.shape
    (2, 3)

    >>> a.dtype
    dtype('float64')

    >>> a.reshape((1, 6))
    array([[ 1.,  2.,  3.,  4.,  5.,  6.]])

    """

    if type == 'real':
        return cuda_array.to_gpu(array(a).astype(float32))
    elif type == 'complex':
        return cuda_array.to_gpu(array(a).astype(complex64))


def get_cuda(a):

    """ Get back GPUArray from GPU memory as NumPy array.

    Parameters
    ----------
    a : gpuarray
        Data on the GPU memory to retrieve.

    Returns
    -------
    array
        The GPUArray returned to RAM as NumPy array.

    Examples
    --------
    >>> a = give_cuda([1, 2, 3])
    >>> b = get_cuda(a)
    array([ 1.,  2.,  3.])

    >>> type(b)
    <class 'numpy.ndarray'>

    """

    return a.get()


def ones_cuda(shape):

    """ Create GPUArray of ones directly on GPU memory.

    Parameters
    ----------
    shape : tuple
        Dimensions of the GPUArray.

    Returns
    -------
    gpuarray
        GPUArray of ones.

    Examples
    --------
    >>> a = ones_cuda((3, 2))
    array([[ 1.,  1.],
           [ 1.,  1.],
           [ 1.,  1.]])

    >>> type(a)
    <class 'pycuda.gpuarray.GPUArray'>

    """

    a = cuda_array.GPUArray(shape, dtype=float32, allocator=pycuda.driver.mem_alloc, order='C')
    a.fill(1.0)
    return a


def zeros_cuda(shape):

    """ Create GPUArray of zeros directly on GPU memory.

    Parameters
    ----------
    shape : tuple
        Dimensions of the GPUArray.

    Returns
    -------
    gpuarray
        GPUArray of zeros.

    Examples
    --------
    >>> a = zeros_cuda((3, 2))
    array([[ 0.,  0.],
           [ 0.,  0.],
           [ 0.,  0.]])

    >>> type(a)
    <class 'pycuda.gpuarray.GPUArray'>

    """

    return cuda_array.zeros(shape, dtype=float32)


def tile_cuda(a, shape):

    """ Horizontally and vertically tile a GPUArray.

    Parameters
    ----------
    a : gpuarray
        GPUArray to tile.
    shape : tuple
        Number of vertical and horizontal tiles.

    Returns
    -------
    gpuarray
        Tiled GPUArray.

    Notes
    -----
    - A temporary function, to be made into a kernal.

    Examples
    --------
    >>> a = tile_cuda(give_cuda([[1, 2], [3, 4]]), (2, 2))
    array([[ 1.,  2.,  1.,  2.],
           [ 3.,  4.,  3.,  4.],
           [ 1.,  2.,  1.,  2.],
           [ 3.,  4.,  3.,  4.]])

    >>> type(a)
    <class 'pycuda.gpuarray.GPUArray'>

    """
    m, n = a.shape

    b = zeros_cuda((m * shape[0], n))
    for i in range(shape[0]):
        b[i * m:i * m + m, :] = a

    c = zeros_cuda((m * shape[0], n * shape[1]))
    for i in range(shape[1]):
        c[:, i * n:i * n + n] = b

    return c


def hstack_cuda():
    raise NotImplementedError


def vstack_cuda():
    raise NotImplementedError


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    # device_cuda()
    a = give_cuda([[1., 2., 3.], [4., 5., 6.]])
    # a = give_cuda([1.+1j, 2.+2j, 3.+3j], type='complex')
    # a = get_cuda(a)
    # a = ones_cuda((3, 3))
    # a = zeros_cuda((3, 3))
    # a = rand_cuda((2, 2))
    # a = tile_cuda(give_cuda([[1, 2], [3, 4]]), (2, 2))

    print(a)
