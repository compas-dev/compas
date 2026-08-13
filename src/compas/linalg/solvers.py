import sys
from typing import Any
from typing import Sequence

from numpy.linalg import cond
from numpy.typing import NDArray
from scipy.linalg import cho_factor
from scipy.linalg import cho_solve
from scipy.linalg import lstsq
from scipy.sparse.linalg import spsolve

# ==============================================================================
# Solving
# ==============================================================================


def solve_with_known(A: NDArray[Any], b: NDArray[Any], x: NDArray[Any], known: Sequence[int]) -> NDArray[Any]:
    r"""Solve a system of linear equations with part of solution known.

    Parameters
    ----------
    A
        Coefficient matrix represented as an (m x n) array.
    b
        Right-hand-side represented as an (m x 1) array.
    x
        Unknowns/knowns represented as an (n x 1) array.
    known
        The indices of the known elements of `x`.

    Returns
    -------
    NDArray[Any]
        The solution vector with shape `(n, 1)`.

    Notes
    -----
    Computes the solution of the system of linear equations.

    $$
    \mathbf{A} \mathbf{x} = \mathbf{b}
    $$

    """
    eps = 1 / sys.float_info.epsilon
    unknown = list(set(range(x.shape[0])) - set(known))
    A11 = A[unknown, :][:, unknown]
    A12 = A[unknown, :][:, known]
    b = b[unknown] - A12.dot(x[known])
    if cond(A11) < eps:
        Y = cho_solve(cho_factor(A11), b)
        x[unknown] = Y
        return x
    Y = lstsq(A11, b)
    x[unknown] = Y[0]
    return x


def spsolve_with_known(A: Any, b: NDArray[Any], x: NDArray[Any], known: Sequence[int]) -> NDArray[Any]:
    r"""Solve (sparse) a system of linear equations with part of solution known.

    Parameters
    ----------
    A
        Coefficient matrix (sparse) represented as an (m x n) array.
    b
        Right-hand-side represented as an (m x 1) array.
    x
        Unknowns/knowns represented as an (n x 1) array.
    known
        The indices of the known elements of `x`.

    Returns
    -------
    NDArray[Any]
        (n x 1) vector solution.

    Notes
    -----
    Computes the solution (using spsolve) of the system of linear equations.

    $$
    \mathbf{A} \mathbf{x} = \mathbf{b}
    $$

    Same function as solve_with_known, but for sparse matrix A.

    Examples
    --------
    >>> A = array([[2, 1, 3], [2, 6, 8], [6, 8, 18]])
    >>> b = array([[1], [3], [5]])
    >>> x = array([[0.3], [0], [0]])
    >>> x = solve_with_known(A, b, x, [0])
    >>> allclose(x, array([[0.3], [0.4], [0.0]]))
    True

    """
    unknown = list(set(range(x.shape[0])) - set(known))
    A11 = A[unknown, :][:, unknown]
    A12 = A[unknown, :][:, known]
    b = b[unknown] - A12.dot(x[known])
    x[unknown] = spsolve(A11, b)
    return x
