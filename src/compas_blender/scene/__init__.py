"""
This package provides sceneobject plugins for visualising COMPAS objects in Blender.
When working in Blender, :class:`compas.scene.SceneObject` will automatically use the corresponding Blender object for each COMPAS object type.
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

from .sceneobject import BlenderSceneObject
from .boxobject import BoxObject
from .capsuleobject import CapsuleObject
from .circleobject import CircleObject
from .coneobject import ConeObject
from .curveobject import CurveObject
from .cylinderobject import CylinderObject
from .frameobject import FrameObject
from .lineobject import LineObject
from .meshobject import MeshObject
from .networkobject import NetworkObject
from .pointobject import PointObject
from .pointcloudobject import PointcloudObject
from .polygonobject import PolygonObject
from .polyhedronobject import PolyhedronObject
from .polylineobject import PolylineObject
from .sphereobject import SphereObject
from .surfaceobject import SurfaceObject
from .torusobject import TorusObject
from .vectorobject import VectorObject
from .volmeshobject import VolMeshObject


@plugin(category="drawing-utils", pluggable_name="clear", requires=["bpy"])
def clear_blender():
    compas_blender.clear()


@plugin(category="drawing-utils", pluggable_name="redraw", requires=["bpy"])
def redraw_blender():
    compas_blender.redraw()


@plugin(category="factories", requires=["bpy"])
def register_sceneobjects():
    SceneObject.register(Box, BoxObject, context="Blender")
    SceneObject.register(Capsule, CapsuleObject, context="Blender")
    SceneObject.register(Circle, CircleObject, context="Blender")
    SceneObject.register(Cone, ConeObject, context="Blender")
    SceneObject.register(Curve, CurveObject, context="Blender")
    SceneObject.register(Cylinder, CylinderObject, context="Blender")
    SceneObject.register(Frame, FrameObject, context="Blender")
    SceneObject.register(Line, LineObject, context="Blender")
    SceneObject.register(Mesh, MeshObject, context="Blender")
    SceneObject.register(Network, NetworkObject, context="Blender")
    SceneObject.register(Point, PointObject, context="Blender")
    SceneObject.register(Pointcloud, PointcloudObject, context="Blender")
    SceneObject.register(Polygon, PolygonObject, context="Blender")
    SceneObject.register(Polyhedron, PolyhedronObject, context="Blender")
    SceneObject.register(Polyline, PolylineObject, context="Blender")
    SceneObject.register(Sphere, SphereObject, context="Blender")
    SceneObject.register(Surface, SurfaceObject, context="Blender")
    SceneObject.register(Torus, TorusObject, context="Blender")
    SceneObject.register(Vector, VectorObject, context="Blender")
    SceneObject.register(VolMesh, VolMeshObject, context="Blender")
    print("Blender Objects registered.")


__all__ = [
    "BlenderObject",
    "BoxObject",
    "CapsuleObject",
    "CircleObject",
    "ConeObject",
    "CurveObject",
    "CylinderObject",
    "FrameObject",
    "LineObject",
    "MeshObject",
    "NetworkObject",
    "PointObject",
    "PointcloudObject",
    "PolygonObject",
    "PolyhedronObject",
    "PolylineObject",
    "SphereObject",
    "SurfaceObject",
    "TorusObject",
    "VectorObject",
    "VolMeshObject",
]
