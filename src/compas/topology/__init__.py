"""
.. _compas.topology:

********************************************************************************
topology
********************************************************************************

.. currentmodule:: compas.topology

.. autosummary::
    :toctree: generated/

    dfs_ordering
    dfs_paths
    bfs_ordering
    bfs_traverse
    bfs_paths
    shortest_path
    dijkstra_distances
    dijkstra_path
    vertex_coloring

"""

from .traversal import *
from .traversal import __all__ as a

from .combinatorial import *
from .combinatorial import __all__ as b


__all__ = a + b
