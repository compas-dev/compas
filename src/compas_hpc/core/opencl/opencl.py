
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

try:
    from numpy import array
    from numpy import float32
    from numpy import complex64
    from numpy import uint32
except:
    pass

try:
    import pyopencl as cl
    import pyopencl.array as cl_array
    import pyopencl.clrandom
except:
    pass


__all__ = [
    'rand_cl',
    'give_cl',
    'get_cl',
    'ones_cl',
    'zeros_cl',
    'tile_cl',
    'hstack_cl',
    'vstack_cl',
]


def rand_cl(queue, shape):

    """ Create random values in the range [0, 1] in a GPUArray.

    Parameters
    ----------
    queue
        PyOpenCL queue.
    shape : tuple
        Size of the random array.

    Returns
    -------
    gpuarray
        Random floats from 0 to 1 in GPUArray.

    Examples
    --------
    >>> a = rand_cl((2, 2))
    [[ 0.80916596,  0.82687163],
     [ 0.03921388,  0.44197764]]

    >>> type(a)
    <class 'pyopencl.array.Array'>

    """

    return pyopencl.clrandom.rand(queue, shape, dtype=float32)


def give_cl(queue, a, type='real'):

    """ Give a list or an array to GPU memory.

    Parameters
    ----------
    queue
        PyOpenCL queue.
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
    >>> a = give_cl([[1., 2., 3.], [4., 5., 6.]])
    [[ 1.,  2.,  3.],
     [ 4.,  5.,  6.]]

    >>> type(a)
    <class 'pyopencl.array.Array'>

    >>> a.shape
    (2, 3)

    >>> a.dtype
    'float32'

    >>> a.reshape((1, 6))
    [[ 1.,  2.,  3.,  4.,  5.,  6.]]

    """

    if type == 'real':
        return cl_array.to_device(queue, array(a).astype(float32))

    elif type == 'complex':
        return cl_array.to_device(queue, array(a).astype(complex64))


def get_cl(a):

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
    >>> a = give_cl([1, 2, 3])
    >>> b = get_cl(a)
    [ 1.,  2.,  3.]

    >>> type(b)
    <class 'numpy.ndarray'>

    """

    return a.get()


def ones_cl(queue, shape):

    """ Create GPUArray of ones directly on GPU memory.

    Parameters
    ----------
    queue
        PyOpenCL queue.
    shape : tuple
        Dimensions of the GPUArray.

    Returns
    -------
    gpuarray
        GPUArray of ones.

    Examples
    --------
    >>> a = ones_cl((3, 2))
    [[ 1.,  1.],
     [ 1.,  1.],
     [ 1.,  1.]]

    >>> type(a)
    <class 'pyopencl.array.Array'>

    """

    a = cl_array.zeros(queue, shape, dtype=float32)
    a.fill(1.0)

    return a


def zeros_cl(queue, shape):

    """ Create GPUArray of zeros directly on GPU memory.

    Parameters
    ----------
    queue
        PyOpenCL queue.
    shape : tuple
        Dimensions of the GPUArray.

    Returns
    -------
    gpuarray
        GPUArray of zeros.

    Examples
    --------
    >>> a = zeros_cl((3, 2))
    [[ 0.,  0.],
     [ 0.,  0.],
     [ 0.,  0.]]

    >>> type(a)
    <class 'pyopencl.array.Array'>

    """

    return cl_array.zeros(queue, shape, dtype=float32)


def tile_cl(queue, a, shape, dim=4):

    """ Horizontally and vertically tile a GPUArray.

    Parameters
    ----------
    queue
        PyOpenCL queue.
    a : gpuarray
        GPUArray to tile.
    shape : tuple
        Number of vertical and horizontal tiles.

    Returns
    -------
    gpuarray
        Tiled GPUArray.

    """

    m, n = a.shape
    repy, repx = shape
    b = cl_array.empty(queue, (m * repy, n * repx), dtype=float32)

    kernel = cl.Program(queue.context, """

    __kernel void tile_cl(__global float *a, __global float *b, unsigned m, unsigned n, unsigned repx, unsigned repy)
    {
        int idx = get_global_id(0);
        int idy = get_global_id(1);
        int id  = idy * (n * repx) + idx;

        b[id] = a[(idy % m) * n + (idx % n)];
    }

    """).build()

    kernel.tile_cl(queue, (n * repx, m * repy), None, a.data, b.data, uint32(m), uint32(n), uint32(repx), uint32(repy))

    return b


def hstack_cl(queue, a, b, dim=4):

    """ Stack two GPUArrays horizontally.

    Parameters
    ----------
    queue
        PyOpenCL queue.
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
    o = b.shape[1]
    c = cl_array.empty(queue, (m, n + o), dtype=float32)

    kernel = cl.Program(queue.context, """

    __kernel void hstack_cl(__global float *a, __global float *b, __global float *c, unsigned n, unsigned o)
    {
        int idx = get_global_id(0);
        int idy = get_global_id(1);
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

    """).build()

    kernel.hstack_cl(queue, (n + o, m), None, a.data, b.data, c.data, uint32(n), uint32(o))

    return c


def vstack_cl(queue, a, b, dim=4):

    """ Stack two GPUArrays vertically.

    Parameters
    ----------
    queue
        PyOpenCL queue.
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
    o = b.shape[0]
    c = cl_array.empty(queue, (m + o, n), dtype=float32)

    kernel = cl.Program(queue.context, """

    __kernel void vstack_cl(__global float *a, __global float *b, __global float *c, unsigned m, unsigned n, unsigned o)
    {
        int idx = get_global_id(0);
        int idy = get_global_id(1);
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

    """).build()

    kernel.vstack_cl(queue, (n, m + o), None, a.data, b.data, c.data, uint32(m), uint32(n), uint32(o))

    return c


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    ctx   = cl.create_some_context()
    queue = cl.CommandQueue(ctx)  # need to find the device association

    a = give_cl(queue, [[1., 2., 3.], [4., 5., 6.]])
    # a = give_cl(queue, [1.+1j, 2.+2j, 3.+3j], type='complex')
    a = get_cl(a)
    a = ones_cl(queue, (2, 2))
    b = zeros_cl(queue, (2, 2))
    c = rand_cl(queue, (1, 3))
    d = rand_cl(queue, (1, 2))
    # e = vstack_cl(queue, c, d)
    e = tile_cl(queue, d, (2, 2))

    print(d)
    print(e)
