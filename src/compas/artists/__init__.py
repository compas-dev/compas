"""
********************************************************************************
artists
********************************************************************************

.. currentmodule:: compas.artists

Classes
=======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    Artist
    RobotModelArtist
    MeshArtist
    NetworkArtist
    PrimitiveArtist
    ShapeArtist
    VolMeshArtist


Exceptions
==========

.. autosummary::
    :toctree: generated/
    :nosignatures:

    DataArtistNotRegistered


Pluggables
==========

.. autosummary::
    :toctree: generated/
    :nosignatures:

    clear
    redraw
    register_artists

"""
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from .exceptions import DataArtistNotRegistered
from .artist import Artist
from .meshartist import MeshArtist
from .networkartist import NetworkArtist
from .primitiveartist import PrimitiveArtist
from .robotmodelartist import RobotModelArtist
from .shapeartist import ShapeArtist
from .volmeshartist import VolMeshArtist

from .artist import clear  # noqa: F401
from .artist import redraw  # noqa: F401
from .artist import register_artists  # noqa: F401

BaseRobotModelArtist = RobotModelArtist


__all__ = [
    'DataArtistNotRegistered',
    'Artist',
    'MeshArtist',
    'NetworkArtist',
    'PrimitiveArtist',
    'RobotModelArtist',
    'ShapeArtist',
    'VolMeshArtist',
]
