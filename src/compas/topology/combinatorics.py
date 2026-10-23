from collections import deque
from collections.abc import Collection
from collections.abc import Hashable
from collections.abc import Mapping
from typing import TypeVar

from compas.topology.traversal import breadth_first_traverse

Key = TypeVar("Key", bound=Hashable)


def vertex_coloring(adjacency: Mapping[Key, Collection[Key]]) -> dict[Key, int]:
    """Color the vertices of a graph such that no two colors are adjacent.

    Parameters
    ----------
    adjacency
        An adjacency dictionary representing the connectivity of the graph
        by mapping nodes identifiers to neighbour identifiers.
        Examples of valid adjacency dicts are

        - `{0: [1, 2, 3, 4], 1: [0], 2: [0], 3: [0], 4: [0]}`
        - `{0: {1: None, 2: None, 3: None, 4: None}, 1: {0: None}, ...}`

    Returns
    -------
    dict[Key, int]
        A dict mapping each node of the graph to a color number.

    Notes
    -----
    This algorithms works on any data structure that can be interpreted as a graph, e.g.
    graphs, meshes, volmeshes, etc..

    This is a greedy algorithm and does not necessarily use the minimum number
    of colors.[^vertex-coloring-greedy]

    References
    ----------
    [^vertex-coloring-greedy]: Chu-Carroll, M. [*Graph Coloring
        Algorithms*](https://scienceblogs.com/goodmath/2007/06/28/graph-coloring-algorithms-1/).

    Warnings
    --------
    This is a greedy algorithm, so it might be slow for large graphs.

    Examples
    --------
    >>> import compas
    >>> from compas.datastructures import Graph
    >>> graph = Graph.from_obj(compas.get("lines.obj"))
    >>> key_color = vertex_coloring(graph.adjacency)
    >>> key = graph.node_sample(size=1)[0]
    >>> color = key_color[key]
    >>> any(key_color[nbr] == color for nbr in graph.neighbors(key))
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


def connected_components(adjacency: Mapping[Key, Collection[Key]]) -> list[list[Key]]:
    """Identify the connected components of a graph.

    Parameters
    ----------
    adjacency
        An adjacency dictionary representing the connectivity of the graph
        by mapping nodes identifiers to neighbour identifiers.
        Examples of valid adjacency dicts are

        - `{0: [1, 2, 3, 4], 1: [0], 2: [0], 3: [0], 4: [0]}`
        - `{0: {1: None, 2: None, 3: None, 4: None}, 1: {0: None}, ...}`

    Returns
    -------
    list[list[Key]]
        A list of connected components,
        with each component a list of connected nodes.

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
