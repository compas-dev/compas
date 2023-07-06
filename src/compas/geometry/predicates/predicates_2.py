from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry import distance_point_point_xy
from compas.geometry import distance_point_line_xy
from compas.geometry import closest_point_on_segment_xy


def is_ccw_xy(a, b, c, colinear=False):
    """Determine if c is on the left of ab when looking from a to b,
    and assuming that all points lie in the XY plane.

    Parameters
    ----------
    a : [float, float, float] | :class:`~compas.geometry.Point`
        Base point defined by XY(Z) coordinates.
    b : [float, float, float] | :class:`~compas.geometry.Point`
        First end point defined by XY(Z) coordinates.
    c : [float, float, float] | :class:`~compas.geometry.Point`
        Second end point defined by XY(Z) coordinates.
    colinear : bool, optional
        If True, colinear points will return a positive result.

    Returns
    -------
    bool
        True if ccw.
        False otherwise.

    References
    ----------
    For more info, see [1]_.

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
        return ab_x * ac_y - ab_y * ac_x >= 0
    return ab_x * ac_y - ab_y * ac_x > 0


def is_colinear_xy(a, b, c):
    """Determine if three points are colinear on the XY-plane.

    Parameters
    ----------
    a : [float, float, float] | :class:`~compas.geometry.Point`
        Point 1 defined by XY(Z) coordinates.
    b : [float, float, float] | :class:`~compas.geometry.Point`
        Point 2 defined by XY(Z) coordinates.
    c : [float, float, float] | :class:`~compas.geometry.Point`
        Point 3 defined by XY(Z) coordinates.

    Returns
    -------
    bool
        True if the points are colinear.
        False otherwise.

    """
    ab_x = b[0] - a[0]
    ab_y = b[1] - a[1]
    ac_x = c[0] - a[0]
    ac_y = c[1] - a[1]
    return ab_x * ac_y == ab_y * ac_x


def is_polygon_convex_xy(polygon, colinear=False):
    """Determine if the polygon is convex on the XY-plane.

    Parameters
    ----------
    polygon : sequence[point] | :class:`~compas.geometry.Polygon`
        The XY(Z) coordinates of the corners of a polygon.
        The vertices are assumed to be in order.
        The polygon is assumed to be closed: the first and last vertex in the sequence should not be the same.
    colinear : bool, optional
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


def is_point_on_line_xy(point, line, tol=1e-6):
    """Determine if a point lies on a line on the XY-plane.

    Parameters
    ----------
    point : [float, float, float] | :class:`~compas.geometry.Point`
        XY(Z) coordinates of a point.
    line : [point, point] | :class:`~compas.geometry.Line`
        XY(Z) coordinates of two points defining a line.
    tol : float, optional
        A tolerance for membership verification.

    Returns
    -------
    bool
        True if the point is in on the line.
        False otherwise.

    """
    return distance_point_line_xy(point, line) <= tol


def is_point_on_segment_xy(point, segment, tol=1e-6):
    """Determine if a point lies on a given line segment on the XY-plane.

    Parameters
    ----------
    point : [float, float, float] | :class:`~compas.geometry.Point`
        XY(Z) coordinates of a point.
    segment : [point, point] | :class:`~compas.geometry.Line`
        XY(Z) coordinates of two points defining a segment.
    tol : float, optional
        A tolerance for membership verification.

    Returns
    -------
    bool
        True if the point is on the line segment.
        False otherwise.

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


def is_point_on_polyline_xy(point, polyline, tol=1e-6):
    """Determine if a point is on a polyline on the XY-plane.

    Parameters
    ----------
    point : [float, float, float] | :class:`~compas.geometry.Point`
        XY(Z) coordinates.
    polyline : sequence[point] | :class:`~compas.geometry.Polyline`
        XY(Z) coordinates of the points of the polyline.
    tol : float, optional
        The tolerance for membership verification.

    Returns
    -------
    bool
        True if the point is on the polyline.
        False otherwise.

    """
    for i in range(len(polyline) - 1):
        a = polyline[i]
        b = polyline[i + 1]
        c = closest_point_on_segment_xy(point, (a, b))

        if distance_point_point_xy(point, c) <= tol:
            return True

    return False


def is_point_in_triangle_xy(point, triangle, colinear=False):
    """Determine if a point is in the interior of a triangle lying on the XY-plane.

    Parameters
    ----------
    point : [float, float, float] | :class:`~compas.geometry.Point`
        XY(Z) coordinates of a point.
    triangle : [point, point, point]
        XY(Z) coordinates of the corners of the triangle.
    colinear : bool, optional
        Allow points to be colinear.

    Returns
    -------
    bool
        True if the point is in the convex polygon.
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
    """Determine if a point is in the interior of a convex polygon lying on the XY-plane.

    Parameters
    ----------
    point : [float, float, float] | :class:`~compas.geometry.Point`
        XY(Z) coordinates of a point (Z will be ignored).
    polygon : sequence[point] | :class:`~compas.geometry.Polygon`
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
    """Determine if a point is in the interior of a polygon lying on the XY-plane.

    Parameters
    ----------
    point : [float, float, float] | :class:`~compas.geometry.Point`
        XY(Z) coordinates of a point (Z will be ignored).
    polygon : sequence[point] | :class:`~compas.geometry.Polygon`
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


def is_point_in_circle_xy(point, circle):
    """Determine if a point lies in a circle lying on the XY-plane.

    Parameters
    ----------
    point : [float, float, float] | :class:`~compas.geometry.Point`
        XY(Z) coordinates of a point (Z will be ignored).
    circle : [[point, vector], float] | :class:`~compas.geometry.Circle`
        Center and radius of the circle on the XY plane.

    Returns
    -------
    bool
        True if the point lies in the circle.
        False otherwise.

    """
    dis = distance_point_point_xy(point, circle[0][0])
    if dis <= circle[1]:
        return True
    return False


def is_polygon_in_polygon_xy(polygon1, polygon2):
    """Determine if a polygon is in the interior of another polygon on the XY-plane.

    Parameters
    ----------
    polygon1 : sequence[point] | :class:`~compas.geometry.Polygon`
        List of XY(Z) coordinates of points representing the locations of the corners of the exterior polygon (Z will be ignored).
        The vertices are assumed to be in order. The polygon is assumed to be closed:
        the first and last vertex in the sequence should not be the same.
    polygon2 : sequence[point] | :class:`~compas.geometry.Polygon`
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


def polygon_to_polygon_relationship_xy(polygon1, polygon2):
    """Determine if a polygon (polygon1) is inside, intersects, is outside or contains another polygon (polygon2) on the XY-plane.

    Parameters
    ----------
    polygon1 : sequence[point] | :class:`~compas.geometry.Polygon`
        List of XY(Z) coordinates of points representing the locations of the corners of the polygon to examine the position regarding the boundary polygon (Z will be ignored).
        The vertices are assumed to be in order. The polygon is assumed to be closed:
        the first and last vertex in the sequence should not be the same.
    polygon2 : sequence[point] | :class:`~compas.geometry.Polygon`
        List of XY(Z) coordinates of points representing the locations of the corners of the boundary polygon (Z will be ignored).
        The vertices are assumed to be in order. The polygon is assumed to be closed:
        the first and last vertex in the sequence should not be the same.

    Returns
    -------
    int
        1 if polygon1 is inside polygon2.
        0 if polygon1 intersects polygon2.
        -1 if polygon1 is outside polygon2.
        -2 if polygon1 contains polygon2 (polygon2 is inside polygon1).
    """
    for i in range(len(polygon1)):
        line1 = [polygon1[i], polygon1[i - 1]]
        for j in range(len(polygon2)):
            line2 = [polygon2[j], polygon2[j - 1]]
            if is_intersection_segment_segment_xy(line1, line2):
                return 0
    for pt in polygon1:
        if is_point_in_polygon_xy(pt, polygon2):
            return 1
    if is_point_in_polygon_xy(polygon2.centroid, polygon1):
        return -2
    return -1


def point_to_polygon_relationship_xy(point, polygon, tolerance=10**-6):
    """Determine if a point is inside, outside or on the boundary (with tolerance) of a polygon in the XY-plane.

    Parameters
    ----------
    point : [float, float, float] | :class:`~compas.geometry.Point`
            XY(Z) coordinates of a point (Z will be ignored).
    polygon : sequence[point] | :class:`~compas.geometry.Polygon`
        List of XY(Z) coordinates of points representing the locations of the corners of the boundary polygon (Z will be ignored).
        The vertices are assumed to be in order. The polygon is assumed to be closed:
        the first and last vertex in the sequence should not be the same.

    Returns
    -------
    int
        1 if point is inside polygon.
        0 if point is on the boundary of polygon.
        -1 if point is outside polygon.
    """
    x, y = point[0], point[1]
    polygon = [(p[0], p[1]) for p in polygon]  # make 2D
    flag = -1
    for i in range(-1, len(polygon) - 1):
        x1, y1 = polygon[i]
        x2, y2 = polygon[i + 1]
        segment = ([x1, y1], [x2, y2])
        if is_point_on_segment_xy(point, segment, tolerance):
            return 0
        elif y > min(y1, y2):
            if y <= max(y1, y2):
                if x <= max(x1, x2):
                    if y1 != y2:
                        xinters = (y - y1) * (x2 - x1) / (y2 - y1) + x1
                    if x1 == x2 or x <= xinters:
                        flag = -flag
    return flag


def is_intersection_polygon_polygon_xy(polygon1, polygon2):
    """Determines if two polygons intersect, assuming they lie in the XY plane.

    Parameters
    ----------
    polygon1 : sequence[point] | :class:`~compas.geometry.Polygon`
        A Polygon lying in the XY.
    polygon2 : sequence[point] | :class:`~compas.geometry.Polygon`
        A Polygon lying in the XY.

    Returns
    -------
    bool
        True if the polygons intersect. False if they don't.

    Examples
    --------
    >>> from compas.geometry import Polygon
    >>> polygon1 = Polygon([[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0]])
    >>> polygon2 = Polygon([[0.5, 0.5], [1.5, 0.5], [1.5, 1.5], [0.5, 1.5]])
    >>> is_intersection_polygon_polygon_xy(polygon1, polygon2)
    True

    >>> from compas.geometry import Polygon
    >>> polygon1 = Polygon([[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0]])
    >>> polygon2 = Polygon([[1.5, 1.5], [2.5, 1.5], [2.5, 2.5], [1.5, 2.5]])
    >>> is_intersection_polygon_polygon_xy(polygon1, polygon2)
    False
    """
    for i in range(len(polygon1)):
        line1 = [polygon1[i], polygon1[i - 1]]
        for j in range(len(polygon2)):
            line2 = [polygon2[j], polygon2[j - 1]]
            if is_intersection_segment_segment_xy(line1, line2):
                return True
    return False


def is_intersection_line_line_xy(l1, l2, tol=1e-6):
    """Verifies if two lines intersect on the XY-plane.

    Parameters
    ----------
    l1 : [point, point] | :class:`~compas.geometry.Line`
        XY(Z) coordinates of two points defining a line.
    l2 : [point, point] | :class:`~compas.geometry.Line`
        XY(Z) coordinates of two points defining a line.
    tol : float, optional
        A tolerance for intersection verification.

    Returns
    -------
    bool
        True if the lines intersect in one point
        False if the lines are skew, parallel or lie on top of each other.

    """
    raise NotImplementedError


def is_intersection_segment_segment_xy(ab, cd):
    """Determines if two segments, ab and cd, intersect.

    Parameters
    ----------
    ab : [point, point] | :class:`~compas.geometry.Line`
        Two points representing the start and end points of a segment.
        Z coordinates will be ignored.
    cd : [point, point] | :class:`~compas.geometry.Line`
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
