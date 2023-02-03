from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry import Point
from compas.geometry import Vector
from compas.geometry import Line
from compas.geometry import Plane
from compas.geometry import Frame
from compas.geometry import Circle
from compas.geometry import Ellipse
from compas.geometry import Polyline
from compas.geometry import Polygon
from compas.geometry import Arc

from Rhino.Geometry import Point3d
from Rhino.Geometry import Vector3d
from Rhino.Geometry import Interval
from Rhino.Geometry import Line as RhinoLine
from Rhino.Geometry import Plane as RhinoPlane
from Rhino.Geometry import Circle as RhinoCircle
from Rhino.Geometry import Ellipse as RhinoEllipse
from Rhino.Geometry import Polyline as RhinoPolyline
from Rhino.Geometry import Arc as RhinoArc


def point_to_compas(point):
    """Convert a Rhino point to a COMPAS point.

    Parameters
    ----------
    point : :rhino:`Rhino.Geometry.Point3d`

    Returns
    -------
    :class:`~compas.geometry.Point`

    """
    return Point(point.X, point.Y, point.Z)


def point_to_rhino(point):
    """Convert a COMPAS point to a Rhino point.

    Parameters
    ----------
    point : :class:`~compas.geometry.Point`

    Returns
    -------
    :rhino:`Rhino.Geometry.Point3d`

    """
    return Point3d(point[0], point[1], point[2])


def vector_to_compas(vector):
    """Convert a Rhino vector to a COMPAS vector.

    Parameters
    ----------
    vector : :rhino:`Rhino.Geometry.Vector3d`

    Returns
    -------
    :class:`~compas.geometry.Vector`

    """
    return Vector(vector.X, vector.Y, vector.Z)


def vector_to_rhino(vector):
    """Convert a COMPAS vector to a Rhino vector.

    Parameters
    ----------
    vector : :class:`~compas.geometry.Vector`

    Returns
    -------
    :rhino:`Rhino.Geometry.Vector3d`

    """
    return Vector3d(vector[0], vector[1], vector[2])


def line_to_compas(line):
    """Convert a Rhino line to a COMPAS line.

    Parameters
    ----------
    line : :rhino:`Rhino.Geometry.Line`

    Returns
    -------
    :class:`~compas.geometry.Line`

    """
    return Line(point_to_compas(line.From), point_to_compas(line.To))


def line_to_rhino(line):
    """Convert a COMPAS line to a Rhino line.

    Parameters
    ----------
    line : :class:`~compas.geometry.Line`

    Returns
    -------
    :rhino:`Rhino.Geometry.Line`

    """
    return RhinoLine(point_to_rhino(line[0]), point_to_rhino(line[1]))


def plane_to_compas(plane):
    """Convert a Rhino plane to a COMPAS plane.

    Parameters
    ----------
    plane : :rhino:`Rhino.Geometry.Plane`

    Returns
    -------
    :class:`~compas.geometry.Plane`

    """
    return Plane(point_to_compas(plane.Origin), vector_to_compas(plane.Normal))


def plane_to_rhino(plane):
    """Convert a COMPAS plane to a Rhino plane.

    Parameters
    ----------
    plane : :class:`~compas.geometry.Plane`

    Returns
    -------
    :rhino:`Rhino.Geometry.Plane`

    """
    return RhinoPlane(point_to_rhino(plane[0]), vector_to_rhino(plane[1]))


def plane_to_compas_frame(plane):
    """Convert a Rhino plane to a COMPAS frame.

    Parameters
    ----------
    plane : :rhino:`Rhino.Geometry.Plane`

    Returns
    -------
    :class:`~compas.geometry.Frame`

    """
    return Frame(
        point_to_compas(plane.Origin),
        vector_to_compas(plane.XAxis),
        vector_to_compas(plane.YAxis),
    )


def frame_to_rhino_plane(frame):
    """Convert a COMPAS frame to a Rhino plane.

    Parameters
    ----------
    frame : :class:`~compas.geometry.Frame`

    Returns
    -------
    :rhino:`Rhino.Geometry.Plane`

    """
    return RhinoPlane(point_to_rhino(frame.point), vector_to_rhino(frame.xaxis), vector_to_rhino(frame.yaxis))


def frame_to_rhino(frame):
    """Convert a COMPAS frame to a Rhino plane.

    Parameters
    ----------
    frame : :class:`~compas.geometry.Frame`

    Returns
    -------
    :rhino:`Rhino.Geometry.Plane`

    """
    return RhinoPlane(point_to_rhino(frame[0]), vector_to_rhino(frame[1]), vector_to_rhino(frame[2]))


def circle_to_compas(circle):
    """Convert a Rhino circle to a COMPAS circle.

    Parameters
    ----------
    circle : :rhino:`Rhino.Geometry.Circle`

    Returns
    -------
    :class:`~compas.geometry.Circle`

    """
    return Circle(plane_to_compas(circle.Plane), circle.Radius)


def circle_to_rhino(circle):
    """Convert a COMPAS circle to a Rhino circle.

    Parameters
    ----------
    circle : :class:`~compas.geometry.Circle`

    Returns
    -------
    :rhino:`Rhino.Geometry.Circle`

    """
    return RhinoCircle(plane_to_rhino(circle[0]), circle[1])


def ellipse_to_compas(ellipse):
    """Convert a Rhino ellipse to a COMPAS ellipse.

    Parameters
    ----------
    ellipse : :rhino:`Rhino.Geometry.Ellipse`

    Returns
    -------
    :class:`~compas.geometry.Ellipse`

    """
    return Ellipse(plane_to_compas(ellipse.Plane), ellipse.Radius1, ellipse.Radius2)


def ellipse_to_rhino(ellipse):
    """Convert a COMPAS ellipse to a Rhino ellipse.

    Parameters
    ----------
    ellipse : :class:`~compas.geometry.Ellipse`

    Returns
    -------
    :rhino:`Rhino.Geometry.Ellipse`

    """
    return RhinoEllipse(plane_to_rhino(ellipse[0]), ellipse[1], ellipse[2])


def polyline_to_compas(polyline):
    """Convert a Rhino polyline to a COMPAS polyline.

    Parameters
    ----------
    polyline : :rhino:`Rhino.Geometry.Polyline`

    Returns
    -------
    :class:`~compas.geometry.Polyline`

    """
    return Polyline([point_to_compas(point) for point in polyline])


def polyline_to_rhino(polyline):
    """Convert a COMPAS polyline to a Rhino polyline.

    Parameters
    ----------
    polyline : :class:`~compas.geometry.Polyline`

    Returns
    -------
    :rhino:`Rhino.Geometry.Ellipse`

    """
    return RhinoPolyline([point_to_rhino(point) for point in polyline])


def polygon_to_compas(polygon):
    """Convert a Rhino polygon to a COMPAS polygon.

    Parameters
    ----------
    polygon : :rhino:`Rhino.Geometry.Polygon`

    Returns
    -------
    :class:`~compas.geometry.Polygon`

    """
    return Polygon([point_to_compas(point) for point in polygon])


def polygon_to_rhino(polygon):
    """Convert a COMPAS polygon to a Rhino polygon.

    Parameters
    ----------
    polygon : :class:`~compas.geometry.Polygon`

    Returns
    -------
    :rhino:`Rhino.Geometry.Polygon`

    """
    raise NotImplementedError


def arc_to_rhino(arc):
    """Convert a COMPAS Arc to a Rhino one.

    Parameters
    ----------
    arc : :class:`~compas.geometry.Arc`
        The COMPAS Arc to convert.

    Returns
    -------
    :rhino:`Rhino.Geometry.Arc`

    """
    plane = frame_to_rhino_plane(arc.frame)
    circle = RhinoCircle(plane, arc.radius)
    angle_interval = Interval(arc.start_angle, arc.end_angle)
    return RhinoArc(circle, angle_interval)


def arc_to_compas(arc):
    """Convert a Rhino Arc Structure to a COMPAS Arc.

    Parameters
    ----------
    arc : :rhino:`Rhino.Geometry.Arc`
        The Rhino Arc to convert.

    Returns
    -------
    :class:`~compas.geometry.Arc`

    """
    frame = plane_to_compas_frame(arc.Plane)
    # Arc center point can be set independently of its plane's origin
    center = point_to_compas(arc.Center)
    frame.point = center
    return Arc(frame, arc.Radius, start_angle=arc.StartAngle, end_angle=arc.EndAngle)
