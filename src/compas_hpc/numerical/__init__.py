"""
********************************************************************************
compas_hpc.numerical
********************************************************************************

.. currentmodule:: compas_hpc.numerical

Linalg
======

Numba
-----

.. autosummary::
    :toctree: generated/
    :nosignatures:

    rotate_x_numba
    rotate_y_numba
    rotate_z_numba
    trace_numba
    diag_numba
    diag_complex_numba
    diag_fill_numba
    diag_fill_complex_numba
    scale_matrix_numba
    scale_matrix_complex_numba
    multiply_matrices_numba
    multiply_matrices_complex_numba
    divide_matrices_numba
    divide_matrices_complex_numba
    dot_numba
    dotv_numba
    transpose_numba

PyCUDA
------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    diag_cuda
    transpose_cuda
    dot_cuda
    eye_cuda

PyOpenCL
--------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    diag_cl
    transpose_cl
    eye_cl

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from .linalg_cl import *  # noqa: F401 F403
from .linalg_cuda import *  # noqa: F401 F403
from .linalg_numba import *  # noqa: F401 F403

__all__ = [name for name in dir() if not name.startswith('_')]
