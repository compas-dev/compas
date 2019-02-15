"""
********************************************************************************
datastructures
********************************************************************************

.. currentmodule:: compas.datastructures


Mesh
====

The mesh is implemented as a half-edge datastructure.
It is meant for the representation of polygonal *"surface"* meshes. A mesh can be
connected or disconnected. A mesh can be closed or open. A mesh can be comprised
of only vertices.

Classes
-------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    Mesh

Functions
---------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    mesh_adjacency_matrix
    mesh_bounding_box
    mesh_bounding_box_xy
    mesh_connectivity_matrix
    mesh_contours_numpy
    mesh_contours_pymesh
    mesh_degree_matrix
    mesh_delete_duplicate_vertices
    mesh_dual
    mesh_face_adjacency
    mesh_face_matrix
    mesh_flatness
    mesh_flip_cycles
    mesh_geodesic_distances
    mesh_is_connected
    mesh_isolines_numpy
    mesh_laplacian_matrix
    mesh_planarize_faces
    mesh_quads_to_triangles
    mesh_smooth_centroid
    mesh_smooth_area
    mesh_subdivide
    mesh_subdivide_tri
    mesh_subdivide_corner
    mesh_subdivide_quad
    mesh_subdivide_catmullclark
    mesh_subdivide_doosabin
    mesh_transform
    mesh_transformed
    mesh_unify_cycles

    trimesh_cotangent_laplacian_matrix
    trimesh_gaussian_curvature
    trimesh_mean_curvature
    trimesh_remesh
    trimesh_subdivide_loop
    trimesh_vertexarea_matrix

Network
=======

The network is a connectivity graph.
It is meant for the representation of networks of vertices connected by edges.
The edges are directed. A network does not have faces. A network can be connected
or disconnected. A network with vertices only is also a valid network.

Classes
-------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    Network

Functions
---------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    network_complement
    network_count_crossings
    network_dual
    network_embed_in_plane
    network_find_crossings
    network_find_faces
    network_is_connected
    network_is_crossed
    network_is_planar
    network_is_planar_embedding
    network_is_xy
    network_smooth_centroid

VolMesh
=======

The volmesh is a cellular mesh. It is implemented as
a half-plane, the three-dimensional equivalent of a half-edge. It can, for example,
be used for the representation of subdivided/partitioned polyhedra.

Classes
-------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    VolMesh

Functions
---------

.. autosummary::
    :toctree: generated/
    :nosignatures:

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


class Datastructure(object):
    pass


from .network import *
from .mesh import *
from .volmesh import *

__all__ = [name for name in dir() if not name.startswith('_')]
