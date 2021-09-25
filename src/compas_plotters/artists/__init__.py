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
    NetworkArtist

"""
import inspect

from compas.plugins import plugin
from compas.artists import Artist
from compas.artists import DataArtistNotRegistered

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

Artist.register(Point, PointArtist)
Artist.register(Vector, VectorArtist)
Artist.register(Line, LineArtist)
Artist.register(Polyline, PolylineArtist)
Artist.register(Polygon, PolygonArtist)
Artist.register(Circle, CircleArtist)
Artist.register(Ellipse, EllipseArtist)
Artist.register(Mesh, MeshArtist)
Artist.register(Network, NetworkArtist)


@plugin(category='factories', pluggable_name='new_artist', trylast=True, requires=['matplotlib'])
def new_artist_plotter(cls, *args, **kwargs):
    data = args[0]
    dtype = type(data)
    if dtype not in Artist.ITEM_ARTIST:
        raise DataArtistNotRegistered('No Plotter artist is registered for this data type: {}'.format(dtype))
    # TODO: move this to the plugin module and/or to a dedicated function
    cls = Artist.ITEM_ARTIST[dtype]
    for name, value in inspect.getmembers(cls):
        if inspect.isfunction(value):
            if hasattr(value, '__isabstractmethod__'):
                raise Exception('Abstract method not implemented: {}'.format(value))
    return super(Artist, cls).__new__(cls)


__all__ = [
    'PlotterArtist',
    'PointArtist',
    'VectorArtist',
    'LineArtist',
    'PolylineArtist',
    'PolygonArtist',
    'CircleArtist',
    'EllipseArtist',
    'MeshArtist',
    'NetworkArtist'
]
