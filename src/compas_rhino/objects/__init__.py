"""
********************************************************************************
objects
********************************************************************************

.. currentmodule:: compas_rhino.objects


Classes
=======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    BoxObject


.. autosummary::
    :toctree: generated/
    :nosignatures:

    NetworkObject
    MeshObject
    VolMeshObject

"""
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
from ._modify import (  # noqa : F401 F403
    network_update_attributes,
    network_update_node_attributes,
    network_update_edge_attributes,
    network_move_node,
    mesh_update_attributes,
    mesh_update_vertex_attributes,
    mesh_update_face_attributes,
    mesh_update_edge_attributes,
    mesh_move_vertex,
    mesh_move_vertices,
    mesh_move_face
)
from .inspectors import MeshVertexInspector  # noqa : F401 F403

from ._object import Object
from ._shapeobject import ShapeObject  # noqa: F401

from .boxobject import BoxObject

from .networkobject import NetworkObject
from .meshobject import MeshObject
from .volmeshobject import VolMeshObject

from compas.geometry import Box

from compas.datastructures import Network
from compas.datastructures import Mesh
from compas.datastructures import VolMesh

Object.register(Box, BoxObject)

Object.register(Network, NetworkObject)
Object.register(Mesh, MeshObject)
Object.register(VolMesh, VolMeshObject)

__all__ = [
    'Object',
    'BoxObject'
    'MeshObject',
    'NetworkObject',
    'VolMeshObject'
]
