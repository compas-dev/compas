"""
********************************************************************************
compas.numerical
********************************************************************************

.. currentmodule:: compas.numerical


Solvers
=======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    descent
    devo_numpy
    dr
    dr_numpy
    drx_numpy
    fd_numpy
    ga
    lma
    mma
    moga
    pca_numpy
    topop2d_numpy
    topop3d_numpy


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
    degree_matrix
    connectivity_matrix
    laplacian_matrix
    face_matrix
    mass_matrix
    equilibrium_matrix


Operators
=========

.. autosummary::
    :toctree: generated/
    :nosignatures:

    grad


Utilities
=========

.. autosummary::
    :toctree: generated/
    :nosignatures:

    float_formatter
    set_array_print_precision
    unset_array_print_precision


"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from .linalg import *
from .matrices import *
from .operators import *
from .utilities import *

from .solvers import *
from .algorithms import *

from .dr import *
from .drx import *
from .fd import *

__all__ = [name for name in dir() if not name.startswith('_')]
