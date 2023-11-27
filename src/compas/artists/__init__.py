"""
This package defines artists for visualising COMPAS objects.
Every object type is paired with a corresponding artist type that is capable of visualizing the data of the object.
The artists are implemented as pluggables, and automatically switch between plugins depending on the contexct in which they are used.
"""

from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from .exceptions import DataArtistNotRegisteredError
from .exceptions import NoArtistContextError
from .artist import Artist
from .meshartist import MeshArtist
from .networkartist import NetworkArtist
from .geometryartist import GeometryArtist
from .volmeshartist import VolMeshArtist

from .artist import clear
from .artist import redraw
from .artist import register_artists


__all__ = [
    "DataArtistNotRegisteredError",
    "NoArtistContextError",
    "Artist",
    "MeshArtist",
    "NetworkArtist",
    "GeometryArtist",
    "VolMeshArtist",
    "clear",
    "redraw",
    "register_artists",
]
