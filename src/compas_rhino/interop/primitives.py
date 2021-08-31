from compas.geometry import Point
from compas.geometry import Vector
from compas.geometry import Line
from compas.geometry import Plane
from compas.geometry import Frame
from compas.geometry import Circle
from compas.geometry import Ellipse
from compas.geometry import Polyline
from compas.geometry import Polygon

from Rhino.Geometry import Point3d
from Rhino.Geometry import Vector3d
from Rhino.Geometry import Line as RhinoLine
from Rhino.Geometry import Plane as RhinoPlane
from Rhino.Geometry import Circle as RhinoCircle
from Rhino.Geometry import Ellipse as RhinoEllipse
from Rhino.Geometry import Polyline as RhinoPolyline


def rhino_point_to_compas_point(point):
    """Convert a Rhino point to a COMPAS point.

    Parameters
    ----------
    point : :class:`Rhino.Geometry.Point3d`

    Returns
    -------
    :class:`compas.geometry.Point`
    """
    return Point(point.X, point.Y, point.Z)


def compas_point_to_rhino_point(point):
    """Convert a COMPAS point to a Rhino point.

    Parameters
    ----------
    point : :class:`compas.geometry.Point`

    Returns
    -------
    :class:`Rhino.Geometry.Point3d`
    """
    return Point3d(point.x, point.y, point.z)


def rhino_vector_to_compas_vector(vector):
    """Convert a Rhino vector to a COMPAS vector.

    Parameters
    ----------
    vector : :class:`Rhino.Geometry.Vector3d`

    Returns
    -------
    :class:`compas.geometry.Vector`
    """
    return Vector(vector.X, vector.Y, vector.Z)


def compas_vector_to_rhino_vector(vector):
    """Convert a COMPAS vector to a Rhino vector.

    Parameters
    ----------
    vector : :class:`compas.geometry.Vector`

    Returns
    -------
    :class:`Rhino.Geometry.Vector3d`
    """
    return Vector3d(vector.x, vector.y, vector.z)


def rhino_line_to_compas_line(line):
    """Convert a Rhino line to a COMPAS line.

    Parameters
    ----------
    line : :class:`Rhino.Geometry.Line`

    Returns
    -------
    :class:`compas.geometry.Line`
    """
    return Line(rhino_point_to_compas_point(line.From),
                rhino_point_to_compas_point(line.To))


def compas_line_to_rhino_line(line):
    """Convert a COMPAS line to a Rhino line.

    Parameters
    ----------
    line : :class:`compas.geometry.Line`

    Returns
    -------
    :class:`Rhino.Geometry.Line`
    """
    return RhinoLine(compas_point_to_rhino_point(line.start),
                     compas_point_to_rhino_point(line.end))


def rhino_plane_to_compas_plane(plane):
    """Convert a Rhino plane to a COMPAS plane.

    Parameters
    ----------
    plane : :class:`Rhino.Geometry.Plane`

    Returns
    -------
    :class:`compas.geometry.Plane`
    """
    return Plane(rhino_point_to_compas_point(plane.Origin),
                 rhino_vector_to_compas_vector(plane.Normal))


def compas_plane_to_rhino_plane(plane):
    """Convert a COMPAS plane to a Rhino plane.

    Parameters
    ----------
    plane : :class:`compas.geometry.Plane`

    Returns
    -------
    :class:`Rhino.Geometry.Plane`
    """
    return RhinoPlane(compas_point_to_rhino_point(plane.point),
                      compas_vector_to_rhino_vector(plane.normal))


def rhino_plane_to_compas_frame(plane):
    """Convert a Rhino plane to a COMPAS frame.

    Parameters
    ----------
    plane : :class:`Rhino.Geometry.Plane`

    Returns
    -------
    :class:`compas.geometry.Frame`
    """
    return Frame(rhino_point_to_compas_point(plane.Origin),
                 rhino_vector_to_compas_vector(plane.XAxis),
                 rhino_vector_to_compas_vector(plane.YAxis))


def compas_frame_to_rhino_plane(frame):
    """Convert a COMPAS frame to a Rhino plane.

    Parameters
    ----------
    frame : :class:`compas.geometry.Frame`

    Returns
    -------
    :class:`Rhino.Geometry.Plane`
    """
    return RhinoPlane(compas_point_to_rhino_point(frame.point),
                      compas_vector_to_rhino_vector(frame.xaxis),
                      compas_vector_to_rhino_vector(frame.yaxis))


def rhino_circle_to_compas_circle(circle):
    """Convert a Rhino circle to a COMPAS circle.

    Parameters
    ----------
    circle : :class:`Rhino.Geometry.Circle`

    Returns
    -------
    :class:`compas.geometry.Circle`
    """
    return Circle(rhino_plane_to_compas_plane(circle.Plane), circle.Radius)


def compas_circle_to_rhino_circle(circle):
    """Convert a COMPAS circle to a Rhino circle.

    Parameters
    ----------
    circle : :class:`compas.geometry.Circle`

    Returns
    -------
    :class:`Rhino.Geometry.Circle`
    """
    return RhinoCircle(compas_plane_to_rhino_plane(circle.plane), circle.radius)


def rhino_ellipse_to_compas_ellipse(ellipse):
    """Convert a Rhino ellipse to a COMPAS ellipse.

    Parameters
    ----------
    ellipse : :class:`Rhino.Geometry.Ellipse`

    Returns
    -------
    :class:`compas.geometry.Ellipse`
    """
    return Ellipse(rhino_plane_to_compas_plane(ellipse.Plane), ellipse.major, ellipse.minor)


def compas_ellipse_to_rhino_ellipse(ellipse):
    """Convert a COMPAS ellipse to a Rhino ellipse.

    Parameters
    ----------
    ellipse : :class:`compas.geometry.Ellipse`

    Returns
    -------
    :class:`Rhino.Geometry.Ellipse`
    """
    return RhinoEllipse(compas_plane_to_rhino_plane(ellipse.plane), ellipse.major, ellipse.minor)


def rhino_polyline_to_compas_polyline(polyline):
    """Convert a Rhino polyline to a COMPAS polyline.

    Parameters
    ----------
    polyline : :class:`Rhino.Geometry.Polyline`

    Returns
    -------
    :class:`compas.geometry.Polyline`
    """
    return Polyline([rhino_point_to_compas_point(point) for point in polyline])


def compas_polyline_to_rhino_polyline(polyline):
    """Convert a COMPAS polyline to a Rhino polyline.

    Parameters
    ----------
    polyline : :class:`compas.geometry.Ellipse`

    Returns
    -------
    :class:`Rhino.Geometry.Ellipse`
    """
    return RhinoPolyline([compas_point_to_rhino_point(point) for point in polyline])


def rhino_polygon_to_compas_polygon(polygon):
    """Convert a Rhino polygon to a COMPAS polygon.

    Parameters
    ----------
    polygon : :class:`Rhino.Geometry.Polygon`

    Returns
    -------
    :class:`compas.geometry.Ellipse`
    """
    return Polygon([rhino_point_to_compas_point(point) for point in polygon])


def compas_polygon_to_rhino_polygon(polygon):
    """Convert a COMPAS polygon to a Rhino polygon.

    Parameters
    ----------
    polygon : :class:`compas.geometry.Ellipse`

    Returns
    -------
    :class:`Rhino.Geometry.Ellipse`
    """
    raise NotImplementedError
