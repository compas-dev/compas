"""
This package defines sceneobjects for visualising COMPAS items (geometry & datastructures).
Every item type is paired with a corresponding scene object type that is capable of visualizing the data of the object.
The scene objects are implemented as pluggables, and automatically switch between plugins depending on the contexct in which they are used.
"""

from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from .exceptions import SceneObjectNotRegisteredError
from .sceneobject import SceneObject
from .meshobject import MeshObject
from .graphobject import GraphObject
from .geometryobject import GeometryObject
from .volmeshobject import VolMeshObject
from .group import Group

from .context import clear
from .context import before_draw
from .context import after_draw
from .context import register_scene_objects
from .context import get_sceneobject_cls
from .context import register

from .scene import Scene

from compas.plugins import plugin
from compas.geometry import Geometry
from compas.datastructures import Mesh
from compas.datastructures import Graph
from compas.datastructures import VolMesh


@plugin(category="factories", pluggable_name="register_scene_objects")
def register_scene_objects_base():
    register(Geometry, GeometryObject, context=None)
    register(Mesh, MeshObject, context=None)
    register(Graph, GraphObject, context=None)
    register(VolMesh, VolMeshObject, context=None)


__all__ = [
    "SceneObjectNotRegisteredError",
    "SceneObject",
    "MeshObject",
    "GraphObject",
    "GeometryObject",
    "VolMeshObject",
    "Scene",
    "clear",
    "before_draw",
    "after_draw",
    "register_scene_objects",
    "get_sceneobject_cls",
    "register",
    "Group",
]
