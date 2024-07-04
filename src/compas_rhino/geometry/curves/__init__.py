from .nurbs import RhinoCurve
from .nurbs import RhinoNurbsCurve

from compas.plugins import plugin


@plugin(category="factories", requires=["Rhino"])
def curve_from_native(cls, *args, **kwargs):
    return RhinoCurve.from_native(*args, **kwargs)


@plugin(category="factories", requires=["Rhino"])
def nurbscurve_from_interpolation(cls, *args, **kwargs):
    return RhinoNurbsCurve.from_interpolation(*args, **kwargs)


@plugin(category="factories", requires=["Rhino"])
def nurbscurve_from_native(cls, *args, **kwargs):
    return RhinoNurbsCurve.from_native(*args, **kwargs)


@plugin(category="factories", requires=["Rhino"])
def nurbscurve_from_parameters(cls, *args, **kwargs):
    return RhinoNurbsCurve.from_parameters(*args, **kwargs)


@plugin(category="factories", requires=["Rhino"])
def nurbscurve_from_points(cls, *args, **kwargs):
    return RhinoNurbsCurve.from_points(*args, **kwargs)


# @plugin(category="factories", requires=["Rhino"])
# def nurbscurve_from_step(cls, *args, **kwargs):
#     return RhinoNurbsCurve.from_step(*args, **kwargs)
