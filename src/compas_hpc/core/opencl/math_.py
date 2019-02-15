
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

try:
    from numpy import float32
    from numpy import uint32
except:
    pass

try:
    import pyopencl as cl
    import pyopencl.clmath
    import pyopencl.array as cl_array
except:
    pass


__all__ = [
    'abs_cl',
    'acos_cl',
    'asin_cl',
    'atan_cl',
    'ceil_cl',
    'cos_cl',
    'cosh_cl',
    'exp_cl',
    'floor_cl',
    'log_cl',
    'log10_cl',
    'maximum_cl',
    'minimum_cl',
    'round_cl',
    'sin_cl',
    'sinh_cl',
    'sqrt_cl',
    'sum_cl',
    'tan_cl',
    'tanh_cl',
]


def abs_cl(a):

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
    >>> a = abs_cl(give_cl([-0.1, -1.7]))
    [0.1, 1.7]

    >>> type(a)
    <class 'pyopencl.array.Array'>

    """

    return pyopencl.clmath.fabs(a)


def acos_cl(a):

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
    >>> a = acos_cl(give_cl(queue, [0.5, 1]))
    [ 1.04719755,  0.]

    >>> type(a)
    <class 'pyopencl.array.Array'>

    """

    return pyopencl.clmath.acos(a)


def asin_cl(a):

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
    >>> a = asin_cl(give_cl(queue, [0.5, 1]))
    [ 0.52359878,  1.57079633]

    >>> type(a)
    <class 'pyopencl.array.Array'>

    """

    return pyopencl.clmath.asin(a)


def atan_cl(a):

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
    >>> a = atan_cl(give_cl(queue, [0.5, 1]))
    [ 0.46364761,  0.78539816]

    >>> type(a)
    <class 'pyopencl.array.Array'>

    """

    return pyopencl.clmath.atan(a)


def ceil_cl(a):

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
    >>> a = ceil_cl(give_cl(queue, [0.5, 0.1, 1.9]))
    [ 1.,  1.,  2.]

    >>> type(a)
    <class 'pyopencl.array.Array'>

    """

    return pyopencl.clmath.ceil(a)


def cos_cl(a):

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
    >>> a = cos_cl(give_cl(queue, [0, pi/4]))
    [ 1.,  0.70710678]

    >>> type(a)
    <class 'pyopencl.array.Array'>

    """

    return pyopencl.clmath.cos(a)


def cosh_cl(a):

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
    >>> a = cosh_cl(give_cl(queue, [0, pi/4]))
    [ 1.,  1.32460909]

    >>> type(a)
    <class 'pyopencl.array.Array'>

    """

    return pyopencl.clmath.cosh(a)


def exp_cl(a):

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
    >>> a = exp_cl(give_cl(queue, [0, 1]))
    [ 1.,  2.7182817]

    >>> type(a)
    <class 'pyopencl.array.Array'>

    """

    return pyopencl.clmath.exp(a)


def floor_cl(a):

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
    >>> a = floor_cl(give_cl(queue, [0.5, 0.1, 1.9]))
    [ 0.,  0.,  1.]

    >>> type(a)
    <class 'pyopencl.array.Array'>

    """

    return pyopencl.clmath.floor(a)


def log_cl(a):

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
    >>> a = log_cl(give_cl(queue, [1, 10]))
    [ 0.,  2.30258509]

    >>> type(a)
    <class 'pyopencl.array.Array'>

    """

    return pyopencl.clmath.log(a)


def log10_cl(a):

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
    >>> a = log10_cl(give_cl(queue, [1, 10]))
    [ 0.,  1.]

    >>> type(a)
    <class 'pycuda.gpuarray.GPUArray'>

    """
    return pyopencl.clmath.log10(a)


def maximum_cl(a, b=None):

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
    >>> a = maximum_cl(give_cl(queue, [1, 2, 3]), give_cl(queue, [3, 2, 1]))
    [3, 2, 3]

    >>> type(a)
    <class 'pyopencl.array.Array'>

    """

    if b is not None:
        return cl_array.maximum(a, b)
    return cl_array.max(a)


def minimum_cl(a, b=None):

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
    >>> a = minimum_cl(give_cl(queue, [1, 2, 3]), give_cl(queue, [3, 2, 1]))
    [1, 2, 1]

    >>> type(a)
    <class 'pyopencl.array.Array'>

    """

    if b is not None:
        return cl_array.minimum(a, b)
    return cl_array.min(a)


def round_cl(a):

    """ Rounding of GPUArray elements.

    Parameters
    ----------
    a : gpuarray
        GPUArray with elements to be operated on.

    Returns
    -------
    gpuarray
        round(GPUArray)

    Examples
    --------
    >>> a = round_cl(give_cl(queue, [1.4, 1.5, 1.6]))
    [1., 2., 2.]

    >>> type(a)
    <class 'pyopencl.array.Array'>

    """

    return pyopencl.clmath.round(a)


def sin_cl(a):

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
    >>> a = sin_cl(give_cl(queue, [0, pi/4]))
    [ 0.,  0.70710678]

    >>> type(a)
    <class 'pyopencl.array.Array'>

    """

    return pyopencl.clmath.sin(a)


def sinh_cl(a):

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
    >>> a = sinh_cl(give_cl(queue, [0, pi/4]))
    [ 0.,  0.86867096]

    >>> type(a)
    <class 'pyopencl.array.Array'>

    """

    return pyopencl.clmath.sinh(a)


def sqrt_cl(a):

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
    >>> a = sqrt_cl(give_cl(queue, [4, 9]))
    [ 2.,  3.]

    >>> type(a)
    <class 'pyopencl.array.Array'>

    """

    return pyopencl.clmath.sqrt(a)


def sum_cl(queue, a, axis=None):

    """ Sum of GPUArray elements in a given axis direction or all elements.

    Parameters
    ----------
    queue
        PyOpenCL queue.
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

        kernel = cl.Program(queue.context, """

        __kernel void sum0_cl(__global float *a, __global float *b, unsigned m, unsigned n)
        {
            int bid = get_group_id(0);
            int tid = get_local_id(1);
            int id  = get_global_id(1) * n + get_global_id(0);
            int stride = 0;

            __local float sum[32000 / sizeof(float)];
            sum[tid] = a[id];
            sum[m] = 0.;

            for (stride = 1; stride < m; stride *= 2)
            {
                barrier(CLK_LOCAL_MEM_FENCE);
                if (tid % (2 * stride) == 0)
                {
                    sum[tid] += sum[tid + stride];
                }
            }

            b[bid] = sum[0];
        }

        __kernel void sum1_cl(__global float *a, __global float *b, unsigned m, unsigned n)
        {
            int bid = get_group_id(1);
            int tid = get_local_id(0);
            int id  = get_global_id(1) * n + get_global_id(0);
            int stride = 0;

            __local float sum[32000 / sizeof(float)];
            sum[tid] = a[id];
            sum[n] = 0.;

            for (stride = 1; stride < n; stride *= 2)
            {
                barrier(CLK_LOCAL_MEM_FENCE);
                if (tid % (2 * stride) == 0)
                {
                    sum[tid] += sum[tid + stride];
                }
            }

            b[bid] = sum[0];
        }

        """).build()

        if axis == 0:

            b = cl_array.empty(queue, (1, n), dtype=float32)
            kernel.sum0_cl(queue, (n, m), (1, m), a.data, b.data, uint32(m), uint32(n))

        elif axis == 1:

            b = cl_array.empty(queue, (m, 1), dtype=float32)
            kernel.sum1_cl(queue, (n, m), (n, 1), a.data, b.data, uint32(m), uint32(n))

        return b

    else:
        return cl_array.sum(a)


def tan_cl(a):

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
    >>> a = tan_cl(give_cl(queue, [0, pi/4]))
    [ 0.,  1]

    >>> type(a)
    <class 'pyopencl.array.Array'>

    """

    return pyopencl.clmath.tan(a)


def tanh_cl(a):

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
    >>> a = tanh_cl(give_cl(queue, [0, pi/4]))
    [ 0.,  0.6557942]

    >>> type(a)
    <class 'pyopencl.array.Array'>

    """

    return pyopencl.clmath.tanh(a)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    from compas_hpc import give_cl
    from compas_hpc import get_cl

    from numpy import pi

    ctx   = cl.create_some_context()
    queue = cl.CommandQueue(ctx)

    # a = abs_cl(give_cl(queue, [-0.1, -1.7]))
    # a = acos_cl(give_cl(queue, [0.5, 1]))
    # a = asin_cl(give_cl(queue, [0.5, 1]))
    # a = atan_cl(give_cl(queue, [0.5, 1]))
    # a = cos_cl(give_cl(queue, [0, pi/4]))
    # a = cosh_cl(give_cl(queue, [0, pi/4]))
    # a = maximum_cl(give_cl(queue, [1, 2, 3]), give_cl(queue, [3, 2, 1]))
    # a = maximum_cl(give_cl(queue, [1, 2, 3]))
    # a = minimum_cl(give_cl(queue, [1, 2, 3]), give_cl(queue, [3, 2, 1]))
    # a = minimum_cl(give_cl(queue, [1, 2, 3]))
    # a = sin_cl(give_cl(queue, [0, pi/4]))
    # a = sinh_cl(give_cl(queue, [0, pi/4]))
    # a = sqrt_cl(give_cl(queue, [4, 9]))
    # a = tan_cl(give_cl(queue, [0, pi/4]))
    # a = tanh_cl(give_cl(queue, [0, pi/4]))
    # a = exp_cl(give_cl(queue, [0, 1]))
    # a = floor_cl(give_cl(queue, [0.5, 0.1, 1.9]))
    # a = ceil_cl(give_cl(queue, [0.5, 0.1, 1.9]))
    # a = log_cl(give_cl(queue, [1, 10]))
    # a = log10_cl(give_cl(queue, [1, 10]))
    # a = round_cl(give_cl(queue, [1.4, 1.5, 1.6]))
    a = sum_cl(queue, give_cl(queue, [[1, 2, 3], [4, 5, 6], [7, 8, 9]]), axis=1)

    print(a)
    print(type(a))
