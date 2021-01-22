"""
********************************************************************************
objects
********************************************************************************

.. currentmodule:: compas_rhino.objects

.. .. rst-class:: lead

.. code-block:: python

    import compas
    from compas.datastructures import Mesh
    from compas_rhino.objects import MeshObject

    mesh = Mesh.from_off(compas.get('tubemesh.off'))

    meshobject = MeshObject(mesh, name='MeshObject', layer='COMPAS::MeshObject')
    meshobject.draw()

    vertices = meshobject.select_vertices()

    if vertices and meshobject.modify_vertices(vertices):
        meshobject.draw()


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
