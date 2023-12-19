from .curve import RhinoCurve
from .nurbs import RhinoNurbsCurve

from compas.plugins import plugin


@plugin(category="factories", requires=["Rhino"])
def new_curve(cls, *args, **kwargs):
    curve = object.__new__(RhinoCurve)
    curve.__init__(*args, **kwargs)
    return curve


@plugin(category="factories", requires=["Rhino"])
def new_nurbscurve(cls, *args, **kwargs):
    curve = object.__new__(RhinoNurbsCurve)
    curve.__init__(*args, **kwargs)
    return curve


@plugin(category="factories", requires=["Rhino"])
def new_nurbscurve_from_native(cls, *args, **kwargs):
    return RhinoCurve.from_rhino(*args, **kwargs)


@plugin(category="factories", requires=["Rhino"])
def new_nurbscurve_from_parameters(cls, *args, **kwargs):
    return RhinoNurbsCurve.from_parameters(*args, **kwargs)


@plugin(category="factories", requires=["Rhino"])
def new_nurbscurve_from_points(cls, *args, **kwargs):
    return RhinoNurbsCurve.from_points(*args, **kwargs)


@plugin(category="factories", requires=["Rhino"])
def new_nurbscurve_from_interpolation(cls, *args, **kwargs):
    return RhinoNurbsCurve.from_interpolation(*args, **kwargs)


@plugin(category="factories", requires=["Rhino"])
def new_nurbscurve_from_step(cls, *args, **kwargs):
    return RhinoNurbsCurve.from_step(*args, **kwargs)
