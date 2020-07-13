"""
********************************************************************************
artists
********************************************************************************

.. currentmodule:: compas_rhino.artists

Artists for visualising (painting) COMPAS objects in Rhino.


Base Classes
============

.. autosummary::
    :toctree: generated/
    :nosignatures:

    BaseArtist
    PrimitiveArtist
    ShapeArtist


Artists for Primitives
======================

.. autosummary::
    :toctree: generated/
    :nosignatures:

    PointArtist
    LineArtist
    PolylineArtist
    FrameArtist


Artists for Shapes
==================

.. autosummary::
    :toctree: generated/
    :nosignatures:


Artists for Data Structures
===========================

.. autosummary::
    :toctree: generated/
    :nosignatures:

    MeshArtist
    NetworkArtist
    VolMeshArtist

"""
from __future__ import absolute_import

from .base import BaseArtist

from .primitiveartist import PrimitiveArtist  # noqa: F401
from .shapeartist import ShapeArtist  # noqa: F401

from .pointartist import PointArtist
from .lineartist import LineArtist
from .polylineartist import PolylineArtist
from .frameartist import FrameArtist

from .networkartist import NetworkArtist
from .meshartist import MeshArtist
from .volmeshartist import VolMeshArtist  # noqa: F401

from compas.geometry import Point
from compas.geometry import Line
from compas.geometry import Polyline
from compas.geometry import Frame

from compas.datastructures import Mesh
from compas.datastructures import Network

BaseArtist.register(Point, PointArtist)
BaseArtist.register(Frame, FrameArtist)
BaseArtist.register(Line, LineArtist)
BaseArtist.register(Polyline, PolylineArtist)
BaseArtist.register(Mesh, MeshArtist)
BaseArtist.register(Network, NetworkArtist)


__all__ = [name for name in dir() if not name.startswith('_')]
