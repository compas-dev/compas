from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry._core import subtract_vectors
from compas.geometry._core import subtract_vectors_xy
from compas.geometry._core import cross_vectors
from compas.geometry._core import cross_vectors_xy
from compas.geometry._core import length_vector
from compas.geometry._core import normalize_vector

from compas.geometry._core import centroid_points


__all__ = [
    'normal_polygon',
    'normal_triangle',
    'normal_triangle_xy',
]


def normal_polygon(polygon, unitized=True):
    """Compute the normal of a polygon defined by a sequence of points.

    Parameters
    ----------
    polygon : sequence[point] | :class:`~compas.geometry.Polygon`
        A list of polygon point coordinates.
    unitized : bool, optional
        If True, unitize the normal vector.

    Returns
    -------
    [float, float, float]
        The normal vector.

    Raises
    ------
    AssertionError
        If less than three points are provided.

    Notes
    -----
    The points in the list should be unique. For example, the first and last
    point in the list should not be the same.

    """
    p = len(polygon)

    assert p > 2, "At least three points required"

    nx = 0
    ny = 0
    nz = 0

    o = centroid_points(polygon)
    a = polygon[-1]
    oa = subtract_vectors(a, o)

    for i in range(p):
        b = polygon[i]
        ob = subtract_vectors(b, o)
        n = cross_vectors(oa, ob)
        oa = ob

        nx += n[0]
        ny += n[1]
        nz += n[2]

    if not unitized:
        return [nx, ny, nz]

    return normalize_vector([nx, ny, nz])


def normal_triangle(triangle, unitized=True):
    """Compute the normal vector of a triangle.

    Parameters
    ----------
    triangle : [point, point, point] | :class:`~compas.geometry.Polygon`
        A list of triangle point coordinates.
    unitized : bool, optional
        If True, unitize the normal vector.

    Returns
    -------
    [float, float, float]
        The normal vector.

    Raises
    ------
    AssertionError
        If the triangle does not have three vertices.

    """
    assert len(triangle) == 3, "Three points are required."
    a, b, c = triangle
    ab = subtract_vectors(b, a)
    ac = subtract_vectors(c, a)
    n = cross_vectors(ab, ac)
    if not unitized:
        return n
    lvec = 1 / length_vector(n)
    return [lvec * n[0], lvec * n[1], lvec * n[2]]


def normal_triangle_xy(triangle, unitized=True):
    """Compute the normal vector of a triangle assumed to lie in the XY plane.

    Parameters
    ----------
    triangle : [point, point, point] | :class:`~compas.geometry.Polygon`
        A list of triangle point coordinates.
        Z-coordinates are ignored.
    unitized : bool, optional
        If True, unitize the normal vector.

    Returns
    -------
    [float, float, float]
        The normal vector, which is a vector perpendicular to the XY plane.

    Raises
    ------
    AssertionError
        If the triangle does not have three vertices.

    """
    a, b, c = triangle
    ab = subtract_vectors_xy(b, a)
    ac = subtract_vectors_xy(c, a)
    n = cross_vectors_xy(ab, ac)
    if not unitized:
        return n
    return [0, 0, n[2] / length_vector(n)]
