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

    Examples
    --------
    >>> import compas
    >>> from compas.datastructures import Network
    >>> from compas.datastructures import network_is_connected
    >>> network = Network.from_obj(compas.get('lines.obj'))
    >>> network_is_connected(network)
    True
    """
    if network.number_of_nodes() == 0:
        return False
    nodes = breadth_first_traverse(network.adjacency, network.get_any_node())
    return len(nodes) == network.number_of_nodes()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import doctest

    doctest.testmod(globs=globals())
