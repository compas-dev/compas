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

from compas.plugins import plugin
from compas.artists import Artist
from compas.artists import ShapeArtist

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
import compas_rhino

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

BaseArtist = RhinoArtist

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


@plugin(category='drawing-utils', pluggable_name='clear', requires=['Rhino'])
def clear_rhino():
    compas_rhino.clear()


@plugin(category='drawing-utils', pluggable_name='redraw', requires=['Rhino'])
def redraw_rhino():
    compas_rhino.redraw()


@plugin(category='factories', requires=['Rhino'])
def register_artists():
        Artist.register(Circle, CircleArtist, context='Rhino')
        Artist.register(Frame, FrameArtist, context='Rhino')
        Artist.register(Line, LineArtist, context='Rhino')
        Artist.register(Plane, PlaneArtist, context='Rhino')
        Artist.register(Point, PointArtist, context='Rhino')
        Artist.register(Polygon, PolygonArtist, context='Rhino')
        Artist.register(Polyline, PolylineArtist, context='Rhino')
        Artist.register(Vector, VectorArtist, context='Rhino')
        Artist.register(Box, BoxArtist, context='Rhino')
        Artist.register(Capsule, CapsuleArtist, context='Rhino')
        Artist.register(Cone, ConeArtist, context='Rhino')
        Artist.register(Cylinder, CylinderArtist, context='Rhino')
        Artist.register(Polyhedron, PolyhedronArtist, context='Rhino')
        Artist.register(Sphere, SphereArtist, context='Rhino')
        Artist.register(Torus, TorusArtist, context='Rhino')
        Artist.register(Mesh, MeshArtist, context='Rhino')
        Artist.register(Network, NetworkArtist, context='Rhino')
        Artist.register(VolMesh, VolMeshArtist, context='Rhino')
        Artist.register(RobotModel, RobotModelArtist, context='Rhino')
        print('Rhino Artists registered.')


__all__ = [
    'BaseArtist',
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
    'RobotModelArtist',
]
