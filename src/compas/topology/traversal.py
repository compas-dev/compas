from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

try:
    from queue import PriorityQueue
except ImportError:
    from Queue import PriorityQueue  # type: ignore

from collections import deque

from compas.geometry import distance_point_point

# ==============================================================================
# DFS
# ==============================================================================


def depth_first_ordering(adjacency, root):
    """Compute a depth-first ordering of the nodes of a graph, starting from a root node.

    Parameters
    ----------
    adjacency : dict[hashable, dict[hashable, None]] | dict[hashable, sequence[hashable]]
        An adjacency dictionary representing the connectivity of the graph
        by mapping nodes identifiers to neighbour identifiers.
        Examples of valid adjacency dicts are

        * ``{0: [1, 2, 3, 4], 1: [0], 2: [0], 3: [0], 4: [0]}``
        * ``{0: {1: None, 2: None, 3: None, 4: None}, 1: {0: None}, 2: {0: None}, 3: {0: None}, 4: {0: None}}``

    root : hashable
        The node from which to start the depth-first search.

    Returns
    -------
    list[hashable]
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


# def depth_first_tree(adjacency, root):
#     """Construct a spanning tree using a depth-first search.

#     Parameters
#     ----------
#     adjacency : dict
#         An adjacency dictionary.
#     root : hashable
#         The identifier of the root node.

#     Returns
#     -------
#     list
#         List of nodes in depth-first order.
#     dict
#         Dictionary of predecessors for each of the nodes.
#     list
#         The depth-first paths.

#     Examples
#     --------
#     >>>
#     """
#     adjacency = {key: set(nbrs) for key, nbrs in iter(adjacency.items())}
#     tovisit = [root]
#     visited = set()
#     ordering = []
#     predecessors = {}
#     paths = [[root]]

#     while tovisit:
#         # pop the last added element from the stack
#         node = tovisit.pop()
#         if node not in visited:
#             paths[-1].append(node)
#             # mark the node as visited
#             visited.add(node)
#             ordering.append(node)
#             # add the unvisited nbrs to the stack
#             nodes = adjacency[node] - visited
#             if nodes:
#                 for child in nodes:
#                     predecessors[child] = node
#             else:
#                 paths.append([])
#             tovisit.extend(nodes)
#     if not len(paths[-1]):
#         del paths[-1]
#     return ordering, predecessors, paths


# ==============================================================================
# BFS
# ==============================================================================


def breadth_first_ordering(adjacency, root):
    """Compute a breadth-first ordering of the nodes of a graph, starting from a root node.

    Parameters
    ----------
    adjacency : dict[hashable, dict[hashable, None]] | dict[hashable, sequence[hashable]]
        An adjacency dictionary representing the connectivity of the graph
        by mapping nodes identifiers to neighbour identifiers.
        Examples of valid adjacency dicts are

        * ``{0: [1, 2, 3, 4], 1: [0], 2: [0], 3: [0], 4: [0]}``
        * ``{0: {1: None, 2: None, 3: None, 4: None}, 1: {0: None}, 2: {0: None}, 3: {0: None}, 4: {0: None}}``

    root : hashable
        The node from which to start the breadth-first search.

    Returns
    -------
    list[hashable]
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


def breadth_first_traverse(adjacency, root, callback=None):
    """Traverse an adjacency dict in "breadth-first" order.

    Parameters
    ----------
    adjacency : dict[hashable, dict[hashable, None]] | dict[hashable, sequence[hashable]]
        An adjacency dictionary representing the connectivity of the graph
        by mapping nodes identifiers to neighbour identifiers.
        Examples of valid adjacency dicts are

        * ``{0: [1, 2, 3, 4], 1: [0], 2: [0], 3: [0], 4: [0]}``
        * ``{0: {1: None, 2: None, 3: None, 4: None}, 1: {0: None}, 2: {0: None}, 3: {0: None}, 4: {0: None}}``

    root : hashable
        The identifier of the starting node.
    callback : callable, optional
        A callback function applied to every traversed node and its current neighbour.

    Returns
    -------
    set[hashable]
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


def breadth_first_paths(adjacency, root, goal):
    """Return all paths from root to goal.

    Parameters
    ----------
    adjacency : dict[hashable, dict[hashable, None]] | dict[hashable, sequence[hashable]]
        An adjacency dictionary representing the connectivity of the graph
        by mapping nodes identifiers to neighbour identifiers.
        Examples of valid adjacency dicts are

        * ``{0: [1, 2, 3, 4], 1: [0], 2: [0], 3: [0], 4: [0]}``
        * ``{0: {1: None, 2: None, 3: None, 4: None}, 1: {0: None}, 2: {0: None}, 3: {0: None}, 4: {0: None}}``

    root : hashable
        The identifier of the starting node.
    goal : hashable
        The identifier of the ending node.

    Yields
    ------
    list[hashable]
        A path from root to goal.

    Notes
    -----
    Due to the nature of the search, the first path returned is the shortest.

    """
    adjacency = {key: set(nbrs) for key, nbrs in iter(adjacency.items())}
    tovisit = deque([(root, [root])])
    while tovisit:
        node, path = tovisit.popleft()
        for nbr in adjacency[node] - set(path):
            if nbr == goal:
                yield path + [nbr]
            else:
                tovisit.append((nbr, path + [nbr]))


def breadth_first_tree(adjacency, root):
    """Compute a BFS tree, starting from a root node.

    Parameters
    ----------
    adjacency : dict[hashable, dict[hashable, None]] | dict[hashable, sequence[hashable]]
        An adjacency dictionary representing the connectivity of the graph
        by mapping nodes identifiers to neighbour identifiers.
        Examples of valid adjacency dicts are

        * ``{0: [1, 2, 3, 4], 1: [0], 2: [0], 3: [0], 4: [0]}``
        * ``{0: {1: None, 2: None, 3: None, 4: None}, 1: {0: None}, 2: {0: None}, 3: {0: None}, 4: {0: None}}``

    root : hashable
        Identifier of the root node.

    Returns
    -------
    list[hashable]
        BFS ordering of all nodes.
    dict[hashable, hashable]
        A dict mapping each node to its direct predecessor in the tree.
    list[list[hashable]]
        A traversal path for every node in the graph.

    """
    tovisit = deque([root])
    visited = set([root])
    ordering = [root]
    predecessors = {}
    paths = []
    while tovisit:
        node = tovisit.popleft()
        for nbr in adjacency[node]:
            if nbr not in visited:
                predecessors[nbr] = node
                tovisit.append(nbr)
                visited.add(nbr)
                ordering.append(nbr)
            else:
                path = [node]
                while path[-1] in predecessors:
                    path.append(predecessors[path[-1]])
                paths.append(reversed(path))
    return ordering, predecessors, paths


# ==============================================================================
# shortest
# ==============================================================================


def shortest_path(adjacency, root, goal):
    """Find the shortest path between two vertices of a graph.

    Parameters
    ----------
    adjacency : dict[hashable, dict[hashable, None]] | dict[hashable, sequence[hashable]]
        An adjacency dictionary representing the connectivity of the graph
        by mapping nodes identifiers to neighbour identifiers.
        Examples of valid adjacency dicts are

        * ``{0: [1, 2, 3, 4], 1: [0], 2: [0], 3: [0], 4: [0]}``
        * ``{0: {1: None, 2: None, 3: None, 4: None}, 1: {0: None}, 2: {0: None}, 3: {0: None}, 4: {0: None}}``

    root : hashable
        The identifier of the starting node.
    goal : hashable
        The identifier of the ending node.

    Returns
    -------
    list[hashable] | None
        The path from root to goal, or None, if no path exists between the vertices.

    """
    try:
        return next(breadth_first_paths(adjacency, root, goal))
    except StopIteration:
        return None


# ==============================================================================
# A*
# ==============================================================================


def reconstruct_path(came_from, current):
    if current not in came_from:
        return None
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.append(current)
    total_path.reverse()
    return total_path


def astar_lightest_path(adjacency, weights, heuristic, root, goal):
    """Find the path of least weight between two vertices of a graph using the A* search algorithm.

    Parameters
    ----------
    adjacency : dict[hashable, dict[hashable, None]] | dict[hashable, sequence[hashable]]
        An adjacency dictionary representing the connectivity of the graph
        by mapping nodes identifiers to neighbour identifiers.
        Examples of valid adjacency dicts are

        * ``{0: [1, 2, 3, 4], 1: [0], 2: [0], 3: [0], 4: [0]}``
        * ``{0: {1: None, 2: None, 3: None, 4: None}, 1: {0: None}, 2: {0: None}, 3: {0: None}, 4: {0: None}}``

    weights : dict[tuple[hashable, hashable], float]
        A dictionary of edge weights.
    heuristic : dict[hashable, float]
        A dictionary of guesses of weights of paths from a node to the goal.
    root : hashable
        The start vertex.
    goal : hashable
        The end vertex.

    Returns
    -------
    list[hashable] | None
        The path from root to goal, or None, if no path exists between the vertices.

    References
    ----------
    https://en.wikipedia.org/wiki/A*_search_algorithm

    """
    visited_set = set()

    candidates_set = {root}
    best_candidate_heap = PriorityQueue()
    best_candidate_heap.put((heuristic[root], root))

    came_from = dict()

    g_score = dict()
    for v in adjacency:
        g_score[v] = float("inf")
    g_score[root] = 0

    while not best_candidate_heap.empty():
        _, current = best_candidate_heap.get()
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
            best_candidate_heap.put((new_f_score, neighbor))

    return reconstruct_path(came_from, goal)


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


def astar_shortest_path(graph, root, goal):
    """Find the shortest path between two vertices of a graph or mesh using the A* search algorithm.

    Parameters
    ----------
    graph : :class:`compas.datastructures.Graph` | :class:`compas.datastructures.Mesh`
        A graph or mesh data structure.
    root : hashable
        The identifier of the starting node.
    goal : hashable
        The identifier of the ending node.

    Returns
    -------
    list[hashable] | None
        The path from root to goal, or None, if no path exists between the vertices.

    References
    ----------
    https://en.wikipedia.org/wiki/A*_search_algorithm

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

    return astar_lightest_path(adjacency, weights, heuristic, root, goal)


def dijkstra_distances(adjacency, weight, target):
    """Compute Dijkstra distances from all nodes in a graph to one target node.

    Parameters
    ----------
    adjacency : dict[hashable, dict[hashable, None]] | dict[hashable, sequence[hashable]]
        An adjacency dictionary representing the connectivity of the graph
        by mapping nodes identifiers to neighbour identifiers.
        Examples of valid adjacency dicts are

        * ``{0: [1, 2, 3, 4], 1: [0], 2: [0], 3: [0], 4: [0]}``
        * ``{0: {1: None, 2: None, 3: None, 4: None}, 1: {0: None}, 2: {0: None}, 3: {0: None}, 4: {0: None}}``

    weight : dict[tuple[hashable, hashable], float]
        A dictionary of edge weights.
    target : hashable
        The key of the vertex to which the distances are computed.

    Returns
    -------
    dict[hashable, float]
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


def dijkstra_path(adjacency, weight, source, target, dist=None):
    """Find the shortest path between two nodes of a graph if the weights of the connecting edges are not all the same.

    Parameters
    ----------
    adjacency : dict[hashable, dict[hashable, None]] | dict[hashable, sequence[hashable]]
        An adjacency dictionary representing the connectivity of the graph
        by mapping nodes identifiers to neighbour identifiers.
        Examples of valid adjacency dicts are

        * ``{0: [1, 2, 3, 4], 1: [0], 2: [0], 3: [0], 4: [0]}``
        * ``{0: {1: None, 2: None, 3: None, 4: None}, 1: {0: None}, 2: {0: None}, 3: {0: None}, 4: {0: None}}``

    weight : dict[tuple[hashable, hashable], float]
        A dictionary of edge weights.
    source : hashable
        The start vertex.
    target : hashable
        The end vertex.

    Returns
    -------
    list[hashable]
        The shortest path.

    Notes
    -----
    The edge weights should all be positive.
    For a directed graph, set the weights of the reversed edges to ``+inf``.
    For an undirected graph, add the same weight for an edge in both directions.

    """
    if not dist:
        dist = dijkstra_distances(adjacency, weight, target)
    path = [source]
    node = source
    node = min(adjacency[node], key=lambda nbr: dist[nbr] + weight[(node, nbr)])
    path.append(node)
    while node != target:
        node = min(adjacency[node], key=lambda nbr: dist[nbr] + weight[(node, nbr)])
        path.append(node)
    return path
