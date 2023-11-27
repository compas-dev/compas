"""
This package defines sceneobjects for visualising COMPAS items (geometry & datastructures).
Every item type is paired with a corresponding sceneobject type that is capable of visualizing the data of the object.
The sceneobjects are implemented as pluggables, and automatically switch between plugins depending on the contexct in which they are used.
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

from .sceneobject import clear
from .sceneobject import redraw
from .sceneobject import register_sceneobjects

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
    "register_sceneobjects",
]
