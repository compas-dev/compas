from .surface import RhinoSurface  # noqa : F401
from .nurbs import RhinoNurbsSurface

from compas.plugins import plugin


@plugin(category="factories", requires=["Rhino"])
def surface_from_native(cls, *args, **kwargs):
    return RhinoSurface.from_native(*args, **kwargs)


@plugin(category="factories", requires=["Rhino"])
def nurbssurface_from_cylinder(cls, *args, **kwargs):
    return RhinoNurbsSurface.from_cylinder(*args, **kwargs)


@plugin(category="factories", requires=["Rhino"])
def nurbssurface_from_fill(cls, *args, **kwargs):
    return RhinoNurbsSurface.from_fill(*args, **kwargs)


@plugin(category="factories", requires=["Rhino"])
def nurbssurface_from_frame(cls, *args, **kwargs):
    return RhinoNurbsSurface.from_frame(*args, **kwargs)


@plugin(category="factories", requires=["Rhino"])
def nurbssurface_from_native(cls, *args, **kwargs):
    return RhinoNurbsSurface.from_native(*args, **kwargs)


@plugin(category="factories", requires=["Rhino"])
def nurbssurface_from_parameters(cls, *args, **kwargs):
    return RhinoNurbsSurface.from_parameters(*args, **kwargs)


@plugin(category="factories", requires=["Rhino"])
def nurbssurface_from_plane(cls, *args, **kwargs):
    return RhinoNurbsSurface.from_plane(*args, **kwargs)


@plugin(category="factories", requires=["Rhino"])
def nurbssurface_from_points(cls, *args, **kwargs):
    return RhinoNurbsSurface.from_points(*args, **kwargs)


@plugin(category="factories", requires=["Rhino"])
def nurbssurface_from_sphere(cls, *args, **kwargs):
    return RhinoNurbsSurface.from_sphere(*args, **kwargs)


@plugin(category="factories", requires=["Rhino"])
def nurbssurface_from_step(cls, *args, **kwargs):
    return RhinoNurbsSurface.from_step(*args, **kwargs)


@plugin(category="factories", requires=["Rhino"])
def nurbssurface_from_torus(cls, *args, **kwargs):
    return RhinoNurbsSurface.from_torus(*args, **kwargs)
