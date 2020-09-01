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
from ._geometry import BaseBlenderGeometry  # noqa: F401

from .curve import BlenderCurve  # noqa: F401
from .mesh import BlenderMesh  # noqa: F401


__all__ = [name for name in dir() if not name.startswith('_')]
