
********************************************************************************
compas.datastructures
********************************************************************************

.. currentmodule:: compas.datastructures

.. rst-class:: lead

This package defines the core data structures of the COMPAS framework.
The data structures provide a structured way of storing and accessing data on individual components of both topological and geometrical objects.


Classes
=======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    Assembly
    AssemblyError
    CellNetwork
    Datastructure
    Feature
    FeatureError
    GeometricFeature
    Graph
    HalfEdge
    HalfFace
    Mesh
    Network
    ParametricFeature
    Part
    Tree
    TreeNode
    VolMesh


Functions
=========

.. autosummary::
    :toctree: generated/
    :nosignatures:

    mesh_add_vertex_to_face_edge
    mesh_adjacency_matrix
    mesh_connectivity_matrix
    mesh_conway_ambo
    mesh_conway_bevel
    mesh_conway_dual
    mesh_conway_expand
    mesh_conway_gyro
    mesh_conway_join
    mesh_conway_kis
    mesh_conway_meta
    mesh_conway_needle
    mesh_conway_ortho
    mesh_conway_snub
    mesh_conway_truncate
    mesh_conway_zip
    mesh_degree_matrix
    mesh_delete_duplicate_vertices
    mesh_disconnected_faces
    mesh_disconnected_vertices
    mesh_explode
    mesh_face_matrix
    mesh_flatness
    mesh_insert_vertex_on_edge
    mesh_laplacian_matrix
    mesh_offset
    mesh_planarize_faces
    mesh_quads_to_triangles
    mesh_smooth_centerofmass
    mesh_split_edge
    mesh_subdivide_catmullclark
    mesh_subdivide_corner
    mesh_subdivide_doosabin
    mesh_subdivide_frames
    mesh_subdivide_quad
    mesh_subdivide_tri
    mesh_substitute_vertex_in_faces
    mesh_thicken
    mesh_unweld_edges
    mesh_unweld_vertices
    mesh_weld
    meshes_join
    meshes_join_and_weld
    network_disconnected_edges
    network_disconnected_nodes
    network_embed_in_plane_proxy
    network_explode
    network_join_edges
    network_polylines
    trimesh_collapse_edge
    trimesh_cotangent_laplacian_matrix
    trimesh_descent
    trimesh_face_circle
    trimesh_gaussian_curvature
    trimesh_mean_curvature
    trimesh_remesh
    trimesh_smooth_laplacian_cotangent
    trimesh_split_edge
    trimesh_subdivide_loop
    trimesh_swap_edge
    trimesh_vertexarea_matrix


Functions using Numpy
=====================

In environments where numpy is not available, these functions can still be accessed through RPC.

.. autosummary::
    :toctree: generated/
    :nosignatures:

    mesh_contours_numpy
    mesh_geodesic_distances_numpy
    mesh_isolines_numpy
    mesh_oriented_bounding_box_numpy
    mesh_oriented_bounding_box_xy_numpy
    mesh_transform_numpy
    mesh_transformed_numpy
    trimesh_pull_points_numpy
    trimesh_samplepoints_numpy



