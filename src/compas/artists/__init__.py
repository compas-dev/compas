"""
********************************************************************************
artists
********************************************************************************

.. currentmodule:: compas.artists

.. rst-class:: lead

For visualization of data objects such as geometry objects, robots, and data structures, COMPAS provides "artists".
Every data object type is paired with a corresponding artist type that is capable of visualizing the data.
This package provides base artist classes with pluggable methods
that receive an implementation from plugins defined by various visualization contexts.


Classes
=======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    Artist
    CurveArtist
    RobotModelArtist
    MeshArtist
    NetworkArtist
    PrimitiveArtist
    ShapeArtist
    SurfaceArtist
    VolMeshArtist


Exceptions
==========

.. autosummary::
    :toctree: generated/
    :nosignatures:

    DataArtistNotRegistered
    NoArtistContextError


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
from .exceptions import NoArtistContextError
from .artist import Artist
from .curveartist import CurveArtist
from .meshartist import MeshArtist
from .networkartist import NetworkArtist
from .primitiveartist import PrimitiveArtist
from .robotmodelartist import RobotModelArtist
from .shapeartist import ShapeArtist
from .surfaceartist import SurfaceArtist
from .volmeshartist import VolMeshArtist

from .artist import clear  # noqa: F401
from .artist import redraw  # noqa: F401
from .artist import register_artists  # noqa: F401

BaseRobotModelArtist = RobotModelArtist


__all__ = [
    "DataArtistNotRegistered",
    "NoArtistContextError",
    "Artist",
    "CurveArtist",
    "MeshArtist",
    "NetworkArtist",
    "PrimitiveArtist",
    "RobotModelArtist",
    "ShapeArtist",
    "SurfaceArtist",
    "VolMeshArtist",
]
