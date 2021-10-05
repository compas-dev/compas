"""
********************************************************************************
artists
********************************************************************************

.. currentmodule:: compas_ghpython.artists


Primitive Artists
=================

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


Base Classes
============

.. autosummary::
    :toctree: generated/
    :nosignatures:

    GHArtist

"""
from __future__ import absolute_import

import inspect

from compas.plugins import plugin
from compas.artists import Artist
from compas.artists import ShapeArtist
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

ShapeArtist.default_color = (255, 255, 255)

MeshArtist.default_color = (0, 0, 0)
MeshArtist.default_vertexcolor = (255, 255, 255)
MeshArtist.default_edgecolor = (0, 0, 0)
MeshArtist.default_facecolor = (255, 255, 255)

NetworkArtist.default_nodecolor = (255, 255, 255)
NetworkArtist.default_edgecolor = (0, 0, 0)

VolMeshArtist.default_color = (0, 0, 0)
VolMeshArtist.default_vertexcolor = (255, 255, 255)
VolMeshArtist.default_edgecolor = (0, 0, 0)
VolMeshArtist.default_facecolor = (255, 255, 255)
VolMeshArtist.default_cellcolor = (255, 0, 0)


@plugin(category='factories', pluggable_name='new_artist', requires=['ghpythonlib'])
def new_artist_gh(cls, *args, **kwargs):
    # "lazy registration" seems necessary to avoid item-artist pairs to be overwritten unintentionally

    GHArtist.register(Circle, CircleArtist)
    GHArtist.register(Frame, FrameArtist)
    GHArtist.register(Line, LineArtist)
    GHArtist.register(Point, PointArtist)
    GHArtist.register(Polyline, PolylineArtist)
    GHArtist.register(Mesh, MeshArtist)
    GHArtist.register(Network, NetworkArtist)
    GHArtist.register(VolMesh, VolMeshArtist)

    data = args[0]

    if 'artist_type' in kwargs:
        cls = kwargs['artist_type']
    else:
        dtype = type(data)
        if dtype not in GHArtist.ITEM_ARTIST:
            raise DataArtistNotRegistered('No GH artist is registered for this data type: {}'.format(dtype))
        cls = GHArtist.ITEM_ARTIST[dtype]

    # TODO: move this to the plugin module and/or to a dedicated function

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
