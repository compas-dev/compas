from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.topology import connected_components

__all__ = [
    'network_disconnected_nodes',
    'network_disconnected_edges',
    'network_explode'
]


def network_disconnected_nodes(network):
    """Get the disconnected node groups in a network.

    Parameters
    ----------
    network : Network
        A network.

    Returns
    -------
    list
        The list of disconnected node groups.
    """
    return connected_components(network.adjacency)


def network_disconnected_edges(network):
    """Get the disconnected edge groups in a network.

    Parameters
    ----------
    network : Network
        A network.

    Returns
    -------
    parts : list
        The list of disconnected edge groups.
    """
    components = network_disconnected_nodes(network)
    return [[(u, v) for u in component for v in network.neighbors(u) if u < v] for component in components]


def network_explode(network, cls=None):
    """Explode a network into its connected components.

    Parameters
    ----------
    network : Network
        A network.

    Returns
    -------
    exploded_networks : list
        The list of the networks from the exploded network parts.
    """
    if cls is None:
        cls = type(network)

    exploded_networks = []

    parts = network_disconnected_edges(network)

    for part in parts:
        keys = list(set([key for edge in part for key in edge]))
        nodes = [network.node_coordinates(key) for key in keys]
        key_index = {key: index for index, key in enumerate(keys)}
        edges = [(key_index[u], key_index[v]) for u, v in part]
        exploded_networks.append(cls.from_nodes_and_edges(nodes, edges))

    return exploded_networks


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    # from compas.datastructures import Network

    # nodes = [
    #     [0.0, 0.0, 0.0],
    #     [1.0, 0.0, 0.0],
    #     [2.0, 0.0, 0.0],
    #     [3.0, 0.0, 0.0],
    #     [4.0, 0.0, 0.0],
    # ]

    # edges = [
    #     (0, 1),
    #     (2, 3),
    #     (3, 4),
    # ]

    # network = Network.from_nodes_and_edges(nodes, edges)

    # print(network_disconnected_nodes(network))
    # print(network_disconnected_edges(network))
    # print(network_explode(network))

    import doctest
    doctest.testmod(globs=globals())
