""""""

try:
    from compas.numerical.alglib.xalglib import sparsecreate
    from compas.numerical.alglib.xalglib import sparseset
    from compas.numerical.alglib.xalglib import sparseget
    from compas.numerical.alglib.xalglib import sparsegetnrows
    from compas.numerical.alglib.xalglib import sparsegetncols
    from compas.numerical.alglib.xalglib import sparseconverttocrs
    from compas.numerical.alglib.xalglib import sparseconverttohash
    from compas.numerical.alglib.xalglib import sparseishash
except ImportError:
    import platform
    if platform.python_implementation() == 'IronPython':
        raise


__author__    = 'Tom Van Mele'
__copyright__ = 'Copyright 2016, Block Research Group - ETH Zurich'
__license__   = 'MIT license'
__email__     = 'vanmelet@ethz.ch'


__all__ = [
    'connectivity_matrix',
    'laplacian_matrix',
    'edgeweighted_laplacian_matrix',
]


def connectivity_matrix(edges, n, rtype=None):
    """Construct a sparse connectivity matrix.

    Parameters:
        edges (list) : Pairs of vertex indices.
        n (int) : The number of vertices.
        rtype (str) : Optional. The return type. Default is `None`.

    >>> import compas
    >>> network = Network.from_obj(compas.get_data('lines.obj'))
    >>> key_index = dict((key, index) for index, key in network.vertices_enum())
    >>> edges = [(key_index[u], key_index[v]) for u, v in network.edges_iter()]
    >>> n = len(network)
    >>> C = connectivity_matrix(edges, n)

    """
    m = len(edges)
    C = sparsecreate(m, n)
    for row, (i, j) in enumerate(edges):
        sparseset(C, row, i, -1)
        sparseset(C, row, j, +1)
    if rtype == 'crs':
        sparseconverttocrs(C)
    return C


def laplacian_matrix(neighbours, rtype=None):
    """Construct a sparse Laplacian matrix.

    Parameters:
        neighbours (list) : An adjacency list. For each vertex it should contain
            a list of neighbouring vertex indices.
        rtype (str) : Optional. The return type. Default is `None`.

    >>> import compas
    >>> network = Network.from_obj(compas.get_data('lines.obj'))
    >>> k_i = dict((key, index) for index, key in network.vertices_enum())
    >>> neighbours = [[k_i[nbr] for nbr in network.neighbours(key)] for key in network]
    >>> L = laplacian_matrix(neighbours)

    """
    n = len(neighbours)
    L = sparsecreate(n, n)
    for i in range(n):
        nbrs = neighbours[i]
        w = -1.0 / len(nbrs)
        for j in nbrs:
            sparseset(L, i, j, w)
        sparseset(L, i, i, 1.0)
    if rtype == 'crs':
        sparseconverttocrs(L)
    return L


def laplacian_block_diagonal_matrix(neighbours, rtype=None):
    pass


def overconstrained_laplacian_matrix(L, constraints, rtype=None):
    if not sparseishash(L):
        sparseconverttohash(L)
    c = len(constraints)
    m = sparsegetnrows(L)
    n = sparsegetncols(L)
    O = sparsecreate(m + c, n)
    for i in range(m):
        for j in range(n):
            v = sparseget(L, i, j)
            sparseset(O, i, j, v)
    for i in range(c):
        j = constraints[i]
        sparseset(O, m + i, j, 1.0)
    if rtype == 'crs':
        sparseconverttocrs(O)
    return O


def edgeweighted_laplacian_matrix(neighbours, rtype=None):
    """Construct an *edge-weighted* Laplacian matrix.

    Parameters:
        neighbours (list) : An adjacency list where every adjacent vertex is a
            tuple of the vertex index and the weight of the corresponding edge.
            An example of edge weights is force density.
        rtype (str) : Optional. The return type. Default is `None`.

    >>> import compas
    >>> network = Network.from_obj(compas.get_data('lines.obj'))
    >>> k_i = dict((key, index) for index, key in network.vertices_enum())
    >>> uv_q = dict(((u, v), attr['q']) for u, v, attr in network.edges_iter(True))
    >>> uv_q.update(((v, u), attr['q']) for u, v, attr in network.edges_iter(True))
    >>> neighbours = [[(k_i[nbr], uv_q[(key, nbr)]) for nbr in network.neighbours(key)] for key in network]
    >>> CtQC = edgeweighted_laplacian_matrix(neighbours)

    """
    n = len(neighbours)
    CtQC = sparsecreate(n, n)
    for i in range(n):
        Q = 0
        for j, q in neighbours[i]:
            Q += q
            sparseset(CtQC, i, j, -q)
        sparseset(CtQC, i, i, Q)
    if rtype == 'crs':
        sparseconverttocrs(CtQC)
    return CtQC


def CitQCi():
    pass


def CitQCf():
    pass


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    import compas
    from compas.datastructures.network import Network

    network = Network.from_obj(compas.get_data('lines.obj'))

    key_index = network.key_index()
    edges = [(key_index[u], key_index[v]) for u, v in network.edges()]

    n = network.number_of_vertices()

    C = connectivity_matrix(edges, n)

    print C
