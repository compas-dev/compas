__author__     = ['Robin Oval']
__copyright__  = 'Copyright 2018, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'oval@arch.ethz.ch'

__all__ = [
    'network_disjointed_parts',
    'network_explode'
]

def network_disjointed_parts(network):
    """Get the disjointed parts in a network as lists of edges.

    Parameters
    ----------
    network : Network
        A network.

    Returns
    -------
    parts : list
        The list of disjointed parts as lists of edges.

    """

    parts = []
    edges = list(network.edges())

    while len(edges) > 0:
        # pop one vertex to start a part
        part = [edges.pop()]
        next_neighbours = [part[-1]]

        # propagate to neighbours
        while len(next_neighbours) > 0:

            for u, v in network.edge_connected_edges(*next_neighbours.pop()):

                if (u, v) not in part and (v, u) not in part:
                    part.append((u, v))
                    edges.remove((u, v))

                    if (u, v) not in next_neighbours:
                        next_neighbours.append((u, v))
        
        parts.append(part)

    return parts

def network_explode(network, cls=None):
    """Explode a network into its disjointed parts.

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

    parts = network_disjointed_parts(network)

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

    pass
