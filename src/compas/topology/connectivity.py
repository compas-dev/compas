from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

__all__ = [
    'adjacency_from_edges'
]


def adjacency_from_edges(edges):
    """Construct an adjacency dictionary from a set of edges.

    Parameters
    ----------
    edges : list
        A list of index pairs.

    Returns
    -------
    dict
        A dictionary mapping each index in the list of index pairs
        to a list of adjacent indices.

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


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import doctest

    doctest.testmod(globs=globals())
