"""
********************************************************************************
compas_rhino.artists
********************************************************************************

.. currentmodule:: compas_rhino.artists


Artists for visualising (painting) COMPAS data structures in Rhino.


.. autosummary::
    :toctree: generated/
    :nosignatures:

    Artist
    MeshArtist
    NetworkArtist
    VolMeshArtist

"""
from __future__ import absolute_import

from .artist import Artist
from .meshartist import MeshArtist
from .networkartist import NetworkArtist
from .volmeshartist import VolMeshArtist
from .primitiveartist import PrimitiveArtist
from .pointartist import PointArtist


__all__ = [name for name in dir() if not name.startswith('_')]


from compas.geometry import Point

Artist.register(Point, PointArtist)
