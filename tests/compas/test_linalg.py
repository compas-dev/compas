import numpy as np

from compas.linalg import dof
from compas.linalg import nonpivots
from compas.linalg import normalizerow
from compas.linalg import normrow
from compas.linalg import nullspace
from compas.linalg import pivots
from compas.linalg import rank
from compas.linalg import rot90


def test_matrix_rank_nullspace_and_degrees_of_freedom():
    matrix = [[1, 2, 1], [-2, -3, 1], [3, 5, 0]]

    assert rank(matrix) == 2
    assert nullspace(matrix).shape == (3, 1)
    assert dof(matrix) == (1, 1)
    assert len(dof(matrix, condition=True)) == 3


def test_pivots_and_nonpivots():
    matrix = [[1, 0, 2], [0, 1, 3]]

    assert pivots(matrix) == [0, 1]
    assert nonpivots(matrix) == [2]


def test_row_norms_and_normalization():
    matrix = [[3, 4, 0], [0, 0, 0]]

    assert np.allclose(normrow(matrix), [[5], [0]])
    with np.errstate(invalid="ignore"):
        normalized = normalizerow(matrix)
    assert np.allclose(normalized, [[0.6, 0.8, 0], [0, 0, 0]])


def test_rot90_preserves_vector_lengths():
    vectors = [[1, 0, 0], [0, 2, 0]]
    axes = [[0, 0, 1], [0, 0, 1]]

    rotated = rot90(vectors, axes)

    assert np.allclose(rotated, [[0, 1, 0], [-2, 0, 0]])
    assert np.allclose(normrow(rotated), normrow(vectors))
