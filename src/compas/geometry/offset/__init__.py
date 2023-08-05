from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.plugins import pluggable


@pluggable(category="offset")
def offset_line(line, distance, **kwargs):
    """Offset a line by a distance.

    Parameters
    ----------
    line : :class:`~compas.geometry.Line`
        A line defined by two points.
    distance : float
        The offset distance as float.

    Returns
    -------
    list[point]
        The two points of the offseted line.

    Notes
    -----
    The offset direction is chosen such that if the line were along the positve
    X axis and the normal of the offset plane is along the positive Z axis, the
    offset line is in the direction of the postive Y axis.

    Depending of the backend used, additional parameters can be added as keyword arguments. (point somewhere in api, or list
    accepted arguments)

    """
    raise NotImplementedError


@pluggable(category="offset")
def offset_polyline(polyline, distance, **kwargs):
    """Offset a polyline by a distance.

    Parameters
    ----------
    polyline : :class:`~compas.geometry.Polyline`
        A polyline defined by a sequence of points.
    distance : float
        The offset distance as float.

    Returns
    -------
    list[point]
        The points of the offseted polyline.

    Notes
    -----
    The offset direction is chosen such that if the polyline were along the positve
    X axis and the normal of the offset plane is along the positive Z axis, the
    offset polyline is in the direction of the postive Y axis.

    Depending of the backend used, additional parameters can be added as keyword arguments. (point somewhere in api, or list
    accepted arguments)

    """
    raise NotImplementedError


@pluggable(category="offset")
def offset_polygon(polygon, distance, **kwargs):
    """Offset a polygon by a distance.

    Parameters
    ----------
    polygon : :class:`~compas.geometry.Polygon`
        A polygon defined by a sequence of vertices.
    distance : float
        The offset distance as float.

    Returns
    -------
    list[point]
        The vertices of the offseted polygon.

    Notes
    -----
    The offset direction is determined by the provided normal vector.
    If the polyline is in the XY plane and the normal is along the positive Z axis,
    positive offset distances will result in counterclockwise offsets,
    and negative values in clockwise direction.
    Depending of the backend used, additional parameters can be added as keyword arguments. (point somewhere in api, or list
    accepted arguments)

    """
    raise NotImplementedError
