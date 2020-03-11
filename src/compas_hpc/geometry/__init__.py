"""
********************************************************************************
compas_hpc.geometry
********************************************************************************

.. currentmodule:: compas_hpc.geometry

Numba
=====

.. autosummary::
    :toctree: generated/
    :nosignatures:

    add_vectors_numba
    add_vectors_xy_numba
    center_of_mass_polyline_numba
    center_of_mass_polyline_xy_numba
    center_of_mass_polyhedron_numba
    centroid_points_numba
    centroid_points_xy_numba
    circle_from_points_numba
    circle_from_points_xy_numba
    closest_distance_field_numba
    cross_vectors_numba
    cross_vectors_xy_numba
    distance_matrix_numba
    divide_vectors_numba
    divide_vectors_xy_numba
    dot_vectors_numba
    dot_vectors_xy_numba
    length_vector_numba
    length_vector_xy_numba
    length_vector_sqrd_numba
    length_vector_sqrd_xy_numba
    midpoint_point_point_numba
    midpoint_point_point_xy_numba
    multiply_vectors_numba
    multiply_vectors_xy_numba
    norm_vector_numba
    norm_vectors_numba
    normalize_vector_numba
    normalize_vector_xy_numba
    normalize_vectors_numba
    normalize_vectors_xy_numba
    orthonormalize_vectors_numba
    plane_from_points_numba
    power_vector_numba
    power_vectors_numba
    scale_vector_numba
    scale_vector_xy_numba
    scale_vectors_numba
    scale_vectors_xy_numba
    square_vector_numba
    square_vectors_numba
    sum_vectors_numba
    subtract_vectors_numba
    subtract_vectors_xy_numba
    vector_component_numba
    vector_component_xy_numba

PyCUDA
======

.. autosummary::
    :toctree: generated/
    :nosignatures:

PyOpenCL
========

.. autosummary::
    :toctree: generated/
    :nosignatures:

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from .basic_numba import *  # noqa: F401 F403
from .average_numba import *  # noqa: F401 F403
from .spatial_numba import *  # noqa: F401 F403

__all__ = [name for name in dir() if not name.startswith('_')]
