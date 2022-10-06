from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.topology import shortest_path


__all__ = ["network_shortest_path"]


def network_shortest_path(network, start, end):
    """Find the shortest path between two nodes of the network.

    Parameters
    ----------
    network : :class:`~compas.datastructures.Network`
        A network data structure.
    start : hashable
        The identifier of the start node.
    end : hashable
        The identifier of the end node.

    Returns
    -------
    list[hashable]
        The nodes of the network leading from start to end.

    """
    return shortest_path(network.adjacency, start, end)
