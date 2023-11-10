from __future__ import absolute_import

from compas.plugins import plugin
from compas.scene import SceneObject

from compas.geometry import Circle
from compas.geometry import Ellipse
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

from compas.geometry import Curve
from compas.geometry import Surface
from compas.brep import Brep

from compas.datastructures import Mesh
from compas.datastructures import Network
from compas.datastructures import VolMesh

import compas_rhino

from .artist import RhinoArtist
from .circleartist import CircleArtist
from .ellipseartist import EllipseArtist
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

from .curveartist import CurveArtist
from .surfaceartist import SurfaceArtist
from .brepartist import BrepArtist


@plugin(category="drawing-utils", pluggable_name="clear", requires=["Rhino"])
def clear_rhino():
    compas_rhino.clear()


@plugin(category="drawing-utils", pluggable_name="redraw", requires=["Rhino"])
def redraw_rhino():
    compas_rhino.redraw()


@plugin(category="factories", requires=["Rhino"])
def register_artists():
    SceneObject.register(Circle, CircleArtist, context="Rhino")
    SceneObject.register(Ellipse, EllipseArtist, context="Rhino")
    SceneObject.register(Frame, FrameArtist, context="Rhino")
    SceneObject.register(Line, LineArtist, context="Rhino")
    SceneObject.register(Plane, PlaneArtist, context="Rhino")
    SceneObject.register(Point, PointArtist, context="Rhino")
    SceneObject.register(Polygon, PolygonArtist, context="Rhino")
    SceneObject.register(Polyline, PolylineArtist, context="Rhino")
    SceneObject.register(Vector, VectorArtist, context="Rhino")
    SceneObject.register(Box, BoxArtist, context="Rhino")
    SceneObject.register(Capsule, CapsuleArtist, context="Rhino")
    SceneObject.register(Cone, ConeArtist, context="Rhino")
    SceneObject.register(Cylinder, CylinderArtist, context="Rhino")
    SceneObject.register(Polyhedron, PolyhedronArtist, context="Rhino")
    SceneObject.register(Sphere, SphereArtist, context="Rhino")
    SceneObject.register(Torus, TorusArtist, context="Rhino")
    SceneObject.register(Mesh, MeshArtist, context="Rhino")
    SceneObject.register(Network, NetworkArtist, context="Rhino")
    SceneObject.register(VolMesh, VolMeshArtist, context="Rhino")
    SceneObject.register(Curve, CurveArtist, context="Rhino")
    SceneObject.register(Surface, SurfaceArtist, context="Rhino")
    SceneObject.register(Brep, BrepArtist, context="Rhino")
    print("Rhino Artists registered.")


__all__ = [
    "RhinoArtist",
    "CircleArtist",
    "EllipseArtist",
    "FrameArtist",
    "LineArtist",
    "PlaneArtist",
    "PointArtist",
    "PolygonArtist",
    "PolylineArtist",
    "VectorArtist",
    "BoxArtist",
    "CapsuleArtist",
    "ConeArtist",
    "CylinderArtist",
    "PolyhedronArtist",
    "SphereArtist",
    "TorusArtist",
    "MeshArtist",
    "NetworkArtist",
    "VolMeshArtist",
    "CurveArtist",
    "SurfaceArtist",
    "BrepArtist",
]
