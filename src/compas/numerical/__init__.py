"""
This package defines a number of numerical utilities.
In future versions, this package will disappear,
and its functionality will be integrated into the geometry and datastructure packages directly.
"""
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
        uvw_lengths,
        normrow,
        normalizerow,
        rot90,
        solve_with_known,
        spsolve_with_known,
        chofactor,
        lufactorized,
    )


__all__ = []

if not compas.IPY:
    __all__ += [
        "nullspace",
        "rank",
        "dof",
        "pivots",
        "nonpivots",
        "rref",
        "uvw_lengths",
        "normrow",
        "normalizerow",
        "rot90",
        "solve_with_known",
        "spsolve_with_known",
        "chofactor",
        "lufactorized",
    ]
