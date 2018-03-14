
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

try:
    import pycuda
    import pycuda.autoinit
    import pycuda.cumath
except ImportError as e:
    pass

try:
    import skcuda
    import skcuda.autoinit
except ImportError as e:
    pass


__author__    = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__ = 'Copyright 2018, Block Research Group - ETH Zurich'
__license__   = 'MIT License'
__email__     = 'liew@arch.ethz.ch'


__all__ = [
    'abs_cuda',
    'argmax_cuda',
    'argmin_cuda',
#     'cuda_acos',
#     'cuda_asin',
#     'cuda_atan',
#     'cuda_ceil',
#     'cuda_cos',
#     'cuda_cosh',
#     'cuda_exp',
#     'cuda_floor',
#     'cuda_log',
#     'cuda_max',
#     'cuda_min',
#     'cuda_mean',
#     'cuda_sin',
#     'cuda_sinh',
#     'cuda_sqrt',
#     'cuda_sum',
#     'cuda_tan',
#     'cuda_tanh',
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


def argmax_cuda(a, axis):

    """ Location of maximum GPUArray elements.

    Parameters
    ----------
    a : gpuarray
        GPUArray with the elements to find maximum values.
    axis : int
        The dimension to evaluate through.

    Returns
    -------
    gpuarray
        Location of maximum values.

    Examples
    --------
    >>> a = argmax_cuda(give_cuda([[1, 2, 3], [6, 5, 4]]), axis=1)
    array([[2],
           [0]], dtype=uint32)

    >>> type(a)
    <class 'pycuda.gpuarray.GPUArray'>

    """

    return skcuda.misc.argmax(a, axis, keepdims=True)


def argmin_cuda(a, axis):

    """ Location of minimum GPUArray elements.

    Parameters
    ----------
    a : gpuarray
        GPUArray with the elements to find minimum values.
    axis : int
        The dimension to evaluate through.

    Returns
    -------
    gpuarray
        Location of minimum values.

    Examples
    --------
    >>> a = argmin_cuda(give_cuda([[1, 2, 3], [6, 5, 4]]), axis=1)
    array([[0],
           [2]], dtype=uint32)

    >>> type(a)
    <class 'pycuda.gpuarray.GPUArray'>

    """

    return skcuda.misc.argmin(a, axis, keepdims=True)


# def cuda_acos(a):
#     """ Trigonometric arccosine of GPUArray elements.

#     Parameters:
#         a (gpuarray): GPUArray with elements to be operated on.

#     Returns:
#         gpuarray: acos(GPUArray)

#     Examples:
#         >>> a = cuda_acos(give_cuda([0.5, 1]))
#         array([ 1.04719755,  0.])
#         >>> type(a)
#         <class 'pycuda.gpuarray.GPUArray'>
#     """
#     return pycuda.cumath.acos(a)


# def cuda_asin(a):
#     """ Trigonometric arcsine of GPUArray elements.

#     Parameters:
#         a (gpuarray): GPUArray with elements to be operated on.

#     Returns:
#         gpuarray: asin(GPUArray)

#     Examples:
#         >>> a = cuda_asin(give_cuda([0.5, 1]))
#         array([ 0.52359878,  1.57079633])
#         >>> type(a)
#         <class 'pycuda.gpuarray.GPUArray'>
#     """
#     return pycuda.cumath.asin(a)


# def cuda_atan(a):
#     """ Trigonometric arctangent of GPUArray elements.

#     Parameters:
#         a (gpuarray): GPUArray with elements to be operated on.

#     Returns:
#         gpuarray: atan(GPUArray)

#     Examples:
#         >>> a = cuda_atan(give_cuda([0.5, 1]))
#         array([ 0.46364761,  0.78539816])
#         >>> type(a)
#         <class 'pycuda.gpuarray.GPUArray'>
#     """
#     return pycuda.cumath.atan(a)


# def cuda_ceil(a):
#     """ Ceiling of GPUArray elements.

#     Parameters:
#         a (gpuarray): GPUArray with elements to be operated on.

#     Returns:
#         gpuarray: ceil(GPUArray)

#     Examples:
#         >>> a = cuda_ceil(give_cuda([0.5, 0.1, 1.9]))
#         array([ 1.,  1.,  2.])
#         >>> type(a)
#         <class 'pycuda.gpuarray.GPUArray'>
#     """
#     return pycuda.cumath.ceil(a)


# def cuda_cos(a):
#     """ Trigonometric cosine of GPUArray elements.

#     Parameters:
#         a (gpuarray): GPUArray with elements to be operated on.

#     Returns:
#         gpuarray: cos(GPUArray)

#     Examples:
#         >>> a = cuda_cos(give_cuda([0, pi / 4]))
#         array([ 1.,  0.70710678])
#         >>> type(a)
#         <class 'pycuda.gpuarray.GPUArray'>
#     """
#     return pycuda.cumath.cos(a)


# def cuda_cosh(a):
#     """ Hyperbolic cosine of GPUArray elements.

#     Parameters:
#         a (gpuarray): GPUArray with elements to be operated on.

#     Returns:
#         gpuarray: cosh(GPUArray)

#     Examples:
#         >>> a = cuda_cosh(give_cuda([0, pi / 4]))
#         array([ 1.,  1.32460909])
#         >>> type(a)
#         <class 'pycuda.gpuarray.GPUArray'>
#     """
#     return pycuda.cumath.cosh(a)


# def cuda_exp(a):
#     """ Exponential of GPUArray elements.

#     Parameters:
#         a (gpuarray): GPUArray with elements to be operated on.

#     Returns:
#         gpuarray: exp(GPUArray)

#     Examples:
#         >>> a = cuda_exp(give_cuda([0, 1]))
#         array([ 1.,  2.71828183])
#         >>> type(a)
#         <class 'pycuda.gpuarray.GPUArray'>
#     """
#     return pycuda.cumath.exp(a)


# def cuda_floor(a):
#     """ Floor of GPUArray elements.

#     Parameters:
#         a (gpuarray): GPUArray with elements to be operated on.

#     Returns:
#         b = floor(GPUArray)

#     Examples:
#         >>> a = cuda_floor(give_cuda([0.5, 0.1, 1.9]))
#         array([ 0.,  0.,  1.])
#         >>> type(a)
#         <class 'pycuda.gpuarray.GPUArray'>
#     """
#     return pycuda.cumath.floor(a)


# def cuda_log(a):
#     """ Natural logarithm of GPUArray elements.

#     Parameters:
#         a (gpuarray): GPUArray with elements to be operated on.

#     Returns:
#         gpuarray: log(GPUArray)

#     Examples:
#         >>> a = cuda_log(give_cuda([1, 10]))
#         array([ 0.,  2.30258509])
#         >>> type(a)
#         <class 'pycuda.gpuarray.GPUArray'>
#     """
#     return pycuda.cumath.log(a)


# def cuda_log10(a):
#     """ Base10 logarithm of GPUArray elements.

#     Parameters:
#         a (gpuarray): GPUArray with elements to be operated on.

#     Returns:
#         gpuarray: log10(GPUArray)

#     Examples:
#         >>> a = cuda_log10(give_cuda([1, 10]))
#         array([ 0.,  1.])
#         >>> type(a)
#         <class 'pycuda.gpuarray.GPUArray'>
#     """
#     return pycuda.cumath.log10(a)


# def cuda_max(a, axis):
#     """ Maximum values of GPUArray elements.

#     Parameters:
#         a (gpuarray): GPUArray with the elements to find maximum values.
#         axis (int): The dimension to evaluate through.

#     Returns:
#         gpuarray: Maximum values.

#     Examples:
#         >>> a = cuda_max(give_cuda([[1, 2, 3], [6, 5, 4]]), axis=1)
#         array([[3],
#                [6]])
#         >>> type(a)
#         <class 'pycuda.gpuarray.GPUArray'>
#     """
#     return skcuda.misc.max(a, axis, keepdims=True)


# def cuda_min(a, axis):
#     """ Minimum values of GPUArray elements.

#     Parameters:
#         a (gpuarray): GPUArray with the elements to find minimum values.
#         axis (int): The dimension to evaluate through.

#     Returns:
#         gpuarray: Minimum values.

#     Examples:
#         >>> a = cuda_min(give_cuda([[1, 2, 3], [6, 5, 4]]), axis=1)
#         array([[1],
#                [4]])
#         >>> type(a)
#         <class 'pycuda.gpuarray.GPUArray'>
#     """
#     return skcuda.misc.min(a, axis, keepdims=True)


# def cuda_mean(a, axis):
#     """ Mean of GPUArray elements in a given axis direction.

#     Parameters:
#         a (gpuarray): GPUArray with elements to be operated on.
#         axis (int): Axis direction to mean average through.

#     Returns:
#         gpuarray: GPUArray mean through specified dimension.

#     Examples
#         >>> cuda_mean(give_cuda([[1, 2], [3, 4]]), axis=0)
#         array([ 2.,  3.])
#         >>> type(a)
#         <class 'pycuda.gpuarray.GPUArray'>
#     """
#     return skcuda.misc.mean(a, axis)


# def cuda_sin(a):
#     """ Trigonometric sine of GPUArray elements.

#     Parameters:
#         a (gpuarray): GPUArray with elements to be operated on.

#     Returns:
#         gpuarray: sin(GPUArray)

#     Examples:
#         >>> a = cuda_sin(give_cuda([0, pi / 4]))
#         array([ 0.,  0.70710678])
#         >>> type(a)
#         <class 'pycuda.gpuarray.GPUArray'>
#     """
#     return pycuda.cumath.sin(a)


# def cuda_sinh(a):
#     """ Hyperbolic sine of GPUArray elements.

#     Parameters:
#         a (gpuarray): GPUArray with elements to be operated on.

#     Returns:
#         gpuarray: sinh(GPUArray)

#     Examples:
#         >>> a = cuda_sinh(give_cuda([0, pi / 4]))
#         array([ 0.,  0.86867096])
#         >>> type(a)
#         <class 'pycuda.gpuarray.GPUArray'>
#     """
#     return pycuda.cumath.sinh(a)


# def cuda_sqrt(a):
#     """ Square-root of GPUArray elements.

#     Parameters:
#         a (gpuarray): GPUArray with elements to be operated on.

#     Returns:
#         gpuarray: sqrt(GPUArray)

#     Examples:
#         >>> a = cuda_sqrt(give_cuda([4, 9]))
#         array([ 2.,  3.])
#         >>> type(a)
#         <class 'pycuda.gpuarray.GPUArray'>
#     """
#     return pycuda.cumath.sqrt(a)


# def cuda_sum(a, axis):
#     """ Sum of GPUArray elements in a given axis direction.

#     Parameters:
#         a (gpuarray): GPUArray with elements to be operated on.
#         axis (int) : Axis direction to sum through.

#     Returns:
#         gpuarray: GPUArray sum across the specified dimension.

#     Examples:
#         >>> cuda_sum(give_cuda([[1, 2], [3, 4]]), axis=0)
#         array([ 4.,  6.])
#         >>> type(a)
#         <class 'pycuda.gpuarray.GPUArray'>
#     """
#     return skcuda.misc.sum(a, axis=axis)


# def cuda_tan(a):
#     """ Trigonometric tangent of GPUArray elements.

#     Parameters:
#         a (gpuarray): GPUArray with elements to be operated on.

#     Returns:
#         gpuarray: tan(GPUArray)

#     Examples:
#         >>> a = cuda_tan(give_cuda([0, pi / 4]))
#         array([ 0.,  1])
#         >>> type(a)
#         <class 'pycuda.gpuarray.GPUArray'>
#     """
#     return pycuda.cumath.tan(a)


# def cuda_tanh(a):
#     """ Hyperbolic tangent of GPUArray elements.

#     Parameters:
#         a (gpuarray): GPUArray with elements to be operated on.

#     Returns:
#         gpuarray: tanh(GPUArray)

#     Examples:
#         >>> a = cuda_tanh(give_cuda([0, pi / 4]))
#         array([ 0.,  0.6557942])
#         >>> type(a)
#         <class 'pycuda.gpuarray.GPUArray'>
#     """
#     return pycuda.cumath.tanh(a)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    from compas.hpc import give_cuda

    a = abs_cuda(give_cuda([-0.1, -1.7]))
    b = argmax_cuda(give_cuda([[1, 2, 3], [6, 5, 4]]), axis=1)
    c = argmin_cuda(give_cuda([[1, 2, 3], [6, 5, 4]]), axis=1)
