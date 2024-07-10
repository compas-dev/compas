from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from math import fabs
from math import sqrt

from compas.geometry import add_vectors
from compas.geometry import cross_vectors
from compas.geometry import distance_point_point
from compas.geometry import dot_vectors
from compas.geometry import is_point_in_triangle
from compas.geometry import is_point_on_segment
from compas.geometry import is_point_on_segment_xy
from compas.geometry import length_vector_xy
from compas.geometry import normalize_vector
from compas.geometry import scale_vector
from compas.geometry import subtract_vectors
from compas.geometry import subtract_vectors_xy
from compas.itertools import pairwise
from compas.plugins import PluginNotInstalledError
from compas.plugins import pluggable
from compas.tolerance import TOL


def intersection_line_line(l1, l2, tol=None):
    """Computes the intersection of two lines.

    Parameters
    ----------
    l1 : [point, point] | :class:`compas.geometry.Line`
        XYZ coordinates of two points defining the first line.
    l2 : [point, point] | :class:`compas.geometry.Line`
        XYZ coordinates of two points defining the second line.
    tol : float, optional
        Tolerance for evaluating the intersection points of each of the lines with the corresponding skew plane.
        Default is :attr:`TOL.absolute`.

    Returns
    -------
    tuple[[float, float, float], [float, float, float]] | tuple[None, None]
        Two intersection points.
        If the lines intersect, these two points are identical.
        If the lines are skewed and thus only have an apparent intersection, the two points are different.
        In all other cases there are no intersection points.

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


def intersection_segment_segment(ab, cd, tol=None):
    """Compute the intersection of two lines segments.

    Parameters
    ----------
    ab : [point, point] | :class:`compas.geometry.Line`
        XYZ coordinates of two points defining a line segment.
    cd : [point, point] | :class:`compas.geometry.Line`
        XYZ coordinates of two points defining another line segment.
    tol : float, optional
        Tolerance value for computing the intersection points of the underlying lines,
        and for verifying that those points are contained by the segments.
        Default is :attr:`TOL.absolute`.

    Returns
    -------
    tuple[[float, float, float], [float, float, float]] | tuple[None, None]
        Two intersection points.
        If the segments intersect and the intersection points lie on the respective segments, the two points are identical.
        If the segments are skew and the apparent intersection points lie on the respective segments, the two points are different.
        In all other cases there are no intersection points.

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


def intersection_line_segment(line, segment, tol=None):
    """Compute the intersection of a line and a segment.

    Parameters
    ----------
    line : [point, point] | :class:`compas.geometry.Line`
        Two points defining a line.
    segment : [point, point] | :class:`compas.geometry.Line`
        Two points defining a line segment.
    tol : float, optional
        Tolerance value for computing the intersection points of the underlying lines,
        and for verifying that those points are contained by the segment.
        Default is :attr:`TOL.absolute`.

    Returns
    -------
    tuple[[float, float, float], [float, float, float]] | tuple[None, None]
        Two intersection points.
        If the line and segment intersect and the second intersection point lies on the segment, the two points are identical.
        If the line and segment are skew and the second apparent intersection point lies on the segment, the two points are different.
        In all other cases there are no intersection points.

    """
    x1, x2 = intersection_line_line(line, segment, tol=tol)

    if not x1 or not x2:
        return None, None

    if not is_point_on_segment(x2, segment, tol=tol):
        return None, None

    return x1, x2


def intersection_line_plane(line, plane, tol=None):
    """Computes the intersection point of a line and a plane

    Parameters
    ----------
    line : [point, point] | :class:`compas.geometry.Line`
        Two points defining the line.
    plane : [point, vector]
        The base point and normal defining the plane.
    tol : float, optional
        Tolerance for evaluating that the dot product of the line direction and the plane normal is zero.
        Default is :attr:`TOL.absolute`.

    Returns
    -------
    [float, float, float] | None
        The intersection point between the line and the plane,
        or None if the line and the plane are parallel.

    See Also
    --------
    :func:`intersection_segment_plane`
    :func:`intersection_polyline_plane`

    """
    a, b = line
    o, n = plane

    ab = subtract_vectors(b, a)
    cosa = dot_vectors(n, ab)

    if TOL.is_zero(cosa, tol):
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
    ratio = -dot_vectors(n, oa) / cosa
    ab = scale_vector(ab, ratio)
    return add_vectors(a, ab)


def intersection_segment_plane(segment, plane, tol=None):
    """Computes the intersection point of a line segment and a plane

    Parameters
    ----------
    segment : [point, point] | :class:`compas.geometry.Line`
        Two points defining the line segment.
    plane : [point, vector]
        The base point and normal defining the plane.
    tol : float, optional
        Tolerance for evaluating that the dot product of the line direction and the plane normal is zero.
        Default is :attr:`TOL.absolute`.

    Returns
    -------
    [float, float, float] | None
        The intersection point between the line and the plane,
        or None if the line and the plane are parallel.

    See Also
    --------
    :func:`intersection_line_plane`
    :func:`intersection_polyline_plane`

    """
    a, b = segment
    o, n = plane

    ab = subtract_vectors(b, a)
    cosa = dot_vectors(n, ab)

    if TOL.is_zero(cosa, tol):
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
    ratio = -dot_vectors(n, oa) / cosa

    if 0.0 <= ratio and ratio <= 1.0:
        ab = scale_vector(ab, ratio)
        return add_vectors(a, ab)

    return None


def intersection_polyline_plane(polyline, plane, expected_number_of_intersections=None, tol=None):
    """Calculate the intersection point of a plane with a polyline. Reduce expected_number_of_intersections to speed up.

    Parameters
    ----------
    polyline : sequence[point] | :class:`compas.geometry.Polyline`
        Polyline to test intersection.
    plane : [point, vector]
        Plane to compute intersection.
    expected_number_of_intersections : int, optional
        Number of useful or expected intersections.
        Default is the number of line segments of the polyline.
    tol : float, optional
        Tolerance for computing the intersection points between the individual segments of the polyline and the plane.
        Default is :attr:`TOL.absolute`.

    Returns
    -------
    list[[float, float, float]]
        The intersection points between the polyline segments and the plane.

    See Also
    --------
    :func:`intersection_segment_plane`
    :func:`intersection_line_plane`

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


def intersection_line_triangle(line, triangle, tol=None):
    """Computes the intersection point of a line (ray) and a triangle
    based on the Moeller Trumbore intersection algorithm

    Parameters
    ----------
    line : [point, point] | :class:`compas.geometry.Line`
        Two points defining the line.
    triangle : [point, point, point]
        XYZ coordinates of the triangle corners.
    tol : float, optional
        Tolerance value for computing the intersection between the line and the plane of the triangle.
        Default is :attr:`TOL.absolute`.

    Returns
    -------
    [float, float, float] | None
        The intersection point between the line and the triangle,
        or None if the line and the plane are parallel.

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


def intersection_plane_plane(plane1, plane2, tol=None):
    """Computes the intersection of two planes

    Parameters
    ----------
    plane1 : [point, vector]
        The base point and normal (normalized) defining the 1st plane.
    plane2 : [point, vector]
        The base point and normal (normalized) defining the 2nd plane.
    tol : float, optional
        Tolerance for evaluating if the dot product of the plane normals is one.
        Default is :attr:`TOL.absolute`.

    Returns
    -------
    tuple[[float, float, float], [float, float, float]] | None
        Two points defining the intersection line.
        None if the planes are parallel.

    """
    o1, n1 = plane1
    o2, n2 = plane2

    if TOL.is_close(dot_vectors(n1, n2), 1.0, tol):
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


def intersection_plane_plane_plane(plane1, plane2, plane3, tol=None):
    """Computes the intersection of three planes

    Parameters
    ----------
    plane1 : [point, vector]
        The base point and normal (normalized) defining the 1st plane.
    plane2 : [point, vector]
        The base point and normal (normalized) defining the 2nd plane.
    plane3 : [point, vector]
        The base point and normal (normalized) defining the 3rd plane.
    tol : float, optional
        Tolerance for computing the intersection line between the first two planes, and between the intersection line and the third plane.
        Default is :attr:`TOL.absolute`.

    Returns
    -------
    [float, float, float] | None
        The intersection point
        or None if at least one pair of planes is parallel.

    Notes
    -----
    Currently this only computes the intersection point.
    For example, if two planes are parallel the intersection lines are not computed [1]_.

    References
    ----------
    .. [1] http://geomalgorithms.com/Pic_3-planes.gif

    """
    line = intersection_plane_plane(plane1, plane2, tol=tol)
    if line:
        return intersection_line_plane(line, plane3, tol=tol)


def intersection_sphere_sphere(sphere1, sphere2):
    """Computes the intersection of 2 spheres.

    Parameters
    ----------
    sphere1 : [point, float]
        A sphere defined by a point and radius.
    sphere2 : [point, float]
        A sphere defined by a point and radius.

    Returns
    -------
    {'point', 'circle', or 'sphere'}
        The type of intersection.
    [float, float, float] | tuple[[float, float, float], float, [float, float, float]] | tuple[[float, float, float], float]
        If the type is 'point', the coordinates of the point.
        If the type is 'circle', the center point and radius of the circle, and the normal of the plane containing the circle.
        If the type is 'sphere', the center point and radius of the sphere.

    Notes
    -----
    There are 4 cases of sphere-sphere intersection [1]_:

    1. the spheres intersect in a circle,
    2. they intersect in a point,
    3. they overlap,
    4. they do not intersect.

    References
    ----------
    .. [1] https://gamedev.stackexchange.com/questions/75756/sphere-sphere-intersection-and-circle-sphere-intersection

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
        ipt = scale_vector(ipt, radius1 / distance)
        ipt = add_vectors(center1, ipt)
        return "point", ipt

    # Case 2: point intersection, smaller sphere is within the bigger
    elif distance + min(radius1, radius2) == max(radius1, radius2):
        if radius1 > radius2:
            ipt = subtract_vectors(center2, center1)
            ipt = scale_vector(ipt, radius1 / distance)
            ipt = add_vectors(center1, ipt)
        else:
            ipt = subtract_vectors(center1, center2)
            ipt = scale_vector(ipt, radius2 / distance)
            ipt = add_vectors(center2, ipt)
        return "point", ipt

    # Case 1: circle intersection
    h = 0.5 + (radius1**2 - radius2**2) / (2 * distance**2)
    ci = subtract_vectors(center2, center1)
    ci = scale_vector(ci, h)
    ci = add_vectors(center1, ci)
    ri = sqrt(radius1**2 - h**2 * distance**2)
    normal = scale_vector(subtract_vectors(center2, center1), 1 / distance)
    return "circle", (ci, ri, normal)


def intersection_segment_polyline(segment, polyline, tol=None):
    """Calculate the intersection point of a segment and a polyline.

    Parameters
    ----------
    segment : [point, point] | :class:`compas.geometry.Line`
        XYZ coordinates of two points defining a line segment.
    polyline : sequence[point] | :class:`compas.geometry.Polyline`
        XYZ coordinates of the points of the polyline.
    tol : float, optional
        Tolerance value for computing the intersection points between the segment and the polyline segments.
        Default is :attr:`TOL.absolute`.

    Returns
    -------
    [float, float, float] | None
        The intersection point
        or None if the segment does not intersect with any of the polyline segments.

    Examples
    --------
    >>> from compas.geometry import is_point_on_polyline
    >>> from compas.geometry import is_point_on_segment
    >>> from compas.geometry import distance_point_point
    >>> from compas.geometry import centroid_points
    >>> p = [(0.0, 0.0, 0.0), (1.0, 0.0, 0.5), (2.0, 0.5, 1.0)]
    >>> s = [(0.5, 0.0, 0.0), (0.5, 0.0, 2.0)]
    >>> x1, x2 = intersection_segment_polyline(s, p)
    >>> x = centroid_points([x1, x2])

    >>> is_point_on_polyline(x, p)
    True

    >>> is_point_on_segment(x, s)
    True

    >>> distance_point_point((0.5, 0.0, 0.25), x) < 1e-6
    True
    """
    for cd in pairwise(polyline):
        pt = intersection_segment_segment(segment, cd, tol)
        if pt:
            return pt


def intersection_sphere_line(sphere, line):
    """Computes the intersection of a sphere and a line.

    Parameters
    ----------
    sphere : [point, radius]
        A sphere defined by a point and a radius.
    line : [point, point] | :class:`compas.geometry.Line`
        A line defined by two points.

    Returns
    -------
    tuple[[float, float, float], [float, float, float]] | [float, float, float] | None
        Two points (if the line goes through the sphere), one point (if the line is tangent to the sphere), or None (otherwise).

    Notes
    -----
    There are 3 cases of sphere-line intersection:

    1. they intersect in 2 points
    2. they intersect in 1 point (line tangent to sphere), or
    3. they do not intersect.

    Examples
    --------
    >>> from compas.tolerance import TOL

    >>> sphere = (3.0, 7.0, 4.0), 10.0
    >>> line = (1.0, 0, 0.5), (2.0, 1.0, 0.5)
    >>> x1, x2 = intersection_sphere_line(sphere, line)

    >>> TOL.is_allclose(x1, [11.634, 10.634, 0.500], atol=1e-3)
    True
    >>> TOL.is_allclose(x2, [-0.634, -1.634, 0.50], atol=1e-3)
    True

    """
    l1, l2 = line
    sp, radius = sphere

    a = (l2[0] - l1[0]) ** 2 + (l2[1] - l1[1]) ** 2 + (l2[2] - l1[2]) ** 2
    b = 2.0 * ((l2[0] - l1[0]) * (l1[0] - sp[0]) + (l2[1] - l1[1]) * (l1[1] - sp[1]) + (l2[2] - l1[2]) * (l1[2] - sp[2]))

    c = sp[0] ** 2 + sp[1] ** 2 + sp[2] ** 2 + l1[0] ** 2 + l1[1] ** 2 + l1[2] ** 2 - 2.0 * (sp[0] * l1[0] + sp[1] * l1[1] + sp[2] * l1[2]) - radius**2

    i = b * b - 4.0 * a * c

    if i < 0.0:  # case 3: no intersection
        return None
    elif i == 0.0:  # case 2: one intersection
        mu = -b / (2.0 * a)
        ipt = (
            l1[0] + mu * (l2[0] - l1[0]),
            l1[1] + mu * (l2[1] - l1[1]),
            l1[2] + mu * (l2[2] - l1[2]),
        )
        return ipt
    elif i > 0.0:  # case 1: two intersections
        # 1.
        mu = (-b + sqrt(i)) / (2.0 * a)
        ipt1 = (
            l1[0] + mu * (l2[0] - l1[0]),
            l1[1] + mu * (l2[1] - l1[1]),
            l1[2] + mu * (l2[2] - l1[2]),
        )
        # 2.
        mu = (-b - sqrt(i)) / (2.0 * a)
        ipt2 = (
            l1[0] + mu * (l2[0] - l1[0]),
            l1[1] + mu * (l2[1] - l1[1]),
            l1[2] + mu * (l2[2] - l1[2]),
        )
        return ipt1, ipt2


def intersection_plane_circle(plane, circle):
    """Computes the intersection of a plane and a circle.

    Parameters
    ----------
    plane : [point, vector]
        A plane defined by a point and normal vector.
    circle : [plane, float]
        A circle defined by a plane and radius.

    Returns
    -------
    tuple[[float, float, float], [float, float, float]] | [float, float, float] | None
        Two points (secant intersection), one point (tangent intersection), or None (otherwise).

    Notes
    -----
    There are 4 cases of plane-circle intersection:

    1. they intersect in 2 points (secant),
    2. they intersect in 1 point (tangent),
    3. they do not intersect, or
    4. they coincide (circle.plane == plane).

    Examples
    --------
    >>> plane = (0, 0, 0), (0, 0, 1)
    >>> circle = ((0, 0, 0), (0, 1, 0)), 10.0
    >>> x1, x2 = intersection_plane_circle(plane, circle)
    >>> x1
    (-10.0, 0.0, 0.0)
    >>> x2
    (10.0, 0.0, 0.0)

    """
    circle_plane, circle_radius = circle
    line = intersection_plane_plane(plane, circle_plane)
    if not line:
        return None
    circle_point = circle_plane[0]
    sphere = circle_point, circle_radius
    return intersection_sphere_line(sphere, line)


@pluggable(category="intersections")
def intersection_mesh_mesh(A, B):
    """Compute the intersection of two meshes.

    Parameters
    ----------
    A : tuple of vertices and faces
        Mesh A.
    B : tuple of vertices and faces
        Mesh B.

    Returns
    -------
    list of arrays of points
        The intersection polylines as arrays of points.

    """
    raise PluginNotInstalledError


intersection_mesh_mesh.__pluggable__ = True


@pluggable(category="intersections")
def intersection_ray_mesh(ray, mesh):
    """Compute the intersection(s) between a ray and a mesh.

    Parameters
    ----------
    ray : tuple of point and vector
        A ray represented by a point and a direction vector.
    mesh : tuple of vertices and faces
        A mesh represented by a list of vertices and a list of faces.

    Returns
    -------
    list of tuple
        Per intersection of the ray with the mesh:

        0. the index of the intersected face
        1. the u coordinate of the intersection in the barycentric coordinates of the face
        2. the u coordinate of the intersection in the barycentric coordinates of the face
        3. the distance between the ray origin and the hit

    Examples
    --------
    >>>

    """
    raise PluginNotInstalledError


intersection_ray_mesh.__pluggable__ = True


# ==============================================================================
# XY
# ==============================================================================


def intersection_line_line_xy(l1, l2, tol=None):
    """Compute the intersection of two lines, assuming they lie on the XY plane.

    Parameters
    ----------
    l1 : [point, point] | :class:`compas.geometry.Line`
        A line defined by two points, with at least XY coordinates.
    l2 : [point, point] | :class:`compas.geometry.Line`
        A line defined by two points, with at least XY coordinates.
    tol : float, optional
        Tolerance for comparing the length of the cross product of the line directions with zero.
        Default is :attr:`TOL.absolute`.

    Returns
    -------
    [float, float, 0.0] | None
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

    if TOL.is_zero(d, tol):
        return None

    a = x1 * y2 - y1 * x2
    b = x3 * y4 - y3 * x4
    x = (a * (x3 - x4) - (x1 - x2) * b) / d
    y = (a * (y3 - y4) - (y1 - y2) * b) / d

    return [x, y, 0.0]


def intersection_line_segment_xy(line, segment, tol=None):
    """Compute the intersection between a line and a segment.

    Parameters
    ----------
    line : [point, point] | :class:`compas.geometry.Line`
        A line defined by two points, with at least XY coordinates.
    segment : [point, point] | :class:`compas.geometry.Line`
        A segment defined by two points, with at least XY coordinates.
    tol : float, optional
        Tolerance for computing the intersection between the line and the underlying line of the segment,
        and for verifying that the point is on the segment.
        Default is :attr:`TOL.absolute`.

    Returns
    -------
    [float, float, 0.0] | None
        XYZ coordinates of the intersection, if one exists, with Z = 0.
        None otherwise.

    """
    x = intersection_line_line_xy(line, segment, tol=tol)
    if x:
        if is_point_on_segment_xy(x, segment, tol=tol):
            return x


def intersection_line_box_xy(line, box, tol=None):
    """Compute the intersection between a line and a box in the XY plane.

    Parameters
    ----------
    line : [point, point] | :class:`compas.geometry.Line`
        A line defined by two points, with at least XY coordinates.
    box : [point, point, point, point]
        A box defined by 4 points, with at least XY coordinates.
    tol : float, optional
        A tolerance value for point comparison.
        Default is :attr:`TOL.absolute`.

    Returns
    -------
    tuple[[float, float, 0.0], [float, float, 0.0]] | [float, float, 0.0] | None
        Two points if the line goes through the box.
        One point if the line goes through one of the box vertices only.
        None otherwise.

    """
    points = []
    for segment in pairwise(box + box[:1]):
        x = intersection_line_segment_xy(line, segment, tol=tol)
        if x:
            points.append(x)

    if len(points) < 3:
        return tuple(points)

    if len(points) == 3:
        a, b, c = points

        if TOL.is_allclose(a, b, rtol=0, atol=tol):
            return a, c

        if TOL.is_allclose(b, c, rtol=0, atol=tol):
            return a, b

        return b, c


def intersection_polyline_box_xy(polyline, box, tol=None):
    """Compute the intersection between a polyline and a box in the XY plane.

    Parameters
    ----------
    polyline : sequence[point] | :class:`compas.geometry.Polyline`
        A polyline defined by a sequence of points, with at least XY coordinates.
    box : [point, point, point, point]
        A box defined by a sequence of 4 points, with at least XY coordinates.
    tol : float, optional
        A tolerance value for point comparison.

    Returns
    -------
    list[[float, float, 0.0]]
        A list of intersection points.

    """
    precision = TOL.precision_from_tolerance(tol)
    points = []
    for side in pairwise(box + box[:1]):
        for segment in pairwise(polyline):
            x = intersection_segment_segment_xy(side, segment, tol=tol)
            if x:
                points.append(x)
    points = {TOL.geometric_key(point, precision): point for point in points}
    return list(points.values())


def intersection_segment_segment_xy(ab, cd, tol=None):
    """Compute the intersection of two lines segments, assuming they lie in the XY plane.

    Parameters
    ----------
    ab : [point, point] | :class:`compas.geometry.Line`
        A segment defined by two points, with at least XY coordinates.
    cd : [point, point] | :class:`compas.geometry.Line`
        A segment defined by two points, with at least XY coordinates.
    tol : float, optional
        A tolerance for verifying that the point lies on both segments.
        Default is :attr:`TOL.absolute`.

    Returns
    -------
    [float, float, 0.0] | None
        XYZ coordinates of intersection point if one exists.
        None otherwise.

    """
    intx_pt = intersection_line_line_xy(ab, cd, tol=tol)

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
    circle1 : [plane, float]
        Circle defined by a plane, with at least XY coordinates, and a radius.
    circle2 : [plane, float]
        Circle defined by a plane, with at least XY coordinates, and a radius.

    Returns
    -------
    tuple[[float, float, float], [float, float, float]] | None
        The intersection points if there are any.
        If the circles are tangent to each other, the two intersection points are identical.
        None otherwise.

    """
    plane1, r1 = circle1
    plane2, r2 = circle2
    p1, n1 = plane1
    p2, n2 = plane2
    R = length_vector_xy(subtract_vectors_xy(p2, p1))

    if R > r1 + r2:
        return None

    if R < fabs(r1 - r2):
        return None

    if (R == 0) and (r1 == r2):
        return None

    x1, y1 = p1[:2]
    x2, y2 = p2[:2]

    cx = 0.5 * (x1 + x2)
    cy = 0.5 * (y2 + y1)

    R2 = R * R
    R4 = R2 * R2

    a = (r1 * r1 - r2 * r2) / (2 * R2)
    b = 0.5 * sqrt(2 * (r1 * r1 + r2 * r2) / R2 - (r1 * r1 - r2 * r2) ** 2 / R4 - 1)

    i1 = cx + a * (x2 - x1) + b * (y2 - y1), cy + a * (y2 - y1) + b * (x1 - x2), 0
    i2 = cx + a * (x2 - x1) - b * (y2 - y1), cy + a * (y2 - y1) - b * (x1 - x2), 0

    return i1, i2


def intersection_segment_polyline_xy(segment, polyline, tol=None):
    """
    Calculate the intersection point of a segment and a polyline on the XY-plane.

    Parameters
    ----------
    segment : [point, point] | :class:`compas.geometry.Line`
        A line segment defined by two points, with at least XY coordinates.
    polyline : sequence[point] | :class:`compas.geometry.Polyline`
        A polyline defined by a sequence of points, with at least XY coordinates.
    tol : float, optional
        Tolerance for computing the intersection points between the segment and the polyline segments.
        Default is :attr:`TOL.absolute`.

    Returns
    -------
    [float, float, 0.0] | None
        XYZ coordinates of the first intersection point if one exists.
        None otherwise

    Examples
    --------
    >>> from compas.geometry import is_point_on_polyline_xy
    >>> from compas.geometry import is_point_on_segment_xy
    >>> from compas.geometry import distance_point_point
    >>> p = [(0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (2.0, 0.0, 0.0)]
    >>> s = [(0.5, -0.5, 0.0), (0.5, 0.5, 0.0)]
    >>> x = intersection_segment_polyline_xy(s, p)
    >>> is_point_on_polyline_xy(x, p)
    True
    >>> is_point_on_segment_xy(x, s)
    True
    >>> distance_point_point((0.5, 0.0, 0.0), x) < 1e-6
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
    ellipse : tuple[float, float]
        The major and minor of the ellipse.
    line : [point, point] | :class:`compas.geometry.Line`
        A line defined by two points, with at least XY coordinates.

    Returns
    -------
    tuple[[float, float, float], [float, float, float]] | [float, float, float] | None
        Two points, if the line goes through the ellipse.
        One point, if the line is tangent to the ellipse.
        None, otherwise.

    References
    ----------
    Based on [1]_.

    .. [1] C# Helper. *Calculate where a line segment and an ellipse intersect in C#*.
           Available at: http://csharphelper.com/blog/2017/08/calculate-where-a-line-segment-and-an-ellipse-intersect-in-c/

    Examples
    --------
    >>> ellipse = 6.0, 2.5
    >>> p1 = (4.1, 2.8, 0.0)
    >>> p2 = (3.4, -3.1, 0.0)
    >>> i1, i2 = intersection_ellipse_line_xy(ellipse, [p1, p2])

    """
    x1, y1 = line[0][0], line[0][1]
    x2, y2 = line[1][0], line[1][1]

    a, b = ellipse

    A = (x2 - x1) ** 2 / a**2 + (y2 - y1) ** 2 / b**2
    B = 2 * x1 * (x2 - x1) / a**2 + 2 * y1 * (y2 - y1) / b**2
    C = x1**2 / a**2 + y1**2 / b**2 - 1

    discriminant = B**2 - 4 * A * C
    if discriminant == 0:
        t = -B / (2 * A)
        return (x1 + (x2 - x1) * t, y1 + (y2 - y1) * t, 0.0)
    elif discriminant > 0:
        t1 = (-B + sqrt(discriminant)) / (2 * A)
        t2 = (-B - sqrt(discriminant)) / (2 * A)
        p1 = (x1 + (x2 - x1) * t1, y1 + (y2 - y1) * t1, 0.0)
        p2 = (x1 + (x2 - x1) * t2, y1 + (y2 - y1) * t2, 0.0)
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
