from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry import Translation
from compas.geometry import Line
from compas.geometry import Polyline
from compas.geometry import Vector
from compas.geometry import Point

__all__ = [
    'extend_line',
    'extend_polyline',
]


def extend_line(line, start_extension=0, end_extension=0):
    """Extend the given line from one end or the other, or both, depending on the given values

    Parameters
    ----------
    line : tuple
        Two points defining the line.
    start_extension : float
        The extension distance at the start of the line as float.
    end_extension : float
        The extension distance at the end of the line as float.

    Returns
    -------
    extended line : tuple
        Two points defining the offset line.

    Examples
    --------
    >>> line = Line([0.0,0.0,0.0],[1.0,0.0,0.0])
    >>> extended_line = extend_line(line, 1, 1)
    Line([-1.0, 0.0, 0.0], [2.0, 0.0, 0.0])
    """
    def calculate_translation(line, distance):
        vector = line.direction.copy()
        vector.scale(distance)
        return Translation(vector)

    if start_extension != 0:
        translation = calculate_translation(line, -start_extension)
        line.start.transform(translation)
    if end_extension != 0:
        translation = calculate_translation(line, end_extension)
        line.end.transform(translation)

    return line


def extend_polyline(polyline, start_extension=0, end_extension=0):
    """Extend a polyline by line from the vectors on segments at extreme sides

    Parameters
    ----------
    polyline : list
        list of points defining the polyline.
    start_extension : float
        The extension distance at the start of the polyline as float.
    end_extension : float
        The extension distance at the end of the polyline as float.

    Returns
    -------
    extended polyline : compas.geometry.Polyline(points)

    Examples
    --------
    >>> polyline = Polyline([0.0,0.0,0.0],[1.0,0.0,0.0],[2.0,1.0,0.0],[3.0,1.0,0.0],[4.0,0.0,0.0],[5.0,0.0,0.0])
    >>> extended_polyline = extend_polyline(polyline, 1, 1)
    Polyline([-1.0,0.0,0.0],[0.0,0.0,0.0],[1.0,0.0,0.0],[2.0,1.0,0.0],[3.0,1.0,0.0],[4.0,0.0,0.0],[5.0,0.0,0.0],[6.0,0.0,0.0])
    """
    def calculate_translation_vector(vector, distance):
        vector.unitize()
        vector.scale(distance)
        return Translation(vector)

    points = polyline.points
    if start_extension != 0:
        point_start = polyline.points[0]
        vec = Vector.from_start_end(polyline.points[1], point_start)
        translation = calculate_translation_vector(vec, start_extension)
        new_point_start = point_start.transformed(translation)
        points.insert(0, new_point_start)

    if end_extension != 0:
        point_end = polyline.points[-1]
        vec_end = Vector.from_start_end(polyline.points[-2], point_end)
        translation = calculate_translation_vector(vec_end, end_extension)
        new_point_end = point_end.transformed(translation)
        points.append(new_point_end)

    return Polyline(points)
