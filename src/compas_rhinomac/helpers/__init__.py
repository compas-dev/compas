"""
.. _compas_rhinomac.helpers:

********************************************************************************
helpers
********************************************************************************

.. module:: compas_rhinomac.helpers


Helpers make it easier to work with datastructures in Rhino.


mesh
====

.. autosummary::
    :toctree: generated/

    mesh_from_guid
    mesh_from_surface
    mesh_from_surface_uv
    mesh_from_surface_heightfield
    draw_mesh
    draw_mesh_as_faces
    select_mesh_vertices
    select_mesh_vertex
    select_mesh_edges
    select_mesh_edge
    select_mesh_faces
    select_mesh_face
    update_mesh_vertex_attributes
    update_mesh_edge_attributes
    update_mesh_face_attributes
    display_mesh_vertex_labels
    display_mesh_edge_labels
    display_mesh_face_labels
    move_mesh_vertex


network
=======

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
    update_network_from_points
    update_network_edge_attributes
    update_network_from_lines
    update_network_face_attributes
    display_network_vertex_labels
    display_network_edge_labels
    display_network_face_labels
    move_network
    move_network_vertex
    display_network_axial_forces
    display_network_reaction_forces
    display_network_residual_forces
    display_network_selfweight
    display_network_applied_loads


volmesh
=======

.. autosummary::
    :toctree: generated/

    volmesh_from_polysurfaces
    volmesh_from_wireframe
    draw_volmesh

"""

# from .mesh import *
# from .network import *
# from .volmesh import *

# from .mesh import __all__ as a
# from .network import __all__ as b
# from .volmesh import __all__ as c

from .artists import *
from .artists import __all__ as a

__all__ = a
