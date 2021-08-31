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


def point_to_compas(point):
    """Convert a Rhino point to a COMPAS point.

    Parameters
    ----------
    point : :class:`Rhino.Geometry.Point3d`

    Returns
    -------
    :class:`compas.geometry.Point`
    """
    return Point(point.X, point.Y, point.Z)


def point_to_rhino(point):
    """Convert a COMPAS point to a Rhino point.

    Parameters
    ----------
    point : :class:`compas.geometry.Point`

    Returns
    -------
    :class:`Rhino.Geometry.Point3d`
    """
    return Point3d(point.x, point.y, point.z)


def vector_to_compas(vector):
    """Convert a Rhino vector to a COMPAS vector.

    Parameters
    ----------
    vector : :class:`Rhino.Geometry.Vector3d`

    Returns
    -------
    :class:`compas.geometry.Vector`
    """
    return Vector(vector.X, vector.Y, vector.Z)


def vector_to_rhino(vector):
    """Convert a COMPAS vector to a Rhino vector.

    Parameters
    ----------
    vector : :class:`compas.geometry.Vector`

    Returns
    -------
    :class:`Rhino.Geometry.Vector3d`
    """
    return Vector3d(vector.x, vector.y, vector.z)


def line_to_compas(line):
    """Convert a Rhino line to a COMPAS line.

    Parameters
    ----------
    line : :class:`Rhino.Geometry.Line`

    Returns
    -------
    :class:`compas.geometry.Line`
    """
    return Line(point_to_compas(line.From),
                point_to_compas(line.To))


def line_to_rhino(line):
    """Convert a COMPAS line to a Rhino line.

    Parameters
    ----------
    line : :class:`compas.geometry.Line`

    Returns
    -------
    :class:`Rhino.Geometry.Line`
    """
    return RhinoLine(point_to_rhino(line.start),
                     point_to_rhino(line.end))


def plane_to_compas(plane):
    """Convert a Rhino plane to a COMPAS plane.

    Parameters
    ----------
    plane : :class:`Rhino.Geometry.Plane`

    Returns
    -------
    :class:`compas.geometry.Plane`
    """
    return Plane(point_to_compas(plane.Origin),
                 vector_to_compas(plane.Normal))


def plane_to_rhino(plane):
    """Convert a COMPAS plane to a Rhino plane.

    Parameters
    ----------
    plane : :class:`compas.geometry.Plane`

    Returns
    -------
    :class:`Rhino.Geometry.Plane`
    """
    return RhinoPlane(point_to_rhino(plane.point),
                      vector_to_rhino(plane.normal))


def plane_to_compas_frame(plane):
    """Convert a Rhino plane to a COMPAS frame.

    Parameters
    ----------
    plane : :class:`Rhino.Geometry.Plane`

    Returns
    -------
    :class:`compas.geometry.Frame`
    """
    return Frame(point_to_compas(plane.Origin),
                 vector_to_compas(plane.XAxis),
                 vector_to_compas(plane.YAxis))


def frame_to_rhino(frame):
    """Convert a COMPAS frame to a Rhino plane.

    Parameters
    ----------
    frame : :class:`compas.geometry.Frame`

    Returns
    -------
    :class:`Rhino.Geometry.Plane`
    """
    return RhinoPlane(point_to_rhino(frame.point),
                      vector_to_rhino(frame.xaxis),
                      vector_to_rhino(frame.yaxis))


def circle_to_compas(circle):
    """Convert a Rhino circle to a COMPAS circle.

    Parameters
    ----------
    circle : :class:`Rhino.Geometry.Circle`

    Returns
    -------
    :class:`compas.geometry.Circle`
    """
    return Circle(plane_to_compas(circle.Plane), circle.Radius)


def circle_to_rhino(circle):
    """Convert a COMPAS circle to a Rhino circle.

    Parameters
    ----------
    circle : :class:`compas.geometry.Circle`

    Returns
    -------
    :class:`Rhino.Geometry.Circle`
    """
    return RhinoCircle(plane_to_rhino(circle.plane), circle.radius)


def ellipse_to_compas(ellipse):
    """Convert a Rhino ellipse to a COMPAS ellipse.

    Parameters
    ----------
    ellipse : :class:`Rhino.Geometry.Ellipse`

    Returns
    -------
    :class:`compas.geometry.Ellipse`
    """
    return Ellipse(plane_to_compas(ellipse.Plane), ellipse.major, ellipse.minor)


def ellipse_to_rhino(ellipse):
    """Convert a COMPAS ellipse to a Rhino ellipse.

    Parameters
    ----------
    ellipse : :class:`compas.geometry.Ellipse`

    Returns
    -------
    :class:`Rhino.Geometry.Ellipse`
    """
    return RhinoEllipse(plane_to_rhino(ellipse.plane), ellipse.major, ellipse.minor)


def polyline_to_compas(polyline):
    """Convert a Rhino polyline to a COMPAS polyline.

    Parameters
    ----------
    polyline : :class:`Rhino.Geometry.Polyline`

    Returns
    -------
    :class:`compas.geometry.Polyline`
    """
    return Polyline([point_to_compas(point) for point in polyline])


def polyline_to_rhino(polyline):
    """Convert a COMPAS polyline to a Rhino polyline.

    Parameters
    ----------
    polyline : :class:`compas.geometry.Polyline`

    Returns
    -------
    :class:`Rhino.Geometry.Ellipse`
    """
    return RhinoPolyline([point_to_rhino(point) for point in polyline])


def polygon_to_compas(polygon):
    """Convert a Rhino polygon to a COMPAS polygon.

    Parameters
    ----------
    polygon : :class:`Rhino.Geometry.Polygon`

    Returns
    -------
    :class:`compas.geometry.Polygon`
    """
    return Polygon([point_to_compas(point) for point in polygon])


def polygon_to_rhino(polygon):
    """Convert a COMPAS polygon to a Rhino polygon.

    Parameters
    ----------
    polygon : :class:`compas.geometry.Polygon`

    Returns
    -------
    :class:`Rhino.Geometry.Polygon`
    """
    raise NotImplementedError
