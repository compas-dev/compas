from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry import Line

from ._exceptions import ConversionError

from ._primitives import line_to_rhino
from ._primitives import circle_to_rhino
from ._primitives import ellipse_to_rhino
from ._primitives import point_to_compas
from ._primitives import circle_to_compas
from ._primitives import ellipse_to_compas
from ._primitives import polyline_to_compas

from Rhino.Geometry import NurbsCurve as RhinoNurbsCurve


def curve_to_compas_line(curve):
    """Convert a Rhino curve to a COMPAS line.

    Parameters
    ----------
    curve: :rhino:`Rhino.Geometry.Curve`

    Returns
    -------
    :class:`~compas.geometry.Line`

    """
    return Line(point_to_compas(curve.PointAtStart), point_to_compas(curve.PointAtEnd))


def line_to_rhino_curve(line):
    """Convert a COMPAS line to a Rhino curve.

    Parameters
    ----------
    line: :class:`~compas.geometry.Line`

    Returns
    -------
    :rhino:`Rhino.Geometry.Curve`

    """
    return RhinoNurbsCurve.CreateFromLine(line_to_rhino(line))


def curve_to_compas_circle(curve):
    """Convert a Rhino curve to a COMPAS circle.

    Parameters
    ----------
    curve: :rhino:`Rhino.Geometry.Curve`

    Returns
    -------
    :class:`~compas.geometry.Circle`

    Raises
    ------
    ConversionError
        If the curve cannot be converted to a circle.

    """
    result, circle = curve.TryGetCircle()
    if not result:
        raise ConversionError("The curve cannot be converted to a circle.")
    return circle_to_compas(circle)


def circle_to_rhino_curve(circle):
    """Convert a COMPAS circle to a Rhino curve.

    Parameters
    ----------
    circle: :class:`~compas.geometry.Circle`

    Returns
    -------
    :rhino:`Rhino.Geometry.Curve`

    """
    return RhinoNurbsCurve.CreateFromCircle(circle_to_rhino(circle))


def curve_to_compas_ellipse(curve):
    """Convert a Rhino curve to a COMPAS ellipse.

    Parameters
    ----------
    curve: :rhino:`Rhino.Geometry.Curve`

    Returns
    -------
    :class:`~compas.geometry.Ellipse`

    Raises
    ------
    ConversionError
        If the curve cannot be converted to an ellipse.

    """
    result, ellipse = curve.TryGetEllipse()
    if not result:
        raise ConversionError("The curve cannot be converted to an ellipse.")
    return ellipse_to_compas(ellipse)


def ellipse_to_rhino_curve(ellipse):
    """Convert a COMPAS ellipse to a Rhino curve.

    Parameters
    ----------
    ellipse: :class:`~compas.geometry.Ellipse`

    Returns
    -------
    :rhino:`Rhino.Geometry.Curve`

    """
    return RhinoNurbsCurve.CreateFromEllipse(ellipse_to_rhino(ellipse))


def curve_to_compas_polyline(curve):
    """Convert a Rhino curve to a COMPAS polyline.

    Parameters
    ----------
    curve: :rhino:`Rhino.Geometry.Curve`

    Returns
    -------
    :class:`~compas.geometry.Polyline`

    Raises
    ------
    ConversionError
        If the curve cannot be converted to a polyline.

    """
    result, polyline = curve.TryGetPolyline()
    if not result:
        raise ConversionError("The curve cannot be converted to a polyline.")
    return polyline_to_compas(polyline)


def curve_to_compas_data(curve):
    """Convert a Rhino curve to a COMPAS data dict.

    Parameters
    ----------
    curve: :rhino:`Rhino.Geometry.Curve`

    Returns
    -------
    dict

    """
    nurbs = curve.ToNurbsCurve()
    points = []
    weights = []
    knots = []
    multiplicities = []
    degree = nurbs.Degree
    is_periodic = nurbs.IsPeriodic

    for index in range(nurbs.Points.Count):
        point = nurbs.Points.Item[index]
        points.append(point_to_compas(point.Location))
        weights.append(point.Weight)

    for index in range(nurbs.Knots.Count):
        knots.append(nurbs.Knots.Item[index])
        multiplicities.append(nurbs.Knots.KnotMultiplicity(index))

    return {
        "points": [point.data for point in points],
        "weights": weights,
        "knots": knots,
        "multiplicities": multiplicities,
        "degree": degree,
        "is_periodic": is_periodic,
    }


def data_to_rhino_curve(data):
    """Convert a COMPAS curve to a Rhino curve.

    Parameters
    ----------
    data: dict

    Returns
    -------
    :rhino:`Rhino.Geometry.NurbsCurve`

    """
    nurbs = RhinoNurbsCurve(data["degree"], len(data["points"]))

    for index, xyz in enumerate(data["points"]):
        nurbs.Points.SetPoint(index, *xyz)

    knotvector = []
    for knot, mult in zip(data["knots"], data["multiplicities"]):
        for i in range(mult):
            knotvector.append(knot)

    for index, knot in enumerate(knotvector):
        nurbs.Knots.Item[index] = knot
    return nurbs
