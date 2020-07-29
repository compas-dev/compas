"""
********************************************************************************
artists
********************************************************************************

.. currentmodule:: compas_ghpython.artists


Artists for visualising (painting) COMPAS data structures in compas_ghpython.

Classes
========

.. autosummary::
    :toctree: generated/

    MeshArtist
    PointArtist
    NetworkArtist
    VolMeshArtist

Base Classes
============
.. autosummary::
    :toctree: generated/
    :nosignatures:

    BaseArtist
    PrimitiveArtist

"""
from __future__ import absolute_import

from .base import BaseArtist

from .primitiveartist import PrimitiveArtist  # noqa: F401

from .pointartist import PointArtist

from .meshartist import *  # noqa: F401 F403
from .networkartist import *  # noqa: F401 F403
from .volmeshartist import *  # noqa: F401 F403

__all__ = [name for name in dir() if not name.startswith('_')]
