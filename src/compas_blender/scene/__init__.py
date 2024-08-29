"""
This package provides scene object plugins for visualising COMPAS objects in Blender.
When working in Blender, :class:`compas.scene.SceneObject` will automatically use the corresponding Blender object for each COMPAS object type.
"""

import compas_blender

from compas.plugins import plugin
from compas.scene import register

from compas.geometry import Box
from compas.geometry import Capsule
from compas.geometry import Circle
from compas.geometry import Cone
from compas.geometry import Curve
from compas.geometry import Cylinder
from compas.geometry import Frame
from compas.geometry import Line
from compas.geometry import Plane
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
from compas.datastructures import Graph
from compas.datastructures import VolMesh

from .sceneobject import BlenderSceneObject
from .shapeobject import ShapeObject
from .boxobject import BoxObject
from .circleobject import CircleObject
from .curveobject import CurveObject
from .frameobject import FrameObject
from .lineobject import LineObject
from .meshobject import MeshObject
from .graphobject import GraphObject
from .planeobject import PlaneObject
from .pointobject import PointObject
from .pointcloudobject import PointcloudObject
from .polygonobject import PolygonObject
from .polyhedronobject import PolyhedronObject
from .polylineobject import PolylineObject
from .surfaceobject import SurfaceObject
from .vectorobject import VectorObject
from .volmeshobject import VolMeshObject


@plugin(category="drawing-utils", pluggable_name="clear", requires=["bpy"])
def clear_blender(guids=None):
    compas_blender.clear(guids=guids)


@plugin(category="drawing-utils", pluggable_name="after_draw", requires=["bpy"])
def after_draw_blender(drawn_objects):
    compas_blender.redraw()  # not sure we should do this


@plugin(category="factories", requires=["bpy"])
def register_scene_objects():
    register(Box, BoxObject, context="Blender")
    register(Capsule, ShapeObject, context="Blender")
    register(Circle, CircleObject, context="Blender")
    register(Cone, ShapeObject, context="Blender")
    register(Curve, CurveObject, context="Blender")
    register(Cylinder, ShapeObject, context="Blender")
    register(Frame, FrameObject, context="Blender")
    register(Line, LineObject, context="Blender")
    register(Mesh, MeshObject, context="Blender")
    register(Graph, GraphObject, context="Blender")
    register(Plane, PlaneObject, context="Blender")
    register(Point, PointObject, context="Blender")
    register(Pointcloud, PointcloudObject, context="Blender")
    register(Polygon, PolygonObject, context="Blender")
    register(Polyhedron, PolyhedronObject, context="Blender")
    register(Polyline, PolylineObject, context="Blender")
    register(Sphere, ShapeObject, context="Blender")
    register(Surface, SurfaceObject, context="Blender")
    register(Torus, ShapeObject, context="Blender")
    register(Vector, VectorObject, context="Blender")
    register(VolMesh, VolMeshObject, context="Blender")

    # print("Blender Objects registered.")


__all__ = [
    "BlenderSceneObject",
    "ShapeObject",
    "BoxObject",
    "CircleObject",
    "CurveObject",
    "FrameObject",
    "LineObject",
    "MeshObject",
    "GraphObject",
    "PlaneObject",
    "PointObject",
    "PointcloudObject",
    "PolygonObject",
    "PolyhedronObject",
    "PolylineObject",
    "SurfaceObject",
    "VectorObject",
    "VolMeshObject",
]
