"""
********************************************************************************
artists
********************************************************************************

.. currentmodule:: compas_rhino.artists


Primitive Artists
=================

.. autosummary::
    :toctree: generated/
    :nosignatures:

    CircleArtist
    FrameArtist
    LineArtist
    PlaneArtist
    PointArtist
    PolygonArtist
    PolylineArtist
    VectorArtist


Shape Artists
=============

.. autosummary::
    :toctree: generated/
    :nosignatures:

    BoxArtist
    CapsuleArtist
    ConeArtist
    CylinderArtist
    PolyhedronArtist
    SphereArtist
    TorusArtist


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

    RhinoArtist

"""
from __future__ import absolute_import

import inspect

from compas.plugins import plugin
from compas.artists import Artist
from compas.artists import DataArtistNotRegistered

from compas.geometry import Circle
from compas.geometry import Frame
from compas.geometry import Line
from compas.geometry import Plane
from compas.geometry import Point
from compas.geometry import Polygon
from compas.geometry import Polyline
from compas.geometry import Vector

from compas.geometry import Box
from compas.geometry import Capsule
from compas.geometry import Cone
from compas.geometry import Cylinder
from compas.geometry import Polyhedron
from compas.geometry import Sphere
from compas.geometry import Torus

from compas.datastructures import Mesh
from compas.datastructures import Network
from compas.datastructures import VolMesh

from compas.robots import RobotModel

from .artist import RhinoArtist
from .circleartist import CircleArtist
from .frameartist import FrameArtist
from .lineartist import LineArtist
from .planeartist import PlaneArtist
from .pointartist import PointArtist
from .polygonartist import PolygonArtist
from .polylineartist import PolylineArtist
from .vectorartist import VectorArtist
from .boxartist import BoxArtist
from .capsuleartist import CapsuleArtist
from .coneartist import ConeArtist
from .cylinderartist import CylinderArtist
from .polyhedronartist import PolyhedronArtist
from .sphereartist import SphereArtist
from .torusartist import TorusArtist
from .meshartist import MeshArtist
from .networkartist import NetworkArtist
from .volmeshartist import VolMeshArtist
from .robotmodelartist import RobotModelArtist

Artist.register(Circle, CircleArtist)
Artist.register(Frame, FrameArtist)
Artist.register(Line, LineArtist)
Artist.register(Plane, PlaneArtist)
Artist.register(Point, PointArtist)
Artist.register(Polygon, PolygonArtist)
Artist.register(Polyline, PolylineArtist)
Artist.register(Vector, VectorArtist)
Artist.register(Box, BoxArtist)
Artist.register(Capsule, CapsuleArtist)
Artist.register(Cone, ConeArtist)
Artist.register(Cylinder, CylinderArtist)
Artist.register(Polyhedron, PolyhedronArtist)
Artist.register(Sphere, SphereArtist)
Artist.register(Torus, TorusArtist)
Artist.register(Mesh, MeshArtist)
Artist.register(Network, NetworkArtist)
Artist.register(VolMesh, VolMeshArtist)
Artist.register(RobotModel, RobotModelArtist)


@plugin(category='factories', pluggable_name='new_artist', requires=['Rhino'])
def new_artist_rhino(cls, *args, **kwargs):
    data = args[0]
    dtype = type(data)
    if dtype not in Artist.ITEM_ARTIST:
        raise DataArtistNotRegistered('No Rhino artist is registered for this data type: {}'.format(dtype))
    # TODO: move this to the plugin module and/or to a dedicated function
    cls = Artist.ITEM_ARTIST[dtype]
    for name, value in inspect.getmembers(cls):
        if inspect.ismethod(value):
            if hasattr(value, '__isabstractmethod__'):
                raise Exception('Abstract method not implemented')
    return super(Artist, cls).__new__(cls)


__all__ = [
    'RhinoArtist',
    'CircleArtist',
    'FrameArtist',
    'LineArtist',
    'PlaneArtist',
    'PointArtist',
    'PolygonArtist',
    'PolylineArtist',
    'VectorArtist',
    'BoxArtist',
    'CapsuleArtist',
    'ConeArtist',
    'CylinderArtist',
    'PolyhedronArtist',
    'SphereArtist',
    'TorusArtist',
    'MeshArtist',
    'NetworkArtist',
    'VolMeshArtist',
    'RobotModelArtist'
]
