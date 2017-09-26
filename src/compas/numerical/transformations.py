from __future__ import print_function

from numpy import array
from numpy import asarray
from numpy import ones
from numpy import hstack
from numpy import vstack

from numpy.random import randint

from compas.numerical.xforms import rotation_matrix


__author__     = ['Tom Van Mele <vanmelet@ethz.ch>',
                  'Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2016, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


__all__ = [
]


def homogenize(points):
    points = asarray(points)
    points = hstack((points, ones((points.shape[0], 1))))
    return points


def dehomogenize(points):
    points = asarray(points)
    return points[:, :-1] / points[:, -1].reshape((-1, 1))


def transform(points, T):
    points = homogenize(points)
    points = T.dot(points.T).T
    return dehomogenize(points)


# ==============================================================================
# rotate
# ==============================================================================


def rotate_points(points, axis, angle, origin=None):
    """Rotates points around an arbitrary axis in 3D (radians).

    Parameters:
        points (sequence of sequence of float): XYZ coordinates of the points.
        axis (sequence of float): The rotation axis.
        angle (float): the angle of rotation in radians.
        origin (sequence of float): Optional. The origin of the rotation axis.
            Default is ``[0.0, 0.0, 0.0]``.

    Returns:
        list: the rotated points

    References:
        https://en.wikipedia.org/wiki/Rotation_matrix

    """
    R = rotation_matrix(angle, axis, origin)
    points = transform(points, R)
    return points


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    from math import pi

    import matplotlib.pyplot as plt

    n = 200

    points = randint(0, high=100, size=(n, 3)).astype(float)
    points = vstack((points, array([[0, 0, 0], [100, 0, 0]], dtype=float).reshape((2, 3))))

    print(points)

    a = pi / randint(1, high=8)

    points_ = rotate_points(points, [0, 0, 1], a, [0, 0, 0])

    # R = rotation_matrix(a, (0, 0, 1), [50, 0, 0]).astype(float).reshape((4, 4))

    # points_ = transform(points, R)

    # # R = rotation_matrix(a, (0, 0, 1), [0, 0, 0]).astype(float).reshape((4, 4))

    # # T1 = translation_matrix([-50, 0, 0]).astype(float).reshape((4, 4))
    # # T2 = translation_matrix([50, 0, 0]).astype(float).reshape((4, 4))

    # # points_ = transform(points, T2.dot(R.dot(T1)))

    # print(points_)

    plt.plot(points[:, 0], points[:, 1], 'bo')
    plt.plot(points_[:, 0], points_[:, 1], 'ro')

    plt.plot(points[-2:, 0], points[-2:, 1], 'b-', label='before')
    plt.plot(points_[-2:, 0], points_[-2:, 1], 'r-', label='after')

    plt.legend(title='Rotation {0}'.format(180 * a / pi), fancybox=True)

    ax = plt.gca()
    ax.set_aspect('equal')

    plt.show()
