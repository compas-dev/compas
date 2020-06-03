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
    """ Extends the given line from one end or the other, or both, depending on the given values

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
    .. code-block:: python

        extended_line = extend_line(line, 10, 10)

    """
    def calculate_translation(line, distance):
        vector = line.direction.copy()
        vector.scale(distance)
        return Translation(vector)

    if start_extension !=0:
        translation = calculate_translation(line, -start_extension)
        line.start.transform(translation)
    if end_extension !=0:
        translation = calculate_translation(line, end_extension)
        line.end.transform(translation)

    return line

def extend_polyline(polyline, start_extension= 0, end_extension= 0):
    """ Extends a polyline by line from the vectors on segments at extremes

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
    .. code-block:: python

        extended_polyline = extend_polyline(polyline, 10, 10)
    """
    def calculate_translation_vector(vector, distance):
        vector.unitize()
        vector.scale(distance)
        return Translation(vector)

    new_pts = polyline.points
    if start_extension != 0:
        init_pt = polyline.points[0]
        vec = Vector.from_start_end(polyline.points[1], init_pt)
        translation = calculate_translation_vector(vec, start_extension)
        new_pt_start = init_pt.transformed(translation)
        new_pts.insert(0, new_pt_start)
        
    if end_extension != 0:
        end_pt = polyline.points[-1] 
        vec_end = Vector.from_start_end(polyline.points[-2], end_pt)
        translation = calculate_translation_vector(vec_end, end_extension)
        new_pt_end = end_pt.transformed(translation)
        new_pts.append(new_pt_end)

    return Polyline(new_pts)