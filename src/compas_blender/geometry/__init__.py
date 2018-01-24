"""
********************************************************************************
geometry
********************************************************************************

.. module:: compas_blender.geometry


Object-oriented wrappers for native Blender geometry.


.. autosummary::
    :toctree: generated/

    BlenderPoint
    BlenderCurve
    BlenderMesh
    BlenderSurface

"""

from .point import BlenderPoint
from .curve import BlenderCurve
from .mesh import BlenderMesh
from .surface import BlenderSurface

__all__ = ['BlenderPoint', 'BlenderCurve', 'BlenderMesh', 'BlenderSurface', ]
