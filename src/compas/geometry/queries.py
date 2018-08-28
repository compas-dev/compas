from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from math import pi
from math import fabs

from compas.geometry.basic import subtract_vectors
from compas.geometry.basic import cross_vectors
from compas.geometry.basic import dot_vectors
from compas.geometry.basic import normalize_vector

from compas.geometry.distance import distance_point_point
from compas.geometry.distance import distance_point_point_xy
from compas.geometry.distance import distance_point_plane
from compas.geometry.distance import distance_point_line
from compas.geometry.distance import distance_point_line_xy
from compas.geometry.distance import closest_point_on_segment
from compas.geometry.distance import closest_point_on_segment_xy

from compas.geometry.size import area_triangle

from compas.geometry.angles import angle_vectors
from compas.geometry.average import center_of_mass_polygon


__all__ = [
    'is_ccw_xy',
    'is_colinear',
    'is_colinear_xy',
    'is_coplanar',
    'is_polygon_convex',
    'is_polygon_convex_xy',
    'is_point_on_plane',
    'is_point_infront_plane',
    'is_point_on_line',
    'is_point_on_line_xy',
    'is_point_on_segment',
    'is_point_on_segment_xy',
    'is_point_on_polyline',
    'is_point_on_polyline_xy',
    'is_point_in_triangle',
    'is_point_in_triangle_xy',
    'is_point_in_polygon_xy',
    'is_point_in_convex_polygon_xy',
    'is_point_in_circle',
    'is_point_in_circle_xy',
    'is_intersection_line_line',
    'is_intersection_line_line_xy',
    'is_intersection_segment_segment',
    'is_intersection_segment_segment_xy',
    'is_intersection_line_triangle',
    'is_intersection_line_plane',
    'is_intersection_segment_plane',
    'is_intersection_plane_plane',
]


def is_ccw_xy(a, b, c, colinear=False):
    """Determine if c is on the left of ab when looking from a to b,
    and assuming that all points lie in the XY plane.

    Parameters
    ----------
    a : sequence of float
        XY(Z) coordinates of the base point.
    b : sequence of float
        XY(Z) coordinates of the first end point.
    c : sequence of float
        XY(Z) coordinates of the second end point.
    colinear : bool, optional
        Allow points to be colinear.
        Default is ``False``.

    Returns
    -------
    bool
        ``True`` if ccw.
        ``False`` otherwise.

    Notes
    -----
    For more info, see [1]_.

    References
    ----------
    .. [1] Marsh, C. *Computational Geometry in Python: From Theory to Application*.
           Available at: https://www.toptal.com/python/computational-geometry-in-python-from-theory-to-implementation

    Examples
    --------
    >>> print(is_ccw_xy([0,0,0], [0,1,0], [-1, 0, 0]))
    True

    >>> print(is_ccw_xy([0,0,0], [0,1,0], [+1, 0, 0]))
    False

    >>> print(is_ccw_xy([0,0,0], [1,0,0], [2,0,0]))
    False

    >>> print(is_ccw_xy([0,0,0], [1,0,0], [2,0,0], True))
    True

    """
    ab_x = b[0] - a[0]
    ab_y = b[1] - a[1]
    ac_x = c[0] - a[0]
    ac_y = c[1] - a[1]

    if colinear:
        return ab_x * ac_y - ab_y  * ac_x >= 0
    return ab_x * ac_y - ab_y  * ac_x > 0


def is_colinear(a, b, c):
    """Determine if three points are colinear.

    Parameters
    ----------
    a : tuple, list, Point
        Point 1.
    b : tuple, list, Point
        Point 2.
    c : tuple, list, Point
        Point 3.

    Returns
    -------
    bool
        ``True`` if the points are collinear
        ``False`` otherwise.

    """
    return area_triangle([a, b, c]) < 1e-9


def is_colinear_xy(a, b, c):
    """Determine if three points are colinear in the XY plane.

    Parameters
    ----------
    a : tuple, list, Point
        Point 1.
    b : tuple, list, Point
        Point 2.
    c : tuple, list, Point
        Point 3.

    Returns
    -------
    bool
        ``True`` if the points are collinear
        ``False`` otherwise.

    """
    ab_x = b[0] - a[0]
    ab_y = b[1] - a[1]
    ac_x = c[0] - a[0]
    ac_y = c[1] - a[1]

    return ab_x * ac_y == ab_y  * ac_x


def is_coplanar(points, tol=0.01):
    """Determine if the points are coplanar.

    Parameters
    ----------
    points : sequence
        A sequence of locations in three-dimensional space.

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

    u = subtract_vectors(points[1], points[0])
    v = subtract_vectors(points[2], points[1])
    w = cross_vectors(u, v)

    for i in range(1, len(points) - 2):
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

    See Also
    --------
    is_polygon_convex_xy

    """
    c = center_of_mass_polygon(polygon)

    for i in range(-1, len(polygon) - 1):
        p0 = polygon[i]
        p1 = polygon[i - 1]
        p2 = polygon[i + 1]
        v0 = subtract_vectors(c, p0)
        v1 = subtract_vectors(p1, p0)
        v2 = subtract_vectors(p2, p0)
        a1 = angle_vectors(v1, v0)
        a2 = angle_vectors(v0, v2)
        if a1 + a2 > pi:
            return False

    return True


def is_polygon_convex_xy(polygon, colinear=False):
    """Determine if the polygon is convex in the XY-plane.

    Parameters
    ----------
    polygon : list, tuple
        The XY(Z) coordinates of the corners of a polygon.
        The vertices are assumed to be in order.
        The polygon is assumed to be closed: the first and last vertex in the sequence should not be the same.
    colinear : bool
        Are points allowed to be colinear?

    Returns
    -------
    bool
        ``True`` if the figure is convex.
        ``False`` otherwise.

    """
    a = polygon[-2]
    b = polygon[-1]
    c = polygon[0]
    direction = is_ccw_xy(a, b, c, colinear)
    for i in range(-1, len(polygon) - 2):
        a = b
        b = c
        c = polygon[i + 2]
        if direction != is_ccw_xy(a, b, c, colinear):
            return False
    return True


def is_point_on_plane(point, plane, tol=0.0):
    """Determine if a point lies in a plane.

    Parameters
    ----------
    point : sequence of float
        XYZ coordinates.
    plane : tuple
        Base point and normal defining a plane.
    tol : float, optional
        A tolerance. Default is ``0.0``.

    Returns
    -------
    bool
        ``True`` if the point is in on the plane.
        ``False`` otherwise.

    """
    return distance_point_plane(point, plane) <= tol


def is_point_infront_plane(point, plane):
    """Determine if a point lies in front of a plane.

    Parameters
    ----------
    point : sequence of float
        XYZ coordinates.
    plane : tuple
        Base point and normal defining a plane.

    Returns
    -------
    bool
        ``True`` if the point is in front of the plane.
        ``False`` otherwise.

    """
    return dot_vectors(subtract_vectors(point, plane[0]), plane[1]) > 0.0



def is_point_on_line(point, line, tol=0.0):
    """Determine if a point lies on a line.

    Parameters
    ----------
    point : sequence of float
        XYZ coordinates.
    line : tuple
        Two points defining a line.
    tol : float, optional
        A tolerance. Default is ``0.0``.

    Returns
    -------
    bool
        ``True`` if the point is in on the line.
        ``False`` otherwise.

    """
    return distance_point_line(point, line) <= tol


def is_point_on_line_xy(point, line, tol=0.0):
    """Determine if a point lies on a line in the XY-plane.

    Parameters
    ----------
    point : sequence of float
        XY(Z) coordinates of a point.
    line : tuple
        XY(Z) coordinates of two points defining a line.
    tol : float, optional
        A tolerance.
        Default is ``0.0``.

    Returns
    -------
    bool
        ``True`` if the point is in on the line.
        ``False`` otherwise.

    """
    return distance_point_line_xy(point, line) <= tol


def is_point_on_segment(point, segment, tol=0.0):
    """Determine if a point lies on a given line segment.

    Parameters
    ----------
    point : sequence of float
        XYZ coordinates.
    segment : tuple
        Two points defining the line segment.

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


def is_point_on_segment_xy(point, segment, tol=0.0):
    """Determine if a point lies on a given line segment in the XY-plane.

    Parameters
    ----------
    point : sequence of float
        XY(Z) coordinates of a point.
    segment : tuple, list
        XY(Z) coordinates of two points defining a segment.

    Returns
    -------
    bool
        ``True`` if the point is on the line segment.
        ``False`` otherwise.

    """
    a, b = segment

    if not is_point_on_line_xy(point, segment, tol=tol):
        return False

    d_ab = distance_point_point_xy(a, b)

    if d_ab == 0:
        return False

    d_pa = distance_point_point_xy(a, point)
    d_pb = distance_point_point_xy(b, point)

    if d_pa + d_pb <= d_ab + tol:
        return True

    return False


# def is_closest_point_on_segment(point, segment, tol=0.0, return_point=False):
#     """Determine if the closest point on the line of a segment is on the segment.

#     Parameters
#     ----------
#     point : sequence of float
#         XYZ coordinates of the point.
#     segment : tuple
#         Two points defining the line segment.
#     tol : float, optional
#         A tolerance.
#         Default is ``0.0``.
#     return_point : bool, optional
#         If ``True`` return the closest point.
#         Default is ``False``.

#     Returns
#     -------
#     bool, tuple
#         XYZ coordinates of the point on the line.
#     bool
#         True if the point is in on the line, False otherwise.

#     """
#     a, b = segment
#     v = subtract_vectors(b, a)
#     d_ab = distance_point_point_sqrd(a, b)
#     if d_ab == 0:
#         return
#     u = sum((point[i] - a[i]) * v[i] for i in range(3)) / d_ab
#     c = a[0] + u * v[0], a[1] + u * v[1], a[2] + u * v[2]
#     d_ac = distance_point_point_sqrd(a, c)
#     d_bc = distance_point_point_sqrd(b, c)
#     if d_ac + d_bc <= d_ab + tol:
#         if return_point:
#             return c
#         return True
#     return False


def is_point_on_polyline(point, polyline, tol=0.0):
    """Determine if a point is on a polyline.

    Parameters
    ----------
    point : sequence of float
        XYZ coordinates.
    polyline : sequence of sequence of float
        XYZ coordinates of the points of the polyline.
    tol : float, optional
        The tolerance.
        Default is ``0.0``.

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


def is_point_on_polyline_xy(point, polyline, tol=0.0):
    """Determine if a point is on a polyline in the XY plane.

    Parameters
    ----------
    point : sequence of float
        XY(Z) coordinates.
    polyline : sequence of sequence of float
        XY(Z) coordinates of the points of the polyline.
    tol : float, optional
        The tolerance.
        Default is ``0.0``.

    Returns
    -------
    bool
        ``True`` if the point is on the polyline.
        ``False`` otherwise.

    """
    for i in range(len(polyline) - 1):
        a = polyline[i]
        b = polyline[i + 1]
        c = closest_point_on_segment_xy(point, (a, b))

        if distance_point_point_xy(point, c) <= tol:
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
        True if the point is in inside the triangle.
        False otherwise.

    Notes
    -----
    Should the point be in the same plane as the triangle?

    See Also
    --------
    is_point_in_triangle_xy

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


def is_point_in_triangle_xy(point, triangle, colinear=False):
    """Determine if a point is in the interior of a triangle lying in the XY-plane.

    Parameters
    ----------
    point : sequence of float
        XY(Z) coordinates of a point.
    triangle : sequence
        XY(Z) coordinates of the corners of the triangle.
    colinear : bool, optional
        Allow points to be colinear.
        Default is ``False``.

    Returns
    -------
    bool
        True if the point is in the convex polygon
        False otherwise.

    """
    a, b, c = triangle
    ccw = is_ccw_xy(c, a, point, colinear)

    if ccw != is_ccw_xy(a, b, point, colinear):
        return False

    if ccw != is_ccw_xy(b, c, point, colinear):
        return False

    return True


def is_point_in_convex_polygon_xy(point, polygon):
    """Determine if a point is in the interior of a convex polygon lying in the XY-plane.

    Parameters
    ----------
    point : sequence of float
        XY(Z) coordinates of a 2D or 3D point (Z will be ignored).
    polygon : sequence
        A sequence of XY(Z) coordinates of 2D or 3D points
        (Z will be ignored) representing the locations of the corners of a polygon.
        The vertices are assumed to be in order. The polygon is assumed to be closed:
        the first and last vertex in the sequence should not be the same.

    Returns
    -------
    bool
        True if the point is in the convex polygon, False otherwise.

    Warning
    -------
    Does not work for concave polygons.

    """
    ccw = None
    for i in range(-1, len(polygon) - 1):
        a = polygon[i]
        b = polygon[i + 1]
        if ccw is None:
            ccw = is_ccw_xy(a, b, point, True)
        else:
            if ccw != is_ccw_xy(a, b, point, True):
                return False
    return True


def is_point_in_polygon_xy(point, polygon):
    """Determine if a point is in the interior of a polygon lying in the XY-plane.

    Parameters:
        point (sequence of float): XY(Z) coordinates of a 2D or 3D point (Z will be ignored).
        polygon (sequence) : A sequence of XY(Z) coordinates of 2D or 3D points
        (Z will be ignored) representing the locations of the corners of a polygon.
        The vertices are assumed to be in order. The polygon is assumed to be closed:
        the first and last vertex in the sequence should not be the same.

    Warning:
        A boundary check is not yet implemented.
        This should include a tolerance value.

    Returns:
        bool: True if the point is in the polygon, False otherwise.
    """
    x, y = point[0], point[1]
    polygon = [(p[0], p[1]) for p in polygon]  # make 2D
    inside = False
    for i in range(-1, len(polygon) - 1):
        x1, y1 = polygon[i]
        x2, y2 = polygon[i + 1]
        if y > min(y1, y2):
            if y <= max(y1, y2):
                if x <= max(x1, x2):
                    if y1 != y2:
                        xinters = (y - y1) * (x2 - x1) / (y2 - y1) + x1
                    if x1 == x2 or x <= xinters:
                        inside = not inside
    return inside


def is_point_in_circle(point, circle):
    """Determine if a point lies in a circle.

    Parameters:
        point (sequence of float): XYZ coordinates of a 3D point.
        circle (tuple): center, radius, normal

    Returns:
        (bool): True if the point lies in the circle, False otherwise.

    """
    center, radius, normal = circle
    if is_point_on_plane(point, (center, normal)):
        return distance_point_point(point, center) <= radius
    return False


def is_point_in_circle_xy(point, circle):
    """Determine if a point lies in a circle lying in the XY plane.

    Parameters:
        point (sequence of float): XY(Z) coordinates of a 2D or 3D point (Z will be ignored).
        circle (tuple): center, radius of the circle in the xy plane.

    Returns:
        (bool): True if the point lies in the circle, False otherwise.

    """
    dis = distance_point_point_xy(point, circle[0])
    if dis <= circle[1]:
        return True
    return False


# ==============================================================================
# intersections
# ==============================================================================


def is_intersection_line_line(l1, l2, epsilon=1e-6):
    """Verifies if two lines intersection in one point.

    Parameters:
        ab: (tuple): A sequence of XYZ coordinates of two 3D points representing
            two points on the line.
        cd: (tuple): A sequence of XYZ coordinates of two 3D points representing
            two points on the line.

    Returns:
        True (bool): if the lines intersect in one point, False is the lines are
        skew, parallel or lie on top of each other.
    """
    a, b = l1
    c, d = l2

    e1 = normalize_vector(subtract_vectors(b, a))
    e2 = normalize_vector(subtract_vectors(d, c))

    # check for parallel lines
    if abs(dot_vectors(e1, e2)) > 1.0 - epsilon:
        return False

    # check for intersection
    d_vector = cross_vectors(e1, e2)
    if dot_vectors(d_vector, subtract_vectors(c, a)) == 0:
        return True

    return False


def is_intersection_line_line_xy(l1, l2):
    """Determine if two lines intersect in 2d lying in the XY plane.

    Parameters:
        l1 (tuple):
        l2 (tuple):

    Returns:
        (bool): True if there is a intersection, False otherwise.

    """
    raise NotImplementedError


def is_intersection_segment_segment():
    raise NotImplementedError


def is_intersection_segment_segment_xy(ab, cd):
    """Determine if two the segments ab and cd intersect?

    Two segments a-b and c-d intersect, if both of the following conditions are true:

        * c is on the left of ab, and d is on the right, or vice versa
        * d is on the left of ac, and on the right of bc, or vice versa

    Parameters:
        ab: (tuple): A sequence of XY(Z) coordinates of two 2D or 3D points
        (Z will be ignored) representing the start and end points of a line segment.
        cd: (tuple): A sequence of XY(Z) coordinates of two 2D or 3D points
        (Z will be ignored) representing the start and end points of a line segment.

    Returns:
        bool: ``True`` if the segments intersect, ``False`` otherwise.

    """
    a, b = ab
    c, d = cd
    return is_ccw_xy(a, c, d) != is_ccw_xy(b, c, d) and is_ccw_xy(a, b, c) != is_ccw_xy(a, b, d)


def is_intersection_line_triangle(line, triangle, epsilon=1e-6):
    """Verifies if a line (ray) intersects with a triangle.

    Notes
    -----
    Based on the Moeller Trumbore intersection algorithm.
    The line is treated as continues, directed ray and not as line segment with a start and end point

    Parameters
    ----------
    line : tuple
        Two points defining the line.
    triangle : sequence of sequence of float
        XYZ coordinates of the triangle corners.

    Returns
    -------
    bool
        True if the line (ray) intersects with the triangle, False otherwise.

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
    if det > - epsilon and det < epsilon:
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
    if v < 0.0 or u + v  > 1.0:
        return False

    t = dot_vectors(e2, q) * inv_det

    if t > epsilon:
        return True

    # No hit
    return False


def is_intersection_line_plane(line, plane, epsilon=1e-6):
    """Determine if a line (continuous ray) intersects with a plane.

    Parameters:
        line (tuple): Two points defining the line.
        plane (tuple): The base point and normal defining the plane.
    Returns:
        (bool): True if the line intersects with the plane, False otherwise.

    """
    pt1 = line[0]
    pt2 = line[1]
    p_norm = plane[1]

    v1 = subtract_vectors(pt2, pt1)
    dot = dot_vectors(p_norm, v1)

    if fabs(dot) > epsilon:
        return True
    return False


def is_intersection_segment_plane(segment, plane, epsilon=1e-6):
    """Determine if a line segment intersects with a plane.

    Parameters:
        segment (tuple): Two points defining the line segment.
        plane (tuple): The base point and normal defining the plane.
    Returns:
        (bool): True if the line segment intersects with the plane, False otherwise.

    """
    pt1 = segment[0]
    pt2 = segment[1]
    p_cent = plane[0]
    p_norm = plane[1]

    v1 = subtract_vectors(pt2, pt1)
    dot = dot_vectors(p_norm, v1)

    if fabs(dot) > epsilon:
        v2 = subtract_vectors(pt1, p_cent)
        fac = - dot_vectors(p_norm, v2) / dot
        if fac > 0. and fac < 1.:
            return True
        return False
    else:
        return False


def is_intersection_plane_plane(plane1, plane2, epsilon=1e-6):
    """Computes the intersection of two planes

    Parameters:
        plane1 (tuple): The base point and normal (normalized) defining the 1st plane.
        plane2 (tuple): The base point and normal (normalized) defining the 2nd plane.
    Returns:
        (bool): True if the planes intersect, False otherwise.

    """
    # check for parallelity of planes
    if abs(dot_vectors(plane1[1], plane2[1])) > 1 - epsilon:
        return False
    return True





# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
