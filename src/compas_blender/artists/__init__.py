"""
This package provides artist plugins for visualising COMPAS objects in Blender.
When working in Blender, :class:`compas.artists.Artist` will automatically use the corresponding Blender artist for each COMPAS object type.
"""

import compas_blender

from compas.plugins import plugin
from compas.scene import SceneObject

from compas.geometry import Box
from compas.geometry import Capsule
from compas.geometry import Circle
from compas.geometry import Cone
from compas.geometry import Curve
from compas.geometry import Cylinder
from compas.geometry import Frame
from compas.geometry import Line
from compas.geometry import Point
from compas.geometry import Pointcloud
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
from .pointcloudartist import PointcloudArtist
from .polygonartist import PolygonArtist
from .polyhedronartist import PolyhedronArtist
from .polylineartist import PolylineArtist
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
    SceneObject.register(Box, BoxArtist, context="Blender")
    SceneObject.register(Capsule, CapsuleArtist, context="Blender")
    SceneObject.register(Circle, CircleArtist, context="Blender")
    SceneObject.register(Cone, ConeArtist, context="Blender")
    SceneObject.register(Curve, CurveArtist, context="Blender")
    SceneObject.register(Cylinder, CylinderArtist, context="Blender")
    SceneObject.register(Frame, FrameArtist, context="Blender")
    SceneObject.register(Line, LineArtist, context="Blender")
    SceneObject.register(Mesh, MeshArtist, context="Blender")
    SceneObject.register(Network, NetworkArtist, context="Blender")
    SceneObject.register(Point, PointArtist, context="Blender")
    SceneObject.register(Pointcloud, PointcloudArtist, context="Blender")
    SceneObject.register(Polygon, PolygonArtist, context="Blender")
    SceneObject.register(Polyhedron, PolyhedronArtist, context="Blender")
    SceneObject.register(Polyline, PolylineArtist, context="Blender")
    SceneObject.register(Sphere, SphereArtist, context="Blender")
    SceneObject.register(Surface, SurfaceArtist, context="Blender")
    SceneObject.register(Torus, TorusArtist, context="Blender")
    SceneObject.register(Vector, VectorArtist, context="Blender")
    SceneObject.register(VolMesh, VolMeshArtist, context="Blender")
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
    "PointcloudArtist",
    "PolygonArtist",
    "PolyhedronArtist",
    "PolylineArtist",
    "SphereArtist",
    "SurfaceArtist",
    "TorusArtist",
    "VectorArtist",
    "VolMeshArtist",
]
