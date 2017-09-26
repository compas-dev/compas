"""
.. _compas_compas_rhino.helpers:

********************************************************************************
helpers
********************************************************************************

.. module:: compas_compas_rhino.helpers


Helpers make it easier to work with datastructures in Rhino.


mesh
====

.. currentmodule:: compas_compas_rhino.helpers.mesh

:mod:`compas_compas_rhino.helpers.mesh`

.. autosummary::
    :toctree: generated/

    mesh_from_guid
    mesh_from_surface
    mesh_from_surface_uv
    mesh_from_surface_heightfield
    draw_mesh
    display_mesh_vertex_normals
    display_mesh_face_normals


network
=======

.. currentmodule:: compas_compas_rhino.helpers.network

:mod:`compas_compas_rhino.helpers.network`

.. autosummary::
    :toctree: generated/

    draw_network
    select_network_vertices
    select_network_vertex
    select_network_edges
    select_network_edge
    select_network_faces
    select_network_face
    update_network_attributes
    update_network_vertex_attributes
    update_network_edge_attributes
    update_network_face_attributes
    display_network_vertex_labels
    display_network_edge_labels
    display_network_face_labels
    move_network
    move_network_vertex


volmesh
=======

.. currentmodule:: compas_compas_rhino.helpers.volmesh

:mod:`compas_compas_rhino.helpers.volmesh`

.. autosummary::
    :toctree: generated/

    volmesh_from_polysurfaces
    volmesh_from_wireframe
    draw_volmesh

"""

from .mesh import *
from .network import *
from .volmesh import *

