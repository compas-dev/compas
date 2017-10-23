"""
.. _compas_rhino.helpers:

********************************************************************************
helpers
********************************************************************************

.. module:: compas_rhino.helpers


Helpers make it easier to work with datastructures in Rhino.


mesh
====

.. autosummary::
    :toctree: generated/

    mesh_from_guid
    mesh_from_surface
    mesh_from_surface_uv
    mesh_from_surface_heightfield
    mesh_draw
    mesh_draw_vertices
    mesh_draw_edges
    mesh_draw_faces
    mesh_draw_vertex_labels
    mesh_draw_edge_labels
    mesh_draw_face_labels
    mesh_select_vertices
    mesh_select_vertex
    mesh_select_edges
    mesh_select_edge
    mesh_select_faces
    mesh_select_face
    mesh_update_vertex_attributes
    mesh_update_edge_attributes
    mesh_update_face_attributes
    mesh_move_vertex


network
=======

.. autosummary::
    :toctree: generated/

    network_draw
    network_draw_vertices
    network_draw_edges
    network_draw_vertex_labels
    network_draw_edge_labels
    network_select_vertices
    network_select_vertex
    network_select_edges
    network_select_edge
    network_update_attributes
    network_update_vertex_attributes
    network_update_edge_attributes
    network_move
    network_move_vertex


volmesh
=======

.. autosummary::
    :toctree: generated/

    volmesh_from_polysurfaces
    volmesh_from_wireframe
    volmesh_draw
    volmesh_draw_vertices
    volmesh_draw_edges
    volmesh_draw_faces
    volmesh_draw_cells
    volmesh_select_vertex
    volmesh_select_vertices
    volmesh_select_edge
    volmesh_select_edges
    volmesh_select_face
    volmesh_select_faces

"""

from .mesh import *
from .network import *
from .volmesh import *

from .mesh import __all__ as a
from .network import __all__ as b
from .volmesh import __all__ as c

__all__ = a + b + c
