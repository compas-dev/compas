from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


__all__ = [
    "network_split_edge",
]


def network_split_edge(network, u, v, t=0.5):
    """Split and edge by inserting a node along its length.

    Parameters
    ----------
    u : str
        The key of the first node of the edge.
    v : str
        The key of the second node of the edge.
    t : float, optional
        The position of the inserted node on the edge.

    Returns
    -------
    hashable
        The key of the inserted node.

    Raises
    ------
    ValueError
        If `t` is not in the range 0-1.
    Exception
        If `u` and `v` are not neighbors.

    """
    if not network.has_edge(u, v):
        return

    if t <= 0.0:
        raise ValueError("t should be greater than 0.0.")
    if t >= 1.0:
        raise ValueError("t should be smaller than 1.0.")

    # the split node
    x, y, z = network.edge_point(u, v, t)
    w = network.add_node(x=x, y=y, z=z)

    network.add_edge(u, w)
    network.add_edge(w, v)

    if v in network.edge[u]:
        del network.edge[u][v]
    elif u in network.edge[v]:
        del network.edge[v][u]
    else:
        raise Exception

    # split half-edge UV
    network.adjacency[u][w] = None
    network.adjacency[w][v] = None
    del network.adjacency[u][v]

    # split half-edge VU
    network.adjacency[v][w] = None
    network.adjacency[w][u] = None
    del network.adjacency[v][u]

    # return the key of the split node
    return w
