from typing import TYPE_CHECKING
from typing import Hashable
from typing import Iterable
from typing import Optional
from typing import Sequence

from compas.itertools import pairwise
from compas.tolerance import TOL

if TYPE_CHECKING:
    from compas.datastructures import Graph


def graph_join_edges(graph: "Graph", key: Hashable) -> None:
    """Join the edges incidental on the given node, if there are exactly two incident edges.

    Parameters
    ----------
    graph
        A graph data structure.
    key
        The node identifier.

    Returns
    -------
    None
        The graph is modified in place.

    Notes
    -----
    A new edge is created to replace the two joined edges.
    The attributes of the joined edges are not transferred to the new edge.
    Therefore, the new edge has only default edge attributes.

    """
    nbrs = graph.neighbors(key)
    if len(nbrs) != 2:
        return
    a, b = nbrs
    graph.delete_node(key)
    # set attributes based on average of two joining edges?
    graph.add_edge(a, b)


def graph_polylines(
    graph: "Graph",
    splits: Optional[Iterable[Sequence[float]]] = None,
) -> list[list[list[float]]]:
    """Join graph edges into polylines.

    The polylines stop at points with a valency different from 2 in the graph of line.
    Optional splits can be included.

    Parameters
    ----------
    graph
        A graph.
    splits
        List of point coordinates for polyline splits.

    Returns
    -------
    list[list[[float, float, float]]]
        The joined polylines.
        If a polyline is closed, the two extremities are the same.

    Examples
    --------
    Joining the lines (a, b), (b, c), (c, d), (c, e) and (e, f),
    where a ... f are different point coordinates.
    This will result in the following polylines (a, b, c), (c, d) and (c, e, f).

    >>> from compas.datastructures import Graph
    >>> a = [0.0, 0.0, 0.0]
    >>> b = [1.0, 0.0, 0.0]
    >>> c = [2.0, 0.0, 0.0]
    >>> d = [2.0, 1.0, 0.0]
    >>> e = [3.0, 0.0, 0.0]
    >>> f = [4.0, 0.0, 0.0]
    >>> lines = [(a, b), (b, c), (c, d), (c, e), (e, f)]
    >>> graph = Graph.from_lines(lines)
    >>> len(graph_polylines(graph)) == 3
    True

    """
    # geometric keys of split points
    if splits is None:
        splits = []
    stop_geom_keys = {TOL.geometric_key(xyz) for xyz in splits}

    polylines = []
    edges_to_visit = set(graph.edges())

    # initiate a polyline from an unvisited edge
    while edges_to_visit:
        polyline = list(edges_to_visit.pop())

        # get adjacent edges until the polyline is closed...
        while polyline[0] != polyline[-1]:
            # ... or until both end are non-two-valent vertices
            if len(graph.neighbors(polyline[-1])) != 2 or TOL.geometric_key(graph.node_coordinates(polyline[-1])) in stop_geom_keys:
                polyline = list(reversed(polyline))
                if len(graph.neighbors(polyline[-1])) != 2 or TOL.geometric_key(graph.node_coordinates(polyline[-1])) in stop_geom_keys:
                    break

            # add next edge
            polyline.append([nbr for nbr in graph.neighbors(polyline[-1]) if nbr != polyline[-2]][0])

        # delete polyline edges from the list of unvisited edges
        for u, v in pairwise(polyline):
            if (u, v) in edges_to_visit:
                edges_to_visit.remove((u, v))
            elif (v, u) in edges_to_visit:
                edges_to_visit.remove((v, u))

        polylines.append(polyline)

    return [[graph.node_coordinates(vkey) for vkey in polyline] for polyline in polylines]
