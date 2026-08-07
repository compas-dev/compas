from itertools import product
from math import cos
from math import pi
from math import sin
from typing import TYPE_CHECKING
from typing import Any
from typing import Iterable
from typing import Mapping
from typing import Optional
from typing import Sequence

from compas.geometry import angle_vectors_xy
from compas.geometry import is_ccw_xy
from compas.geometry import subtract_vectors_xy
from compas.geometry._core.predicates_2 import is_intersection_segment_segment_xy

from .types import Crossing
from .types import Edge
from .types import Node

if TYPE_CHECKING:
    from compas.datastructures import Graph


def graph_is_crossed(graph: "Graph") -> bool:
    """Verify if a graph has crossing edges.

    Parameters
    ----------
    graph
        A graph object.

    Returns
    -------
    bool
        True if the graph has at least one pair of crossing edges.
        False otherwise.

    Notes
    -----
    This algorithm assumes that the graph lies in the XY plane.

    """
    for (u1, v1), (u2, v2) in product(graph.edges(), graph.edges()):
        if u1 == u2 or v1 == v2 or u1 == v2 or u2 == v1:
            continue
        a = graph.node_attributes(u1, "xy")
        b = graph.node_attributes(v1, "xy")
        c = graph.node_attributes(u2, "xy")
        d = graph.node_attributes(v2, "xy")
        if is_intersection_segment_segment_xy((a, b), (c, d)):
            return True
    return False


def _are_edges_crossed(edges: Iterable[Edge], vertices: Mapping[Node, Sequence[float]]) -> bool:
    """Verify whether any two edges cross.

    Parameters
    ----------
    edges
        The edges to check.
    vertices
        A mapping of node identifiers to point coordinates.

    Returns
    -------
    bool
        True if at least one pair of edges crosses.

    """
    for (u1, v1), (u2, v2) in product(edges, edges):
        if u1 == u2 or v1 == v2 or u1 == v2 or u2 == v1:
            continue
        a = vertices[u1]
        b = vertices[v1]
        c = vertices[u2]
        d = vertices[v2]
        if is_intersection_segment_segment_xy((a, b), (c, d)):
            return True
    return False


def graph_count_crossings(graph: "Graph") -> int:
    """Count the number of crossings (pairs of crossing edges) in the graph.

    Parameters
    ----------
    graph
        A graph object.

    Returns
    -------
    int
        The number of crossings.

    Notes
    -----
    This algorithm assumes that the graph lies in the XY plane.

    """
    return len(graph_find_crossings(graph))


def graph_find_crossings(graph: "Graph") -> list[Crossing]:
    """Identify all pairs of crossing edges in a graph.

    Parameters
    ----------
    graph
        A graph object.

    Returns
    -------
    list[tuple[tuple[hashable, hashable], tuple[hashable, hashable]]]
        A list of edge pairs, with each edge represented by two vertex keys.

    Notes
    -----
    This algorithm assumes that the graph lies in the XY plane.

    """
    crossings: set[Crossing] = set()
    for (u1, v1), (u2, v2) in product(graph.edges(), graph.edges()):
        if u1 == u2 or v1 == v2 or u1 == v2 or u2 == v1:
            continue
        if ((u1, v1), (u2, v2)) in crossings:
            continue
        if ((u2, v2), (u1, v1)) in crossings:
            continue
        a = graph.node_attributes(u1, "xy")
        b = graph.node_attributes(v1, "xy")
        c = graph.node_attributes(u2, "xy")
        d = graph.node_attributes(v2, "xy")
        if is_intersection_segment_segment_xy((a, b), (c, d)):
            crossings.add(((u1, v1), (u2, v2)))
    return list(crossings)


def graph_is_xy(graph: "Graph") -> bool:
    """Verify that all nodes of a graph lie in a plane parallel to XY.

    Parameters
    ----------
    graph
        A graph object.

    Returns
    -------
    bool
        True if all nodes have the same Z coordinate.
        False otherwise.

    """
    z = None
    for key in graph.nodes():
        if z is None:
            z = graph.node_attribute(key, "z") or 0.0
        else:
            if z != (graph.node_attribute(key, "z") or 0.0):
                return False
    return True


def graph_is_planar(graph: "Graph") -> bool:
    """Check if the graph is planar.

    Parameters
    ----------
    graph
        A graph object.

    Returns
    -------
    bool
        True if the graph is planar.
        False otherwise.

    Raises
    ------
    ImportError
        If the networkx package is not installed.

    Notes
    -----
    A graph is planar if it can be drawn in the plane without crossing edges.
    If a graph is planar, it can be shown that an embedding of the graph in
    the plane exists, and, furthermore, that straight-line embedding in the plane
    exists.

    """
    import networkx as nx

    return nx.is_planar(graph.to_networkx())


def graph_is_planar_embedding(graph: "Graph") -> bool:
    """Verify that a graph is embedded in the plane without crossing edges.

    Parameters
    ----------
    graph
        A graph object.

    Returns
    -------
    bool
        True if the graph is embedded in the plane without crossing edges.
        False otherwise.

    """
    return graph_is_planar(graph) and graph_is_xy(graph) and not graph_is_crossed(graph)


def graph_embed_in_plane(graph: "Graph", fixed: Optional[Sequence[Node]] = None) -> bool:
    """Embed the graph in the plane.

    Parameters
    ----------
    graph
        A graph object.
    fixed
        Two fixed points.

    Returns
    -------
    bool
        True if the embedding was successful.
        False otherwise.

    Raises
    ------
    ImportError
        If NetworkX is not installed.

    """
    import networkx as nx

    x = graph.nodes_attribute("x") or []
    y = graph.nodes_attribute("y") or []

    if not x or not y:
        return False

    xmin, xmax = min(x), max(x)
    ymin, ymax = min(y), max(y)
    xspan = xmax - xmin
    yspan = ymax - ymin

    edges = [(u, v) for u, v in graph.edges() if not graph.is_leaf(u) and not graph.is_leaf(v)]

    is_embedded = False
    pos: dict[Node, Any] = {}

    count = 100
    while count:
        pos = nx.spring_layout(nx.Graph(edges), iterations=100, scale=max(xspan, yspan))
        if not _are_edges_crossed(edges, pos):
            is_embedded = True
            break
        count -= 1

    if not is_embedded:
        return False

    if not pos:
        return False

    if fixed:
        a, b = fixed
        p0 = graph.node_attributes(a, "xy")
        p1 = graph.node_attributes(b, "xy")
        p2 = pos[b]
        vec0 = subtract_vectors_xy(p1, p0)
        vec1 = subtract_vectors_xy(pos[b], pos[a])
        # rotate
        angle = angle_vectors_xy(vec0, vec1)
        if is_ccw_xy(p0, p1, p2):
            angle = 2 * pi - angle
        cosa = cos(angle)
        sina = sin(angle)
        for key in pos:
            x, y = pos[key]
            pos[key][0] = cosa * x - sina * y
            pos[key][1] = sina * x + cosa * y
        # scale
        l0 = (vec0[0] ** 2 + vec0[1] ** 2) ** 0.5
        l1 = (vec1[0] ** 2 + vec1[1] ** 2) ** 0.5
        scale = l0 / l1
        for key in pos:
            pos[key][0] *= scale
            pos[key][1] *= scale
        # translate
        t = subtract_vectors_xy(p0, pos[a])
        for key in pos:
            pos[key][0] += t[0]
            pos[key][1] += t[1]

    # update graph node coordinates
    for key in graph.nodes():
        if key in pos:
            graph.node_attributes(key, "xy", pos[key])

    return True
