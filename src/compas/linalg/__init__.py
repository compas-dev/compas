"""Linear algebra utilities for vectors, matrices, and quaternions."""

# The imports below intentionally define the public package-level API.
from .vectors import add_vectors
from .vectors import add_vectors_xy
from .vectors import argmax
from .vectors import argmin
from .transformations import axis_and_angle_from_matrix
from .quaternions import axis_angle_from_quaternion
from .transformations import axis_angle_vector_from_matrix
from .transformations import basis_vectors_from_matrix
from .transformations import compose_matrix
from .vectors import cross_vectors
from .vectors import cross_vectors_xy
from .transformations import decompose_matrix
from .vectors import dehomogenize_vectors
from .vectors import divide_vectors
from .vectors import divide_vectors_xy
from .vectors import dot_vectors
from .vectors import dot_vectors_xy
from .transformations import euler_angles_from_matrix
from .quaternions import euler_angles_from_quaternion
from .vectors import homogenize_vectors
from .transformations import identity_matrix
from .matrices import is_matrix_square
from .vectors import length_vector
from .vectors import length_vector_sqrd
from .vectors import length_vector_sqrd_xy
from .vectors import length_vector_xy
from .matrices import matrix_determinant
from .transformations import matrix_from_axis_and_angle
from .transformations import matrix_from_axis_angle_vector
from .transformations import matrix_from_basis_vectors
from .transformations import matrix_from_change_of_basis
from .transformations import matrix_from_euler_angles
from .transformations import matrix_from_frame
from .transformations import matrix_from_frame_to_frame
from .transformations import matrix_from_orthogonal_projection
from .transformations import matrix_from_parallel_projection
from .transformations import matrix_from_perspective_entries
from .transformations import matrix_from_perspective_projection
from .transformations import matrix_from_quaternion
from .transformations import matrix_from_scale_factors
from .transformations import matrix_from_shear
from .transformations import matrix_from_shear_entries
from .transformations import matrix_from_translation
from .matrices import matrix_inverse
from .matrices import matrix_minor
from .matrices import multiply_matrices
from .matrices import multiply_matrix_vector
from .vectors import multiply_vectors
from .vectors import multiply_vectors_xy
from .vectors import norm_vector
from .vectors import norm_vectors
from .vectors import normalize_vector
from .vectors import normalize_vector_xy
from .vectors import normalize_vectors
from .vectors import normalize_vectors_xy
from .vectors import orthonormalize_vectors
from .vectors import power_vector
from .vectors import power_vectors
from .quaternions import quaternion_from_axis_angle
from .quaternions import quaternion_from_euler_angles
from .transformations import quaternion_from_matrix
from .vectors import scale_vector
from .vectors import scale_vector_xy
from .vectors import scale_vectors
from .vectors import scale_vectors_xy
from .vectors import square_vector
from .vectors import square_vectors
from .vectors import subtract_vectors
from .vectors import subtract_vectors_xy
from .vectors import sum_vectors
from .transformations import translation_from_matrix
from .matrices import transpose_matrix
from .vectors import vector_average
from .vectors import vector_component
from .vectors import vector_component_xy
from .vectors import vector_standard_deviation
from .vectors import vector_variance
from .decompositions import chofactor
from .decompositions import dof
from .decompositions import lufactorized
from .decompositions import nonpivots
from .decompositions import normalizerow
from .decompositions import normrow
from .decompositions import nullspace
from .decompositions import pivots
from .decompositions import rank
from .decompositions import rot90
from .decompositions import rref
from .solvers import solve_with_known
from .solvers import spsolve_with_known
from .decompositions import uvw_lengths
from .operators import adjacency_matrix
from .operators import connectivity_matrix
from .operators import degree_matrix
from .operators import equilibrium_matrix
from .operators import face_matrix
from .operators import laplacian_matrix
from .operators import mass_matrix
from .operators import stiffness_matrix
from .quaternions import quaternion_canonize
from .quaternions import quaternion_conjugate
from .quaternions import quaternion_is_unit
from .quaternions import quaternion_multiply
from .quaternions import quaternion_norm
from .quaternions import quaternion_unitize

__all__ = [
    "add_vectors",
    "add_vectors_xy",
    "argmax",
    "argmin",
    "axis_and_angle_from_matrix",
    "axis_angle_from_quaternion",
    "axis_angle_vector_from_matrix",
    "basis_vectors_from_matrix",
    "compose_matrix",
    "cross_vectors",
    "cross_vectors_xy",
    "decompose_matrix",
    "dehomogenize_vectors",
    "divide_vectors",
    "divide_vectors_xy",
    "dot_vectors",
    "dot_vectors_xy",
    "euler_angles_from_matrix",
    "euler_angles_from_quaternion",
    "homogenize_vectors",
    "identity_matrix",
    "is_matrix_square",
    "length_vector",
    "length_vector_sqrd",
    "length_vector_sqrd_xy",
    "length_vector_xy",
    "matrix_determinant",
    "matrix_from_axis_and_angle",
    "matrix_from_axis_angle_vector",
    "matrix_from_basis_vectors",
    "matrix_from_change_of_basis",
    "matrix_from_euler_angles",
    "matrix_from_frame",
    "matrix_from_frame_to_frame",
    "matrix_from_orthogonal_projection",
    "matrix_from_parallel_projection",
    "matrix_from_perspective_entries",
    "matrix_from_perspective_projection",
    "matrix_from_quaternion",
    "matrix_from_scale_factors",
    "matrix_from_shear",
    "matrix_from_shear_entries",
    "matrix_from_translation",
    "matrix_inverse",
    "matrix_minor",
    "multiply_matrices",
    "multiply_matrix_vector",
    "multiply_vectors",
    "multiply_vectors_xy",
    "norm_vector",
    "norm_vectors",
    "normalize_vector",
    "normalize_vector_xy",
    "normalize_vectors",
    "normalize_vectors_xy",
    "orthonormalize_vectors",
    "power_vector",
    "power_vectors",
    "quaternion_from_axis_angle",
    "quaternion_from_euler_angles",
    "quaternion_from_matrix",
    "scale_vector",
    "scale_vector_xy",
    "scale_vectors",
    "scale_vectors_xy",
    "square_vector",
    "square_vectors",
    "subtract_vectors",
    "subtract_vectors_xy",
    "sum_vectors",
    "translation_from_matrix",
    "transpose_matrix",
    "vector_average",
    "vector_component",
    "vector_component_xy",
    "vector_standard_deviation",
    "vector_variance",
    "chofactor",
    "dof",
    "lufactorized",
    "nonpivots",
    "normalizerow",
    "normrow",
    "nullspace",
    "pivots",
    "rank",
    "rot90",
    "rref",
    "solve_with_known",
    "spsolve_with_known",
    "uvw_lengths",
    "adjacency_matrix",
    "connectivity_matrix",
    "degree_matrix",
    "equilibrium_matrix",
    "face_matrix",
    "laplacian_matrix",
    "mass_matrix",
    "stiffness_matrix",
    "quaternion_canonize",
    "quaternion_conjugate",
    "quaternion_is_unit",
    "quaternion_multiply",
    "quaternion_norm",
    "quaternion_unitize",
]
