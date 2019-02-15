from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
import compas

from functools import wraps

try:
    from numpy import array
    from numpy import asarray
    from numpy import atleast_2d
    from numpy import nan_to_num
    from numpy import nonzero
    from numpy import seterr
    from numpy import sum
    from numpy import zeros
    from numpy import absolute
    from numpy.linalg import cond

    from scipy import cross
    from scipy.linalg import cho_factor
    from scipy.linalg import cho_solve
    from scipy.linalg import lstsq
    from scipy.linalg import lu
    from scipy.linalg import qr
    from scipy.linalg import solve
    from scipy.linalg import svd
    from scipy.io import loadmat
    from scipy.io import savemat
    from scipy.sparse.linalg import factorized
    from scipy.sparse.linalg import spsolve

except ImportError:
    compas.raise_if_not_ironpython()

else:
    old_settings = seterr(all='ignore')

try:
    from subprocess import Popen
except ImportError:
    compas.raise_if_not_ironpython()


__all__ = [
    'nullspace',
    'rank',
    'dof',
    'pivots',
    'nonpivots',
    'rref',
    'rref_sympy',
    'rref_matlab',
    'uvw_lengths',
    'normrow',
    'normalizerow',
    'rot90',
    'solve_with_known',
    'spsolve_with_known',
    'chofactor',
    'lufactorized'
]


# ==============================================================================
# Fundamentals
# ==============================================================================

def nullspace(A, tol=0.001):
    r"""Calculates the nullspace of the input matrix A.

    Parameters
    ----------
    A : array-like
        Matrix A represented as an array or list.
    tol : float
        Tolerance.

    Returns
    -------
    array
        Null(A).

    Notes
    -----
    The nullspace is the set of vector solutions to the equation

    .. math::

        \mathbf{A} \mathbf{x} = 0

    where 0 is a vector of zeros.

    When determining the nullspace using SVD decomposition (A = U S Vh),
    the right-singular vectors (rows of Vh or columns of V) corresponding to
    vanishing singular values of A, span the nullspace of A.

    Examples
    --------
    >>> nullspace(array([[2, 3, 5], [-4, 2, 3]]))
    [[-0.03273859]
     [-0.85120177]
     [ 0.52381647]]

    """
    A = atleast_2d(asarray(A, dtype=float))
    u, s, vh = svd(A, compute_uv=True)
    tol = s[0] * tol
    r = (s >= tol).sum()
    # nullspace
    # ---------
    # if A is m x n
    # the last (n - r) columns of v (or the last n - r rows of vh)
    null = vh[r:].conj().T
    return null


def rank(A, tol=0.001):
    r"""Calculates the rank of the input matrix A.

    Parameters
    ----------
    A : array-like
        Matrix A represented as an array or list.
    tol : float
        Tolerance.

    Returns
    -------
    int
        rank(A)

    Notes
    -----
    The rank of a matrix is the maximum number of linearly independent rows in
    a matrix. Note that the row rank is equal to the column rank of the matrix.

    Examples
    --------
    >>> rank([[1, 2, 1], [-2, -3, 1], [3, 5, 0]])
    2

    """
    A = atleast_2d(asarray(A, dtype=float))
    s = svd(A, compute_uv=False)
    tol = s[0] * tol
    r = (s >= tol).sum()
    return r


def dof(A, tol=0.001, condition=False):
    r"""Returns the degrees-of-freedom of the input matrix A.

    Parameters
    ----------
    A : array-like
        Matrix A represented as an array or list.
    tol : float
        Tolerance.
    condition : bool
        Return the condition number of the matrix.

    Returns
    -------
    int
        Column degrees-of-freedom.
    int
        Row degrees-of-freedom.
    float
        Condition number, if ``condition`` is ``True``.

    Notes
    -----
    The degrees-of-freedom are the number of columns and rows minus the rank.

    Examples
    --------
    >>> dof([[2, -1, 3,], [1, 0, 1], [0, 2, -1], [1, 1, 4]], condition=True)
    (0, 1, 5.073597)

    """
    A = atleast_2d(asarray(A, dtype=float))
    r = rank(A, tol=tol)
    k = A.shape[1] - r
    m = A.shape[0] - r
    if condition:
        c = cond(A)
        return k, m, c
    return k, m


def pivots(U, tol=None):
    r"""Identify the pivots of input matrix U.

    Parameters
    ----------
    U : array-like
        Matrix U represented as an array or list.

    Returns
    -------
    list
        Pivot column indices.

    Notes
    -----
    The pivots are the non-zero leading coefficients of each row.

    Examples
    --------
    >>> A = [[1, 0, 1, 3], [2, 3, 4, 7], [-1, -3, -3, -4]]
    >>> n = rref(A, algo='sympy')
    >>> pivots(n)
    [0, 1]

    """
    if tol is None:
        tol = sys.float_info.epsilon
    U = atleast_2d(array(U, dtype=float))
    U[absolute(U) < tol] = 0.0
    pivots = []
    for row in U:
        cols = nonzero(row)[0]
        if len(cols):
            pivots.append(cols[0])
    return pivots


def nonpivots(U, tol=None):
    r"""Identify the non-pivots of input matrix U.

    Parameters
    ----------
    U : array-like
        Matrix U represented as an array or list.

    Returns
    -------
    list
        Non-pivot column indices.

    Notes
    -----
    The non-pivots are where there are no non-zero leading coefficients in a row.

    Examples
    --------
    >>> A = [[1, 0, 1, 3], [2, 3, 4, 7], [-1, -3, -3, -4]]
    >>> n = rref(A, algo='sympy')
    >>> nonpivots(n)
    [2, 3]

    """
    U = atleast_2d(asarray(U, dtype=float))
    cols = pivots(U, tol=tol)
    return list(set(range(U.shape[1])) - set(cols))


def rref(A, tol=None):
    r"""Reduced row-echelon form of matrix A.

    Parameters
    ----------
    A : array-like
        Matrix A represented as an array or list.
    algo : str
        Algorithm to use: 'qr', 'sympy', 'matlab'.
    tol : float
        Tolerance.

    Returns
    -------
    array
        RREF of A.

    Notes
    -----
    A matrix is in reduced row-echelon form after Gauss-Jordan elimination, the
    result is independent of the method/algorithm used.

    Examples
    --------
    >>> A = [[1, 0, 1, 3], [2, 3, 4, 7], [-1, -3, -3, -4]]
    >>> n = rref(A, algo='sympy')
    >>> array(n)
    [[1.0 0 1.0 3.0]
     [0 1.0 0.667 0.333]
     [0 0 0 0]]

    """
    A = atleast_2d(asarray(A, dtype=float))

    # do qr with column pivoting
    # to have non-decreasing absolute values on the diagonal of R
    # column pivoting ensures that the largest absolute value is used
    # as leading element
    _, U = qr(A)
    lead_pos = 0
    num_rows, num_cols = U.shape
    for r in range(num_rows):
        if lead_pos >= num_cols:
            return
        i = r
        # find a nonzero lead in column lead_pos
        while U[i][lead_pos] == 0:
            i += 1
            if i == num_rows:
                i = r
                lead_pos += 1
                if lead_pos == num_cols:
                    return
        # swap the row with the nonzero lead with the current row
        U[[i, r]] = U[[r, i]]
        # "normalize" the values of the row
        lead_val = U[r][lead_pos]
        U[r] = U[r] / lead_val
        # make sure all other column values are zero
        for i in range(num_rows):
            if i != r:
                lead_val = U[i][lead_pos]
                U[i] = U[i] - lead_val * U[r]
        # go to the next column
        lead_pos += 1
    return U


def rref_sympy(A, tol=None):
    r"""Reduced row-echelon form of matrix A.

    Parameters
    ----------
    A : array-like
        Matrix A represented as an array or list.
    tol : float
        Tolerance.

    Returns
    -------
    array
        RREF of A.

    Notes
    -----
    A matrix is in reduced row-echelon form after Gauss-Jordan elimination, the
    result is independent of the method/algorithm used.

    Examples
    --------
    >>> A = [[1, 0, 1, 3], [2, 3, 4, 7], [-1, -3, -3, -4]]
    >>> n = rref(A, algo='sympy')
    >>> array(n)
    [[1.0 0 1.0 3.0]
     [0 1.0 0.667 0.333]
     [0 0 0 0]]

    """
    import sympy

    A = atleast_2d(asarray(A, dtype=float))
    return sympy.Matrix(A).rref()[0].tolist()


def rref_matlab(A, ifile, ofile, tol=None):
    r"""Reduced row-echelon form of matrix A.

    Parameters
    ----------
    A : array-like
        Matrix A represented as an array or list.
    tol : float
        Tolerance.

    Returns
    -------
    array
        RREF of A.

    Notes
    -----
    A matrix is in reduced row-echelon form after Gauss-Jordan elimination, the
    result is independent of the method/algorithm used.

    Examples
    --------
    >>> A = [[1, 0, 1, 3], [2, 3, 4, 7], [-1, -3, -3, -4]]
    >>> n = rref(A, algo='sympy')
    >>> array(n)
    [[1.0 0 1.0 3.0]
     [0 1.0 0.667 0.333]
     [0 0 0 0]]

    """
    A = atleast_2d(asarray(A, dtype=float))

    idict = {'A': A}
    savemat(ifile, idict)

    matlab = ['matlab']
    if compas.is_windows():
        options = ['-nosplash', '-wait', '-r']
    else:
        options = ['-nosplash', '-r']
    command = ["load('{0}');[R, jb]=rref(A);save('{1}');exit;".format(ifile, ofile)]

    p = Popen(matlab + options + command)
    stdout, stderr = p.communicate()

    odict = loadmat(ofile)
    return odict['R']


# ==============================================================================
# Factorisation
# ==============================================================================

class Memoized:
    """"""
    def __init__(self, f):
        self.f = f
        self.memo = {}

    def __call__(self, *args):
        key = args[-1]
        if key in self.memo:
            return self.memo[key]
        self.memo[key] = res = self.f(args[0])
        return res


def memoize(f):
    memo = {}

    @wraps(f)
    def wrapper(*args):
        key = args[-1]
        if key in memo:
            return memo[key]
        memo[key] = res = f(args[0])
        return res

    return wrapper


def _chofactor(A):
    r"""Returns the Cholesky factorisation/decomposition matrix.

    Parameters
    ----------
    A : array
        Matrix A represented as an (m x m) array.

    Returns
    -------
    array
        Matrix (m x m) with upper/lower triangle containing Cholesky factor of A.

    Notes
    -----
    The Cholesky factorisation decomposes a Hermitian positive-definite matrix
    into the product of a lower/upper triangular matrix and its transpose.

    .. math::

        \mathbf{A} = \mathbf{L} \mathbf{L}^{\mathrm{T}}

    Examples
    --------
    >>> _chofactor(array([[25, 15, -5], [15, 18, 0], [-5, 0, 11]]))
    (array([[  5.,   3.,  -1.],
            [ 15.,   3.,   1.],
            [ -5.,   0.,   3.]]), False)

    """
    return cho_factor(A)


def _lufactorized(A):
    r"""Return a function for solving a sparse linear system (LU decomposition).

    Parameters
    ----------
    A : array
        Matrix A represented as an (m x n) array.

    Returns
    -------
    callable
        Function to solve linear system with input matrix (n x 1).

    Notes
    -----
    LU decomposition factors a matrix as the product of a lower triangular and
    an upper triangular matrix L and U.

    .. math::

        \mathbf{A} = \mathbf{L} \mathbf{U}

    Examples
    --------
    >>> fn = _lufactorized(array([[3, 2, -1], [2, -2, 4], [-1, 0.5, -1]]))
    >>> fn(array([1, -2, 0]))
    array([ 1., -2., -2.])

    """
    return factorized(A)


chofactor = memoize(_chofactor)
lufactorized = memoize(_lufactorized)


# ------------------------------------------------------------------------------
# Geometry
# ------------------------------------------------------------------------------

def uvw_lengths(C, X):
    r"""Calculates the lengths and co-ordinate differences.

    Parameters
    ----------
    C : sparse
        Connectivity matrix (m x n).
    X : array
        Co-ordinates of vertices/points (n x 3).

    Returns
    -------
    array
        Vectors of co-ordinate differences in x, y and z (m x 3).
    array
        Lengths of members (m x 1).

    Examples
    --------
    >>> C = connectivity_matrix([[0, 1], [1, 2]], 'csr')
    >>> X = array([[0, 0, 0], [1, 1, 0], [0, 0, 1]])
    >>> uvw
    array([[ 1,  1,  0],
           [-1, -1,  1]])
    >>> l
    array([[ 1.41421356],
           [ 1.73205081]])

    """
    uvw = C.dot(X)
    return uvw, normrow(uvw)


def normrow(A):
    """Calculates the 2-norm of each row of matrix A.

    Parameters
    ----------
    A : array
        Matrix A represented as an (m x n) array.

    Returns
    -------
    array
        Column vector (m x 1) of values.

    Notes
    -----
    The calculation is the Euclidean 2-norm, i.e. the square root of the sum
    of the squares of the elements in each row, this equates to the "length" of
    the m row vectors.

    Examples
    --------
    >>> normrow(array([[2, -1, 3,], [1, 0, 1], [0, 2, -1]]))
    [[ 3.74165739]
     [ 1.41421356]
     [ 2.23606798]]

    """
    A = atleast_2d(asarray(A, dtype=float))
    return (sum(A ** 2, axis=1) ** 0.5).reshape((-1, 1))


def normalizerow(A, do_nan_to_num=True):
    """Normalise the rows of matrix A.

    Parameters
    ----------
    A : array
        Matrix A represented as an (m x n) array.
    do_nan_to_num : bool
        Convert NaNs and INF to numbers, default=True.

    Returns
    -------
    array
        Matrix of normalized row vectors (m x n).

    Notes
    -----
    Normalises the row vectors of A by the normrows, i.e. creates an array of
    vectors where the row vectors have length of unity.

    Tiling is not necessary, because of NumPy's broadcasting behaviour.

    Examples
    --------
    >>> normalizerow(array([[2, -1, 3,], [1, 0, 1], [0, 2, -1]]))
    array([[ 0.53452248, -0.26726124,  0.80178373],
           [ 0.70710678,  0.        ,  0.70710678],
           [ 0.        ,  0.89442719, -0.4472136 ]])

    """
    if do_nan_to_num:
        return nan_to_num(A / normrow(A))
    else:
        return A / normrow(A)


def rot90(vectors, axes):
    """Rotate an array of vectors through 90 degrees around an array of axes.

    Parameters
    ----------
    vectors : array
        An array of row vectors (m x 3).
    axes : array
        An array of axes (m x 3).

    Returns
    -------
    array
        Matrix of row vectors (m x 3).

    Notes
    -----
    Computes the cross product of each row vector with its corresponding axis,
    and then rescales the resulting normal vectors to match the length of the
    original row vectors.

    Examples
    --------
    >>> vectors = array([[2, 1, 3], [2, 6, 8]])
    >>> axes = array([[7, 0, 1], [4, 4, 2]])
    >>> rot90(vectors, axes)
    [[-0.18456235 -3.50668461  1.29193644]
     [ 5.3748385  -7.5247739   4.2998708 ]]

    """
    return normalizerow(cross(axes, vectors)) * normrow(vectors)


# ==============================================================================
# Solving
# ==============================================================================

def solve_with_known(A, b, x, known):
    r"""Solve a system of linear equations with part of solution known.

    Parameters
    ----------
    A : array
        Coefficient matrix represented as an (m x n) array.
    b : array
        Right-hand-side represented as an (m x 1) array.
    x : array
        Unknowns/knowns represented as an (n x 1) array.
    known : list
        The indices of the known elements of ``x``.

    Returns
    -------
    array: (n x 1) vector solution.

    Notes
    -----
    Computes the solution of the system of linear equations.

    .. math::

        \mathbf{A} \mathbf{x} = \mathbf{b}

    Examples
    --------
    >>> A = array([[2, 1, 3], [2, 6, 8], [6, 8, 18]])
    >>> b = array([[1], [3], [5]])
    >>> x = array([[0.3], [0], [0]])
    >>> solve_with_known(A, b, x, [0])
    array([ 0.3, 0.4, 0.0])

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


def spsolve_with_known(A, b, x, known):
    r"""Solve (sparse) a system of linear equations with part of solution known.

    Parameters
    ----------
    A : array
        Coefficient matrix (sparse) represented as an (m x n) array.
    b : array
        Right-hand-side represented as an (m x 1) array.
    x : array
        Unknowns/knowns represented as an (n x 1) array.
    known : list
        The indices of the known elements of ``x``.

    Returns
    -------
    array
        (n x 1) vector solution.

    Notes
    -----
    Computes the solution (using spsolve) of the system of linear equations.

    .. math::

        \mathbf{A} \mathbf{x} = \mathbf{b}

    Same function as solve_with_known, but for sparse matrix A.

    Examples
    --------
    >>> A = array([[2, 1, 3], [2, 6, 8], [6, 8, 18]])
    >>> b = array([[1], [3], [5]])
    >>> x = array([[0.3], [0], [0]])
    >>> solve_with_known(A, b, x, [0])
    array([ 0.3, 0.4, 0.0])

    """
    unknown = list(set(range(x.shape[0])) - set(known))
    A11 = A[unknown, :][:, unknown]
    A12 = A[unknown, :][:, known]
    b = b[unknown] - A12.dot(x[known])
    x[unknown] = spsolve(A11, b)
    return x


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    import numpy as np

    np.set_printoptions(precision=3, threshold=10000, linewidth=1000)

    E = array([[2, 3, 5], [-4, 2, 3]], dtype=float)

    null = nullspace(E)

    assert np.allclose(zeros((E.shape[0], 1)), E.dot(null), atol=1e-6), 'E.dot(null) not aproximately zero'

    m, n = E.shape
    s, t = null.shape

    print(m, n)
    print(s, t)

    assert n == s, 'num_cols of E should be equal to num_rows of null(E)'

    print(rank(E))
    print(dof(E))

    print(len(pivots(rref(E))))
    print(len(nonpivots(rref(E))))

    # ifile = './data/ifile.mat'
    # ofile = './data/ofile.mat'

    # with open(ifile, 'wb+') as fp: pass
    # with open(ofile, 'wb+') as fp: pass

    # print nonpivots(rref(E, algo='qr'))
    # print nonpivots(rref(E, algo='sympy'))
    # print nonpivots(rref(E, algo='matlab', ifile=ifile, ofile=ofile))
