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

    PointArtist
    VectorArtist
    LineArtist
    PolylineArtist
    PolygonArtist
    CircleArtist
    EllipseArtist


.. autosummary::
    :toctree: generated/
    :nosignatures:

    MeshArtist

"""
from compas.geometry import Point
from compas.geometry import Vector
from compas.geometry import Line
from compas.geometry import Polyline
from compas.geometry import Polygon
from compas.geometry import Circle
from compas.geometry import Ellipse

from compas.datastructures import Mesh

from .artist import Artist
from .pointartist import PointArtist
from .vectorartist import VectorArtist
from .lineartist import LineArtist
from .polylineartist import PolylineArtist
from .polygonartist import PolygonArtist
from .circleartist import CircleArtist
from .ellipseartist import EllipseArtist

from .meshartist import MeshArtist

Artist.register(Point, PointArtist)
Artist.register(Vector, VectorArtist)
Artist.register(Line, LineArtist)
Artist.register(Polyline, PolylineArtist)
Artist.register(Polygon, PolygonArtist)
Artist.register(Circle, CircleArtist)
Artist.register(Ellipse, EllipseArtist)

Artist.register(Mesh, MeshArtist)


__all__ = [
    'Artist',
    'PointArtist',
    'VectorArtist',
    'LineArtist',
    'PolylineArtist',
    'PolygonArtist',
    'CircleArtist',
    'EllipseArtist',
    'MeshArtist'
]
