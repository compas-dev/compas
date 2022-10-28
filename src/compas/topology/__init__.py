"""
********************************************************************************
topology
********************************************************************************

.. currentmodule:: compas.topology

.. rst-class:: lead

    Package containing topological algorithms for traversal, connectivity, combinatorics, etc.


Connectivity
============

.. autosummary::
    :toctree: generated/
    :nosignatures:

    adjacency_from_edges


Combinatorics
=============

.. autosummary::
    :toctree: generated/
    :nosignatures:

    vertex_coloring
    connected_components


Orientation
===========

.. autosummary::
    :toctree: generated/
    :nosignatures:

    face_adjacency
    face_adjacency_numpy
    face_adjacency_rhino
    unify_cycles
    unify_cycles_numpy
    unify_cycles_rhino


Traversal
=========

.. autosummary::
    :toctree: generated/
    :nosignatures:

    astar_lightest_path
    astar_shortest_path
    breadth_first_ordering
    breadth_first_traverse
    breadth_first_paths
    depth_first_ordering
    dijkstra_distances
    dijkstra_path
    shortest_path

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
