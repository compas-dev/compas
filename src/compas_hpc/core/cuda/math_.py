
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

try:
    import pycuda
    import pycuda.autoinit
    import pycuda.cumath
    import pycuda.gpuarray as cuda_array
except:
    pass


__author__    = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__ = 'Copyright 2018, Block Research Group - ETH Zurich'
__license__   = 'MIT License'
__email__     = 'liew@arch.ethz.ch'


__all__ = [
    'abs_cuda',
    # 'argmax_cuda',
    # 'argmin_cuda',
    'acos_cuda',
    # 'acosh_cuda',
    'asin_cuda',
    # 'asinh_cuda',
    'atan_cuda',
    # 'atan2_cuda',
    # 'atanh_cuda',
    'ceil_cuda',
    'cos_cuda',
    'cosh_cuda',
    'exp_cuda',
    'floor_cuda',
    'log_cuda',
    'log10_cuda',
    # 'max_cuda',
    # 'min_cuda',
    # 'mean_cuda',
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
    array([0.1, 1.7])

    >>> type(a)
    <class 'pycuda.gpuarray.GPUArray'>

    """

    return pycuda.cumath.fabs(a)


# def argmax_cuda(a, axis):

#     """ Location of maximum GPUArray elements.

#     Parameters
#     ----------
#     a : gpuarray
#         GPUArray with the elements to find maximum values.
#     axis : int
#         The dimension to evaluate through.

#     Returns
#     -------
#     gpuarray
#         Location of maximum values.

#     Examples
#     --------
#     >>> a = argmax_cuda(give_cuda([[1, 2, 3], [6, 5, 4]]), axis=1)
#     array([[2],
#            [0]], dtype=uint32)

#     >>> type(a)
#     <class 'pycuda.gpuarray.GPUArray'>

#     """

#     return skcuda.misc.argmax(a, axis, keepdims=True)


# def argmin_cuda(a, axis):

#     """ Location of minimum GPUArray elements.

#     Parameters
#     ----------
#     a : gpuarray
#         GPUArray with the elements to find minimum values.
#     axis : int
#         The dimension to evaluate through.

#     Returns
#     -------
#     gpuarray
#         Location of minimum values.

#     Examples
#     --------
#     >>> a = argmin_cuda(give_cuda([[1, 2, 3], [6, 5, 4]]), axis=1)
#     array([[0],
#            [2]], dtype=uint32)

#     >>> type(a)
#     <class 'pycuda.gpuarray.GPUArray'>

#     """

#     return skcuda.misc.argmin(a, axis, keepdims=True)


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
    array([ 1.04719755,  0.])

    >>> type(a)
    <class 'pycuda.gpuarray.GPUArray'>

    """

    return pycuda.cumath.acos(a)


def acosh_cuda():
    raise NotImplementedError


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
    array([ 0.52359878,  1.57079633])

    >>> type(a)
    <class 'pycuda.gpuarray.GPUArray'>

    """

    return pycuda.cumath.asin(a)


def asinh_cuda():
    raise NotImplementedError


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
    array([ 0.46364761,  0.78539816])

    >>> type(a)
    <class 'pycuda.gpuarray.GPUArray'>

    """

    return pycuda.cumath.atan(a)


def atan2_cuda():
    raise NotImplementedError


def atanh_cuda():
    raise NotImplementedError


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
    array([ 1.,  1.,  2.])

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
    array([ 1.,  0.70710678])

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
    array([ 1.,  1.32460909])

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
    array([ 1.,  2.71828183])

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
    array([ 0.,  0.,  1.])

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
        log(GPUArray)

    Examples
    --------
    >>> a = log_cuda(give_cuda([1, 10]))
    array([ 0.,  2.30258509])

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
    array([ 0.,  1.])

    >>> type(a)
    <class 'pycuda.gpuarray.GPUArray'>

    """

    return pycuda.cumath.log10(a)


# def max_cuda(a, axis):

#     """ Maximum values of GPUArray elements.

#     Parameters
#     ----------
#     a : gpuarray
#         GPUArray with the elements to find maximum values.
#     axis : int
#         The dimension to evaluate through.

#     Returns
#     -------
#     gpuarray
#         Maximum values.

#     Examples
#     --------
#     >>> a = max_cuda(give_cuda([[1, 2, 3], [6, 5, 4]]), axis=1)
#     array([[3],
#            [6]])

#     >>> type(a)
#     <class 'pycuda.gpuarray.GPUArray'>

#     """

#     return skcuda.misc.max(a, axis, keepdims=True)


# def min_cuda(a, axis):

#     """ Minimum values of GPUArray elements.

#     Parameters
#     ----------
#     a : gpuarray
#         GPUArray with the elements to find minimum values.
#     axis : int
#         The dimension to evaluate through.

#     Returns
#     -------
#     gpuarray
#         Minimum values.

#     Examples
#     --------
#     >>> a = min_cuda(give_cuda([[1, 2, 3], [6, 5, 4]]), axis=1)
#     array([[1],
#            [4]])

#     >>> type(a)
#     <class 'pycuda.gpuarray.GPUArray'>

#     """

#     return skcuda.misc.min(a, axis, keepdims=True)


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
        Maximum values from both GPArrays, or single value if only one GPUarray.

    Examples
    --------
    >>> a = maximum_cuda(give_cuda([1, 2, 3]), give_cuda([3, 2, 1]))
    array([[3, 2, 3]])

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
        Minimum values from both GPArrays, or single value if only one GPUarray.

    Examples
    --------
    >>> a = minimum_cuda(give_cuda([1, 2, 3]), give_cuda([3, 2, 1]))
    array([[1, 2, 1]])

    >>> type(a)
    <class 'pycuda.gpuarray.GPUArray'>

    """

    if b is not None:
        return cuda_array.minimum(a, b)
    return cuda_array.min(a)


# def mean_cuda(a, axis):

#     """ Mean of GPUArray elements in a given axis direction.

#     Parameters
#     ----------
#     a : gpuarray
#         GPUArray with elements to be operated on.
#     axis : int
#         Axis direction to mean average through.

#     Returns
#     -------
#     gpuarray
#         GPUArray mean through specified dimension.

#     Examples
#     --------
#     >>> mean_cuda(give_cuda([[1, 2], [3, 4]]), axis=0)
#     array([ 2.,  3.])

#     >>> type(a)
#     <class 'pycuda.gpuarray.GPUArray'>

#     """

#     return skcuda.misc.mean(a, axis)


def round_cuda():
    raise NotImplementedError


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
    >>> a = sin_cuda(give_cuda([0, pi / 4]))
    array([ 0.,  0.70710678])

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
    >>> a = sinh_cuda(give_cuda([0, pi / 4]))
    array([ 0.,  0.86867096])

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
    array([ 2.,  3.])

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

    Examples
    --------
    >>> a = sum_cuda(give_cuda([[1, 2], [3, 4]]), axis=0)
    array([ 4.,  6.])

    >>> type(a)
    <class 'pycuda.gpuarray.GPUArray'>

    """

    if axis is not None:
        raise NotImplementedError
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
    >>> a = tan_cuda(give_cuda([0, pi / 4]))
    array([ 0.,  1])

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
    >>> a = tanh_cuda(give_cuda([0, pi / 4]))
    array([ 0.,  0.6557942])

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

    a = maximum_cuda(give_cuda([1, 2, 3]), give_cuda([3, 2, 1]))
    # a = maximum_cuda(give_cuda([1, 2, 3]))
    # a = minimum_cuda(give_cuda([1, 2, 3]), give_cuda([3, 2, 1]))
    # a = minimum_cuda(give_cuda([1, 2, 3]))
    # a = abs_cuda(give_cuda([-0.1, -1.7]))
    # b = argmax_cuda(give_cuda([[1, 2, 3], [6, 5, 4]]), axis=1)
    # c = argmin_cuda(give_cuda([[1, 2, 3], [6, 5, 4]]), axis=1)
    # a = acos_cuda(give_cuda([0.5, 1]))
    # a = asin_cuda(give_cuda([0.5, 1]))
    # a = atan_cuda(give_cuda([0.5, 1]))
    # a = ceil_cuda(give_cuda([0.5, 0.1, 1.9]))
    # a = cos_cuda(give_cuda([0, pi / 4]))
    # a = cosh_cuda(give_cuda([0, pi / 4]))
    # a = exp_cuda(give_cuda([0, 1]))
    # a = floor_cuda(give_cuda([0.5, 0.1, 1.9]))
    # a = log_cuda(give_cuda([1, 10]))
    # a = log10_cuda(give_cuda([1, 10]))
    # k = max_cuda(give_cuda([[1, 2, 3], [6, 5, 4]]), axis=1)
    # l = min_cuda(give_cuda([[1, 2, 3], [6, 5, 4]]), axis=1)
    # m = mean_cuda(give_cuda([[1, 2], [3, 4]]), axis=0)
    # a = sin_cuda(give_cuda([0, pi / 4]))
    # a = sinh_cuda(give_cuda([0, pi / 4]))
    # a = sqrt_cuda(give_cuda([4, 9]))
    # a = sum_cuda(give_cuda([[1, 2], [3, 4]]), axis=None)
    # a = tan_cuda(give_cuda([0, pi / 4]))
    # a = tanh_cuda(give_cuda([0, pi / 4]))

    # print(a)


