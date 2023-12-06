"""
This package provides scene object plugins for visualising COMPAS objects in Grasshopper.
When working in GH Python components, :class:`compas.scene.SceneObject` will automatically use the corresponding GHPython scene object for each COMPAS object type.
"""
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
from compas.geometry import Brep

from compas.datastructures import Mesh
from compas.datastructures import Network
from compas.datastructures import VolMesh

from .sceneobject import GHSceneObject
from .boxobject import BoxObject
from .capsuleobject import CapsuleObject
from .circleobject import CircleObject
from .coneobject import ConeObject
from .curveobject import CurveObject
from .cylinderobject import CylinderObject
from .ellipseobject import EllipseObject
from .frameobject import FrameObject
from .lineobject import LineObject
from .meshobject import MeshObject
from .networkobject import NetworkObject
from .pointobject import PointObject
from .polygonobject import PolygonObject
from .polyhedronobject import PolyhedronObject
from .polylineobject import PolylineObject
from .sphereobject import SphereObject
from .surfaceobject import SurfaceObject
from .torusobject import TorusObject
from .vectorobject import VectorObject
from .volmeshobject import VolMeshObject
from .brepobject import BrepObject


@plugin(category="factories", requires=["Rhino"])
def register_scene_objects():
    SceneObject.register(Box, BoxObject, context="Grasshopper")
    SceneObject.register(Capsule, CapsuleObject, context="Grasshopper")
    SceneObject.register(Circle, CircleObject, context="Grasshopper")
    SceneObject.register(Cone, ConeObject, context="Grasshopper")
    SceneObject.register(Curve, CurveObject, context="Grasshopper")
    SceneObject.register(Cylinder, CylinderObject, context="Grasshopper")
    SceneObject.register(Ellipse, EllipseObject, context="Grasshopper")
    SceneObject.register(Frame, FrameObject, context="Grasshopper")
    SceneObject.register(Line, LineObject, context="Grasshopper")
    SceneObject.register(Mesh, MeshObject, context="Grasshopper")
    SceneObject.register(Network, NetworkObject, context="Grasshopper")
    SceneObject.register(Point, PointObject, context="Grasshopper")
    SceneObject.register(Polygon, PolygonObject, context="Grasshopper")
    SceneObject.register(Polyhedron, PolyhedronObject, context="Grasshopper")
    SceneObject.register(Polyline, PolylineObject, context="Grasshopper")
    SceneObject.register(Sphere, SphereObject, context="Grasshopper")
    SceneObject.register(Surface, SurfaceObject, context="Grasshopper")
    SceneObject.register(Torus, TorusObject, context="Grasshopper")
    SceneObject.register(Vector, VectorObject, context="Grasshopper")
    SceneObject.register(VolMesh, VolMeshObject, context="Grasshopper")
    SceneObject.register(Brep, BrepObject, context="Grasshopper")
    print("GH SceneObjects registered.")


__all__ = [
    "GHSceneObject",
    "BoxObject",
    "CapsuleObject",
    "CircleObject",
    "ConeObject",
    "CurveObject",
    "CylinderObject",
    "EllipseObject",
    "FrameObject",
    "LineObject",
    "MeshObject",
    "NetworkObject",
    "PointObject",
    "PolygonObject",
    "PolyhedronObject",
    "PolylineObject",
    "SphereObject",
    "SurfaceObject",
    "TorusObject",
    "VectorObject",
    "VolMeshObject",
]
