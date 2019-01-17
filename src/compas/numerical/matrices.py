from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas

try:
    from numpy import abs
    from numpy import array
    from numpy import asarray
    from numpy import tile

    from scipy.sparse import coo_matrix
    from scipy.sparse import csr_matrix
    from scipy.sparse import diags
    from scipy.sparse import vstack as svstack

except ImportError:
    compas.raise_if_not_ironpython()


__all__ = [
    'adjacency_matrix',
    'degree_matrix',
    'connectivity_matrix',
    'laplacian_matrix',
    'face_matrix',
    'mass_matrix',
    'stiffness_matrix',
    'equilibrium_matrix',
]


def _return_matrix(M, rtype):
    if rtype == 'list':
        return M.toarray().tolist()
    if rtype == 'array':
        return M.toarray()
    if rtype == 'csr':
        return M.tocsr()
    if rtype == 'csc':
        return M.tocsc()
    if rtype == 'coo':
        return M.tocoo()
    return M


# ==============================================================================
# adjacency
# ==============================================================================

def adjacency_matrix(adjacency, rtype='array'):
    """Creates a vertex adjacency matrix.

    Parameters
    ----------
    adjacency : list
        List of lists, vertex adjacency data.
    rtype : {'array', 'csc', 'csr', 'coo', 'list'}
        Format of the result.

    Returns
    -------
    array-like
        Constructed adjacency matrix.

    """
    a = [(1, i, j) for i in range(len(adjacency)) for j in adjacency[i]]
    data, rows, cols = zip(*a)
    A = coo_matrix((data, (rows, cols))).asfptype()
    return _return_matrix(A, rtype)


def face_matrix(face_vertices, rtype='array', normalize=False):
    """Creates a face-vertex adjacency matrix.

    Parameters
    ----------
    face_vertices : list
        List of lists, vertices per face.
    rtype : {'array', 'csc', 'csr', 'coo', 'list'}
        Format of the result.

    Returns
    -------
    array-like
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

def degree_matrix(adjacency, rtype='array'):
    """Creates a matrix representing vertex degrees.

    Parameters
    ----------
    adjacency : list
        List of lists, vertex adjacency data.
    rtype : {'array', 'csc', 'csr', 'coo', 'list'}
        Format of the result.

    Returns
    -------
    array-like
        Constructed degree matrix.

    """
    d = [(len(adjacency[i]), i, i) for i in range(len(adjacency))]
    data, rows, cols = zip(*d)
    D = coo_matrix((data, (rows, cols))).asfptype()
    return _return_matrix(D, rtype)


# ==============================================================================
# connectivity
# ==============================================================================

def connectivity_matrix(edges, rtype='array'):
    r"""Creates a connectivity matrix from a list of vertex index pairs.

    Parameters
    ----------
    edges : list
        List of lists [[node_i, node_j], [node_k, node_l]].
    rtype : {'array', 'csc', 'csr', 'coo', 'list'}
        Format of the result.

    Returns
    -------
    array-like
        Constructed connectivity matrix.

    Notes
    -----
    The connectivity matrix encodes how edges in a network are connected
    together. Each row represents an edge and has 1 and -1 inserted into the
    columns for the start and end nodes.

    .. math::

        \mathbf{C}_{ij} =
        \cases{
            -1 & if edge i starts at vertex j \cr
            +1 & if edge i ends at vertex j \cr
            0  & otherwise
        }

    A connectivity matrix is generally sparse and will perform superior
    in numerical calculations as a sparse matrix.

    Examples
    --------
    >>> connectivity_matrix([[0, 1], [0, 2], [0, 3]], rtype='array')
    [[-1  1  0  0]
     [-1  0  1  0]
     [-1  0  0  1]]

    """
    m    = len(edges)
    data = array([-1] * m + [1] * m)
    rows = array(list(range(m)) + list(range(m)))
    cols = array([edge[0] for edge in edges] + [edge[1] for edge in edges])
    C    = coo_matrix((data, (rows, cols))).asfptype()
    return _return_matrix(C, rtype)


# ==============================================================================
# laplacian
# ==============================================================================

# change this to a procedural approach
# constructing (fundamental) matrices should not involve matrix operations
def laplacian_matrix(edges, normalize=False, rtype='array'):
    r"""Creates a laplacian matrix from a list of edge topologies.

    Parameters
    ----------
    edges : list
        List of lists [[node_i, node_j], [node_k, node_l]].
    rtype : {'array', 'csc', 'csr', 'coo', 'list'}
        Format of the result.

    Returns
    -------
    array-like
        Constructed Laplacian matrix.

    Notes
    -----
    The laplacian matrix is defined as

    .. math::

        \mathbf{L} = \mathbf{C} ^ \mathrm{T} \mathbf{C}

    The current implementation only supports umbrella weights.

    Examples
    --------
    >>> laplacian_matrix([[0, 1], [0, 2], [0, 3]], rtype='array')
    [[ 3 -1 -1 -1]
     [-1  1  0  0]
     [-1  0  1  0]
     [-1  0  0  1]]

    """
    C = connectivity_matrix(edges, rtype='csr')
    L = C.transpose().dot(C)
    if normalize:
        L = L / L.diagonal().reshape((-1, 1))
        L = csr_matrix(L)
    return _return_matrix(L, rtype)


# ==============================================================================
# structural
# ==============================================================================

def equilibrium_matrix(C, xyz, free, rtype='array'):
    r"""Construct the equilibrium matrix of a structural system.

    Parameters
    ----------
    C : array-like
        Connectivity matrix (m x n).
    xyz : array-like
        Array of vertex coordinates (n x 3).
    free : list
        The index values of the free vertices.
    rtype : {'array', 'csc', 'csr', 'coo', 'list'}
        Format of the result.

    Returns
    -------
    array-like
        Constructed equilibrium matrix.

    Notes
    -----
    Analysis of the equilibrium matrix reveals some of the properties of the
    structural system, its size is (2ni x m) where ni is the number of free or
    internal nodes. It is calculated by

    .. math::

        \mathbf{E}
        =
        \left[
            \begin{array}{c}
                \mathbf{C}^{\mathrm{T}}_{\mathrm{i}}\mathbf{U} \\[0.3em]
                \hline \\[-0.7em]
                \mathbf{C}^{\mathrm{T}}_{\mathrm{i}}\mathbf{V}
            \end{array}
        \right].

    The matrix of vertex coordinates is vectorised to speed up the
    calculations.

    Examples
    --------
    >>> C = connectivity_matrix([[0, 1], [0, 2], [0, 3]])
    >>> xyz = [[0, 0, 1], [0, 1, 0], [-1, -1, 0], [1, -1, 0]]
    >>> equilibrium_matrix(C, xyz, [0], rtype='array')
        [[ 0.  1. -1.]
         [-1.  1.  1.]]

    """
    xyz = asarray(xyz, dtype=float)
    C   = csr_matrix(C)
    xy  = xyz[:, :2]
    uv  = C.dot(xy)
    U   = diags([uv[:, 0].flatten()], [0])
    V   = diags([uv[:, 1].flatten()], [0])
    Ct  = C.transpose()
    Cti = Ct[free, :]
    E   = svstack((Cti.dot(U), Cti.dot(V)))
    return _return_matrix(E, rtype)


def mass_matrix(Ct, ks, q=0, c=1, tiled=True):
    r"""Creates a network's nodal mass matrix.

    Parameters
    ----------
    Ct : sparse
        Sparse transpose of the connectivity matrix (n x m).
    ks : array
        Vector of member EA / L (m x 1).
    q : array
        Vector of member force densities (m x 1).
    c : float
        Convergence factor.
    tiled : bool
        Whether to tile horizontally by 3 for x, y, z.

    Returns
    -------
    array
        Mass matrix, either (m x 1) or (m x 3).

    Notes
    -----
    The mass matrix is defined as the sum of the member axial stiffnesses
    (inline) of the elements connected to each node, plus the force density.
    The force density ensures a non-zero value in form-finding/pre-stress
    modelling where E=0.

    .. math::

        \mathbf{m} =
        |\mathbf{C}^\mathrm{T}|
        (\mathbf{E} \circ \mathbf{A} \oslash \mathbf{l} + \mathbf{f} \oslash \mathbf{l})

    """
    m = c * abs(Ct).dot(ks + q)
    if tiled:
        return tile(m.reshape((-1, 1)), (1, 3))
    return m


def stiffness_matrix():
    raise NotImplementedError


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import compas

    from compas.datastructures import Network

    network = Network.from_obj(compas.get('grid_irregular.obj'))

    A = network_adjacency_matrix(network)
    C = network_connectivity_matrix(network)
    L = network_laplacian_matrix(network, normalize=True, rtype='csr')
    D = network_degree_matrix(network)
