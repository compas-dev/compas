"""
********************************************************************************
compas_plotters.artists
********************************************************************************

.. currentmodule:: compas_plotters.artists


Classes
=======

.. autosummary::
    :toctree: generated/
    :nosignatures:


"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.geometry import Point
from compas.geometry import Vector
from compas.geometry import Line
from compas.geometry import Circle
from compas.geometry import Ellipse
from compas.datastructures import Mesh

from .artist import Artist

from .pointartist import PointArtist
from .vectorartist import VectorArtist
from .segmentartist import SegmentArtist  # noqa: F401
from .lineartist import LineArtist
from .circleartist import CircleArtist
from .ellipseartist import EllipseArtist
from .meshartist import MeshArtist

Artist.register(Point, PointArtist)
Artist.register(Vector, VectorArtist)
Artist.register(Line, LineArtist)
Artist.register(Circle, CircleArtist)
Artist.register(Ellipse, EllipseArtist)
Artist.register(Mesh, MeshArtist)


__all__ = [name for name in dir() if not name.startswith('_')]
