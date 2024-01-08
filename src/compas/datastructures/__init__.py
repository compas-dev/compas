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

from .mesh.operations.collapse import trimesh_collapse_edge
from .mesh.operations.insert import mesh_add_vertex_to_face_edge, mesh_insert_vertex_on_edge
from .mesh.operations.split import trimesh_split_edge
from .mesh.operations.substitute import mesh_substitute_vertex_in_faces
from .mesh.operations.swap import trimesh_swap_edge
from .mesh.operations.weld import mesh_unweld_edges, mesh_unweld_vertices

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
from .mesh.remesh import trimesh_remesh
from .mesh.smoothing import mesh_smooth_area, mesh_smooth_centerofmass, mesh_smooth_centroid
from .mesh.subdivision import trimesh_subdivide_loop

if not compas.IPY:
    from .mesh.matrices import (
        trimesh_cotangent_laplacian_matrix,
        trimesh_vertexarea_matrix,
    )

    from .mesh.smoothing_numpy import trimesh_smooth_laplacian_cotangent

# =============================================================================
# Halffaces
# =============================================================================

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

__all__ = [
    "Datastructure",
    # Graphs
    "Graph",
    # Networks
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
    "Mesh",
    "mesh_add_vertex_to_face_edge",
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
    "mesh_insert_vertex_on_edge",
    "mesh_smooth_area",
    "mesh_smooth_centerofmass",
    "mesh_smooth_centroid",
    "mesh_substitute_vertex_in_faces",
    "mesh_unweld_edges",
    "mesh_unweld_vertices",
    "trimesh_collapse_edge",
    "trimesh_remesh",
    "trimesh_split_edge",
    "trimesh_subdivide_loop",
    "trimesh_swap_edge",
    # HalfFace
    "HalfFace",
    # Volumetric Meshes
    "VolMesh",
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
        "trimesh_cotangent_laplacian_matrix",
        "trimesh_smooth_laplacian_cotangent",
        "trimesh_vertexarea_matrix",
    ]
