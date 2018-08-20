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
from __future__ import absolute_import

from .meshartist import *
from .networkartist import *
from .volmeshartist import *

from . import meshartist
from . import networkartist
from . import volmeshartist

__all__ = meshartist.__all__ + networkartist.__all__ + volmeshartist.__all__
