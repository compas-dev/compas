""".. _compas.numerical:

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

"""

from .geometry import *
from .linalg import *
from .matrices import *
from .operators import *
from .spatial import *
from .statistics import *
from .transformations import *
from .triangulation import *
from .utilities import *
from .xforms import *
from .methods import *
from .solvers import *

from .geometry import __all__ as a
from .linalg import __all__ as b
from .matrices import __all__ as c
from .operators import __all__ as d
from .spatial import __all__ as e
from .statistics import __all__ as f
from .transformations import __all__ as g
from .triangulation import __all__ as h
from .utilities import __all__ as i
from .xforms import __all__ as j
from .methods import __all__ as k
from .solvers import __all__ as l

__all__ = a + b + c + d + e + f + g + h + i + j + k + l
