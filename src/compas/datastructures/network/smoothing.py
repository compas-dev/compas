from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry import centroid_points


__all__ = ['network_smooth_centroid']


def network_smooth_centroid(network, fixed=None, kmax=100, damping=1.0, callback=None, callback_args=None):
    """Smooth a network by moving each vertex to the centroid of its neighbors.

    Parameters
    ----------
    network : Mesh
        A network object.
    fixed : list, optional
        The fixed vertices of the mesh.
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
    .. plot::
        :include-source:

        import compas

        from compas.datastructures import Network
        from compas.datastructures import network_smooth_centroid
        from compas.plotters import NetworkPlotter

        network = Network.from_obj(compas.get('grid_irregular.obj'))
        fixed = [key for key in network.vertices() if network.vertex_degree(key) == 1]

        network_smooth_centroid(network, fixed=fixed)

        plotter = NetworkPlotter(network)

        plotter.draw_vertices(facecolor={key: '#ff0000' for key in fixed})
        plotter.draw_edges()

        plotter.show()

    """
    if callback:
        if not callable(callback):
            raise Exception('Callback is not callable.')

    fixed = fixed or []
    fixed = set(fixed)

    for k in range(kmax):
        key_xyz = {key: network.vertex_coordinates(key) for key in network.vertices()}

        for key, attr in network.vertices(True):
            if key in fixed:
                continue

            x, y, z = key_xyz[key]

            cx, cy, cz = centroid_points([key_xyz[nbr] for nbr in network.vertex_neighbors(key)])

            attr['x'] += damping * (cx - x)
            attr['y'] += damping * (cy - y)
            attr['z'] += damping * (cz - z)

        if callback:
            callback(k, callback_args)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
