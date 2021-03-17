"""
********************************************************************************
geometry
********************************************************************************

.. currentmodule:: compas_blender.geometry

Object-oriented convenience wrappers for native Blender geometry.

.. autosummary::
    :toctree: generated/

    BlenderCurve
    BlenderMesh

"""
from ._geometry import BaseBlenderGeometry
from .curve import BlenderCurve
from .mesh import BlenderMesh

__all__ = [
    'BaseBlenderGeometry',
    'BlenderCurve',
    'BlenderMesh'
]
