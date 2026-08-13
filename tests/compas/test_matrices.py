import numpy as np
from scipy.sparse import spmatrix

from compas.matrices import adjacency_matrix
from compas.matrices import connectivity_matrix
from compas.matrices import degree_matrix
from compas.matrices import face_matrix
from compas.matrices import laplacian_matrix


def test_matrix_return_formats():
    adjacency = [[1], [0]]

    assert isinstance(adjacency_matrix(adjacency, rtype="list"), list)
    assert isinstance(adjacency_matrix(adjacency, rtype="array"), np.ndarray)
    assert isinstance(adjacency_matrix(adjacency, rtype="csr"), spmatrix)
    assert isinstance(adjacency_matrix(adjacency, rtype="csc"), spmatrix)
    assert isinstance(adjacency_matrix(adjacency, rtype="coo"), spmatrix)


def test_graph_matrices():
    adjacency = [[1, 2], [0], [0]]
    edges = [[0, 1], [0, 2]]

    assert np.allclose(adjacency_matrix(adjacency), [[0, 1, 1], [1, 0, 0], [1, 0, 0]])
    assert np.allclose(degree_matrix(adjacency), np.diag([2, 1, 1]))
    assert np.allclose(connectivity_matrix(edges), [[-1, 1, 0], [-1, 0, 1]])
    assert np.allclose(laplacian_matrix(edges), [[2, -1, -1], [-1, 1, 0], [-1, 0, 1]])


def test_normalized_face_matrix():
    matrix = face_matrix([[0, 1, 2], [0, 2, 3]], normalize=True)

    assert np.allclose(matrix, [[1 / 3, 1 / 3, 1 / 3, 0], [1 / 3, 0, 1 / 3, 1 / 3]])
