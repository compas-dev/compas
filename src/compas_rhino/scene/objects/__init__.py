from __future__ import absolute_import

from ._select import (  # noqa : F401 F403
    mesh_select_vertex,
    mesh_select_vertices,
    mesh_select_face,
    mesh_select_faces,
    mesh_select_edge,
    mesh_select_edges,
    network_select_node,
    network_select_nodes,
    network_select_edge,
    network_select_edges
)
from .inspectors import MeshVertexInspector  # noqa : F401 F403

from ._object import Object
from ._shapeobject import ShapeObject  # noqa: F401

from .boxobject import BoxObject
from .capsuleobject import CapsuleObject
from .coneobject import ConeObject
from .cylinderobject import CylinderObject
from .polyhedronobject import PolyhedronObject
from .sphereobject import SphereObject
from .torusobject import TorusObject

from .networkobject import NetworkObject
from .meshobject import MeshObject
from .volmeshobject import VolMeshObject

from compas.geometry import Box
from compas.geometry import Capsule
from compas.geometry import Cone
from compas.geometry import Cylinder
from compas.geometry import Polyhedron
from compas.geometry import Sphere
from compas.geometry import Torus

from compas.datastructures import Network
from compas.datastructures import Mesh
from compas.datastructures import VolMesh

Object.register(Box, BoxObject)
Object.register(Capsule, CapsuleObject)
Object.register(Cone, ConeObject)
Object.register(Cylinder, CylinderObject)
Object.register(Polyhedron, PolyhedronObject)
Object.register(Sphere, SphereObject)
Object.register(Torus, TorusObject)

Object.register(Network, NetworkObject)
Object.register(Mesh, MeshObject)
Object.register(VolMesh, VolMeshObject)
