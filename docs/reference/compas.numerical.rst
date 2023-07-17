********************************************************************************
compas.numerical
********************************************************************************

.. currentmodule:: compas.numerical

.. rst-class:: lead

This package provides some basic linear algabra functions,
and matrix-based implementations of various geometric and topological algorithms.

Solvers
=======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    pca_numpy


Isolines
========

.. autosummary::
    :toctree: generated/
    :nosignatures:

    scalarfield_contours_numpy


Linalg
======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    nullspace
    rank
    dof
    pivots
    nonpivots
    rref
    rref_sympy
    rref_matlab
    chofactor
    lufactorized
    uvw_lengths
    normrow
    normalizerow
    rot90
    solve_with_known
    spsolve_with_known


Matrices
========

.. autosummary::
    :toctree: generated/
    :nosignatures:

    adjacency_matrix
    connectivity_matrix
    degree_matrix
    equilibrium_matrix
    face_matrix
    laplacian_matrix
    mass_matrix
    stiffness_matrix
