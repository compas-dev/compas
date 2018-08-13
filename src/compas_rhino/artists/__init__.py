"""
********************************************************************************
compas_rhino.artists
********************************************************************************

.. currentmodule:: compas_rhino.artists


Artists for visualising (painting) COMPAS data structures in Rhino.


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
