from numpy import array
from numpy import float32
from numpy import float64
from numpy import complex64

try:
    import pycuda
    import pycuda.autoinit
    import pycuda.curandom
    import pycuda.gpuarray
except ImportError as e:
    pass

try:
    import skcuda
    import skcuda.autoinit
    import skcuda.linalg
except ImportError as e:
    pass


__author__     = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2016, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'liew@arch.ethz.ch'


__all__ = [
    'cuda_diag',
    'cuda_eye',
    'cuda_get',
    'cuda_give',
    'cuda_ones',
    'cuda_random',
    'cuda_real',
    'cuda_reshape',
    'cuda_flatten',
    'cuda_tile',
    'cuda_zeros',
]


def cuda_diag(a):
    """ Construct or extract GPUArray diagonal.

    Note:
        If a is 1D, a GPUArray is constructed, if 2D, the diagonal is extracted.

    Parameters:
        a (gpu): GPUArray (1D or 2D).

    Returns:
        gpu: GPUArray with inserted diagonal, or vector of diagonal.

    Examples:
        >>> a = cuda_diag(cuda_give([1, 2, 3]))
        array([[ 1.,  0.,  0.],
               [ 0.,  2.,  0.],
               [ 0.,  0.,  3.]])
        >>> b = cuda_diag(a)
        array([ 1.,  2.,  3.])
        >>> type(b)
        <class 'pycuda.gpuarray.GPUArray'>
    """
    return skcuda.linalg.diag(a)


def cuda_eye(n, bit=64):
    """ Create GPUArray identity matrix (ones on diagonal) of size (n x n).

    Parameters:
        n (int): Size of identity matrix (n x n).
        bit (int): 32 or 64 for corresponding float precision.

    Returns:
        gpu: Identity matrix (n x n) as GPUArray.

    Examples:
        >>> a = cuda_eye(3)
        array([[ 1.,  0.,  0.],
               [ 0.,  1.,  0.],
               [ 0.,  0.,  1.]])
        >>> type(a)
        <class 'pycuda.gpuarray.GPUArray'>
    """
    if bit == 32:
        return skcuda.linalg.eye(n, dtype=float32)
    elif bit == 64:
        return skcuda.linalg.eye(n, dtype=float64)


def cuda_flatten(a):
    """ Flatten/ravel out a GPUArray.

    Parameters:
        a (gpu): GPUArray.

    Returns:
        gpu: 1D version of original GPUArray.

    Examples:
        >>> a = cuda_flatten(cuda_eye(3))
        array([ 1.,  0.,  0.,  0.,  1.,  0.,  0.,  0.,  1.])
        >>> type(a)
        <class 'pycuda.gpuarray.GPUArray'>
    """
    return a.ravel()


def cuda_get(a):
    """ Get back GPUArray from GPU memory as NumPy array.

    Parameters:
        a (gpu): Data on the GPU memory to retrieve.

    Returns:
        array: The GPUArray returned to RAM as NumPy array.

    Examples:
        >>> a = cuda_give([1, 2, 3], bit=64)
        >>> b = cuda_get(a)
        array([ 1.,  2.,  3.])
        >>> type(b)
        <class 'numpy.ndarray'>
    """
    return a.get()


def cuda_give(a, bit=64, type='real'):
    """ Give a list or an array to GPU memory.

    Parameters:
        a (array, list): Data to send to the GPU memory.
        bit (int): 32 or 64 for corresponding float precision.
        type (str): 'real' or 'complex'.

    Returns:
        gpu: GPUArray of input array.

    Creates and sends an array of float32 or float64 dtype from RAM to GPU
    memory.

    Examples:
        >>> a = cuda_give([[1, 2, 3], [4, 5, 6]], bit=64)
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
        if bit == 32:
            return pycuda.gpuarray.to_gpu(array(a).astype(float32))
        elif bit == 64:
            return pycuda.gpuarray.to_gpu(array(a).astype(float64))
    elif type == 'complex':
        if bit == 32:
            print('Complex numbers in 32 bit are not supported')
        elif bit == 64:
            return pycuda.gpuarray.to_gpu(array(a).astype(complex64))


def cuda_imag(a):
    """ Return the imaginary parts of GPUArray.

    Parameters:
        a (gpu): Complex GPUArray.

    Returns:
        gpu: Real parts of the input GPUArray.

    Examples:
        >>> cuda_imag(cuda_give([1 + 2.j, 2 - 4.j], type='complex'))
        array([ 2., -4.], dtype=float32)
    """
    return a.imag


def cuda_ones(shape, bit=64):
    """ Create GPUArray of ones directly on GPU memory.

    Parameters:
        shape (tuple): Dimensions of the GPUArray.
        bit (int): 32 or 64 for corresponding float precision.

    Returns:
        gpu: GPUArray of ones.

    Examples:
        >>> a = cuda_ones((3, 2), bit=64)
        array([[ 1.,  1.],
               [ 1.,  1.],
               [ 1.,  1.]])
        >>> type(a)
        <class 'pycuda.gpuarray.GPUArray'>
    """
    if bit == 32:
        return skcuda.misc.ones(shape, float32)
    if bit == 64:
        return skcuda.misc.ones(shape, float64)


def cuda_random(shape, bit=64):
    """ Create random values in the range [0, 1] as GPUArray.

    Parameters:
        shape (tuple): Size of the random array.
        bit (int): 32 or 64 for corresponding float precision.

    Returns:
        gpu: Random floats from 0 to 1 in GPUArray.

    Examples:
        >>> a = cuda_random((2, 2), bit=64)
        array([[ 0.80916596,  0.82687163],
               [ 0.03921388,  0.44197764]])
        >>> type(a)
        <class 'pycuda.gpuarray.GPUArray'>
    """
    if bit == 32:
        return pycuda.curandom.rand(shape, float32)
    elif bit == 64:
        return pycuda.curandom.rand(shape, float64)


def cuda_real(a):
    """ Return the real parts of GPUArray.

    Parameters:
        a (gpu): Complex GPUArray.

    Returns:
        gpu: Real parts of the input GPUArray.

    Examples:
        >>> cuda_real(cuda_give([1 + 2.j, 2 - 4.j], type='complex'))
        array([ 1.,  2.], dtype=float32)
    """
    return a.real


def cuda_reshape(a, shape):
    """ Reshape a GPUArray.

    Parameters:
        a (gpu): GPUArray.
        shape (tuple): Dimension of new reshaped GPUArray.

    Returns:
        gpu: Reshaped GPUArray.

    Examples:
        >>> a = cuda_reshape(cuda_give([[1, 2], [3, 4]]), (4, 1))
        array([[ 1.],
               [ 2.],
               [ 3.],
               [ 4.]])
        >>> type(a)
        <class 'pycuda.gpuarray.GPUArray'>
    """
    return a.reshape(shape)


def cuda_squeeze(a):
    """ Removes dimensions of length 1 from GPUArray.

    Parameters:
        a (gpu): The GPUArray to squeeze.

    Returns:
        gpu: Squeezed GPUArray.

    Examples:
        >>> a = cuda_squeeze(cuda_give([[1], [2]]))
        array([ 1.,  2.])
        >>> type(a)
        <class 'pycuda.gpuarray.GPUArray'>
    """
    return a.squeeze()


def cuda_tile(a, shape):
    """ Horizontally and vertically tile a GPUArray.

    Notes:
        May be slow for large tiling shapes as For loops are used.

    Parameters:
        a (gpu): GPUArray to tile.
        shape (tuple): Number of vertical and horizontal tiles.

    Returns:
        gpu: Tiled GPUArray.

    Examples:
        >>> a = cuda_tile(cuda_give([[1, 2], [3, 4]]), (2, 2))
        array([[ 1.,  2.,  1.,  2.],
               [ 3.,  4.,  3.,  4.],
               [ 1.,  2.,  1.,  2.],
               [ 3.,  4.,  3.,  4.]])
        >>> type(a)
        <class 'pycuda.gpuarray.GPUArray'>

    """
    m, n = a.shape
    b = cuda_zeros((m * shape[0], n))
    for i in range(shape[0]):
        b[i * m:i * m + m, :] = a
    c = cuda_zeros((m * shape[0], n * shape[1]))
    for i in range(shape[1]):
        c[:, i * n:i * n + n] = b
    return c


def cuda_zeros(shape, bit=64):
    """ Create GPUArray of zeros directly on GPU memory.

    Parameters:
        shape (tuple): Dimensions of the GPUArray.
        bit (int): 32 or 64 for corresponding float precision.

    Returns:
        gpu: GPUArray of zeros.

    Examples:
        >>> a = cuda_zeros((3, 2), bit=64)
        array([[ 0.,  0.],
               [ 0.,  0.],
               [ 0.,  0.]])
        >>> type(a)
        <class 'pycuda.gpuarray.GPUArray'>
    """
    return pycuda.gpuarray.zeros(shape, dtype='float' + str(bit))


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    a = cuda_give([[1, 2, 3], [4, 5, 6]], bit=64, type='complex')
    b = cuda_ones((3, 2), bit=64)
    c = cuda_random((2, 2), bit=64)
    d = cuda_real(cuda_give([1 + 2.j, 2 - 4.j], type='complex'))
    e = cuda_zeros((3, 2), bit=64)
    f = cuda_eye(3)
    g = cuda_diag(cuda_give([1, 2, 3]))
    h = cuda_tile(cuda_give([[1, 2], [3, 4]]), (2, 2))
    i = cuda_squeeze(cuda_give([[1], [2]]))
    j = cuda_imag(cuda_give([1 + 2.j, 2 - 4.j], bit=64, type='complex'))
