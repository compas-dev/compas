from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry.basic import scale_vector
from compas.geometry.basic import normalize_vector
from compas.geometry.basic import add_vectors
from compas.geometry.basic import subtract_vectors
from compas.geometry.basic import cross_vectors

from compas.geometry.average import centroid_points

from compas.geometry.intersections import intersection_line_line

from compas.geometry.normals import normal_polygon


__all__ = [
    'offset_line',
    'offset_polyline',
    'offset_polygon',
]


def offset_line(line, distance, normal=[0., 0., 1.]):
    """Offset a line by a distance.

    Parameters:
        line (tuple): Two points defining the line.
        distances (float or tuples of floats): The offset distance as float.
            A single value determines a constant offset. Alternatively, two
            offset values for the start and end point of the line can be used to
            a create variable offset.
        normal (tuple): The normal of the offset plane.

    Returns:
        offset line (tuple): Two points defining the offset line.

    Examples:

        .. code-block:: python

            line = [(0.0, 0.0, 0.0), (3.0, 3.0, 0.0)]

            distance = 0.2 # constant offset
            line_offset = offset_line(line, distance)
            print(line_offset)

            distance = [0.2, 0.1] # variable offset
            line_offset = offset_line(line, distance)
            print(line_offset)

    """
    pt1, pt2 = line[0], line[1]
    vec = subtract_vectors(pt1, pt2)
    dir_vec = normalize_vector(cross_vectors(vec, normal))

    if isinstance(distance, list) or isinstance(distance, tuple):
        distances = distance
    else:
        distances = [distance, distance]

    vec_pt1 = scale_vector(dir_vec, distances[0])
    vec_pt2 = scale_vector(dir_vec, distances[1])
    pt1_new = add_vectors(pt1, vec_pt1)
    pt2_new = add_vectors(pt2, vec_pt2)
    return pt1_new, pt2_new


def offset_polygon(polygon, distance):
    """Offset a polygon (closed) by a distance.

    Parameters:
        polygon (sequence of sequence of floats): The XYZ coordinates of the
            corners of the polygon. The first and last coordinates must be identical.
        distance (float or list of tuples of floats): The offset distance as float.
            A single value determines a constant offset globally. Alternatively, pairs of local
            offset values per line segment can be used to create variable offsets.
            Distance > 0: offset to the outside, distance < 0: offset to the inside

    Returns:
        offset polygon (sequence of sequence of floats): The XYZ coordinates of the
            corners of the offset polygon. The first and last coordinates are identical.

    Notes:
        The offset direction is determined by the normal of the polygon. The
        algorithm works also for spatial polygons that do not perfectly fit a plane.

    Examples:

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

    if isinstance(distance, list) or isinstance(distance, tuple):
        distances = distance
        if len(distances) < len(polygon):
            distances = distances + [distances[-1]] * (len(polygon) - len(distances) - 1)
    else:
        distances = [[distance, distance]] * len(polygon)

    lines = [polygon[i:i + 2] for i in range(len(polygon[:-1]))]
    lines_offset = []
    for i, line in enumerate(lines):
        lines_offset.append(offset_line(line, distances[i], normal))

    polygon_offset = []

    for i in range(len(lines_offset)):
        intx_pt1, intx_pt2 = intersection_line_line(lines_offset[i - 1], lines_offset[i])

        if intx_pt1 and intx_pt2:
            polygon_offset.append(centroid_points([intx_pt1, intx_pt2]))
        else:
            polygon_offset.append(lines_offset[i][0])

    polygon_offset.append(polygon_offset[0])
    return polygon_offset


def offset_polyline(polyline, distance, normal=[0., 0., 1.]):
    """Offset a polyline by a distance.

    Parameters:
        polyline (sequence of sequence of floats): The XYZ coordinates of the
            vertices of a polyline.
        distance (float or list of tuples of floats): The offset distance as float.
            A single value determines a constant offset globally. Alternatively, pairs of local
            offset values per line segment can be used to create variable offsets.
            Distance > 0: offset to the "left", distance < 0: offset to the "right"
        normal (tuple): The normal of the offset plane.

    Returns:
        offset polyline (sequence of sequence of floats): The XYZ coordinates of the resulting polyline.

    """

    if isinstance(distance, list) or isinstance(distance, tuple):
        distances = distance
        if len(distances) < len(polyline):
            distances = distances + [distances[-1]] * (len(polyline) - len(distances) - 1)
    else:
        distances = [[distance, distance]] * len(polyline)

    lines = [polyline[i:i + 2] for i in range(len(polyline[:-1]))]
    lines_offset = []
    for i, line in enumerate(lines):
        lines_offset.append(offset_line(line, distances[i], normal))

    polyline_offset = []
    polyline_offset.append(lines_offset[0][0])
    for i in range(len(lines_offset[:-1])):
        intx_pt1, intx_pt2 = intersection_line_line(lines_offset[i], lines_offset[i + 1])

        if intx_pt1 and intx_pt2:
            polyline_offset.append(centroid_points([intx_pt1, intx_pt2]))
        else:
            polyline_offset.append(lines_offset[i][0])
    polyline_offset.append(lines_offset[-1][1])
    return polyline_offset


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
