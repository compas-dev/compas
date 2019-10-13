from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from numpy import asarray
from numpy import hstack
from numpy import ones

from scipy.linalg import solve


__all__ = [
    'transform_points_numpy',
    'transform_vectors_numpy',

    'homogenize_numpy',
    'dehomogenize_numpy',

]


def transform_points_numpy(points, T):
    T = asarray(T)
    points = homogenize_numpy(points, w=1.0)
    return dehomogenize_numpy(points.dot(T.T))


def transform_vectors_numpy(vectors, T):
    T = asarray(T)
    vectors = homogenize_numpy(vectors, w=0.0)
    return dehomogenize_numpy(vectors.dot(T.T))


# ==============================================================================
# helping helpers
# ==============================================================================


def homogenize_numpy(points, w=1.0):
    points = asarray(points)
    points = hstack((points, w * ones((points.shape[0], 1))))
    return points


def dehomogenize_numpy(points):
    points = asarray(points)
    return points[:, :-1] / points[:, -1].reshape((-1, 1))


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
