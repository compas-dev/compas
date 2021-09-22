"""
********************************************************************************
artists
********************************************************************************

.. currentmodule:: compas_ghpython.artists


Base Classes
============

.. autosummary::
    :toctree: generated/
    :nosignatures:

    GHArtist


Geometry Artists
================

.. autosummary::
    :toctree: generated/
    :nosignatures:

    CircleArtist
    FrameArtist
    LineArtist
    PointArtist
    PolylineArtist


Datastructure Artists
=====================

.. autosummary::
    :toctree: generated/
    :nosignatures:

    MeshArtist
    NetworkArtist
    VolMeshArtist


Robot Artist
============

.. autosummary::
    :toctree: generated/
    :nosignatures:

    RobotModelArtist

"""
from __future__ import absolute_import

from .artist import GHArtist

from .circleartist import CircleArtist
from .frameartist import FrameArtist
from .lineartist import LineArtist
from .pointartist import PointArtist
from .polylineartist import PolylineArtist

from .meshartist import MeshArtist
from .networkartist import NetworkArtist
from .volmeshartist import VolMeshArtist

from .robotmodelartist import RobotModelArtist

__all__ = [
    'GHArtist',
    'PrimitiveArtist',
    'ShapeArtist',
    'CircleArtist',
    'FrameArtist',
    'LineArtist',
    'PointArtist',
    'PolylineArtist',
    'MeshArtist',
    'NetworkArtist',
    'VolMeshArtist',
    'RobotModelArtist'
]
