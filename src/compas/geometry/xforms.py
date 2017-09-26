""""""

from __future__ import print_function
from __future__ import division

from math import cos
from math import sin

from compas.geometry import normalize_vector
from compas.geometry import multiply_matrices


__author__     = ['Tom Van Mele <vanmelet@ethz.ch>',
                  'Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2016, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


__all__ = [
    'transform',
    'translation_matrix',
    'rotation_matrix',
    'scale_matrix',
    'shear_matrix',
    'projection_matrix'
]


# notes:
# - add object oriented interface
# - quaternions?
# - quaternion math?
# - functions to apply transformations
# - homogenization
# - dehomogenization
# - Matrix.apply
# - Matrix.factory
# - ...

def _homogenize(points):
    points = [[point[0], point[1], point[2], 1.0] for point in points]
    return points


def _dehomogenize(points):
    return [point[0:3] for point in points]


def transform(points, T):
    points = _homogenize(points)
    points = transpose_matrix(multiply_matrices(T, transpose_matrix(points)))
    return _dehomogenize(points)


def translation_matrix(direction):
    """Creates a translation matrix to translate vectors.

    Parameters:
        direction (list): The x, y and z components of the translation.

    Returns:
        list: The (4 x 4) translation matrix.

    Homogeneous vectors are used, i.e. vector [x, y, z].T is represented as
    [x, y, z, 1].T. Matrix multiplication of the translation matrix with the
    homogeneous vector will return the new translated vector.

    Examples:
        >>> T = translation_matrix([1, 2, 3])
        [[1 0 0 1]
         [0 1 0 2]
         [0 0 1 3]
         [0 0 0 1]]
    """
    return [[1.0, 0.0, 0.0, direction[0]],
            [0.0, 1.0, 0.0, direction[1]],
            [0.0, 0.0, 1.0, direction[2]],
            [0.0, 0.0, 0.0, 1.0]]


def rotation_matrix(angle, direction, point=None):
    """Creates a rotation matrix for rotating vectors around an axis.

    Parameters:
        angle (float): Angle in radians to rotate by.
        direction (list): The x, y and z components of the rotation axis.

    Returns:
        list: The (3 x 3) rotation matrix.

    Rotates a vector around a given axis (the axis will be unitised), the
    rotation is based on the right hand rule, i.e. anti-clockwise when the axis
    of rotation points towards the observer.

    Examples:
        >>> R = rotation_matrix(angle=pi/2, direction=[0, 0, 1])
        [[  6.12-17  -1.00+00   0.00+00]
         [  1.00+00   6.12-17   0.00+00]
         [  0.00+00   0.00+00   1.00+00]]
    """
    # To perform a rotation around an arbitrary line (i.e. an axis not through
    # the origin) an origin other than (0, 0, 0) may be provided for the
    # direction vector. Note that the returned 'rotation matrix' is then
    # composed of three translations and a rotation: Tp-1 Txy-1 Tz-1 R Tz Txy Tp
    # l = sum(direction[i] ** 2 for i in range(3)) ** 0.5
    # u = [direction[i] / l for i in range(3)]
    x, y, z = normalize_vector(direction)
    c = cos(angle)
    t = 1 - c
    s = sin(angle)
    R = [
        [t * x * x + c    , t * x * y - s * z, t * x * z + s * y, 0.0],
        [t * x * y + s * z, t * y * y + c    , t * y * z - s * x, 0.0],
        [t * x * z - s * y, t * y * z + s * x, t * z * z + c    , 0.0],
        [0.0              , 0.0              , 0.0              , 1.0]
    ]

    if point is None:
        return R

    T1 = translation_matrix([-p for p in point])
    T2 = translation_matrix(point)

    return multiply_matrices(T2, multiply_matrices(R, T1))


def scale_matrix(x, y=None, z=None):
    """Creates a scale matrix to scale vectors.

    Parameters:
        factor (float): Uniform scale factor for the  x, y and z components.

    Returns:
        list: The (3 x 3) scale matrix.

    The scale matrix is a (3 x 3) matrix with the scale factor along all of the
    three diagonal elements, used to scale a vector.

    Examples:
        >>> S = scale_matrix(2)
        [[2 0 0]
         [0 2 0]
         [0 0 2]]
    """
    if y is None:
        y = x
    if z is None:
        z = x
    return [[x, 0.0, 0.0, 0.0],
            [0.0, y, 0.0, 0.0],
            [0.0, 0.0, z, 0.0],
            [0.0, 0.0, 0.0, 1.0]]


def shear_matrix():
    pass


def projection_matrix(point, normal):
    pass


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":
    pass
