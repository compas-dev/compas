"""
********************************************************************************
compas_blender.geometry
********************************************************************************

.. currentmodule:: compas_blender.geometry


Object-oriented wrappers for native Blender geometry.


.. autosummary::
    :toctree: generated/

    BlenderPoint
    BlenderCurve
    BlenderMesh
    BlenderSurface

"""
from __future__ import absolute_import


class BlenderGeometry(object):
    pass


from .point import BlenderPoint
from .curve import BlenderCurve
from .mesh import BlenderMesh
from .surface import BlenderSurface


__all__ = ['BlenderPoint', 'BlenderCurve', 'BlenderMesh', 'BlenderSurface']
