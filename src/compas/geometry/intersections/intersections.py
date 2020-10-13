from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from math import fabs
from math import sqrt

import compas

from compas.utilities import pairwise
from compas.utilities import geometric_key

from compas.geometry import allclose
from compas.geometry import add_vectors
from compas.geometry import subtract_vectors
from compas.geometry import scale_vector
from compas.geometry import cross_vectors
from compas.geometry import dot_vectors
from compas.geometry import length_vector_xy
from compas.geometry import subtract_vectors_xy
from compas.geometry import normalize_vector
from compas.geometry import distance_point_point
from compas.geometry import is_point_on_segment
from compas.geometry import is_point_on_segment_xy
from compas.geometry import is_point_in_triangle


__all__ = [
    'intersection_line_line',
    'intersection_segment_segment',
    'intersection_line_segment',
    'intersection_line_plane',
    'intersection_polyline_plane',
    'intersection_line_triangle',
    'intersection_segment_plane',
    'intersection_plane_circle',
    'intersection_plane_plane',
    'intersection_plane_plane_plane',
    'intersection_sphere_line',
    'intersection_sphere_sphere',
    'intersection_segment_polyline',

    'intersection_line_line_xy',
    'intersection_segment_segment_xy',
    'intersection_line_segment_xy',
    'intersection_line_box_xy',
    'intersection_circle_circle_xy',
    'intersection_ellipse_line_xy',
    'intersection_segment_polyline_xy'
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
    tuple
        Two intersection points.

        If the lines intersect, these two points are identical.
        If the lines are skewed and thus only have an apparent intersection, the two points are different.

        In all other cases the return is `(None, None)`.

    Examples
    --------
    The 2 intersection points of intersecting lines are identical.

    >>> l1 = [0, 0, 0], [1, 0, 0]
    >>> l2 = [0, 0, 0], [0, 1, 0]
    >>> intersection_line_line(l1, l2)
    ([0.0, 0.0, 0.0], [0.0, 0.0, 0.0])

    Note that lines extend beyond their start and end points.

    >>> l1 = [0, 0, 0], [1, 0, 0]
    >>> l2 = [2, 0, 0], [0, 1, 0]
    >>> intersection_line_line(l1, l2)
    ([2.0, 0.0, 0.0], [2.0, 0.0, 0.0])

    Skew lines have two different intersection points.

    >>> l1 = [0, 0, 0], [1, 0, 0]
    >>> l2 = [0, 0, 1], [0, 1, 1]
    >>> intersection_line_line(l1, l2)
    ([0.0, 0.0, 0.0], [0.0, 0.0, 1.0])

    Parallel lines don't intersect.

    >>> l1 = [0, 0, 0], [1, 0, 0]
    >>> l2 = [0, 0, 0], [1, 0, 0]
    >>> intersection_line_line(l1, l2)
    (None, None)

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

    if not i1 or not i2:
        return None, None

    return i1, i2


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
    tuple
        Two intersection points.

        If the segments intersect and the intersection points lie on the respective segments, the two points are identical.
        If the segments are skew and the apparent intersection points lie on the respective segments, the two points are different.

        In all other cases the return is `(None, None)`.

    Examples
    --------
    The 2 intersection points of intersecting segments are identical.

    >>> s1 = [0, 0, 0], [1, 0, 0]
    >>> s2 = [0, 0, 0], [0, 1, 0]
    >>> intersection_segment_segment(s1, s2)
    ([0.0, 0.0, 0.0], [0.0, 0.0, 0.0])

    Unlike lines, segments don't extend beyond their start and end points.

    >>> s1 = [0, 0, 0], [1, 0, 0]
    >>> s2 = [2, 0, 0], [0, 1, 0]
    >>> intersection_segment_segment(s1, s2)
    (None, None)

    Skew segments have two different intersection points.

    >>> s1 = [0, 0, 0], [1, 0, 0]
    >>> s2 = [0, 0, 1], [0, 1, 1]
    >>> intersection_segment_segment(s1, s2)
    ([0.0, 0.0, 0.0], [0.0, 0.0, 1.0])

    Parallel segments don't intersect.

    >>> s1 = [0, 0, 0], [1, 0, 0]
    >>> s2 = [0, 0, 0], [1, 0, 0]
    >>> intersection_segment_segment(s1, s2)
    (None, None)

    """
    x1, x2 = intersection_line_line(ab, cd, tol=tol)

    if not x1 or not x2:
        return None, None

    if not is_point_on_segment(x1, ab, tol=tol):
        return None, None

    if not is_point_on_segment(x2, cd, tol=tol):
        return None, None

    return x1, x2


def intersection_line_segment(line, segment, tol=1e-6):
    """Compute the intersection of a line and a segment.

    Parameters
    ----------
    line : tuple
        Two points defining a line.
    segment : tuple
        Two points defining a line segment.
    tol : float, optional
        A tolerance for membership verification.
        Default is ``1e-6``.

    Returns
    -------
    tuple
        Two intersection points.

        If the line and segment intersect and the second intersection point lies on the segment, the two points are identical.
        If the line and segment are skew and the second apparent intersection point lies on the segment, the two points are different.

        In all other cases the return is `(None, None)`.

    """
    x1, x2 = intersection_line_line(line, segment, tol=tol)

    if not x1 or not x2:
        return None, None

    if not is_point_on_segment(x2, segment, tol=tol):
        return None, None

    return x1, x2


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
    point or None

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
    point or None

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


def intersection_polyline_plane(polyline, plane, expected_number_of_intersections=None, tol=1e-6):
    """Calculate the intersection point of a plane with a polyline. Reduce expected_number_of_intersections to speed up.

    Parameters
    ----------
    polyline : :class:`compas.geometry.Polyline` or sequence of points
        Polyline to test intersection.
    plane : :class:`compas.geometry.Plane` or point and vector
        Plane to compute intersection.
    expected_number_of_intersections : integer, optional
        Number of useful or expected intersections.
        Default is the number of lines conforming the polyline.
    tol : float, optional
        A tolerance for membership verification.
        Default is ``1e-6``.

    Returns
    -------
    list of points

    """
    if not expected_number_of_intersections:
        expected_number_of_intersections = len(polyline)
    intersections = []
    for segment in pairwise(polyline):
        if len(intersections) == expected_number_of_intersections:
            break
        point = intersection_segment_plane(segment, plane, tol)
        if point:
            intersections.append(point)
    return intersections


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
    point or None

    """
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
    plane3 : tuple
        The base point and normal (normalized) defining the 3rd plane.
    tol : float, optional
        A tolerance for membership verification.
        Default is ``1e-6``.

    Returns
    -------
    point or None

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
    ...     case, res = result
    ...     if case == "circle":
    ...         center, radius, normal = res
    ...     elif case == "point":
    ...         point = res
    ...     elif case == "sphere":
    ...         center, radius = res

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
    h = 0.5 + (radius1**2 - radius2**2)/(2 * distance**2)
    ci = subtract_vectors(center2, center1)
    ci = scale_vector(ci, h)
    ci = add_vectors(center1, ci)
    ri = sqrt(radius1**2 - h**2 * distance**2)
    normal = scale_vector(subtract_vectors(center2, center1), 1/distance)
    return "circle", (ci, ri, normal)


def intersection_segment_polyline(segment, polyline, tol=1e-6):
    """Calculate the intersection point of a segment and a polyline.

    Parameters
    ----------
    segment : sequence of sequence of float
        XYZ coordinates of two points defining a line segment.
    polyline : sequence of sequence of float
        XYZ coordinates of the points of the polyline.
    tol : float, optional
        The tolerance for intersection verification.
        Default is ``1e-6``.

    Returns
    -------
    point or None

    Examples
    --------
    >>> from compas.geometry._core import is_point_on_polyline
    >>> from compas.geometry._core import is_point_on_segment
    >>> from compas.geometry._core import distance_point_point
    >>> p = [(0.0, 0.0, 0.0), (1.0, 0.0, 0.5), (2.0, 0.5, 1.0)]
    >>> s = [(0.5, 0.0, 0.0), (0.5, 0.0, 2.0)]
    >>> intpt = intersection_segment_polyline(s, p)
    >>> is_point_on_polyline(intpt, p)
    True
    >>> is_point_on_segment(intpt, s)
    True
    >>> distance_point_point((0.5, 0.0, 0.25), intpt) < 1e-6
    True
    """
    for cd in pairwise(polyline):
        pt = intersection_segment_segment(segment, cd, tol)
        if pt:
            return pt


def intersection_sphere_line(sphere, line):
    """Computes the intersection of a sphere and a line.

    There are 3 cases of sphere-line intersection : 1) they intersect in 2
    points, 2) they intersect in 1 point (line tangent to sphere), or 3) they
    do not intersect.

    Parameters
    ----------
    sphere : tuple
        center, radius of the sphere.
    line : tuple
        xyz coordinates of two points defining the line.

    Returns
    -------
    None or point or list of points

    Examples
    --------
    >>> sphere = (3.0, 7.0, 4.0), 10.0
    >>> line = (1.0, 0, 0.5), (2.0, 1.0, 0.5)
    >>> ipt1, ipt2 = intersection_sphere_line(sphere, line)
    >>> Point(*ipt1), Point(*ipt2)
    (Point(11.634, 10.634, 0.500), Point(-0.634, -1.634, 0.500))

    References
    --------
    https://gamedev.stackexchange.com/questions/75756/sphere-sphere-intersection-and-circle-sphere-intersection

    """
    l1, l2 = line
    sp, radius = sphere

    a = (l2[0] - l1[0])**2 + (l2[1] - l1[1])**2 + (l2[2] - l1[2])**2
    b = 2.0 * ((l2[0] - l1[0]) * (l1[0] - sp[0]) +
               (l2[1] - l1[1]) * (l1[1] - sp[1]) +
               (l2[2] - l1[2]) * (l1[2] - sp[2]))

    c = sp[0]**2 + sp[1]**2 + sp[2]**2 + l1[0]**2 + l1[1]**2 + l1[2]**2 - 2.0 * (sp[0] * l1[0] + sp[1] * l1[1] + sp[2] * l1[2]) - radius**2

    i = b * b - 4.0 * a * c

    if i < 0.0:  # case 3: no intersection
        return None
    elif i == 0.0:  # case 2: one intersection
        mu = -b / (2.0 * a)
        ipt = (l1[0] + mu * (l2[0] - l1[0]), l1[1] + mu * (l2[1] - l1[1]), l1[2] + mu * (l2[2] - l1[2]))
        return ipt
    elif i > 0.0:  # case 1: two intersections
        # 1.
        mu = (-b + sqrt(i)) / (2.0 * a)
        ipt1 = (l1[0] + mu * (l2[0] - l1[0]), l1[1] + mu * (l2[1] - l1[1]), l1[2] + mu * (l2[2] - l1[2]))
        # 2.
        mu = (-b - sqrt(i)) / (2.0 * a)
        ipt2 = (l1[0] + mu * (l2[0] - l1[0]), l1[1] + mu * (l2[1] - l1[1]), l1[2] + mu * (l2[2] - l1[2]))
        return ipt1, ipt2


def intersection_plane_circle(plane, circle):
    """Computes the intersection of a plane and a circle.

    There are 4 cases of plane-circle intersection : 1) they do not intersect,
    2) they coincide (circle.plane == plane), 3) they intersect in 2
    points (secant), 4) they intersect in 1 point (tangent).

    Parameters
    ----------
    plane : tuple
        point, normal of the plane.
    circle : tuple
        (point, normal), radius of the circle

    Returns
    -------
    None or point or list of points

    Examples
    --------
    >>> plane = (0, 0, 0), (0, 0, 1)
    >>> circle = ((3.0, 7.0, 4.0), (0, 1, 0)), 10.0
    >>> ipt1, ipt2 = intersection_plane_circle(plane, circle)
    >>> Point(*ipt1), Point(*ipt2)
    (Point(-6.165, 7.000, 0.000), Point(12.165, 7.000, 0.000))
    """
    circle_plane, circle_radius = circle
    line = intersection_plane_plane(plane, circle_plane)
    if not line:
        return None
    circle_point = circle_plane[0]
    sphere = circle_point, circle_radius
    return intersection_sphere_line(sphere, line)


# ==============================================================================
# XY
# ==============================================================================


def intersection_line_line_xy(l1, l2, tol=1e-6):
    """Compute the intersection of two lines, assuming they lie on the XY plane.

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
    point or None
        XYZ coordinates of intersection point if one exists, with Z = 0.
        Otherwise, None.

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

    return [x, y, 0.0]


def intersection_line_segment_xy(line, segment, tol=1e-6):
    """"""
    x = intersection_line_line_xy(line, segment, tol=tol)
    if x:
        if is_point_on_segment_xy(x, segment, tol=tol):
            return x


def intersection_line_box_xy(line, box, tol=1e-6):
    """Compute the intersection between a line and a box in the XY plane.

    Parameters
    ----------
    line : list of 2 points or :class:`compas.geometry.Line`
    box : list of 4 points
    tol : float, optional
        A tolerance value for point comparison.
        Default is ``1e-6``.

    Returns
    -------
    list
        A list of at most two intersection points.
    """
    points = []
    for segment in pairwise(box + box[:1]):
        x = intersection_line_segment_xy(line, segment, tol=tol)
        if x:
            points.append(x)
    if len(points) < 3:
        return points
    if len(points) == 3:
        a, b, c = points
        if allclose(a, b, tol=tol):
            return [a, c]
        if allclose(b, c, tol=tol):
            return [a, b]
        return [a, b]
    return [a, c]


def intersection_polyline_box_xy(polyline, box, tol=1e-6):
    """Compute the intersection between a polyline and a box in the XY plane.

    Parameters
    ----------
    polyline : list of points or :class:`compas.geometry.Polyline`
    box : list of 4 points
    tol : float, optional
        A tolerance value for point comparison.
        Default is ``1e-6``.

    Returns
    -------
    list
        A list of intersection points.
    """
    precision = compas.PRECISION
    compas.set_precision(tol)
    points = []
    for side in pairwise(box + box[:1]):
        for segment in pairwise(polyline):
            x = intersection_segment_segment_xy(side, segment, tol=tol)
            if x:
                points.append(x)
    points = {geometric_key(point): point for point in points}
    compas.PRECISION = precision
    return list(points.values())


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


def intersection_segment_polyline_xy(segment, polyline, tol=1e-6):
    """
    Calculate the intersection point of a segment and a polyline on the XY-plane.

    Parameters
    ----------
    segment : sequence of sequence of float
        XY(Z) coordinates of two points defining a line segment.
    polyline : sequence of sequence of float
        XY(Z) coordinates of the points of the polyline.
    tol : float, optional
        The tolerance for intersection verification.
        Default is ``1e-6``.

    Returns
    -------
    None
        If there is no intersection point.
    point : list of tuple
        XYZ coordinates of the first intersection point if one exists (Z = 0).

    Examples
    --------
    >>> from compas.geometry._core import is_point_on_polyline_xy
    >>> from compas.geometry._core import is_point_on_segment_xy
    >>> from compas.geometry._core import distance_point_point
    >>> p = [(0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (2.0, 0.0, 0.0)]
    >>> s = [(0.5, -0.5, 0.0), (0.5, 0.5, 0.0)]
    >>> intpt = intersection_segment_polyline_xy(s, p)
    >>> is_point_on_polyline_xy(intpt, p)
    True
    >>> is_point_on_segment_xy(intpt, s)
    True
    >>> distance_point_point((0.5, 0.0, 0.0), intpt) < 1e-6
    True
    """
    for cd in pairwise(polyline):
        pt = intersection_segment_segment_xy(segment, cd, tol)
        if pt:
            return pt


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


# def intersection_line_circle_xy(line, circle):
#     """Compute the intersection of a line and a circle in the XY plane.

#     Parameters
#     ----------

#     """
#     x0, y0 = circle[0][:2]
#     r = circle[1]
#     x1, y1 = line[0][:2]
#     x2, y2 = line[1][:2]
#     a = y1 - y2
#     b = x2 - x1
#     c = x1 * y2 - x2 * y1
#     D = sqrt(r**2 - c**2 / (a**2 + b**2))
#     m = sqrt(D**2 / (a**2 + b**2))
#     p1 = [x0 + b * m, y0 - a * m, 0]
#     p2 = [x0 - b * m, y0 + a * m, 0]
#     return p1, p2


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    import doctest
    from compas.geometry import Point    # noqa: F401
    doctest.testmod(globs=globals())
