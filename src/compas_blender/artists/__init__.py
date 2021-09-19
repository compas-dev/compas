"""
********************************************************************************
artists
********************************************************************************

.. currentmodule:: compas_blender.artists

Artists for visualising (painting) COMPAS data structures in Blender.


Base Classes
============

.. autosummary::
    :toctree: generated/

    BlenderArtist


Classes
=======

.. autosummary::
    :toctree: generated/

    FrameArtist
    NetworkArtist
    MeshArtist
    RobotModelArtist

"""
import inspect

from compas.plugins import plugin
from compas.artists import Artist
from compas.artists import DataArtistNotRegistered

from compas.geometry import Frame
from compas.datastructures import Mesh
from compas.datastructures import Network
from compas.robots import RobotModel

from .artist import BlenderArtist  # noqa: F401
from .frameartist import FrameArtist
from .meshartist import MeshArtist
from .networkartist import NetworkArtist
from .robotmodelartist import (  # noqa: F401
    BaseRobotModelArtist,
    RobotModelArtist
)


Artist.register(Frame, FrameArtist)
Artist.register(Mesh, MeshArtist)
Artist.register(Network, NetworkArtist)
Artist.register(RobotModel, RobotModelArtist)


@plugin(category='factories', pluggable_name='new_artist', requires=['bpy'])
def new_artist_blender(cls, *args, **kwargs):
    data = args[0]
    dtype = type(data)
    if dtype not in Artist.ITEM_ARTIST:
        raise DataArtistNotRegistered('No Blender artist is registered for this data type: {}'.format(dtype))
    cls = Artist.ITEM_ARTIST[dtype]
    for name, value in inspect.getmembers(cls):
        if inspect.isfunction(value):
            if hasattr(value, '__isabstractmethod__'):
                raise Exception('Abstract method not implemented: {}'.format(value))
    return super(Artist, cls).__new__(cls)


__all__ = [
    'FrameArtist',
    'NetworkArtist',
    'MeshArtist',
    'RobotModelArtist'
]
