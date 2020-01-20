"""
********************************************************************************
compas_hpc
********************************************************************************

.. module:: compas_hpc

This package provides GPU-accelerated and compiled versions of many geometry,
numerical and topological functions and algorithms. The package is built around
`Numba`_, `PyCUDA`_ and `PyOpenCL`_.

.. _Numba: https://numba.pydata.org/
.. _PyCuda: https://mathema.tician.de/software/pycuda/
.. _PyOpenCL: https://mathema.tician.de/software/pyopencl/


.. warning::

    The functionality of this package is experimental and subject to frequent change.
    For now, don't use it for anything important :)


linalg
======

linalg_numba
------------

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

linalg_cuda
-----------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    diag_cuda
    transpose_cuda
    dot_cuda
    eye_cuda


linalg_cl
---------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    diag_cl
    transpose_cl
    eye_cl


core
====

cuda
----

.. autosummary::
    :toctree: generated/
    :nosignatures:

    device_cuda
    rand_cuda
    give_cuda
    get_cuda
    ones_cuda
    zeros_cuda
    tile_cuda
    hstack_cuda
    vstack_cuda

    abs_cuda
    acos_cuda
    asin_cuda
    atan_cuda
    ceil_cuda
    cos_cuda
    cosh_cuda
    exp_cuda
    floor_cuda
    log_cuda
    log10_cuda
    maximum_cuda
    minimum_cuda
    round_cuda
    sin_cuda
    sinh_cuda
    sqrt_cuda
    sum_cuda
    tan_cuda
    tanh_cuda


opencl
------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    rand_cl
    give_cl
    get_cl
    ones_cl
    zeros_cl
    tile_cl
    hstack_cl
    vstack_cl

    abs_cl
    acos_cl
    asin_cl
    atan_cl
    ceil_cl
    cos_cl
    cosh_cl
    exp_cl
    floor_cl
    log_cl
    log10_cl
    maximum_cl
    minimum_cl
    round_cl
    sin_cl
    sinh_cl
    sqrt_cl
    sum_cl
    tan_cl
    tanh_cl


geometry
========

basic
-----

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
    orthonormalize_vectors_numba
    plane_from_points_numba
    circle_from_points_numba
    circle_from_points_xy_numba

average_numba
-------------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    centroid_points_numba
    centroid_points_xy_numba
    midpoint_point_point_numba
    midpoint_point_point_xy_numba
    center_of_mass_polyline_numba
    center_of_mass_polyline_xy_numba


spatial_numba
-------------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    distance_matrix_numba
    closest_distance_field_numba

"""

from .geometry import *
from .core import *
from .linalg import *

from .geometry import __all__ as b
from .core import __all__ as c
from .linalg import __all__ as a

__all__ = b + c + a
