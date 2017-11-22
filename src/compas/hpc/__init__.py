""".. _compas.hpc:

********************************************************************************
hpc
********************************************************************************

.. module:: compas.hpc


.. warning::

    The functionality of this package is experimental and subject to frequent change.
    For now, don't use it for anything important :)


algorithms
==========

.. autosummary::
    :toctree: generated/

    drx_numba


geometry
========

.. autosummary::
    :toctree: generated/

    sum_vectors_numba
    norm_vector_numba
    norm_vectors_numba
    length_vector_numba
    length_vector_xy_numba
    length_vector_sqrd_numba
    length_vector_sqrd_xy_numba
    scale_vector_numba
    scale_vector_xy_numba
    scale_vectors_numba
    scale_vectors_xy_numba
    normalize_vector_numba
    normalize_vector_xy_numba
    normalize_vectors_numba
    normalize_vectors_xy_numba
    power_vector_numba
    power_vectors_numba
    square_vector_numba
    square_vectors_numba
    add_vectors_numba
    add_vectors_xy_numba
    subtract_vectors_numba
    subtract_vectors_xy_numba
    multiply_vectors_numba
    multiply_vectors_xy_numba
    divide_vectors_numba
    divide_vectors_xy_numba
    cross_vectors_numba
    cross_vectors_xy_numba
    dot_vectors_numba
    dot_vectors_xy_numba
    vector_component_numba
    vector_component_xy_numba
    multiply_matrices_numba
    multiply_matrix_vector_numba
    transpose_matrix_numba
    orthonormalise_vectors_numba
    plane_from_points_numba
    circle_from_points_numba
    circle_from_points_xy_numba


solvers
====

.. autosummary::
    :toctree: generated/

    devo_numba


core
=====

.. autosummary::
    :toctree: generated/

    connect_to_euler
    load_euler_module
    recieve_file_from_euler
    send_file_to_euler
    send_folder_to_euler
    show_euler_jobs
    show_euler_quotas
    show_euler_modules
    show_euler_module_info
    show_euler_resources
    submit_job
    kill_job
    sync_folder_to_euler

"""

from .geometry import *
from .core import *
from .algorithms import *
from .solvers import *

from .geometry import __all__ as a
from .core import __all__ as b
from .algorithms import __all__ as c
from .solvers import __all__ as d

__all__ = a + b + c + d
