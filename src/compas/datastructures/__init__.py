"""
This package defines the core data structures of the COMPAS framework.
The data structures provide a structured way of storing and accessing data on individual components of both topological and geometrical objects.
"""

from __future__ import absolute_import

from .datastructure import Datastructure

# =============================================================================
# Graphs
# =============================================================================

from .graph.planarity import graph_embed_in_plane_proxy  # noqa: F401

# =============================================================================
# Meshes
# =============================================================================

from .mesh.conway import (  # noqa: F401
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
from .mesh.smoothing import mesh_smooth_centerofmass  # noqa: F401
from .mesh.subdivision import trimesh_subdivide_loop  # noqa: F401

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
from .mesh.mesh import Mesh
from .volmesh.volmesh import VolMesh
from .assembly.exceptions import AssemblyError, FeatureError
from .assembly.assembly import Assembly
from .assembly.part import Feature, GeometricFeature, ParametricFeature, Part
from .cell_network.cell_network import CellNetwork
from .tree.tree import Tree, TreeNode
from .tree.hashtree import HashTree, HashNode

Network = Graph

__all__ = [
    "Datastructure",
    "CellNetwork",
    "Mesh",
    "VolMesh",
    "Assembly",
    "Part",
    "AssemblyError",
    "FeatureError",
    "Feature",
    "GeometricFeature",
    "ParametricFeature",
    "Tree",
    "TreeNode",
    "HashTree",
    "HashNode",
]
