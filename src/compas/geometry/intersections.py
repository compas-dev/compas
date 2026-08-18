from itertools import chain
from math import fabs
from math import sqrt
from typing import Literal
from typing import Optional
from typing import Union

from compas._typing import CoordinatesType
from compas._typing import CoordinateType
from compas.itertools import pairwise
from compas.linalg.vectors import add_vectors
from compas.linalg.vectors import cross_vectors
from compas.linalg.vectors import dot_vectors
from compas.linalg.vectors import length_vector
from compas.linalg.vectors import length_vector_xy
from compas.linalg.vectors import normalize_vector
from compas.linalg.vectors import scale_vector
from compas.linalg.vectors import subtract_vectors
from compas.linalg.vectors import subtract_vectors_xy
from compas.plugins import PluginNotInstalledError
from compas.plugins import pluggable
from compas.tolerance import TOL

from ._core.distance import distance_point_point
from ._core.predicates_2 import is_point_on_segment_xy
from ._core.predicates_3 import is_point_in_triangle
from ._core.predicates_3 import is_point_on_segment
from ._typing import CircleType
from ._typing import LineType
from ._typing import MeshType
from ._typing import PlaneType
from ._typing import PolylineType
from ._typing import RayMeshHit
from ._typing import RayType
from ._typing import SphereType
from ._typing import TriangleType


def intersection_line_line(
    l1: LineType,
    l2: LineType,
    tol: Optional[float] = None,
) -> tuple[Optional[list[float]], Optional[list[float]]]:
    """Compute the closest points between two lines.

    Parameters
    ----------
    l1
        Two points defining the first line.
    l2
        Two points defining the second line.
    tol
        Tolerance for evaluating the intersection points of each of the lines with the corresponding skew plane.
        Default is `TOL.absolute`.

    Returns
    -------
    tuple[Optional[list[float]], Optional[list[float]]]
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
    if TOL.is_zero(length_vector(n), tol):
        return None, None
    n1 = normalize_vector(cross_vectors(ab, n))
    n2 = normalize_vector(cross_vectors(cd, n))

    plane_1 = (a, n1)
    plane_2 = (c, n2)

    i1 = intersection_line_plane(l1, plane_2, tol=tol)
    i2 = intersection_line_plane(l2, plane_1, tol=tol)

    if i1 is None or i2 is None:
        return None, None

    return i1, i2


def intersection_segment_segment(
    ab: LineType,
    cd: LineType,
    tol: Optional[float] = None,
) -> tuple[Optional[list[float]], Optional[list[float]]]:
    """Compute the intersection of two lines segments.

    Parameters
    ----------
    ab
        Two points defining a line segment.
    cd
        Two points defining another line segment.
    tol
        Tolerance value for computing the intersection points of the underlying lines,
        and for verifying that those points are contained by the segments.
        Default is `TOL.absolute`.

    Returns
    -------
    tuple[Optional[list[float]], Optional[list[float]]]
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

    if x1 is None or x2 is None:
        return None, None

    if not is_point_on_segment(x1, ab, tol=tol):
        return None, None

    if not is_point_on_segment(x2, cd, tol=tol):
        return None, None

    return x1, x2


def intersection_line_segment(
    line: LineType,
    segment: LineType,
    tol: Optional[float] = None,
) -> tuple[Optional[list[float]], Optional[list[float]]]:
    """Compute the intersection of a line and a segment.

    Parameters
    ----------
    line
        Two points defining a line.
    segment
        Two points defining a line segment.
    tol
        Tolerance value for computing the intersection points of the underlying lines,
        and for verifying that those points are contained by the segment.
        Default is `TOL.absolute`.

    Returns
    -------
    tuple[Optional[list[float]], Optional[list[float]]]
        Two intersection points.
        If the line and segment intersect and the second intersection point lies on the segment, the two points are identical.
        If the line and segment are skew and the second apparent intersection point lies on the segment, the two points are different.
        In all other cases there are no intersection points.

    """
    x1, x2 = intersection_line_line(line, segment, tol=tol)

    if x1 is None or x2 is None:
        return None, None

    if not is_point_on_segment(x2, segment, tol=tol):
        return None, None

    return x1, x2


def intersection_line_plane(line: LineType, plane: PlaneType, tol: Optional[float] = None) -> Optional[list[float]]:
    """Compute the intersection point of a line and a plane.

    Parameters
    ----------
    line
        Two points defining the line.
    plane
        The base point and normal defining the plane.
    tol
        Tolerance for evaluating that the dot product of the line direction and the plane normal is zero.
        Default is `TOL.absolute`.

    Returns
    -------
    Optional[list[float]]
        The intersection point between the line and the plane,
        or None if the line and the plane are parallel.

    See Also
    --------
    [`intersection_segment_plane`][compas.geometry.intersection_segment_plane] and
    [`intersection_polyline_plane`][compas.geometry.intersection_polyline_plane].

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


def intersection_segment_plane(segment: LineType, plane: PlaneType, tol: Optional[float] = None) -> Optional[list[float]]:
    """Compute the intersection point of a line segment and a plane.

    Parameters
    ----------
    segment
        Two points defining the line segment.
    plane
        The base point and normal defining the plane.
    tol
        Tolerance for evaluating that the dot product of the line direction and the plane normal is zero.
        Default is `TOL.absolute`.

    Returns
    -------
    Optional[list[float]]
        The intersection point between the line and the plane,
        or None if the line and the plane are parallel.

    See Also
    --------
    [`intersection_line_plane`][compas.geometry.intersection_line_plane] and
    [`intersection_polyline_plane`][compas.geometry.intersection_polyline_plane].

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

    if 0.0 <= ratio <= 1.0:
        ab = scale_vector(ab, ratio)
        return add_vectors(a, ab)

    return None


def intersection_polyline_plane(
    polyline: PolylineType,
    plane: PlaneType,
    expected_number_of_intersections: Optional[int] = None,
    tol: Optional[float] = None,
) -> list[list[float]]:
    """Compute the intersections of a polyline and a plane.

    Parameters
    ----------
    polyline
        Polyline to test intersection.
    plane
        Plane to compute intersection.
    expected_number_of_intersections
        Maximum number of intersections to return.
        Default is all intersections.
    tol
        Tolerance for computing the intersection points between the individual segments of the polyline and the plane.
        Default is `TOL.absolute`.

    Returns
    -------
    list[list[float]]
        The intersection points between the polyline segments and the plane.

    See Also
    --------
    [`intersection_segment_plane`][compas.geometry.intersection_segment_plane] and
    [`intersection_line_plane`][compas.geometry.intersection_line_plane].

    """
    if expected_number_of_intersections is not None and expected_number_of_intersections < 0:
        raise ValueError("The expected number of intersections cannot be negative.")
    intersections: list[list[float]] = []
    for segment in pairwise(polyline):
        if expected_number_of_intersections is not None and len(intersections) >= expected_number_of_intersections:
            break
        point = intersection_segment_plane(segment, plane, tol)
        if point is not None:
            intersections.append(point)
    return intersections


def intersection_line_triangle(line: LineType, triangle: TriangleType, tol: Optional[float] = None) -> Optional[list[float]]:
    """Compute the intersection point of a line and a triangle.

    Parameters
    ----------
    line
        Two points defining the line.
    triangle
        XYZ coordinates of the triangle corners.
    tol
        Tolerance value for computing the intersection between the line and the plane of the triangle.
        Default is `TOL.absolute`.

    Returns
    -------
    Optional[list[float]]
        The intersection point between the line and the triangle,
        or None if the line and the plane are parallel.

    """
    a, b, c = triangle
    ab = subtract_vectors(b, a)
    ac = subtract_vectors(c, a)
    n = cross_vectors(ab, ac)
    plane = a, n

    x = intersection_line_plane(line, plane, tol=tol)

    if x is not None and is_point_in_triangle(x, triangle):
        return x
    return None


def intersection_plane_plane(
    plane1: PlaneType,
    plane2: PlaneType,
    tol: Optional[float] = None,
) -> Optional[tuple[list[float], list[float]]]:
    """Compute the intersection of two planes.

    Parameters
    ----------
    plane1
        The base point and normal (normalized) defining the 1st plane.
    plane2
        The base point and normal (normalized) defining the 2nd plane.
    tol
        Tolerance for evaluating whether the plane normals are parallel.
        Default is `TOL.absolute`.

    Returns
    -------
    Optional[tuple[list[float], list[float]]]
        Two points defining the intersection line.
        None if the planes are parallel.

    """
    o1, n1 = plane1
    o2, n2 = plane2

    # direction of intersection line
    d = cross_vectors(n1, n2)
    if TOL.is_zero(length_vector(d), tol):
        return None
    # vector in plane 1 perpendicular to the direction of the intersection line
    v1 = cross_vectors(d, n1)
    # point on plane 1
    p1 = add_vectors(o1, v1)

    x1 = intersection_line_plane((o1, p1), plane2, tol=tol)
    if x1 is None:
        return None
    x2 = add_vectors(x1, d)
    return x1, x2


def intersection_plane_plane_plane(
    plane1: PlaneType,
    plane2: PlaneType,
    plane3: PlaneType,
    tol: Optional[float] = None,
) -> Optional[list[float]]:
    """Compute the intersection of three planes.

    Parameters
    ----------
    plane1
        The base point and normal (normalized) defining the 1st plane.
    plane2
        The base point and normal (normalized) defining the 2nd plane.
    plane3
        The base point and normal (normalized) defining the 3rd plane.
    tol
        Tolerance for computing the intersection line between the first two planes, and between the intersection line and the third plane.
        Default is `TOL.absolute`.

    Returns
    -------
    Optional[list[float]]
        The intersection point
        or None if at least one pair of planes is parallel.

    Notes
    -----
    Currently this only computes a unique intersection point. If two planes
    are parallel, their possible intersection with the third plane is not
    returned.[^intersection-three-planes]

    References
    ----------
    [^intersection-three-planes]: [Intersection of Three Planes](http://geomalgorithms.com/Pic_3-planes.gif)

    """
    line = intersection_plane_plane(plane1, plane2, tol=tol)
    if line is not None:
        return intersection_line_plane(line, plane3, tol=tol)
    return None


def intersection_sphere_sphere(
    sphere1: SphereType,
    sphere2: SphereType,
    tol: Optional[float] = None,
) -> Optional[
    Union[
        tuple[Literal["point"], list[float]],
        tuple[Literal["circle"], tuple[list[float], float, list[float]]],
        tuple[Literal["sphere"], tuple[list[float], float]],
    ]
]:
    """Compute the intersection of two spheres.

    Parameters
    ----------
    sphere1
        A sphere defined by a point and radius.
    sphere2
        A sphere defined by a point and radius.
    tol
        Tolerance for classifying tangent and coincident spheres.
        Default is `TOL.absolute`.

    Returns
    -------
    Optional[Union[tuple[Literal["point"], list[float]], tuple[Literal["circle"], tuple[list[float], float, list[float]]], tuple[Literal["sphere"], tuple[list[float], float]]]]
        The intersection type and geometry, or `None` if there is no
        intersection. Point geometry is represented by coordinates, circle
        geometry by center, radius, and normal, and coincident-sphere geometry
        by center and radius.

    Notes
    -----
    There are four cases of sphere-sphere intersection:[^intersection-sphere-sphere]

    1. the spheres intersect in a circle,
    2. they intersect in a point,
    3. they overlap,
    4. they do not intersect.

    References
    ----------
    [^intersection-sphere-sphere]: [Sphere-Sphere Intersection](https://gamedev.stackexchange.com/questions/75756/sphere-sphere-intersection-and-circle-sphere-intersection)

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

    if radius1 < 0.0 or radius2 < 0.0:
        raise ValueError("Sphere radii cannot be negative.")

    distance = distance_point_point(center1, center2)

    # Case 4: No intersection
    if distance > radius1 + radius2 and not TOL.is_close(distance, radius1 + radius2, atol=tol):
        return None

    # Case 4: No intersection, sphere is within the other sphere
    if distance + min(radius1, radius2) < max(radius1, radius2) and not TOL.is_close(distance + min(radius1, radius2), max(radius1, radius2), atol=tol):
        return None

    # Case 3: sphere's overlap
    if TOL.is_zero(distance, tol) and TOL.is_close(radius1, radius2, atol=tol):
        return "sphere", ([center1[0], center1[1], center1[2]], float(radius1))

    # Case 2: point intersection
    if TOL.is_close(radius1 + radius2, distance, atol=tol):
        ipt = subtract_vectors(center2, center1)
        ipt = scale_vector(ipt, radius1 / distance)
        ipt = add_vectors(center1, ipt)
        return "point", ipt

    # Case 2: point intersection, smaller sphere is within the bigger
    if TOL.is_close(distance + min(radius1, radius2), max(radius1, radius2), atol=tol):
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
    ri = sqrt(max(0.0, radius1**2 - h**2 * distance**2))
    normal = scale_vector(subtract_vectors(center2, center1), 1 / distance)
    return "circle", (ci, ri, normal)


def intersection_segment_polyline(
    segment: LineType,
    polyline: PolylineType,
    tol: Optional[float] = None,
) -> tuple[Optional[list[float]], Optional[list[float]]]:
    """Compute the first intersection of a segment and a polyline.

    Parameters
    ----------
    segment
        XYZ coordinates of two points defining a line segment.
    polyline
        XYZ coordinates of the points of the polyline.
    tol
        Tolerance value for computing the intersection points between the segment and the polyline segments.
        Default is `TOL.absolute`.

    Returns
    -------
    tuple[Optional[list[float]], Optional[list[float]]]
        The closest points on the intersecting segments, or `(None, None)` if
        there is no intersection.

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
        if pt[0] is not None and pt[1] is not None:
            return pt
    return None, None


def intersection_sphere_line(
    sphere: SphereType,
    line: LineType,
    tol: Optional[float] = None,
) -> Optional[Union[CoordinateType, tuple[CoordinateType, CoordinateType]]]:
    """Compute the intersection of a sphere and a line.

    Parameters
    ----------
    sphere
        A sphere defined by a point and a radius.
    line
        A line defined by two points.
    tol
        Tolerance for classifying a tangent intersection.
        Default is `TOL.absolute`.

    Returns
    -------
    Optional[Union[CoordinateType, tuple[CoordinateType, CoordinateType]]]
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

    if radius < 0.0:
        raise ValueError("The sphere radius cannot be negative.")

    a = (l2[0] - l1[0]) ** 2 + (l2[1] - l1[1]) ** 2 + (l2[2] - l1[2]) ** 2
    if TOL.is_zero(a, tol):
        raise ValueError("A line requires two distinct points.")
    b = 2.0 * ((l2[0] - l1[0]) * (l1[0] - sp[0]) + (l2[1] - l1[1]) * (l1[1] - sp[1]) + (l2[2] - l1[2]) * (l1[2] - sp[2]))

    c = sp[0] ** 2 + sp[1] ** 2 + sp[2] ** 2 + l1[0] ** 2 + l1[1] ** 2 + l1[2] ** 2 - 2.0 * (sp[0] * l1[0] + sp[1] * l1[1] + sp[2] * l1[2]) - radius**2

    i = b * b - 4.0 * a * c

    if TOL.is_zero(i, tol):  # case 2: one intersection
        i = 0.0
    elif i < 0.0:  # case 3: no intersection
        return None

    if i == 0.0:
        mu = -b / (2.0 * a)
        ipt = (
            l1[0] + mu * (l2[0] - l1[0]),
            l1[1] + mu * (l2[1] - l1[1]),
            l1[2] + mu * (l2[2] - l1[2]),
        )
        return ipt

    if i > 0.0:  # case 1: two intersections
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
    return None


def intersection_plane_circle(
    plane: PlaneType,
    circle: CircleType,
    tol: Optional[float] = None,
) -> Optional[Union[CoordinateType, tuple[CoordinateType, CoordinateType]]]:
    """Compute the intersection of a plane and a circle.

    Parameters
    ----------
    plane
        A plane defined by a point and normal vector.
    circle
        A circle defined by a plane and radius.
    tol
        Tolerance used for the plane and sphere intersections.
        Default is `TOL.absolute`.

    Returns
    -------
    Optional[Union[CoordinateType, tuple[CoordinateType, CoordinateType]]]
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
    line = intersection_plane_plane(plane, circle_plane, tol=tol)
    if line is None:
        return None
    circle_point = circle_plane[0]
    sphere = circle_point, circle_radius
    return intersection_sphere_line(sphere, line, tol=tol)


@pluggable(category="intersections")
def intersection_mesh_mesh(A: MeshType, B: MeshType) -> list[CoordinatesType]:
    """Compute the intersection of two meshes.

    Parameters
    ----------
    A
        The vertices and faces of the first mesh.
    B
        The vertices and faces of the second mesh.

    Returns
    -------
    list[CoordinatesType]
        The intersection polylines.

    Raises
    ------
    PluginNotInstalledError
        If no intersection plugin is available.

    """
    raise PluginNotInstalledError


intersection_mesh_mesh.__pluggable__ = True


@pluggable(category="intersections")
def intersection_ray_mesh(ray: RayType, mesh: MeshType) -> list[RayMeshHit]:
    """Compute the intersection(s) between a ray and a mesh.

    Parameters
    ----------
    ray
        The ray origin and direction vector.
    mesh
        The vertices and faces of the mesh.

    Returns
    -------
    list[RayMeshHit]
        For every hit, the intersected face index, the `u` and `v` barycentric
        coordinates, and the distance from the ray origin.

    Raises
    ------
    PluginNotInstalledError
        If no intersection plugin is available.

    """
    raise PluginNotInstalledError


intersection_ray_mesh.__pluggable__ = True


# ==============================================================================
# XY
# ==============================================================================


def intersection_line_line_xy(l1: LineType, l2: LineType, tol: Optional[float] = None) -> Optional[list[float]]:
    """Compute the intersection of two lines, assuming they lie on the XY plane.

    Parameters
    ----------
    l1
        A line defined by two points, with at least XY coordinates.
    l2
        A line defined by two points, with at least XY coordinates.
    tol
        Tolerance for comparing the length of the cross product of the line directions with zero.
        Default is `TOL.absolute`.

    Returns
    -------
    Optional[list[float]]
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


def intersection_line_segment_xy(
    line: LineType,
    segment: LineType,
    tol: Optional[float] = None,
) -> Optional[list[float]]:
    """Compute the intersection between a line and a segment.

    Parameters
    ----------
    line
        A line defined by two points, with at least XY coordinates.
    segment
        A segment defined by two points, with at least XY coordinates.
    tol
        Tolerance for computing the intersection between the line and the underlying line of the segment,
        and for verifying that the point is on the segment.
        Default is `TOL.absolute`.

    Returns
    -------
    Optional[list[float]]
        XYZ coordinates of the intersection, if one exists, with Z = 0.
        None otherwise.

    """
    x = intersection_line_line_xy(line, segment, tol=tol)
    if x is not None and is_point_on_segment_xy(x, segment, tol=tol):
        return x
    return None


def intersection_line_box_xy(
    line: LineType,
    box: CoordinatesType,
    tol: Optional[float] = None,
) -> list[list[float]]:
    """Compute the intersection between a line and a box in the XY plane.

    Parameters
    ----------
    line
        A line defined by two points, with at least XY coordinates.
    box
        A box defined by 4 points, with at least XY coordinates.
    tol
        A tolerance value for point comparison.
        Default is `TOL.absolute`.

    Returns
    -------
    list[list[float]]
        The unique intersection points in box-edge order.

    Raises
    ------
    ValueError
        If the box does not have four corners.

    """
    if len(box) != 4:
        raise ValueError("An XY box requires exactly four corners.")

    points: list[list[float]] = []
    for segment in pairwise(chain(box, (box[0],))):
        x = intersection_line_segment_xy(line, segment, tol=tol)
        if x is not None and not any(TOL.is_allclose(x, point, rtol=0.0, atol=tol) for point in points):
            points.append(x)
    return points


def intersection_polyline_box_xy(
    polyline: PolylineType,
    box: CoordinatesType,
    tol: Optional[float] = None,
) -> list[list[float]]:
    """Compute the intersection between a polyline and a box in the XY plane.

    Parameters
    ----------
    polyline
        A polyline defined by a sequence of points, with at least XY coordinates.
    box
        A box defined by a sequence of 4 points, with at least XY coordinates.
    tol
        A tolerance value for point comparison.

    Returns
    -------
    list[list[float]]
        A list of intersection points.

    Raises
    ------
    ValueError
        If the box does not have four corners.

    """
    if len(box) != 4:
        raise ValueError("An XY box requires exactly four corners.")

    points: list[list[float]] = []
    for side in pairwise(chain(box, (box[0],))):
        for segment in pairwise(polyline):
            x = intersection_segment_segment_xy(side, segment, tol=tol)
            if x is not None and not any(TOL.is_allclose(x, point, rtol=0.0, atol=tol) for point in points):
                points.append(x)
    return points


def intersection_segment_segment_xy(
    ab: LineType,
    cd: LineType,
    tol: Optional[float] = None,
) -> Optional[list[float]]:
    """Compute the intersection of two lines segments, assuming they lie in the XY plane.

    Parameters
    ----------
    ab
        A segment defined by two points, with at least XY coordinates.
    cd
        A segment defined by two points, with at least XY coordinates.
    tol
        A tolerance for verifying that the point lies on both segments.
        Default is `TOL.absolute`.

    Returns
    -------
    Optional[list[float]]
        XYZ coordinates of intersection point if one exists.
        None otherwise.

    """
    intx_pt = intersection_line_line_xy(ab, cd, tol=tol)

    if intx_pt is None:
        return None

    if not is_point_on_segment_xy(intx_pt, ab, tol=tol):
        return None

    if not is_point_on_segment_xy(intx_pt, cd, tol=tol):
        return None

    return intx_pt


def intersection_circle_circle_xy(
    circle1: CircleType,
    circle2: CircleType,
    tol: Optional[float] = None,
) -> Optional[tuple[tuple[float, float, float], tuple[float, float, float]]]:
    """Compute the intersection points of two circles in the XY plane.

    Parameters
    ----------
    circle1
        Circle defined by a plane, with at least XY coordinates, and a radius.
    circle2
        Circle defined by a plane, with at least XY coordinates, and a radius.
    tol
        Tolerance for classifying tangent and concentric circles.
        Default is `TOL.absolute`.

    Returns
    -------
    Optional[tuple[tuple[float, float, float], tuple[float, float, float]]]
        The intersection points if there are any.
        If the circles are tangent to each other, the two intersection points are identical.
        None otherwise.

    Raises
    ------
    ValueError
        If either radius is negative.

    """
    plane1, r1 = circle1
    plane2, r2 = circle2
    p1, _ = plane1
    p2, _ = plane2

    if r1 < 0.0 or r2 < 0.0:
        raise ValueError("Circle radii cannot be negative.")

    R = length_vector_xy(subtract_vectors_xy(p2, p1))

    if TOL.is_zero(R, tol):
        return None

    if R > r1 + r2 and not TOL.is_close(R, r1 + r2, atol=tol):
        return None

    if R < fabs(r1 - r2) and not TOL.is_close(R, fabs(r1 - r2), atol=tol):
        return None

    x1, y1 = p1[0], p1[1]
    x2, y2 = p2[0], p2[1]

    cx = 0.5 * (x1 + x2)
    cy = 0.5 * (y2 + y1)

    R2 = R * R
    R4 = R2 * R2

    a = (r1 * r1 - r2 * r2) / (2 * R2)
    discriminant = 2 * (r1 * r1 + r2 * r2) / R2 - (r1 * r1 - r2 * r2) ** 2 / R4 - 1
    b = 0.5 * sqrt(max(0.0, discriminant))

    i1 = cx + a * (x2 - x1) + b * (y2 - y1), cy + a * (y2 - y1) + b * (x1 - x2), 0
    i2 = cx + a * (x2 - x1) - b * (y2 - y1), cy + a * (y2 - y1) - b * (x1 - x2), 0

    return i1, i2


def intersection_segment_polyline_xy(
    segment: LineType,
    polyline: PolylineType,
    tol: Optional[float] = None,
) -> Optional[list[float]]:
    """Compute the first intersection of a segment and a polyline in the XY plane.

    Parameters
    ----------
    segment
        A line segment defined by two points, with at least XY coordinates.
    polyline
        A polyline defined by a sequence of points, with at least XY coordinates.
    tol
        Tolerance for computing the intersection points between the segment and the polyline segments.
        Default is `TOL.absolute`.

    Returns
    -------
    Optional[list[float]]
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
        if pt is not None:
            return pt
    return None


def intersection_ellipse_line_xy(
    ellipse: tuple[float, float],
    line: LineType,
    tol: Optional[float] = None,
) -> Optional[
    Union[
        tuple[float, float, float],
        tuple[tuple[float, float, float], tuple[float, float, float]],
    ]
]:
    """Compute the intersection of an origin-centered ellipse and a line in the XY plane.

    Parameters
    ----------
    ellipse
        The positive major and minor semi-axis lengths.
    line
        A line defined by two points, with at least XY coordinates.
    tol
        Tolerance for classifying a tangent intersection.
        Default is `TOL.absolute`.

    Returns
    -------
    Optional[Union[tuple[float, float, float], tuple[tuple[float, float, float], tuple[float, float, float]]]]
        Two points, if the line goes through the ellipse.
        One point, if the line is tangent to the ellipse.
        None, otherwise.

    Raises
    ------
    ValueError
        If either semi-axis is not positive or the line points coincide.

    References
    ----------
    Based on the method described by C# Helper.[^intersection-ellipse-line-csharp]

    [^intersection-ellipse-line-csharp]: [Calculate where a line segment and an ellipse intersect in C#](http://csharphelper.com/blog/2017/08/calculate-where-a-line-segment-and-an-ellipse-intersect-in-c/)

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

    if a <= 0.0 or b <= 0.0:
        raise ValueError("Ellipse semi-axis lengths must be positive.")

    A = (x2 - x1) ** 2 / a**2 + (y2 - y1) ** 2 / b**2
    if TOL.is_zero(A, tol):
        raise ValueError("A line requires two distinct points.")
    B = 2 * x1 * (x2 - x1) / a**2 + 2 * y1 * (y2 - y1) / b**2
    C = x1**2 / a**2 + y1**2 / b**2 - 1

    discriminant = B**2 - 4 * A * C
    if TOL.is_zero(discriminant, tol):
        t = -B / (2 * A)
        return (x1 + (x2 - x1) * t, y1 + (y2 - y1) * t, 0.0)
    if discriminant > 0:
        t1 = (-B + sqrt(discriminant)) / (2 * A)
        t2 = (-B - sqrt(discriminant)) / (2 * A)
        p1 = (x1 + (x2 - x1) * t1, y1 + (y2 - y1) * t1, 0.0)
        p2 = (x1 + (x2 - x1) * t2, y1 + (y2 - y1) * t2, 0.0)
        return p1, p2
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
