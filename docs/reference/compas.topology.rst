
********************************************************************************
compas.topology
********************************************************************************

.. currentmodule:: compas.topology

.. rst-class:: lead

Package containing topological algorithms for traversal, connectivity, combinatorics, etc.


Functions
=========

.. autosummary::
    :toctree: generated/
    :nosignatures:

    adjacency_from_edges
    astar_lightest_path
    astar_shortest_path
    breadth_first_ordering
    breadth_first_paths
    breadth_first_traverse
    connected_components
    depth_first_ordering
    dijkstra_distances
    dijkstra_path
    face_adjacency
    shortest_path
    unify_cycles
    vertex_coloring


Functions using Numpy
=====================

In environments where numpy is not available, these functions can still be accessed through RPC.

.. autosummary::
    :toctree: generated/
    :nosignatures:

    face_adjacency_numpy
    unify_cycles_numpy



