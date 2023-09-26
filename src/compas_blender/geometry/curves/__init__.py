from .curve import BlenderCurve
from .nurbs import BlenderNurbsCurve

from compas.plugins import plugin


@plugin(category="factories", requires=["bpy"])
def new_curve(cls, *args, **kwargs):
    curve = object.__new__(BlenderCurve)
    curve.__init__(*args, **kwargs)
    return curve


@plugin(category="factories", requires=["bpy"])
def new_nurbscurve(cls, *args, **kwargs):
    curve = object.__new__(BlenderNurbsCurve)
    curve.__init__(*args, **kwargs)
    return curve


@plugin(category="factories", requires=["bpy"])
def new_nurbscurve_from_parameters(cls, *args, **kwargs):
    return BlenderNurbsCurve.from_parameters(*args, **kwargs)


@plugin(category="factories", requires=["bpy"])
def new_nurbscurve_from_points(cls, *args, **kwargs):
    return BlenderNurbsCurve.from_points(*args, **kwargs)


# @plugin(category="factories", requires=["bpy"])
# def new_nurbscurve_from_step(cls, *args, **kwargs):
#     return BlenderNurbsCurve.from_step(*args, **kwargs)
