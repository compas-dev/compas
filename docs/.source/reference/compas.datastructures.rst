
.. _compas.datastructures:

********************************************************************************
datastructures
********************************************************************************

.. module:: compas.datastructures


Network
=======

.. autosummary::
    :toctree: generated/

    Network
    FaceNetwork


network.operations
------------------

.. autosummary::
    :toctree: generated/

    network_split_edge


network.algorithms
------------------

.. autosummary::
    :toctree: generated/

    network_count_crossings
    network_dual
    network_embed_in_plane
    network_find_faces
    network_find_crossings
    network_is_xy
    network_is_crossed
    network_is_planar
    network_is_planar_embedding
    network_vertex_coloring


Mesh
====

Package for working with mesh objects.

.. autosummary::
    :toctree: generated/

    Mesh


mesh.operations
---------------

.. autosummary::
    :toctree: generated/

    mesh_collapse_edge
    mesh_split_edge
    mesh_split_face
    mesh_unweld_vertices


.. note::

    The following operations are specifically designed for triangle meshes.


.. autosummary::
    :toctree: generated/

    trimesh_collapse_edge
    trimesh_split_edge
    trimesh_swap_edge


mesh.algorithms
---------------

.. autosummary::
    :toctree: generated/

    mesh_delaunay_from_points
    mesh_dual
    mesh_flip_cycles
    mesh_subdivide
    mesh_subdivide_tri
    mesh_subdivide_catmullclark
    mesh_subdivide_doosabin
    mesh_unify_cycles
    mesh_voronoi_from_points


.. note::

    The following algorithms are specifically designed for triangle meshes.


.. autosummary::
    :toctree: generated/

    trimesh_remesh
    trimesh_subdivide_loop


VolMesh
=======


volmesh.operations
------------------


volmesh.algorithms
------------------


