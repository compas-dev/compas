"""
********************************************************************************
compas_hpc
********************************************************************************

.. module:: compas_hpc

This package provides GPU-accelerated and compiled versions of many geometry,
numerical and topological functions and algorithms. The package is built around
`Numba`_, C, `PyCuda`_ and `PyOpenCL`_.

.. _Numba: https://numba.pydata.org/
.. _PyCuda: https://mathema.tician.de/software/pycuda/
.. _PyOpenCL: https://mathema.tician.de/software/pyopencl/


.. warning::

    The functionality of this package is experimental and subject to frequent change.
    For now, don't use it for anything important :)


algorithms
==========

.. autosummary::
    :toctree: generated/
    :nosignatures:

    drx_numba


core
====

cuda
----

.. autosummary::
    :toctree: generated/
    :nosignatures:

    rand_cuda
    device_cuda
    give_cuda
    get_cuda
    ones_cuda
    zeros_cuda
    tile_cuda

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
    vstack_cl


euler
-----

.. autosummary::
    :toctree: generated/
    :nosignatures:

    EulerSSH


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

average
-------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    centroid_points_numba
    centroid_points_xy_numba
    midpoint_point_point_numba
    midpoint_point_point_xy_numba
    center_of_mass_polyline_numba
    center_of_mass_polyline_xy_numba


"""

from .algorithms import *
from .geometry import *
from .core import *
from .linalg import *

from .algorithms import __all__ as a
from .geometry import __all__ as b
from .core import __all__ as c
from .linalg import __all__ as d

__all__ = a + b + c + d
