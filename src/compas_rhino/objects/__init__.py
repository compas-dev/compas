"""
********************************************************************************
objects
********************************************************************************

.. currentmodule:: compas_rhino.objects

.. rst-class:: lead

Objects provide a high-level way to interact with both COMPAS and Rhino objects in Rhino.

.. code-block:: python

    import compas
    from compas.datastructures import Mesh
    from compas_rhino.objects import MeshObject

    mesh = Mesh.from_off(compas.get('tubemesh.off'))
    meshobject = MeshObject(None, mesh, 'MeshObject', 'COMPAS::MeshObject', True)
    meshobject.draw()
    meshobject.redraw()

    vertices = meshobject.select_vertices()

    if meshobject.modify_vertices(vertices):
        meshobject.draw()
        meshobject.redraw()

----

BaseObject
==========

.. autoclass:: BaseObject
    :members: clear, draw, select, modify, move

----

NetworkObject
=============

.. autoclass:: NetworkObject
    :members: clear, draw, select_nodes, select_edges, modify_nodes, modify_edges
    :no-show-inheritance:

----

MeshObject
==========

.. autoclass:: MeshObject
    :members: clear, draw, select_vertices, select_faces, select_edges, modify_vertices, modify_faces, modify_edges
    :no-show-inheritance:

----

VolMeshObject
=============

.. autoclass:: VolMeshObject
    :members: clear, draw, select_vertices, select_faces, select_edges, modify_vertices, modify_faces, modify_edges
    :no-show-inheritance:

----

Selecting
=========

.. autosummary::
    :toctree: generated/
    :nosignatures:

    network_select_node
    network_select_nodes
    network_select_edge
    network_select_edges
    mesh_select_vertex
    mesh_select_vertices
    mesh_select_face
    mesh_select_faces
    mesh_select_edge
    mesh_select_edges


Modifying
=========

.. autosummary::
    :toctree: generated/
    :nosignatures:

    network_update_attributes
    network_update_node_attributes
    network_update_edge_attributes
    network_move_node
    mesh_update_attributes
    mesh_update_vertex_attributes
    mesh_update_face_attributes
    mesh_update_edge_attributes
    mesh_move_vertex
    mesh_move_vertices
    mesh_move_face


Inspecting
==========

.. autosummary::
    :toctree: generated/
    :nosignatures:


"""
from __future__ import absolute_import

from .select import *  # noqa : F401 F403
from .modify import *  # noqa : F401 F403
from .inspect import *  # noqa : F401 F403

from ._object import BaseObject
from .meshobject import MeshObject
from .networkobject import NetworkObject
from .volmeshobject import VolMeshObject

from compas.datastructures import Mesh
from compas.datastructures import Network
from compas.datastructures import VolMesh

BaseObject.register(Mesh, MeshObject)
BaseObject.register(Network, NetworkObject)
BaseObject.register(VolMesh, VolMeshObject)

__all__ = [name for name in dir() if not name.startswith('_')]
