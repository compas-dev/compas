"""
This package provides scene object plugins for visualising COMPAS objects in Grasshopper.
When working in GH Python components, :class:`compas.scene.SceneObject` will automatically use the corresponding GHPython scene object for each COMPAS object type.
"""

from __future__ import absolute_import

from compas.plugins import plugin
from compas.scene import register

from compas.geometry import Box
from compas.geometry import Capsule
from compas.geometry import Circle
from compas.geometry import Cone
from compas.geometry import Curve
from compas.geometry import Cylinder
from compas.geometry import Ellipse
from compas.geometry import Frame
from compas.geometry import Line
from compas.geometry import Plane
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
from compas.datastructures import Graph
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
from .graphobject import GraphObject
from .planeobject import PlaneObject
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


# @plugin(category="drawing-utils", pluggable_name="clear", requires=["Grasshopper"])
# def clear_GH(guids=None):
#     pass


@plugin(category="factories", requires=["Rhino"])
def register_scene_objects():
    register(Box, BoxObject, context="Grasshopper")
    register(Capsule, CapsuleObject, context="Grasshopper")
    register(Circle, CircleObject, context="Grasshopper")
    register(Cone, ConeObject, context="Grasshopper")
    register(Curve, CurveObject, context="Grasshopper")
    register(Cylinder, CylinderObject, context="Grasshopper")
    register(Ellipse, EllipseObject, context="Grasshopper")
    register(Frame, FrameObject, context="Grasshopper")
    register(Line, LineObject, context="Grasshopper")
    register(Mesh, MeshObject, context="Grasshopper")
    register(Graph, GraphObject, context="Grasshopper")
    register(Plane, PlaneObject, context="Grasshopper")
    register(Point, PointObject, context="Grasshopper")
    register(Polygon, PolygonObject, context="Grasshopper")
    register(Polyhedron, PolyhedronObject, context="Grasshopper")
    register(Polyline, PolylineObject, context="Grasshopper")
    register(Sphere, SphereObject, context="Grasshopper")
    register(Surface, SurfaceObject, context="Grasshopper")
    register(Torus, TorusObject, context="Grasshopper")
    register(Vector, VectorObject, context="Grasshopper")
    register(VolMesh, VolMeshObject, context="Grasshopper")
    register(Brep, BrepObject, context="Grasshopper")

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
    "GraphObject",
    "PlaneObject",
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
