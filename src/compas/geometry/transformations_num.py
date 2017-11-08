from __future__ import print_function

from random import choice

from numpy import array
from numpy import asarray
from numpy import vstack

from numpy.random import randint

from compas.geometry.basic_num import homogenize_vectors_numpy
from compas.geometry.basic_num import dehomogenize_vectors_numpy


__author__     = ['Tom Van Mele <vanmelet@ethz.ch>',
                  'Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2016, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


__all__ = [
]


def transform_numpy(points, T):
    T = asarray(T)
    points = homogenize_vectors_numpy(points)
    points = T.dot(points.T).T
    return dehomogenize_vectors_numpy(points)


# def random_rotation_matrix():
#     a = randint(1, high=8) * 10 * 3.14159 / 180
#     d = [choice([0, 1]), choice([0, 1]), choice([0, 1])]
#     if d == [0, 0, 0]:
#         d = [0, 0, 1]
#     return rotation_matrix(a, d)


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    from math import pi

    import matplotlib.pyplot as plt

    from compas.geometry.transformations import rotation_matrix

    n = 200

    points = randint(0, high=100, size=(n, 3)).astype(float)
    points = vstack((points, array([[0, 0, 0], [100, 0, 0]], dtype=float).reshape((2, 3))))

    print(points)

    a = pi / randint(1, high=8)

    points_ = transform_numpy(points, [0, 0, 1], a, [0, 0, 0])

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
