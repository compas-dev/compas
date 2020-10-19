from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

try:
    from queue import PriorityQueue
except ImportError:
    from Queue import PriorityQueue

from collections import deque

from compas.geometry import distance_point_point


__all__ = [
    'depth_first_ordering',
    'breadth_first_ordering',
    'breadth_first_traverse',
    'breadth_first_paths',
    'shortest_path',
    'astar_shortest_path',
    'dijkstra_distances',
    'dijkstra_path'
]


# ==============================================================================
# DFS
# ==============================================================================


def depth_first_ordering(adjacency, root):
    """Compute depth-first ordering of connected vertices.

    Parameters
    ----------
    adjacency : dict
        An adjacency dictionary. Each key represents a vertex
        and maps to a list of neighboring vertex keys.
    root : str
        The vertex from which to start the depth-first search.

    Returns
    -------
    list
        A depth-first ordering of all vertices in the network.

    Notes
    -----
    Return all nodes of a connected component containing 'root' of a network
    represented by an adjacency dictionary.

    This implementation uses a *to visit* stack. The principle of a stack
    is LIFO. In Python, a list is a stack.

    Initially only the root element is on the stack. While there are still
    elements on the stack, the node on top of the stack is 'popped off' and if
    this node was not already visited, its neighbors are added to the stack if
    they hadn't already been visited themselves.

    Since the last element on top of the stack is always popped off, the
    algorithm goes deeper and deeper in the datastructure, until it reaches a
    node without (unvisited) neighbors and then backtracks. Once a new node
    with unvisited neighbors is found, there too it will go as deep as possible
    before backtracking again, and so on. Once there are no more nodes on the
    stack, the entire structure has been traversed.

    Note that this returns a depth-first spanning tree of a connected component
    of the network.

    Examples
    --------
    >>>
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
    """Return a breadth-first ordering of all vertices in an adjacency dictionary
    reachable from a chosen root vertex.

    Parameters
    ----------
    adjacency : dict
        An adjacency dictionary. Each key represents a vertex
        and maps to a list of neighboring vertex keys.
    root : str
        The vertex from which to start the breadth-first search.

    Returns
    -------
    list
        A breadth-first ordering of all vertices in the adjacency dict.

    Notes
    -----
    This implementation uses a double-ended queue (deque) to keep track of nodes to visit.
    The principle of a queue is FIFO. In Python, a deque is ideal for removing elements
    from the beginning, i.e. from the 'left'.

    In a breadth-first search, all unvisited neighbors of a node are visited
    first. When a neighbor is visited, its univisited neighbors are added to
    the list of nodes to visit.

    By appending the neighbors to the end of the list of nodes to visit,
    and by visiting the nodes at the start of the list first, the network is
    traversed in *breadth-first* order.

    Examples
    --------
    >>>
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
    adjacency : dict
        Map of every node to a list of neighbouring nodes.
    root : int
        The identifier of the starting node.
    callback : callable, optional
        A callback function applied to every traversed node and its current neighbour.

    Returns
    -------
    set
        The visited nodes.

    Examples
    --------
    >>>
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
    adjacency : dict
        An adjacency dictionary.
    root : hashable
        The identifier of the starting node.
    goal : hashable
        The identifier of the ending node.

    Yields
    ------
    list
        A path from root to goal.

    Notes
    -----
    Due to the nature of the search, the first path returned is the shortest.

    Examples
    --------
    >>>
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
    """Find the shortest path between two vertices of a network.

    Parameters
    ----------
    adjacency : dict
        An adjacency dictionary.
    root : hashable
        The identifier of the starting node.
    goal : hashable
        The identifier of the ending node.

    Returns
    -------
    list, None
        The path from root to goal, or None, if no path exists between the vertices.

    Examples
    --------
    >>>
    """
    try:
        return next(breadth_first_paths(adjacency, root, goal))
    except StopIteration:
        return None


# ==============================================================================
# A*
# ==============================================================================


def reconstruct_path(came_from, current):
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.append(current)
    total_path.reverse()
    return total_path


def astar_shortest_path(network, root, goal):
    """Find the shortest path between two vertices of a network using the A* search algorithm.

    Parameters
    ----------
    network : instance of the Network class
    root : hashable
        The identifier of the starting node.
    goal : hashable
        The identifier of the ending node.

    Returns
    -------
    list, None
        The path from root to goal, or None, if no path exists between the vertices.

    Examples
    --------
    >>>

    References
    ----------
    https://en.wikipedia.org/wiki/A*_search_algorithm
    """
    root_coords = network.vertex_coordinates(root)
    goal_coords = network.vertex_coordinates(goal)

    # The set of nodes already evaluated
    visited_set = set()

    # The set of currently discovered nodes that are not evaluated yet.
    # Initially, only the start node is known.
    candidates_set = {root}
    best_candidate_heap = PriorityQueue()
    best_candidate_heap.put((0, root))

    # For each node, which node it can most efficiently be reached from.
    # If a node can be reached from many nodes, came_from will eventually contain the
    # most efficient previous step.
    came_from = dict()

    # g_score is a dict mapping node index to the cost of getting from the root node to that node.
    # The default value is Infinity.
    # The cost of going from start to start is zero.
    g_score = dict()

    for v in network.vertices():
        g_score[v] = float("inf")

    g_score[root] = 0

    # For each node, the total cost of getting from the start node to the goal
    # by passing by that node. That value is partly known, partly heuristic.
    # The default value of f_score is Infinity
    f_score = dict()

    for v in network.vertices():
        f_score[v] = float("inf")

    # For the first node, that value is completely heuristic.
    f_score[root] = distance_point_point(root_coords, goal_coords)

    while not best_candidate_heap.empty():
        _, current = best_candidate_heap.get()
        if current == goal:
            break

        visited_set.add(current)
        current_coords = network.vertex_coordinates(current)
        for neighbor in network.vertex_neighbors(current):
            if neighbor in visited_set:
                continue  # Ignore the neighbor which is already evaluated.

            # The distance from start to a neighbor
            neighbor_coords = network.vertex_coordinates(neighbor)
            tentative_gScore = g_score[current] + distance_point_point(current_coords, neighbor_coords)
            if neighbor not in candidates_set:  # Discover a new node
                candidates_set.add(neighbor)
            elif tentative_gScore >= g_score[neighbor]:
                continue

            # This path is the best until now. Record it!
            came_from[neighbor] = current
            g_score[neighbor] = tentative_gScore
            new_fscore = g_score[neighbor] + distance_point_point(neighbor_coords, goal_coords)
            f_score[neighbor] = new_fscore
            best_candidate_heap.put((new_fscore, neighbor))

    return reconstruct_path(came_from, goal)


def dijkstra_distances(adjacency, weight, target):
    """Compute Dijkstra distances from all vertices in a connected set to one target vertex.

    Parameters
    ----------
    adjacency : dict
        An adjacency dictionary. Each key represents a vertex
        and maps to a list of neighboring vertex keys.
    weight : dict
        A dictionary of edge weights.
    target : str
        The key of the vertex to which the distances are computed.

    Returns
    -------
    dict
        A dictionary of distances to the target.

    Notes:
        ...

    Examples
    --------
    >>>
    """
    adjacency = {key: set(nbrs) for key, nbrs in adjacency.items()}
    distance = {key: (0 if key == target else 1e+17) for key in adjacency}
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
    """Find the shortest path between two vertices if the edge weights are not
    all the same.

    Parameters
    ----------
    adjacency : dict
        An adjacency dictionary. Each key represents a vertex
        and maps to a list of neighboring vertex keys.
    weight : dict
        A dictionary of edge weights.
    source : str
        The start vertex.
    target : str
        The end vertex.

    Returns
    -------
    list
        The shortest path.

    Notes
    -----
    The edge weights should all be positive.
    For a directed graph, set the weights of the reversed edges to ``+inf``.
    For an undirected graph, add the same weight for an edge in both directions.

    Examples
    --------
    >>>
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


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
