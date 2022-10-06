from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.topology import connected_components

__all__ = [
    "network_disconnected_nodes",
    "network_disconnected_edges",
    "network_explode",
]


def network_disconnected_nodes(network):
    """Get the disconnected node groups in a network.

    Parameters
    ----------
    network : :class:`~compas.datastructures.Network`
        A network.

    Returns
    -------
    list[list[hashable]]
        The list of disconnected node groups.

    """
    return connected_components(network.adjacency)


def network_disconnected_edges(network):
    """Get the disconnected edge groups in a network.

    Parameters
    ----------
    network : :class:`~compas.datastructures.Network`
        A network.

    Returns
    -------
    list[list[tuple[hashable, hashable]]]
        The list of disconnected edge groups.

    """
    components = network_disconnected_nodes(network)
    return [[(u, v) for u in component for v in network.neighbors(u) if u < v] for component in components]


def network_explode(network, cls=None):
    """Explode a network into its connected components.

    Parameters
    ----------
    network : :class:`~compas.datastructures.Network`
        A network.

    Returns
    -------
    list[:class:`~compas.datastructures.Network`]
        The list of exploded network parts.

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
