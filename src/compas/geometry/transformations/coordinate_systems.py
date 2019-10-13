from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import math

from compas.geometry.basic import normalize_vector
from compas.geometry.basic import cross_vectors
from compas.geometry.basic import norm_vector

from compas.geometry.transformations.matrices import matrix_change_basis
from compas.geometry.transformations.helpers import transform_points

__all__ = [
    'correct_axes',
    'local_coords',
    'local_coords_numpy',
    'global_coords',
    'global_coords_numpy',
]


def correct_axes(xaxis, yaxis):
    """Corrects xaxis and yaxis to be unit vectors and orthonormal.

    Parameters
    ----------
    xaxis: :class:`Vector` or list of float
    yaxis: :class:`Vector` or list of float

    Returns
    -------
    tuple: (xaxis, yaxis)
        The corrected axes.

    Raises
    ------
    ValueError: If xaxis and yaxis cannot span a plane.

    Examples
    --------
    >>> xaxis = [1, 4, 5]
    >>> yaxis = [1, 0, -2]
    >>> xaxis, yaxis = correct_axes(xaxis, yaxis)
    >>> allclose(xaxis, [0.1543, 0.6172, 0.7715], tol=0.001)
    True
    >>> allclose(yaxis, [0.6929, 0.4891, -0.5298], tol=0.001)
    True
    """
    xaxis = normalize_vector(xaxis)
    yaxis = normalize_vector(yaxis)
    zaxis = cross_vectors(xaxis, yaxis)
    if not norm_vector(zaxis):
        raise ValueError("Xaxis and yaxis cannot span a plane.")
    yaxis = cross_vectors(normalize_vector(zaxis), xaxis)
    return xaxis, yaxis


def local_coords(frame, xyz):
    """Convert global coordinates to local coordinates.

    Parameters
    ----------
    frame : :class:`Frame` or [point, xaxis, yaxis]
        The local coordinate system.
    xyz : array-like
        The global coordinates of the points to convert.

    Returns
    -------
    list of list of float
        The coordinates of the given points in the local coordinate system.


    Examples
    --------
    >>> import numpy as np
    >>> f = Frame([0, 1, 0], [3, 4, 1], [1, 5, 9])
    >>> xyz = [Point(2, 3, 5)]
    >>> Point(*local_coords(f, xyz)[0])
    Point(3.726, 4.088, 1.550)
    """
    from compas.geometry.primitives import Frame
    T = matrix_change_basis(Frame.worldXY(), frame)
    return transform_points(xyz, T)


def local_coords_numpy(frame, xyz):
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

    Examples
    --------
    >>> import numpy as np
    >>> frame = Frame([0, 1, 0], [3, 4, 1], [1, 5, 9])
    >>> xyz = [Point(2, 3, 5)]
    >>> rst = local_coords_numpy(frame, xyz)
    >>> np.allclose(rst, [[3.726, 4.088, 1.550]], rtol=1e-3)
    True
    """
    from numpy import asarray
    from scipy.linalg import solve

    origin = frame[0]
    uvw = [frame[1], frame[2], cross_vectors(frame[1], frame[2])]
    uvw = asarray(uvw).T
    xyz = asarray(xyz).T - asarray(origin).reshape((-1, 1))
    rst = solve(uvw, xyz)
    return rst.T


def global_coords(frame, xyz):
    """Convert local coordinates to global coordinates.

    Parameters
    ----------
    frame : :class:`Frame` or [point, xaxis, yaxis]
        The local coordinate system.
    xyz : list of `Points` or list of list of float
        The global coordinates of the points to convert.

    Returns
    -------
    list of list of float
        The coordinates of the given points in the local coordinate system.


    Examples
    --------
    >>> import numpy as np
    >>> f = Frame([0, 1, 0], [3, 4, 1], [1, 5, 9])
    >>> xyz = [Point(3.726, 4.088, 1.550)]
    >>> Point(*global_coords(f, xyz)[0])
    Point(2.000, 3.000, 5.000)
    """
    T = matrix_change_basis(frame, Frame.worldXY())
    return transform_points(xyz, T)


def global_coords_numpy(frame, rst):
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

    Examples
    --------
    >>> frame = Frame([0, 1, 0], [3, 4, 1], [1, 5, 9])
    >>> rst = [Point(3.726, 4.088, 1.550)]
    >>> xyz = global_coords_numpy(frame, rst)
    >>> numpy.allclose(xyz, [[2.000, 3.000, 5.000]], rtol=1e-3)
    True
    """
    from numpy import asarray

    origin = frame[0]
    uvw = [frame[1], frame[2], cross_vectors(frame[1], frame[2])]

    uvw = asarray(uvw).T
    rst = asarray(rst).T
    xyz = uvw.dot(rst) + asarray(origin).reshape((-1, 1))
    return xyz.T

# ==============================================================================
# Main
# ==============================================================================


if __name__ == "__main__":
    import doctest
    import numpy
    from compas.geometry import Point
    from compas.geometry import Frame
    from compas.geometry import allclose
    doctest.testmod(globs=globals())
