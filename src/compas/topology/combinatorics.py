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

    Warnings
    --------
    This is a greedy algorithm, so it might be slow for large networks.

    Examples
    --------
    >>> import compas
    >>> from compas.datastructures import Network
    >>> network = Network.from_obj(compas.get('lines.obj'))
    >>> key_color = vertex_coloring(network.adjacency)
    >>> key = network.get_any_vertex()
    >>> color = key_color[key]
    >>> any(key_color[nbr] == color for nbr in network.vertex_neighbors(key))
    False
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
    >>> adjacency = {0: [1, 2], 1: [0, 2], 2: [0, 1], 3: []}
    >>> connected_components(adjacency)
    [[0, 1, 2], [3]]
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

    import doctest

    doctest.testmod(globs=globals())
