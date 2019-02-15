from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.topology import breadth_first_traverse


__all__ = [
    'network_is_connected'
]


def network_is_connected(network):
    """Verify that the network is connected.

    Returns
    -------
    bool
        True, if the network is connected.
        False, otherwise.

    Notes
    -----
    A network is connected if for every two vertices a path exists connecting them.

    """
    if not network.vertex:
        return False

    nodes = breadth_first_traverse(network.adjacency, network.get_any_vertex())

    return len(nodes) == network.number_of_vertices()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
