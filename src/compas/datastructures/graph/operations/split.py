from typing import TYPE_CHECKING
from typing import Optional

from ..types import Edge
from ..types import Node

if TYPE_CHECKING:
    from compas.datastructures import Graph


def graph_split_edge(
    graph: "Graph",
    edge: Edge,
    t: float = 0.5,
) -> Optional[Node]:
    """Split an edge by inserting a node along its length.

    Parameters
    ----------
    graph
        A graph data structure.
    edge
        The identifier of the edge to split.
    t
        The position of the inserted node on the edge.

    Returns
    -------
    hashable | None
        The key of the inserted node, or None if the edge does not exist.

    Raises
    ------
    ValueError
        If `t` is not in the range 0-1.
    """
    u, v = edge
    if not graph.has_edge(edge):
        return

    if t <= 0.0:
        raise ValueError("t should be greater than 0.0.")
    if t >= 1.0:
        raise ValueError("t should be smaller than 1.0.")

    # the split node
    x, y, z = graph.edge_point(edge, t)
    w = graph.add_node(x=x, y=y, z=z)

    graph.add_edge(u, w)
    graph.add_edge(w, v)
    graph.delete_edge(edge)

    # return the key of the split node
    return w
