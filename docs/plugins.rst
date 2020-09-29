================
Extension points
================

.. rst-class:: lead

COMPAS has an extensible architecture based on plugins that allows to
customize and extend the functionality of the core framework.
Check out the developer guide for additional details.

The following *extension points* are currently defined:


Category: ``booleans``
^^^^^^^^^^^^^^^^^^^^^^

.. currentmodule:: compas.geometry

* :func:`boolean_union_mesh_mesh`
* :func:`boolean_difference_mesh_mesh`
* :func:`boolean_intersection_mesh_mesh`


Category: ``install``
^^^^^^^^^^^^^^^^^^^^^

.. currentmodule:: compas_rhino.install

* :func:`installable_rhino_packages`


Category: ``intersections``
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. currentmodule:: compas.geometry

* :func:`intersection_mesh_mesh`
* :func:`intersection_ray_mesh`


Category: ``quadmesh``
^^^^^^^^^^^^^^^^^^^^^^

.. currentmodule:: compas.geometry

* :func:`quadmesh_planarize`


Category: ``triangulation``
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. currentmodule:: compas.geometry

* :func:`delaunay_triangulation`
* :func:`constrained_delaunay_triangulation`
* :func:`conforming_delaunay_triangulation`


Category: ``trimesh``
^^^^^^^^^^^^^^^^^^^^^

.. currentmodule:: compas.geometry

* :func:`trimesh_gaussian_curvature`
* :func:`trimesh_principal_curvature`
* :func:`trimesh_geodistance`
* :func:`trimesh_isolines`
* :func:`trimesh_massmatrix`
* :func:`trimesh_harmonic`
* :func:`trimesh_lscm`
* :func:`trimesh_remesh`
* :func:`trimesh_remesh_constrained`
* :func:`trimesh_slice`
