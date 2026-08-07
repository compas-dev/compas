from typing import TYPE_CHECKING
from typing import Any
from typing import Callable
from typing import Hashable
from typing import Iterable
from typing import Optional

from compas.geometry import centroid_points

if TYPE_CHECKING:
    from compas.datastructures import Graph


def graph_smooth_centroid(
    graph: "Graph",
    fixed: Optional[Iterable[Hashable]] = None,
    kmax: int = 100,
    damping: float = 0.5,
    callback: Optional[Callable[[int, Any], None]] = None,
    callback_args: Any = None,
) -> None:
    """Smooth a graph by moving every free node to the centroid of its neighbors.

    Parameters
    ----------
    graph
        A graph object.
    fixed
        The fixed nodes of the graph.
    kmax
        The maximum number of iterations.
    damping
        The damping factor.
    callback
        A user-defined callback function to be executed after every iteration.
    callback_args
        Additional arguments to pass to the callback.

    Returns
    -------
    None

    Raises
    ------
    TypeError
        If a callback is provided, but it is not callable.

    """
    if callback is not None and not callable(callback):
        raise TypeError("Callback is not callable.")

    fixed_nodes = set(fixed or [])

    for k in range(kmax):
        key_xyz = {key: graph.node_coordinates(key) for key in graph.nodes()}

        for key, attr in graph.nodes(data=True):
            if key in fixed_nodes:
                continue

            neighbors = graph.neighbors(key)
            if not neighbors:
                continue

            x, y, z = key_xyz[key]

            cx, cy, cz = centroid_points([key_xyz[nbr] for nbr in neighbors])

            attr["x"] += damping * (cx - x)
            attr["y"] += damping * (cy - y)
            attr["z"] += damping * (cz - z)

        if callback is not None:
            callback(k, callback_args)
