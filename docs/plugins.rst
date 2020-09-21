================
Extension points
================

COMPAS has an extensible architecture based on plugins that allows to
customize and extend the functionality of the core framework.

The following **extension points** are currently defined:


Category: ``booleans``
^^^^^^^^^^^^^^^^^^^^^^

.. currentmodule:: compas.geometry
.. autosummary::
    :toctree: generated/
    :nosignatures:

    boolean_union_mesh_mesh
    boolean_difference_mesh_mesh
    boolean_intersection_mesh_mesh


Category: ``install``
^^^^^^^^^^^^^^^^^^^^^

.. currentmodule:: compas_rhino.install
.. autosummary::
    :toctree: generated/
    :nosignatures:

    installable_rhino_packages


Category: ``intersections``
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. currentmodule:: compas.geometry
.. autosummary::
    :toctree: generated/
    :nosignatures:

    intersection_mesh_mesh
    intersection_ray_mesh


Category: ``quadmesh``
^^^^^^^^^^^^^^^^^^^^^^

.. currentmodule:: compas.geometry
.. autosummary::
    :toctree: generated/
    :nosignatures:

    quadmesh_planarize


Category: ``triangulation``
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. currentmodule:: compas.geometry
.. autosummary::
    :toctree: generated/
    :nosignatures:

    delaunay_triangulation
    constrained_delaunay_triangulation
    conforming_delaunay_triangulation


Category: ``trimesh``
^^^^^^^^^^^^^^^^^^^^^

.. currentmodule:: compas.geometry
.. autosummary::
    :toctree: generated/
    :nosignatures:

    trimesh_gaussian_curvature
    trimesh_principal_curvature
    trimesh_geodistance
    trimesh_isolines
    trimesh_massmatrix
    trimesh_harmonic
    trimesh_lscm
    trimesh_remesh
    trimesh_remesh_constrained
    trimesh_slice


Check out the developer guide to :ref:`plugins` for additional details.
