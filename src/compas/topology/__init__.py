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
    unify_cycles

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
    dijkstra_distances
    dijkstra_path

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


from .traversal import *
from .combinatorics import *
from .orientation import *
from .connectivity import *
from .conway import *


__all__ = [name for name in dir() if not name.startswith('_')]
