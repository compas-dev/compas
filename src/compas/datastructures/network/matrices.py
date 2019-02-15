from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.numerical import adjacency_matrix
from compas.numerical import degree_matrix
from compas.numerical import connectivity_matrix
from compas.numerical import laplacian_matrix


__all__ = [
    'network_adjacency_matrix',
    'network_degree_matrix',
    'network_connectivity_matrix',
    'network_laplacian_matrix',
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


def network_adjacency_matrix(network, rtype='array'):
    """Creates a vertex adjacency matrix from a Network datastructure.

    Parameters
    ----------
    network : obj
        Network datastructure object to get data from.
    rtype : {'array', 'csc', 'csr', 'coo', 'list'}
        Format of the result.

    Returns
    -------
    array-like
        Constructed adjacency matrix.

    """
    key_index = network.key_index()
    adjacency = [[key_index[nbr] for nbr in network.vertex_neighbors(key)] for key in network.vertices()]
    return adjacency_matrix(adjacency, rtype=rtype)


def network_degree_matrix(network, rtype='array'):
    """Creates a vertex degree matrix from a Network datastructure.

    Parameters
    ----------
    network : obj
        Network datastructure object to get data from.
    rtype : {'array', 'csc', 'csr', 'coo', 'list'}
        Format of the result.

    Returns
    -------
    array-like
        Constructed vertex degree matrix.

    """
    key_index = network.key_index()
    adjacency = [[key_index[nbr] for nbr in network.vertex_neighbors(key)] for key in network.vertices()]
    return degree_matrix(adjacency, rtype=rtype)


def network_connectivity_matrix(network, rtype='array'):
    """Creates a connectivity matrix from a Network datastructure.

    Parameters
    ----------
    network : obj
        Network datastructure object to get data from.
    rtype : {'array', 'csc', 'csr', 'coo', 'list'}
        Format of the result.

    Returns
    -------
    array-like
        Constructed connectivity matrix.

    """
    key_index = network.key_index()
    edges = [(key_index[u], key_index[v]) for u, v in network.edges()]
    return connectivity_matrix(edges, rtype=rtype)


def network_laplacian_matrix(network, normalize=False, rtype='array'):
    r"""Construct a Laplacian matrix from a Network datastructure.

    Parameters
    ----------
    network : obj
        Network datastructure object to get data from.
    normalize : bool
        Normalize the entries such that the value on the diagonal is ``1``.
    rtype : {'array', 'csc', 'csr', 'coo', 'list'}
        Format of the result.

    Returns
    -------
    array-like
        Constructed Laplacian matrix.

    Notes
    -----
    ``d = L.dot(xyz)`` is currently a vector that points from the centroid to the vertex.
    Therefore ``c = xyz - d``. By changing the signs in the laplacian, the dsiplacement
    vectors could be used in a more natural way ``c = xyz + d``.

    Examples
    --------
    .. plot::
        :include-source:

        from numpy import array

        import compas
        from compas.datastructures import Network
        from compas.numerical import network_laplacian_matrix

        network = Network.from_obj(compas.get('grid_irregular.obj'))

        xy = array([network.vertex_coordinates(key, 'xy') for key in network.vertices()])
        L  = network_laplacian_matrix(network, normalize=True, rtype='csr')
        d  = L.dot(xy)

        lines = [{'start': xy[i], 'end': xy[i] - d[i]} for i, k in enumerate(network.vertices())]

    """
    key_index = network.key_index()
    edges = [(key_index[u], key_index[v]) for u, v in network.edges()]
    return laplacian_matrix(edges, normalize=normalize, rtype=rtype)


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
