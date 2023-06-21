from __future__ import absolute_import

import compas

if not compas.IPY:
    from .linalg import (
        nullspace,
        rank,
        dof,
        pivots,
        nonpivots,
        rref,
        rref_sympy,
        rref_matlab,
        uvw_lengths,
        normrow,
        normalizerow,
        rot90,
        solve_with_known,
        spsolve_with_known,
        chofactor,
        lufactorized,
    )
    from .matrices import (
        adjacency_matrix,
        degree_matrix,
        connectivity_matrix,
        laplacian_matrix,
        face_matrix,
        mass_matrix,
        stiffness_matrix,
        equilibrium_matrix,
    )
    from .operators import grad, div, curl
    from .utilities import (
        float_formatter,
        set_array_print_precision,
        unset_array_print_precision,
    )

    from .descent.descent_numpy import descent_numpy
    from .topop.topop_numpy import topop_numpy
    from .pca.pca_numpy import pca_numpy
    from .fd.fd_numpy import fd_numpy
    from .devo.devo_numpy import devo_numpy
    from .isolines.isolines_numpy import scalarfield_contours_numpy

from .ga.ga import ga
from .ga.moga import moga

__all__ = [
    "ga",
    "moga",
]

if not compas.IPY:
    __all__ += [
        "nullspace",
        "rank",
        "dof",
        "pivots",
        "nonpivots",
        "rref",
        "rref_sympy",
        "rref_matlab",
        "uvw_lengths",
        "normrow",
        "normalizerow",
        "rot90",
        "solve_with_known",
        "spsolve_with_known",
        "chofactor",
        "lufactorized",
        "adjacency_matrix",
        "degree_matrix",
        "connectivity_matrix",
        "laplacian_matrix",
        "face_matrix",
        "mass_matrix",
        "stiffness_matrix",
        "equilibrium_matrix",
        "grad",
        "div",
        "curl",
        "float_formatter",
        "set_array_print_precision",
        "unset_array_print_precision",
        "descent_numpy",
        "topop_numpy",
        "pca_numpy",
        "devo_numpy",
        "fd_numpy",
        "scalarfield_contours_numpy",
    ]
