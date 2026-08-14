from typing import Any
from typing import Optional
from typing import Sequence

from compas.geometry import closest_point_on_segment_xy
from compas.geometry import distance_point_line_xy
from compas.geometry import distance_point_point_xy
from compas.tolerance import TOL

from compas.geometry._typing import CoordinatesType
from compas.geometry._typing import CoordinateType

# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# Fundamental
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================


def is_ccw_xy(a: CoordinateType, b: CoordinateType, c: CoordinateType, colinear: bool = False) -> bool:
    """Determine if c is on the left of ab when looking from a to b,
    and assuming that all points lie in the XY plane.

    Parameters
    ----------
    a
        Base point defined by XY(Z) coordinates.
    b
        First end point defined by XY(Z) coordinates.
    c
        Second end point defined by XY(Z) coordinates.
    colinear
        If True, colinear points will return a positive result.

    Returns
    -------
    bool
        True if ccw.
        False otherwise.

    See Also
    --------
    [`is_colinear_xy`][compas.geometry.is_colinear_xy]

    Notes
    -----
    This follows the orientation test described by Marsh.[^is-ccw-xy-marsh]

    References
    ----------
    [^is-ccw-xy-marsh]: Marsh, C. [*Computational Geometry in Python: From Theory to Application*](https://www.toptal.com/python/computational-geometry-in-python-from-theory-to-implementation).

    Examples
    --------
    >>> print(is_ccw_xy([0, 0, 0], [0, 1, 0], [-1, 0, 0]))
    True

    >>> print(is_ccw_xy([0, 0, 0], [0, 1, 0], [+1, 0, 0]))
    False

    >>> print(is_ccw_xy([0, 0, 0], [1, 0, 0], [2, 0, 0]))
    False

    >>> print(is_ccw_xy([0, 0, 0], [1, 0, 0], [2, 0, 0], True))
    True

    """
    ab_x = b[0] - a[0]
    ab_y = b[1] - a[1]
    ac_x = c[0] - a[0]
    ac_y = c[1] - a[1]
    if colinear:
        return ab_x * ac_y - ab_y * ac_x >= 0
    return ab_x * ac_y - ab_y * ac_x > 0


def is_colinear_xy(a: Sequence[float], b: Sequence[float], c: Sequence[float]) -> bool:
    """Determine if three points are colinear on the XY-plane.

    Parameters
    ----------
    a
        Point 1 defined by XY(Z) coordinates.
    b
        Point 2 defined by XY(Z) coordinates.
    c
        Point 3 defined by XY(Z) coordinates.

    Returns
    -------
    bool
        True if the points are colinear.
        False otherwise.

    See Also
    --------
    [`is_ccw_xy`][compas.geometry.is_ccw_xy]

    """
    ab_x = b[0] - a[0]
    ab_y = b[1] - a[1]
    ac_x = c[0] - a[0]
    ac_y = c[1] - a[1]
    return ab_x * ac_y == ab_y * ac_x


# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# Parallel, Perpendicular
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
# Convexity
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================


def is_polygon_convex_xy(polygon: Sequence[Sequence[float]], colinear: bool = False) -> bool:
    """Determine if the polygon is convex on the XY-plane.

    Parameters
    ----------
    polygon
        The XY(Z) coordinates of the corners of a polygon.
        The vertices are assumed to be in order.
        The polygon is assumed to be closed: the first and last vertex in the sequence should not be the same.
    colinear
        Are points allowed to be colinear?

    Returns
    -------
    bool
        True if the polygon is convex.
        False otherwise.

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


# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# Containment (Curves)
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================


def is_point_on_line_xy(point: Sequence[float], line: Sequence[Sequence[float]], tol: Optional[float] = None) -> bool:
    """Determine if a point lies on a line on the XY-plane.

    Parameters
    ----------
    point
        XY(Z) coordinates of a point.
    line
        XY(Z) coordinates of two points defining a line.
    tol
        The tolerance for comparing the distance between point and line to zero.
        Default is `TOL.absolute`.

    Returns
    -------
    bool
        True if the point is in on the line.
        False otherwise.

    See Also
    --------
    [`is_point_on_segment_xy`][compas.geometry.is_point_on_segment_xy]
    [`is_point_on_polyline_xy`][compas.geometry.is_point_on_polyline_xy]

    """
    return TOL.is_zero(distance_point_line_xy(point, line), tol)


def is_point_on_segment_xy(point: Sequence[float], segment: Sequence[Sequence[float]], tol: Optional[float] = None) -> bool:
    """Determine if a point lies on a given line segment on the XY-plane.

    Parameters
    ----------
    point
        XY(Z) coordinates of a point.
    segment
        XY(Z) coordinates of two points defining a segment.
    tol
        The tolerance for comparing the distance between point and segment to zero.
        Default is `TOL.absolute`.

    Returns
    -------
    bool
        True if the point is on the line segment.
        False otherwise.

    See Also
    --------
    [`is_point_on_line_xy`][compas.geometry.is_point_on_line_xy]
    [`is_point_on_polyline_xy`][compas.geometry.is_point_on_polyline_xy]

    """
    a, b = segment

    if not is_point_on_line_xy(point, segment, tol=tol):
        return False

    d_ab = distance_point_point_xy(a, b)

    if d_ab == 0:
        return False

    d_pa = distance_point_point_xy(a, point)
    d_pb = distance_point_point_xy(b, point)

    if TOL.is_close(d_pa + d_pb, d_ab, atol=tol):
        return True

    return False


def is_point_on_polyline_xy(point: Sequence[float], polyline: Sequence[Sequence[float]], tol: Optional[float] = None) -> bool:
    """Determine if a point is on a polyline on the XY-plane.

    Parameters
    ----------
    point
        XY(Z) coordinates.
    polyline
        XY(Z) coordinates of the points of the polyline.
    tol
        The tolerance for comparing the distance between point and polyline to zero.
        Default is `TOL.absolute`.

    Returns
    -------
    bool
        True if the point is on the polyline.
        False otherwise.

    See Also
    --------
    [`is_point_on_line_xy`][compas.geometry.is_point_on_line_xy]
    [`is_point_on_segment_xy`][compas.geometry.is_point_on_segment_xy]

    """
    for i in range(len(polyline) - 1):
        a = polyline[i]
        b = polyline[i + 1]
        c = closest_point_on_segment_xy(point, (a, b))

        if TOL.is_zero(distance_point_point_xy(point, c), tol):
            return True

    return False


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


def is_point_in_triangle_xy(point: Sequence[float], triangle: Sequence[Sequence[float]], colinear: bool = False) -> bool:
    """Determine if a point is in the interior of a triangle lying on the XY-plane.

    Parameters
    ----------
    point
        XY(Z) coordinates of a point.
    triangle
        XY(Z) coordinates of the corners of the triangle.
    colinear
        Allow points to be colinear.

    Returns
    -------
    bool
        True if the point is in the convex polygon.
        False otherwise.

    See Also
    --------
    [`is_point_in_convex_polygon_xy`][compas.geometry.is_point_in_convex_polygon_xy]
    [`is_point_in_polygon_xy`][compas.geometry.is_point_in_polygon_xy]
    [`is_point_in_circle_xy`][compas.geometry.is_point_in_circle_xy]

    """
    a, b, c = triangle
    ccw = is_ccw_xy(c, a, point, colinear)

    if ccw != is_ccw_xy(a, b, point, colinear):
        return False

    if ccw != is_ccw_xy(b, c, point, colinear):
        return False

    return True


def is_point_in_convex_polygon_xy(point: CoordinateType, polygon: CoordinatesType) -> bool:
    """Determine if a point is in the interior of a convex polygon lying on the XY-plane.

    Parameters
    ----------
    point
        XY(Z) coordinates of a point (Z will be ignored).
    polygon
        A sequence of XY(Z) coordinates of points representing the locations of the corners of a polygon (Z will be ignored).
        The vertices are assumed to be in order. The polygon is assumed to be closed:
        the first and last vertex in the sequence should not be the same.

    Returns
    -------
    bool
        True if the point is in the convex polygon
        False otherwise.

    Warnings
    --------
    Does not work for concave polygons.

    See Also
    --------
    [`is_point_in_triangle_xy`][compas.geometry.is_point_in_triangle_xy]
    [`is_point_in_polygon_xy`][compas.geometry.is_point_in_polygon_xy]
    [`is_point_in_circle_xy`][compas.geometry.is_point_in_circle_xy]

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


def is_point_in_polygon_xy(point: CoordinateType, polygon: CoordinatesType) -> bool:
    """Determine if a point is in the interior of a polygon lying on the XY-plane.

    Parameters
    ----------
    point
        XY(Z) coordinates of a point (Z will be ignored).
    polygon
        A sequence of XY(Z) coordinates of points representing the locations of the corners of a polygon (Z will be ignored).
        The vertices are assumed to be in order.
        The polygon is assumed to be closed.
        The first and last vertex in the sequence should not be the same.

    Returns
    -------
    bool
        True if the point is in the polygon.
        False otherwise.

    Warnings
    --------
    A boundary check is not yet implemented. This should include a tolerance value.

    See Also
    --------
    [`is_point_in_triangle_xy`][compas.geometry.is_point_in_triangle_xy]
    [`is_point_in_convex_polygon_xy`][compas.geometry.is_point_in_convex_polygon_xy]
    [`is_point_in_circle_xy`][compas.geometry.is_point_in_circle_xy]

    """
    x, y = point[0], point[1]
    polygon = [(p[0], p[1]) for p in polygon]  # make 2D
    inside = False
    for i in range(-1, len(polygon) - 1):
        x1, y1 = polygon[i]
        x2, y2 = polygon[i + 1]
        if y1 != y2:
            xinters = (y - y1) * (x2 - x1) / (y2 - y1) + x1
        else:
            xinters = None
        if y > min(y1, y2):
            if y <= max(y1, y2):
                if x <= max(x1, x2):
                    if x1 == x2 or (xinters is not None and x <= xinters):
                        inside = not inside
    return inside


def is_point_in_circle_xy(point: Sequence[float], circle: Sequence[Any]) -> bool:
    """Determine if a point lies in a circle lying on the XY-plane.

    Parameters
    ----------
    point
        XY(Z) coordinates of a point (Z will be ignored).
    circle
        Center and radius of the circle on the XY plane.

    Returns
    -------
    bool
        True if the point lies in the circle.
        False otherwise.

    See Also
    --------
    [`is_point_in_triangle_xy`][compas.geometry.is_point_in_triangle_xy]
    [`is_point_in_convex_polygon_xy`][compas.geometry.is_point_in_convex_polygon_xy]
    [`is_point_in_polygon_xy`][compas.geometry.is_point_in_polygon_xy]

    """
    dis = distance_point_point_xy(point, circle[0][0])
    if dis <= circle[1]:
        return True
    return False


def is_polygon_in_polygon_xy(polygon1: Sequence[Sequence[float]], polygon2: Sequence[Sequence[float]]) -> bool:
    """Determine if a polygon is in the interior of another polygon on the XY-plane.

    Parameters
    ----------
    polygon1
        List of XY(Z) coordinates of points representing the locations of the corners of the exterior polygon (Z will be ignored).
        The vertices are assumed to be in order. The polygon is assumed to be closed:
        the first and last vertex in the sequence should not be the same.
    polygon2
        List of XY(Z) coordinates of points representing the locations of the corners of the interior polygon (Z will be ignored).
        The vertices are assumed to be in order. The polygon is assumed to be closed:
        the first and last vertex in the sequence should not be the same.

    Returns
    -------
    bool
        True if polygon2 is inside polygon1.
        False otherwise.

    """
    if is_polygon_convex_xy(polygon1) and is_polygon_convex_xy(polygon2):
        for pt in polygon2:
            if not is_point_in_convex_polygon_xy(pt, polygon1):
                return False
        return True
    else:
        for i in range(len(polygon1)):
            line = [polygon1[-i], polygon1[-i - 1]]
            for j in range(len(polygon2)):
                line_ = [polygon2[-j], polygon2[-j - 1]]
                if is_intersection_segment_segment_xy(line, line_):
                    return False
        for pt in polygon2:
            if is_point_in_polygon_xy(pt, polygon1):
                return True
        return False


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


def is_intersection_line_line_xy(l1: Sequence[Sequence[float]], l2: Sequence[Sequence[float]], tol: Optional[float] = None) -> bool:
    """Verifies if two lines intersect on the XY-plane.

    Parameters
    ----------
    l1
        XY(Z) coordinates of two points defining a line.
    l2
        XY(Z) coordinates of two points defining a line.
    tol
        A tolerance for intersection verification.

    Returns
    -------
    bool
        True if the lines intersect in one point
        False if the lines are skew, parallel or lie on top of each other.

    """
    raise NotImplementedError


def is_intersection_segment_segment_xy(ab: Sequence[Sequence[float]], cd: Sequence[Sequence[float]]) -> bool:
    """Determines if two segments, ab and cd, intersect.

    Parameters
    ----------
    ab
        Two points representing the start and end points of a segment.
        Z coordinates will be ignored.
    cd
        Two points representing the start and end points of a segment.
        Z coordinates will be ignored.

    Returns
    -------
    bool
        True if the segments intersect.
        False otherwise.

    Notes
    -----
    The segments intersect if both of the following conditions are true:

    * `c` is on the left of `ab`, and `d` is on the right, or vice versa.
    * `d` is on the left of `ac`, and on the right of `bc`, or vice versa.

    """
    a, b = ab
    c, d = cd
    return is_ccw_xy(a, c, d) != is_ccw_xy(b, c, d) and is_ccw_xy(a, b, c) != is_ccw_xy(a, b, d)
