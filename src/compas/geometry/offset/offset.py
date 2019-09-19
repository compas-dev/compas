from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry import scale_vector
from compas.geometry import normalize_vector
from compas.geometry import add_vectors
from compas.geometry import subtract_vectors
from compas.geometry import cross_vectors
from compas.geometry import centroid_points
from compas.geometry import intersection_line_line
from compas.geometry import normal_polygon
from compas.geometry import is_colinear

from compas.utilities import pairwise


__all__ = [
    'offset_line',
    'offset_polyline',
    'offset_polygon',
]


def offset_line(line, distance, normal=[0.0, 0.0, 1.0]):
    """Offset a line by a distance.

    Parameters
    ----------
    line : tuple
        Two points defining the line.
    distances : float or list of floats
        The offset distance as float.
        A single value determines a constant offset. Alternatively, two
        offset values for the start and end point of the line can be used to
        a create variable offset.
    normal : vector
        The normal of the offset plane.

    Returns
    -------
    offset line : tuple
        Two points defining the offset line.

    Notes
    -----
    The offset direction is chosen such that if the line were along the positve
    X axis and the normal of the offset plane is along the positive Z axis, the
    offset line is in the direction of the postive Y axis.

    Examples
    --------
    .. code-block:: python

        line = [(0.0, 0.0, 0.0), (3.0, 3.0, 0.0)]

        distance = 0.2 # constant offset
        line_offset = offset_line(line, distance)
        print(line_offset)

        distance = [0.2, 0.1] # variable offset
        line_offset = offset_line(line, distance)
        print(line_offset)

    """

    a, b = line
    ab = subtract_vectors(b, a)
    direction = normalize_vector(cross_vectors(normal, ab))
    distances = match_value_sequence(distance, line)

    u = scale_vector(direction, distances[0])
    v = scale_vector(direction, distances[1])
    c = add_vectors(a, u)
    d = add_vectors(b, v)
    return c, d


def offset_polygon(polygon, distance, tol=1e-6):
    """Offset a polygon (closed) by a distance.

    Parameters
    ----------
    polygon : list of point
        The XYZ coordinates of the corners of the polygon.
        The first and last coordinates must not be identical.
    distance : float or list of float
        The offset distance as float.
        A single value determines a constant offset globally.
        Alternatively, pairs of local offset values per line segment can be used to create variable offsets.
        Distance > 0: offset to the outside, distance < 0: offset to the inside.

    Returns
    -------
    offset polygon : list of point
        The XYZ coordinates of the corners of the offset polygon.
        The first and last coordinates are identical.

    Notes
    -----
    The offset direction is determined by the normal of the polygon.
    If the polygon is in the XY plane and the normal is along the positive Z axis,
    positive offset distances will result in an offset towards the inside of the
    polygon.

    The algorithm works also for spatial polygons that do not perfectly fit a plane.

    Examples
    --------
    .. code-block:: python

        polygon = [
            (0.0, 0.0, 0.0),
            (3.0, 0.0, 1.0),
            (3.0, 3.0, 2.0),
            (1.5, 1.5, 2.0),
            (0.0, 3.0, 1.0),
            (0.0, 0.0, 0.0)
            ]

        distance = 0.5 # constant offset
        polygon_offset = offset_polygon(polygon, distance)
        print(polygon_offset)

        distance = [
            (0.1, 0.2),
            (0.2, 0.3),
            (0.3, 0.4),
            (0.4, 0.3),
            (0.3, 0.1)
            ] # variable offset
        polygon_offset = offset_polygon(polygon, distance)
        print(polygon_offset)

    """
    normal = normal_polygon(polygon)
    distances = match_value_sequence(distance, polygon)
    polygon = polygon + polygon[:1]
    segments = offset_segments(polygon, distances, normal)

    offset = []
    for s1, s2 in pairwise(segments[-1:] + segments):
        point = intersect(s1, s2, tol)
        offset.append(point)

    return offset


def offset_polyline(polyline, distance, normal=[0.0, 0.0, 1.0], tol=1e-6):
    """Offset a polyline by a distance.

    Parameters
    ----------
    polyline : list of point
        The XYZ coordinates of the vertices of a polyline.
    distance : float or list of tuples of floats
        The offset distance as float.
        A single value determines a constant offset globally.
        Alternatively, pairs of local offset values per line segment can be used to create variable offsets.
        Distance > 0: offset to the "left", distance < 0: offset to the "right".
    normal : vector
        The normal of the offset plane.

    Returns
    -------
    offset polyline : list of point
        The XYZ coordinates of the resulting polyline.

    """

    distances = match_value_sequence(distance, polyline)
    segments = offset_segments(polyline, distances, normal)

    offset = [segments[0][0]]
    for s1, s2 in pairwise(segments):
        point = intersect(s1, s2, tol)
        offset.append(point)
    offset.append(segments[-1][1])

    return offset


def match_value_sequence(value, sequence):
    """
    """
    p = len(sequence)
    if isinstance(value, (list, tuple)):
        values = value
    else:
        values = [value] * p

    d = len(values)
    if d < p:
        values.extend(values[-1:] * (p - d))

    return values


def intersect_lines(l1, l2, tol):
    """
    """
    x1, x2 = intersection_line_line(l1, l2, tol)
    if x1 and x2:
        return centroid_points([x1, x2])


def intersect_lines_colinear(l1, l2, tol):
    """
    """
    def are_segments_colinear(l1, l2, tol):
        a, b = l1
        d, c = l2
        return is_colinear(a, b, c, tol)

    if are_segments_colinear(l1, l2, tol):
        return centroid_points([l1[1], l2[0]])


def intersect(l1, l2, tol):
    """
    """
    supported_funcs = [intersect_lines, intersect_lines_colinear]

    for func in supported_funcs:
        point = func(l1, l2, tol)
        if point:
            return point

    msg = "Intersection not found for line: {}, and line: {}".format(l1, l2)
    raise ValueError(msg)


def offset_segments(point_list, distances, normal):
    """
    """
    segments = []
    for line, distance in zip(pairwise(point_list), distances):
        segments.append(offset_line(line, distance, normal))
    return segments

# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import compas

    from compas_plotters import MeshPlotter
    from compas.datastructures import Mesh

    mesh = Mesh.from_obj(compas.get('faces.obj'))

    polygons = []
    lines = []
    for fkey in mesh.faces():
        points = mesh.face_coordinates(fkey)
        offset = offset_polyline(points, 0.1)
        polygons.append({
            'points': offset,
            'edgecolor': '#ff0000'
        })
        for a, b in zip(points, offset):
            lines.append({
                'start': a,
                'end': b,
                'color': '#00ff00'
            })

    plotter = MeshPlotter(mesh, figsize=(12, 9))
    plotter.draw_faces()
    plotter.draw_polylines(polygons)
    plotter.draw_lines(lines)
    plotter.show()
