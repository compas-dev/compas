from typing import Any
from typing import Literal
from typing import NoReturn
from typing import Sequence
from typing import Union
from typing import cast
from typing import overload

from numpy import abs
from numpy import array
from numpy import asarray
from numpy import tile
from numpy.typing import ArrayLike
from numpy.typing import NDArray
from scipy.sparse import coo_matrix
from scipy.sparse import csc_matrix
from scipy.sparse import csr_matrix
from scipy.sparse import diags
from scipy.sparse import spmatrix
from scipy.sparse import vstack as svstack

MatrixResult = Union[list[list[float]], NDArray[Any], spmatrix]
SparseFormat = Literal["csr", "csc", "coo"]


@overload
def _return_matrix(M: Any, rtype: Literal["list"]) -> list[list[float]]: ...


@overload
def _return_matrix(M: Any, rtype: Literal["array"]) -> NDArray[Any]: ...


@overload
def _return_matrix(M: Any, rtype: Literal["csr"]) -> csr_matrix: ...


@overload
def _return_matrix(M: Any, rtype: Literal["csc"]) -> csc_matrix: ...


@overload
def _return_matrix(M: Any, rtype: Literal["coo"]) -> coo_matrix: ...


@overload
def _return_matrix(M: Any, rtype: str) -> MatrixResult: ...


def _return_matrix(M: Any, rtype: str) -> MatrixResult:
    # SciPy's sparse base type omits conversion methods shared by concrete matrices.
    if rtype == "list":
        return M.toarray().tolist()
    if rtype == "array":
        return M.toarray()
    if rtype == "csr":
        return M.tocsr()
    if rtype == "csc":
        return M.tocsc()
    if rtype == "coo":
        return M.tocoo()
    return M


# ==============================================================================
# adjacency
# ==============================================================================


@overload
def adjacency_matrix(adjacency: Sequence[Sequence[int]], rtype: Literal["array"] = "array") -> NDArray[Any]: ...


@overload
def adjacency_matrix(adjacency: Sequence[Sequence[int]], rtype: Literal["list"]) -> list[list[float]]: ...


@overload
def adjacency_matrix(adjacency: Sequence[Sequence[int]], rtype: SparseFormat) -> spmatrix: ...


@overload
def adjacency_matrix(adjacency: Sequence[Sequence[int]], rtype: str) -> MatrixResult: ...


def adjacency_matrix(adjacency: Sequence[Sequence[int]], rtype: str = "array") -> MatrixResult:
    """Creates a vertex adjacency matrix.

    Parameters
    ----------
    adjacency
        List of lists, vertex adjacency data.
    rtype
        Format of the result.

    Returns
    -------
    list[list[float]] | numpy.typing.NDArray[Any] | scipy.sparse.spmatrix
        Constructed adjacency matrix.

    """
    a = [(1, i, j) for i in range(len(adjacency)) for j in adjacency[i]]
    data, rows, cols = zip(*a)
    A = coo_matrix((data, (rows, cols))).asfptype()
    return _return_matrix(A, rtype)


@overload
def face_matrix(face_vertices: Sequence[Sequence[int]], rtype: Literal["array"] = "array", normalize: bool = False) -> NDArray[Any]: ...


@overload
def face_matrix(face_vertices: Sequence[Sequence[int]], rtype: Literal["list"], normalize: bool = False) -> list[list[float]]: ...


@overload
def face_matrix(face_vertices: Sequence[Sequence[int]], rtype: SparseFormat, normalize: bool = False) -> spmatrix: ...


@overload
def face_matrix(face_vertices: Sequence[Sequence[int]], rtype: str, normalize: bool = False) -> MatrixResult: ...


def face_matrix(face_vertices: Sequence[Sequence[int]], rtype: str = "array", normalize: bool = False) -> MatrixResult:
    """Creates a face-vertex adjacency matrix.

    Parameters
    ----------
    face_vertices
        List of lists, vertices per face.
    rtype
        Format of the result.
    normalize
        If `True`, divide each nonzero entry by the number of vertices in its face.

    Returns
    -------
    list[list[float]] | numpy.typing.NDArray[Any] | scipy.sparse.spmatrix
        Constructed face matrix.

    """
    if normalize:
        f = array([(i, j, 1.0 / len(vertices)) for i, vertices in enumerate(face_vertices) for j in vertices])
    else:
        f = array([(i, j, 1.0) for i, vertices in enumerate(face_vertices) for j in vertices])
    F = coo_matrix((f[:, 2], (f[:, 0].astype(int), f[:, 1].astype(int))))
    return _return_matrix(F, rtype)


# ==============================================================================
# degree
# ==============================================================================


@overload
def degree_matrix(adjacency: Sequence[Sequence[int]], rtype: Literal["array"] = "array") -> NDArray[Any]: ...


@overload
def degree_matrix(adjacency: Sequence[Sequence[int]], rtype: Literal["list"]) -> list[list[float]]: ...


@overload
def degree_matrix(adjacency: Sequence[Sequence[int]], rtype: SparseFormat) -> spmatrix: ...


@overload
def degree_matrix(adjacency: Sequence[Sequence[int]], rtype: str) -> MatrixResult: ...


def degree_matrix(adjacency: Sequence[Sequence[int]], rtype: str = "array") -> MatrixResult:
    """Creates a matrix representing vertex degrees.

    Parameters
    ----------
    adjacency
        List of lists, vertex adjacency data.
    rtype
        Format of the result.

    Returns
    -------
    list[list[float]] | numpy.typing.NDArray[Any] | scipy.sparse.spmatrix
        Constructed degree matrix.

    """
    d = [(len(adjacency[i]), i, i) for i in range(len(adjacency))]
    data, rows, cols = zip(*d)
    D = coo_matrix((data, (rows, cols))).asfptype()
    return _return_matrix(D, rtype)


# ==============================================================================
# connectivity
# ==============================================================================


@overload
def connectivity_matrix(edges: Sequence[Sequence[int]], rtype: Literal["array"] = "array") -> NDArray[Any]: ...


@overload
def connectivity_matrix(edges: Sequence[Sequence[int]], rtype: Literal["list"]) -> list[list[float]]: ...


@overload
def connectivity_matrix(edges: Sequence[Sequence[int]], rtype: Literal["csr"]) -> csr_matrix: ...


@overload
def connectivity_matrix(edges: Sequence[Sequence[int]], rtype: Literal["csc"]) -> csc_matrix: ...


@overload
def connectivity_matrix(edges: Sequence[Sequence[int]], rtype: Literal["coo"]) -> coo_matrix: ...


@overload
def connectivity_matrix(edges: Sequence[Sequence[int]], rtype: str) -> MatrixResult: ...


def connectivity_matrix(edges: Sequence[Sequence[int]], rtype: str = "array") -> MatrixResult:
    r"""Creates a connectivity matrix from a list of vertex index pairs.

    Parameters
    ----------
    edges
        List of lists [[node_i, node_j], [node_k, node_l]].
    rtype
        Format of the result.

    Returns
    -------
    list[list[float]] | numpy.typing.NDArray[Any] | scipy.sparse.spmatrix
        Constructed connectivity matrix.

    Notes
    -----
    The connectivity matrix encodes how edges in a graph are connected
    together. Each row represents an edge and has 1 and -1 inserted into the
    columns for the start and end nodes.

    $$
    \mathbf{C}_{ij} =
    \begin{cases}
        -1 & \text{if edge } i \text{ starts at vertex } j \\
        +1 & \text{if edge } i \text{ ends at vertex } j \\
        0  & \text{otherwise}
    \end{cases}
    $$

    A connectivity matrix is generally sparse and will perform superior
    in numerical calculations as a sparse matrix.

    Examples
    --------
    >>> connectivity_matrix([[0, 1], [0, 2], [0, 3]], rtype="array")
    array([[-1.,  1.,  0.,  0.],
           [-1.,  0.,  1.,  0.],
           [-1.,  0.,  0.,  1.]])

    """
    m = len(edges)
    data = array([-1] * m + [1] * m)
    rows = array(list(range(m)) + list(range(m)))
    cols = array([edge[0] for edge in edges] + [edge[1] for edge in edges])
    C = coo_matrix((data, (rows, cols))).asfptype()
    return _return_matrix(C, rtype)


# ==============================================================================
# laplacian
# ==============================================================================


# change this to a procedural approach
# constructing (fundamental) matrices should not involve matrix operations
@overload
def laplacian_matrix(edges: Sequence[Sequence[int]], normalize: bool = False, rtype: Literal["array"] = "array") -> NDArray[Any]: ...


@overload
def laplacian_matrix(edges: Sequence[Sequence[int]], normalize: bool, rtype: Literal["list"]) -> list[list[float]]: ...


@overload
def laplacian_matrix(edges: Sequence[Sequence[int]], normalize: bool, rtype: SparseFormat) -> spmatrix: ...


@overload
def laplacian_matrix(edges: Sequence[Sequence[int]], normalize: bool, rtype: str) -> MatrixResult: ...


def laplacian_matrix(edges: Sequence[Sequence[int]], normalize: bool = False, rtype: str = "array") -> MatrixResult:
    r"""Creates a laplacian matrix from a list of edge topologies.

    Parameters
    ----------
    edges
        List of lists [[node_i, node_j], [node_k, node_l]].
    normalize
        If `True`, normalize each row by its diagonal entry.
    rtype
        Format of the result.

    Returns
    -------
    list[list[float]] | numpy.typing.NDArray[Any] | scipy.sparse.spmatrix
        Constructed Laplacian matrix.

    Notes
    -----
    The laplacian matrix is defined as

    $$
    \mathbf{L} = \mathbf{C}^{\mathrm{T}} \mathbf{C}
    $$

    The current implementation only supports umbrella weights.

    Examples
    --------
    >>> laplacian_matrix([[0, 1], [0, 2], [0, 3]], rtype="array")
    array([[ 3., -1., -1., -1.],
           [-1.,  1.,  0.,  0.],
           [-1.,  0.,  1.,  0.],
           [-1.,  0.,  0.,  1.]])

    """
    C = connectivity_matrix(edges, rtype="csr")
    L = C.transpose().dot(C)
    if normalize:
        L = L / L.diagonal().reshape((-1, 1))
        L = csr_matrix(L)
    return _return_matrix(L, rtype)


# ==============================================================================
# structural
# ==============================================================================


@overload
def equilibrium_matrix(C: ArrayLike, xyz: ArrayLike, free: Sequence[int], rtype: Literal["array"] = "array") -> NDArray[Any]: ...


@overload
def equilibrium_matrix(C: ArrayLike, xyz: ArrayLike, free: Sequence[int], rtype: Literal["list"]) -> list[list[float]]: ...


@overload
def equilibrium_matrix(C: ArrayLike, xyz: ArrayLike, free: Sequence[int], rtype: SparseFormat) -> spmatrix: ...


@overload
def equilibrium_matrix(C: ArrayLike, xyz: ArrayLike, free: Sequence[int], rtype: str) -> MatrixResult: ...


def equilibrium_matrix(C: ArrayLike, xyz: ArrayLike, free: Sequence[int], rtype: str = "array") -> MatrixResult:
    r"""Construct the equilibrium matrix of a structural system.

    Parameters
    ----------
    C
        Connectivity matrix (m x n).
    xyz
        Array of vertex coordinates (n x 3).
    free
        The index values of the free vertices.
    rtype
        Format of the result.

    Returns
    -------
    list[list[float]] | numpy.typing.NDArray[Any] | scipy.sparse.spmatrix
        Constructed equilibrium matrix.

    Notes
    -----
    Analysis of the equilibrium matrix reveals some of the properties of the
    structural system, its size is (2ni x m) where ni is the number of free or
    internal nodes. It is calculated by

    $$
    \mathbf{E}
    =
    \left[
        \begin{array}{c}
            \mathbf{C}^{\mathrm{T}}_{\mathrm{i}}\mathbf{U} \\[0.3em]
            \hline \\[-0.7em]
            \mathbf{C}^{\mathrm{T}}_{\mathrm{i}}\mathbf{V}
        \end{array}
    \right].
    $$

    The matrix of vertex coordinates is vectorised to speed up the
    calculations.

    Examples
    --------
    >>> C = connectivity_matrix([[0, 1], [0, 2], [0, 3]])
    >>> xyz = [[0, 0, 1], [0, 1, 0], [-1, -1, 0], [1, -1, 0]]
    >>> equilibrium_matrix(C, xyz, [0], rtype="array")
    array([[ 0.,  1., -1.],
           [-1.,  1.,  1.]])

    """
    xyz = asarray(xyz, dtype=float)
    # Keep the concrete sparse matrix separate from the general ArrayLike input.
    C_ = csr_matrix(C)
    xy = xyz[:, :2]
    uv = C_.dot(xy)
    # SciPy's overload does not accept the supported sequence-of-offsets form.
    offsets = cast(Any, [0])
    U = diags([uv[:, 0].flatten()], offsets)
    V = diags([uv[:, 1].flatten()], offsets)
    Ct = C_.transpose()
    Cti = Ct[free, :]
    E = svstack((Cti.dot(U), Cti.dot(V)))
    return _return_matrix(E, rtype)


def mass_matrix(
    Ct: spmatrix,
    ks: NDArray[Any],
    q: Union[NDArray[Any], float] = 0,
    c: float = 1,
    tiled: bool = True,
) -> NDArray[Any]:
    r"""Creates a graph's nodal mass matrix.

    Parameters
    ----------
    Ct
        Sparse transpose of the connectivity matrix (n x m).
    ks
        Vector of member EA / L (m x 1).
    q
        Vector of member force densities (m x 1).
    c
        Convergence factor.
    tiled
        Whether to tile horizontally by 3 for x, y, z.

    Returns
    -------
    numpy.typing.NDArray[Any]
        Mass matrix, either (m x 1) or (m x 3).

    Notes
    -----
    The mass matrix is defined as the sum of the member axial stiffnesses
    (inline) of the elements connected to each node, plus the force density.
    The force density ensures a non-zero value in form-finding/pre-stress
    modelling where E=0.

    $$
    \mathbf{m} =
    |\mathbf{C}^\mathrm{T}|
    (\mathbf{E} \circ \mathbf{A} \oslash \mathbf{l} + \mathbf{f} \oslash \mathbf{l})
    $$

    """
    # SciPy's sparse base type omits the NumPy ufunc support of concrete matrices.
    m = c * abs(cast(Any, Ct)).dot(ks + q)
    if tiled:
        return tile(m.reshape((-1, 1)), (1, 3))
    return m


def stiffness_matrix() -> NoReturn:
    """Raise because stiffness matrix construction is not implemented.

    Raises
    ------
    NotImplementedError
        Always.

    """
    raise NotImplementedError
