from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.data.validators import is_item_iterable
from compas.geometry import add_vectors
from compas.geometry import centroid_points
from compas.geometry import cross_vectors
from compas.geometry import intersection_line_line
from compas.geometry import is_colinear
from compas.geometry import normal_polygon
from compas.geometry import normalize_vector
from compas.geometry import scale_vector
from compas.geometry import subtract_vectors
from compas.itertools import iterable_like
from compas.itertools import pairwise


def intersect_lines(l1, l2, tol):
    x1, x2 = intersection_line_line(l1, l2, tol)
    if x1 and x2:
        return centroid_points([x1, x2])


def intersect_lines_colinear(l1, l2, tol):
    def are_segments_colinear(l1, l2, tol):
        a, b = l1
        d, c = l2
        return is_colinear(a, b, c, tol)

    if are_segments_colinear(l1, l2, tol):
        return centroid_points([l1[1], l2[0]])


def intersect(l1, l2, tol):
    supported_funcs = [intersect_lines, intersect_lines_colinear]
    for func in supported_funcs:
        point = func(l1, l2, tol)
        if point:
            return point
    msg = "Intersection not found for line: {}, and line: {}".format(l1, l2)
    raise ValueError(msg)


def offset_segments(point_list, distances, normal):
    segments = []
    for line, distance in zip(pairwise(point_list), distances):
        segments.append(offset_line(line, distance, normal))
    return segments


def offset_line(line, distance, normal=[0.0, 0.0, 1.0]):
    """Offset a line by a distance.

    Parameters
    ----------
    line : [point, point] | :class:`compas.geometry.Line`
        A line defined by two points.
    distances : float or list[float]
        The offset distance as float.
        A single value determines a constant offset.
        A list of two offset values can be used to a create variable offset at the start and end.
    normal : [float, float, float] | :class:`compas.geometry.Vector`, optional
        The normal of the offset plane.

    Returns
    -------
    tuple[[float, float, float], [float, float, float]]
        Two points defining the offset line.

    See Also
    --------
    offset_polyline
    offset_polygon

    Notes
    -----
    The offset direction is chosen such that if the line were along the positve
    X axis and the normal of the offset plane is along the positive Z axis, the
    offset line is in the direction of the postive Y axis.

    """

    a, b = line
    ab = subtract_vectors(b, a)
    direction = normalize_vector(cross_vectors(normal, ab))

    if not is_item_iterable(distance):
        distance = [distance]
    distances = list(iterable_like(line, distance, distance[-1]))

    u = scale_vector(direction, distances[0])
    v = scale_vector(direction, distances[1])
    c = add_vectors(a, u)
    d = add_vectors(b, v)
    return c, d


def offset_polygon(polygon, distance, tol=None):
    """Offset a polygon (closed) by a distance.

    Parameters
    ----------
    polygon : sequence[point] | :class:`compas.geometry.Polygon`
        The XYZ coordinates of the corners of the polygon.
        The first and last coordinates must not be identical.
    distance : float | list[tuple[float, float]]
        The offset distance as float.
        A single value determines a constant offset globally.
        A list of pairs of local offset values per line segment can be used to create variable offsets.
    tol : float, optional
        A tolerance value for intersection calculations.
        Default is :attr:`TOL.absolute`.

    Returns
    -------
    list[[float, float, float]]
        The XYZ coordinates of the corners of the offset polygon.
        The first and last coordinates are identical.

    See Also
    --------
    offset_polyline
    offset_line

    Notes
    -----
    The offset direction is determined by the normal of the polygon.
    If the polygon is in the XY plane and the normal is along the positive Z axis,
    positive offset distances will result in an offset towards the inside of the
    polygon.

    The algorithm works also for spatial polygons that do not perfectly fit a plane.

    Examples
    --------
    >>> from compas.geometry import Polygon
    >>> polygon = Polygon([(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)])
    >>> offsetted_polygon = offset_polygon(polygon, 0.5)
    >>> offsetted_polygon
    [[0.5, 0.5, 0.0], [0.5, 0.5, 0.0], [0.5, 0.5, 0.0], [0.5, 0.5, 0.0]]

    """
    normal = normal_polygon(polygon)

    if not is_item_iterable(distance):
        distance = [distance]
    distances = iterable_like(polygon, distance, distance[-1])

    polygon = polygon[:] + polygon[:1]
    segments = offset_segments(polygon, distances, normal)

    offset = []
    for s1, s2 in pairwise(segments[-1:] + segments):
        point = intersect(s1, s2, tol)
        offset.append(point)

    return offset


def offset_polyline(polyline, distance, normal=[0.0, 0.0, 1.0], tol=None):
    """Offset a polyline by a distance.

    Parameters
    ----------
    polyline : sequence[point] | :class:`compas.geometry.Polyline`
        The XYZ coordinates of the vertices of a polyline.
    distance : float | list[tuple[float, float]]
        The offset distance as float.
        A single value determines a constant offset globally.
        Alternatively, pairs of local offset values per line segment can be used to create variable offsets.
    normal : [float, float, float] | :class:`compas.geometry.Vector`, optional
        The normal of the offset plane.
    tol : float, optional
        A tolerance value for intersection calculations.
        Default is :attr:`TOL.absolute`.

    Returns
    -------
    list[[float, float, float]]
        The XYZ coordinates of the resulting polyline.

    See Also
    --------
    offset_polygon
    offset_line

    Notes
    -----
    The offset direction is determined by the provided normal vector.
    If the polyline is in the XY plane and the normal is along the positive Z axis,
    positive offset distances will result in counterclockwise offsets,
    and negative values in clockwise direction.

    """

    if not is_item_iterable(distance):
        distance = [distance]
    distances = iterable_like(polyline, distance, distance[-1])
    segments = offset_segments(polyline, distances, normal)

    offset = [segments[0][0]]
    for s1, s2 in pairwise(segments):
        point = intersect(s1, s2, tol)
        offset.append(point)
    offset.append(segments[-1][1])

    return offset
