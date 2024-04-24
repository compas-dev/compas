from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from ._algebra import cross_vectors
from ._algebra import cross_vectors_xy
from ._algebra import length_vector
from ._algebra import normalize_vector
from ._algebra import subtract_vectors
from ._algebra import subtract_vectors_xy
from .centroids import centroid_points


def normal_polygon(polygon, unitized=True):
    """Compute the normal of a polygon defined by a sequence of points.

    Parameters
    ----------
    polygon : sequence[point] | :class:`compas.geometry.Polygon`
        A list of polygon point coordinates.
    unitized : bool, optional
        If True, unitize the normal vector.

    Returns
    -------
    [float, float, float]
        The normal vector.

    Raises
    ------
    ValueError
        If less than three points are provided.

    See Also
    --------
    normal_triangle
    normal_triangle_xy

    Notes
    -----
    The points in the list should be unique. For example, the first and last
    point in the list should not be the same.

    """
    p = len(polygon)

    if p < 3:
        raise ValueError("At least three points required.")

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

        nx += n[0] * 0.5
        ny += n[1] * 0.5
        nz += n[2] * 0.5

    if not unitized:
        return [nx, ny, nz]

    return normalize_vector([nx, ny, nz])


def normal_triangle(triangle, unitized=True):
    """Compute the normal vector of a triangle.

    Parameters
    ----------
    triangle : [point, point, point] | :class:`compas.geometry.Polygon`
        A list of triangle point coordinates.
    unitized : bool, optional
        If True, unitize the normal vector.

    Returns
    -------
    [float, float, float]
        The normal vector.

    Raises
    ------
    ValueError
        If the triangle does not have three vertices.

    See Also
    --------
    normal_polygon
    normal_triangle_xy

    """
    if len(triangle) != 3:
        raise ValueError("Three points are required.")

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
    triangle : [point, point, point] | :class:`compas.geometry.Polygon`
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
    ValueError
        If the triangle does not have three vertices.

    See Also
    --------
    normal_polygon
    normal_triangle

    """
    if len(triangle) != 3:
        raise ValueError("Three points are required.")

    a, b, c = triangle
    ab = subtract_vectors_xy(b, a)
    ac = subtract_vectors_xy(c, a)
    n = cross_vectors_xy(ab, ac)
    if not unitized:
        return n
    return [0, 0, n[2] / length_vector(n)]
