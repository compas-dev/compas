"""
********************************************************************************
compas_blender.artists
********************************************************************************

.. currentmodule:: compas_blender.artists

Artists for visualising (painting) COMPAS data structures in Blender.


.. autosummary::
    :toctree: generated/

    MeshArtist
    NetworkArtist
    VolMeshArtist

"""

from .artist import *
from .meshartist import *
from .networkartist import *
from .volmeshartist import *

__all__ = [name for name in dir() if not name.startswith('_')]
