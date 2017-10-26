""".. _compas.numerical:

********************************************************************************
numerical
********************************************************************************

.. module:: compas.numerical

A package for numerical computation.


.. note::

    This package is built around NumPy and Scipy

    * NumPy: http://www.numpy.org/ 
    * SciPy: http://www.scipy.org/

    and has several other optional dependencies (SymPy, Numba, PyCuda, Cython, CVXPY, Alglib).
    Most of these are shipped with scientific Python distributions, such as Anaconda and EPD.


Methods
=======

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
    GA
    lma
    mma
    MOGA


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

.. autosummary::
    :toctree: generated/

    network_adjacency_matrix
    network_degree_matrix
    network_connectivity_matrix
    network_laplacian_matrix

.. autosummary::
    :toctree: generated/

    mesh_adjacency_matrix
    mesh_degree_matrix
    mesh_connectivity_matrix
    mesh_laplacian_matrix

.. autosummary::
    :toctree: generated/

    trimesh_cotangent_laplacian_matrix


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

from .solvers import *
from .methods import *

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

from .solvers import __all__ as k
from .methods import __all__ as l

__all__ = a + b + c + d + e + f + g + h + i + j + k + l
