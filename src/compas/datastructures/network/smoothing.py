from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry import centroid_points


__all__ = ['network_smooth_centroid']


def network_smooth_centroid(network, fixed=None, kmax=100, damping=1.0, callback=None, callback_args=None):
    """Smooth a network by moving each node to the centroid of its neighbors.

    Parameters
    ----------
    network : Mesh
        A network object.
    fixed : list, optional
        The fixed nodes of the mesh.
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


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    # import compas

    # from compas.datastructures import Network
    # from compas_plotters import NetworkPlotter

    # network = Network.from_obj(compas.get('grid_irregular.obj'))
    # fixed = network.leaves()

    # network_smooth_centroid(network, fixed=fixed)

    # plotter = NetworkPlotter(network, figsize=(8, 5))

    # plotter.draw_nodes(facecolor={key: '#ff0000' for key in fixed})
    # plotter.draw_edges()

    # plotter.show()

    import doctest
    doctest.testmod(globs=globals())
