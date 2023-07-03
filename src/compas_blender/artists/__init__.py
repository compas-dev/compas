"""
********************************************************************************
artists
********************************************************************************

.. currentmodule:: compas_blender.artists

.. rst-class:: lead

Artists for visualizing (painting) COMPAS geometry, robots, and data structures in Blender.
The artists in this package provide plugins for the pluggable methods of the base artists defined in :mod:`compas.artists`.
They can be used directly from here (:mod:`compas_blender.artists`), or through the base artist :class:`~compas.artists.Artist`.


Primitive Artists
=================

.. autosummary::
    :toctree: generated/
    :nosignatures:

    CircleArtist
    FrameArtist
    LineArtist
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


Curve and Surface Artists
=========================

.. autosummary::
    :toctree: generated/
    :nosignatures:

    CurveArtist
    SurfaceArtist


Datastructure Artists
=====================

.. autosummary::
    :toctree: generated/
    :nosignatures:

    MeshArtist
    NetworkArtist


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
from compas.artists import Artist

from compas.geometry import Box
from compas.geometry import Capsule
from compas.geometry import Circle
from compas.geometry import Cone
from compas.geometry import Curve
from compas.geometry import Cylinder
from compas.geometry import Frame
from compas.geometry import Line
from compas.geometry import Point
from compas.geometry import Polygon
from compas.geometry import Polyhedron
from compas.geometry import Polyline
from compas.geometry import Sphere
from compas.geometry import Surface
from compas.geometry import Torus
from compas.geometry import Vector
from compas.datastructures import Mesh
from compas.datastructures import Network
from compas.datastructures import VolMesh
from compas.robots import RobotModel

from .artist import BlenderArtist
from .boxartist import BoxArtist
from .capsuleartist import CapsuleArtist
from .circleartist import CircleArtist
from .coneartist import ConeArtist
from .curveartist import CurveArtist
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
from .surfaceartist import SurfaceArtist
from .torusartist import TorusArtist
from .vectorartist import VectorArtist
from .volmeshartist import VolMeshArtist


@plugin(category="drawing-utils", pluggable_name="clear", requires=["bpy"])
def clear_blender():
    compas_blender.clear()


@plugin(category="drawing-utils", pluggable_name="redraw", requires=["bpy"])
def redraw_blender():
    compas_blender.redraw()


@plugin(category="factories", requires=["bpy"])
def register_artists():
    Artist.register(Box, BoxArtist, context="Blender")
    Artist.register(Capsule, CapsuleArtist, context="Blender")
    Artist.register(Circle, CircleArtist, context="Blender")
    Artist.register(Cone, ConeArtist, context="Blender")
    Artist.register(Curve, CurveArtist, context="Blender")
    Artist.register(Cylinder, CylinderArtist, context="Blender")
    Artist.register(Frame, FrameArtist, context="Blender")
    Artist.register(Line, LineArtist, context="Blender")
    Artist.register(Mesh, MeshArtist, context="Blender")
    Artist.register(Network, NetworkArtist, context="Blender")
    Artist.register(Point, PointArtist, context="Blender")
    Artist.register(Polygon, PolygonArtist, context="Blender")
    Artist.register(Polyhedron, PolyhedronArtist, context="Blender")
    Artist.register(Polyline, PolylineArtist, context="Blender")
    Artist.register(RobotModel, RobotModelArtist, context="Blender")
    Artist.register(Sphere, SphereArtist, context="Blender")
    Artist.register(Surface, SurfaceArtist, context="Blender")
    Artist.register(Torus, TorusArtist, context="Blender")
    Artist.register(Vector, VectorArtist, context="Blender")
    Artist.register(VolMesh, VolMeshArtist, context="Blender")
    print("Blender Artists registered.")


__all__ = [
    "BlenderArtist",
    "BoxArtist",
    "CapsuleArtist",
    "CircleArtist",
    "ConeArtist",
    "CurveArtist",
    "CylinderArtist",
    "FrameArtist",
    "LineArtist",
    "MeshArtist",
    "NetworkArtist",
    "PointArtist",
    "PolygonArtist",
    "PolyhedronArtist",
    "PolylineArtist",
    "RobotModelArtist",
    "SphereArtist",
    "SurfaceArtist",
    "TorusArtist",
    "VectorArtist",
    "VolMeshArtist",
]
