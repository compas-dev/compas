
********************************************************************************
compas.numerical
********************************************************************************

.. currentmodule:: compas.numerical

.. rst-class:: lead


This package defines a number of numerical utilities.
In future versions, this package will disappear,
and its functionality will be integrated into the geometry and datastructure packages directly.


Functions
=========

.. autosummary::
    :toctree: generated/
    :nosignatures:

    adjacency_matrix
    chofactor
    connectivity_matrix
    degree_matrix
    dof
    equilibrium_matrix
    face_matrix
    laplacian_matrix
    lufactorized
    mass_matrix
    nonpivots
    normalizerow
    normrow
    nullspace
    pivots
    rank
    rot90
    rref
    solve_with_known
    spsolve_with_known
    stiffness_matrix
    uvw_lengths


Functions using Numpy
=====================

In environments where numpy is not available, these functions can still be accessed through RPC.

.. autosummary::
    :toctree: generated/
    :nosignatures:

    pca_numpy


Pluggables
==========

Pluggables are functions that don't have an actual implementation, but receive an implementation from a plugin.

.. autosummary::
    :toctree: generated/
    :nosignatures:

    scalarfield_contours
