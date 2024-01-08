"""
Package containing topological algorithms for traversal, connectivity, combinatorics, etc.
"""

from __future__ import absolute_import

from .traversal import (
    depth_first_ordering,
    breadth_first_ordering,
    breadth_first_traverse,
    breadth_first_paths,
    shortest_path,
    astar_lightest_path,
    astar_shortest_path,
    dijkstra_distances,
    dijkstra_path,
)
from .combinatorics import vertex_coloring, connected_components
from .orientation import face_adjacency, unify_cycles
from .connectivity import vertex_adjacency_from_edges
from .matrices import adjacency_matrix, degree_matrix, connectivity_matrix, laplacian_matrix, face_matrix


__all__ = [
    "depth_first_ordering",
    "breadth_first_ordering",
    "breadth_first_traverse",
    "breadth_first_paths",
    "shortest_path",
    "astar_lightest_path",
    "astar_shortest_path",
    "dijkstra_distances",
    "dijkstra_path",
    "vertex_coloring",
    "connected_components",
    "face_adjacency",
    "unify_cycles",
    "vertex_adjacency_from_edges",
    "adjacency_matrix",
    "degree_matrix",
    "connectivity_matrix",
    "laplacian_matrix",
    "face_matrix",
]
