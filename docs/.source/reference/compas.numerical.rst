.. _compas.numerical:

********************************************************************************
numerical
********************************************************************************

.. module:: compas.numerical


A package for numerical computation.


Core
====

geometry
--------

.. autosummary::
    :toctree: generated/

    scalarfield_contours
    plot_scalarfield_contours


linalg
------

.. autosummary::
    :toctree: generated/

    nullspace
    rank
    dof
    pivots
    nonpivots
    rref
    chofactor
    lufactorized
    normrow
    normalizerow
    rot90
    solve_with_known
    spsolve_with_known


matrices
--------

.. autosummary::
    :toctree: generated/

    adjacency_matrix
    degree_matrix
    connectivity_matrix
    laplacian_matrix
    face_matrix
    mass_matrix
    stiffness_matrix
    equilibrium_matrix


operators
---------

.. autosummary::
    :toctree: generated/

    grad
    div
    curl


spatial
-------

.. autosummary::
    :toctree: generated/

    closest_points_points
    project_points_heightfield
    iterative_closest_point
    bounding_box_xy
    bounding_box


statistics
----------

.. autosummary::
    :toctree: generated/

    principal_components


transformations
---------------

.. autosummary::
    :toctree: generated/


triangulation
-------------

.. autosummary::
    :toctree: generated/


utilities
---------

.. autosummary::
    :toctree: generated/

    set_array_print_precision
    unset_array_print_precision


xforms
------

.. autosummary::
    :toctree: generated/

    translation_matrix
    rotation_matrix
    random_rotation_matrix
    scale_matrix
    projection_matrix


Methods
=======

.. autosummary::
    :toctree: generated/

    methods.dr
    methods.drx
    methods.fd


Solvers
=======

.. autosummary::
    :toctree: generated/

    solvers.descent
    solvers.devo
    solvers.GA
    solvers.lma
    solvers.mma
    solvers.MOGA

