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

from .artist import BlenderArtist
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


@plugin(category='factories', pluggable_name='new_artist', tryfirst=True, requires=['bpy'])
def new_artist_blender(cls, *args, **kwargs):
    # "lazy registration" seems necessary to avoid item-artist pairs to be overwritten unintentionally

    BlenderArtist.register(Box, BoxArtist)
    BlenderArtist.register(Capsule, CapsuleArtist)
    BlenderArtist.register(Cone, ConeArtist)
    BlenderArtist.register(Cylinder, CylinderArtist)
    BlenderArtist.register(Frame, FrameArtist)
    BlenderArtist.register(Mesh, MeshArtist)
    BlenderArtist.register(Network, NetworkArtist)
    BlenderArtist.register(Polyhedron, PolyhedronArtist)
    BlenderArtist.register(RobotModel, RobotModelArtist)
    BlenderArtist.register(Sphere, SphereArtist)
    BlenderArtist.register(Torus, TorusArtist)

    data = args[0]

    if 'artist_type' in kwargs:
        cls = kwargs['artist_type']
    else:
        dtype = type(data)
        if dtype not in BlenderArtist.ITEM_ARTIST:
            raise DataArtistNotRegistered('No Blender artist is registered for this data type: {}'.format(dtype))
        cls = BlenderArtist.ITEM_ARTIST[dtype]

    # TODO: move this to the plugin module and/or to a dedicated function

    for name, value in inspect.getmembers(cls):
        if inspect.isfunction(value):
            if hasattr(value, '__isabstractmethod__'):
                raise Exception('Abstract method not implemented: {}'.format(value))

    return super(Artist, cls).__new__(cls)


__all__ = [
    'BlenderArtist',
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
