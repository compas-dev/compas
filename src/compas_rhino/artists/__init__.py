"""
********************************************************************************
compas_rhino.artists
********************************************************************************

.. currentmodule:: compas_rhino.artists

Artists for visualising (painting) COMPAS objects in Rhino.

Primitive Artists
=================

.. autosummary::
    :toctree: generated/
    :nosignatures:

    PointArtist
    LineArtist
    FrameArtist


Shape Artists
=============

.. autosummary::
    :toctree: generated/
    :nosignatures:


Data Structure Artists
======================

.. autosummary::
    :toctree: generated/
    :nosignatures:

    MeshArtist
    NetworkArtist
    VolMeshArtist

"""
from __future__ import absolute_import

from ._artist import _Artist
from ._primitiveartist import *  # noqa: F401 F403

from .pointartist import PointArtist
from .lineartist import LineArtist
from .frameartist import FrameArtist

from .artist import *  # noqa: F401 F403
from .meshartist import *  # noqa: F401 F403
from .networkartist import *  # noqa: F401 F403
from .volmeshartist import *  # noqa: F401 F403

from compas.geometry import Frame
from compas.geometry import Line
from compas.geometry import Point

_Artist.register(Point, PointArtist)
_Artist.register(Frame, FrameArtist)
_Artist.register(Line, LineArtist)

__all__ = [name for name in dir() if not name.startswith('_')]
