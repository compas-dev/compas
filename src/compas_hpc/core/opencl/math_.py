
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

try:
    import pyopencl as cl
    import pyopencl.clmath
    import pyopencl.array as cl_array
except:
    pass


__author__    = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__ = 'Copyright 2018, BLOCK Research Group - ETH Zurich'
__license__   = 'MIT License'
__email__     = 'liew@arch.ethz.ch'


__all__ = [
    'abs_cl',
    # 'argmax_cl',
    # 'argmin_cl',
    'acos_cl',
    'acosh_cl',
    'asin_cl',
    'asinh_cl',
    'atan_cl',
    'atan2_cl',
    'atanh_cl',
    'ceil_cl',
    'cos_cl',
    'cosh_cl',
    'exp_cl',
    'floor_cl',
    'log_cl',
    'log10_cl',
    # 'max_cl',
    # 'min_cl',
    # 'mean_cl',
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

    """

    return pyopencl.clmath.fabs(a)


def argmax_cl():
    raise NotImplementedError


def argmin_cl():
    raise NotImplementedError


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

    """

    return pyopencl.clmath.acos(a)


def acosh_cl(a):

    """ Hyperbolic arccosh of GPUArray elements.

    Parameters
    ----------
    a : gpuarray
        GPUArray with elements to be operated on.

    Returns
    -------
    gpuarray
        acosh(GPUArray)

    """

    return pyopencl.clmath.acosh(a)


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

    """

    return pyopencl.clmath.asin(a)


def asinh_cl(a):

    """ Hyperbolic arcsinh of GPUArray elements.

    Parameters
    ----------
    a : gpuarray
        GPUArray with elements to be operated on.

    Returns
    -------
    gpuarray
        asinh(GPUArray)

    """

    return pyopencl.clmath.asinh(a)


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

    """

    return pyopencl.clmath.atan(a)


def atan2_cl(y, x):

    """ Trigonometric arctangent(2) of GPUArray elements.

    Parameters
    ----------
    y : gpuarray
        GPUArray with elements y.
    x : gpuarray
        GPUArray with elements x.

    Returns
    -------
    gpuarray
        atan2(GPUArray)

    """

    return pyopencl.clmath.atan2(y, x)


def atanh_cl(a):

    """ Hyperbolic arctanh of GPUArray elements.

    Parameters
    ----------
    a : gpuarray
        GPUArray with elements to be operated on.

    Returns
    -------
    gpuarray
        atanh(GPUArray)

    """

    return pyopencl.clmath.atanh(a)


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
        log(GPUArray)

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

    """

    return pyopencl.clmath.log10(a)


def max_cl():
    raise NotImplementedError


def min_cl():
    raise NotImplementedError


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
        Maximum values from both GPArrays, or single value if only one GPUarray.

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
        Minimum values from both GPArrays, or single value if only one GPUarray.

    """

    if b is not None:
        return cl_array.minimum(a, b)
    return cl_array.min(a)


def mean_cl():
    raise NotImplementedError


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

    """

    return pyopencl.clmath.sqrt(a)


def sum_cl(a, axis=None):

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

    """

    if axis is not None:
        raise NotImplementedError
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

    """

    return pyopencl.clmath.tanh(a)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    from compas.hpc import give_cl
    from compas.hpc import get_cl

    from numpy import pi

    ctx = cl.create_some_context()
    queue = cl.CommandQueue(ctx)

    e_ = give_cl(queue, [1, 2, 3])
    f_ = give_cl(queue, [3, 2, 1])

    a_ = give_cl(queue, [-1, 3, -2])
    b_ = maximum_cl(e_, f_)
    c_ = minimum_cl(e_, f_)

    print(get_cl(abs_cl(a_)))
    print(get_cl(b_))
    print(get_cl(c_))
    print(get_cl(maximum_cl(e_)))
    print(get_cl(minimum_cl(e_)))
    print(get_cl(sum_cl(e_)))

    print(get_cl(acos_cl(give_cl(queue, [0.5, 1.0]))))
    print(get_cl(acosh_cl(give_cl(queue, [2.0, 1.0]))))
    print(get_cl(asin_cl(give_cl(queue, [0.5, 1.0]))))
    print(get_cl(asinh_cl(give_cl(queue, [0.5, 1.0]))))

    print(get_cl(atan_cl(give_cl(queue, [0.5, 1.0]))))
    print(get_cl(atan2_cl(f_, e_)))
    print(get_cl(atanh_cl(give_cl(queue, [0.5, 0.7]))))

    print(get_cl(cos_cl(give_cl(queue, [0, pi / 4]))))
    print(get_cl(cosh_cl(give_cl(queue, [0, pi / 4]))))

    print(get_cl(exp_cl(give_cl(queue, [0, 1]))))

    print(get_cl(ceil_cl(give_cl(queue, [0.5, 1.2, 1.9]))))
    print(get_cl(floor_cl(give_cl(queue, [0.5, 1.2, 1.9]))))

    print(get_cl(log_cl(give_cl(queue, [1, 10]))))
    print(get_cl(log10_cl(give_cl(queue, [1, 10]))))

    print(get_cl(round_cl(give_cl(queue, [0.5, 1.2, 1.9]))))

    print(get_cl(sin_cl(give_cl(queue, [0, pi / 4]))))
    print(get_cl(sinh_cl(give_cl(queue, [0, pi / 4]))))

    print(get_cl(sqrt_cl(give_cl(queue, [4, 9]))))

    print(get_cl(tan_cl(give_cl(queue, [0, pi / 4]))))
    print(get_cl(tanh_cl(give_cl(queue, [0, pi / 4]))))
