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

from compas.utilities import pairwise


__all__ = [
    'offset_line',
    'offset_polyline',
    'offset_polygon',
]


def offset_line(line, distance, normal=[0., 0., 1.]):
    """Offset a line by a distance.

    Parameters
    ----------
    line : tuple
        Two points defining the line.
    distances : float or tuples of floats
        The offset distance as float.
        A single value determines a constant offset. Alternatively, two
        offset values for the start and end point of the line can be used to
        a create variable offset.
    normal : tuple
        The normal of the offset plane.

    Returns
    -------
    offset line (tuple)
        Two points defining the offset line.

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

    Parameters
    ----------
    polygon : list of point
        The XYZ coordinates of the corners of the polygon.
        The first and last coordinates must not be identical.
    distance : float or list of tuples of floats
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
    p = len(polygon)

    if isinstance(distance, (list, tuple)):
        distances = distance
    else:
        distances = [distance] * p

    d = len(distances)

    if d < p:
        distances.extend(distances[-1:] * (p - d))

    normal = normal_polygon(polygon)

    offset = []
    for line, distance in zip(pairwise(polygon + polygon[:1]), distances):
        offset.append(offset_line(line, distance, normal))

    points = []
    for l1, l2 in pairwise(offset[-1:] + offset):
        x1, x2 = intersection_line_line(l1, l2)
        if x1 and x2:
            points.append(centroid_points([x1, x2]))
        else:
            points.append(x1)

    return points


def offset_polyline(polyline, distance, normal=[0., 0., 1.]):
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
    normal : tuple
        The normal of the offset plane.

    Returns
    -------
    offset polyline : list of point
        The XYZ coordinates of the resulting polyline.

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

    import compas

    from compas.plotters import MeshPlotter
    from compas.datastructures import Mesh

    mesh = Mesh.from_obj(compas.get('faces.obj'))

    polygons = []
    lines = []
    for fkey in mesh.faces():
        points = mesh.face_coordinates(fkey)
        offset = offset_polygon(points, 0.1)
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

    plotter = MeshPlotter(mesh)
    plotter.draw_faces()
    plotter.draw_polygons(polygons)
    plotter.draw_lines(lines)
    plotter.show()
