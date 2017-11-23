""".. _compas.hpc:

********************************************************************************
hpc
********************************************************************************

.. module:: compas.hpc

.. warning::

    The functionality of this package is experimental and subject to frequent change.
    For now, don't use it for anything important :)

.. note::

    The HPC package id built around Numba, PyCuda and PyOpenCL

    * Numba: https://numba.pydata.org/
    * PyCuda: https://mathema.tician.de/software/pycuda/
    * PyOpenCL: https://mathema.tician.de/software/pyopencl/


algorithms
==========

.. autosummary::
    :toctree: generated/
    :nosignatures:

    drx_numba


geometry
========

.. autosummary::
    :toctree: generated/
    :nosignatures:

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


core
====

cuda
----

.. autosummary::
    :toctree: generated/
    :nosignatures:


euler
-----

.. autosummary::
    :toctree: generated/
    :nosignatures:

    core.euler.connect_to_euler
    core.euler.load_euler_module
    core.euler.recieve_file_from_euler
    core.euler.send_file_to_euler
    core.euler.send_folder_to_euler
    core.euler.show_euler_jobs
    core.euler.show_euler_quotas
    core.euler.show_euler_modules
    core.euler.show_euler_module_info
    core.euler.show_euler_resources
    core.euler.submit_job
    core.euler.kill_job
    core.euler.sync_folder_to_euler


numba
-----

.. autosummary::
    :toctree: generated/
    :nosignatures:


opencl
------

.. autosummary::
    :toctree: generated/
    :nosignatures:


"""
from .geometry import *
from .algorithms import *

from .geometry import __all__ as a
from .algorithms import __all__ as b

__all__ = a + b
