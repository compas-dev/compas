"""
********************************************************************************
artists
********************************************************************************

.. currentmodule:: compas_ghpython.artists

.. rst-class:: lead

Artists for visualizing (painting) COMPAS geometry, robots, and data structures in Grasshopper using the GH Python component.
The artists in this package provide plugins for the pluggable methods of the base artists in :mod:`compas.artists`.
Therefore, they can be used directly, from here, or through the base artists :class:`~compas.artists.Artist`.


Primitive Artists
=================

.. autosummary::
    :toctree: generated/
    :nosignatures:

    BoxArtist
    CapsuleArtist
    CircleArtist
    ConeArtist
    CurveArtist
    CylinderArtist
    FrameArtist
    LineArtist
    PointArtist
    PolygonArtist
    PolyhedronArtist
    PolylineArtist
    SphereArtist
    SurfaceArtist
    TorusArtist
    VectorArtist
    BrepArtist


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
from compas.geometry import Brep

from compas.datastructures import Mesh
from compas.datastructures import Network
from compas.datastructures import VolMesh

from compas.robots import RobotModel

from .artist import GHArtist
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
from .brepartist import BrepArtist


ShapeArtist.default_color = (255, 255, 255)

# MeshArtist.default_color = (0, 0, 0)
# MeshArtist.default_vertexcolor = (255, 255, 255)
# MeshArtist.default_edgecolor = (0, 0, 0)
# MeshArtist.default_facecolor = (255, 255, 255)

NetworkArtist.default_nodecolor = (255, 255, 255)
NetworkArtist.default_edgecolor = (0, 0, 0)

VolMeshArtist.default_color = (0, 0, 0)
VolMeshArtist.default_vertexcolor = (255, 255, 255)
VolMeshArtist.default_edgecolor = (0, 0, 0)
VolMeshArtist.default_facecolor = (255, 255, 255)
VolMeshArtist.default_cellcolor = (255, 0, 0)


@plugin(category="factories", requires=["Rhino"])
def register_artists():
    Artist.register(Box, BoxArtist, context="Grasshopper")
    Artist.register(Capsule, CapsuleArtist, context="Grasshopper")
    Artist.register(Circle, CircleArtist, context="Grasshopper")
    Artist.register(Cone, ConeArtist, context="Grasshopper")
    Artist.register(Curve, CurveArtist, context="Grasshopper")
    Artist.register(Cylinder, CylinderArtist, context="Grasshopper")
    Artist.register(Frame, FrameArtist, context="Grasshopper")
    Artist.register(Line, LineArtist, context="Grasshopper")
    Artist.register(Mesh, MeshArtist, context="Grasshopper")
    Artist.register(Network, NetworkArtist, context="Grasshopper")
    Artist.register(Point, PointArtist, context="Grasshopper")
    Artist.register(Polygon, PolygonArtist, context="Grasshopper")
    Artist.register(Polyhedron, PolyhedronArtist, context="Grasshopper")
    Artist.register(Polyline, PolylineArtist, context="Grasshopper")
    Artist.register(RobotModel, RobotModelArtist, context="Grasshopper")
    Artist.register(Sphere, SphereArtist, context="Grasshopper")
    Artist.register(Surface, SurfaceArtist, context="Grasshopper")
    Artist.register(Torus, TorusArtist, context="Grasshopper")
    Artist.register(Vector, VectorArtist, context="Grasshopper")
    Artist.register(VolMesh, VolMeshArtist, context="Grasshopper")
    Artist.register(Brep, BrepArtist, context="Grasshopper")
    print("GH Artists registered.")


__all__ = [
    "GHArtist",
    "ShapeArtist",
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
