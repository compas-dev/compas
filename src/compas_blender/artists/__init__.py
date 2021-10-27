"""
********************************************************************************
artists
********************************************************************************

.. currentmodule:: compas_blender.artists

Artists for visualising (painting) COMPAS data structures in Blender.


Primitive Artists
=================

.. autosummary::
    :toctree: generated/

    FrameArtist


Shape Artists
=============

.. autosummary::
    :toctree: generated/
    :nosignatures:

    BoxArtist
    CapsuleArtist
    ConeArtist
    CylinderArtist
    SphereArtist
    PolyhedronArtist


Datastructure Artists
=====================

.. autosummary::
    :toctree: generated/
    :nosignatures:

    NetworkArtist
    MeshArtist


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

    BlenderArtist

"""

import compas_blender

from compas.plugins import plugin
from compas.plugins import PluginValidator
from compas.artists import Artist

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


@plugin(category='drawing-utils', pluggable_name='clear', requires=['bpy'])
def clear_blender():
    compas_blender.clear()


@plugin(category='drawing-utils', pluggable_name='redraw', requires=['bpy'])
def redraw_blender():
    compas_blender.redraw()


artists_registered = False


@plugin(category='factories', pluggable_name='new_artist', tryfirst=True, requires=['bpy'])
def new_artist_blender(cls, *args, **kwargs):
    # "lazy registration" seems necessary to avoid item-artist pairs to be overwritten unintentionally
    global artists_registered

    if not artists_registered:
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
        artists_registered = True

    data = args[0]

    cls = Artist.get_artist_cls(data, **kwargs)

    PluginValidator.ensure_implementations(cls)

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
