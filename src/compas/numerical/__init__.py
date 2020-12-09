"""
********************************************************************************
numerical
********************************************************************************

.. currentmodule:: compas.numerical


Solvers
=======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    devo_numpy
    dr
    dr_numpy
    fd_numpy
    ga
    moga
    pca_numpy
    topop_numpy


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

import compas

if not compas.IPY:
    from .linalg import *  # noqa: F401 F403
    from .matrices import *  # noqa: F401 F403
    from .operators import *  # noqa: F401 F403
    from .utilities import *  # noqa: F401 F403

from .topop import *  # noqa: F401 F403
from .pca import *  # noqa: F401 F403
from .ga import *  # noqa: F401 F403
from .fd import *  # noqa: F401 F403
# from .drx import *  # noqa: F401 F403
from .dr import *  # noqa: F401 F403
from .devo import *  # noqa: F401 F403
from .isolines import *  # noqa: F401 F403


__all__ = [name for name in dir() if not name.startswith('_')]
