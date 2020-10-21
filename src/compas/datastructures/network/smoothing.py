from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry import centroid_points


__all__ = [
    'network_smooth_centroid',
]


def network_smooth_centroid(network, fixed=None, kmax=100, damping=0.5, callback=None, callback_args=None):
    """Smooth a network by moving every free node to the centroid of its neighbors.

    Parameters
    ----------
    network : Mesh
        A network object.
    fixed : list, optional
        The fixed nodes of the network.
    kmax : int, optional
        The maximum number of iterations.
    damping : float, optional
        The damping factor.
    callback : callable, optional
        A user-defined callback function to be executed after every iteration.
    callback_args : list, optional
        A list of arguments to be passed to the callback.

    Raises
    ------
    Exception
        If a callback is provided, but it is not callable.

    Examples
    --------
    >>>

    """
    if callback:
        if not callable(callback):
            raise Exception('Callback is not callable.')

    fixed = fixed or []
    fixed = set(fixed)

    for k in range(kmax):
        key_xyz = {key: network.node_coordinates(key) for key in network.nodes()}

        for key, attr in network.nodes(True):
            if key in fixed:
                continue

            x, y, z = key_xyz[key]

            cx, cy, cz = centroid_points([key_xyz[nbr] for nbr in network.neighbors(key)])

            attr['x'] += damping * (cx - x)
            attr['y'] += damping * (cy - y)
            attr['z'] += damping * (cz - z)

        if callback:
            callback(k, callback_args)
