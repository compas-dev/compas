from __future__ import print_function

from collections import deque


__author__     = ['Tom Van Mele <vanmelet@ethz.ch>', ]
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


__all__ = [
    'network_dfs',
    'network_bfs',
    'network_bfs2',
    'network_dfs_paths',
    'network_bfs_paths',
    'network_shortest_path',
    'network_dijkstra_distances',
    'network_dijkstra_path'
]


# @todo: remove the callbacks
# @todo: add specialised bfs to mesh orientation module
# @todo: move to _graph module


# ==============================================================================
# depth-first
# ==============================================================================


def network_dfs(adjacency, root, callback=None):
    """
    Return all nodes of a connected component containing 'root' of a network
    represented by an adjacency dictionary.

    This implementation uses a 'to visit' stack. The principle of a stack
    is LIFO. In Python, a list is a stack.

    Initially only the root element is on the stack. While there are still
    elements on the stack, the node on top of the stack is 'popped off' and if
    this node was not already visited, its neighbours are added to the stack if
    they hadn't already been visited themselves.

    Since the last element on top of the stack is always popped off, the
    algorithm goes deeper and deeper in the datastructure, until it reaches a
    node without (unvisited) neighbours and then backtracks. Once a new node
    with unvisited neighbours is found, there too it will go as deep as possible
    before backtracking again, and so on. Once there are no more nodes on the
    stack, the entire structure has been traversed.

    Note that this returns a depth-first spanning tree of a connected component
    of the network.

    Parameters:
        adjacency (dict): An adjacency dictionary. Each key represents a vertex
            and maps to a list of neighbouring vertex keys.
        root (str): The vertex from which to start the depth-first search.
        callback (callable): Optional. A function that is called on every node
            when it is found. Default is ``None``.

    Returns:
        list: A depth-first ordering of all vertices in the network.

    Raises:
        AssertionError: If the callback is provided, but is not callable.

    Examples:
        >>> import compas
        >>> network = Network.from_obj(compas.get_data('lines.obj'))
        >>> print(network_dfs(network, network.get_any_vertex()))

    See Also:
        ...

    """
    if callback:
        assert callable(callback), 'The provided callback is not callable: {0}'.format(callback)

    adjacency = {key: set(nbrs) for key, nbrs in iter(adjacency.items())}
    tovisit = [root]
    visited = set()
    tree = []

    while tovisit:
        # pop the last added element from the stack
        node = tovisit.pop()
        if node not in visited:
            # mark the node as visited
            visited.add(node)
            tree.append(node)
            # call the callback
            if callback:
                callback(node)
            # add the unvisited nbrs to the stack
            tovisit.extend(adjacency[node] - visited)

    return tree


# def network_dfs_tree(adjacency, root):
#     adjacency = dict((key, set(nbrs)) for key, nbrs in adjacency.iteritems())
#     tovisit = [(root, [root])]
#     visited = {}
#     while tovisit:
#         # a node to visit
#         # and the nodes that have been visited to get there
#         node, path = tovisit.pop()
#         # add every unvisited nbr
#         # and the path that leads to it
#         for nbr in adjacency[node] - set(path):
#             # if the nbr is the goal, yield the path that leads to it
#             tovisit.append((nbr, path + [nbr]))
#         visited[node] = path
#     return visited


def network_dfs_paths(adjacency, root, goal):
    """
    Yield all paths that lead from a root node to a specific goal.

    The implementation is based on
    http://eddmann.com/posts/depth-first-search-and-breadth-first-search-in-python/
    """
    adjacency = {key: set(nbrs) for key, nbrs in iter(adjacency.items())}
    tovisit = [(root, [root])]

    while tovisit:
        # get the last added node and the path that led to that node
        node, path = tovisit.pop()
        # add every unvisited nbr
        # and the path that leads to it
        for nbr in adjacency[node] - set(path):
            # if the nbr is the goal, yield the path that leads to it
            if nbr == goal:
                yield path + [nbr]
            else:
                tovisit.append((nbr, path + [nbr]))


# ==============================================================================
# depth-first
# ==============================================================================


def network_bfs(adjacency, root, callback=None):
    """Return all nodes of a connected component containing 'root' of a network
    represented by an adjacency dictionary.

    This implementation uses a queue to keep track of nodes to visit.
    The principle of a queue is FIFO. In Python, a deque (double-ended queue) is
    ideal for removing elements from the beginning, i.e. from the 'left'.

    In a breadth-first search, all unvisited neighbours of a node are visited
    first. When a neighbour is visited, its univisited neighbours are added to
    the list of nodes to visit.

    Parameters:
        adjacency (dict): An adjacency dictionary. Each key represents a vertex
            and maps to a list of neighbouring vertex keys.
        root (str): The vertex from which to start the breadth-first search.
        callback (callable): Optional. A function that is called on every node
            when it is found. Default is ``None``.

    Returns:
        list: A breadth-first ordering of all vertices in the network.

    Raises:
        AssertionError: If the callback is provided, but is not callable.

    Examples:
        >>> import compas
        >>> network = Network.from_obj(compas.get_data('lines.obj'))

    Notes:
        By appending the neighbours to the end of the list of nodes to visit,
        and by visiting the nodes at the start of the list first, the network is
        traversed in *breadth-first* order.

    """
    if callback:
        assert callable(callback), 'The provided callback is not callable: {0}'.format(callback)

    tovisit = deque([root])
    tree = [root]
    visited = set(tree)

    while tovisit:
        node = tovisit.popleft()
        # for nbr in adjacency[node] - visited:
        #     tovisit
        for nbr in adjacency[node]:
            if nbr not in visited:
                tovisit.append(nbr)
                visited.add(nbr)
                tree.append(nbr)
                if callback:
                    callback(node, nbr)
    return tree


def network_bfs2(adjacency, root):
    adjacency = {key: set(nbrs) for key, nbrs in iter(adjacency.items())}
    tovisit = deque([root])
    visited = set()

    while tovisit:
        # visit all the neighbours of a node first
        # before moving on to their respective neighbours in the same order
        node = tovisit.popleft()
        if node not in visited:
            visited.add(node)
            # add all the neighbours of the current node that have not yet been visited
            tovisit.extend(adjacency[node] - visited)
    # returning this is pointless
    # since visited is a set
    # and sets have no order
    return visited


def network_bfs_paths(adjacency, root, goal):
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

    Note
    ----
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


def network_shortest_path(adjacency, root, goal):
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
    list
        The path from root to goal.
    None
        If no path exists between the vertices.

    """
    try:
        return next(network_bfs_paths(adjacency, root, goal))
    except StopIteration:
        return None


# ==============================================================================
# dijkstra
# ==============================================================================


def network_dijkstra_distances(adjacency, weight, target):
    """Compute Dijkstra distances to a specific vertex of a network to every other
    vertex of the network.

    Parameters:
        adjacency (dict): An adjacency dictionary. Each key represents a vertex
            and maps to a list of neighbouring vertex keys.
        weight (dict): A dictionary of edge weights.
        target (str): The key of the vertex to which the distances are computed.

    Returns:
        dict: A dictionary of distances from every vertex in the network.

    Examples:
        >>>

    Notes:
        ...

    """
    adjacency = dict((key, set(nbrs)) for key, nbrs in adjacency.items())
    dist = dict((key, 0 if key == target else 1e17) for key in adjacency)
    tovisit = set(adjacency.keys())
    visited = set()
    while tovisit:
        u = min(tovisit, key=lambda k: dist[k])
        tovisit.remove(u)
        visited.add(u)
        for v in adjacency[u] - visited:
            d_uuv = dist[u] + weight[(u, v)]
            if d_uuv < dist[v]:
                dist[v] = d_uuv
    return dist


def network_dijkstra_path(adjacency, weight, source, target, dist=None):
    """Find the shortest path between two vertices if the edge weights are not
    all one.

    Parameters:
        adjacency (dict): An adjacency dictionary. Each key represents a vertex
            and maps to a list of neighbouring vertex keys.
        weight (dict): A dictionary of edge weights.
        source (str): The start vertex.
        target (str): The end vertex.

    Returns:
        list: The shortest path.

    Note:
        The edge weights should all be positive.
        For a directed graph, set the weights of the reversed edges to ``+inf``.
        For an undirected graph, add the same weight for an edge in both directions.

    Examples:

        .. plot::
            :include-source:

            import compas

            from compas.datastructures import Network
            from compas.datastructures import network_dijkstra_path
            from compas.visualization import NetworkPlotter

            network = Network.from_obj(compas.get_data('grid_irregular.obj'))

            weight = dict(((u, v), network.edge_length(u, v)) for u, v in network.edges())
            weight.update({(v, u): weight[(u, v)] for u, v in network.edges()})

            start = 21
            end = 22

            path = network_dijkstra_path(network.adjacency, weight, start, end)

            edges = []
            for i in range(len(path) - 1):
                u = path[i]
                v = path[i + 1]
                if v not in network.edge[u]:
                    u, v = v, u
                edges.append([u, v])

            plotter = NetworkPlotter(network)

            plotter.draw_vertices(
                text={key: key for key in path},
                facecolor={key: '#ff0000' for key in (path[0], path[-1])},
                radius=0.15
            )

            plotter.draw_edges(
                color={(u, v): '#ff0000' for u, v in edges},
                width={(u, v): 2.0 for u, v in edges},
                text={(u, v): '{:.1f}'.format(weight[(u, v)]) for u, v in network.edges()}
            )

            plotter.show()

        .. plot::
            :include-source:

            import compas

            from compas.datastructures import Network
            from compas.datastructures import network_dijkstra_path
            from compas.visualization import NetworkPlotter

            network = Network.from_obj(compas.get_data('grid_irregular.obj'))

            weight = dict(((u, v), network.edge_length(u, v)) for u, v in network.edges())
            weight.update({(v, u): weight[(u, v)] for u, v in network.edges()})

            weight[(8, 7)] = 1000
            weight[(7, 8)] = 1000

            start = 21
            end = 22

            path = network_dijkstra_path(network.adjacency, weight, start, end)

            edges = []
            for i in range(len(path) - 1):
                u = path[i]
                v = path[i + 1]
                if v not in network.edge[u]:
                    u, v = v, u
                edges.append([u, v])

            plotter = NetworkPlotter(network)

            plotter.draw_vertices(
                text={key: key for key in path},
                facecolor={key: '#ff0000' for key in (path[0], path[-1])},
                radius=0.15
            )

            plotter.draw_edges(
                color={(u, v): '#ff0000' for u, v in edges},
                width={(u, v): 2.0 for u, v in edges},
                text={(u, v): '{:.1f}'.format(weight[(u, v)]) for u, v in network.edges()}
            )

            plotter.show()

    """
    if not dist:
        dist = network_dijkstra_distances(adjacency, weight, target)
    path = [source]
    node = source
    node = min(adjacency[node], key=lambda nbr: dist[nbr] + weight[(node, nbr)])
    path.append(node)
    while node != target:
        node = min(adjacency[node], key=lambda nbr: dist[nbr])
        path.append(node)
    return path


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':

    import compas

    from compas.datastructures import Network
    from compas.datastructures import network_dijkstra_path
    from compas.visualization import NetworkPlotter

    network = Network.from_obj(compas.get_data('grid_irregular.obj'))

    weight = {(u, v): 1.0 for u, v in network.edges()}
    weight.update({(v, u): weight[(u, v)] for u, v in network.edges()})

    weight[(7, 17)] = 1000
    weight[(17, 7)] = 1000

    start = 21
    end = 29

    path1 = network_dijkstra_path(network.adjacency, weight, start, end)

    start = 29
    end = 22

    path2 = network_dijkstra_path(network.adjacency, weight, start, end)

    path = path1 + path2[1:]

    edges = []
    for i in range(len(path) - 1):
        u = path[i]
        v = path[i + 1]
        if v not in network.edge[u]:
            u, v = v, u
        edges.append([u, v])

    vertexcolor = {key: '#ff0000' for key in path}
    vertexcolor[21] = '#00ff00'
    vertexcolor[22] = '#00ff00'

    plotter = NetworkPlotter(network)

    plotter.draw_vertices(text={key: key for key in network.vertices()},
                          textcolor={key: '#ffffff' for key in path[1:-1]},
                          facecolor=vertexcolor,
                          radius=0.15)

    plotter.draw_edges(color={(u, v): '#ff0000' for u, v in edges},
                       width={(u, v): 2.0 for u, v in edges},
                       text={(u, v): '{:.1f}'.format(weight[(u, v)]) for u, v in network.edges()})

    plotter.show()
