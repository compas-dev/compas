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
<<<<<<< HEAD
=======
from compas.geometry import Ellipse
from compas.datastructures import Mesh
>>>>>>> 1309732c7e895e8614ac6dcb0b10360471d1ab06

from .artist import Artist

from .pointartist import PointArtist
from .vectorartist import VectorArtist
from .segmentartist import SegmentArtist  # noqa: F401
from .lineartist import LineArtist
from .circleartist import CircleArtist
<<<<<<< HEAD
=======
from .ellipseartist import EllipseArtist
from .meshartist import MeshArtist
>>>>>>> 1309732c7e895e8614ac6dcb0b10360471d1ab06

Artist.register(Point, PointArtist)
Artist.register(Vector, VectorArtist)
Artist.register(Line, LineArtist)
Artist.register(Circle, CircleArtist)
<<<<<<< HEAD
=======
Artist.register(Ellipse, EllipseArtist)
Artist.register(Mesh, MeshArtist)
>>>>>>> 1309732c7e895e8614ac6dcb0b10360471d1ab06


__all__ = [name for name in dir() if not name.startswith('_')]
