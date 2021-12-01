from .nurbs import RhinoNurbsCurve

from compas.geometry import NurbsCurve
from compas.plugins import plugin


@plugin(category='factories', requires=['Rhino'])
def new_nurbscurve(cls, *args, **kwargs):
    """Create a new empty Nurbs curve."""
    return super(NurbsCurve, RhinoNurbsCurve).__new__(RhinoNurbsCurve)


@plugin(category='factories', requires=['Rhino'])
def new_nurbscurve_from_parameters(*args, **kwargs):
    """Create a new Nurbs curve from explicit curve parameters."""
    return RhinoNurbsCurve.from_parameters(*args, **kwargs)


@plugin(category='factories', requires=['Rhino'])
def new_nurbscurve_from_points(*args, **kwargs):
    """Construct a NURBS curve from control points.

    Parameters
    ----------
    points : list of :class:`compas.geometry.Point`
        The control points.
    degree : int
        The degree of the curve.
    is_periodic : bool, optional
        Flag indicating whether the curve is periodic or not.

    Returns
    -------
    :class:`compas_rhino.geometry.RhinoNurbsCurve`

    """
    return RhinoNurbsCurve.from_points(*args, **kwargs)


@plugin(category='factories', requires=['Rhino'])
def new_nurbscurve_from_interpolation(cls, *args, **kwargs):
    """Construct a NURBS curve by interpolating a set of points.

    Parameters
    ----------
    points : list of :class:`compas.geometry.Point`
        The control points.
    precision : float, optional
        The required precision of the interpolation.
        This parameter is currently not supported.

    Returns
    -------
    :class:`compas_rhino.geometry.RhinoNurbsCurve`

    """
    return RhinoNurbsCurve.from_interpolation(*args, **kwargs)


@plugin(category='factories', requires=['Rhino'])
def new_nurbscurve_from_step(cls, *args, **kwargs):
    """Create a new Nurbs curve from the data contained in a step file."""
    return RhinoNurbsCurve.from_step(*args, **kwargs)
