from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.geometry import centroid_points


def graph_smooth_centroid(graph, fixed=None, kmax=100, damping=0.5, callback=None, callback_args=None):
    """Smooth a graph by moving every free node to the centroid of its neighbors.

    Parameters
    ----------
    graph : Mesh
        A graph object.
    fixed : list, optional
        The fixed nodes of the graph.
    kmax : int, optional
        The maximum number of iterations.
    damping : float, optional
        The damping factor.
    callback : callable, optional
        A user-defined callback function to be executed after every iteration.
    callback_args : list, optional
        A list of arguments to be passed to the callback.

    Returns
    -------
    None

    Raises
    ------
    Exception
        If a callback is provided, but it is not callable.

    """
    if callback:
        if not callable(callback):
            raise Exception("Callback is not callable.")

    fixed = fixed or []
    fixed = set(fixed)

    for k in range(kmax):
        key_xyz = {key: graph.node_coordinates(key) for key in graph.nodes()}

        for key, attr in graph.nodes(True):
            if key in fixed:
                continue

            x, y, z = key_xyz[key]

            cx, cy, cz = centroid_points([key_xyz[nbr] for nbr in graph.neighbors(key)])

            attr["x"] += damping * (cx - x)
            attr["y"] += damping * (cy - y)
            attr["z"] += damping * (cz - z)

        if callback:
            callback(k, callback_args)
