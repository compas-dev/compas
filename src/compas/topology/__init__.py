"""
Package containing topological algorithms for traversal, connectivity, combinatorics, etc.
"""

from __future__ import absolute_import

import compas

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
from .connectivity import adjacency_from_edges

if compas.RHINO:
    from .orientation_rhino import face_adjacency_rhino, unify_cycles_rhino

if not compas.IPY:
    from .orientation_numpy import face_adjacency_numpy, unify_cycles_numpy


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
    "adjacency_from_edges",
]

if compas.RHINO:
    __all__ += [
        "face_adjacency_rhino",
        "unify_cycles_rhino",
    ]

if not compas.IPY:
    __all__ += [
        "face_adjacency_numpy",
        "unify_cycles_numpy",
    ]
