from compas.plugins import plugin

from .brep import RhinoBRep


@plugin(category="factories", requires=["Rhino"])
def new_brep_from_shape(cls, *args, **kwargs):
    return RhinoBRep.from_shape(*args, **kwargs)


@plugin(category="factories", requires=["Rhino"])
def new_brep_from_box(cls, *args, **kwargs):
    return RhinoBRep.from_box(*args, **kwargs)
