"""
********************************************************************************
topology
********************************************************************************

.. currentmodule:: compas.topology


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
    unify_cycles
    unify_cycles_numpy


Traversal
=========

.. autosummary::
    :toctree: generated/
    :nosignatures:

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
    astar_shortest_path,
    dijkstra_distances,
    dijkstra_path
)
from .combinatorics import (
    vertex_coloring,
    connected_components
)
from .orientation import (
    face_adjacency,
    unify_cycles
)
from .connectivity import adjacency_from_edges

if compas.IPY:
    from .orientation_rhino import (
        face_adjacency_rhino,
        unify_cycles_rhino
    )
else:
    from .orientation_numpy import (
        face_adjacency_numpy,
        unify_cycles_numpy
    )


__all__ = [
    'depth_first_ordering',
    'breadth_first_ordering',
    'breadth_first_traverse',
    'breadth_first_paths',
    'shortest_path',
    'astar_shortest_path',
    'dijkstra_distances',
    'dijkstra_path',
    'vertex_coloring',
    'connected_components',
    'face_adjacency',
    'unify_cycles',
    'adjacency_from_edges'
]

if compas.IPY:
    __all__ += [
        'face_adjacency_rhino',
        'unify_cycles_rhino',
    ]
else:
    __all__ += [
        'face_adjacency_numpy',
        'unify_cycles_numpy',
    ]
