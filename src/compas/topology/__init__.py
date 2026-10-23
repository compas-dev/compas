"""Topological algorithms for traversal, connectivity, and combinatorics."""

from .combinatorics import vertex_coloring, connected_components
from .connectivity import (
    edges_from_faces,
    faces_from_edges,
    vertex_adjacency_from_edges,
    vertex_adjacency_from_faces,
)
from .orientation import face_adjacency, unify_cycles
from .traversal import (
    astar_lightest_path,
    astar_shortest_path,
    breadth_first_ordering,
    breadth_first_paths,
    breadth_first_traverse,
    breadth_first_tree,
    depth_first_ordering,
    dijkstra_distances,
    dijkstra_path,
    shortest_path,
)

__all__ = [
    "astar_lightest_path",
    "astar_shortest_path",
    "breadth_first_ordering",
    "breadth_first_paths",
    "breadth_first_traverse",
    "breadth_first_tree",
    "connected_components",
    "depth_first_ordering",
    "dijkstra_distances",
    "dijkstra_path",
    "edges_from_faces",
    "face_adjacency",
    "faces_from_edges",
    "shortest_path",
    "unify_cycles",
    "vertex_adjacency_from_edges",
    "vertex_adjacency_from_faces",
    "vertex_coloring",
]
