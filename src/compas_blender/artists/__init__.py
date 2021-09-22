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

    BoxArtist
    CapsuleArtist
    ConeArtist
    CylinderArtist
    FrameArtist
    NetworkArtist
    MeshArtist
    PolyhedronArtist
    RobotModelArtist
    SphereArtist

"""
import inspect

from compas.plugins import plugin
from compas.artists import Artist
from compas.artists import DataArtistNotRegistered

from compas.geometry import Box
from compas.geometry import Capsule
from compas.geometry import Cone
from compas.geometry import Cylinder
from compas.geometry import Frame
from compas.geometry import Polyhedron
from compas.geometry import Sphere
from compas.geometry import Torus
from compas.datastructures import Mesh
from compas.datastructures import Network
from compas.robots import RobotModel

from .artist import BlenderArtist  # noqa: F401
from .boxartist import BoxArtist
from .capsuleartist import CapsuleArtist
from .coneartist import ConeArtist
from .cylinderartist import CylinderArtist
from .frameartist import FrameArtist
from .meshartist import MeshArtist
from .networkartist import NetworkArtist
from .polyhedronartist import PolyhedronArtist
from .robotmodelartist import RobotModelArtist
from .sphereartist import SphereArtist
from .torusartist import TorusArtist


Artist.register(Box, BoxArtist)
Artist.register(Capsule, CapsuleArtist)
Artist.register(Cone, ConeArtist)
Artist.register(Cylinder, CylinderArtist)
Artist.register(Frame, FrameArtist)
Artist.register(Mesh, MeshArtist)
Artist.register(Network, NetworkArtist)
Artist.register(Polyhedron, PolyhedronArtist)
Artist.register(RobotModel, RobotModelArtist)
Artist.register(Sphere, SphereArtist)
Artist.register(Torus, TorusArtist)


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
    'BoxArtist',
    'CapsuleArtist',
    'ConeArtist',
    'CylinderArtist',
    'FrameArtist',
    'MeshArtist',
    'NetworkArtist',
    'PolyhedronArtist',
    'RobotModelArtist',
    'SphereArtist',
    'TorusArtist',
]
