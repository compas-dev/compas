
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

try:
    from numpy import array
    from numpy import ceil
    from numpy import complex64
    from numpy import float32
    from numpy import int32
except:
    pass

try:
    import pycuda
    import pycuda.gpuarray as cuda_array
    import pycuda.curandom
    import pycuda.autoinit
    has_pycuda = True
except:
    has_pycuda = False


__all__ = [
    'device_cuda',
    'rand_cuda',
    'give_cuda',
    'get_cuda',
    'ones_cuda',
    'zeros_cuda',
    'tile_cuda',
    'hstack_cuda',
    'vstack_cuda',
]


kernel = """

__global__ void hstack_cuda(int m, int n, int o, float *a, float *b, float *c)
{
    int idx = blockDim.x * blockIdx.x + threadIdx.x;
    int idy = blockDim.y * blockIdx.y + threadIdx.y;

    if (idx < n + o && idy < m)
    {
        int id  = idy * (n + o) + idx;

        if (idx < n)
        {
            c[id] = a[idy * n + idx];
        }
        else
        {
            c[id] = b[idy * o + (idx - n)];
        }
    }
}


__global__ void vstack_cuda(int m, int n, int o, float *a, float *b, float *c)
{
    int idx = blockDim.x * blockIdx.x + threadIdx.x;
    int idy = blockDim.y * blockIdx.y + threadIdx.y;

    if (idx < n && idy < m + o)
    {
        int id  = idy * n + idx;

        if (idy < m)
        {
            c[id] = a[idy * n + idx];
        }
        else
        {
            c[id] = b[(idy - m) * n + idx];
        }
    }
}


__global__ void tile_cuda(int m, int n, int repx, int repy, float *a, float *b)
{
    int idx = blockDim.x * blockIdx.x + threadIdx.x;
    int idy = blockDim.y * blockIdx.y + threadIdx.y;

    if (idx < (repx * n) && idy < (repy * m))
    {
        int id  = idy * (n * repx) + idx;

        b[id] = a[(idy % m) * n + (idx % n)];
    }
}

"""
if has_pycuda:
    mod = pycuda.compiler.SourceModule(kernel)


def device_cuda():

    """ Display CUDA GPU device details.

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

    attrs = [(key, value) for key, value in dev.get_attributes().items()]
    attrs.sort()

    for attr, value in attrs:
        print('%s: %s' % (attr, value))


def rand_cuda(shape):

    """ Create random values in the range [0, 1] in a GPUArray.

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
    [[ 0.80916596,  0.82687163],
     [ 0.03921388,  0.44197764]]

    >>> type(a)
    <class 'pycuda.gpuarray.GPUArray'>

    """

    return pycuda.curandom.rand(shape, dtype=float32)


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
        GPUArray version of the input array.

    Examples
    --------
    >>> a = give_cuda([[1., 2., 3.], [4., 5., 6.]])
    [[ 1.,  2.,  3.],
     [ 4.,  5.,  6.]]

    >>> type(a)
    <class 'pycuda.gpuarray.GPUArray'>

    >>> a.shape
    (2, 3)

    >>> a.dtype
    'float32'

    >>> a.reshape((1, 6))
    [[ 1.,  2.,  3.,  4.,  5.,  6.]]

    """

    if type == 'real':
        return cuda_array.to_gpu(array(a).astype(float32))

    elif type == 'complex':
        return cuda_array.to_gpu(array(a).astype(complex64))


def get_cuda(a):

    """ Return GPUArray from GPU memory as NumPy array.

    Parameters
    ----------
    a : gpuarray
        Data on the GPU memory to retrieve.

    Returns
    -------
    array
        The GPUArray returned to RAM as a NumPy array.

    Examples
    --------
    >>> a = give_cuda([1, 2, 3])
    >>> b = get_cuda(a)
    [ 1.,  2.,  3.]

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
    [[ 1.,  1.],
     [ 1.,  1.],
     [ 1.,  1.]]

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
    [[ 0.,  0.],
     [ 0.,  0.],
     [ 0.,  0.]]

    >>> type(a)
    <class 'pycuda.gpuarray.GPUArray'>

    """

    return cuda_array.zeros(shape, dtype=float32)


def tile_cuda(a, shape, dim=4):

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

    Examples
    --------
    >>> a = tile_cuda(give_cuda([[1, 2], [3, 4]]), (2, 2))
    [[ 1.,  2.,  1.,  2.],
     [ 3.,  4.,  3.,  4.],
     [ 1.,  2.,  1.,  2.],
     [ 3.,  4.,  3.,  4.]]

     >>> type(a)
     <class 'pycuda.gpuarray.GPUArray'>

    """

    m, n = a.shape
    repy, repx = shape
    nx = int(ceil(n * repx / dim))
    ny = int(ceil(m * repy / dim))

    func = mod.get_function('tile_cuda')
    b = pycuda.gpuarray.empty((m * repy, n * repx), dtype=float32)
    func(int32(m), int32(n), int32(repx), int32(repy), a, b, block=(dim, dim, 1), grid=(nx, ny, 1))

    return b


def hstack_cuda(a, b, dim=4):

    """ Stack two GPUArrays horizontally.

    Parameters
    ----------
    a : gpuarray
        First GPUArray.
    b : gpuarray
        Second GPUArray.

    Returns
    -------
    gpuarray
        Horizontally stacked GPUArrays.

    """

    m, n = a.shape
    o  = b.shape[1]
    nx = int(ceil((n + o) / dim))
    ny = int(ceil(m / dim))

    func = mod.get_function('hstack_cuda')
    c = pycuda.gpuarray.empty((m, n + o), dtype=float32)
    func(int32(m), int32(n), int32(o), a, b, c, block=(dim, dim, 1), grid=(nx, ny, 1))

    return c


def vstack_cuda(a, b, dim=4):

    """ Stack two GPUArrays vertically.

    Parameters
    ----------
    a : gpuarray
        First GPUArray.
    b : gpuarray
        Second GPUArray.

    Returns
    -------
    gpuarray
        Vertically stacked GPUArrays.

    """

    m, n = a.shape
    o  = b.shape[0]
    nx = int(ceil(n / dim))
    ny = int(ceil((m + o) / dim))

    func = mod.get_function('vstack_cuda')
    c = pycuda.gpuarray.empty((m + o, n), dtype=float32)
    func(int32(m), int32(n), int32(o), a, b, c, block=(dim, dim, 1), grid=(nx, ny, 1))

    return c


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    n = 500
    device_cuda()
    # a = give_cuda([[1., 2., 3.], [4., 5., 6.]])
    # a = give_cuda([1.+1j, 2.+2j, 3.+3j], type='complex')
    # a = get_cuda(a)
    # a = ones_cuda((3, 3))
    # a = zeros_cuda((3, 3))
    # a = give_cuda([[1, 2, 3], [4, 5, 6]])
    # a = rand_cuda((n, n))
    # b = rand_cuda((n, n))
    # c = hstack_cuda(a, b, dim=4)

    # print(a)
    # print(b)
    # print(c)
    # print(type(a))
    # print(a.shape)
    # print(a.dtype)
