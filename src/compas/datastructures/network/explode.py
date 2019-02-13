from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.topology import connected_components

__all__ = [
    'network_disconnected_vertices',
    'network_disconnected_edges',
    'network_explode'
]


def network_disconnected_vertices(network):
    """Get the disconnected vertex groups in a network.

    Parameters
    ----------
    network : Network
        A network.

    Returns
    -------
    list
        The list of disconnected vertex groups.

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


    parts = network_disconnected_vertices(network)

    return [[(u, v) for u in part for v in network.vertex_neighbors(u) if u < v] for part in parts]


def network_explode(network, cls=None):
    """Explode a network into its disconnected parts.

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

    parts = network_disconnected_edges(network)

    exploded_networks = []

    for part in parts:
        
        vertex_keys = list(set([vkey for edge in part for vkey in edge]))
        vertices = [network.vertex_coordinates(vkey) for vkey in vertex_keys]
        
        key_to_index = {vkey: i for i, vkey in enumerate(vertex_keys)}
        edges = [ (key_to_index[u], key_to_index[v]) for u, v in part]
        
        exploded_networks.append(cls.from_vertices_and_edges(vertices, edges))

    return exploded_networks


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    
    from compas.datastructures import Network

    vertices = [
        [0.0, 0.0, 0.0],
        [1.0, 0.0, 0.0],
        [2.0, 0.0, 0.0],
        [3.0, 0.0, 0.0],
        [4.0, 0.0, 0.0],
    ]

    edges = [
        (0, 1),
        (2, 3),
        (3, 4),
    ]

    network = Network.from_vertices_and_edges(vertices, edges)

    print(network_disconnected_vertices(network))
    print(network_disconnected_edges(network))
    print(network_explode(network))
