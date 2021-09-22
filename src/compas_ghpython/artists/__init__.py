"""
********************************************************************************
artists
********************************************************************************

.. currentmodule:: compas_ghpython.artists


Base Classes
============

.. autosummary::
    :toctree: generated/
    :nosignatures:

    GHArtist


Geometry Artists
================

.. autosummary::
    :toctree: generated/
    :nosignatures:

    CircleArtist
    FrameArtist
    LineArtist
    PointArtist
    PolylineArtist


Datastructure Artists
=====================

.. autosummary::
    :toctree: generated/
    :nosignatures:

    MeshArtist
    NetworkArtist
    VolMeshArtist


Robot Artist
============

.. autosummary::
    :toctree: generated/
    :nosignatures:

    RobotModelArtist

"""
from __future__ import absolute_import

import inspect

from compas.plugins import plugin
from compas.artists import Artist
from compas.artists import DataArtistNotRegistered

from compas.geometry import Circle
from compas.geometry import Frame
from compas.geometry import Line
from compas.geometry import Point
from compas.geometry import Polyline

from compas.datastructures import Mesh
from compas.datastructures import Network
from compas.datastructures import VolMesh

from .artist import GHArtist
from .circleartist import CircleArtist
from .frameartist import FrameArtist
from .lineartist import LineArtist
from .pointartist import PointArtist
from .polylineartist import PolylineArtist
from .meshartist import MeshArtist
from .networkartist import NetworkArtist
from .volmeshartist import VolMeshArtist
from .robotmodelartist import RobotModelArtist

Artist.register(Circle, CircleArtist)
Artist.register(Frame, FrameArtist)
Artist.register(Line, LineArtist)
Artist.register(Point, PointArtist)
Artist.register(Polyline, PolylineArtist)
Artist.register(Mesh, MeshArtist)
Artist.register(Network, NetworkArtist)
Artist.register(VolMesh, VolMeshArtist)


@plugin(category='factories', pluggable_name='new_artist', requires=['ghpythonlib'])
def new_artist_gh(cls, *args, **kwargs):
    data = args[0]
    dtype = type(data)
    if dtype not in Artist.ITEM_ARTIST:
        raise DataArtistNotRegistered('No GH artist is registered for this data type: {}'.format(dtype))
    # TODO: move this to the plugin module and/or to a dedicated function
    cls = Artist.ITEM_ARTIST[dtype]
    for name, value in inspect.getmembers(cls):
        if inspect.ismethod(value):
            if hasattr(value, '__isabstractmethod__'):
                raise Exception('Abstract method not implemented')
    return super(Artist, cls).__new__(cls)


__all__ = [
    'GHArtist',
    'PrimitiveArtist',
    'ShapeArtist',
    'CircleArtist',
    'FrameArtist',
    'LineArtist',
    'PointArtist',
    'PolylineArtist',
    'MeshArtist',
    'NetworkArtist',
    'VolMeshArtist',
    'RobotModelArtist'
]
