from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.tolerance import TOL

from compas.utilities import window

from compas.geometry import subtract_vectors
from compas.geometry import cross_vectors
from compas.geometry import dot_vectors
from compas.geometry import centroid_points
from compas.geometry import normal_polygon
from compas.geometry import length_vector

from compas.geometry import distance_point_point
from compas.geometry import distance_point_plane
from compas.geometry import distance_point_line
from compas.geometry import closest_point_on_segment


# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# Colinear, Coplanar
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================

def is_colinear(a, b, c, tol=None):
    """Determine if three points are colinear.

    Parameters
    ----------
    a : [float, float, float] | :class:`compas.geometry.Point`
        Point 1.
    b : [float, float, float] | :class:`compas.geometry.Point`
        Point 2.
    c : [float, float, float] | :class:`compas.geometry.Point`
        Point 3.
    tol : float, optional
        Tolerance for comparing the area of the triangle formed by the three points to zero.
        Default is :attr:`TOL.absolute`.

    Returns
    -------
    bool
        True if the points are colinear.
        False otherwise.

    See Also
    --------
    is_colinear_line_line

    """
    return TOL.is_zero(area_triangle([a, b, c]), tol)


def is_colinear_line_line(line1, line2, tol=None):
    """Determine if two lines are colinear.

    Parameters
    ----------
    line1 : [point, point] | :class:`compas.geometry.Line`
        Line 1.
    line2 : [point, point] | :class:`compas.geometry.Line`
        Line 2.
    tol : float, optional
        Tolerance for colinearity verification used by this function.
        Default is :attr:`TOL.absolute`.

    Returns
    -------
    bool
        True if the lines are colinear.
        False otherwise.

    See Also
    --------
    is_colinear

    """
    a, b = line1
    c, d = line2
    return is_colinear(a, b, c, tol) and is_colinear(a, b, d, tol)


def is_parallel_vector_vector(u, v, tol=None):
    """Determine if two vectors are parallel.

    Parameters
    ----------
    u : [float, float, float] | :class:`~compas.geometry.Vector`
        Vector 1.
    v : [float, float, float] | :class:`~compas.geometry.Vector`
        Vector 2.
    tol : float, optional
        Tolerance for comparing the length of the cross product of the two vectors to zero.
        Default is :attr:`TOL.absolute`.

    Returns
    -------
    bool
        True if the vectors are parallel.
        False otherwise.

    See Also
    --------
    is_parallel_line_line
    is_parallel_plane_plane

    Notes
    -----
    The length of the cross product of two vectors is equal to the area of the parallelogram formed by the two vectors.
    If the vectors are parallel, the area of the parallelogram is zero.

    Therefore, this predicate is based on the comparison of the length of the cross product of the two vectors to zero,
    and not on the comparison to zero of the actual angle between the two vectors.

    """
    # Lv = length_vector(v)
    # V = scale_vector(v, 1 / Lv)
    # sinus = length_vector(scale_vector(subtract_vectors(scale_vector(V, dot_vectors(u, V)), u), Lv))
    # # for small angles, the sinus is equal to the angle in radians
    # # for larger angles, it doesn't matter :)
    # return TOL.is_angle_zero(sinus, tol)
    return TOL.is_zero(length_vector(cross_vectors(u, v)), tol)


def is_parallel_line_line(line1, line2, tol=None):
    """Determine if two lines are parallel.

    Parameters
    ----------
    line1 : [point, point] | :class:`compas.geometry.Line`
        Line 1.
    line2 : [point, point] | :class:`compas.geometry.Line`
        Line 2.
    tol : float, optional
        Tolerance for comparing the length of the cross product of the direction vectors of the two lines to zero.
        Default is :attr:`TOL.absolute`.

    Returns
    -------
    bool
        True if the lines are colinear.
        False otherwise.

    See Also
    --------
    is_parallel_vector_vector
    is_parallel_plane_plane

    """
    a, b = line1
    c, d = line2
    ab = subtract_vectors(b, a)
    cd = subtract_vectors(d, c)
    return is_parallel_vector_vector(ab, cd, tol)


def is_parallel_plane_plane(plane1, plane2, tol=None):
    """Determine if two planes are parallel.

    Parameters
    ----------
    plane1 : [point, vector] | :class:`~compas.geometry.Plane`
        Plane 1.
    plane2 : [point, vector] | :class:`~compas.geometry.Plane`
        Plane 2.
    tol : float, optional
        Tolerance for comparing the length of the cross product of the normal vectors of the two planes to zero.
        Default is :attr:`TOL.absolute`.

    Returns
    -------
    bool
        True if the planes are parallel.
        False otherwise.

    See Also
    --------
    is_parallel_vector_vector
    is_parallel_line_line

    """
    return is_parallel_vector_vector(plane1[1], plane2[1], tol)


def is_perpendicular_vector_vector(u, v, tol=None):
    """Determine if two vectors are perpendicular.

    Parameters
    ----------
    u : [float, float, float] | :class:`~compas.geometry.Vector`
        Vector 1.
    v : [float, float, float] | :class:`~compas.geometry.Vector`
        Vector 2.
    tol : float, optional
        Tolerance for comparing the dot product of the two vectors to zero.
        Default is :attr:`TOL.absolute`.

    Returns
    -------
    bool
        True if the vectors are perpendicular.
        False otherwise.

    See Also
    --------
    is_perpendicular_line_line
    is_perpendicular_plane_plane

    Notes
    -----
    The dot product of two vectors is equal to the product of the lengths of the two vectors and the cosine of the angle between the two vectors.
    If the vectors are perpendicular, the cosine of the angle between the two vectors is zero.

    Therefore, this predicate is based on the comparison of the dot product of the two vectors to zero,
    and not on the comparison to zero of the actual angle between the two vectors.

    """
    return TOL.is_zero(dot_vectors(u, v), tol)


def is_perpendicular_line_line(line1, line2, tol=None):
    """Determine if two lines are perpendicular.

    Parameters
    ----------
    line1 : [point, point] | :class:`~compas.geometry.Line`
        Line 1.
    line2 : [point, point] | :class:`~compas.geometry.Line`
        Line 2.
    tol : float, optional
        Tolerance for verifying the perpendicularity of the direction vectors of the two lines.
        Default is :attr:`TOL.absolute`.

    Returns
    -------
    bool
        True if the lines are perpendicular.
        False otherwise.

    See Also
    --------
    is_perpendicular_vector_vector
    is_perpendicular_plane_plane

    """
    a, b = line1
    c, d = line2
    ab = subtract_vectors(b, a)
    cd = subtract_vectors(d, c)
    return is_perpendicular_vector_vector(ab, cd, tol)


def is_perpendicular_plane_plane(plane1, plane2, tol=None):
    """Determine if two planes are perpendicular.

    Parameters
    ----------
    plane1 : [point, vector] | :class:`~compas.geometry.Plane`
        Plane 1.
    plane2 : [point, vector] | :class:`~compas.geometry.Plane`
        Plane 2.
    tol : float, optional
        Tolerance for verifying the perpendicularity of the normal vectors of the two planes.
        Default is :attr:`TOL.absolute`.

    Returns
    -------
    bool
        True if the planes are perpendicular.
        False otherwise.

    See Also
    --------
    is_perpendicular_vector_vector
    is_perpendicular_line_line

    """
    return is_perpendicular_vector_vector(plane1[1], plane2[1], tol)


def is_coplanar(points, tol=None):
    """Determine if the points are coplanar.

    Parameters
    ----------
    plane1 : [point, vector] | :class:`compas.geometry.Plane`
        Plane 1.
    plane2 : [point, vector] | :class:`compas.geometry.Plane`
        Plane 2.
    tol : float, optional
        Tolerance for verifying the perpendicularity of the normal of a plane through three of the points with the vectors formed by the other points.
        Default is :attr:`TOL.absolute`.

    Returns
    -------
    bool
        True if the planes are parallel.
        False otherwise.

    Notes
    -----
    Compute the normal vector (cross product) of the vectors formed by the first three points.
    Taking the firs tpoint as base point, include one more vector at a time and check if that vector is perpendicular to the normal vector.
    If all vectors are perpendicular, the points are coplanar.

    See Also
    --------
    is_colinear


def is_perpendicular_vector_vector(u, v, tol=1e-6):
    """Determine if two vectors are perpendicular.

    Parameters
    ----------
    u : [float, float, float] | :class:`compas.geometry.Vector`
        Vector 1.
    v : [float, float, float] | :class:`compas.geometry.Vector`
        Vector 2.
    tol : float, optional
        A tolerance for comparing the dot product of the two vectors to zero.

    Returns
    -------
    bool
        True if the vectors are perpendicular.
        False otherwise.

    See Also
    --------
    is_perpendicular_line_line
    is_perpendicular_plane_plane
    is_parallel_vector_vector

    """
    return abs(dot_vectors(u, v)) < tol

    temp = points[:]

    while True:
        a = temp.pop(0)
        b = temp.pop(0)
        c = temp.pop(0)
        if not is_colinear(a, b, c, tol):
            break
        if not temp:
            return True

    n = cross_vectors(subtract_vectors(b, a), subtract_vectors(c, a))

    return all(is_perpendicular_vector_vector(n, subtract_vectors(d, a), tol) for d in temp)


def is_polygon_convex(polygon):
    """Determine if a polygon is convex.

    Parameters
    ----------
    polygon : sequence[point] | :class:`compas.geometry.Polygon`
        A polygon.

    Returns
    -------
    bool
        True if the polygon is convex.
        False otherwise.

    See Also
    --------
    is_polyhedron_convex

    Notes
    -----
    Use this function for *spatial* polygons.
    If the polygon is in a horizontal plane, use :func:`compas.geometry.is_polygon_convex_xy` instead.

    See Also
    --------
    compas.geometry.is_polygon_convex_xy

    Examples
    --------
    >>> polygon = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.4, 0.4, 0.0], [0.0, 1.0, 0.0]]
    >>> is_polygon_convex(polygon)
    False

    """
    if len(polygon) == 3:
        return True

    temp = polygon[:]

    while True:
        a = temp.pop(0)
        o = temp.pop(0)
        b = temp.pop(0)
        if not is_colinear(a, o, b):
            break
        if not temp:
            return True

    oa = subtract_vectors(a, o)
    ob = subtract_vectors(b, o)
    n0 = cross_vectors(oa, ob)

    for a, o, b in window(temp + temp[:2], 3):
        oa = subtract_vectors(a, o)
        ob = subtract_vectors(b, o)
        n = cross_vectors(oa, ob)
        if dot_vectors(n, n0) < 0:
            return False
    return True


def is_point_on_plane(point, plane, tol=None):
    """Determine if a point lies on a plane.

    Parameters
    ----------
    point : [float, float, float] | :class:`~compas.geometry.Point`
        A point.
    plane : [point, vector] | :class:`~compas.geometry.Plane`
        A plane.
    tol : float, optional
        Tolerance for comparing the distance between the point and the plane to zero.
        Default is :attr:`TOL.absolute`.

    Returns
    -------
    bool
        True if the polyhedron is convex.
        False otherwise.

    """
    return TOL.is_zero(distance_point_plane(point, plane), tol)


def is_point_infront_plane(point, plane, tol=None):
    """Determine if a point lies in front of a plane.

    Parameters
    ----------
    point : [float, float, float] | :class:`~compas.geometry.Point`
        A point.
    plane : [point, vector] | :class:`~compas.geometry.Plane`
        A plane.
    tol : float, optional
        Tolerance for verifying that the dot product of the vector from the plane origin to the point and the plane normal is positive.
        Default is :attr:`TOL.absolute`.

    Returns
    -------
    bool
        True if the point is in front of the plane.
        False otherwise.

    """
    return TOL.is_positive(dot_vectors(subtract_vectors(point, plane[0]), plane[1]), tol)


# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# Containment (Plane)
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================


def is_point_behind_plane(point, plane, tol=None):
    """Determine if a point lies behind a plane.

    Parameters
    ----------
    point : [float, float, float] | :class:`compas.geometry.Point`
        A point.
    plane : [point, vector] | :class:`compas.geometry.Plane`
        A plane.
    tol : float, optional
        Tolerance for verifying that the dot product of the vector from the plane origin to the point and the plane normal is negative.
        Default is :attr:`TOL.absolute`.

    Returns
    -------
    bool
        True if the point is in on the plane.
        False otherwise.

    """
    return TOL.is_negative(dot_vectors(subtract_vectors(point, plane[0]), plane[1]), tol)


def is_point_on_line(point, line, tol=None):
    """Determine if a point lies on a line.

    Parameters
    ----------
    point : [float, float, float] | :class:`compas.geometry.Point`
        A point.
    line : [point, point] | :class:`compas.geometry.Line`
        A line.
    tol : float, optional
        Tolerance for comparing the distance between the point and the line to zero.
        Default is :attr:`TOL.absolute`.

    Returns
    -------
    bool
        True if the point is in on the line.
        False otherwise.

    """
    return TOL.is_zero(distance_point_line(point, line), tol)


def is_point_on_segment(point, segment, tol=None):
    """Determine if a point lies on a given line segment.

    Parameters
    ----------
    point : [float, float, float] | :class:`compas.geometry.Point`
        A point.
    segment : [point, point] | :class:`compas.geometry.Line`
        A line segment.
    tol : float, optional
        Tolerance for comparing the distance between the point and the line segment to zero.
        Default is :attr:`TOL.absolute`.

    Returns
    -------
    bool
        True if the point is on the line segment.
        False otherwise.

    """
    a, b = segment

    d_ab = distance_point_point(a, b)
    if d_ab == 0:
        return False

    if not is_point_on_line(point, (a, b), tol=tol):
        return False

    d_pa = distance_point_point(a, point)
    d_pb = distance_point_point(b, point)

    if TOL.is_close(d_pa + d_pb, d_ab, rtol=0, atol=tol):
        return True
    return False


def is_point_on_polyline(point, polyline, tol=None):
    """Determine if a point is on a polyline.

    Parameters
    ----------
    point : [float, float, float] | :class:`compas.geometry.Point`
        A point.
    polyline : sequence[point] | :class:`compas.geometry.Polyline`
        A polyline.
    tol : float, optional
        Tolerance for comparing the distance between the point and the polyline to zero.
        Default is :attr:`TOL.absolute`.

    Returns
    -------
    bool
        True if the point is on the polyline.
        False otherwise.

    """
    for i in range(len(polyline) - 1):
        a = polyline[i]
        b = polyline[i + 1]
        c = closest_point_on_segment(point, (a, b))

        if TOL.is_zero(distance_point_point(point, c), tol):
            return True

    return False


def is_point_on_circle(point, circle, tol=1e-6):
    """Determine if a point lies on a circle.

    Parameters
    ----------
    point : [float, float, float] | :class:`compas.geometry.Point`
        A point.
    circle : [plane, float]
        A circle.
    tol : float, optional
        A tolerance for membership verification.

    Returns
    -------
    bool
        True if the point lies on the circle.
        False otherwise.

    """
    plane, radius = circle
    if is_point_on_plane(point, plane):
        return abs(distance_point_point(point, plane[0]) - radius) <= tol
    return False


# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# Containment (Surfaces)
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================


# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# Containment (Shapes)
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================


def is_point_in_circle(point, circle, tol=1e-6):
    """Determine if a point lies in a circle.

    Parameters
    ----------
    point : [float, float, float] | :class:`compas.geometry.Point`
        A point.
    circle : [plane, float]
        A circle.

    Returns
    -------
    bool
        True if the point lies in the circle.
        False otherwise.

    """
    plane, radius = circle
    if is_point_on_plane(point, plane, tol=tol):
        return distance_point_point(point, plane[0]) <= radius
    return False


def is_intersection_line_line(l1, l2, tol=None):
    """Verifies if two lines intersect.

    Parameters
    ----------
    l1 : [point, point] | :class:`~compas.geometry.Line`
        A line.
    l2 : [point, point] | :class:`~compas.geometry.Line`
        A line.
    tol : float, optional
        Tolerance for veryfing that the lines are not parallel, and for comparing the distance between the lines to zero.
        Default is :attr:`TOL.absolute`.

    Returns
    -------
    bool
        True if the point is in inside the triangle.
        False otherwise.

    See Also
    --------
    is_parallel_line_line
    is_intersection_line_triangle
    is_intersection_line_plane

    """

    e1 = normalize_vector(subtract_vectors(b, a))
    e2 = normalize_vector(subtract_vectors(d, c))

    # check for parallel lines
    if is_parallel_vector_vector(e1, e2, tol):
        return False

    # check for intersection
    return TOL.is_zero(dot_vectors(cross_vectors(e1, e2), subtract_vectors(c, a)), tol)


def is_intersection_segment_segment(s1, s2, tol=None):
    """Verifies if two segments intersect.

    Parameters
    ----------
    point : [float, float, float] | :class:`compas.geometry.Point`
        A point.
    polygon : sequence[point] | :class:`compas.geometry.Polygon`
        A polygon.

    Returns
    -------
    bool
        True if the point is in inside the polygon.
        False otherwise.

    """
    raise NotImplementedError


def is_intersection_line_triangle(line, triangle, tol=None):
    """Verifies if a line (ray) intersects with a triangle.


def is_point_in_sphere(point, sphere, tol=1e-6):
    """Determine if a point lies in a sphere.

    Parameters
    ----------
    line : [point, point] | :class:`~compas.geometry.Line`
        A line.
    triangle : [point, point, point]
        A triangle.
    tol : float, optional
        Tolerance for comparing the dot product of the direction vector of the ray and the normal vector of the plane of the triangle to zero.
        Default is :attr:`TOL.absolute`.

    Returns
    -------
    bool
        True if the point lies in the sphere.
        False otherwise.

    """
    a, b, c = triangle

    o = line[0]

    d = subtract_vectors(line[1], line[0])  # coulmn 0
    e1 = subtract_vectors(b, a)  # column 1
    e2 = subtract_vectors(c, a)  # column 2

    # det([A B C]) = -1 * dot(cross(A, C), B) = -1 * dot(cross(C, B), A)

    # cross column 0 and column 2
    d_e2 = cross_vectors(d, e2)
    # dot column 1 with cross of columns 0 and 2
    det = dot_vectors(e1, d_e2)

    if TOL.is_zero(det, tol):
        return False

    ao = subtract_vectors(o, a)  # substitution column
    inv_det = 1.0 / det

    # substitute ao for column 1 of the matrix
    # compute the determinant of the new matrix
    det_Au = dot_vectors(ao, d_e2)
    u = det_Au * inv_det  # barycentric coordinate 1
    if u < 0.0 or u > 1.0:
        return False

    # substitute ao for column 2 of the matrix
    # compute the determinant of the new matrix
    d_ao = cross_vectors(d, ao)
    det_Av = dot_vectors(e1, d_ao)
    v = det_Av * inv_det  # barycentric coordinate 2
    if v < 0.0 or u + v > 1.0:
        return False

    # t = dot_vectors(e2, ap_x_e1) * inv_det  # distance from ray origin to intersection
    # return TOL.is_positive(t, tol)
    return True


def is_intersection_ray_triangle(ray, triangle, tol=None):
    """Verifies if a ray intersects with a triangle.

    Parameters
    ----------
    ray : [point, point] | :class:`~compas.geometry.Line`
        A ray.
    triangle : [point, point, point]
        A triangle.
    tol : float, optional
        Tolerance for comparing the dot product of the direction vector of the ray and the normal vector of the plane of the triangle to zero,
        and for veryfing that the parameter t is a strictly positive number.
        Default is :attr:`TOL.absolute`.

    Returns
    -------
    bool
        True if the ray intersects with the triangle.
        False otherwise.

    Notes
    -----
    Based on the Moeller Trumbore intersection algorithm.
    The ray is treated as a line segment with a start and end point.

    Examples
    --------
    >>>

    """
    a, b, c = triangle

    o = ray[0]
    d = subtract_vectors(ray[1], ray[0])  # coulmn 0
    e1 = subtract_vectors(b, a)  # column 1
    e2 = subtract_vectors(c, a)  # column 2

    # det([A B C]) = -1 * dot(cross(A, C), B) = -1 * dot(cross(C, B), A)

    # cross column 0 and column 2
    d_e2 = cross_vectors(d, e2)
    # dot column 1 with cross of columns 0 and 2
    det = dot_vectors(e1, d_e2)

    if TOL.is_zero(det, tol):
        return False

    ao = subtract_vectors(o, a)  # substitution column
    inv_det = 1.0 / det

    # substitute ao for column 1 of the matrix
    # compute the determinant of the new matrix
    det_Au = dot_vectors(ao, d_e2)
    u = det_Au * inv_det  # barycentric coordinate 1
    if u < 0.0 or u > 1.0:
        return False

    # substitute ao for column 2 of the matrix
    # compute the determinant of the new matrix
    d_ao = cross_vectors(d, ao)
    det_Av = dot_vectors(e1, d_ao)
    # ao_x_e1 = cross_vectors(ao, e1)
    # det_Av = dot_vectors(d, ao_x_e1)
    v = det_Av * inv_det  # barycentric coordinate 2
    if v < 0.0 or u + v > 1.0:
        return False

    # substitute ao for column 0 of the matrix
    # compute the determinant of the new matrix
    ao_e2 = cross_vectors(ao, e2)
    det_At = dot_vectors(e1, ao_e2)
    t = det_At * inv_det  # distance from ray origin to intersection

    return TOL.is_positive(t, tol)


def is_intersection_line_plane(line, plane, tol=None):
    """Determine if a line (ray) intersects with a plane.

    Parameters
    ----------
    line : [point, point] | :class:`~compas.geometry.Line`
        A line.
    plane : [point, vector] | :class:`~compas.geometry.Plane`
        A plane.
    tol : float, optional
        Tolerance for comparing the dot product of the direction vector of the line and the normal vector of the plane to zero.
        Default is :attr:`TOL.absolute`.

    Returns
    -------
    bool
        True, if the point lies in the polyhedron.
        False, otherwise.

    """
    vertices, faces = polyhedron
    polygons = [[vertices[index] for index in face] for face in faces]
    planes = [[centroid_points(polygon), normal_polygon(polygon)] for polygon in polygons]
    return all(is_point_behind_plane(point, plane) for plane in planes)


    return not TOL.is_zero(dot, tol)


def is_intersection_segment_plane(segment, plane, tol=None):
    """Determine if a line segment intersects with a plane.

    Parameters
    ----------
    point : [float, float, float] | :class:`compas.geometry.Point`
        A point.
    plane : [point, vector] | :class:`compas.geometry.Plane`
        A plane.
    tol : float, optional
        Tolerance for comparing the dot product of the direction vector of the line segment and the normal vector of the plane to zero.
        Default is :attr:`TOL.absolute`.

    Returns
    -------
    bool
        True if the point is in front of the plane.
        False otherwise.

    """
    return dot_vectors(subtract_vectors(point, plane[0]), plane[1]) > tol


    if TOL.is_zero(dot, tol):
        return False

    v2 = subtract_vectors(pt1, p_cent)
    fac = -dot_vectors(p_norm, v2) / dot
    if fac > 0.0 and fac < 1.0:
        return True
    return False


def is_intersection_plane_plane(plane1, plane2, tol=None):
    """Verifies if two planes intersect.

    Parameters
    ----------
    point : [float, float, float] | :class:`compas.geometry.Point`
        A point.
    plane : [point,  normal] | :class:`compas.geometry.Plane`
        A plane.
    tol : float, optional
        Tolerance for veryfing that the planes are not parallel.
        Default is :attr:`TOL.absolute`.

    Returns
    -------
    bool
        True if the point is in front of the plane.
        False otherwise.

    See Also
    --------
    is_parallel_plane_plane
    is_parallel_vector_vector

    """
    n1 = plane1[1]
    n2 = plane2[1]
    return not is_parallel_vector_vector(n1, n2, tol)


# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# Deprecated
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================


# def is_intersection_line_line(l1, l2, tol=1e-6):
#     """Verifies if two lines intersect.

#     Parameters
#     ----------
#     l1 : [point, point] | :class:`compas.geometry.Line`
#         A line.
#     l2 : [point, point] | :class:`compas.geometry.Line`
#         A line.
#     tol : float, optional
#         A tolerance for intersection verification.

#     Returns
#     -------
#     bool
#         True if the lines intersect in one point.
#         False if the lines are skew, parallel or lie on top of each other.

#     """
#     a, b = l1
#     c, d = l2

#     e1 = normalize_vector(subtract_vectors(b, a))
#     e2 = normalize_vector(subtract_vectors(d, c))

#     # check for parallel lines
#     if abs(dot_vectors(e1, e2)) > 1.0 - tol:
#         return False

#     # check for intersection
#     if abs(dot_vectors(cross_vectors(e1, e2), subtract_vectors(c, a))) < tol:
#         return True
#     return False


# def is_intersection_segment_segment(s1, s2, tol=1e-6):
#     """Verifies if two segments intersect.

#     Parameters
#     ----------
#     s1 : [point, point] | :class:`compas.geometry.Line`
#         A line segment.
#     s2 : [point, point] | :class:`compas.geometry.Line`
#         A line segment.
#     tol : float, optional
#         A tolerance for intersection verification.

#     Returns
#     -------
#     bool
#         True if the segments intersect in one point.
#         False if the segments are skew, parallel or lie on top of each other.

#     """
#     raise NotImplementedError


# def is_intersection_line_triangle(line, triangle, tol=1e-6):
#     """Verifies if a line (ray) intersects with a triangle.

#     Parameters
#     ----------
#     line : [point, point] | :class:`compas.geometry.Line`
#         A line.
#     triangle : [point, point, point]
#         A triangle.
#     tol : float, optional
#         A tolerance for intersection verification.

#     Returns
#     -------
#     bool
#         True if the line (ray) intersects with the triangle.
#         False otherwise.

#     Notes
#     -----
#     Based on the Moeller Trumbore intersection algorithm.
#     The line is treated as continues, directed ray and not as line segment with a start and end point

#     Examples
#     --------
#     >>>

#     """
#     a, b, c = triangle
#     # direction vector and base point of line
#     v1 = subtract_vectors(line[1], line[0])
#     p1 = line[0]
#     # Find vectors for two edges sharing triangle vertex 1
#     e1 = subtract_vectors(b, a)
#     e2 = subtract_vectors(c, a)
#     # Begin calculating determinant - also used to calculate u parameter
#     p = cross_vectors(v1, e2)
#     # if determinant is near zero, ray lies in plane of triangle
#     det = dot_vectors(e1, p)

#     # NOT CULLING
#     if det > -tol and det < tol:
#         return False

#     inv_det = 1.0 / det
#     # calculate distance from V1 to ray origin
#     t = subtract_vectors(p1, a)
#     # Calculate u parameter and make_blocks bound
#     u = dot_vectors(t, p) * inv_det

#     # The intersection lies outside of the triangle
#     if u < 0.0 or u > 1.0:
#         return False

#     # Prepare to make_blocks v parameter
#     q = cross_vectors(t, e1)
#     # Calculate V parameter and make_blocks bound
#     v = dot_vectors(v1, q) * inv_det

#     # The intersection lies outside of the triangle
#     if v < 0.0 or u + v > 1.0:
#         return False

#     t = dot_vectors(e2, q) * inv_det

#     if t > tol:
#         return True
#     # No hit
#     return False


# def is_intersection_line_plane(line, plane, tol=1e-6):
#     """Determine if a line (ray) intersects with a plane.

#     Parameters
#     ----------
#     line : [point, point] | :class:`compas.geometry.Line`
#         A line.
#     plane : [point, vector] | :class:`compas.geometry.Plane`
#         A plane.
#     tol : float, optional
#         A tolerance for intersection verification.

#     Returns
#     -------
#     bool
#         True if the line intersects with the plane.
#         False otherwise.

#     """
#     pt1 = line[0]
#     pt2 = line[1]
#     p_norm = plane[1]

#     v1 = subtract_vectors(pt2, pt1)
#     dot = dot_vectors(p_norm, v1)

#     if fabs(dot) > tol:
#         return True
#     return False


# def is_intersection_segment_plane(segment, plane, tol=1e-6):
#     """Determine if a line segment intersects with a plane.

#     Parameters
#     ----------
#     segment : [point, point] | :class:`compas.geometry.Line`
#         A line segment.
#     plane : [point, vector] | :class:`compas.geometry.Plane`
#         A plane.
#     tol : float, optional
#         A tolerance for intersection verification.

#     Returns
#     -------
#     bool
#         True if the segment intersects with the plane.
#         False otherwise.

#     """
#     pt1 = segment[0]
#     pt2 = segment[1]
#     p_cent = plane[0]
#     p_norm = plane[1]

#     v1 = subtract_vectors(pt2, pt1)
#     dot = dot_vectors(p_norm, v1)

#     if fabs(dot) > tol:
#         v2 = subtract_vectors(pt1, p_cent)
#         fac = -dot_vectors(p_norm, v2) / dot
#         if fac > 0.0 and fac < 1.0:
#             return True
#         return False
#     else:
#         return False


# def is_intersection_plane_plane(plane1, plane2, tol=1e-6):
#     """Verifies if two planes intersect.

#     Parameters
#     ----------
#     plane1 : [point, vector] | :class:`compas.geometry.Plane`
#         A plane.
#     plane2 : [point, vector] | :class:`compas.geometry.Plane`
#         A plane.
#     tol : float, optional
#         A tolerance for intersection verification.

#     Returns
#     -------
#     bool
#         True if plane1 intersects with plane2.
#         False otherwise.

#     """
#     # check for parallelity of planes
#     if abs(dot_vectors(plane1[1], plane2[1])) > 1 - tol:
#         return False
#     return True
