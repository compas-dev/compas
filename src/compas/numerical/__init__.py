""".. _compas.numerical:

********************************************************************************
numerical
********************************************************************************

.. module:: compas.numerical


Algorithms
==========

.. autosummary::
    :toctree: generated/

    dr
    drx
    fd


Solvers
=======

.. autosummary::
    :toctree: generated/

    descent
    devo
    ga
    lma
    mma
    moga


Functions
=========

**linalg**

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


**matrices**

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


**operators**

.. autosummary::
    :toctree: generated/

    grad
    div
    curl


Utilities
=========

.. autosummary::
    :toctree: generated/

    set_array_print_precision
    unset_array_print_precision


"""

from .linalg import *
from .matrices import *
from .operators import *
from .utilities import *

from .solvers import *
from .algorithms import *

from .linalg import __all__ as a
from .matrices import __all__ as b
from .operators import __all__ as c
from .utilities import __all__ as d

from .solvers import __all__ as e
from .algorithms import __all__ as f

__all__ = a + b + c + d + e + f
