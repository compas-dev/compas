"""
This package provides scene object plugins for visualising COMPAS objects in Rhino.
When working in Rhino, :class:`compas.scene.SceneObject` will automatically use the corresponding Rhino scene object for each COMPAS object type.
"""
from __future__ import absolute_import

from compas.plugins import plugin
from compas.scene import register

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
from compas.datastructures import Graph
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
from .graphobject import GraphObject
from .volmeshobject import VolMeshObject

from .curveobject import CurveObject
from .surfaceobject import SurfaceObject
from .brepobject import BrepObject


@plugin(category="drawing-utils", pluggable_name="clear", requires=["Rhino"])
def clear_rhino(guids=None):
    compas_rhino.clear(guids=guids)


@plugin(category="drawing-utils", pluggable_name="after_draw", requires=["Rhino"])
def after_draw_rhino(drawn_objects):
    compas_rhino.redraw()


@plugin(category="factories", requires=["Rhino"])
def register_scene_objects():
    register(Circle, CircleObject, context="Rhino")
    register(Ellipse, EllipseObject, context="Rhino")
    register(Frame, FrameObject, context="Rhino")
    register(Line, LineObject, context="Rhino")
    register(Plane, PlaneObject, context="Rhino")
    register(Point, PointObject, context="Rhino")
    register(Polygon, PolygonObject, context="Rhino")
    register(Polyline, PolylineObject, context="Rhino")
    register(Vector, VectorObject, context="Rhino")
    register(Box, BoxObject, context="Rhino")
    register(Capsule, CapsuleObject, context="Rhino")
    register(Cone, ConeObject, context="Rhino")
    register(Cylinder, CylinderObject, context="Rhino")
    register(Polyhedron, PolyhedronObject, context="Rhino")
    register(Sphere, SphereObject, context="Rhino")
    register(Torus, TorusObject, context="Rhino")
    register(Mesh, MeshObject, context="Rhino")
    register(Graph, GraphObject, context="Rhino")
    register(VolMesh, VolMeshObject, context="Rhino")
    register(Curve, CurveObject, context="Rhino")
    register(Surface, SurfaceObject, context="Rhino")
    register(Brep, BrepObject, context="Rhino")
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
    "GraphObject",
    "VolMeshObject",
    "CurveObject",
    "SurfaceObject",
    "BrepObject",
]
