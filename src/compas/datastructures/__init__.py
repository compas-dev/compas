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
import compas

from .datastructure import Datastructure
from .network import (
    Graph,
    Network,
    network_join_edges,
    network_polylines,
    network_split_edge,
    network_is_connected,
    network_complement,
    network_find_cycles,
    network_disconnected_nodes,
    network_disconnected_edges,
    network_explode,
    network_is_crossed,
    network_count_crossings,
    network_find_crossings,
    network_is_xy,
    network_is_planar,
    network_is_planar_embedding,
    network_embed_in_plane,
    network_embed_in_plane_proxy,
    network_smooth_centroid,
    network_transform,
    network_transformed,
    network_shortest_path
)
from .mesh import (
    HalfEdge,
    Mesh,
    trimesh_collapse_edge,
    mesh_add_vertex_to_face_edge,
    mesh_insert_vertex_on_edge,
    mesh_merge_faces,
    trimesh_split_edge,
    mesh_substitute_vertex_in_faces,
    trimesh_swap_edge,
    mesh_unweld_vertices,
    mesh_unweld_edges,
    mesh_conway_dual,
    mesh_conway_join,
    mesh_conway_ambo,
    mesh_conway_kis,
    mesh_conway_needle,
    mesh_conway_zip,
    mesh_conway_truncate,
    mesh_conway_ortho,
    mesh_conway_expand,
    mesh_conway_gyro,
    mesh_conway_snub,
    mesh_conway_meta,
    mesh_conway_bevel,
    trimesh_mean_curvature,
    trimesh_gaussian_curvature,
    mesh_disconnected_vertices,
    mesh_disconnected_faces,
    mesh_explode,
    trimesh_face_circle,
    mesh_weld,
    meshes_join,
    meshes_join_and_weld,
    mesh_offset,
    mesh_thicken,
    mesh_flatness,
    mesh_planarize_faces,
    trimesh_remesh
)
from .volmesh import (
    VolMesh,
    volmesh_bounding_box,
    volmesh_transform,
    volmesh_transformed
)

if not compas.IPY:
    from .network import (
        network_adjacency_matrix,
        network_degree_matrix,
        network_connectivity_matrix,
        network_laplacian_matrix,
    )
    from .mesh import (
        mesh_adjacency_matrix,
        mesh_connectivity_matrix,
        mesh_degree_matrix,
        mesh_face_matrix,
        mesh_laplacian_matrix,
        trimesh_cotangent_laplacian_matrix,
        trimesh_vertexarea_matrix,
        mesh_oriented_bounding_box_numpy,
        mesh_oriented_bounding_box_xy_numpy,
        mesh_isolines_numpy,
        mesh_contours_numpy,
        trimesh_descent,
        mesh_geodesic_distances_numpy,
        trimesh_smooth_laplacian_cotangent,
        trimesh_pull_points_numpy,
        mesh_transform_numpy,
        mesh_transformed_numpy,
        trimesh_samplepoints_numpy,
    )

__all__ = [
    'Datastructure',
    # Networks
    'Graph',
    'Network',
    'network_join_edges',
    'network_polylines',
    'network_split_edge',
    'network_is_connected',
    'network_complement',
    'network_find_cycles',
    'network_disconnected_nodes',
    'network_disconnected_edges',
    'network_explode',
    'network_is_crossed',
    'network_count_crossings',
    'network_find_crossings',
    'network_is_xy',
    'network_is_planar',
    'network_is_planar_embedding',
    'network_embed_in_plane',
    'network_embed_in_plane_proxy',
    'network_smooth_centroid',
    'network_transform',
    'network_transformed',
    'network_shortest_path',
    # Meshes
    'HalfEdge',
    'Mesh',
    'trimesh_collapse_edge',
    'mesh_add_vertex_to_face_edge',
    'mesh_insert_vertex_on_edge',
    'mesh_merge_faces',
    'trimesh_split_edge',
    'mesh_substitute_vertex_in_faces',
    'trimesh_swap_edge',
    'mesh_unweld_vertices',
    'mesh_unweld_edges',
    'mesh_conway_dual',
    'mesh_conway_join',
    'mesh_conway_ambo',
    'mesh_conway_kis',
    'mesh_conway_needle',
    'mesh_conway_zip',
    'mesh_conway_truncate',
    'mesh_conway_ortho',
    'mesh_conway_expand',
    'mesh_conway_gyro',
    'mesh_conway_snub',
    'mesh_conway_meta',
    'mesh_conway_bevel',
    'trimesh_mean_curvature',
    'trimesh_gaussian_curvature',
    'mesh_disconnected_vertices',
    'mesh_disconnected_faces',
    'mesh_explode',
    'trimesh_face_circle',
    'mesh_weld',
    'meshes_join',
    'meshes_join_and_weld',
    'mesh_offset',
    'mesh_thicken',
    'mesh_flatness',
    'mesh_planarize_faces',
    'trimesh_remesh',
    # Volumetric Meshes
    'VolMesh',
    'volmesh_bounding_box',
    'volmesh_transform',
    'volmesh_transformed',
]

if not compas.IPY:
    __all__ += [
        # Networks
        'network_adjacency_matrix',
        'network_degree_matrix',
        'network_connectivity_matrix',
        'network_laplacian_matrix',
        # Meshes
        'mesh_adjacency_matrix',
        'mesh_connectivity_matrix',
        'mesh_degree_matrix',
        'mesh_face_matrix',
        'mesh_laplacian_matrix',
        'trimesh_cotangent_laplacian_matrix',
        'trimesh_vertexarea_matrix',
        'mesh_oriented_bounding_box_numpy',
        'mesh_oriented_bounding_box_xy_numpy',
        'mesh_isolines_numpy',
        'mesh_contours_numpy',
        'trimesh_descent',
        'mesh_geodesic_distances_numpy',
        'trimesh_smooth_laplacian_cotangent',
        'trimesh_pull_points_numpy',
        'mesh_transform_numpy',
        'mesh_transformed_numpy',
        'trimesh_samplepoints_numpy',
    ]
