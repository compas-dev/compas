
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
    import skcuda.misc
except ImportError as e:
    pass


__author__    = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__ = 'Copyright 2018, Block Research Group - ETH Zurich'
__license__   = 'MIT License'
__email__     = 'liew@arch.ethz.ch'


__all__ = [
    'device_cuda',
    'give_cuda',
    'get_cuda',
    'ones_cuda',
    'zeros_cuda',
]


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
        return pycuda.gpuarray.to_gpu(array(a).astype(float64))
    elif type == 'complex':
        return pycuda.gpuarray.to_gpu(array(a).astype(complex64))


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

    return skcuda.misc.ones(shape, float64)


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

    return pycuda.gpuarray.zeros(shape, dtype='float64')


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    device_cuda()
    a = give_cuda([[1., 2., 3.], [4., 5., 6.]])
    b = get_cuda(a)
    c = ones_cuda((3, 3))
    d = zeros_cuda((3, 3))
