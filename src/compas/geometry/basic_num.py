""""""

from __future__ import division
from __future__ import print_function

from numpy import asarray
from numpy import hstack
from numpy import ones


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


__all__ = [
    'homogenize_vectors_numpy',
    'dehomogenize_vectors_numpy',
]


def homogenize_vectors_numpy(points):
    points = asarray(points)
    points = hstack((points, ones((points.shape[0], 1))))
    return points


def dehomogenize_vectors_numpy(points):
    points = asarray(points)
    return points[:, :-1] / points[:, -1].reshape((-1, 1))


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":
    pass
