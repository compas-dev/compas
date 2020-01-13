"""
********************************************************************************
topology
********************************************************************************

.. currentmodule:: compas.topology

conway_operators
----------------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    conway_dual
    conway_join
    conway_ambo
    conway_kis
    conway_needle
    conway_zip
    conway_truncate
    conway_ortho
    conway_expand
    conway_gyro
    conway_snub
    conway_meta
    conway_bevel

connectivity
------------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    adjacency_from_edges

combinatorics
-------------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    vertex_coloring
    connected_components

orientation
-----------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    face_adjacency
    face_adjacency_numpy
    unify_cycles
    unify_cycles_numpy

traversal
---------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    depth_first_ordering
    breadth_first_ordering
    breadth_first_traverse
    breadth_first_paths
    shortest_path
    astar_shortest_path
    dijkstra_distances
    dijkstra_path

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
from .conway import *  # noqa: F401 F403


__all__ = [name for name in dir() if not name.startswith('_')]
