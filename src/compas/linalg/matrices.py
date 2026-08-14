from typing import Iterable
from typing import Sequence

from .vectors import dot_vectors

# =============================================================================
# general matrices
# =============================================================================


def transpose_matrix(M: Iterable[Iterable[float]]) -> list[list[float]]:
    """Transpose a matrix.

    Parameters
    ----------
    M
        The matrix to be transposed.

    Returns
    -------
    list[list[float]]
        The result matrix.

    """
    return list(map(list, zip(*list(M))))


def multiply_matrices(A: Sequence[Sequence[float]], B: Sequence[Sequence[float]]) -> list[list[float]]:
    r"""Mutliply a matrix with a matrix.

    Parameters
    ----------
    A
        The first matrix.
    B
        The second matrix.

    Returns
    -------
    list[list[float]]
        The result matrix.

    Raises
    ------
    Exception
        If the shapes of the matrices are not compatible.
        If the row length of B is inconsistent.

    Notes
    -----
    This is a pure Python version of the following linear algebra procedure:

    $$
        \mathbf{A} \cdot \mathbf{B} = \mathbf{C}
    $$

    with $\mathbf{A}$ [m x n], $\mathbf{B}$ [n x o], and $\mathbf{C}$ [m x o].

    Examples
    --------
    >>> A = [[2.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, 0.0, 2.0]]
    >>> B = [[2.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, 0.0, 2.0]]
    >>> multiply_matrices(A, B)
    [[4.0, 0.0, 0.0], [0.0, 4.0, 0.0], [0.0, 0.0, 4.0]]

    """
    A = list(A)
    B = list(B)
    n = len(B)  # number of rows in B
    o = len(B[0])  # number of cols in B
    if not all(len(row) == o for row in B):
        raise Exception("Row length in matrix B is inconsistent.")
    if not all([len(row) == n for row in A]):
        raise Exception("Matrix shapes are not compatible.")
    B = list(zip(*list(B)))
    return [[dot_vectors(row, col) for col in B] for row in A]


def multiply_matrix_vector(A: Sequence[Sequence[float]], b: Sequence[float]) -> list[float]:
    r"""Multiply a matrix with a vector.

    Parameters
    ----------
    A
        The matrix.
    b
        The vector.

    Returns
    -------
    list[float]
        The resulting vector.

    Raises
    ------
    Exception
        If not all rows of the matrix have the same length as the vector.

    Notes
    -----
    This is a Python version of the following linear algebra procedure:

    $$
        \mathbf{A} \cdot \mathbf{x} = \mathbf{b}
    $$

    with $\mathbf{A}$ an *m* by *n* matrix, $\mathbf{x}$ a vector of
    length *n*, and $\mathbf{b}$ a vector of length *m*.

    Examples
    --------
    >>> matrix = [[2.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, 0.0, 2.0]]
    >>> vector = [1.0, 2.0, 3.0]
    >>> multiply_matrix_vector(matrix, vector)
    [2.0, 4.0, 6.0]

    """
    n = len(b)
    if not all([len(row) == n for row in A]):
        raise Exception("Matrix shape is not compatible with vector length.")
    return [dot_vectors(row, b) for row in A]


def is_matrix_square(M: Sequence[Sequence[float]]) -> bool:
    """Verify that a matrix is square.

    Parameters
    ----------
    M
        The matrix.

    Returns
    -------
    bool
        True if the length of every row is equal to the number of rows.
        False otherwise.

    Examples
    --------
    >>> M = identity_matrix(4)
    >>> is_matrix_square(M)
    True

    """
    number_of_rows = len(M)
    for row in M:
        if len(row) != number_of_rows:
            return False
    return True


def matrix_minor(M: Sequence[Sequence[float]], i: int, j: int) -> list[list[float]]:
    """Construct the minor corresponding to an element of a matrix.

    Parameters
    ----------
    M
        The matrix.
    i
        Row index of the minor.
    j
        Column index of the minor.

    Returns
    -------
    list[list[float]]
        The minor.

    See Also
    --------
    [`matrix_determinant`][compas.linalg.matrix_determinant]
    [`matrix_inverse`][compas.linalg.matrix_inverse]

    """
    return [list(row[:j]) + list(row[j + 1 :]) for index, row in enumerate(M) if index != i]


def matrix_determinant(M: Sequence[Sequence[float]], check: bool = True) -> float:
    """Calculates the determinant of a square matrix M.

    Parameters
    ----------
    M
        A square matrix of any dimension.
    check
        If True, checks if the matrix is square.

    Raises
    ------
    ValueError
        If the matrix is not square.

    Returns
    -------
    float
        The determinant.

    See Also
    --------
    [`matrix_minor`][compas.linalg.matrix_minor]
    [`matrix_inverse`][compas.linalg.matrix_inverse]

    Examples
    --------
    >>> M = identity_matrix(4)
    >>> matrix_determinant(M)
    1.0

    """
    dim = len(M)

    if check:
        if not is_matrix_square(M):
            raise ValueError("Not a square matrix")

    if dim == 2:
        return M[0][0] * M[1][1] - M[0][1] * M[1][0]

    D = 0
    for c in range(dim):
        D += (-1) ** c * M[0][c] * matrix_determinant(matrix_minor(M, 0, c), check=False)
    return D


def matrix_inverse(M: Sequence[Sequence[float]]) -> list[list[float]]:
    """Calculates the inverse of a square matrix M.

    Parameters
    ----------
    M
        A square matrix of any dimension.

    Returns
    -------
    list[list[float]]
        The inverted matrix.

    Raises
    ------
    ValueError
        If the matrix is not squared
    ValueError
        If the matrix is singular.
    ValueError
        If the matrix is not invertible.

    See Also
    --------
    [`matrix_minor`][compas.linalg.matrix_minor]
    [`matrix_determinant`][compas.linalg.matrix_determinant]

    Examples
    --------
    >>> from compas.geometry import Frame
    >>> f = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
    >>> T = matrix_from_frame(f)
    >>> I = multiply_matrices(T, matrix_inverse(T))
    >>> I2 = identity_matrix(4)
    >>> allclose(I[0], I2[0])
    True
    >>> allclose(I[1], I2[1])
    True
    >>> allclose(I[2], I2[2])
    True
    >>> allclose(I[3], I2[3])
    True

    """
    D = matrix_determinant(M)

    if D == 0:
        raise ValueError("The matrix is singular.")

    if len(M) == 2:
        return [[M[1][1] / D, -1 * M[0][1] / D], [-1 * M[1][0] / D, M[0][0] / D]]

    cofactors = []
    for r in range(len(M)):
        cofactor_row = []
        for c in range(len(M)):
            cofactor_row.append((-1) ** (r + c) * matrix_determinant(matrix_minor(M, r, c)))
        cofactors.append(cofactor_row)

    cofactors = transpose_matrix(cofactors)

    for r in range(len(cofactors)):
        for c in range(len(cofactors)):
            cofactors[r][c] = cofactors[r][c] / D

    return cofactors
