from __future__ import absolute_import

from compas.plugins import plugin
from compas.scene import SceneObject

from compas.geometry import Box
from compas.geometry import Capsule
from compas.geometry import Circle
from compas.geometry import Cone
from compas.geometry import Curve
from compas.geometry import Cylinder
from compas.geometry import Ellipse
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
from compas.brep import Brep

from compas.datastructures import Mesh
from compas.datastructures import Network
from compas.datastructures import VolMesh

from .artist import GHArtist
from .boxartist import BoxArtist
from .capsuleartist import CapsuleArtist
from .circleartist import CircleArtist
from .coneartist import ConeArtist
from .curveartist import CurveArtist
from .cylinderartist import CylinderArtist
from .ellipseartist import EllipseArtist
from .frameartist import FrameArtist
from .lineartist import LineArtist
from .meshartist import MeshArtist
from .networkartist import NetworkArtist
from .pointartist import PointArtist
from .polygonartist import PolygonArtist
from .polyhedronartist import PolyhedronArtist
from .polylineartist import PolylineArtist
from .sphereartist import SphereArtist
from .surfaceartist import SurfaceArtist
from .torusartist import TorusArtist
from .vectorartist import VectorArtist
from .volmeshartist import VolMeshArtist
from .brepartist import BrepArtist


@plugin(category="factories", requires=["Rhino"])
def register_artists():
    SceneObject.register(Box, BoxArtist, context="Grasshopper")
    SceneObject.register(Capsule, CapsuleArtist, context="Grasshopper")
    SceneObject.register(Circle, CircleArtist, context="Grasshopper")
    SceneObject.register(Cone, ConeArtist, context="Grasshopper")
    SceneObject.register(Curve, CurveArtist, context="Grasshopper")
    SceneObject.register(Cylinder, CylinderArtist, context="Grasshopper")
    SceneObject.register(Ellipse, EllipseArtist, context="Grasshopper")
    SceneObject.register(Frame, FrameArtist, context="Grasshopper")
    SceneObject.register(Line, LineArtist, context="Grasshopper")
    SceneObject.register(Mesh, MeshArtist, context="Grasshopper")
    SceneObject.register(Network, NetworkArtist, context="Grasshopper")
    SceneObject.register(Point, PointArtist, context="Grasshopper")
    SceneObject.register(Polygon, PolygonArtist, context="Grasshopper")
    SceneObject.register(Polyhedron, PolyhedronArtist, context="Grasshopper")
    SceneObject.register(Polyline, PolylineArtist, context="Grasshopper")
    SceneObject.register(Sphere, SphereArtist, context="Grasshopper")
    SceneObject.register(Surface, SurfaceArtist, context="Grasshopper")
    SceneObject.register(Torus, TorusArtist, context="Grasshopper")
    SceneObject.register(Vector, VectorArtist, context="Grasshopper")
    SceneObject.register(VolMesh, VolMeshArtist, context="Grasshopper")
    SceneObject.register(Brep, BrepArtist, context="Grasshopper")
    print("GH Artists registered.")


__all__ = [
    "GHArtist",
    "BoxArtist",
    "CapsuleArtist",
    "CircleArtist",
    "ConeArtist",
    "CurveArtist",
    "CylinderArtist",
    "EllipseArtist",
    "FrameArtist",
    "LineArtist",
    "MeshArtist",
    "NetworkArtist",
    "PointArtist",
    "PolygonArtist",
    "PolyhedronArtist",
    "PolylineArtist",
    "SphereArtist",
    "SurfaceArtist",
    "TorusArtist",
    "VectorArtist",
    "VolMeshArtist",
]
