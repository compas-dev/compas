"""
********************************************************************************
compas_plotters.artists
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


def verify_not_blender():
    try:
        import bpy  # noqa: F401
    except ImportError:
        return True
    else:
        return False


artists_registered = False


@plugin(category='factories', pluggable_name='new_artist', trylast=True, requires=['matplotlib', verify_not_blender])
def new_artist_plotter(cls, *args, **kwargs):
    # "lazy registration" seems necessary to avoid item-artist pairs to be overwritten unintentionally
    global artists_registered

    if not artists_registered:
        PlotterArtist.register(Point, PointArtist)
        PlotterArtist.register(Vector, VectorArtist)
        PlotterArtist.register(Line, LineArtist)
        PlotterArtist.register(Polyline, PolylineArtist)
        PlotterArtist.register(Polygon, PolygonArtist)
        PlotterArtist.register(Circle, CircleArtist)
        PlotterArtist.register(Ellipse, EllipseArtist)
        PlotterArtist.register(Mesh, MeshArtist)
        PlotterArtist.register(Network, NetworkArtist)
        artists_registered = True

    data = args[0]

    if 'artist_type' in kwargs:
        cls = kwargs['artist_type']
    else:
        dtype = type(data)
        if dtype not in PlotterArtist.ITEM_ARTIST:
            raise DataArtistNotRegistered('No Plotter artist is registered for this data type: {}'.format(dtype))
        cls = PlotterArtist.ITEM_ARTIST[dtype]

    # TODO: move this to the plugin module and/or to a dedicated function

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
