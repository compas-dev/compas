from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from collections import deque
from compas.utilities import pairwise


__all__ = [
    'depth_first_ordering',
    'breadth_first_ordering',
    'breadth_first_traverse',
    'breadth_first_paths',
    'shortest_path',
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
    >>> import compas
    >>> from compas.datastructures import Network
    >>> from compas.topology import depth_first_search as dfs
    >>> network = Network.from_obj(compas.get('lines.obj'))
    >>> print(dfs(network, network.get_any_vertex()))

    See Also
    --------
    *

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
#     .. plot::
#         :include-source:

#         import compas
#         from compas.datastructures import Mesh
#         from compas.plotters import MeshPlotter
#         from compas.topology import depth_first_tree
#         from compas.utilities import pairwise

#         mesh = Mesh.from_obj(compas.get('faces.obj'))

#         edges = list(mesh.edges())

#         root = mesh.get_any_vertex()

#         ordering, predecessors, paths = depth_first_tree(mesh.adjacency, root)

#         edgecolor = {}
#         edgewidth = {}

#         for u, v in pairwise(paths[0]):
#             if not mesh.has_edge(u, v):
#                 u, v = v, u
#             edgecolor[(u, v)] = '#ff0000'
#             edgewidth[(u, v)] = 3.0

#         for path in paths[1:]:
#             parent = predecessors[path[0]]
#             for u, v in pairwise([parent] + path):
#                 if not mesh.has_edge(u, v):
#                     u, v = v, u
#                 edgecolor[(u, v)] = '#00ff00'
#                 edgewidth[(u, v)] = 3.0

#         plotter = MeshPlotter(mesh, figsize=(10, 7))

#         plotter.draw_vertices(text='key', facecolor={root: '#ff0000'}, radius=0.2)
#         plotter.draw_edges(color=edgecolor, width=edgewidth)

#         plotter.show()

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


def breadth_first_traverse(adjacency, root, callback=None):
    """"""
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
    .. plot::
        :include-source:

        import compas

        from compas.datastructures import Network
        from compas.topology import shortest_path
        from compas.plotters import NetworkPlotter

        network = Network.from_obj(compas.get('grid_irregular.obj'))

        adjacency = {key: network.vertex_neighbors(key) for key in network.vertices()}

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
        return next(breadth_first_paths(adjacency, root, goal))
    except StopIteration:
        return None


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
    .. plot::
        :include-source:

        import compas

        from compas.datastructures import Network
        from compas.topology import dijkstra_distances
        from compas.plotters import NetworkPlotter
        from compas.utilities import i_to_red

        network = Network.from_obj(compas.get('grid_irregular.obj'))

        adjacency = {key: network.vertex_neighbors(key) for key in network.vertices()}

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
    .. plot::
        :include-source:

        import compas

        from compas.datastructures import Network
        from compas.topology import dijkstra_path
        from compas.plotters import NetworkPlotter

        network = Network.from_obj(compas.get('grid_irregular.obj'))

        adjacency = {key: network.vertex_neighbors(key) for key in network.vertices()}

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
        from compas.plotters import NetworkPlotter

        network = Network.from_obj(compas.get('grid_irregular.obj'))

        adjacency = {key: network.vertex_neighbors(key) for key in network.vertices()}

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
# other
# ==============================================================================


# def travel(adjacency, weights, start=None):
#     points = list(adjacency.keys())
#     start = start or points[0]
#     distance = dijkstra_distances(adjacency, weights, start)

#     tovisit = set(adjacency.keys())
#     visited = set()

#     tovisit.remove(start)
#     visited.add(start)

#     path = [start]

#     while tovisit:
#         u = min(tovisit, key=lambda k: distance[k])
#         tovisit.remove(u)
#         visited.add(u)

#         path.append(u)

#     return path


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    testrun = 2

    # ==========================================================================
    # testrun 1
    # ==========================================================================

    # if testrun == 1:
    #     import compas
    #     from compas.datastructures import Mesh
    #     from compas.plotters import MeshPlotter

    #     mesh = Mesh.from_obj(compas.get('faces.obj'))

    #     edges = list(mesh.edges())

    #     root = mesh.get_any_vertex()

    #     print(root)

    #     ordering, predecessors, paths = depth_first_tree(mesh.adjacency, root)

    #     edgecolor = {}
    #     edgewidth = {}

    #     for u, v in pairwise(paths[0]):
    #         if not mesh.has_edge(u, v):
    #             u, v = v, u
    #         edgecolor[(u, v)] = '#ff0000'
    #         edgewidth[(u, v)] = 5.0

    #     for path in paths[1:]:
    #         parent = predecessors[path[0]]
    #         for u, v in pairwise([parent] + path):
    #             if not mesh.has_edge(u, v):
    #                 u, v = v, u
    #             edgecolor[(u, v)] = '#00ff00'
    #             edgewidth[(u, v)] = 5.0

    #     plotter = MeshPlotter(mesh, figsize=(10, 7))

    #     plotter.draw_vertices(text='key', facecolor={key: '#ff0000' for key in (root, )}, radius=0.2)
    #     plotter.draw_edges(color=edgecolor, width=edgewidth)

    #     plotter.show()

    # dynamic traversal to visualize the difference
    # between DFS and BFS

    # ==========================================================================
    # testrun 2
    # ==========================================================================

    if testrun == 2:
        import compas

        from compas.datastructures import Network
        from compas.topology import shortest_path
        from compas.plotters import NetworkPlotter

        network = Network.from_obj(compas.get('grid_irregular.obj'))

        adjacency = {key: network.vertex_neighbors(key) for key in network.vertices()}

        start = 21
        end = 11

        path = shortest_path(adjacency, start, end)

        edges = []
        for i in range(len(path) - 1):
            u = path[i]
            v = path[i + 1]
            if v not in network.edge[u]:
                u, v = v, u
            edges.append([u, v])

        plotter = NetworkPlotter(network, figsize=(10, 8), fontsize=6)

        plotter.draw_vertices(
            text={key: key for key in network.vertices()},
            facecolor={key: '#ff0000' for key in (path[0], path[-1])},
            radius=0.15
        )

        plotter.draw_edges(
            color={(u, v): '#ff0000' for u, v in edges},
            width={(u, v): 5.0 for u, v in edges}
        )

        plotter.show()

    # ==========================================================================
    # testrun 3
    # ==========================================================================

    if testrun == 3:
        import compas

        from compas.datastructures import Network
        from compas.topology import dijkstra_distances
        from compas.plotters import NetworkPlotter
        from compas.utilities import i_to_red

        network = Network.from_obj(compas.get('grid_irregular.obj'))

        adjacency = {key: network.vertex_neighbors(key) for key in network.vertices()}

        weight = {(u, v): network.edge_length(u, v) for u, v in network.edges()}
        weight.update({(v, u): weight[(u, v)] for u, v in network.edges()})

        target = 22

        distances = dijkstra_distances(adjacency, weight, target)

        plotter = NetworkPlotter(network, figsize=(10, 8), fontsize=6)

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

    # ==========================================================================
    # testrun 4
    # ==========================================================================

    if testrun == 4:
        import compas

        from compas.datastructures import Network
        from compas.plotters import NetworkPlotter

        from compas.topology import dijkstra_path

        network = Network.from_obj(compas.get('grid_irregular.obj'))

        adjacency = {key: network.vertex_neighbors(key) for key in network.vertices()}

        weight = {(u, v): network.edge_length(u, v) for u, v in network.edges()}
        weight.update({(v, u): weight[(u, v)] for u, v in network.edges()})

        heavy = [(7, 17), (9, 19)]

        for u, v in heavy:
            weight[(u, v)] = 1000.0
            weight[(v, u)] = 1000.0

        start = 21
        via = 0
        end = 22

        index_key = network.index_key()

        plotter = NetworkPlotter(network, figsize=(10, 8), fontsize=6)

        def via_via(via):
            path1 = dijkstra_path(adjacency, weight, start, via)
            path2 = dijkstra_path(adjacency, weight, via, end)
            path = path1 + path2[1:]

            edges = []
            for i in range(len(path) - 1):
                u = path[i]
                v = path[i + 1]
                if v not in network.edge[u]:
                    u, v = v, u
                edges.append([u, v])

            vertexcolor = {}
            vertexcolor[start] = '#00ff00'
            vertexcolor[end] = '#00ff00'
            vertexcolor[via] = '#0000ff'

            plotter.clear_vertices()
            plotter.clear_edges()

            plotter.draw_vertices(text={key: key for key in (start, via, end)},
                                  textcolor={key: '#ffffff' for key in path[1:-1]},
                                  facecolor=vertexcolor,
                                  radius=0.15,
                                  picker=10)

            plotter.draw_edges(color={(u, v): '#ff0000' for u, v in edges},
                               width={(u, v): 4.0 for u, v in edges},
                               text={(u, v): '{:.1f}'.format(weight[(u, v)]) for u, v in network.edges()},
                               fontsize=4.0)

        def onpick(e):
            index = e.ind[0]
            via = index_key[index]
            via_via(via)
            plotter.update()

        via_via(via)

        plotter.register_listener(onpick)
        plotter.show()
