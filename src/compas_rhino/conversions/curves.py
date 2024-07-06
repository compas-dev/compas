from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import Rhino  # type: ignore
import scriptcontext as sc  # type: ignore

from compas.geometry import Arc
from compas.geometry import Circle
from compas.geometry import Curve
from compas.geometry import Ellipse
from compas.geometry import Line
from compas.geometry import NurbsCurve
from compas.geometry import Polyline

from .exceptions import ConversionError
from .geometry import frame_to_rhino_plane
from .geometry import plane_to_compas
from .geometry import plane_to_compas_frame
from .geometry import plane_to_rhino
from .geometry import point_to_compas
from .geometry import point_to_rhino

# =============================================================================
# To Rhino
# =============================================================================


def line_to_rhino(line):
    """Convert a COMPAS line to a Rhino line.

    Parameters
    ----------
    line : :class:`compas.geometry.Line`

    Returns
    -------
    :rhino:`Rhino.Geometry.Line`

    """
    return Rhino.Geometry.Line(point_to_rhino(line[0]), point_to_rhino(line[1]))


def line_to_rhino_curve(line):
    """Convert a COMPAS line to a Rhino curve.

    Parameters
    ----------
    line : :class:`compas.geometry.Line`

    Returns
    -------
    :rhino:`Rhino.Geometry.Curve`

    """
    return Rhino.Geometry.NurbsCurve.CreateFromLine(line_to_rhino(line))


def polyline_to_rhino(polyline, tol=None):
    """Convert a COMPAS polyline to a Rhino polyline.

    Parameters
    ----------
    polyline : :class:`compas.geometry.Polyline`

    Returns
    -------
    :rhino:`Rhino.Geometry.Ellipse`

    """
    tol = tol or sc.doc.ModelAbsoluteTolerance
    polyline = Rhino.Geometry.Polyline([point_to_rhino(point) for point in polyline])
    polyline.DeleteShortSegments(tol)
    return polyline


def polyline_to_rhino_curve(polyline):
    """Convert a COMPAS polyline to a Rhino curve.

    Parameters
    ----------
    polyline : :class:`compas.geometry.Polyline`

    Returns
    -------
    :rhino:`Rhino.Geometry.PolylineCurve`

    """
    return Rhino.Geometry.PolylineCurve([point_to_rhino(point) for point in polyline])


def circle_to_rhino(circle):
    """Convert a COMPAS circle to a Rhino circle.

    Parameters
    ----------
    circle : :class:`compas.geometry.Circle`

    Returns
    -------
    :rhino:`Rhino.Geometry.Circle`

    """
    return Rhino.Geometry.Circle(plane_to_rhino(circle.plane), circle.radius)


def circle_to_rhino_curve(circle):
    """Convert a COMPAS circle to a Rhino curve.

    Parameters
    ----------
    circle : :class:`compas.geometry.Circle`

    Returns
    -------
    :rhino:`Rhino.Geometry.Curve`

    """
    return Rhino.Geometry.NurbsCurve.CreateFromCircle(circle_to_rhino(circle))


def ellipse_to_rhino(ellipse):
    """Convert a COMPAS ellipse to a Rhino ellipse.

    Parameters
    ----------
    ellipse : :class:`compas.geometry.Ellipse`

    Returns
    -------
    :rhino:`Rhino.Geometry.Ellipse`

    """
    return Rhino.Geometry.Ellipse(plane_to_rhino(ellipse.plane), ellipse.major, ellipse.minor)


def ellipse_to_rhino_curve(ellipse):
    """Convert a COMPAS ellipse to a Rhino curve.

    Parameters
    ----------
    ellipse : :class:`compas.geometry.Ellipse`

    Returns
    -------
    :rhino:`Rhino.Geometry.Curve`

    """
    return Rhino.Geometry.NurbsCurve.CreateFromEllipse(ellipse_to_rhino(ellipse))


def arc_to_rhino(arc):
    """Convert a COMPAS Arc to a Rhino one.

    Parameters
    ----------
    arc : :class:`compas.geometry.Arc`
        The COMPAS Arc to convert.

    Returns
    -------
    :rhino:`Rhino.Geometry.Arc`

    """
    plane = frame_to_rhino_plane(arc.frame)
    circle = Rhino.Geometry.Circle(plane, arc.radius)
    angle_interval = Rhino.Geometry.Interval(arc.start_angle, arc.end_angle)
    return Rhino.Geometry.Arc(circle, angle_interval)


def curve_to_rhino(curve):
    """Convert a COMPAS curve to a Rhino curve.

    Parameters
    ----------
    curve : :class:`compas.geometry.Curve`

    Returns
    -------
    :rhino:`Rhino.Geometry.Curve`

    """
    return curve.rhino_curve


# =============================================================================
# To COMPAS
# =============================================================================


def line_to_compas(line):
    """Convert a Rhino line to a COMPAS line.

    Parameters
    ----------
    line : :rhino:`Rhino.Geometry.Line`

    Returns
    -------
    :class:`compas.geometry.Line`

    """
    return Line(point_to_compas(line.From), point_to_compas(line.To))


def circle_to_compas(circle):
    """Convert a Rhino circle to a COMPAS circle.

    Parameters
    ----------
    circle : :rhino:`Rhino.Geometry.Circle`

    Returns
    -------
    :class:`compas.geometry.Circle`

    """
    frame = plane_to_compas(circle.Plane)
    return Circle(circle.Radius, frame=frame)


def ellipse_to_compas(ellipse):
    """Convert a Rhino ellipse to a COMPAS ellipse.

    Parameters
    ----------
    ellipse : :rhino:`Rhino.Geometry.Ellipse`

    Returns
    -------
    :class:`compas.geometry.Ellipse`

    """
    frame = plane_to_compas(ellipse.Plane)
    return Ellipse(ellipse.Radius1, ellipse.Radius2, frame=frame)


def polyline_to_compas(polyline):
    """Convert a Rhino polyline to a COMPAS polyline.

    Parameters
    ----------
    polyline : :rhino:`Rhino.Geometry.Polyline`

    Returns
    -------
    :class:`compas.geometry.Polyline`

    """
    return Polyline([point_to_compas(point) for point in polyline])


def arc_to_compas(arc):
    """Convert a Rhino Arc Structure to a COMPAS Arc.

    Parameters
    ----------
    arc : :rhino:`Rhino.Geometry.Arc`
        The Rhino Arc to convert.

    Returns
    -------
    :class:`compas.geometry.Arc`

    """
    frame = plane_to_compas_frame(arc.Plane)
    # Arc center point can be set independently of its plane's origin
    center = point_to_compas(arc.Center)
    frame.point = center
    return Arc(radius=arc.Radius, start_angle=arc.StartAngle, end_angle=arc.EndAngle, frame=frame)


def curve_to_compas_line(curve):
    """Convert a Rhino curve to a COMPAS line.

    Parameters
    ----------
    curve : :rhino:`Rhino.Geometry.Curve`

    Returns
    -------
    :class:`compas.geometry.Line`

    """
    return Line(point_to_compas(curve.PointAtStart), point_to_compas(curve.PointAtEnd))


def curve_to_compas_circle(curve):
    """Convert a Rhino curve to a COMPAS circle.

    Parameters
    ----------
    curve : :rhino:`Rhino.Geometry.Curve`

    Returns
    -------
    :class:`compas.geometry.Circle`

    Raises
    ------
    ConversionError
        If the curve cannot be converted to a circle.

    """
    result, circle = curve.TryGetCircle()
    if not result:
        raise ConversionError("The curve cannot be converted to a circle.")
    return circle_to_compas(circle)


def curve_to_compas_ellipse(curve):
    """Convert a Rhino curve to a COMPAS ellipse.

    Parameters
    ----------
    curve : :rhino:`Rhino.Geometry.Curve`

    Returns
    -------
    :class:`compas.geometry.Ellipse`

    Raises
    ------
    ConversionError
        If the curve cannot be converted to an ellipse.

    """
    result, ellipse = curve.TryGetEllipse()
    if not result:
        raise ConversionError("The curve cannot be converted to an ellipse.")
    return ellipse_to_compas(ellipse)


def curve_to_compas_polyline(curve):
    """Convert a Rhino curve to a COMPAS polyline.

    Parameters
    ----------
    curve : :rhino:`Rhino.Geometry.Curve`

    Returns
    -------
    :class:`compas.geometry.Polyline`

    Raises
    ------
    ConversionError
        If the curve cannot be converted to a polyline.

    """
    result, polyline = curve.TryGetPolyline()
    if not result:
        raise ConversionError("The curve cannot be converted to a polyline.")
    return polyline_to_compas(polyline)


def curve_to_compas(curve, try_nurbs=True):
    """Convert a Rhino curve to a COMPAS curve.

    Parameters
    ----------
    curve : :rhino:`Rhino.Geometry.Curve`
        A Rhino curve.
    try_nurbs : bool, optional
        Try to convert the curve to a NURBS curve.

    Returns
    -------
    :class:`compas.geometry.Curve` | :class:`compas.geometry.NurbsCurve`
        If `try_nurbs` is `True`, and the geometry has a NURBS representation, return a NURBS curve.
        Otherwise return a general curve.

    """
    if try_nurbs and curve.HasNurbsForm():
        return NurbsCurve.from_native(curve.ToNurbsCurve())
    return Curve.from_native(curve)
