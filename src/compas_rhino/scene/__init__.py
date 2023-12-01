"""
This package provides sceneobject plugins for visualising COMPAS objects in Rhino.
When working in Rhino, :class:`compas.scene.SceneObject` will automatically use the corresponding Rhino sceneobject for each COMPAS object type.
"""
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
from compas.geometry import Brep

from compas.datastructures import Mesh
from compas.datastructures import Network
from compas.datastructures import VolMesh

import compas_rhino

from .sceneobject import RhinoSceneObject
from .circleobject import CircleObject
from .ellipseobject import EllipseObject
from .frameobject import FrameObject
from .lineobject import LineObject
from .planeobject import PlaneObject
from .pointobject import PointObject
from .polygonobject import PolygonObject
from .polylineobject import PolylineObject
from .vectorobject import VectorObject

from .boxobject import BoxObject
from .capsuleobject import CapsuleObject
from .coneobject import ConeObject
from .cylinderobject import CylinderObject
from .polyhedronobject import PolyhedronObject
from .sphereobject import SphereObject
from .torusobject import TorusObject

from .meshobject import MeshObject
from .networkobject import NetworkObject
from .volmeshobject import VolMeshObject

from .curveobject import CurveObject
from .surfaceobject import SurfaceObject
from .brepobject import BrepObject


@plugin(category="drawing-utils", pluggable_name="clear", requires=["Rhino"])
def clear_rhino():
    compas_rhino.clear()


@plugin(category="drawing-utils", pluggable_name="redraw", requires=["Rhino"])
def redraw_rhino():
    compas_rhino.redraw()


@plugin(category="factories", requires=["Rhino"])
def register_scene_objects():
    SceneObject.register(Circle, CircleObject, context="Rhino")
    SceneObject.register(Ellipse, EllipseObject, context="Rhino")
    SceneObject.register(Frame, FrameObject, context="Rhino")
    SceneObject.register(Line, LineObject, context="Rhino")
    SceneObject.register(Plane, PlaneObject, context="Rhino")
    SceneObject.register(Point, PointObject, context="Rhino")
    SceneObject.register(Polygon, PolygonObject, context="Rhino")
    SceneObject.register(Polyline, PolylineObject, context="Rhino")
    SceneObject.register(Vector, VectorObject, context="Rhino")
    SceneObject.register(Box, BoxObject, context="Rhino")
    SceneObject.register(Capsule, CapsuleObject, context="Rhino")
    SceneObject.register(Cone, ConeObject, context="Rhino")
    SceneObject.register(Cylinder, CylinderObject, context="Rhino")
    SceneObject.register(Polyhedron, PolyhedronObject, context="Rhino")
    SceneObject.register(Sphere, SphereObject, context="Rhino")
    SceneObject.register(Torus, TorusObject, context="Rhino")
    SceneObject.register(Mesh, MeshObject, context="Rhino")
    SceneObject.register(Network, NetworkObject, context="Rhino")
    SceneObject.register(VolMesh, VolMeshObject, context="Rhino")
    SceneObject.register(Curve, CurveObject, context="Rhino")
    SceneObject.register(Surface, SurfaceObject, context="Rhino")
    SceneObject.register(Brep, BrepObject, context="Rhino")
    print("Rhino SceneObjects registered.")


__all__ = [
    "RhinoSceneObject",
    "CircleObject",
    "EllipseObject",
    "FrameObject",
    "LineObject",
    "PlaneObject",
    "PointObject",
    "PolygonObject",
    "PolylineObject",
    "VectorObject",
    "BoxObject",
    "CapsuleObject",
    "ConeObject",
    "CylinderObject",
    "PolyhedronObject",
    "SphereObject",
    "TorusObject",
    "MeshObject",
    "NetworkObject",
    "VolMeshObject",
    "CurveObject",
    "SurfaceObject",
    "BrepObject",
]
