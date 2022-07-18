from compas.plugins import plugin

from .brep import RhinoBrep

import Rhino


@plugin(category="factories", requires=["Rhino"])
def new_brep(*args, **kwargs):
    # Note: this is called inside Brep.__new__, thus Brep.__init__ will be ran by the interpreter
    # upon returning from __new__. This means any fully initialized instance returned here will be overwritten!
    return object.__new__(RhinoBrep, Rhino.Geometry.Brep())


@plugin(category="factories", requires=["Rhino"])
def from_brep(*args, **kwargs):
    return RhinoBrep.from_brep(*args, **kwargs)


@plugin(category="factories", requires=["Rhino"])
def from_box(*args, **kwargs):
    return RhinoBrep.from_box(*args, **kwargs)
