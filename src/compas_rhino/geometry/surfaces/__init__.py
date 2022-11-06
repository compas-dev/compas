from .surface import RhinoSurface  # noqa : F401
from .nurbs import RhinoNurbsSurface

from compas.geometry import Surface
from compas.geometry import NurbsSurface
from compas.plugins import plugin


@plugin(category="factories", requires=["Rhino"])
def new_surface(cls, *args, **kwargs):
    return super(Surface, cls).__new__(cls)


@plugin(category="factories", requires=["Rhino"])
def new_surface_from_plane(cls, *args, **kwargs):
    return RhinoSurface.from_plane(*args, **kwargs)


@plugin(category="factories", requires=["Rhino"])
def new_nurbssurface(cls, *args, **kwargs):
    return super(NurbsSurface, cls).__new__(cls)


@plugin(category="factories", requires=["Rhino"])
def new_nurbssurface_from_parameters(cls, *args, **kwargs):
    return RhinoNurbsSurface.from_parameters(*args, **kwargs)


@plugin(category="factories", requires=["Rhino"])
def new_nurbssurface_from_points(cls, *args, **kwargs):
    return RhinoNurbsSurface.from_points(*args, **kwargs)


@plugin(category="factories", requires=["Rhino"])
def new_nurbssurface_from_fill(cls, *args, **kwargs):
    return RhinoNurbsSurface.from_fill(*args, **kwargs)


@plugin(category="factories", requires=["Rhino"])
def new_nurbssurface_from_step(cls, *args, **kwargs):
    return RhinoNurbsSurface.from_step(*args, **kwargs)
