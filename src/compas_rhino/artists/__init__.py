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

    BoxArtist


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

from ._artist import *
from ._primitiveartist import *
# from ._shapeartist import *
# from ._datastructureartist import *

from .pointartist import *
from .lineartist import *
from .frameartist import *

from .artist import *
from .meshartist import *
from .networkartist import *
from .volmeshartist import *

from compas.geometry import Frame
from compas.geometry import Line
from compas.geometry import Point

_Artist.register(Point, PointArtist)
_Artist.register(Frame, FrameArtist)
_Artist.register(Line, LineArtist)

__all__ = [name for name in dir() if not name.startswith('_')]
