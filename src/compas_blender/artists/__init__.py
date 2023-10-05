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
    Artist.register(Pointcloud, PointcloudArtist, context="Blender")
    Artist.register(Polygon, PolygonArtist, context="Blender")
    Artist.register(Polyhedron, PolyhedronArtist, context="Blender")
    Artist.register(Polyline, PolylineArtist, context="Blender")
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
