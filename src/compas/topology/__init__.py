"""
.. _compas.topology:

********************************************************************************
topology
********************************************************************************

.. currentmodule:: compas.topology


combinatorial
-------------

.. autosummary::
    :toctree: generated/

    vertex_coloring

orientation
-----------

.. autosummary::
    :toctree: generated/

    mesh_flip_cycles
    mesh_unify_cycles

planarity
---------

.. autosummary::
    :toctree: generated/

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

    mesh_subdivide
    mesh_subdivide_tri
    mesh_subdivide_catmullclark
    mesh_subdivide_doosabin

traversal
---------

.. autosummary::
    :toctree: generated/

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

    delaunay_from_points
    voronoi_from_delaunay
    mesh_quads_to_triangles
    trimesh_remesh


"""

from .traversal import *

from .combinatorial import *
from .duality import *
from .orientation import *
from .planarity import *
from .subdivision import *
from .triangulation import *

from .combinatorial import __all__ as a
from .duality import __all__ as b
from .orientation import __all__ as c
from .planarity import __all__ as d
from .subdivision import __all__ as e
from .traversal import __all__ as f
from .triangulation import __all__ as g


__all__ = a + b + c + d + e + f + g
