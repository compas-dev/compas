from .nurbs import RhinoNurbsSurface

from compas.geometry import NurbsSurface
from compas.plugins import plugin


@plugin(category='factories', requires=['Rhino'])
def new_nurbssurface(*args, **kwargs):
    return super(NurbsSurface, RhinoNurbsSurface).__new__(RhinoNurbsSurface)


@plugin(category='factories', requires=['Rhino'])
def new_nurbssurface_from_parameters(*args, **kwargs):
    return RhinoNurbsSurface.from_parameters(*args, **kwargs)


@plugin(category='factories', requires=['Rhino'])
def new_nurbssurface_from_points(*args, **kwargs):
    return RhinoNurbsSurface.from_points(*args, **kwargs)


@plugin(category='factories', requires=['Rhino'])
def new_nurbssurface_from_fill(*args, **kwargs):
    return RhinoNurbsSurface.from_fill(*args, **kwargs)


@plugin(category='factories', requires=['Rhino'])
def new_nurbssurface_from_step(*args, **kwargs):
    return RhinoNurbsSurface.from_step(*args, **kwargs)
