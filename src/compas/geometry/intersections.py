from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from math import fabs
from math import sqrt

from compas.utilities import pairwise

from compas.geometry.basic import add_vectors
from compas.geometry.basic import subtract_vectors
from compas.geometry.basic import scale_vector
from compas.geometry.basic import cross_vectors
from compas.geometry.basic import dot_vectors
from compas.geometry.basic import length_vector_xy
from compas.geometry.basic import subtract_vectors_xy
from compas.geometry.basic import normalize_vector

from compas.geometry.distance import distance_point_point

from compas.geometry.queries import is_point_on_segment
from compas.geometry.queries import is_point_on_segment_xy
from compas.geometry.queries import is_point_in_triangle


__all__ = [
    'intersection_line_line',
    'intersection_line_line_xy',
    'intersection_segment_segment',
    'intersection_segment_segment_xy',
    # 'intersection_circle_circle',
    'intersection_circle_circle_xy',
    'intersection_line_plane',
    'intersection_line_triangle',
    'intersection_segment_plane',
    'intersection_plane_plane',
    'intersection_plane_plane_plane',
    'intersection_sphere_sphere',
    'intersection_ellipse_line_xy',
]


def intersection_line_line(l1, l2, tol=1e-6):
    """Computes the intersection of two lines.

    Parameters
    ----------
    l1 : tuple, list
        XYZ coordinates of two points defining the first line.
    l2 : tuple, list
        XYZ coordinates of two points defining the second line.
    tol : float, optional
        A tolerance for membership verification.
        Default is ``1e-6``.

    Returns
    -------
    list
        XYZ coordinates of the two points marking the shortest distance between the lines.
        If the lines intersect, these two points are identical.
        If the lines are skewed and thus only have an apparent intersection, the two
        points are different.
        If the lines are parallel, the return value is [None, None].

    Examples
    --------
    >>>

    """
    a, b = l1
    c, d = l2

    ab = subtract_vectors(b, a)
    cd = subtract_vectors(d, c)

    n = cross_vectors(ab, cd)
    n1 = normalize_vector(cross_vectors(ab, n))
    n2 = normalize_vector(cross_vectors(cd, n))

    plane_1 = (a, n1)
    plane_2 = (c, n2)

    i1 = intersection_line_plane(l1, plane_2, tol=tol)
    i2 = intersection_line_plane(l2, plane_1, tol=tol)

    return i1, i2


def intersection_line_line_xy(l1, l2, tol=1e-6):
    """Compute the intersection of two lines, assuming they lie in the XY plane.

    Parameters
    ----------
    ab : tuple
        XY(Z) coordinates of two points defining a line.
    cd : tuple
        XY(Z) coordinates of two points defining another line.
    tol : float, optional
        A tolerance for membership verification.
        Default is ``1e-6``.

    Returns
    -------
    None
        If there is no intersection point (parallel lines).
    list
        XYZ coordinates of intersection point if one exists (Z = 0).

    Notes
    -----
    Only if the lines are parallel, there is no intersection point [1]_.

    References
    ----------
    .. [1] Wikipedia. *Line-line intersection*.
           Available at: https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection

    """
    a, b = l1
    c, d = l2

    x1, y1 = a[0], a[1]
    x2, y2 = b[0], b[1]
    x3, y3 = c[0], c[1]
    x4, y4 = d[0], d[1]

    d = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

    if fabs(d) <= tol:
        return None

    a = (x1 * y2 - y1 * x2)
    b = (x3 * y4 - y3 * x4)
    x = (a * (x3 - x4) - (x1 - x2) * b) / d
    y = (a * (y3 - y4) - (y1 - y2) * b) / d

    return x, y, 0.0


def intersection_segment_segment(ab, cd, tol=1e-6):
    """Compute the intersection of two lines segments.

    Parameters
    ----------
    ab : tuple
        XYZ coordinates of two points defining a line segment.
    cd : tuple
        XYZ coordinates of two points defining another line segment.
    tol : float, optional
        A tolerance for membership verification.
        Default is ``1e-6``.

    Returns
    -------
    None
        If there is no intersection point.
    list
        XYZ coordinates of intersection point if one exists.

    """
    x = intersection_line_line(ab, cd, tol=tol)

    if not x:
        return None

    if is_point_on_segment(x, ab, tol=tol) and is_point_on_segment(x, cd, tol=tol):
        return x


def intersection_segment_segment_xy(ab, cd, tol=1e-6):
    """Compute the intersection of two lines segments, assuming they lie in the XY plane.

    Parameters
    ----------
    ab : tuple
        XY(Z) coordinates of two points defining a line segment.
    cd : tuple
        XY(Z) coordinates of two points defining another line segment.
    tol : float, optional
        A tolerance for membership verification.
        Default is ``0.0``.

    Returns
    -------
    None
        If there is no intersection point.
    list
        XYZ coordinates of intersection point if one exists.

    """
    intx_pt = intersection_line_line_xy(ab, cd)

    if not intx_pt:
        return None

    if not is_point_on_segment_xy(intx_pt, ab, tol=tol):
        return None

    if not is_point_on_segment_xy(intx_pt, cd, tol=tol):
        return None

    return intx_pt


def intersection_circle_circle():
    raise NotImplementedError


def intersection_circle_circle_xy(circle1, circle2):
    """Calculates the intersection points of two circles in 2d lying in the XY plane.

    Parameters
    ----------
    circle1 : tuple
        center, radius of the first circle in the xy plane.
    circle2 : tuple
        center, radius of the second circle in the xy plane.

    Returns
    -------
    points : list of tuples
        the intersection points if there are any
    None
        if there are no intersection points

    """
    p1, r1 = circle1[0], circle1[1]
    p2, r2 = circle2[0], circle2[1]

    d = length_vector_xy(subtract_vectors_xy(p2, p1))

    if d > r1 + r2:
        return None

    if d < fabs(r1 - r2):
        return None

    if (d == 0) and (r1 == r2):
        return None

    a = (r1 * r1 - r2 * r2 + d * d) / (2 * d)
    h = (r1 * r1 - a * a) ** 0.5
    cx2 = p1[0] + a * (p2[0] - p1[0]) / d
    cy2 = p1[1] + a * (p2[1] - p1[1]) / d
    i1 = ((cx2 + h * (p2[1] - p1[1]) / d), (cy2 - h * (p2[0] - p1[0]) / d), 0)
    i2 = ((cx2 - h * (p2[1] - p1[1]) / d), (cy2 + h * (p2[0] - p1[0]) / d), 0)

    return i1, i2


def intersection_line_plane(line, plane, tol=1e-6):
    """Computes the intersection point of a line and a plane

    Parameters
    ----------
    line : tuple
        Two points defining the line.
    plane : tuple
        The base point and normal defining the plane.
    tol : float, optional
        A tolerance for membership verification.
        Default is ``1e-6``.


    Returns
    -------
    point : tuple
        if the line (ray) intersects with the plane, None otherwise.

    """
    a, b = line
    o, n = plane

    ab = subtract_vectors(b, a)
    cosa = dot_vectors(n, ab)

    if fabs(cosa) <= tol:
        # if the dot product (cosine of the angle between segment and plane)
        # is close to zero the line and the normal are almost perpendicular
        # hence there is no intersection
        return None

    # based on the ratio = -dot_vectors(n, ab) / dot_vectors(n, oa)
    # there are three scenarios
    # 1) 0.0 < ratio < 1.0: the intersection is between a and b
    # 2) ratio < 0.0: the intersection is on the other side of a
    # 3) ratio > 1.0: the intersection is on the other side of b
    oa = subtract_vectors(a, o)
    ratio = - dot_vectors(n, oa) / cosa
    ab = scale_vector(ab, ratio)
    return add_vectors(a, ab)


def intersection_segment_plane(segment, plane, tol=1e-6):
    """Computes the intersection point of a line segment and a plane

    Parameters
    ----------
    segment : tuple
        Two points defining the line segment.
    plane : tuple
        The base point and normal defining the plane.
    tol : float, optional
        A tolerance for membership verification.
        Default is ``1e-6``.

    Returns
    -------
    point : tuple
        if the line segment intersects with the plane, None otherwise.

    """
    a, b = segment
    o, n = plane

    ab = subtract_vectors(b, a)
    cosa = dot_vectors(n, ab)

    if fabs(cosa) <= tol:
        # if the dot product (cosine of the angle between segment and plane)
        # is close to zero the line and the normal are almost perpendicular
        # hence there is no intersection
        return None

    # based on the ratio = -dot_vectors(n, ab) / dot_vectors(n, oa)
    # there are three scenarios
    # 1) 0.0 < ratio < 1.0: the intersection is between a and b
    # 2) ratio < 0.0: the intersection is on the other side of a
    # 3) ratio > 1.0: the intersection is on the other side of b
    oa = subtract_vectors(a, o)
    ratio = - dot_vectors(n, oa) / cosa

    if 0.0 <= ratio and ratio <= 1.0:
        ab = scale_vector(ab, ratio)
        return add_vectors(a, ab)

    return None


def intersection_line_triangle(line, triangle, tol=1e-6):
    """Computes the intersection point of a line (ray) and a triangle
    based on the Moeller Trumbore intersection algorithm

    Parameters
    ----------
    line : tuple
        Two points defining the line.
    triangle : list of list of float
        XYZ coordinates of the triangle corners.
    tol : float, optional
        A tolerance for membership verification.
        Default is ``1e-6``.

    Returns
    -------
    point : tuple
        The intersectin point.
    None
        If the intersection does not exist.

    """
    # a, b, c = triangle
    # v1 = subtract_vectors(line[1], line[0])
    # p1 = line[0]
    # # Find vectors for two edges sharing V1
    # e1 = subtract_vectors(b, a)
    # e2 = subtract_vectors(c, a)
    # # Begin calculating determinant - also used to calculate u parameter
    # p = cross_vectors(v1, e2)

    # # if determinant is near zero, ray lies in plane of triangle
    # det = dot_vectors(e1, p)
    # if det > - epsilon and det < epsilon:
    #     return None

    # inv_det = 1.0 / det
    # # calculate distance from V1 to ray origin
    # t = subtract_vectors(p1, a)

    # # Calculate u parameter
    # u = dot_vectors(t, p) * inv_det
    # # The intersection lies outside of the triangle
    # if u < 0.0 or u > 1.0:
    #     return None

    # # Prepare to make_blocks v parameter
    # q = cross_vectors(t, e1)
    # # Calculate V parameter

    # v = dot_vectors(v1, q) * inv_det
    # # The intersection lies outside of the triangle
    # if v < 0.0 or u + v > 1.0:
    #     return None

    # t = dot_vectors(e2, q) * inv_det
    # if t > epsilon:
    #     return add_vectors(p1, scale_vector(v1, t))

    # # No hit
    # return None

    a, b, c = triangle
    ab = subtract_vectors(b, a)
    ac = subtract_vectors(c, a)
    n = cross_vectors(ab, ac)
    plane = a, n

    x = intersection_line_plane(line, plane, tol=tol)

    if x:
        if is_point_in_triangle(x, triangle):
            return x


def intersection_plane_plane(plane1, plane2, tol=1e-6):
    """Computes the intersection of two planes

    Parameters
    ----------
    plane1 : tuple
        The base point and normal (normalized) defining the 1st plane.
    plane2 : tuple
        The base point and normal (normalized) defining the 2nd plane.
    tol : float, optional
        A tolerance for membership verification.
        Default is ``1e-6``.

    Returns
    -------
    line : tuple
        Two points defining the intersection line. None if planes are parallel.

    """
    o1, n1 = plane1
    o2, n2 = plane2

    if fabs(dot_vectors(n1, n2)) >= 1 - tol:
        return None

    # direction of intersection line
    d = cross_vectors(n1, n2)
    # vector in plane 1 perpendicular to the direction of the intersection line
    v1 = cross_vectors(d, n1)
    # point on plane 1
    p1 = add_vectors(o1, v1)

    x1 = intersection_line_plane((o1, p1), plane2, tol=tol)
    x2 = add_vectors(x1, d)
    return x1, x2


def intersection_plane_plane_plane(plane1, plane2, plane3, tol=1e-6):
    """Computes the intersection of three planes

    Parameters
    ----------
    plane1 : tuple
        The base point and normal (normalized) defining the 1st plane.
    plane2 : tuple
        The base point and normal (normalized) defining the 2nd plane.
    tol : float, optional
        A tolerance for membership verification.
        Default is ``1e-6``.

    Returns
    -------
    point : tuple
        The intersection point. None if two (or all three) planes are parallel.

    Notes
    -----
    Currently this only computes the intersection point. E.g.: If two planes
    are parallel the intersection lines are not computed [1]_.

    References
    ----------
    .. [1] http://geomalgorithms.com/Pic_3-planes.gif

    """
    line = intersection_plane_plane(plane1, plane2, tol=tol)
    if line:
        return intersection_line_plane(line, plane3, tol=tol)


def intersection_sphere_sphere(sphere1, sphere2):
    """Computes the intersection of 2 spheres.

    There are 4 cases of sphere-sphere intersection : 1) the spheres intersect
    in a circle, 2) they intersect in a point, 3) they overlap, 4) they do not
    intersect.

    Parameters
    ----------
    sphere1 : tuple
        center, radius of the sphere.
    sphere2 : tuple
        center, radius of the sphere.

    Returns
    -------
    case : str
        `point`, `circle`, or `sphere`
    result : tuple
        - point: xyz coordinates
        - circle: center, radius, normal
        - sphere: center, radius

    Examples
    --------
    >>> sphere1 = (3.0, 7.0, 4.0), 10.0
    >>> sphere2 = (7.0, 4.0, 0.0), 5.0
    >>> result = intersection_sphere_sphere(sphere1, sphere2)
    >>> if result:
    >>>    case, res = result
    >>>    if case == "circle":
    >>>        center, radius, normal = res
    >>>    elif case == "point":
    >>>        point = res
    >>>    elif case == "sphere":
    >>>        center, radius = res

    References
    --------
    https://gamedev.stackexchange.com/questions/75756/sphere-sphere-intersection-and-circle-sphere-intersection

    """

    center1, radius1 = sphere1
    center2, radius2 = sphere2

    distance = distance_point_point(center1, center2)

    # Case 4: No intersection
    if radius1 + radius2 < distance:
        return None
    # Case 4: No intersection, sphere is within the other sphere
    elif distance + min(radius1, radius2) < max(radius1, radius2):
        return None
    # Case 3: sphere's overlap
    elif radius1 == radius2 and distance == 0:
        return "sphere", sphere1
    # Case 2: point intersection
    elif radius1 + radius2 == distance:
        ipt = subtract_vectors(center2, center1)
        ipt = scale_vector(ipt, radius1/distance)
        ipt = add_vectors(center1, ipt)
        return "point", ipt
    # Case 2: point intersection, smaller sphere is within the bigger
    elif distance + min(radius1, radius2) == max(radius1, radius2):
        if radius1 > radius2:
            ipt = subtract_vectors(center2, center1)
            ipt = scale_vector(ipt, radius1/distance)
            ipt = add_vectors(center1, ipt)
        else:
            ipt = subtract_vectors(center1, center2)
            ipt = scale_vector(ipt, radius2/distance)
            ipt = add_vectors(center2, ipt)
        return "point", ipt
    # Case 1: circle intersection
    else:
        h  = 0.5 + (radius1**2 - radius2**2)/(2 * distance**2)
        ci = subtract_vectors(center2, center1)
        ci = scale_vector(ci, h)
        ci = add_vectors(center1, ci)
        ri = sqrt(radius1**2 - h**2 * distance**2)
        normal = scale_vector(subtract_vectors(center2, center1), 1/distance)
        return "circle", (ci, ri, normal)


def intersection_ellipse_line_xy(ellipse, line):
    """Computes the intersection of an ellipse and a line in the XY plane.

    Parameters
    ----------
    ellipse : tuple
        The lengths a, b of the ellipse' semiaxes.
    line : tuple
        XY(Z) coordinates of two points defining another line.

    Returns
    -------
    None
        If there is no intersection.
    tuple
        Either 1 or 2 intersection points.

    Examples
    --------
    >>> ellipse = 6., 2.5
    >>> p1 = (4.1, 2.8, 0.)
    >>> p2 = (3.4, -3.1, 0.)
    >>> i1, i2 = intersection_ellipse_line_xy(ellipse, [p1, p2])

    References
    ----------
    .. [1] C# Helper. *Calculate where a line segment and an ellipse intersect in C#*.
           Available at: http://csharphelper.com/blog/2017/08/calculate-where-a-line-segment-and-an-ellipse-intersect-in-c/

    """
    x1, y1 = line[0][0], line[0][1]
    x2, y2 = line[1][0], line[1][1]

    a, b = ellipse

    A = (x2 - x1)**2/a**2 + (y2 - y1)**2/b**2
    B = 2*x1*(x2 - x1)/a**2 + 2*y1*(y2 - y1)/b**2
    C = x1**2/a**2 + y1**2/b**2 - 1

    discriminant = B**2 - 4*A*C
    if discriminant == 0:
        t = -B/(2*A)
        return (x1 + (x2 - x1)*t, y1 + (y2 - y1)*t, 0.0)
    elif discriminant > 0:
        t1 = (-B + sqrt(discriminant))/(2*A)
        t2 = (-B - sqrt(discriminant))/(2*A)
        p1 = (x1 + (x2 - x1)*t1, y1 + (y2 - y1)*t1, 0.0)
        p2 = (x1 + (x2 - x1)*t2, y1 + (y2 - y1)*t2, 0.0)
        return p1, p2
    else:
        return None

# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    
    # # intersection_sphere_sphere(sphere1, sphere2)
    # sphere1 = (3.0, 7.0, 4.0), 10.0
    # sphere2 = (7.0, 4.0, 0.0), 5.0
    # result = intersection_sphere_sphere(sphere1, sphere2)
    # print(result)
    # if result:
    #     case, res = result
    #     if case == "circle":
    #         center, radius, normal = res
    #     elif case == "point":
    #         point = res
    #     elif case == "sphere":
    #         center, radius = res

    a = ([0.0, 0.0, 0.0], [1.0, 1.0, 0.0])
    b = ([1.0, 0.0, 0.0], [2.0, 1.0, 0.0])

    res = intersection_line_line_xy(a, b)

    print(res)
