import Rhino

from compas.plugins import plugin
from compas.geometry import Brep

from .brep import RhinoBrep


@plugin(category="factories", requires=["Rhino"])
def new_brep(cls, *args, **kwargs):
    return super(Brep, cls).__new__(cls)


@plugin(category="factories", requires=["Rhino"])
def from_native(*args, **kwargs):
    return RhinoBrep.from_native(*args, **kwargs)


@plugin(category="factories", requires=["Rhino"])
def from_box(*args, **kwargs):
    return RhinoBrep.from_box(*args, **kwargs)


@plugin(category="factories", requires=["Rhino"])
def from_cylinder(*args, **kwargs):
    return RhinoBrep.from_cylinder(*args, **kwargs)


@plugin(category="factories", requires=["Rhino"])
def from_sphere(*args, **kwargs):
    return RhinoBrep.from_sphere(*args, **kwargs)


@plugin(category="factories", requires=["Rhino"])
def from_mesh(*args, **kwargs):
    return RhinoBrep.from_mesh(*args, **kwargs)
