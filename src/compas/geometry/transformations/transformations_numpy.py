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

    'local_coords_numpy',
    'global_coords_numpy',
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


# this should be defined somewhere else
# and should have a python equivalent
# there is an implementation available in frame
def local_coords_numpy(origin, uvw, xyz):
    """Convert global coordinates to local coordinates.

    Parameters
    ----------
    origin : array-like
        The global (XYZ) coordinates of the origin of the local coordinate system.
    uvw : array-like
        The global coordinate difference vectors of the axes of the local coordinate system.
    xyz : array-like
        The global coordinates of the points to convert.

    Returns
    -------
    array
        The coordinates of the given points in the local coordinate system.

    Notes
    -----
    ``origin`` and ``uvw`` together form the frame of local coordinates.

    """
    uvw = asarray(uvw).T
    xyz = asarray(xyz).T - asarray(origin).reshape((-1, 1))
    rst = solve(uvw, xyz)
    return rst.T


# this should be defined somewhere else
# and should have a python equivalent
# there is an implementation available in frame
def global_coords_numpy(origin, uvw, rst):
    """Convert local coordinates to global (world) coordinates.

    Parameters
    ----------
    origin : array-like
        The origin of the local coordinate system.
    uvw : array-like
        The coordinate axes of the local coordinate system.
    rst : array-like
        The coordinates of the points wrt the local coordinate system.

    Returns
    -------
    array
        The world coordinates of the given points.

    Notes
    -----
    ``origin`` and ``uvw`` together form the frame of local coordinates.

    """
    uvw = asarray(uvw).T
    rst = asarray(rst).T
    xyz = uvw.dot(rst) + asarray(origin).reshape((-1, 1))
    return xyz.T


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
