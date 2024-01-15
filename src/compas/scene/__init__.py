"""
This package defines sceneobjects for visualising COMPAS items (geometry & datastructures).
Every item type is paired with a corresponding scene object type that is capable of visualizing the data of the object.
The scene objects are implemented as pluggables, and automatically switch between plugins depending on the contexct in which they are used.
"""

from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from .exceptions import SceneObjectNotRegisteredError
from .exceptions import NoSceneObjectContextError
from .sceneobject import SceneObject
from .meshobject import MeshObject
from .graphobject import GraphObject
from .geometryobject import GeometryObject
from .volmeshobject import VolMeshObject

from .context import clear
from .context import redraw
from .context import register_scene_objects
from .context import get_sceneobject_cls
from .context import register

from .scene import Scene
from .scene import SceneObjectNode
from .scene import SceneTree

__all__ = [
    "SceneObjectNotRegisteredError",
    "NoSceneObjectContextError",
    "SceneObject",
    "MeshObject",
    "GraphObject",
    "GeometryObject",
    "VolMeshObject",
    "Scene",
    "SceneObjectNode",
    "SceneTree",
    "clear",
    "redraw",
    "register_scene_objects",
    "get_sceneobject_cls",
    "register",
]
