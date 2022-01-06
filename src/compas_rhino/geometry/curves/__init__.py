from .nurbs import RhinoNurbsCurve

from compas.geometry import NurbsCurve
from compas.plugins import plugin


@plugin(category='factories', requires=['Rhino'])
def new_nurbscurve(*args, **kwargs):
    return super(NurbsCurve, RhinoNurbsCurve).__new__(RhinoNurbsCurve)


@plugin(category='factories', requires=['Rhino'])
def new_nurbscurve_from_parameters(*args, **kwargs):
    return RhinoNurbsCurve.from_parameters(*args, **kwargs)


@plugin(category='factories', requires=['Rhino'])
def new_nurbscurve_from_points(*args, **kwargs):
    return RhinoNurbsCurve.from_points(*args, **kwargs)


@plugin(category='factories', requires=['Rhino'])
def new_nurbscurve_from_interpolation(*args, **kwargs):
    return RhinoNurbsCurve.from_interpolation(*args, **kwargs)


@plugin(category='factories', requires=['Rhino'])
def new_nurbscurve_from_step(*args, **kwargs):
    return RhinoNurbsCurve.from_step(*args, **kwargs)
