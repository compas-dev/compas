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
    BaseNetwork,               # NOTE: this class being in the stable API is something we should deprecate before 2.x release
    Graph,
    Network,
    network_complement,
    network_count_crossings,
    network_disconnected_edges,
    network_disconnected_nodes,
    network_embed_in_plane_proxy,
    network_embed_in_plane,
    network_explode,
    network_find_crossings,
    network_find_cycles,
    network_is_connected,
    network_is_crossed,
    network_is_planar_embedding,
    network_is_planar,
    network_is_xy,
    network_join_edges,
    network_polylines,
    network_shortest_path,
    network_smooth_centroid,
    network_split_edge,
    network_transform,
    network_transformed,
)
from .mesh import (
    BaseMesh,                  # NOTE: this class being in the stable API is something we should deprecate before 2.x release
    HalfEdge,
    Mesh,
    mesh_add_vertex_to_face_edge,
    mesh_bounding_box_xy,
    mesh_bounding_box,
    mesh_collapse_edge,
    mesh_connected_components,
    mesh_conway_ambo,
    mesh_conway_bevel,
    mesh_conway_dual,
    mesh_conway_expand,
    mesh_conway_gyro,
    mesh_conway_join,
    mesh_conway_kis,
    mesh_conway_meta,
    mesh_conway_needle,
    mesh_conway_ortho,
    mesh_conway_snub,
    mesh_conway_truncate,
    mesh_conway_zip,
    mesh_delete_duplicate_vertices,
    mesh_disconnected_faces,
    mesh_disconnected_vertices,
    mesh_dual,
    mesh_explode,
    mesh_face_adjacency,
    mesh_flatness,
    mesh_flip_cycles,
    mesh_insert_vertex_on_edge,
    mesh_is_connected,
    mesh_merge_faces,
    mesh_offset,
    mesh_planarize_faces,
    mesh_quads_to_triangles,
    mesh_slice_plane,
    mesh_smooth_area,
    mesh_smooth_centerofmass,
    mesh_smooth_centroid,
    mesh_split_edge,
    mesh_split_face,
    mesh_subdivide_catmullclark,
    mesh_subdivide_corner,
    mesh_subdivide_doosabin,
    mesh_subdivide_frames,
    mesh_subdivide_quad,
    mesh_subdivide_tri,
    mesh_subdivide,
    mesh_substitute_vertex_in_faces,
    mesh_thicken,
    mesh_transform,
    mesh_transformed,
    mesh_unify_cycles,
    mesh_unweld_edges,
    mesh_unweld_vertices,
    mesh_weld,
    meshes_join_and_weld,
    meshes_join,
    trimesh_collapse_edge,
    trimesh_face_circle,
    trimesh_gaussian_curvature,
    trimesh_mean_curvature,
    trimesh_remesh,
    trimesh_split_edge,
    trimesh_subdivide_loop,
    trimesh_swap_edge,
)
from .volmesh import (
    BaseVolMesh,               # NOTE: this class being in the stable API is something we should deprecate before 2.x release
    HalfFace,
    VolMesh,
    volmesh_bounding_box,
    volmesh_transform,
    volmesh_transformed
)

if not compas.IPY:
    from .network import (
        network_adjacency_matrix,
        network_connectivity_matrix,
        network_degree_matrix,
        network_laplacian_matrix,
    )
    from .mesh import (
        mesh_adjacency_matrix,
        mesh_connectivity_matrix,
        mesh_contours_numpy,
        mesh_degree_matrix,
        mesh_face_matrix,
        mesh_geodesic_distances_numpy,
        mesh_isolines_numpy,
        mesh_laplacian_matrix,
        mesh_oriented_bounding_box_numpy,
        mesh_oriented_bounding_box_xy_numpy,
        mesh_transform_numpy,
        mesh_transformed_numpy,
        trimesh_cotangent_laplacian_matrix,
        trimesh_descent,
        trimesh_pull_points_numpy,
        trimesh_samplepoints_numpy,
        trimesh_smooth_laplacian_cotangent,
        trimesh_vertexarea_matrix,
    )

__all__ = [
    'Datastructure',
    # Networks
    'BaseNetwork',
    'Graph',
    'Network',
    'network_complement',
    'network_count_crossings',
    'network_disconnected_edges',
    'network_disconnected_nodes',
    'network_embed_in_plane_proxy',
    'network_embed_in_plane',
    'network_explode',
    'network_find_crossings',
    'network_find_cycles',
    'network_is_connected',
    'network_is_crossed',
    'network_is_planar_embedding',
    'network_is_planar',
    'network_is_xy',
    'network_join_edges',
    'network_polylines',
    'network_shortest_path',
    'network_smooth_centroid',
    'network_split_edge',
    'network_transform',
    'network_transformed',
    # Meshes
    'BaseMesh',
    'HalfEdge',
    'Mesh',
    'mesh_add_vertex_to_face_edge',
    'mesh_bounding_box_xy',
    'mesh_bounding_box',
    'mesh_collapse_edge',
    'mesh_connected_components',
    'mesh_conway_ambo',
    'mesh_conway_bevel',
    'mesh_conway_dual',
    'mesh_conway_expand',
    'mesh_conway_gyro',
    'mesh_conway_join',
    'mesh_conway_kis',
    'mesh_conway_meta',
    'mesh_conway_needle',
    'mesh_conway_ortho',
    'mesh_conway_snub',
    'mesh_conway_truncate',
    'mesh_conway_zip',
    'mesh_delete_duplicate_vertices',
    'mesh_disconnected_faces',
    'mesh_disconnected_vertices',
    'mesh_dual',
    'mesh_explode',
    'mesh_face_adjacency',
    'mesh_flatness',
    'mesh_flip_cycles',
    'mesh_insert_vertex_on_edge',
    'mesh_is_connected',
    'mesh_merge_faces',
    'mesh_offset',
    'mesh_planarize_faces',
    'mesh_quads_to_triangles',
    'mesh_slice_plane',
    'mesh_smooth_area',
    'mesh_smooth_centerofmass',
    'mesh_smooth_centroid',
    'mesh_split_edge',
    'mesh_split_face',
    'mesh_subdivide_catmullclark',
    'mesh_subdivide_corner',
    'mesh_subdivide_doosabin',
    'mesh_subdivide_frames',
    'mesh_subdivide_quad',
    'mesh_subdivide_tri',
    'mesh_subdivide',
    'mesh_substitute_vertex_in_faces',
    'mesh_thicken',
    'mesh_transform',
    'mesh_transformed',
    'mesh_unify_cycles',
    'mesh_unweld_edges',
    'mesh_unweld_vertices',
    'mesh_weld',
    'meshes_join_and_weld',
    'meshes_join',
    'trimesh_collapse_edge',
    'trimesh_face_circle',
    'trimesh_gaussian_curvature',
    'trimesh_mean_curvature',
    'trimesh_remesh',
    'trimesh_split_edge',
    'trimesh_subdivide_loop',
    'trimesh_swap_edge',
    # Volumetric Meshes
    'BaseVolMesh',
    'HalfFace',
    'VolMesh',
    'volmesh_bounding_box',
    'volmesh_transform',
    'volmesh_transformed',
]

if not compas.IPY:
    __all__ += [
        # Networks
        'network_adjacency_matrix',
        'network_connectivity_matrix',
        'network_degree_matrix',
        'network_laplacian_matrix',
        # Meshes
        'mesh_adjacency_matrix',
        'mesh_connectivity_matrix',
        'mesh_contours_numpy',
        'mesh_degree_matrix',
        'mesh_face_matrix',
        'mesh_geodesic_distances_numpy',
        'mesh_isolines_numpy',
        'mesh_laplacian_matrix',
        'mesh_oriented_bounding_box_numpy',
        'mesh_oriented_bounding_box_xy_numpy',
        'mesh_transform_numpy',
        'mesh_transformed_numpy',
        'trimesh_cotangent_laplacian_matrix',
        'trimesh_descent',
        'trimesh_pull_points_numpy',
        'trimesh_samplepoints_numpy',
        'trimesh_smooth_laplacian_cotangent',
        'trimesh_vertexarea_matrix',
    ]
