from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


def adjacency_from_edges(edges):
    """Construct an adjacency dictionary from a set of edges.

    Parameters
    ----------
    edges : sequence[[hashable, hashable]]
        A list of node identifier pairs.

    Returns
    -------
    dict[hashable, list[hashable]]
        A dictionary mapping each node in the list of node pairs
        to a list of adjacent/connected nodes.

    Examples
    --------
    >>> edges = [[0, 1], [0, 2], [0, 3], [0, 4]]
    >>> adjacency_from_edges(edges)
    {0: [1, 2, 3, 4], 1: [0], 2: [0], 3: [0], 4: [0]}

    """
    adj = {}
    for i, j in iter(edges):
        adj.setdefault(i, []).append(j)
        adj.setdefault(j, []).append(i)
    return adj
