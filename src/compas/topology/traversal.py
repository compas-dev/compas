from collections import deque
from collections.abc import Callable
from collections.abc import Hashable
from collections.abc import Iterable
from collections.abc import Iterator
from collections.abc import Mapping
from itertools import count
from queue import PriorityQueue
from typing import TYPE_CHECKING
from typing import TypeVar
from typing import cast

from compas.geometry import distance_point_point

if TYPE_CHECKING:
    from compas.datastructures import Graph
    from compas.datastructures import Mesh

Key = TypeVar("Key", bound=Hashable)

# ==============================================================================
# DFS
# ==============================================================================


def depth_first_ordering(adjacency: Mapping[Key, Iterable[Key]], root: Key) -> list[Key]:
    """Compute a depth-first ordering of the nodes of a graph, starting from a root node.

    Parameters
    ----------
    adjacency
        An adjacency dictionary representing the connectivity of the graph
        by mapping nodes identifiers to neighbour identifiers.
        Examples of valid adjacency dicts are

        * `{0: [1, 2, 3, 4], 1: [0], 2: [0], 3: [0], 4: [0]}`
        * `{0: {1: None, 2: None, 3: None, 4: None}, 1: {0: None}, 2: {0: None}, 3: {0: None}, 4: {0: None}}`

    root
        The node from which to start the depth-first search.

    Returns
    -------
    list[Key]
        A depth-first ordering of all nodes of the graph.

    Notes
    -----
    Return all nodes of a connected component containing `root` of a graph
    represented by an adjacency dictionary.

    This implementation uses a "to visit" stack. The principle of a stack
    is LIFO. In Python, a list is a stack.

    Initially only the root element is on the stack. While there are still
    elements on the stack, the node on top of the stack is "popped off" and if
    this node was not already visited, its neighbors are added to the stack if
    they hadn't already been visited themselves.

    Since the last element on top of the stack is always popped off, the
    algorithm goes deeper and deeper in the datastructure, until it reaches a
    node without (unvisited) neighbors and then backtracks. Once a new node
    with unvisited neighbors is found, there too it will go as deep as possible
    before backtracking again, and so on. Once there are no more nodes on the
    stack, the entire structure has been traversed.

    Note that this returns a depth-first spanning tree of a connected component
    of the graph.

    """
    adjacency = {key: set(nbrs) for key, nbrs in iter(adjacency.items())}
    tovisit = [root]
    visited = set()
    ordering = []

    while tovisit:
        # pop the last added element from the stack
        node = tovisit.pop()
        if node not in visited:
            # mark the node as visited
            visited.add(node)
            ordering.append(node)
            # add the unvisited nbrs to the stack
            tovisit.extend(adjacency[node] - visited)
    return ordering


# ==============================================================================
# BFS
# ==============================================================================


def breadth_first_ordering(adjacency: Mapping[Key, Iterable[Key]], root: Key) -> list[Key]:
    """Compute a breadth-first ordering of the nodes of a graph, starting from a root node.

    Parameters
    ----------
    adjacency
        An adjacency dictionary representing the connectivity of the graph
        by mapping nodes identifiers to neighbour identifiers.
        Examples of valid adjacency dicts are

        * `{0: [1, 2, 3, 4], 1: [0], 2: [0], 3: [0], 4: [0]}`
        * `{0: {1: None, 2: None, 3: None, 4: None}, 1: {0: None}, 2: {0: None}, 3: {0: None}, 4: {0: None}}`

    root
        The node from which to start the breadth-first search.

    Returns
    -------
    list[Key]
        A breadth-first ordering of all nodes of the graph.

    Notes
    -----
    This implementation uses a double-ended queue (deque) to keep track of nodes to visit.
    The principle of a queue is FIFO. In Python, a deque is ideal for removing elements
    from the beginning, i.e. from the 'left'.

    In a breadth-first search, all unvisited neighbors of a node are visited
    first. When a neighbor is visited, its univisited neighbors are added to
    the list of nodes to visit.

    By appending the neighbors to the end of the list of nodes to visit,
    and by visiting the nodes at the start of the list first, the graph is
    traversed in *breadth-first* order.

    """
    tovisit = deque([root])
    visited = set([root])
    ordering = [root]
    while tovisit:
        node = tovisit.popleft()
        for nbr in adjacency[node]:
            if nbr not in visited:
                tovisit.append(nbr)
                visited.add(nbr)
                ordering.append(nbr)
    return ordering


def breadth_first_traverse(adjacency: Mapping[Key, Iterable[Key]], root: Key, callback: Callable[[Key, Key], None] | None = None) -> set[Key]:
    """Traverse an adjacency dict in "breadth-first" order.

    Parameters
    ----------
    adjacency
        An adjacency dictionary representing the connectivity of the graph
        by mapping nodes identifiers to neighbour identifiers.
        Examples of valid adjacency dicts are

        * `{0: [1, 2, 3, 4], 1: [0], 2: [0], 3: [0], 4: [0]}`
        * `{0: {1: None, 2: None, 3: None, 4: None}, 1: {0: None}, 2: {0: None}, 3: {0: None}, 4: {0: None}}`

    root
        The identifier of the starting node.
    callback
        A callback function applied to every traversed node and its current neighbour.

    Returns
    -------
    set[Key]
        The visited nodes.

    """
    tovisit = deque([root])
    visited = set([root])
    while tovisit:
        node = tovisit.popleft()
        for nbr in adjacency[node]:
            if nbr not in visited:
                tovisit.append(nbr)
                visited.add(nbr)
                if callback:
                    callback(node, nbr)
    return visited


def breadth_first_paths(adjacency: Mapping[Key, Iterable[Key]], root: Key, goal: Key) -> Iterator[list[Key]]:
    """Return all paths from root to goal.

    Parameters
    ----------
    adjacency
        An adjacency dictionary representing the connectivity of the graph
        by mapping nodes identifiers to neighbour identifiers.
        Examples of valid adjacency dicts are

        * `{0: [1, 2, 3, 4], 1: [0], 2: [0], 3: [0], 4: [0]}`
        * `{0: {1: None, 2: None, 3: None, 4: None}, 1: {0: None}, 2: {0: None}, 3: {0: None}, 4: {0: None}}`

    root
        The identifier of the starting node.
    goal
        The identifier of the ending node.

    Yields
    ------
    list[Key]
        A path from root to goal.

    Notes
    -----
    Due to the nature of the search, the first path returned is the shortest.

    """
    if root == goal:
        yield [root]
        return

    adjacency = {key: set(nbrs) for key, nbrs in iter(adjacency.items())}
    tovisit = deque([(root, [root])])
    while tovisit:
        node, path = tovisit.popleft()
        for nbr in adjacency[node] - set(path):
            if nbr == goal:
                yield path + [nbr]
            else:
                tovisit.append((nbr, path + [nbr]))


def breadth_first_tree(adjacency: Mapping[Key, Iterable[Key]], root: Key) -> tuple[list[Key], dict[Key, Key], list[list[Key]]]:
    """Compute a BFS tree, starting from a root node.

    Parameters
    ----------
    adjacency
        An adjacency dictionary representing the connectivity of the graph
        by mapping nodes identifiers to neighbour identifiers.
        Examples of valid adjacency dicts are

        * `{0: [1, 2, 3, 4], 1: [0], 2: [0], 3: [0], 4: [0]}`
        * `{0: {1: None, 2: None, 3: None, 4: None}, 1: {0: None}, 2: {0: None}, 3: {0: None}, 4: {0: None}}`

    root
        Identifier of the root node.

    Returns
    -------
    tuple[list[Key], dict[Key, Key], list[list[Key]]]
        The BFS ordering, the predecessor mapping, and the traversal paths.

    """
    tovisit = deque([root])
    visited = set([root])
    ordering = [root]
    predecessors = {}
    paths_by_node = {root: [root]}
    while tovisit:
        node = tovisit.popleft()
        for nbr in adjacency[node]:
            if nbr not in visited:
                predecessors[nbr] = node
                paths_by_node[nbr] = paths_by_node[node] + [nbr]
                tovisit.append(nbr)
                visited.add(nbr)
                ordering.append(nbr)
    return ordering, predecessors, [paths_by_node[node] for node in ordering]


# ==============================================================================
# shortest
# ==============================================================================


def shortest_path(adjacency: Mapping[Key, Iterable[Key]], root: Key, goal: Key) -> list[Key] | None:
    """Find the shortest path between two vertices of a graph.

    Parameters
    ----------
    adjacency
        An adjacency dictionary representing the connectivity of the graph
        by mapping nodes identifiers to neighbour identifiers.
        Examples of valid adjacency dicts are

        * `{0: [1, 2, 3, 4], 1: [0], 2: [0], 3: [0], 4: [0]}`
        * `{0: {1: None, 2: None, 3: None, 4: None}, 1: {0: None}, 2: {0: None}, 3: {0: None}, 4: {0: None}}`

    root
        The identifier of the starting node.
    goal
        The identifier of the ending node.

    Returns
    -------
    list[Key] | None
        The path from root to goal, or None, if no path exists between the vertices.

    """
    try:
        return next(breadth_first_paths(adjacency, root, goal))
    except StopIteration:
        return None


# ==============================================================================
# A*
# ==============================================================================


def _reconstruct_path(came_from: Mapping[Key, Key], current: Key) -> list[Key] | None:
    if current not in came_from:
        return None
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.append(current)
    total_path.reverse()
    return total_path


def astar_lightest_path(
    adjacency: Mapping[Key, Iterable[Key]],
    weights: Mapping[tuple[Key, Key], float],
    heuristic: Mapping[Key, float],
    root: Key,
    goal: Key,
) -> list[Key] | None:
    """Find the path of least weight between two vertices of a graph using the A* search algorithm.

    Parameters
    ----------
    adjacency
        An adjacency dictionary representing the connectivity of the graph
        by mapping nodes identifiers to neighbour identifiers.
        Examples of valid adjacency dicts are

        * `{0: [1, 2, 3, 4], 1: [0], 2: [0], 3: [0], 4: [0]}`
        * `{0: {1: None, 2: None, 3: None, 4: None}, 1: {0: None}, 2: {0: None}, 3: {0: None}, 4: {0: None}}`

    weights
        A dictionary of edge weights.
    heuristic
        A dictionary of guesses of weights of paths from a node to the goal.
    root
        The start vertex.
    goal
        The end vertex.

    Returns
    -------
    list[Key] | None
        The path from root to goal, or None, if no path exists between the vertices.

    References
    ----------
    - [A* search algorithm](https://en.wikipedia.org/wiki/A*_search_algorithm)

    """
    visited_set = set()

    if root == goal:
        return [root]

    candidates_set = {root}
    best_candidate_heap: PriorityQueue[tuple[float, int, Key]] = PriorityQueue()
    counter = count()
    best_candidate_heap.put((heuristic[root], next(counter), root))

    came_from = dict()

    g_score = dict()
    for v in adjacency:
        g_score[v] = float("inf")
    g_score[root] = 0

    while not best_candidate_heap.empty():
        _, _, current = best_candidate_heap.get()
        if current == goal:
            break

        visited_set.add(current)
        for neighbor in adjacency[current]:
            if neighbor in visited_set:
                continue

            tentative_g_score = g_score[current] + weights[(current, neighbor)]
            if neighbor not in candidates_set:
                candidates_set.add(neighbor)
            elif tentative_g_score >= g_score[neighbor]:
                continue

            came_from[neighbor] = current
            g_score[neighbor] = tentative_g_score
            new_f_score = g_score[neighbor] + heuristic[neighbor]
            best_candidate_heap.put((new_f_score, next(counter), neighbor))

    return _reconstruct_path(came_from, goal)


def _get_coordinates(key, structure):
    if hasattr(structure, "node_attributes"):
        return structure.node_attributes(key, "xyz")
    if hasattr(structure, "vertex_coordinates"):
        return structure.vertex_coordinates(key)
    raise Exception("Coordinates cannot be found for object of type {}".format(type(structure)))


def _get_points(structure):
    if hasattr(structure, "nodes"):
        return structure.nodes()
    if hasattr(structure, "vertices"):
        return structure.vertices()
    raise Exception("Points cannot be found for object of type {}".format(type(structure)))


def astar_shortest_path(graph: "Graph | Mesh", root: Key, goal: Key) -> list[Key] | None:
    """Find the shortest path between two vertices of a graph or mesh using the A* search algorithm.

    Parameters
    ----------
    graph
        A graph or mesh data structure.
    root
        The identifier of the starting node.
    goal
        The identifier of the ending node.

    Returns
    -------
    list[Key] | None
        The path from root to goal, or None, if no path exists between the vertices.

    References
    ----------
    - [A* search algorithm](https://en.wikipedia.org/wiki/A*_search_algorithm)

    """
    adjacency = graph.adjacency
    weights = {}
    for u, v in graph.edges():
        u_coords = _get_coordinates(u, graph)
        v_coords = _get_coordinates(v, graph)
        distance = distance_point_point(u_coords, v_coords)
        weights[(u, v)] = distance
        weights[(v, u)] = distance

    heuristic = {}
    goal_coords = _get_coordinates(goal, graph)
    points = _get_points(graph)
    for u in points:
        u_coords = _get_coordinates(u, graph)
        heuristic[u] = distance_point_point(u_coords, goal_coords)

    # Graph and Mesh are not generic, so their annotations cannot express that
    # their adjacency keys have the same type as root and goal.
    return astar_lightest_path(
        cast(Mapping[Key, Iterable[Key]], adjacency),
        cast(Mapping[tuple[Key, Key], float], weights),
        cast(Mapping[Key, float], heuristic),
        root,
        goal,
    )


def dijkstra_distances(adjacency: Mapping[Key, Iterable[Key]], weight: Mapping[tuple[Key, Key], float], target: Key) -> dict[Key, float]:
    """Compute Dijkstra distances from all nodes in a graph to one target node.

    Parameters
    ----------
    adjacency
        An adjacency dictionary representing the connectivity of the graph
        by mapping nodes identifiers to neighbour identifiers.
        Examples of valid adjacency dicts are

        * `{0: [1, 2, 3, 4], 1: [0], 2: [0], 3: [0], 4: [0]}`
        * `{0: {1: None, 2: None, 3: None, 4: None}, 1: {0: None}, 2: {0: None}, 3: {0: None}, 4: {0: None}}`

    weight
        A dictionary of edge weights.
    target
        The key of the vertex to which the distances are computed.

    Returns
    -------
    dict[Key, float]
        A dictionary of distances to the target.

    """
    adjacency = {key: set(nbrs) for key, nbrs in adjacency.items()}
    distance = {key: (0 if key == target else 1e17) for key in adjacency}
    tovisit = set(adjacency.keys())
    visited = set()

    while tovisit:
        u = min(tovisit, key=lambda k: distance[k])
        tovisit.remove(u)
        visited.add(u)
        for v in adjacency[u] - visited:
            d = distance[u] + weight[(u, v)]
            if d < distance[v]:
                distance[v] = d
    return distance


def dijkstra_path(
    adjacency: Mapping[Key, Iterable[Key]],
    weight: Mapping[tuple[Key, Key], float],
    source: Key,
    target: Key,
    dist: Mapping[Key, float] | None = None,
) -> list[Key]:
    """Find the shortest path between two nodes of a graph if the weights of the connecting edges are not all the same.

    Parameters
    ----------
    adjacency
        An adjacency dictionary representing the connectivity of the graph
        by mapping nodes identifiers to neighbour identifiers.
        Examples of valid adjacency dicts are

        * `{0: [1, 2, 3, 4], 1: [0], 2: [0], 3: [0], 4: [0]}`
        * `{0: {1: None, 2: None, 3: None, 4: None}, 1: {0: None}, 2: {0: None}, 3: {0: None}, 4: {0: None}}`

    weight
        A dictionary of edge weights.
    source
        The start vertex.
    target
        The end vertex.

    Returns
    -------
    list[Key]
        The shortest path.

    Notes
    -----
    The edge weights should all be positive.
    For a directed graph, set the weights of the reversed edges to `+inf`.
    For an undirected graph, add the same weight for an edge in both directions.

    """
    if source == target:
        return [source]
    if dist is None:
        dist = dijkstra_distances(adjacency, weight, target)
    path = [source]
    node = source
    node = min(adjacency[node], key=lambda nbr: dist[nbr] + weight[(node, nbr)])
    path.append(node)
    while node != target:
        node = min(adjacency[node], key=lambda nbr: dist[nbr] + weight[(node, nbr)])
        path.append(node)
    return path
