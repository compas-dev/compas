"""
********************************************************************************
compas.topology
********************************************************************************

.. currentmodule:: compas.topology

conway_operators
-------------

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
-------------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    adjacency_from_edges
    connectivity_from_edges
    join_lines_to_polylines

combinatorics
-------------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    vertex_coloring
    connected_components
    mesh_is_connected
    network_is_connected

complementarity
-------------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    network_complement

duality
-------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    mesh_dual
    network_dual
    network_find_faces

orientation
-----------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    face_adjacency
    flip_cycles
    mesh_face_adjacency
    mesh_flip_cycles
    mesh_unify_cycles

planarity
---------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    network_is_crossed
    network_count_crossings
    network_find_crossings
    network_is_xy
    network_is_planar
    network_is_planar_embedding
    network_embed_in_plane

subdivision
-----------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    mesh_subdivide
    mesh_subdivide_tri
    mesh_subdivide_corner
    mesh_subdivide_quad
    mesh_subdivide_catmullclark
    mesh_subdivide_doosabin
    trimesh_subdivide_loop   

traversal
---------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    depth_first_ordering
    depth_first_tree
    breadth_first_ordering
    breadth_first_traverse
    breadth_first_paths
    shortest_path
    dijkstra_distances
    dijkstra_path

triangulation
-------------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    delaunay_from_points
    voronoi_from_delaunay
    mesh_quads_to_triangles
    trimesh_remesh


"""
from __future__ import absolute_imports, division, print_function

from .traversal import *
from .combinatorics import *
from .duality import *
from .orientation import *
from .planarity import *
from .subdivision import *
from .triangulation import *
from .connectivity import *
from .conway import *
from .complementarity import *

__all__ = [name for name in dir() if not name.startswith('_')]
