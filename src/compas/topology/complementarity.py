__author__     = ['Robin Oval']
__copyright__  = 'Copyright 2018, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'oval@arch.ethz.ch'

__all__ = [
    'network_complement'
]

def network_complement(network, cls=None):
    """Generate the complement network of a network.
    The complement of a graph G is the graph H with the same vertices but whose edges consists of the edges not present in the graph G [1].

    Parameters
    ----------
    network : Network
        A network.

    Returns
    -------
    Network
        The complement network.

    References
    ----------
    .. [1] Wolfram MathWorld. *Graph complement*.
           Available at: http://mathworld.wolfram.com/GraphComplement.html.
    """

    if not cls:
        cls = type(network)

    vertices = [network.vertex_coordinates(vkey) for vkey in network.vertices()]

    edges = [(u, v) for u, v in combinations(network.vertices(), 2) if not network.has_edge(u, v, directed = False)]

    return cls.from_vertices_and_edges(vertices, edges)

# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    import compas
