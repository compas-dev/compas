from compas.geometry import Point
from compas.geometry import Vector
from compas.geometry import Line
from compas.geometry import Plane
from compas.geometry import Frame
from compas.geometry import Circle
# from compas.geometry import Ellipse
# from compas.geometry import Polyline
# from compas.geometry import Polygon

from Rhino.Geometry import Point3d
from Rhino.Geometry import Vector3d
from Rhino.Geometry import Line as RhinoLine
from Rhino.Geometry import Plane as RhinoPlane
from Rhino.Geometry import Circle as RhinoCircle


def rhino_to_compas_point(point):
    """Convert a Rhino point to a COMPAS point.

    Parameters
    ----------
    point : :class:`Rhino.Geometry.Point3d`

    Returns
    -------
    :class:`compas.geometry.Point`
    """
    return Point(point.X, point.Y, point.Z)


def compas_to_rhino_point(point):
    """Convert a COMPAS point to a Rhino point.

    Parameters
    ----------
    point : :class:`compas.geometry.Point`

    Returns
    -------
    :class:`Rhino.Geometry.Point3d`
    """
    return Point3d(point[0], point[1], point[2])


def rhino_to_compas_vector(vector):
    """Convert a Rhino vector to a COMPAS vector.

    Parameters
    ----------
    vector : :class:`Rhino.Geometry.Vector3d`

    Returns
    -------
    :class:`compas.geometry.Vector`
    """
    return Vector(vector.X, vector.Y, vector.Z)


def compas_to_rhino_vector(vector):
    """Convert a COMPAS vector to a Rhino vector.

    Parameters
    ----------
    vector : :class:`compas.geometry.Vector`

    Returns
    -------
    :class:`Rhino.Geometry.Vector3d`
    """
    return Vector3d(vector[0], vector[1], vector[2])


def rhino_to_compas_line(line):
    """Convert a Rhino line to a COMPAS line.

    Parameters
    ----------
    line : :class:`Rhino.Geometry.Line`

    Returns
    -------
    :class:`compas.geometry.Line`
    """
    return Line(rhino_to_compas_point(line.From), rhino_to_compas_point(line.To))


def compas_to_rhino_line(line):
    """Convert a COMPAS line to a Rhino line.

    Parameters
    ----------
    line : :class:`compas.geometry.Line`

    Returns
    -------
    :class:`Rhino.Geometry.Line`
    """
    return RhinoLine(compas_to_rhino_point(line[0]), compas_to_rhino_point(line[1]))


def rhino_to_compas_plane(plane):
    """Convert a Rhino plane to a COMPAS plane.

    Parameters
    ----------
    plane : :class:`Rhino.Geometry.Plane`

    Returns
    -------
    :class:`compas.geometry.Plane`
    """
    return Plane(rhino_to_compas_point(plane.Origin), rhino_to_compas_vector(plane.Normal))


def compas_to_rhino_plane(plane):
    """Convert a COMPAS plane to a Rhino plane.

    Parameters
    ----------
    plane : :class:`compas.geometry.Plane`

    Returns
    -------
    :class:`Rhino.Geometry.Plane`
    """
    return RhinoPlane(compas_to_rhino_point(plane[0]), compas_to_rhino_vector(plane[1]))


def rhino_plane_to_compas_frame(plane):
    """Convert a Rhino plane to a COMPAS frame.

    Parameters
    ----------
    plane : :class:`Rhino.Geometry.Plane`

    Returns
    -------
    :class:`compas.geometry.Frame`
    """
    return Frame(rhino_to_compas_point(plane.Origin), rhino_to_compas_vector(plane.XAxis), rhino_to_compas_vector(plane.YAxis))


def compas_frame_to_rhino_plane(frame):
    """Convert a COMPAS frame to a Rhino plane.

    Parameters
    ----------
    frame : :class:`compas.geometry.Frame`

    Returns
    -------
    :class:`Rhino.Geometry.Plane`
    """
    return RhinoPlane(compas_to_rhino_point(frame[0]), compas_to_rhino_vector(frame[1]), compas_to_rhino_vector(frame[2]))


def rhino_to_compas_circle(circle):
    """Convert a Rhino circle to a COMPAS circle.

    Parameters
    ----------
    circle : :class:`Rhino.Geometry.Circle`

    Returns
    -------
    :class:`compas.geometry.Circle`
    """
    return Circle(rhino_to_compas_plane(circle.Plane), circle.Radius)


def compas_to_rhino_circle(circle):
    """Convert a COMPAS circle to a Rhino circle.

    Parameters
    ----------
    circle : :class:`compas.geometry.Circle`

    Returns
    -------
    :class:`Rhino.Geometry.Circle`
    """
    return RhinoCircle(compas_to_rhino_plane(circle[0]), circle[1])
