
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

from .artist import __all_ as a
from .meshartist import __all_ as b
from .networkartist import __all_ as c
from .volmeshartist import __all_ as d

__all__ = a + b + c + d
