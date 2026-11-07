"""Visualize COMPAS geometry and data structures through scene objects.

Each supported item type is paired with one stable semantic scene-object type.
Visualization contexts register operations rather than replacement classes.

"""

from ._scenenode import SceneNode
from .exceptions import SceneItemNotBoundError
from .exceptions import SceneObjectNotRegisteredError
from .exceptions import SceneStateError
from .exceptions import SceneOperationNotRegisteredError
from .sceneobject import SceneObject
from .sceneobject import SceneStateField
from .meshobject import MeshObject
from .graphobject import GraphObject
from .geometryobject import GeometryObject
from .volmeshobject import VolMeshObject
from .group import Group

from .context import register_scene_objects
from .context import register_scene_operations
from .context import get_sceneobject_cls
from .context import get_scene_operation
from .context import register_sceneobject_type
from .context import register_scene_operation

from .scene import Scene

from compas.plugins import plugin
from compas.geometry import Geometry
from compas.datastructures import Mesh
from compas.datastructures import Graph
from compas.datastructures import VolMesh


@plugin(category="factories", pluggable_name="register_scene_objects")
def register_scene_objects_base() -> None:
    """Register stable core scene-object types."""
    register_sceneobject_type(Geometry, GeometryObject)
    register_sceneobject_type(Mesh, MeshObject)
    register_sceneobject_type(Graph, GraphObject)
    register_sceneobject_type(VolMesh, VolMeshObject)


__all__ = [
    "SceneObjectNotRegisteredError",
    "SceneItemNotBoundError",
    "SceneStateError",
    "SceneOperationNotRegisteredError",
    "SceneNode",
    "SceneObject",
    "SceneStateField",
    "MeshObject",
    "GraphObject",
    "GeometryObject",
    "VolMeshObject",
    "Group",
    "register_scene_objects",
    "register_scene_operations",
    "get_sceneobject_cls",
    "get_scene_operation",
    "register_sceneobject_type",
    "register_scene_operation",
    "Scene",
]
