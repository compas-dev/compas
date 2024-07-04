from __future__ import absolute_import  # noqa: I001
from __future__ import division
from __future__ import print_function

import Rhino.Geometry  # type: ignore  # noqa: F401

from .exceptions import ConversionError

from .breps import brep_to_compas
from .curves import curve_to_compas
from .geometry import point_to_compas
from .meshes import mesh_to_compas
from .surfaces import surface_to_compas


def brepobject_to_compas(obj):
    """Convert a Rhino BrepObject to a COMPAS Brep.

    Parameters
    ----------
    obj : Rhino.DocObjects.BrepObject

    Returns
    -------
    :class:`compas.geometry.Brep`

    Raises
    ------
    ConversionError

    """
    try:
        geometry = obj.BrepGeometry
        brep = brep_to_compas(geometry)
    except Exception:
        raise ConversionError("Rhino Object of type {} cannot be converted to a COMPAS Brep.".format(type(obj)))

    return brep


def curveobject_to_compas(obj, try_nurbs=True):
    """Convert a Rhino CurveObject to a COMPAS Curve.

    Parameters
    ----------
    obj : Rhino.DocObjects.CurveObject
        The Rhino Object.
    try_nurbs : bool, optional
        Try to convert the curve to a NURBS curve.

    Returns
    -------
    :class:`compas.geometry.Curve` | :class:`compas.geometry.NurbsCurve`
        If `try_nurbs` is `True`, and the geometry of the object has a NURBS representation, return a NURBS curve.
        Otherwise return a general curve.

    Raises
    ------
    ConversionError

    """
    try:
        geometry = obj.CurveGeometry
        curve = curve_to_compas(geometry, try_nurbs=try_nurbs)
    except Exception:
        raise ConversionError("Rhino Object of type {} cannot be converted to a COMPAS Curve.".format(type(obj)))

    return curve


def meshobject_to_compas(obj):
    """Convert a Rhino MeshObject to a COMPAS Mesh.

    Parameters
    ----------
    obj : Rhino.DocObjects.MeshObject

    Returns
    -------
    :class:`compas.datastructures.Mesh`

    Raises
    ------
    ConversionError

    """
    try:
        geometry = obj.MeshGeometry
        mesh = mesh_to_compas(geometry)
    except Exception:
        raise ConversionError("Rhino Object of type {} cannot be converted to a COMPAS Mesh.".format(type(obj)))

    return mesh


def pointobject_to_compas(obj):
    """Convert a Rhino PointObject to a COMPAS Point.

    Parameters
    ----------
    obj : Rhino.DocObjects.PointObject

    Returns
    -------
    :class:`compas.geometry.Point`

    Raises
    ------
    ConversionError

    """
    try:
        geometry = obj.PointGeometry
        point = point_to_compas(geometry)
    except Exception:
        raise ConversionError("Rhino Object of type {} cannot be converted to a COMPAS Point.".format(type(obj)))

    return point


def surfaceobject_to_compas(obj, try_nurbs=True):
    """Convert a Rhino SurfaceObject to a COMPAS Surface.

    Parameters
    ----------
    obj : Rhino.DocObjects.SurfaceObject
        The surface object.
    try_nurbs : bool, optional
        Try to convert the surface to a NURBS surface.

    Returns
    -------
    :class:`compas.geometry.Surface` | :class:`compas.geometry.NurbsSurface`
        If `try_nurbs` is `True`, and the geometry of the object has a NURBS representation, return a NURBS surface.
        Otherwise return a general surface.

    Raises
    ------
    ConversionError

    """
    try:
        geometry = obj.SurfaceGeometry
        surface = surface_to_compas(geometry, try_nurbs=try_nurbs)
    except Exception:
        raise ConversionError("Rhino Object of type {} cannot be converted to a COMPAS Surface.".format(type(obj)))

    return surface
