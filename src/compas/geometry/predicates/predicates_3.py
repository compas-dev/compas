from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

# from math import pi
from math import fabs
from random import sample

from compas.utilities import window

from compas.geometry._core import subtract_vectors
from compas.geometry._core import cross_vectors
from compas.geometry._core import dot_vectors
from compas.geometry._core import normalize_vector

from compas.geometry._core import distance_point_point
from compas.geometry._core import distance_point_plane
from compas.geometry._core import distance_point_line
from compas.geometry._core import closest_point_on_segment

from compas.geometry._core import area_triangle


__all__ = [
    'is_colinear',
    'is_line_line_colinear',
    'is_coplanar',
    'is_polygon_convex',
    'is_point_on_plane',
    'is_point_infront_plane',
    'is_point_on_line',
    'is_point_on_segment',
    'is_point_on_polyline',
    'is_point_in_triangle',
    'is_point_in_circle',
    'is_intersection_line_line',
    'is_intersection_segment_segment',
    'is_intersection_line_triangle',
    'is_intersection_line_plane',
    'is_intersection_segment_plane',
    'is_intersection_plane_plane',
]


def is_colinear(a, b, c, tol=1e-6):
    """Determine if three points are colinear.

    Parameters
    ----------
    a : tuple, list, Point
        Point 1.
    b : tuple, list, Point
        Point 2.
    c : tuple, list, Point
        Point 3.
    tol : float, optional
        A tolerance for membership verification.
        Default is ``1e-6``.

    Returns
    -------
    bool
        ``True`` if the points are colinear.
        ``False`` otherwise.

    """
    return area_triangle([a, b, c]) < tol


def is_line_line_colinear(line1, line2, tol=1e-6):
    """Determine if two lines are colinear.

    Parameters
    ----------
    line1 : 2-tuple of points, Line
        Line 1.
    line2 : 2-tuple of points, Line
        Line 2.
    tol : float, optional
        A tolerance for colinearity verification.
        Default is ``1e-6``.

    Returns
    -------
    bool
        ``True`` if the lines are colinear.
        ``False`` otherwise.

    """
    a, b = line1
    c, d = line2
    return is_colinear(a, b, c, tol) and is_colinear(a, b, d, tol)


def is_coplanar(points, tol=0.01):
    """Determine if the points are coplanar.

    Parameters
    ----------
    points : sequence
        A sequence of locations in three-dimensional space.
    tol : float, optional
        A tolerance for planarity validation.
        Default is ``0.01``.

    Returns
    -------
    bool
        ``True`` if the points are coplanar.
        ``False`` otherwise.

    Notes
    -----
    Compute the normal vector (cross product) of the vectors formed by the first
    three points. Include one more vector at a time to compute a new normal and
    compare with the original normal. If their cross product is not zero, they
    are not parallel, which means the point are not in the same plane.

    Four points are coplanar if the volume of the tetrahedron defined by them is
    0. Coplanarity is equivalent to the statement that the pair of lines
    determined by the four points are not skew, and can be equivalently stated
    in vector form as (x2 - x0).[(x1 - x0) x (x3 - x2)] = 0.

    """
    tol2 = tol ** 2

    if len(points) == 4:
        v01 = subtract_vectors(points[1], points[0])
        v02 = subtract_vectors(points[2], points[0])
        v23 = subtract_vectors(points[3], points[0])
        res = dot_vectors(v02, cross_vectors(v01, v23))
        return res**2 < tol2

    # len(points) > 4
    # compare length of cross product vector to tolerance

    a, b, c = sample(points, 3)

    u = subtract_vectors(b, a)
    v = subtract_vectors(c, a)
    w = cross_vectors(u, v)

    for i in range(0, len(points) - 2):
        u = v
        v = subtract_vectors(points[i + 2], points[i + 1])
        wuv = cross_vectors(w, cross_vectors(u, v))

        if wuv[0]**2 > tol2 or wuv[1]**2 > tol2 or wuv[2]**2 > tol2:
            return False

    return True


def is_polygon_convex(polygon):
    """Determine if a polygon is convex.

    Parameters
    ----------
    polygon : sequence of sequence of floats
        The XYZ coordinates of the corners of the polygon.

    Notes
    -----
    Use this function for *spatial* polygons.
    If the polygon is in a horizontal plane, use :func:`is_polygon_convex_xy` instead.

    Returns
    -------
    bool
        ``True`` if the polygon is convex.
        ``False`` otherwise.

    See Also
    --------
    is_polygon_convex_xy

    Examples
    --------
    >>> polygon = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.4, 0.4, 0.0], [0.0, 1.0, 0.0]]
    >>> is_polygon_convex(polygon)
    False
    """
    a = polygon[0]
    o = polygon[1]
    b = polygon[2]
    oa = subtract_vectors(a, o)
    ob = subtract_vectors(b, o)
    n0 = cross_vectors(oa, ob)
    for a, o, b in window(polygon + polygon[:2], 3):
        oa = subtract_vectors(a, o)
        ob = subtract_vectors(b, o)
        n = cross_vectors(oa, ob)
        if dot_vectors(n, n0) >= 0:
            continue
        else:
            return False
    return True


def is_point_on_plane(point, plane, tol=1e-6):
    """Determine if a point lies on a plane.

    Parameters
    ----------
    point : sequence of float
        XYZ coordinates.
    plane : tuple
        Base point and normal defining a plane.
    tol : float, optional
        A tolerance for membership verification.
        Default is ``1e-6``.

    Returns
    -------
    bool
        ``True`` if the point is in on the plane.
        ``False`` otherwise.

    """
    return distance_point_plane(point, plane) <= tol


def is_point_infront_plane(point, plane, tol=1e-6):
    """Determine if a point lies in front of a plane.

    Parameters
    ----------
    point : sequence of float
        XYZ coordinates.
    plane : tuple
        Base point and normal defining a plane.
    tol : float, optional
        A tolerance for membership verification.
        Default is ``1e-6``.

    Returns
    -------
    bool
        ``True`` if the point is in front of the plane.
        ``False`` otherwise.

    """
    return dot_vectors(subtract_vectors(point, plane[0]), plane[1]) > tol


def is_point_on_line(point, line, tol=1e-6):
    """Determine if a point lies on a line.

    Parameters
    ----------
    point : sequence of float
        XYZ coordinates.
    line : tuple
        Two points defining a line.
    tol : float, optional
        A tolerance for membership verification.
        Default is ``1e-6``.

    Returns
    -------
    bool
        ``True`` if the point is in on the line.
        ``False`` otherwise.

    """
    return distance_point_line(point, line) <= tol


def is_point_on_segment(point, segment, tol=1e-6):
    """Determine if a point lies on a given line segment.

    Parameters
    ----------
    point : sequence of float
        XYZ coordinates.
    segment : tuple
        Two points defining the line segment.
    tol : float, optional
        A tolerance for membership verification.
        Default is ``1e-6``.

    Returns
    -------
    bool
        ``True`` if the point is on the line segment.
        ``False`` otherwise.

    """
    a, b = segment

    if not is_point_on_line(point, segment, tol=tol):
        return False

    d_ab = distance_point_point(a, b)

    if d_ab == 0:
        return False

    d_pa = distance_point_point(a, point)
    d_pb = distance_point_point(b, point)

    if d_pa + d_pb <= d_ab + tol:
        return True

    return False


def is_point_on_polyline(point, polyline, tol=1e-6):
    """Determine if a point is on a polyline.

    Parameters
    ----------
    point : sequence of float
        XYZ coordinates.
    polyline : sequence of sequence of float
        XYZ coordinates of the points of the polyline.
    tol : float, optional
        The tolerance for membership verification.
        Default is ``1e-6``.

    Returns
    -------
    bool
        ``True`` if the point is on the polyline.
        ``False`` otherwise.

    """
    for i in range(len(polyline) - 1):
        a = polyline[i]
        b = polyline[i + 1]
        c = closest_point_on_segment(point, (a, b))

        if distance_point_point(point, c) <= tol:
            return True

    return False


def is_point_in_triangle(point, triangle):
    """Determine if a point is in the interior of a triangle.

    Parameters
    ----------
    point : sequence of float
        XYZ coordinates.
    triangle : sequence of sequence of float
        XYZ coordinates of the triangle corners.

    Returns
    -------
    bool
        ``True`` if the point is in inside the triangle.
        ``False`` otherwise.

    Notes
    -----
    Should the point be on the same plane as the triangle?

    See Also
    --------
    compas.geometry.is_point_in_triangle_xy

    """
    def is_on_same_side(p1, p2, segment):
        a, b = segment
        v = subtract_vectors(b, a)
        c1 = cross_vectors(v, subtract_vectors(p1, a))
        c2 = cross_vectors(v, subtract_vectors(p2, a))

        if dot_vectors(c1, c2) >= 0:
            return True

        return False

    a, b, c = triangle

    if is_on_same_side(point, a, (b, c)) and \
       is_on_same_side(point, b, (a, c)) and \
       is_on_same_side(point, c, (a, b)):
        return True

    return False


def is_point_in_circle(point, circle):
    """Determine if a point lies in a circle.

    Parameters
    ----------
    point : sequence of float
        XYZ coordinates of a 3D point.
    circle : tuple
        center, radius, normal

    Returns
    -------
    bool
        ``True`` if the point lies in the circle.
        ``False`` otherwise.

    """
    plane, radius = circle
    if is_point_on_plane(point, plane):
        return distance_point_point(point, plane[0]) <= radius
    return False


def is_intersection_line_line(l1, l2, tol=1e-6):
    """Verifies if two lines intersect.

    Parameters
    ----------
    l1 : tuple
        A sequence of XYZ coordinates of two 3D points representing two points on the line.
    l2 : tuple
        A sequence of XYZ coordinates of two 3D points representing two points on the line.
    tol : float, optional
        A tolerance for intersection verification. Default is ``1e-6``.

    Returns
    --------
    bool
        ``True``if the lines intersect in one point.
        ``False`` if the lines are skew, parallel or lie on top of each other.
    """
    a, b = l1
    c, d = l2

    e1 = normalize_vector(subtract_vectors(b, a))
    e2 = normalize_vector(subtract_vectors(d, c))

    # check for parallel lines
    if abs(dot_vectors(e1, e2)) > 1.0 - tol:
        return False

    # check for intersection
    d_vector = cross_vectors(e1, e2)
    if dot_vectors(d_vector, subtract_vectors(c, a)) == 0:
        return True

    return False


def is_intersection_segment_segment(s1, s2, tol=1e-6):
    """Verifies if two segments intersect.

    Parameters
    ----------
    s1 : tuple
        Two 3D points representing the segment.
    s2 : tuple
        Two 3D points representing the segment.
    tol : float, optional
        A tolerance for intersection verification. Default is ``1e-6``.

    Returns
    --------
    bool
        ``True``if the segments intersect in one point.
        ``False`` if the segments are skew, parallel or lie on top of each other.
    """
    raise NotImplementedError


def is_intersection_line_triangle(line, triangle, tol=1e-6):
    """Verifies if a line (ray) intersects with a triangle.

    Parameters
    ----------
    line : tuple
        Two points defining the line.
    triangle : sequence of sequence of float
        XYZ coordinates of the triangle corners.
    tol : float, optional
        A tolerance for intersection verification.
        Default is ``1e-6``.

    Returns
    -------
    bool
        ``True`` if the line (ray) intersects with the triangle.
        ``False`` otherwise.

    Notes
    -----
    Based on the Moeller Trumbore intersection algorithm.
    The line is treated as continues, directed ray and not as line segment with a start and end point

    Examples
    --------
    >>>

    """
    a, b, c = triangle
    # direction vector and base point of line
    v1 = subtract_vectors(line[1], line[0])
    p1 = line[0]
    # Find vectors for two edges sharing V1
    e1 = subtract_vectors(b, a)
    e2 = subtract_vectors(c, a)
    # Begin calculating determinant - also used to calculate u parameter
    p = cross_vectors(v1, e2)
    # if determinant is near zero, ray lies in plane of triangle
    det = dot_vectors(e1, p)

    # NOT CULLING
    if det > - tol and det < tol:
        return False

    inv_det = 1.0 / det
    # calculate distance from V1 to ray origin
    t = subtract_vectors(p1, a)
    # Calculate u parameter and make_blocks bound
    u = dot_vectors(t, p) * inv_det

    # The intersection lies outside of the triangle
    if u < 0.0 or u > 1.0:
        return False

    # Prepare to make_blocks v parameter
    q = cross_vectors(t, e1)
    # Calculate V parameter and make_blocks bound
    v = dot_vectors(v1, q) * inv_det

    # The intersection lies outside of the triangle
    if v < 0.0 or u + v > 1.0:
        return False

    t = dot_vectors(e2, q) * inv_det

    if t > tol:
        return True

    # No hit
    return False


def is_intersection_line_plane(line, plane, tol=1e-6):
    """Determine if a line (ray) intersects with a plane.

    Parameters
    ----------
    line : tuple
        Two points defining the line.
    plane : tuple
        The base point and normal defining the plane.
    tol : float, optional
        A tolerance for intersection verification.
        Default is ``1e-6``.

    Returns
    -------
    bool
        ``True`` if the line intersects with the plane.
        ``False`` otherwise.
    """
    pt1 = line[0]
    pt2 = line[1]
    p_norm = plane[1]

    v1 = subtract_vectors(pt2, pt1)
    dot = dot_vectors(p_norm, v1)

    if fabs(dot) > tol:
        return True
    return False


def is_intersection_segment_plane(segment, plane, tol=1e-6):
    """Determine if a line segment intersects with a plane.

    Parameters
    ----------
    segment : tuple
        Two points defining the segment.
    plane : tuple
        The base point and normal defining the plane.
    tol : float, optional
        A tolerance for intersection verification.
        Default is ``1e-6``.

    Returns
    -------
    bool
        ``True`` if the segment intersects with the plane, ``False`` otherwise.
    """
    pt1 = segment[0]
    pt2 = segment[1]
    p_cent = plane[0]
    p_norm = plane[1]

    v1 = subtract_vectors(pt2, pt1)
    dot = dot_vectors(p_norm, v1)

    if fabs(dot) > tol:
        v2 = subtract_vectors(pt1, p_cent)
        fac = - dot_vectors(p_norm, v2) / dot
        if fac > 0. and fac < 1.:
            return True
        return False
    else:
        return False


def is_intersection_plane_plane(plane1, plane2, tol=1e-6):
    """Verifies if two planes intersect.

    Parameters
    ----------
    plane1 : tuple
        The base point and normal (normalized) defining the 1st plane.
    plane2 : tuple
        The base point and normal (normalized) defining the 2nd plane.
    tol : float, optional
        A tolerance for intersection verification.
        Default is ``1e-6``.

    Returns
    -------
    bool
        ``True`` if plane1 intersects with plane2.
        ``False`` otherwise.

    """
    # check for parallelity of planes
    if abs(dot_vectors(plane1[1], plane2[1])) > 1 - tol:
        return False
    return True


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import doctest
    doctest.testmod(globs=globals())
