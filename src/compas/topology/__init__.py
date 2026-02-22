"""
Package containing topological algorithms for traversal, connectivity, combinatorics, etc.
"""
# ruff: noqa: F401

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
