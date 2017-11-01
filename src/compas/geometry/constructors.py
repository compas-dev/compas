from __future__ import print_function
from __future__ import division

from math import sqrt
from random import sample

from compas.geometry.basic import subtract_vectors
from compas.geometry.basic import scale_vector
from compas.geometry.basic import normalize_vector
from compas.geometry.basic import length_vector
from compas.geometry.basic import length_vector_sqrd
from compas.geometry.basic import cross_vectors
from compas.geometry.basic import dot_vectors
from compas.geometry.basic import sum_vectors


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


__all__ = [
    'vector_from_points',
    'vector_from_points_xy',
    'plane_from_points',
    'circle_from_points',
    'circle_from_points_xy',
    'pointcloud',
    'pointcloud_xy'
]


def vector_from_points(a, b):
    """Construct a vector from two points.

    Parameters
    ----------
    a : sequence of float
        XYZ coordinates of first point.
    b : sequence of float
        XYZ coordinates of second point.

    Returns
    -------
    ab : sequence of float
        The vector from ``a`` to ``b``.

    Examples
    --------
    >>>

    """
    return b[0] - a[0], b[1] - a[1], b[2] - a[2]


def vector_from_points_xy(a, b):
    """
    Create a vector based on a start point a and end point b in the XY-plane.

    Parameters
    ----------
    a : sequence of float
        XY(Z) coordinates of a 2D or 3D point (Z will be ignored).
    b : sequence of float
        XY(Z) coordinates of a 2D or 3D point (Z will be ignored).

    Returns
    -------
    ab : tuple
        Resulting 3D vector in the XY-plane (Z = 0.0).

    Notes
    -----
    The result of this function is equal to ``subtract_vectors(b, a)``

    """
    return b[0] - a[0], b[1] - a[1], 0.0


def plane_from_points(a, b, c):
    """Construct a plane from three points.

    Parameters
    ----------
    a : sequence of float
        XYZ coordinates.
    b : sequence of float
        XYZ coordinates.
    c : sequence of float
        XYZ coordinates.

    Returns
    -------
    plane : tuple
        Base point and normal vector (normalized).

    Examples
    --------
    >>>

    """
    ab = subtract_vectors(b, a)
    ac = subtract_vectors(c, a)
    n = normalize_vector(cross_vectors(ab, ac))
    return a, n


def circle_from_points(a, b, c):
    """Construct a circle from three points.

    Parameters
    ----------
    a : sequence of float
        XYZ coordinates.
    b : sequence of float
        XYZ coordinates.
    c : sequence of float
        XYZ coordinates.

    Returns
    -------
    circle : tuple
        Center, radius, normal  of the circle.

    References
    ----------
    https://en.wikipedia.org/wiki/Circumscribed_circle

    Examples
    --------
    >>>

    """
    ab = subtract_vectors(b, a)
    cb = subtract_vectors(b, c)
    ba = subtract_vectors(a, b)
    ca = subtract_vectors(a, c)
    ac = subtract_vectors(c, a)
    bc = subtract_vectors(c, b)
    normal = normalize_vector(cross_vectors(ab, ac))
    d = 2 * length_vector_sqrd(cross_vectors(ba, cb))
    A = length_vector_sqrd(cb) * dot_vectors(ba, ca) / d
    B = length_vector_sqrd(ca) * dot_vectors(ab, cb) / d
    C = length_vector_sqrd(ba) * dot_vectors(ac, bc) / d
    Aa = scale_vector(a, A)
    Bb = scale_vector(b, B)
    Cc = scale_vector(c, C)
    center = sum_vectors([Aa, Bb, Cc])
    radius = length_vector(subtract_vectors(a, center))
    return center, radius, normal


def circle_from_points_xy(a, b, c):
    """Create a circle from three points lying in the XY-plane.

    Parameters
    ----------
    a : sequence of float
        XY(Z) coordinates of a 2D or 3D point (Z will be ignored).
    b : sequence of float
        XY(Z) coordinates of a 2D or 3D point (Z will be ignored).
    c : sequence of float
        XY(Z) coordinates of a 2D or 3D point (Z will be ignored).

    Returns
    -------
    tuple
        XYZ coordinates of center in the XY-plane (Z = 0.0) and radius of the circle.

    References
    ----------
    https://en.wikipedia.org/wiki/Circumscribed_circle

    Examples
    --------
    >>>

    """
    ax, ay = a[0], a[1]
    bx, by = b[0], b[1]
    cx, cy = c[0], c[1]
    a = bx - ax
    b = by - ay
    c = cx - ax
    d = cy - ay
    e = a * (ax + bx) + b * (ay + by)
    f = c * (ax + cx) + d * (ay + cy)
    g = 2 * (a * (cy - by) - b * (cx - bx))
    if g == 0:
        return None
    centerx = (d * e - b * f) / g
    centery = (a * f - c * e) / g
    radius = sqrt((ax - centerx) ** 2 + (ay - centery) ** 2)
    return [centerx, centery, 0.0], radius, [0, 0, 1]


def pointcloud(n, xbounds, ybounds=None, zbounds=None):
    """Construct a point cloud.

    Parameters
    ----------
    n : int
        The number of points in the cloud.
    xbounds : 2-tuple of int
        The min/max values for the x-coordinates of the points in the cloud.
    ybounds : 2-tuple of int, optional
        The min/max values for the y-coordinates of the points in the cloud.
        If ``None``, defaults to the value of the ``xbounds``.
    zbounds : 2-tuple of int, optional
        The min/max values for the z-coordinates of the points in the cloud.
        If ``None``, defaults to the value of the ``xbounds``.

    Returns
    -------
    list of list:
        A list of points forming the cloud.

    Examples
    --------
    >>>

    """
    if ybounds is None:
        ybounds = xbounds
    if zbounds is None:
        zbounds = xbounds
    xmin, xmax = map(int, xbounds)
    ymin, ymax = map(int, ybounds)
    zmin, zmax = map(int, zbounds)
    assert xmax - xmin > n, 'The bounds do not permit taking a random sample of this size.'
    assert ymax - ymin > n, 'The bounds do not permit taking a random sample of this size.'
    assert zmax - zmin > n, 'The bounds do not permit taking a random sample of this size.'
    x = sample(range(xmin, xmax), n)
    y = sample(range(ymin, ymax), n)
    z = sample(range(zmin, zmax), n)
    return [[1.0 * x[i],
             1.0 * y[i],
             1.0 * z[i]] for i in range(n)]


def pointcloud_xy(n, xbounds, ybounds=None):
    """Construct a point cloud in the XY plane.

    Parameters
    ----------
    n : int
        The number of points in the cloud.
    xbounds : 2-tuple of int
        The min/max values for the x-coordinates of the points in the cloud.
    ybounds : 2-tuple of int, optional
        The min/max values for the y-coordinates of the points in the cloud.
        If ``None``, defaults to the value of the ``xbounds``.

    Returns
    -------
    list:
        A list of points in the XY plane (Z = 0).

    Examples
    --------
    >>>

    """
    if ybounds is None:
        ybounds = xbounds
    xmin, xmax = map(int, xbounds)
    ymin, ymax = map(int, ybounds)
    assert xmax - xmin >= n, 'The bounds do not permit taking a random sample of this size.'
    assert ymax - ymin >= n, 'The bounds do not permit taking a random sample of this size.'
    x = sample(range(xmin, xmax), n)
    y = sample(range(ymin, ymax), n)
    return [[1.0 * x[i],
             1.0 * y[i], 0.0] for i in range(n)]


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":
    pass
