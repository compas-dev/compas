"""
********************************************************************************
artists
********************************************************************************

.. currentmodule:: compas_plotters.artists


Primitive Artists
=================

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


Datastructure Artists
=====================

.. autosummary::
    :toctree: generated/
    :nosignatures:

    MeshArtist
    NetworkArtist


Base Classes
============

.. autosummary::
    :toctree: generated/
    :nosignatures:

    PlotterArtist

"""

from compas.plugins import plugin
from compas.artists import Artist

from compas.geometry import Point
from compas.geometry import Vector
from compas.geometry import Line
from compas.geometry import Polyline
from compas.geometry import Polygon
from compas.geometry import Circle
from compas.geometry import Ellipse

from compas.datastructures import Mesh
from compas.datastructures import Network

from .artist import PlotterArtist
from .pointartist import PointArtist
from .vectorartist import VectorArtist
from .lineartist import LineArtist
from .polylineartist import PolylineArtist
from .polygonartist import PolygonArtist
from .circleartist import CircleArtist
from .ellipseartist import EllipseArtist
from .meshartist import MeshArtist
from .networkartist import NetworkArtist


@plugin(category="factories", requires=["matplotlib"])
def register_artists():
    Artist.register(Point, PointArtist, context="Plotter")
    Artist.register(Vector, VectorArtist, context="Plotter")
    Artist.register(Line, LineArtist, context="Plotter")
    Artist.register(Polyline, PolylineArtist, context="Plotter")
    Artist.register(Polygon, PolygonArtist, context="Plotter")
    Artist.register(Circle, CircleArtist, context="Plotter")
    Artist.register(Ellipse, EllipseArtist, context="Plotter")
    Artist.register(Mesh, MeshArtist, context="Plotter")
    Artist.register(Network, NetworkArtist, context="Plotter")


__all__ = [
    "PlotterArtist",
    "PointArtist",
    "VectorArtist",
    "LineArtist",
    "PolylineArtist",
    "PolygonArtist",
    "CircleArtist",
    "EllipseArtist",
    "MeshArtist",
    "NetworkArtist",
]
