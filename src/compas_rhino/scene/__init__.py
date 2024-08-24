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
from .circleobject import RhinoCircleObject
from .ellipseobject import RhinoEllipseObject
from .frameobject import RhinoFrameObject
from .lineobject import RhinoLineObject
from .planeobject import RhinoPlaneObject
from .pointobject import RhinoPointObject
from .polygonobject import RhinoPolygonObject
from .polylineobject import RhinoPolylineObject
from .vectorobject import RhinoVectorObject
from .boxobject import RhinoBoxObject
from .brepobject import RhinoBrepObject
from .capsuleobject import RhinoCapsuleObject
from .coneobject import RhinoConeObject
from .cylinderobject import RhinoCylinderObject
from .polyhedronobject import RhinoPolyhedronObject
from .sphereobject import RhinoSphereObject
from .torusobject import RhinoTorusObject
from .meshobject import RhinoMeshObject
from .graphobject import RhinoGraphObject
from .volmeshobject import RhinoVolMeshObject
from .curveobject import RhinoCurveObject
from .surfaceobject import RhinoSurfaceObject


@plugin(category="drawing-utils", pluggable_name="clear", requires=["Rhino"])
def clear_rhino(guids=None):
    compas_rhino.clear(guids=guids)


@plugin(category="drawing-utils", pluggable_name="after_draw", requires=["Rhino"])
def after_draw_rhino(drawn_objects):
    compas_rhino.redraw()


@plugin(category="factories", requires=["Rhino"])
def register_scene_objects():
    register(Circle, RhinoCircleObject, context="Rhino")
    register(Ellipse, RhinoEllipseObject, context="Rhino")
    register(Frame, RhinoFrameObject, context="Rhino")
    register(Line, RhinoLineObject, context="Rhino")
    register(Plane, RhinoPlaneObject, context="Rhino")
    register(Point, RhinoPointObject, context="Rhino")
    register(Polygon, RhinoPolygonObject, context="Rhino")
    register(Polyline, RhinoPolylineObject, context="Rhino")
    register(Vector, RhinoVectorObject, context="Rhino")
    register(Box, RhinoBoxObject, context="Rhino")
    register(Capsule, RhinoCapsuleObject, context="Rhino")
    register(Cone, RhinoConeObject, context="Rhino")
    register(Cylinder, RhinoCylinderObject, context="Rhino")
    register(Polyhedron, RhinoPolyhedronObject, context="Rhino")
    register(Sphere, RhinoSphereObject, context="Rhino")
    register(Torus, RhinoTorusObject, context="Rhino")
    register(Mesh, RhinoMeshObject, context="Rhino")
    register(Graph, RhinoGraphObject, context="Rhino")
    register(VolMesh, RhinoVolMeshObject, context="Rhino")
    register(Curve, RhinoCurveObject, context="Rhino")
    register(Surface, RhinoSurfaceObject, context="Rhino")
    register(Brep, RhinoBrepObject, context="Rhino")

    # print("Rhino SceneObjects registered.")


__all__ = [
    "RhinoSceneObject",
    "RhinoCircleObject",
    "RhinoEllipseObject",
    "RhinoFrameObject",
    "RhinoLineObject",
    "RhinoPlaneObject",
    "RhinoPointObject",
    "RhinoPolygonObject",
    "RhinoPolylineObject",
    "RhinoVectorObject",
    "RhinoBoxObject",
    "RhinoCapsuleObject",
    "RhinoConeObject",
    "RhinoCylinderObject",
    "RhinoPolyhedronObject",
    "RhinoSphereObject",
    "RhinoTorusObject",
    "RhinoMeshObject",
    "RhinoGraphObject",
    "RhinoVolMeshObject",
    "RhinoCurveObject",
    "RhinoSurfaceObject",
    "RhinoBrepObject",
]
