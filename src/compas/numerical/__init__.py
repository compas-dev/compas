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

    from .pca.pca_numpy import pca_numpy
    from .isolines.isolines_numpy import scalarfield_contours_numpy


__all__ = []

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
        "pca_numpy",
        "scalarfield_contours_numpy",
    ]
