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
from .connectivity import (
    vertex_adjacency_from_edges,
    vertex_adjacency_from_faces,
    edges_from_faces,
    faces_from_edges,
)

__all__ = [
    "astar_lightest_path",
    "astar_shortest_path",
    "breadth_first_ordering",
    "breadth_first_traverse",
    "breadth_first_paths",
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
