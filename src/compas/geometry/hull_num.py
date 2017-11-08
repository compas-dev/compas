from __future__ import print_function

from numpy import asarray
from scipy.spatial import ConvexHull


__author__     = ['Matthias Rippmann <rippmann@ethz.ch>']
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = '<rippmannt@ethz.ch>'


__all__ = [
    'convex_hull_numpy',
    'convex_hull_xy_numpy',
]


def convex_hull_numpy(points):
    points = asarray(points)
    n, dim = points.shape

    assert 2 < dim, "The point coordinates should be at least 3D: %i" % dim

    points = points[:, :3]
    hull = ConvexHull(points)
    return points[hull.vertices]


def convex_hull_xy_numpy(points):
    points = asarray(points)
    n, dim = points.shape

    assert 1 < dim, "The point coordinates should be at least 2D: %i" % dim

    points = points[:, :2]
    hull = ConvexHull(points)
    return points[hull.vertices].reshape((-1, 2))


# ==============================================================================
# Debugging
# ==============================================================================


if __name__ == "__main__":

    pass
