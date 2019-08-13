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

.. autosummary::
    :toctree: generated/
    :nosignatures:

    Mesh

Mesh matrices
-------------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    mesh_adjacency_matrix
    mesh_connectivity_matrix
    mesh_degree_matrix
    mesh_face_matrix
    mesh_laplacian_matrix

.. autosummary::
    :toctree: generated/
    :nosignatures:

    trimesh_cotangent_laplacian_matrix
    trimesh_vertexarea_matrix

Mesh algorithms
---------------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    mesh_bounding_box
    mesh_bounding_box_xy
    mesh_oriented_bounding_box_numpy
    mesh_oriented_bounding_box_xy_numpy
    mesh_contours_numpy
    mesh_dual
    mesh_geodesic_distances
    mesh_isolines_numpy
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

.. autosummary::
    :toctree: generated/
    :nosignatures:

    trimesh_gaussian_curvature
    trimesh_remesh
    trimesh_subdivide_loop

Mesh helpers
------------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    mesh_delete_duplicate_vertices
    mesh_face_adjacency
    mesh_flip_cycles
    mesh_is_connected
    mesh_unify_cycles

Network
=======

The network is a connectivity graph.
It is meant for the representation of networks of vertices connected by edges.
The edges are directed. A network does not have faces. A network can be connected
or disconnected. A network with vertices only is also a valid network.

.. autosummary::
    :toctree: generated/
    :nosignatures:

    Network

Network algorithms
------------------

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

.. autosummary::
    :toctree: generated/
    :nosignatures:

    VolMesh

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
