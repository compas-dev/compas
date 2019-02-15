from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


__all__ = [
    'network_parallelise_edges',
]


def network_parallelise_edges(network, targets, fixed=None, kmax=1, callback=None, callback_args=None):
    """Parallelise the edges of a network to given target vectors.

    Parameters
    ----------
    network : Network
        The network object.
    targets : list
        A list of target vectors.
    fixed : list, optional
        The fixed vertices of the network.
        Default is ``None``.
    kmax : int, optional
        Maximum number of iterations.
        Default is ``1``.
    callback : callable, optional
        A user-defined callback function to be executed after every iteration.
        Default is ``None``.
    callback_args : tuple, optional
        Additional parameters to be passed to the callback.
        Default is ``None``.

    Returns
    -------
    None

    Examples
    --------
    .. code-block:: python

        #

    """
    if callback:
        if not callable(callback):
            raise Exception('The provided callback is not callable.')

    free = list(set(range(network.number_of_vertices())) - set(fixed))
    uv_e = {(u, v): index for index, (u, v) in enumerate(network.edges())}
    uv_e.update({(v, u): index for index, (u, v) in enumerate(network.edges())})

    # the main loop
    for k in range(kmax):
        # current coorinates and lengths
        key_xyz = {key: network.vertex_coordinates(key) for key in network.vertices()}
        lengths = [network.edge_length(u, v) for u, v in network.edges()]
        # the inner loop
        for key in free:
            nbrs = network.vertex_neighbors(key)
            n = float(len(nbrs))
            x, y, z = 0.0, 0.0, 0.0

            for nbr in nbrs:
                e = uv_e[(key, nbr)]
                ax, ay, az = key_xyz[nbr]
                tx, ty, tz = targets[e]
                l = lengths[e]

                if key in network.edge[nbr]:
                    bx = ax + l * tx
                    by = ay + l * ty
                    bz = az + l * tz
                else:
                    bx = ax - l * tx
                    by = ay - l * ty
                    bz = az - l * tz

                x += bx
                y += by
                z += bz

            network.vertex[key]['x'] = x / n
            network.vertex[key]['y'] = y / n
            network.vertex[key]['z'] = z / n


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
