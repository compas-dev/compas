from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import sys
import compas

try:
    from compas.numerical.alglib.core import Array
    from compas.numerical.alglib.core import Zeros
    from compas.numerical.alglib.core import Diagonal

    from compas.numerical.alglib.core import SparseArray

    from compas.numerical.alglib.core.xalglib import sparsecreate
    from compas.numerical.alglib.core.xalglib import sparseset
    from compas.numerical.alglib.core.xalglib import sparseget
    from compas.numerical.alglib.core.xalglib import sparsegetnrows
    from compas.numerical.alglib.core.xalglib import sparsegetncols
    from compas.numerical.alglib.core.xalglib import sparseconverttocrs
    from compas.numerical.alglib.core.xalglib import sparseconverttohash
    from compas.numerical.alglib.core.xalglib import sparseishash

except ImportError:
    compas.raise_if_ironpython()


__all__ = [
    'connectivity_matrix',
    'sparse_connectivity_matrix',
    # 'laplacian_matrix',
    # 'edgeweighted_laplacian_matrix',
]


def connectivity_matrix(edges, v):
    e = len(edges)
    C = Zeros((e, v))
    for i in range(e):
        C[i, edges[i][0]] = -1
        C[i, edges[i][1]] = +1
    return C


def sparse_connectivity_matrix(edges, v, rtype=None):
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
    e = len(edges)
    shape = e, v
    rows, cols, data = [], [], []
    for i in range(e):
        rows.append(i)
        rows.append(i)
        cols.append(edges[i][0])
        cols.append(edges[i][1])
        data.append(-1)
        data.append(+1)
    C = SparseArray((rows, cols, data), shape)
    return C


# def laplacian_matrix(neighbors, rtype=None):
#     """Construct a sparse Laplacian matrix.

#     Parameters:
#         neighbors (list) : An adjacency list. For each vertex it should contain
#             a list of neighboring vertex indices.
#         rtype (str) : Optional. The return type. Default is `None`.

#     >>> import compas
#     >>> network = Network.from_obj(compas.get_data('lines.obj'))
#     >>> k_i = dict((key, index) for index, key in network.vertices_enum())
#     >>> neighbors = [[k_i[nbr] for nbr in network.neighbors(key)] for key in network]
#     >>> L = laplacian_matrix(neighbors)

#     """
#     n = len(neighbors)
#     L = sparsecreate(n, n)
#     for i in range(n):
#         nbrs = neighbors[i]
#         w = -1.0 / len(nbrs)
#         for j in nbrs:
#             sparseset(L, i, j, w)
#         sparseset(L, i, i, 1.0)
#     if rtype == 'crs':
#         sparseconverttocrs(L)
#     return L


# def overconstrained_laplacian_matrix(L, constraints, rtype=None):
#     if not sparseishash(L):
#         sparseconverttohash(L)
#     c = len(constraints)
#     m = sparsegetnrows(L)
#     n = sparsegetncols(L)
#     O = sparsecreate(m + c, n)
#     for i in range(m):
#         for j in range(n):
#             v = sparseget(L, i, j)
#             sparseset(O, i, j, v)
#     for i in range(c):
#         j = constraints[i]
#         sparseset(O, m + i, j, 1.0)
#     if rtype == 'crs':
#         sparseconverttocrs(O)
#     return O


# def edgeweighted_laplacian_matrix(neighbors, rtype=None):
#     """Construct an *edge-weighted* Laplacian matrix.

#     Parameters:
#         neighbors (list) : An adjacency list where every adjacent vertex is a
#             tuple of the vertex index and the weight of the corresponding edge.
#             An example of edge weights is force density.
#         rtype (str) : Optional. The return type. Default is `None`.

#     >>> import compas
#     >>> network = Network.from_obj(compas.get_data('lines.obj'))
#     >>> k_i = dict((key, index) for index, key in network.vertices_enum())
#     >>> uv_q = dict(((u, v), attr['q']) for u, v, attr in network.edges_iter(True))
#     >>> uv_q.update(((v, u), attr['q']) for u, v, attr in network.edges_iter(True))
#     >>> neighbors = [[(k_i[nbr], uv_q[(key, nbr)]) for nbr in network.neighbors(key)] for key in network]
#     >>> CtQC = edgeweighted_laplacian_matrix(neighbors)

#     """
#     n = len(neighbors)
#     CtQC = sparsecreate(n, n)
#     for i in range(n):
#         Q = 0
#         for j, q in neighbors[i]:
#             Q += q
#             sparseset(CtQC, i, j, -q)
#         sparseset(CtQC, i, i, Q)
#     if rtype == 'crs':
#         sparseconverttocrs(CtQC)
#     return CtQC


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    import compas
    from compas.datastructures import Network

    network = Network.from_obj(compas.get_data('lines.obj'))

    key_index = network.key_index()
    edges = [(key_index[u], key_index[v]) for u, v in network.edges()]

    n = network.number_of_vertices()

    C = connectivity_matrix(edges, n)

    print(C)
