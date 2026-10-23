from itertools import chain
from typing import TYPE_CHECKING

from compas._typing import CoordinatesType
from compas._typing import MeshType
from compas._typing import RayMeshHit
from compas._typing import RayType
from compas._typing import SphereType
from compas.itertools import pairwise
from compas.plugins import PluginNotInstalledError
from compas.plugins import pluggable
from compas.tolerance import TOL

from ._core.intersections import closest_points_line_line as _closest_points_line_line_raw
from ._core.intersections import intersection_circle_circle_xy as _intersection_circle_circle_xy
from ._core.intersections import intersection_ellipse_line_xy as _intersection_ellipse_line_xy
from ._core.intersections import intersection_line_line_xy as _intersection_line_line_xy
from ._core.intersections import intersection_line_plane as _intersection_line_plane_raw
from ._core.intersections import intersection_line_triangle as _intersection_line_triangle
from ._core.intersections import intersection_plane_circle as _intersection_plane_circle
from ._core.intersections import intersection_plane_plane as _intersection_plane_plane
from ._core.intersections import intersection_segment_plane as _intersection_segment_plane
from ._core.intersections import intersection_sphere_line as _intersection_sphere_line
from ._core.intersections import intersection_sphere_sphere as _intersection_sphere_sphere
from ._core.predicates_2 import is_point_on_segment_xy
from ._core.predicates_3 import is_point_on_segment
from ._typing import CircleType
from ._typing import LineType
from ._typing import PlaneType
from ._typing import PolylineType
from ._typing import TriangleType
from .intersection import IntersectionResult

if TYPE_CHECKING:
    from .curves.circle import Circle
    from .line import Line
    from .point import Point
    from .shapes.sphere import Sphere


def intersection_line_line(
    l1: LineType,
    l2: LineType,
    tol: float | None = None,
) -> "IntersectionResult[Point]":
    """Compute the intersection of two lines.

    Parameters
    ----------
    l1
        Two points defining the first line.
    l2
        Two points defining the second line.
    tol
        Tolerance for determining whether the closest points coincide.

    Returns
    -------
    IntersectionResult[Point]
        The unique intersection point, or an empty result if the lines are
        skew, parallel, or coincident.

    Examples
    --------
    >>> l1 = [0, 0, 0], [1, 0, 0]
    >>> l2 = [0, 0, 0], [0, 1, 0]
    >>> intersection_line_line(l1, l2)[0]
    Point(x=0.000, y=0.000, z=0.000)

    """
    a, b = l1
    c, d = l2
    point1, point2 = _closest_points_line_line_raw((a, b), (c, d), tol=tol)
    if point1 is None or point2 is None or not TOL.is_allclose(point1, point2, rtol=0, atol=tol):
        return IntersectionResult()
    from .point import Point

    return IntersectionResult((Point(point1[0], point1[1], point1[2]),))


def intersection_segment_segment(
    ab: LineType,
    cd: LineType,
    tol: float | None = None,
) -> "IntersectionResult[Point]":
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
    IntersectionResult[Point]
        The unique intersection point, or an empty result otherwise.

    Examples
    --------
    >>> s1 = [0, 0, 0], [1, 0, 0]
    >>> s2 = [0, 0, 0], [0, 1, 0]
    >>> intersection_segment_segment(s1, s2)[0]
    Point(x=0.000, y=0.000, z=0.000)

    """
    a, b = ab
    c, d = cd
    x1, x2 = _closest_points_line_line_raw((a, b), (c, d), tol=tol)

    if x1 is None or x2 is None:
        return IntersectionResult()
    if not TOL.is_allclose(x1, x2, rtol=0, atol=tol):
        return IntersectionResult()
    if not is_point_on_segment(x1, ab, tol=tol) or not is_point_on_segment(x2, cd, tol=tol):
        return IntersectionResult()
    from .point import Point

    return IntersectionResult((Point(x1[0], x1[1], x1[2]),))


def intersection_line_segment(
    line: LineType,
    segment: LineType,
    tol: float | None = None,
) -> "IntersectionResult[Point]":
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
    IntersectionResult[Point]
        The unique intersection point, or an empty result otherwise.

    """
    a, b = line
    c, d = segment
    x1, x2 = _closest_points_line_line_raw((a, b), (c, d), tol=tol)

    if x1 is None or x2 is None:
        return IntersectionResult()
    if not TOL.is_allclose(x1, x2, rtol=0, atol=tol) or not is_point_on_segment(x2, segment, tol=tol):
        return IntersectionResult()
    from .point import Point

    return IntersectionResult((Point(x1[0], x1[1], x1[2]),))


def intersection_line_plane(line: LineType, plane: PlaneType, tol: float | None = None) -> "IntersectionResult[Point]":
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
    IntersectionResult[Point]
        The intersection point, or an empty result if the line and plane are
        parallel.

    See Also
    --------
    [`intersection_segment_plane`][compas.geometry.intersection_segment_plane] and
    [`intersection_polyline_plane`][compas.geometry.intersection_polyline_plane].

    """
    a, b = line
    origin, normal = plane
    point = _intersection_line_plane_raw((a, b), (origin, normal), tol=tol)
    if point is None:
        return IntersectionResult()
    from .point import Point

    return IntersectionResult((Point(point[0], point[1], point[2]),))


def intersection_segment_plane(segment: LineType, plane: PlaneType, tol: float | None = None) -> "IntersectionResult[Point]":
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
    IntersectionResult[Point]
        The intersection point, or an empty result if the segment does not
        intersect the plane.

    See Also
    --------
    [`intersection_line_plane`][compas.geometry.intersection_line_plane] and
    [`intersection_polyline_plane`][compas.geometry.intersection_polyline_plane].

    """
    a, b = segment
    origin, normal = plane
    point = _intersection_segment_plane((a, b), (origin, normal), tol=tol)
    if point is None:
        return IntersectionResult()
    from .point import Point

    return IntersectionResult((Point(point[0], point[1], point[2]),))


def intersection_polyline_plane(
    polyline: PolylineType,
    plane: PlaneType,
    expected_number_of_intersections: int | None = None,
    tol: float | None = None,
) -> "IntersectionResult[Point]":
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
    IntersectionResult[Point]
        The intersection points between the polyline segments and the plane.

    See Also
    --------
    [`intersection_segment_plane`][compas.geometry.intersection_segment_plane] and
    [`intersection_line_plane`][compas.geometry.intersection_line_plane].

    """
    if expected_number_of_intersections is not None and expected_number_of_intersections < 0:
        raise ValueError("The expected number of intersections cannot be negative.")
    origin, normal = plane
    intersections: list[list[float]] = []
    for segment in pairwise(polyline):
        if expected_number_of_intersections is not None and len(intersections) >= expected_number_of_intersections:
            break
        point = _intersection_segment_plane(segment, (origin, normal), tol)
        if point is not None:
            intersections.append(point)
    from .point import Point

    return IntersectionResult(tuple(Point(point[0], point[1], point[2]) for point in intersections))


def intersection_line_triangle(line: LineType, triangle: TriangleType, tol: float | None = None) -> "IntersectionResult[Point]":
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
    IntersectionResult[Point]
        The intersection point, or an empty result if the line does not
        intersect the triangle.

    """
    a, b = line
    p1, p2, p3 = triangle
    x = _intersection_line_triangle((a, b), (p1, p2, p3), tol=tol)

    if x is not None:
        from .point import Point

        return IntersectionResult((Point(x[0], x[1], x[2]),))
    return IntersectionResult()


def intersection_plane_plane(
    plane1: PlaneType,
    plane2: PlaneType,
    tol: float | None = None,
) -> "IntersectionResult[Line]":
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
    IntersectionResult[Line]
        The line of intersection, or an empty result if the planes are
        parallel.

    """
    origin1, normal1 = plane1
    origin2, normal2 = plane2
    line = _intersection_plane_plane((origin1, normal1), (origin2, normal2), tol=tol)
    if line is None:
        return IntersectionResult()
    from .line import Line

    return IntersectionResult((Line(line[0], line[1]),))


def intersection_plane_plane_plane(
    plane1: PlaneType,
    plane2: PlaneType,
    plane3: PlaneType,
    tol: float | None = None,
) -> "IntersectionResult[Point]":
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
    IntersectionResult[Point]
        The intersection point, or an empty result if the planes have no unique
        common intersection.

    Notes
    -----
    Currently this only computes a unique intersection point. If two planes
    are parallel, their possible intersection with the third plane is not
    returned.[^intersection-three-planes]

    References
    ----------
    [^intersection-three-planes]: [Intersection of Three Planes](http://geomalgorithms.com/Pic_3-planes.gif)

    """
    origin1, normal1 = plane1
    origin2, normal2 = plane2
    line = _intersection_plane_plane((origin1, normal1), (origin2, normal2), tol=tol)
    if line is not None:
        origin, normal = plane3
        point = _intersection_line_plane_raw(line, (origin, normal), tol=tol)
        if point is not None:
            from .point import Point

            return IntersectionResult((Point(point[0], point[1], point[2]),))
    return IntersectionResult()


def intersection_sphere_sphere(
    sphere1: SphereType,
    sphere2: SphereType,
    tol: float | None = None,
) -> "IntersectionResult[Point | Circle | Sphere]":
    """Compute the intersection of two spheres.

    Parameters
    ----------
    sphere1
        The first sphere, defined by a center point and radius.
    sphere2
        The second sphere, defined by a center point and radius.
    tol
        Tolerance for classifying tangent and coincident spheres.

    Returns
    -------
    IntersectionResult[Point | Circle | Sphere]
        A point for tangent spheres, a circle for intersecting spheres, a
        sphere for coincident spheres, or an empty result otherwise.

    Examples
    --------
    >>> result = intersection_sphere_sphere(((0, 0, 0), 1.0), ((2, 0, 0), 1.0))
    >>> result[0]
    Point(x=1.000, y=0.000, z=0.000)

    """
    result = _intersection_sphere_sphere(sphere1, sphere2, tol=tol)
    if result is None:
        return IntersectionResult()

    if result[0] == "point":
        from .point import Point

        point = result[1]
        return IntersectionResult((Point(point[0], point[1], point[2]),))

    if result[0] == "circle":
        from .curves.circle import Circle
        from .plane import Plane

        center, radius, normal = result[1]
        return IntersectionResult((Circle.from_plane_and_radius(Plane(center, normal), radius),))

    from .shapes.sphere import Sphere

    center, radius = result[1]
    return IntersectionResult((Sphere.from_point_and_radius(center, radius),))


def intersection_segment_polyline(
    segment: LineType,
    polyline: PolylineType,
    tol: float | None = None,
) -> "IntersectionResult[Point]":
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
    IntersectionResult[Point]
        The first intersection point, or an empty result otherwise.

    Examples
    --------
    >>> p = [(0.0, 0.0, 0.0), (1.0, 0.0, 0.5), (2.0, 0.5, 1.0)]
    >>> s = [(0.5, 0.0, 0.0), (0.5, 0.0, 2.0)]
    >>> intersection_segment_polyline(s, p)[0]
    Point(x=0.500, y=0.000, z=0.250)

    """
    for cd in pairwise(polyline):
        result = intersection_segment_segment(segment, cd, tol)
        if result:
            return result
    return IntersectionResult()


def intersection_sphere_line(
    sphere: SphereType,
    line: LineType,
    tol: float | None = None,
) -> "IntersectionResult[Point]":
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
    IntersectionResult[Point]
        Two points if the line crosses the sphere, one point if the line is
        tangent to the sphere, or an empty result otherwise.

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
    start, end = line
    points = _intersection_sphere_line(sphere, (start, end), tol=tol)
    if points is None:
        return IntersectionResult()
    from .point import Point

    if len(points) == 3:
        return IntersectionResult((Point(points[0], points[1], points[2]),))
    return IntersectionResult(
        (
            Point(points[0][0], points[0][1], points[0][2]),
            Point(points[1][0], points[1][1], points[1][2]),
        )
    )


def intersection_plane_circle(
    plane: PlaneType,
    circle: CircleType,
    tol: float | None = None,
) -> "IntersectionResult[Point]":
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
    IntersectionResult[Point]
        Two points for a secant intersection, one point for a tangent
        intersection, or an empty result otherwise.

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
    Point(x=-10.0, y=0.0, z=0.0)
    >>> x2
    Point(x=10.0, y=0.0, z=0.0)

    """
    origin, normal = plane
    circle_plane, radius = circle
    circle_origin, circle_normal = circle_plane
    points = _intersection_plane_circle((origin, normal), ((circle_origin, circle_normal), radius), tol=tol)
    if points is None:
        return IntersectionResult()
    from .point import Point

    if len(points) == 3:
        return IntersectionResult((Point(points[0], points[1], points[2]),))
    return IntersectionResult(
        (
            Point(points[0][0], points[0][1], points[0][2]),
            Point(points[1][0], points[1][1], points[1][2]),
        )
    )


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


# ==============================================================================
# XY
# ==============================================================================


def intersection_line_line_xy(l1: LineType, l2: LineType, tol: float | None = None) -> "IntersectionResult[Point]":
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
    IntersectionResult[Point]
        The unique intersection point with Z = 0, or an empty result if the
        lines are parallel or coincident.

    """
    a, b = l1
    c, d = l2
    point = _intersection_line_line_xy((a, b), (c, d), tol=tol)
    if point is None:
        return IntersectionResult()

    from .point import Point

    return IntersectionResult((Point(point[0], point[1], point[2]),))


def intersection_line_segment_xy(
    line: LineType,
    segment: LineType,
    tol: float | None = None,
) -> "IntersectionResult[Point]":
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
    IntersectionResult[Point]
        The unique intersection point with Z = 0, or an empty result.

    """
    result = intersection_line_line_xy(line, segment, tol=tol)
    if result and is_point_on_segment_xy(result[0], segment, tol=tol):
        return result
    return IntersectionResult()


def intersection_line_box_xy(
    line: LineType,
    box: CoordinatesType,
    tol: float | None = None,
) -> "IntersectionResult[Point]":
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
    IntersectionResult[Point]
        The unique intersection points in box-edge order.

    Raises
    ------
    ValueError
        If the box does not have four corners.

    """
    if len(box) != 4:
        raise ValueError("An XY box requires exactly four corners.")

    points: list[Point] = []
    for segment in pairwise(chain(box, (box[0],))):
        result = intersection_line_segment_xy(line, segment, tol=tol)
        if result and not any(TOL.is_allclose(result[0], point, rtol=0.0, atol=tol) for point in points):
            points.append(result[0])
    return IntersectionResult(tuple(points))


def intersection_polyline_box_xy(
    polyline: PolylineType,
    box: CoordinatesType,
    tol: float | None = None,
) -> "IntersectionResult[Point]":
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
    IntersectionResult[Point]
        The unique intersection points in box-edge order.

    Raises
    ------
    ValueError
        If the box does not have four corners.

    """
    if len(box) != 4:
        raise ValueError("An XY box requires exactly four corners.")

    points: list[Point] = []
    for side in pairwise(chain(box, (box[0],))):
        for segment in pairwise(polyline):
            result = intersection_segment_segment_xy(side, segment, tol=tol)
            if result and not any(TOL.is_allclose(result[0], point, rtol=0.0, atol=tol) for point in points):
                points.append(result[0])
    return IntersectionResult(tuple(points))


def intersection_segment_segment_xy(
    ab: LineType,
    cd: LineType,
    tol: float | None = None,
) -> "IntersectionResult[Point]":
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
    IntersectionResult[Point]
        The unique intersection point with Z = 0, or an empty result.

    """
    result = intersection_line_line_xy(ab, cd, tol=tol)
    if not result:
        return result
    point = result[0]

    if not is_point_on_segment_xy(point, ab, tol=tol):
        return IntersectionResult()

    if not is_point_on_segment_xy(point, cd, tol=tol):
        return IntersectionResult()

    return result


def intersection_circle_circle_xy(
    circle1: CircleType,
    circle2: CircleType,
    tol: float | None = None,
) -> "IntersectionResult[Point | Circle]":
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
    IntersectionResult[Point | Circle]
        The one or two intersection points, the coincident circle, or an empty
        result if the circles do not intersect.

    Raises
    ------
    ValueError
        If either radius is not positive.

    """
    plane1, radius1 = circle1
    plane2, radius2 = circle2
    center1, normal1 = plane1
    center2, normal2 = plane2
    result = _intersection_circle_circle_xy(((center1, normal1), radius1), ((center2, normal2), radius2), tol=tol)
    if result is None:
        return IntersectionResult()
    if result[0] == "circle":
        from .curves.circle import Circle
        from .plane import Plane

        center, radius, normal = result[1]
        return IntersectionResult((Circle.from_plane_and_radius(Plane(center, normal), radius),))
    from .point import Point

    if result[0] == "point":
        point = result[1]
        return IntersectionResult((Point(point[0], point[1], point[2]),))
    point1, point2 = result[1]
    return IntersectionResult((Point(point1[0], point1[1], point1[2]), Point(point2[0], point2[1], point2[2])))


def intersection_segment_polyline_xy(
    segment: LineType,
    polyline: PolylineType,
    tol: float | None = None,
) -> "IntersectionResult[Point]":
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
    IntersectionResult[Point]
        The first intersection point with Z = 0, or an empty result.

    Examples
    --------
    >>> from compas.geometry import is_point_on_polyline_xy
    >>> from compas.geometry import is_point_on_segment_xy
    >>> from compas.geometry import distance_point_point
    >>> p = [(0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (2.0, 0.0, 0.0)]
    >>> s = [(0.5, -0.5, 0.0), (0.5, 0.5, 0.0)]
    >>> point = intersection_segment_polyline_xy(s, p)[0]
    >>> is_point_on_polyline_xy(point, p)
    True
    >>> is_point_on_segment_xy(point, s)
    True
    >>> distance_point_point((0.5, 0.0, 0.0), point) < 1e-6
    True

    """
    for cd in pairwise(polyline):
        result = intersection_segment_segment_xy(segment, cd, tol)
        if result:
            return result
    return IntersectionResult()


def intersection_ellipse_line_xy(
    ellipse: tuple[float, float],
    line: LineType,
    tol: float | None = None,
) -> "IntersectionResult[Point]":
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
    IntersectionResult[Point]
        The one or two intersection points, or an empty result.

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
    start, end = line
    points = _intersection_ellipse_line_xy(ellipse, (start, end), tol=tol)
    if points is None:
        return IntersectionResult()
    from .point import Point

    if len(points) == 3:
        return IntersectionResult((Point(points[0], points[1], points[2]),))
    point1, point2 = points
    return IntersectionResult((Point(point1[0], point1[1], point1[2]), Point(point2[0], point2[1], point2[2])))


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
