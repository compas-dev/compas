"""
********************************************************************************
compas_rhino.constructors
********************************************************************************

.. currentmodule:: compas_rhino.constructors


This package contains constructors for working with COMPAS data structures in Rhino.

mesh
====

.. autosummary::
    :toctree: generated/
    :nosignatures:

    mesh_from_guid
    mesh_from_surface
    mesh_from_surface_uv
    mesh_from_surface_heightfield


volmesh
=======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    volmesh_from_polysurfaces
    volmesh_from_wireframe

"""

from __future__ import absolute_import


from .mesh import *
# from .network import *
from .volmesh import *

__all__ = [name for name in dir() if not name.startswith('_')]
