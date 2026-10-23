import pytest

from compas.linalg import decompose_matrix
from compas.linalg import matrix_determinant
from compas.linalg import matrix_from_axis_and_angle
from compas.linalg import matrix_from_axis_angle_vector
from compas.linalg import matrix_from_orthogonal_projection
from compas.linalg import matrix_from_parallel_projection
from compas.linalg import matrix_inverse
from compas.linalg import normalize_vector
from compas.linalg import orthonormalize_vectors
from compas.linalg import sum_vectors
from compas.linalg import vector_component
from compas.linalg import vector_standard_deviation
from compas.linalg import vector_variance


def test_vector_variance_and_standard_deviation_have_standard_meanings():
    values = [1.0, 2.0, 3.0, 4.0]

    assert vector_variance(values) == pytest.approx(1.25)
    assert vector_standard_deviation(values) == pytest.approx(1.25**0.5)


def test_orthonormalize_vectors_keeps_negative_residuals():
    basis = orthonormalize_vectors([[-1.0, 0.0, 0.0], [0.0, -2.0, 0.0]])

    assert basis == [[-1.0, 0.0, 0.0], [0.0, -1.0, 0.0]]


def test_sum_vectors_rejects_unknown_axis():
    with pytest.raises(ValueError, match="axis must be 0 or 1"):
        sum_vectors([[1.0, 2.0, 3.0]], axis=2)


def test_zero_and_one_dimensional_determinants_and_inverses():
    assert matrix_determinant([]) == 1.0
    assert matrix_determinant([[4.0]]) == 4.0
    assert matrix_inverse([]) == []
    assert matrix_inverse([[4.0]]) == [[0.25]]


def test_matrix_inverse_uses_the_tolerance_policy_for_singularity():
    with pytest.raises(ValueError, match="singular"):
        matrix_inverse([[1.0, 0.0], [0.0, 1e-12]])


def test_decompose_matrix_requires_a_4x4_matrix():
    with pytest.raises(ValueError, match="4x4"):
        decompose_matrix([[1.0, 0.0], [0.0, 1.0]])


def test_zero_length_vector_boundaries():
    zero = (0.0, 0.0, 0.0)

    assert normalize_vector(zero) is zero
    assert vector_component([1.0, 2.0, 3.0], zero) == [0, 0, 0]

    with pytest.raises(ValueError, match="rotation axis"):
        matrix_from_axis_and_angle(zero, 1.0)

    assert matrix_from_axis_angle_vector(zero) == [
        [1.0, 0.0, 0.0, 0.0],
        [0.0, 1.0, 0.0, 0.0],
        [0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 1.0],
    ]

    with pytest.raises(ValueError, match="plane normal"):
        matrix_from_orthogonal_projection(([0.0, 0.0, 0.0], zero))


def test_parallel_projection_rejects_direction_parallel_to_plane():
    with pytest.raises(ValueError, match="parallel to the plane"):
        matrix_from_parallel_projection(
            ([0.0, 0.0, 0.0], [0.0, 0.0, 1.0]),
            [1.0, 0.0, 0.0],
        )
