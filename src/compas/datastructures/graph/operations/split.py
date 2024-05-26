from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


def graph_split_edge(graph, edge, t=0.5):
    """Split and edge by inserting a node along its length.

    Parameters
    ----------
    edge : tuple[hashable, hashable]
        The identifier of the edge to split.
    t : float, optional
        The position of the inserted node on the edge.

    Returns
    -------
    hashable
        The key of the inserted node.

    Raises
    ------
    ValueError
        If `t` is not in the range 0-1.
    Exception
        If the edge is not part of the graph.

    """
    u, v = edge
    if not graph.has_edge(u, v):
        return

    if t <= 0.0:
        raise ValueError("t should be greater than 0.0.")
    if t >= 1.0:
        raise ValueError("t should be smaller than 1.0.")

    # the split node
    x, y, z = graph.edge_point(edge, t)
    w = graph.add_node(x=x, y=y, z=z)

    graph.add_edge((u, w))
    graph.add_edge((w, v))

    if v in graph.edge[u]:
        del graph.edge[u][v]
    elif u in graph.edge[v]:
        del graph.edge[v][u]
    else:
        raise Exception

    # split half-edge UV
    graph.adjacency[u][w] = None
    graph.adjacency[w][v] = None
    del graph.adjacency[u][v]

    # split half-edge VU
    graph.adjacency[v][w] = None
    graph.adjacency[w][u] = None
    del graph.adjacency[v][u]

    # return the key of the split node
    return w
