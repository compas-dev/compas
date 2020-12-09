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
from __future__ import division
from __future__ import print_function

import compas

from .traversal import *  # noqa: F401 F403
from .combinatorics import *  # noqa: F401 F403
from .orientation import *  # noqa: F401 F403

if compas.IPY:
    from .orientation_rhino import *  # noqa: F401 F403
else:
    from .orientation_numpy import *  # noqa: F401 F403

from .connectivity import *  # noqa: F401 F403


__all__ = [name for name in dir() if not name.startswith('_')]
