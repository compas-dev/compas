
try:
    import bpy
except ImportError:
    pass


"""
********************************************************************************
compas_blender.geometry
********************************************************************************

.. currentmodule:: compas_blender.geometry

Object-oriented convenience wrappers for native Blender geometry.

.. autosummary::
    :toctree: generated/

    BlenderCurve
    BlenderMesh
    BlenderPoint
    BlenderSurface

"""


class BlenderGeometry(object):

    def __init__(self, obj):

        self.object     = obj
        self.name       = obj.name
        self.geometry   = obj.data
        self.otype      = obj.type
        self.attributes = {}


    @property
    def location(self):

        return list(self.object.location)


    @classmethod
    def from_selection(cls):

        raise NotImplementedError


    @classmethod
    def from_name(cls, name):

        return BlenderGeometry(obj=bpy.data.objects[name])


    @staticmethod
    def find(guid):

        raise NotImplementedError


    @staticmethod
    def refresh():

        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)


    def delete(self):

        raise NotImplementedError


    def purge(self):

        raise NotImplementedError


    def hide(self):

        raise NotImplementedError


    def show(self):

        raise NotImplementedError


    def select(self):

        raise NotImplementedError


    def unselect(self):

        raise NotImplementedError


    def closest_point(self, *args, **kwargs):

        raise NotImplementedError


    def closest_points(self, *args, **kwargs):

        raise NotImplementedError


from .point import BlenderPoint
from .curve import BlenderCurve
from .mesh import BlenderMesh
from .surface import BlenderSurface


__all__ = [
    'BlenderGeometry',
    'BlenderPoint',
    'BlenderCurve',
    'BlenderMesh',
    'BlenderSurface',
]
