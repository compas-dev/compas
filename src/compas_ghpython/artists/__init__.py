"""
********************************************************************************
compas_ghpython.artists
********************************************************************************

.. currentmodule:: compas_ghpython.artists


Artists for visualising (painting) COMPAS data structures in compas_ghpython.


.. autosummary::
    :toctree: generated/

    MeshArtist
    NetworkArtist
    VolMeshArtist

"""
from __future__ import absolute_import

from .meshartist import *
from .networkartist import *
from .volmeshartist import *

__all__ = [name for name in dir() if not name.startswith('_')]
