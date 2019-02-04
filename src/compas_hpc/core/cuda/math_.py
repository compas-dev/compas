
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

try:
    from numpy import ceil
    from numpy import float32
    from numpy import int32
except:
    pass

try:
    import pycuda
    import pycuda.gpuarray as cuda_array
    import pycuda.cumath
    import pycuda.autoinit
    has_pycuda = True
    from compas_hpc import give_cuda
except:
    has_pycuda = False


__all__ = [
    'abs_cuda',
    'acos_cuda',
    'asin_cuda',
    'atan_cuda',
    'ceil_cuda',
    'cos_cuda',
    'cosh_cuda',
    'exp_cuda',
    'floor_cuda',
    'log_cuda',
    'log10_cuda',
    'maximum_cuda',
    'minimum_cuda',
    'round_cuda',
    'sin_cuda',
    'sinh_cuda',
    'sqrt_cuda',
    'sum_cuda',
    'tan_cuda',
    'tanh_cuda',
]


kernel = """

__global__ void round1d_cuda(float *a, float *b, int m)
{
    int id = blockDim.x * blockIdx.x + threadIdx.x;

    if (id < m)
    {
        b[id] = roundf(a[id]);
    }
}


__global__ void round2d_cuda(float *a, float *b, int m, int n)
{
    int idx = blockDim.x * blockIdx.x + threadIdx.x;
    int idy = blockDim.y * blockIdx.y + threadIdx.y;

    if (idx < n && idy < m)
    {
        int id  = idy * n + idx;

        b[id] = roundf(a[id]);
    }
}


__global__ void sum0_cuda(float *a, float *b, int m, int n)
{
    int bid = blockIdx.x;
    int tid = threadIdx.y;
    int id  = tid * n + bid;
    int stride = 0;

    __shared__ float sum[32000 / sizeof(float)];
    sum[tid] = a[id];
    sum[m] = 0.;

    for (stride = 1; stride < blockDim.y; stride *= 2)
    {
        __syncthreads();
        if (tid % (2 * stride) == 0)
        {
            sum[tid] += sum[tid + stride];
        }
    }

    b[bid] = sum[0];
}


__global__ void sum1_cuda(float *a, float *b, int m, int n)
{
    int bid = blockIdx.y;
    int tid = threadIdx.x;
    int id  = bid * n + tid;
    int stride = 0;

    __shared__ float sum[32000 / sizeof(float)];
    sum[tid] = a[id];
    sum[n] = 0.;

    for (stride = 1; stride < blockDim.x; stride *= 2)
    {
        __syncthreads();
        if (tid % (2 * stride) == 0)
        {
            sum[tid] += sum[tid + stride];
        }
    }

    b[bid] = sum[0];
}

"""
if has_pycuda:
    mod = pycuda.compiler.SourceModule(kernel)


def abs_cuda(a):

    """ Absolute values of GPUArray elements.

    Parameters
    ----------
    a : gpuarray
        GPUArray with the elements to take absolute values of.

    Returns
    -------
    gpuarray
        abs(GPUArray)

    Examples
    --------
    >>> a = abs_cuda(give_cuda([-0.1, -1.7]))
    [0.1, 1.7]

    >>> type(a)
    <class 'pycuda.gpuarray.GPUArray'>

    """

    return pycuda.cumath.fabs(a)


def acos_cuda(a):

    """ Trigonometric arccosine of GPUArray elements.

    Parameters
    ----------
    a : gpuarray
        GPUArray with elements to be operated on.

    Returns
    -------
    gpuarray
        acos(GPUArray)

    Examples
    --------
    >>> a = acos_cuda(give_cuda([0.5, 1]))
    [ 1.04719755,  0.]

    >>> type(a)
    <class 'pycuda.gpuarray.GPUArray'>

    """

    return pycuda.cumath.acos(a)


def asin_cuda(a):

    """ Trigonometric arcsine of GPUArray elements.

    Parameters
    ----------
    a : gpuarray
        GPUArray with elements to be operated on.

    Returns
    -------
    gpuarray
        asin(GPUArray)

    Examples
    --------
    >>> a = asin_cuda(give_cuda([0.5, 1]))
    [ 0.52359878,  1.57079633]

    >>> type(a)
    <class 'pycuda.gpuarray.GPUArray'>

    """

    return pycuda.cumath.asin(a)


def atan_cuda(a):

    """ Trigonometric arctangent of GPUArray elements.

    Parameters
    ----------
    a : gpuarray
        GPUArray with elements to be operated on.

    Returns
    -------
    gpuarray
        atan(GPUArray)

    Examples
    --------
    >>> a = atan_cuda(give_cuda([0.5, 1]))
    [ 0.46364761,  0.78539816]

    >>> type(a)
    <class 'pycuda.gpuarray.GPUArray'>

    """

    return pycuda.cumath.atan(a)


def ceil_cuda(a):

    """ Ceiling of GPUArray elements.

    Parameters
    ----------
    a : gpuarray
        GPUArray with elements to be operated on.

    Returns
    -------
    gpuarray
        ceil(GPUArray)

    Examples
    --------
    >>> a = ceil_cuda(give_cuda([0.5, 0.1, 1.9]))
    [ 1.,  1.,  2.]

    >>> type(a)
    <class 'pycuda.gpuarray.GPUArray'>

    """

    return pycuda.cumath.ceil(a)


def cos_cuda(a):

    """ Trigonometric cosine of GPUArray elements.

    Parameters
    ----------
    a : gpuarray
        GPUArray with elements to be operated on.

    Returns
    -------
    gpuarray
        cos(GPUArray)

    Examples
    --------
    >>> a = cos_cuda(give_cuda([0, pi/4]))
    [ 1.,  0.70710678]

    >>> type(a)
    <class 'pycuda.gpuarray.GPUArray'>

    """

    return pycuda.cumath.cos(a)


def cosh_cuda(a):

    """ Hyperbolic cosine of GPUArray elements.

    Parameters
    ----------
    a : gpuarray
        GPUArray with elements to be operated on.

    Returns
    -------
    gpuarray
        cosh(GPUArray)

    Examples
    --------
    >>> a = cosh_cuda(give_cuda([0, pi/4]))
    [ 1.,  1.32460909]

    >>> type(a)
    <class 'pycuda.gpuarray.GPUArray'>

    """

    return pycuda.cumath.cosh(a)


def exp_cuda(a):

    """ Exponential of GPUArray elements.

    Parameters
    ----------
    a : gpuarray
        GPUArray with elements to be operated on.

    Returns
    -------
    gpuarray
        exp(GPUArray)

    Examples
    --------
    >>> a = exp_cuda(give_cuda([0, 1]))
    [ 1.,  2.7182817]

    >>> type(a)
    <class 'pycuda.gpuarray.GPUArray'>

    """

    return pycuda.cumath.exp(a)


def floor_cuda(a):

    """ Floor of GPUArray elements.

    Parameters
    ----------
    a : gpuarray
        GPUArray with elements to be operated on.

    Returns
    -------
    gpuarray
        floor(GPUArray)

    Examples
    --------
    >>> a = floor_cuda(give_cuda([0.5, 0.1, 1.9]))
    [ 0.,  0.,  1.]

    >>> type(a)
    <class 'pycuda.gpuarray.GPUArray'>

    """

    return pycuda.cumath.floor(a)


def log_cuda(a):

    """ Natural logarithm of GPUArray elements.

    Parameters
    ----------
    a : gpuarray
        GPUArray with elements to be operated on.

    Returns
    -------
    gpuarray
        ln(GPUArray)

    Examples
    --------
    >>> a = log_cuda(give_cuda([1, 10]))
    [ 0.,  2.30258509]

    >>> type(a)
    <class 'pycuda.gpuarray.GPUArray'>

    """

    return pycuda.cumath.log(a)


def log10_cuda(a):

    """ Base10 logarithm of GPUArray elements.

    Parameters
    ----------
    a : gpuarray
        GPUArray with elements to be operated on.

    Returns
    -------
    gpuarray
        log10(GPUArray)

    Examples
    --------
    >>> a = log10_cuda(give_cuda([1, 10]))
    [ 0.,  1.]

    >>> type(a)
    <class 'pycuda.gpuarray.GPUArray'>

    """

    return pycuda.cumath.log10(a)


def maximum_cuda(a, b=None):

    """ Maximum values of two GPUArrays.

    Parameters
    ----------
    a : gpuarray
        First GPUArray.
    b : gpuarray
        Second GPUArray.

    Returns
    -------
    gpuarray
        Maximum values from both GPArrays, or single value if one GPUarray.

    Examples
    --------
    >>> a = maximum_cuda(give_cuda([1, 2, 3]), give_cuda([3, 2, 1]))
    [3, 2, 3]

    >>> type(a)
    <class 'pycuda.gpuarray.GPUArray'>

    """

    if b is not None:
        return cuda_array.maximum(a, b)
    return cuda_array.max(a)


def minimum_cuda(a, b=None):

    """ Minimum values of two GPUArrays.

    Parameters
    ----------
    a : gpuarray
        First GPUArray.
    b : gpuarray
        Second GPUArray.

    Returns
    -------
    gpuarray
        Minimum values from both GPArrays, or single value if one GPUarray.

    Examples
    --------
    >>> a = minimum_cuda(give_cuda([1, 2, 3]), give_cuda([3, 2, 1]))
    [1, 2, 1]

    >>> type(a)
    <class 'pycuda.gpuarray.GPUArray'>

    """

    if b is not None:
        return cuda_array.minimum(a, b)
    return cuda_array.min(a)


def round_cuda(a, dim=4):

    shape = a.shape

    if len(shape) == 1:

        m  = shape[0]
        nx = int(ceil(m / dim))

        func = mod.get_function('round1d_cuda')
        b = pycuda.gpuarray.empty((m), dtype=float32)
        func(a, b, int32(m), block=(dim, 1, 1), grid=(nx, 1, 1))

    elif len(shape) == 2:

        m, n = a.shape
        nx = int(ceil(n / dim))
        ny = int(ceil(m / dim))

        func = mod.get_function('round2d_cuda')
        b = pycuda.gpuarray.empty((m, n), dtype=float32)
        func(a, b, int32(m), int32(n), block=(dim, dim, 1), grid=(nx, ny, 1))

    return b


def sin_cuda(a):

    """ Trigonometric sine of GPUArray elements.

    Parameters
    ----------
    a : gpuarray
        GPUArray with elements to be operated on.

    Returns
    -------
    gpuarray
        sin(GPUArray)

    Examples
    --------
    >>> a = sin_cuda(give_cuda([0, pi/4]))
    [ 0.,  0.70710678]

    >>> type(a)
    <class 'pycuda.gpuarray.GPUArray'>

    """

    return pycuda.cumath.sin(a)


def sinh_cuda(a):

    """ Hyperbolic sine of GPUArray elements.

    Parameters
    ----------
    a : gpuarray
        GPUArray with elements to be operated on.

    Returns
    -------
    gpuarray
        sinh(GPUArray)

    Examples
    --------
    >>> a = sinh_cuda(give_cuda([0, pi/4]))
    [ 0.,  0.86867096]

    >>> type(a)
    <class 'pycuda.gpuarray.GPUArray'>

    """

    return pycuda.cumath.sinh(a)


def sqrt_cuda(a):

    """ Square-root of GPUArray elements.

    Parameters
    ----------
    a : gpuarray
        GPUArray with elements to be operated on.

    Returns
    -------
    gpuarray
        sqrt(GPUArray)

    Examples
    --------
    >>> a = sqrt_cuda(give_cuda([4, 9]))
    [ 2.,  3.]

    >>> type(a)
    <class 'pycuda.gpuarray.GPUArray'>

    """

    return pycuda.cumath.sqrt(a)


def sum_cuda(a, axis=None):

    """ Sum of GPUArray elements in a given axis direction or all elements.

    Parameters
    ----------
    a : gpuarray
        GPUArray with elements to be operated on.
    axis : int
        Axis direction to sum through, all if None.

    Returns
    -------
    gpuarray
        GPUArray sum.

    Notes
    -----
    - This is temporary and not an efficient implementation.

    """

    if axis is not None:

        m, n = a.shape

        if axis == 0:

            func = mod.get_function('sum0_cuda')
            b = pycuda.gpuarray.empty((1, n), dtype=float32)
            func(a, b, int32(m), int32(n), block=(1, m, 1), grid=(n, 1, 1))

        elif axis == 1:

            func = mod.get_function('sum1_cuda')
            b = pycuda.gpuarray.empty((m, 1), dtype=float32)
            func(a, b, int32(m), int32(n), block=(n, 1, 1), grid=(1, m, 1))

        return b

    else:
        return cuda_array.sum(a)


def tan_cuda(a):

    """ Trigonometric tangent of GPUArray elements.

    Parameters
    ----------
    a : gpuarray
        GPUArray with elements to be operated on.

    Returns
    -------
    gpuarray
        tan(GPUArray)

    Examples
    --------
    >>> a = tan_cuda(give_cuda([0, pi/4]))
    [ 0.,  1]

    >>> type(a)
    <class 'pycuda.gpuarray.GPUArray'>

    """

    return pycuda.cumath.tan(a)


def tanh_cuda(a):

    """ Hyperbolic tangent of GPUArray elements.

    Parameters
    ----------
    a : gpuarray
        GPUArray with elements to be operated on.

    Returns
    -------
    gpuarray
        tanh(GPUArray)

    Examples
    --------
    >>> a = tanh_cuda(give_cuda([0, pi/4]))
    [ 0.,  0.6557942]

    >>> type(a)
    <class 'pycuda.gpuarray.GPUArray'>

    """

    return pycuda.cumath.tanh(a)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    from compas_hpc import give_cuda

    from numpy import pi

    # a = abs_cuda(give_cuda([-0.1, -1.7]))
    # a = maximum_cuda(give_cuda([1, 2, 3]), give_cuda([3, 2, 1]))
    # a = maximum_cuda(give_cuda([1, 2, 3]))
    # a = minimum_cuda(give_cuda([1, 2, 3]), give_cuda([3, 2, 1]))
    # a = acos_cuda(give_cuda([0.5, 1]))
    # a = asin_cuda(give_cuda([0.5, 1]))
    # a = atan_cuda(give_cuda([0.5, 1]))
    # a = ceil_cuda(give_cuda([0.5, 0.1, 1.9]))
    # a = cos_cuda(give_cuda([0, pi/4]))
    # a = cosh_cuda(give_cuda([0, pi/4]))
    # a = exp_cuda(give_cuda([0, 1]))
    # a = floor_cuda(give_cuda([0.5, 0.1, 1.9]))
    # a = log_cuda(give_cuda([1, 10]))
    # a = log10_cuda(give_cuda([1, 10]))
    # a = sin_cuda(give_cuda([0, pi/4]))
    # a = sinh_cuda(give_cuda([0, pi/4]))
    # a = sqrt_cuda(give_cuda([4, 9]))
    # a = tan_cuda(give_cuda([0, pi/4]))
    # a = tanh_cuda(give_cuda([0, pi/4]))
    # a = round_cuda(give_cuda([1.4, 1.5, 1.6]))
    # a = round_cuda(give_cuda([[1.4, 1.5, 1.6], [2.4, 2.5, 2.6]]))
    a = sum_cuda(give_cuda([[1, 2, 3], [4, 5, 6], [7, 8, 9]]), axis=1)

    print(a)
    print(type(a))
