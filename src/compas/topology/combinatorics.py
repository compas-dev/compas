from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from collections import deque
from compas.topology import breadth_first_traverse


__all__ = [
    'vertex_coloring',
    'connected_components',
]


def vertex_coloring(adjacency):
    """Color the vertices of a network such that no two colors are adjacent.

    Parameters
    ----------
    network : compas.datastructures.Network
        The network object.

    Notes
    -----
    For more info, see [1]_.

    References
    ----------
    .. [1] Chu-Carroll, M. *Graph Coloring Algorithms*.
           Available at: http://scienceblogs.com/goodmath/2007/06/28/graph-coloring-algorithms-1/.

    Warning
    -------
    This is a greedy algorithm, so it might be slow for large networks.

    Examples
    --------
    .. plot::
        :include-source:

        import compas
        from compas.datastructures import Network
        from compas.plotters import NetworkPlotter
        from compas.topology import vertex_coloring

        network = Network.from_obj(compas.get('grid_irregular.obj'))

        key_color = vertex_coloring(network.adjacency)
        colors = ['#ff0000', '#00ff00', '#0000ff', '#ffff00', '#00ffff']

        plotter = NetworkPlotter(network)

        plotter.draw_vertices(facecolor={key: colors[key_color[key]] for key in network.vertices()})
        plotter.draw_edges()

        plotter.show()

    """
    key_to_color = {}
    key_to_degree = {key: len(adjacency[key]) for key in adjacency}
    vertices = sorted(adjacency.keys(), key=lambda key: key_to_degree[key])
    uncolored = deque(vertices[::-1])
    current_color = 0
    while uncolored:
        a = uncolored.popleft()
        key_to_color[a] = current_color
        colored_with_current = [a]
        for b in uncolored:
            if not any(b in adjacency[key] for key in colored_with_current):
                key_to_color[b] = current_color
                colored_with_current.append(b)
        for key in colored_with_current[1:]:
            uncolored.remove(key)
        current_color += 1
    return key_to_color


def connected_components(adjacency):
    """Identify the vertices of connected components.

    Parameters
    ----------
    adjacency : dict
        An adjacency dictionary mapping vertex identifiers to neighbours.

    Returns
    -------
    list of list of hashable
        A nested list of vertex identifiers.

    Examples
    --------
    .. code-block:: python

        pass

    """
    tovisit = set(adjacency)
    components = []
    while tovisit:
        root = tovisit.pop()
        visited = breadth_first_traverse(adjacency, root)
        tovisit -= visited
        components.append(list(visited))
    return components


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import compas
    from compas.datastructures import Network
    from compas.plotters import NetworkPlotter

    network = Network.from_obj(compas.get('grid_irregular.obj'))

    components = connected_components(network.adjacency)

    key_color = vertex_coloring(network.adjacency)

    colors = ['#ff0000', '#00ff00', '#0000ff', '#ffff00']

    plotter = NetworkPlotter(network, figsize=(10, 7))

    plotter.draw_vertices(facecolor={key: colors[key_color[key]] for key in network.vertices()})
    plotter.draw_edges()

    plotter.show()
