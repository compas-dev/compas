"""
This package defines the core data structures of the COMPAS framework.
The data structures provide a structured way of storing and accessing data on individual components of both topological and geometrical objects.
"""

from __future__ import absolute_import

import compas

from .datastructure import Datastructure

# =============================================================================
# Graphs
# =============================================================================

# =============================================================================
# Networks
# =============================================================================

from .network.operations.join import network_join_edges, network_polylines
from .network.operations.split import network_split_edge

from .network.combinatorics import network_is_connected
from .network.complementarity import network_complement
from .network.duality import network_find_cycles
from .network.explode import network_disconnected_edges, network_disconnected_nodes, network_explode
from .network.planarity import (
    network_count_crossings,
    network_embed_in_plane,
    network_embed_in_plane_proxy,
    network_find_crossings,
    network_is_crossed,
    network_is_planar,
    network_is_planar_embedding,
    network_is_xy,
)
from .network.smoothing import network_smooth_centroid
from .network.transformations import network_transform, network_transformed
from .network.traversal import network_shortest_path

if not compas.IPY:
    from .network.matrices import (
        network_adjacency_matrix,
        network_connectivity_matrix,
        network_degree_matrix,
        network_laplacian_matrix,
    )

# =============================================================================
# Halfedges
# =============================================================================

# =============================================================================
# Meshes
# =============================================================================

from .mesh.operations.collapse import mesh_collapse_edge, trimesh_collapse_edge
from .mesh.operations.insert import mesh_add_vertex_to_face_edge, mesh_insert_vertex_on_edge
from .mesh.operations.merge import mesh_merge_faces
from .mesh.operations.split import mesh_split_edge, mesh_split_face, mesh_split_strip, trimesh_split_edge
from .mesh.operations.substitute import mesh_substitute_vertex_in_faces
from .mesh.operations.swap import trimesh_swap_edge
from .mesh.operations.weld import mesh_unweld_edges, mesh_unweld_vertices

from .mesh.bbox import mesh_bounding_box, mesh_bounding_box_xy  # this needs to be moved to geometry
from .mesh.clean import mesh_delete_duplicate_vertices
from .mesh.combinatorics import mesh_connected_components, mesh_is_connected
from .mesh.conway import (
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
)
from .mesh.curvature import trimesh_gaussian_curvature, trimesh_mean_curvature  # this needs to be moved to geometry
from .mesh.duality import mesh_dual
from .mesh.explode import mesh_disconnected_faces, mesh_disconnected_vertices, mesh_explode
from .mesh.geometry import trimesh_face_circle  # this needs to be moved to geometry
from .mesh.join import mesh_weld, meshes_join, meshes_join_and_weld  # used by offset
from .mesh.orientation import mesh_face_adjacency, mesh_flip_cycles, mesh_unify_cycles  # used by offset
from .mesh.offset import mesh_offset, mesh_thicken
from .mesh.planarisation import mesh_flatness, mesh_planarize_faces  # this needs to be moved to geometry
from .mesh.remesh import trimesh_remesh
from .mesh.slice import mesh_slice_plane
from .mesh.smoothing import mesh_smooth_area, mesh_smooth_centerofmass, mesh_smooth_centroid
from .mesh.subdivision import (
    mesh_subdivide,
    mesh_subdivide_catmullclark,
    mesh_subdivide_corner,
    mesh_subdivide_doosabin,
    mesh_subdivide_frames,
    mesh_subdivide_quad,
    mesh_subdivide_tri,
    trimesh_subdivide_loop,
)
from .mesh.transformations import mesh_transform, mesh_transformed  # this needs to be moved to geometry
from .mesh.triangulation import mesh_quads_to_triangles

if not compas.IPY:
    from .mesh.matrices import (
        mesh_adjacency_matrix,
        mesh_connectivity_matrix,
        mesh_degree_matrix,
        mesh_face_matrix,
        mesh_laplacian_matrix,
        trimesh_cotangent_laplacian_matrix,
        trimesh_vertexarea_matrix,
    )

    from .mesh.bbox_numpy import (
        mesh_oriented_bounding_box_numpy,
        mesh_oriented_bounding_box_xy_numpy,
    )  # this needs to be moved to geometry
    from .mesh.contours_numpy import mesh_isolines_numpy, mesh_contours_numpy  # this needs to be moved to geometry
    from .mesh.descent_numpy import trimesh_descent  # this needs to be moved to geometry
    from .mesh.geodesics_numpy import mesh_geodesic_distances_numpy
    from .mesh.pull_numpy import trimesh_pull_points_numpy  # this needs to be moved to geometry
    from .mesh.smoothing_numpy import trimesh_smooth_laplacian_cotangent
    from .mesh.transformations_numpy import (
        mesh_transform_numpy,
        mesh_transformed_numpy,
    )  # this needs to be moved to geometry
    from .mesh.trimesh_samplepoints_numpy import trimesh_samplepoints_numpy

# =============================================================================
# Halffaces
# =============================================================================

# =============================================================================
# Volmeshes
# =============================================================================

from .volmesh.bbox import volmesh_bounding_box  # this needs to be moved to geometry
from .volmesh.transformations import volmesh_transform, volmesh_transformed  # this needs to be moved to geometry

# =============================================================================
# Volmeshes
# =============================================================================

# =============================================================================
# Class APIs
# =============================================================================

from .graph.graph import Graph
from .network.network import Network

from .halfedge.halfedge import HalfEdge
from .mesh.mesh import Mesh

from .halfface.halfface import HalfFace
from .volmesh.volmesh import VolMesh

from .assembly.exceptions import AssemblyError, FeatureError
from .assembly.assembly import Assembly
from .assembly.part import Feature, GeometricFeature, ParametricFeature, Part

from .cell_network.cell_network import CellNetwork

from .tree.tree import Tree, TreeNode

BaseNetwork = Network
BaseMesh = Mesh
BaseVolMesh = VolMesh

__all__ = [
    "Datastructure",
    # Graphs
    "Graph",
    # Networks
    "BaseNetwork",
    "CellNetwork",
    "Network",
    "network_complement",
    "network_count_crossings",
    "network_disconnected_edges",
    "network_disconnected_nodes",
    "network_embed_in_plane_proxy",
    "network_embed_in_plane",
    "network_explode",
    "network_find_crossings",
    "network_find_cycles",
    "network_is_connected",
    "network_is_crossed",
    "network_is_planar_embedding",
    "network_is_planar",
    "network_is_xy",
    "network_join_edges",
    "network_polylines",
    "network_shortest_path",
    "network_smooth_centroid",
    "network_split_edge",
    "network_transform",
    "network_transformed",
    # HalfEdge
    "HalfEdge",
    # Meshes
    "BaseMesh",
    "Mesh",
    "mesh_add_vertex_to_face_edge",
    "mesh_bounding_box_xy",
    "mesh_bounding_box",
    "mesh_collapse_edge",
    "mesh_connected_components",
    "mesh_conway_ambo",
    "mesh_conway_bevel",
    "mesh_conway_dual",
    "mesh_conway_expand",
    "mesh_conway_gyro",
    "mesh_conway_join",
    "mesh_conway_kis",
    "mesh_conway_meta",
    "mesh_conway_needle",
    "mesh_conway_ortho",
    "mesh_conway_snub",
    "mesh_conway_truncate",
    "mesh_conway_zip",
    "mesh_delete_duplicate_vertices",
    "mesh_disconnected_faces",
    "mesh_disconnected_vertices",
    "mesh_dual",
    "mesh_explode",
    "mesh_face_adjacency",
    "mesh_flatness",
    "mesh_flip_cycles",
    "mesh_insert_vertex_on_edge",
    "mesh_is_connected",
    "mesh_merge_faces",
    "mesh_offset",
    "mesh_planarize_faces",
    "mesh_quads_to_triangles",
    "mesh_slice_plane",
    "mesh_smooth_area",
    "mesh_smooth_centerofmass",
    "mesh_smooth_centroid",
    "mesh_split_edge",
    "mesh_split_face",
    "mesh_split_strip",
    "mesh_subdivide_catmullclark",
    "mesh_subdivide_corner",
    "mesh_subdivide_doosabin",
    "mesh_subdivide_frames",
    "mesh_subdivide_quad",
    "mesh_subdivide_tri",
    "mesh_subdivide",
    "mesh_substitute_vertex_in_faces",
    "mesh_thicken",
    "mesh_transform",
    "mesh_transformed",
    "mesh_unify_cycles",
    "mesh_unweld_edges",
    "mesh_unweld_vertices",
    "mesh_weld",
    "meshes_join_and_weld",
    "meshes_join",
    "trimesh_collapse_edge",
    "trimesh_face_circle",
    "trimesh_gaussian_curvature",
    "trimesh_mean_curvature",
    "trimesh_remesh",
    "trimesh_split_edge",
    "trimesh_subdivide_loop",
    "trimesh_swap_edge",
    # HalfFace
    "HalfFace",
    # Volumetric Meshes
    "BaseVolMesh",
    "VolMesh",
    "volmesh_bounding_box",
    "volmesh_transform",
    "volmesh_transformed",
    # Assemblies
    "Assembly",
    "Part",
    "AssemblyError",
    "FeatureError",
    "Feature",
    "GeometricFeature",
    "ParametricFeature",
    # Trees
    "Tree",
    "TreeNode",
]

if not compas.IPY:
    __all__ += [
        # Networks
        "network_adjacency_matrix",
        "network_connectivity_matrix",
        "network_degree_matrix",
        "network_laplacian_matrix",
        # Meshes
        "mesh_adjacency_matrix",
        "mesh_connectivity_matrix",
        "mesh_contours_numpy",
        "mesh_degree_matrix",
        "mesh_face_matrix",
        "mesh_geodesic_distances_numpy",
        "mesh_isolines_numpy",
        "mesh_laplacian_matrix",
        "mesh_oriented_bounding_box_numpy",
        "mesh_oriented_bounding_box_xy_numpy",
        "mesh_transform_numpy",
        "mesh_transformed_numpy",
        "trimesh_cotangent_laplacian_matrix",
        "trimesh_descent",
        "trimesh_pull_points_numpy",
        "trimesh_samplepoints_numpy",
        "trimesh_smooth_laplacian_cotangent",
        "trimesh_vertexarea_matrix",
    ]
