"""
********************************************************************************
compas.topology
********************************************************************************

.. currentmodule:: compas.topology


combinatorics
-------------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    vertex_coloring
    connected_components
    mesh_is_connected
    network_is_connected

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

from .traversal import *

from .combinatorics import *
from .duality import *
from .orientation import *
from .planarity import *
from .subdivision import *
from .triangulation import *
from .connectivity import *

from .combinatorics import __all__ as a
from .duality import __all__ as b
from .orientation import __all__ as c
from .planarity import __all__ as d
from .subdivision import __all__ as e
from .traversal import __all__ as f
from .triangulation import __all__ as g
from .connectivity import __all__ as h


__all__ = a + b + c + d + e + f + g + h
