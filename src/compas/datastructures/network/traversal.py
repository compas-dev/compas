from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.topology import shortest_path


__all__ = [
    'network_shortest_path'
]


def network_shortest_path(network, start, end):
    """Find the shortest path between two nodes of the network.

    Parameters
    ----------
    network : :class:`compas.datastructures.Network`
    start : int
    end : int

    Returns
    -------
    list of int
        The nodes of the network leading from start to end.

    Examples
    --------
    >>>
    """
    return shortest_path(network.adjacency, start, end)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import doctest

    doctest.testmod(globs=globals())
