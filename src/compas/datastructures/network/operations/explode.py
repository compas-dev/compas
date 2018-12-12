from compas.topology import connected_components

__author__     = ['Robin Oval']
__copyright__  = 'Copyright 2018, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'oval@arch.ethz.ch'

__all__ = [
    'network_explode'
]

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

    connected_vertices = connected_components(network.adjacency)

    exploded_networks = []

    for vertex_keys in connected_vertices:
        
        vertices = [network.vertex_coordinates(vkey) for vkey in vertex_keys]
        
        key_to_index = {vkey: i for i, vkey in enumerate(vertex_keys)}

        edges = [ (key_to_index[ukey], key_to_index[vkey]) for ukey in vertex_keys for vkey in network.vertex_neighbors(vkey) if ukey < vkey]
        
        exploded_networks.append(cls.from_vertices_and_edges(vertices, edges))

    return exploded_networks

# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    
    pass
