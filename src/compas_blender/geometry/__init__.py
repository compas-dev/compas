
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

    def __init__(self):

        pass


    @classmethod
    def from_selection(cls):

        raise NotImplementedError


    @staticmethod
    def from_name(name):

        raise NotImplementedError


    @staticmethod
    def find(guid):

        raise NotImplementedError


    @property
    def name(self):

        raise NotImplementedError


    @name.setter
    def name(self, value):

        raise NotImplementedError


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
