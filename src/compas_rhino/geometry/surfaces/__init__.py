from .surface import RhinoSurface  # noqa : F401
from .nurbs import RhinoNurbsSurface

from compas.geometry import NurbsSurface
from compas.plugins import plugin


@plugin(category="factories", requires=["Rhino"])
def new_surface(cls, *args, **kwargs):
    return object.__new__(RhinoSurface)


@plugin(category="factories", requires=["Rhino"])
def new_surface_from_plane(cls, *args, **kwargs):
    return RhinoSurface.from_plane(*args, **kwargs)


@plugin(category="factories", requires=["Rhino"])
def new_nurbssurface(cls, *args, **kwargs):
    surface = super(NurbsSurface, cls).__new__(cls)
    surface.__init__(*args, **kwargs)
    return surface


@plugin(category="factories", requires=["Rhino"])
def new_nurbssurface_from_native(cls, *args, **kwargs):
    return RhinoNurbsSurface.from_rhino(*args, **kwargs)


@plugin(category="factories", requires=["Rhino"])
def new_nurbssurface_from_parameters(cls, *args, **kwargs):
    return RhinoNurbsSurface.from_parameters(*args, **kwargs)


@plugin(category="factories", requires=["Rhino"])
def new_nurbssurface_from_plane(cls, *args, **kwargs):
    return RhinoNurbsSurface.from_plane(*args, **kwargs)


@plugin(category="factories", requires=["Rhino"])
def new_nurbssurface_from_points(cls, *args, **kwargs):
    return RhinoNurbsSurface.from_points(*args, **kwargs)


@plugin(category="factories", requires=["Rhino"])
def new_nurbssurface_from_fill(cls, *args, **kwargs):
    return RhinoNurbsSurface.from_fill(*args, **kwargs)


@plugin(category="factories", requires=["Rhino"])
def new_nurbssurface_from_step(cls, *args, **kwargs):
    return RhinoNurbsSurface.from_step(*args, **kwargs)
