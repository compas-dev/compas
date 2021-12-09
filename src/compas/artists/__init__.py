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
