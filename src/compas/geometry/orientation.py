""""""

from __future__ import print_function
from __future__ import division

from compas.geometry.basic import subtract_vectors
from compas.geometry.basic import subtract_vectors_xy
from compas.geometry.basic import cross_vectors
from compas.geometry.basic import cross_vectors_xy
from compas.geometry.basic import length_vector
from compas.geometry.basic import length_vector_xy

from compas.geometry.average import centroid_points


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


__all__ = [
    'normal_polygon',
    'normal_triangle',
    'normal_triangle_xy',
]


def normal_polygon(points, unitized=True):
    """Compute the normal of a polygon defined by a sequence of points.

    Note:
        The points in the list should be unique. For example, the first and last
        point in the list should not be the same.

    Parameters:
        points (sequence): A sequence of points.

    Returns:
        list: The normal vector.

    Raises:
        ValueError: If less than three points are provided.
    """
    p = len(points)
    assert p > 2, "At least three points required"
    nx = 0
    ny = 0
    nz = 0
    o = centroid_points(points)
    a = subtract_vectors(points[-1], o)
    for i in range(p):
        b = subtract_vectors(points[i], o)
        n = cross_vectors(a, b)
        a = b
        nx += n[0]
        ny += n[1]
        nz += n[2]
    if not unitized:
        return nx, ny, nz
    l = length_vector([nx, ny, nz])
    return nx / l, ny / l, nz / l


def _normal_polygon(points, unitized=True):
    """Compute the normal of a polygon defined by a sequence of points.

    Note:
        The points in the list should be unique. For example, the first and last
        point in the list should not be the same.

    Parameters:
        points (sequence): A sequence of points.

    Returns:
        list: The normal vector.

    Raises:
        ValueError: If less than three points are provided.
    """
    p = len(points)
    assert p > 2, "At least three points required"
    nx = 0
    ny = 0
    nz = 0
    for i in range(-1, p - 1):
        p1  = points[i - 1]
        p2  = points[i]
        p3  = points[i + 1]
        v1  = subtract_vectors(p1, p2)
        v2  = subtract_vectors(p3, p2)
        n   = cross_vectors(v1, v2)
        nx += n[0]
        ny += n[1]
        nz += n[2]
    if not unitized:
        return nx, ny, nz
    l = length_vector([nx, ny, nz])
    return nx / l, ny / l, nz / l


def normal_triangle(triangle, unitized=True):
    """Compute the normal vector of a triangle.
    """
    assert len(triangle) == 3, "Three points are required."
    a, b, c = triangle
    ab = subtract_vectors(b, a)
    ac = subtract_vectors(c, a)
    n  = cross_vectors(ab, ac)
    if not unitized:
        return n
    lvec = length_vector(n)
    return n[0] / lvec, n[1] / lvec, n[2] / lvec


def normal_triangle_xy(triangle, unitized=True):
    a, b, c = triangle
    ab = subtract_vectors_xy(b, a)
    ac = subtract_vectors_xy(c, a)
    n  = cross_vectors_xy(ab, ac)
    if not unitized:
        return n
    lvec = length_vector_xy(n)
    return n[0] / lvec, n[1] / lvec, n[2] / lvec


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":
    pass
