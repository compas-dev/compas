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

MeshObject
==========

.. autoclass:: MeshObject
    :members: clear, draw, select_vertices, select_faces, select_edges, modify_vertices, modify_faces, modify_edges

"""
from __future__ import absolute_import

from .base import BaseObject
from .meshobject import MeshObject

from compas.datastructures import Mesh


BaseObject.register(Mesh, MeshObject)


__all__ = [name for name in dir() if not name.startswith('_')]
