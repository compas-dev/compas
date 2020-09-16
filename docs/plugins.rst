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

Check out the developer guide to :ref:`plugins` for additional details.
