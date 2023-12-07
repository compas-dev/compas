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
from .networkobject import NetworkObject
from .geometryobject import GeometryObject
from .volmeshobject import VolMeshObject

from .context import clear
from .context import redraw
from .context import register_scene_objects
from .context import register

from .scene import Scene

__all__ = [
    "SceneObjectNotRegisteredError",
    "NoSceneObjectContextError",
    "SceneObject",
    "MeshObject",
    "NetworkObject",
    "GeometryObject",
    "VolMeshObject",
    "Scene",
    "clear",
    "redraw",
    "register_scene_objects",
    "register",
]
