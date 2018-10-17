from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


__all__ = [
    'adjacency_from_edges',
    'connectivity_from_edges'
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
    .. code-block:: python

        #

    """
    adj = {}
    for i, j in iter(edges):
        adj.setdefault(i, []).append(j)
        adj.setdefault(j, []).append(i)
    return adj


def connectivity_from_edges(edges):
    """"""
    raise NotImplementedError


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
