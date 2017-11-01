"""
http://eddmann.com/posts/depth-first-search-and-breadth-first-search-in-python/
"""

from __future__ import print_function

from collections import deque


__author__     = ['Tom Van Mele <vanmelet@ethz.ch>', ]
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


__all__ = [
    'dfs_ordering',
    'dfs_paths',
    'bfs_ordering',
    'bfs_traverse',
    'bfs_paths',
    'shortest_path',
    'dijkstra_distances',
    'dijkstra_path'
]


def dfs_ordering(adjacency, root):
    """
    Return all nodes of a connected component containing 'root' of a network
    represented by an adjacency dictionary.

    This implementation uses a *to visit* stack. The principle of a stack
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

    Returns:
        list: A depth-first ordering of all vertices in the network.

    Examples:
        >>> import compas
        >>> from compas.datastructures import Network
        >>> from compas.topology import depth_first_search as dfs
        >>> network = Network.from_obj(compas.get_data('lines.obj'))
        >>> print(dfs(network, network.get_any_vertex()))

    See Also:
        ...

    """
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


def dfs_paths(adjacency, root, goal):
    """Yield all paths that lead from a root node to a specific goal.

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


def bfs_ordering(adjacency, root):
    """Return a breadth-first ordering of all vertices in an adjacency dictionary
    starting from a chosen root vertex.

    This implementation uses a double-ended queue (deque) to keep track of nodes to visit.
    The principle of a queue is FIFO. In Python, a deque is ideal for removing elements
    from the beginning, i.e. from the 'left'.

    In a breadth-first search, all unvisited neighbours of a node are visited
    first. When a neighbour is visited, its univisited neighbours are added to
    the list of nodes to visit.

    Parameters:
        adjacency (dict): An adjacency dictionary. Each key represents a vertex
            and maps to a list of neighbouring vertex keys.
        root (str): The vertex from which to start the breadth-first search.

    Returns:
        list: A breadth-first ordering of all vertices in the adjacency dict.

    Examples:
        >>>

    Notes:
        By appending the neighbours to the end of the list of nodes to visit,
        and by visiting the nodes at the start of the list first, the network is
        traversed in *breadth-first* order.

    """
    tovisit  = deque([root])
    visited  = set([root])
    ordering = [root]

    while tovisit:
        node = tovisit.popleft()

        for nbr in adjacency[node]:
            if nbr not in visited:
                tovisit.append(nbr)
                visited.add(nbr)
                ordering.append(nbr)

    return ordering


def bfs_traverse(adjacency, root, callback=None):
    tovisit  = deque([root])
    visited  = set([root])

    while tovisit:
        node = tovisit.popleft()

        for nbr in adjacency[node]:
            if nbr not in visited:
                tovisit.append(nbr)
                visited.add(nbr)

                if callback:
                    callback(node, nbr)

    return visited


def bfs_paths(adjacency, root, goal):
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
    list
        The path from root to goal.
    None
        If no path exists between the vertices.

    Examples
    --------

    .. plot::
        :include-source:

        import compas

        from compas.datastructures import Network
        from compas.topology import shortest_path
        from compas.visualization import NetworkPlotter

        network = Network.from_obj(compas.get_data('grid_irregular.obj'))

        adjacency = {key: network.vertex_neighbours(key) for key in network.vertices()}

        start = 21
        end = 2

        path = shortest_path(adjacency, start, end)

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
            width={(u, v): 2.0 for u, v in edges}
        )

        plotter.show()

    """
    try:
        return next(bfs_paths(adjacency, root, goal))
    except StopIteration:
        return None


def dijkstra_distances(adjacency, weight, target):
    """Compute Dijkstra distances from all vertices in a connected set to one target vertex.

    Parameters:
        adjacency (dict): An adjacency dictionary. Each key represents a vertex
            and maps to a list of neighbouring vertex keys.
        weight (dict): A dictionary of edge weights.
        target (str): The key of the vertex to which the distances are computed.

    Returns:
        dict: A dictionary of distances to the target.

    Examples:

        .. plot::
            :include-source:

            import compas

            from compas.datastructures import Network
            from compas.topology import dijkstra_distances
            from compas.visualization import NetworkPlotter
            from compas.utilities import i_to_red

            network = Network.from_obj(compas.get_data('grid_irregular.obj'))

            adjacency = {key: network.vertex_neighbours(key) for key in network.vertices()}

            weight = {(u, v): network.edge_length(u, v) for u, v in network.edges()}
            weight.update({(v, u): weight[(u, v)] for u, v in network.edges()})

            target = 22

            distances = dijkstra_distances(adjacency, weight, target)

            plotter = NetworkPlotter(network)

            dmax = max(distances.values())

            facecolor = {key: i_to_red(distances[key] / dmax) for key in network.vertices()}
            text = {key: '{:.1f}'.format(distances[key]) for key in network.vertices()}

            plotter.draw_vertices(
                text=text,
                facecolor=facecolor,
                radius=0.15
            )
            plotter.draw_edges()

            plotter.show()

    Notes:
        ...

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
            from compas.topology import dijkstra_path
            from compas.visualization import NetworkPlotter

            network = Network.from_obj(compas.get_data('grid_irregular.obj'))

            adjacency = {key: network.vertex_neighbours(key) for key in network.vertices()}

            weight = {(u, v): network.edge_length(u, v) for u, v in network.edges()}
            weight.update({(v, u): weight[(u, v)] for u, v in network.edges()})

            start = 21
            end = 22

            path = dijkstra_path(adjacency, weight, start, end)

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
            from compas.topology import dijkstra_path
            from compas.visualization import NetworkPlotter

            network = Network.from_obj(compas.get_data('grid_irregular.obj'))

            adjacency = {key: network.vertex_neighbours(key) for key in network.vertices()}

            weight = {(u, v): network.edge_length(u, v) for u, v in network.edges()}
            weight.update({(v, u): weight[(u, v)] for u, v in network.edges()})

            weight[(8, 7)] = 1000
            weight[(7, 8)] = 1000

            start = 21
            end = 22

            path = dijkstra_path(adjacency, weight, start, end)

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
# Debugging
# ==============================================================================

if __name__ == '__main__':

    import compas

    from compas.datastructures import Network
    from compas.topology import bfs_paths
    from compas.visualization import NetworkPlotter

    network = Network.from_obj(compas.get('lines.obj'))

    adjacency = {key: network.vertex_neighbours(key) for key in network.vertices()}

    start = 22
    end = 25

    paths = list(dfs_paths(adjacency, start, end))
    path = paths[-1]

    print(paths)

    edges = []
    for i in range(len(path) - 1):
        u = path[i]
        v = path[i + 1]
        if v not in network.edge[u]:
            u, v = v, u
        edges.append([u, v])

    plotter = NetworkPlotter(network)

    plotter.draw_vertices(text='key')
    plotter.draw_edges()

    plotter.draw_vertices(
        text={key: key for key in network.vertices()},
        facecolor={key: '#ff0000' for key in (path[0], path[-1])},
        radius=0.15
    )

    plotter.draw_edges(
        color={(u, v): '#ff0000' for u, v in edges},
        width={(u, v): 2.0 for u, v in edges}
    )

    plotter.show()

    # import compas

    # from compas.datastructures import Network
    # from compas.topology import shortest_path
    # from compas.visualization import NetworkPlotter

    # network = Network.from_obj(compas.get_data('grid_irregular.obj'))

    # adjacency = {key: network.vertex_neighbours(key) for key in network.vertices()}

    # start = 0
    # end = 22

    # path = shortest_path(adjacency, start, end)

    # edges = []
    # for i in range(len(path) - 1):
    #     u = path[i]
    #     v = path[i + 1]
    #     if v not in network.edge[u]:
    #         u, v = v, u
    #     edges.append([u, v])

    # plotter = NetworkPlotter(network)

    # plotter.draw_vertices(
    #     text={key: key for key in network.vertices()},
    #     facecolor={key: '#ff0000' for key in (path[0], path[-1])},
    #     radius=0.15
    # )

    # plotter.draw_edges(
    #     color={(u, v): '#ff0000' for u, v in edges},
    #     width={(u, v): 2.0 for u, v in edges}
    # )

    # plotter.show()

    # import compas

    # from compas.datastructures import Network
    # from compas.topology import dijkstra_distances
    # from compas.visualization import NetworkPlotter
    # from compas.utilities import i_to_red

    # network = Network.from_obj(compas.get_data('grid_irregular.obj'))

    # adjacency = {key: network.vertex_neighbours(key) for key in network.vertices()}

    # weight = {(u, v): network.edge_length(u, v) for u, v in network.edges()}
    # weight.update({(v, u): weight[(u, v)] for u, v in network.edges()})

    # target = 22

    # distances = dijkstra_distances(adjacency, weight, target)

    # plotter = NetworkPlotter(network)

    # dmax = max(distances.values())

    # facecolor = {key: i_to_red(distances[key] / dmax) for key in network.vertices()}
    # text = {key: '{:.1f}'.format(distances[key]) for key in network.vertices()}

    # plotter.draw_vertices(
    #     text=text,
    #     facecolor=facecolor,
    #     radius=0.15
    # )
    # plotter.draw_edges()

    # plotter.show()

    # import compas

    # from compas.datastructures import Network
    # from compas.visualization import NetworkPlotter

    # from compas.topology import dijkstra_path

    # network = Network.from_obj(compas.get('grid_irregular.obj'))

    # adjacency = {key: network.vertex_neighbours(key) for key in network.vertices()}

    # weight = {(u, v): network.edge_length(u, v) for u, v in network.edges()}
    # weight.update({(v, u): weight[(u, v)] for u, v in network.edges()})

    # heavy = [(7, 17), (9, 19)]

    # for u, v in heavy:
    #     weight[(u, v)] = 1000.0
    #     weight[(v, u)] = 1000.0

    # start = 21
    # via = 0
    # end = 22

    # index_key = network.index_key()

    # plotter = NetworkPlotter(network, figsize=(10, 8), fontsize=6)

    # def via_via(via):
    #     path1 = dijkstra_path(adjacency, weight, start, via)
    #     path2 = dijkstra_path(adjacency, weight, via, end)
    #     path = path1 + path2[1:]

    #     edges = []
    #     for i in range(len(path) - 1):
    #         u = path[i]
    #         v = path[i + 1]
    #         if v not in network.edge[u]:
    #             u, v = v, u
    #         edges.append([u, v])

    #     vertexcolor = {}
    #     vertexcolor[start] = '#00ff00'
    #     vertexcolor[end] = '#00ff00'
    #     vertexcolor[via] = '#0000ff'

    #     plotter.clear_vertices()
    #     plotter.clear_edges()

    #     plotter.draw_vertices(text={key: key for key in (start, via, end)},
    #                           textcolor={key: '#ffffff' for key in path[1:-1]},
    #                           facecolor=vertexcolor,
    #                           radius=0.15,
    #                           picker=10)

    #     plotter.draw_edges(color={(u, v): '#ff0000' for u, v in edges},
    #                        width={(u, v): 4.0 for u, v in edges},
    #                        text={(u, v): '{:.1f}'.format(weight[(u, v)]) for u, v in network.edges()},
    #                        fontsize=4.0)

    # def onpick(e):
    #     index = e.ind[0]
    #     via = index_key[index]
    #     via_via(via)
    #     plotter.update()

    # via_via(via)

    # plotter.register_listener(onpick)
    # plotter.show()
