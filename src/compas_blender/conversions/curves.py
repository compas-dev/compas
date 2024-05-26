from typing import Optional

import bpy  # type: ignore

from compas.geometry import Circle
from compas.geometry import Line
from compas.geometry import NurbsCurve
from compas.geometry import Polyline

# =============================================================================
# To Blender
# =============================================================================


def line_to_blender_curve(line: Line) -> bpy.types.Curve:
    """Convert a COMPAS line to a Blender curve.

    Parameters
    ----------
    line : :class:`compas.geometry.Line`
        A COMPAS line.

    Returns
    -------
    :class:`bpy.types.Curve`
        A Blender curve.

    """
    curve = bpy.data.curves.new(name=line.name, type="CURVE")
    curve.dimensions = "3D"

    spline = curve.splines.new("POLY")
    spline.points.add(1)

    start = line.start
    end = line.end

    spline.points[0].co = [*start, 1.0]
    spline.points[1].co = [*end, 1.0]

    spline.order_u = 1

    return curve


def polyline_to_blender_curve(polyline: Polyline, name: Optional[str] = None) -> bpy.types.Curve:
    """Convert a COMPAS polyline to a Blender curve.

    Parameters
    ----------
    polyline : :class:`compas.geometry.Polyline`
        A COMPAS polyline.

    Returns
    -------
    :class:`bpy.types.Curve`
        A Blender curve.

    """
    curve = bpy.data.curves.new(name=name or polyline.name, type="CURVE")
    curve.dimensions = "3D"

    spline = curve.splines.new("POLY")
    spline.points.add(len(polyline.points) - 1)

    for i, (point) in enumerate(polyline.points):
        spline.points[i].co = [point[0], point[1], point[2], 1.0]

    spline.order_u = 1

    return curve


def circle_to_blender_curve(circle: Circle) -> bpy.types.Curve:
    """Convert a COMPAS circle to a Blender circle.

    Parameters
    ----------
    circle : :class:`compas.geometry.Circle`
        A COMPAS circle.

    Returns
    -------
    :class:`bpy.types.Curve`
        A Blender curve.

    """
    raise NotImplementedError


def nurbscurve_to_blender_curve(nurbscurve: NurbsCurve) -> bpy.types.Curve:
    """Convert a COMPAS NURBS curve to a Blender curve.

    Parameters
    ----------
    nurbscurve : :class:`compas.geometry.NurbsCurve`
        A COMPAS NURBS curve.

    Returns
    -------
    :class:`bpy.types.Curve`
        A Blender curve.

    """
    curve = bpy.data.curves.new(name=nurbscurve.name, type="CURVE")
    curve.dimensions = "3D"

    spline = curve.splines.new("NURBS")
    spline.points.add(len(nurbscurve.points) - 1)

    for i, (point, weight) in enumerate(zip(nurbscurve.points, nurbscurve.weights)):
        spline.points[i].co = [point[0], point[1], point[2], weight]
        spline.points[i].weight = weight

    spline.order_u = nurbscurve.order
    spline.use_cyclic_u = nurbscurve.is_periodic
    spline.use_endpoint_u = True
    spline.use_bezier_u = False

    return curve


# =============================================================================
# To COMPAS
# =============================================================================
