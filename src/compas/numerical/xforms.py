from __future__ import print_function

from random import choice

from numpy import array
from numpy.random import randint

import compas.geometry.xforms as xf


__author__     = ['Tom Van Mele <vanmelet@ethz.ch>',
                  'Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2016, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


__all__ = [
    'translation_matrix',
    'rotation_matrix',
    'random_rotation_matrix',
    'scale_matrix',
    'projection_matrix'
]


def translation_matrix(direction):
    """Creates a translation matrix to translate vectors.

    Parameters:
        direction (list): The x, y and z components of the translation.
        rtype (str): Return the result as 'list' or 'array'.

    Returns:
        (list, array): The (4 x 4) translation matrix.

    Homogeneous vectors are used, i.e. vector [x, y, z]T is represented as
    [x, y, z, 1]T. Matrix multiplication of the translation matrix with the
    homogeneous vector will return the new translated vector.

    Examples:
        >>> T = translation_matrix([1, 2, 3], rtype='array')
        [[1 0 0 1]
         [0 1 0 2]
         [0 0 1 3]
         [0 0 0 1]]
        >>> dot(T, array([[2], [2], [2], [1]]))
        [[3]
         [4]
         [5]
         [1]]
    """
    T = xf.translation_matrix(direction)
    return array(T)


def rotation_matrix(angle, direction, point=None):
    """Creates a rotation matrix for rotating vectors around an axis.

    Parameters:
        angle (float): Angle in radians to rotate by.
        direction (list): The x, y and z components of the rotation axis.
        rtype (str): Return the result as 'list' or 'array'.

    Returns:
        (list, array): The (3 x 3) rotation matrix.

    Rotates a vector around a given axis (the axis will be unitised), the
    rotation is based on the right hand rule, i.e. anti-clockwise when the axis
    of rotation points towards the observer.

    Examples:
        >>> R = rotation_matrix(angle=pi/2, direction=[0, 0, 1], rtype='array')
        [[  6.12-17  -1.00+00   0.00+00]
         [  1.00+00   6.12-17   0.00+00]
         [  0.00+00   0.00+00   1.00+00]]
        >>> dot(R, array([[1], [1], [1]]))
        [[-1.]
         [ 1.]
         [ 1.]]
    """
    # To perform a rotation around an arbitrary line (i.e. an axis not through
    # the origin) an origin other than (0, 0, 0) may be provided for the
    # direction vector. Note that the returned 'rotation matrix' is then
    # composed of three translations and a rotation: Tp-1 Txy-1 Tz-1 R Tz Txy Tp
    R = xf.rotation_matrix(angle, direction, point)
    return array(R)


def random_rotation_matrix():
    a = randint(1, high=8) * 10 * 3.14159 / 180
    d = [choice([0, 1]), choice([0, 1]), choice([0, 1])]
    if d == [0, 0, 0]:
        d = [0, 0, 1]
    return rotation_matrix(a, d)


def scale_matrix(factor):
    """Creates a scale matrix to scale vectors.

    Parameters:
        factor (float): Uniform scale factor for the  x, y and z components.
        rtype (str): Return the result as 'list' or 'array'.

    Returns:
        (list, array): The (3 x 3) scale matrix.

    The scale matrix is a (3 x 3) matrix with the scale factor along all of the
    three diagonal elements, used to scale a vector.

    Examples:
        >>> S = scale_matrix(2, rtype='array')
        [[2 0 0]
         [0 2 0]
         [0 0 2]]
        >>> dot(S, array([[1], [2], [3]]))
        [[2]
         [4]
         [6]]
    """
    S = xf.scale_matrix(factor)
    return array(S)


def projection_matrix():
    raise NotImplementedError


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    pass
