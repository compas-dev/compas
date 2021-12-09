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

    BoxArtist
    CapsuleArtist
    CircleArtist
    ConeArtist
    CylinderArtist
    FrameArtist
    LineArtist
    PointArtist
    PolygonArtist
    PolyhedronArtist
    PolylineArtist
    SphereArtist
    TorusArtist
    VectorArtist


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

from compas.plugins import plugin
from compas.artists import Artist
from compas.artists import ShapeArtist

from compas.geometry import Box
from compas.geometry import Capsule
from compas.geometry import Circle
from compas.geometry import Cone
from compas.geometry import Cylinder
from compas.geometry import Frame
from compas.geometry import Line
from compas.geometry import Point
from compas.geometry import Polygon
from compas.geometry import Polyhedron
from compas.geometry import Polyline
from compas.geometry import Sphere
from compas.geometry import Torus
from compas.geometry import Vector

from compas.datastructures import Mesh
from compas.datastructures import Network
from compas.datastructures import VolMesh

from compas.robots import RobotModel

from .artist import GHArtist
from .boxartist import BoxArtist
from .capsuleartist import CapsuleArtist
from .circleartist import CircleArtist
from .coneartist import ConeArtist
from .cylinderartist import CylinderArtist
from .frameartist import FrameArtist
from .lineartist import LineArtist
from .meshartist import MeshArtist
from .networkartist import NetworkArtist
from .pointartist import PointArtist
from .polygonartist import PolygonArtist
from .polyhedronartist import PolyhedronArtist
from .polylineartist import PolylineArtist
from .robotmodelartist import RobotModelArtist
from .sphereartist import SphereArtist
from .torusartist import TorusArtist
from .vectorartist import VectorArtist
from .volmeshartist import VolMeshArtist


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


@plugin(category='factories', pluggable_name='register_artists', requires=['Rhino'])
def register_artists_gh():
    Artist.register(Box, BoxArtist, context='GrassHopper')
    Artist.register(Capsule, CapsuleArtist, context='GrassHopper')
    Artist.register(Circle, CircleArtist, context='GrassHopper')
    Artist.register(Cone, ConeArtist, context='GrassHopper')
    Artist.register(Cylinder, CylinderArtist, context='GrassHopper')
    Artist.register(Frame, FrameArtist, context='GrassHopper')
    Artist.register(Line, LineArtist, context='GrassHopper')
    Artist.register(Mesh, MeshArtist, context='GrassHopper')
    Artist.register(Network, NetworkArtist, context='GrassHopper')
    Artist.register(Point, PointArtist, context='GrassHopper')
    Artist.register(Polygon, PolygonArtist, context='GrassHopper')
    Artist.register(Polyhedron, PolyhedronArtist, context='GrassHopper')
    Artist.register(Polyline, PolylineArtist, context='GrassHopper')
    Artist.register(RobotModel, RobotModelArtist, context='GrassHopper')
    Artist.register(Sphere, SphereArtist, context='GrassHopper')
    Artist.register(Torus, TorusArtist, context='GrassHopper')
    Artist.register(Vector, VectorArtist, context='GrassHopper')
    Artist.register(VolMesh, VolMeshArtist, context='GrassHopper')
    print('GH Artists registered.')


__all__ = [
    'GHArtist',
    'ShapeArtist',
    'BoxArtist',
    'CapsuleArtist',
    'CircleArtist',
    'ConeArtist',
    'CylinderArtist',
    'FrameArtist',
    'LineArtist',
    'MeshArtist',
    'NetworkArtist',
    'PointArtist',
    'PolygonArtist',
    'PolyhedronArtist',
    'PolylineArtist',
    'RobotModelArtist',
    'SphereArtist',
    'TorusArtist',
    'VectorArtist',
    'VolMeshArtist',
]
