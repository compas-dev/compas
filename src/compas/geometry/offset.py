from collections.abc import Iterable
from collections.abc import Sequence
from typing import Any

from compas._typing import CoordinatesType
from compas._typing import CoordinateType
from compas.data.validators import is_item_iterable
from compas.geometry import centroid_points
from compas.geometry import is_colinear
from compas.geometry import normal_polygon
from compas.itertools import iterable_like
from compas.itertools import pairwise
from compas.linalg.vectors import add_vectors
from compas.linalg.vectors import cross_vectors
from compas.linalg.vectors import normalize_vector
from compas.linalg.vectors import scale_vector
from compas.linalg.vectors import subtract_vectors

from ._core.intersections import closest_points_line_line
from ._typing import LineType
from ._typing import PolygonType
from ._typing import PolylineType

_LineDistance = float | Sequence[float]
_OffsetDistance = float | Sequence[float | Sequence[float]]


def intersect_lines(l1: LineType, l2: LineType, tol: float | None) -> list[float] | None:
    a, b = l1
    c, d = l2
    x1, x2 = closest_points_line_line((a, b), (c, d), tol)
    if x1 and x2:
        return centroid_points([x1, x2])


def intersect_lines_colinear(l1: LineType, l2: LineType, tol: float | None) -> list[float] | None:
    def are_segments_colinear(l1: LineType, l2: LineType, tol: float | None) -> bool:
        a, b = l1
        d, c = l2
        return is_colinear(a, b, c, tol)

    if are_segments_colinear(l1, l2, tol):
        return centroid_points([l1[1], l2[0]])


def intersect(l1: LineType, l2: LineType, tol: float | None) -> list[float]:
    supported_funcs = [intersect_lines, intersect_lines_colinear]
    for func in supported_funcs:
        point = func(l1, l2, tol)
        if point:
            return point
    msg = f"Intersection not found for line: {l1}, and line: {l2}"
    raise ValueError(msg)


def offset_segments(
    point_list: CoordinatesType,
    distances: Iterable[_LineDistance],
    normal: CoordinateType,
) -> list[tuple[list[float], list[float]]]:
    segments: list[tuple[list[float], list[float]]] = []
    for line, distance in zip(pairwise(point_list), distances):
        segments.append(offset_line(line, distance, normal))
    return segments


def offset_line(
    line: LineType,
    distance: _LineDistance,
    normal: CoordinateType = (0.0, 0.0, 1.0),
) -> tuple[list[float], list[float]]:
    """Offset a line by a distance.

    Parameters
    ----------
    line
        A line defined by two points.
    distance
        The offset distance.
        A single value determines a constant offset.
        Two values create a variable offset at the start and end.
    normal
        The normal of the offset plane.

    Returns
    -------
    tuple[list[float], list[float]]
        Two points defining the offset line.

    See Also
    --------
    [`offset_polyline`][compas.geometry.offset_polyline]
    [`offset_polygon`][compas.geometry.offset_polygon]

    Notes
    -----
    The offset direction is chosen such that if the line were along the positive
    X axis and the normal of the offset plane is along the positive Z axis, the
    offset line is in the direction of the positive Y axis.

    """

    a, b = line
    ab = subtract_vectors(b, a)
    direction = normalize_vector(cross_vectors(normal, ab))

    distance_values: Any = distance
    if not is_item_iterable(distance_values):
        distance_values = [distance_values]
    distances = list(iterable_like(line, distance_values, distance_values[-1]))

    u = scale_vector(direction, distances[0])
    v = scale_vector(direction, distances[1])
    c = add_vectors(a, u)
    d = add_vectors(b, v)
    return c, d


def offset_polygon(
    polygon: PolygonType,
    distance: _OffsetDistance,
    tol: float | None = None,
) -> list[list[float]]:
    """Offset a polygon (closed) by a distance.

    Parameters
    ----------
    polygon
        The XYZ coordinates of the corners of the polygon.
        The first and last coordinates must not be identical.
    distance
        The offset distance.
        A single value determines a constant offset globally.
        A list of pairs of local offset values per line segment can be used to create variable offsets.
    tol
        A tolerance value for intersection calculations.
        Default is `TOL.absolute`.

    Returns
    -------
    list[list[float]]
        The XYZ coordinates of the corners of the offset polygon.

    See Also
    --------
    [`offset_polyline`][compas.geometry.offset_polyline]
    [`offset_line`][compas.geometry.offset_line]

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
    >>> polygon = Polygon([(0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (1.0, 1.0, 0.0), (0.0, 1.0, 0.0)])
    >>> offsetted_polygon = offset_polygon(polygon, 0.5)
    >>> offsetted_polygon
    [[0.5, 0.5, 0.0], [0.5, 0.5, 0.0], [0.5, 0.5, 0.0], [0.5, 0.5, 0.0]]

    """
    normal = normal_polygon(polygon)

    distance_values: Any = distance
    if not is_item_iterable(distance_values):
        distance_values = [distance_values]
    distances = iterable_like(polygon, distance_values, distance_values[-1])

    points = list(polygon)
    points += points[:1]
    segments = offset_segments(points, distances, normal)

    offset = []
    for s1, s2 in pairwise(segments[-1:] + segments):
        point = intersect(s1, s2, tol)
        offset.append(point)

    return offset


def offset_polyline(
    polyline: PolylineType,
    distance: _OffsetDistance,
    normal: CoordinateType = (0.0, 0.0, 1.0),
    tol: float | None = None,
) -> list[list[float]]:
    """Offset a polyline by a distance.

    Parameters
    ----------
    polyline
        The XYZ coordinates of the vertices of a polyline.
    distance
        The offset distance.
        A single value determines a constant offset globally.
        Alternatively, pairs of local offset values per line segment can be used to create variable offsets.
    normal
        The normal of the offset plane.
    tol
        A tolerance value for intersection calculations.
        Default is `TOL.absolute`.

    Returns
    -------
    list[list[float]]
        The XYZ coordinates of the resulting polyline.

    See Also
    --------
    [`offset_polygon`][compas.geometry.offset_polygon]
    [`offset_line`][compas.geometry.offset_line]

    Notes
    -----
    The offset direction is determined by the provided normal vector.
    If the polyline is in the XY plane and the normal is along the positive Z axis,
    positive offset distances will result in counterclockwise offsets,
    and negative values in clockwise direction.

    """

    distance_values: Any = distance
    if not is_item_iterable(distance_values):
        distance_values = [distance_values]
    distances = iterable_like(polyline, distance_values, distance_values[-1])
    segments = offset_segments(polyline, distances, normal)

    offset = [segments[0][0]]
    for s1, s2 in pairwise(segments):
        point = intersect(s1, s2, tol)
        offset.append(point)
    offset.append(segments[-1][1])

    return offset
