"""
********************************************************************************
datastructures
********************************************************************************

.. currentmodule:: compas.datastructures

Meshes
======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    Mesh


Functions
---------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    mesh_contours_numpy
    mesh_conway_dual
    mesh_conway_join
    mesh_conway_ambo
    mesh_conway_kis
    mesh_conway_needle
    mesh_conway_zip
    mesh_conway_truncate
    mesh_conway_ortho
    mesh_conway_expand
    mesh_conway_gyro
    mesh_conway_snub
    mesh_conway_meta
    mesh_conway_bevel
    mesh_delete_duplicate_vertices
    mesh_explode
    mesh_flip_cycles
    mesh_geodesic_distances_numpy
    mesh_isolines_numpy
    mesh_offset
    mesh_oriented_bounding_box_numpy
    mesh_oriented_bounding_box_xy_numpy
    mesh_planarize_faces
    mesh_thicken
    mesh_transform_numpy
    mesh_transformed_numpy
    mesh_weld
    meshes_join
    meshes_join_and_weld
    trimesh_descent
    trimesh_face_circle
    trimesh_gaussian_curvature


Matrices
--------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    mesh_adjacency_matrix
    mesh_connectivity_matrix
    mesh_degree_matrix
    mesh_face_matrix
    mesh_laplacian_matrix


Networks
========

Classes
-------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    Network


Functions
---------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    network_complement
    network_count_crossings
    network_embed_in_plane
    network_find_crossings
    network_find_cycles
    network_is_connected
    network_is_crossed
    network_is_planar
    network_is_planar_embedding
    network_is_xy
    network_transform
    network_transformed


VolMesh
=======

Classes
-------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    VolMesh


Functions
---------

.. autosummary::
    :toctree: generated/
    :nosignatures:


"""

from __future__ import absolute_import


from .datastructure import *  # noqa: F401 E402 F403

from .network import *  # noqa: F401 E402 F403
from .mesh import *  # noqa: F401 E402 F403
from .volmesh import *  # noqa: F401 E402 F403


__all__ = [name for name in dir() if not name.startswith('_')]
