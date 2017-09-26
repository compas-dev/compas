from compas.geometry import centroid_points
from compas.geometry import center_of_mass_polygon
from compas.geometry import add_vectors
from compas.geometry import subtract_vectors
from compas.geometry import scale_vector
from compas.geometry import length_vector


__author__     = 'Tom Van Mele'
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT'
__email__      = '<vanmelet@ethz.ch>'


__all__ = [
    'network_smooth_mixed',
    'network_smooth_centroid',
    'network_smooth_mass',
    'network_smooth_area',
    'network_smooth_length',
]


def network_smooth_mixed(network,
                         smoothers,
                         lmin=None,
                         lmax=None,
                         fixed=None,
                         kmax=1,
                         d=0.5,
                         callback=None,
                         callback_args=None):
    """Smooth a network using mixed criteria.

    Parameters:
        network (compas.datastructures.network.Network): The network object.
        smoothers (list): A list of smoothing algorithms and their weight.
        lmin (float): Optional.
            Minimum length. Default is ``None``.
        lmax (float): Optional.
            Maximum length. Default is ``None``.
        fixed (list): Optional.
            The fixed vertices of the network. Default is ``None``.
        kmax (int): Optional.
            The maximum number of iterations. Default is ``1``.
        d (float): Optional.
            A damping factor. Default is ``0.5``.
        callback (callable): Optional.
            A user-defined callback function to be executed after every iteration.
            Default is ``None``.

    Raises:
        Exception: If a callback is provided, but not callable.

    Example:

        .. plot::
            :include-source:

            import compas
            from compas.datastructures.network import Network
            from compas.visualization.plotters import NetworkPlotter
            from compas.datastructures.network.algorithms import network_smooth_mixed
            from compas.datastructures.network.algorithms import network_find_faces

            network = Network.from_obj(compas.get_data('grid_irregular.obj'))
            smooth = network.copy()

            network_find_faces(smooth, breakpoints=smooth.leaves())

            network_smooth_mixed(smooth,
                                 [('centroid', 0.5), ('area', 0.5)],
                                 fixed=smooth.leaves(),
                                 kmax=10)

            lines = []
            for u, v, attr in network.edges(True):
                lines.append({
                    'start': network.vertex_coordinates(u, 'xy'),
                    'end'  : network.vertex_coordinates(v, 'xy'),
                    'color': '#cccccc',
                    'width': 1.0
                })

            plotter = NetworkPlotter(smooth)

            plotter.draw_xlines(lines)
            plotter.draw_vertices(radius=0.15, text={key: key for key in smooth.vertices()})
            plotter.draw_edges()

            plotter.show()

    """
    w = sum(weight for smoother, weight in smoothers)
    smoothers = [(smoother, weight / w) for smoother, weight in smoothers]
    fixed     = fixed or []
    fixed     = set(fixed)
    leaves    = set(network.leaves())

    if callback:
        if not callable(callback):
            raise Exception('The callback is not callable.')

    for k in range(kmax):
        key_xyz       = {key: network.vertex_coordinates(key) for key in network.vertices()}
        fkey_centroid = {fkey: network.face_centroid(fkey) for fkey in network.faces()}
        fkey_area     = {fkey: network.face_area(fkey) for fkey in network.faces()}

        for key in network.vertices():
            if key in fixed:
                continue

            xyz0 = key_xyz[key]
            xyzN = [0, 0, 0]

            for smoother, weight in smoothers:

                if smoother == 'centroid':
                    nbrs = network.vertex_neighbours(key)
                    xyz = centroid_points([key_xyz[nbr] for nbr in nbrs])
                    xyzN[0] += weight * xyz[0]
                    xyzN[1] += weight * xyz[1]
                    xyzN[2] += weight * xyz[2]
                    continue

                if smoother == 'area':
                    if key in leaves:
                        nbr   = network.vertex_neighbours(key)[0]
                        fkeys = [network.halfedge[key][nbr], network.halfedge[nbr][key]]
                    else:
                        fkeys = network.vertex_faces(key)

                    A = 0
                    x, y, z = 0, 0, 0

                    for fkey in fkeys:
                        # if fkey == 0:
                        #     continue

                        if fkey is None:
                            continue

                        a = fkey_area[fkey]
                        c = fkey_centroid[fkey]
                        x += a * c[0]
                        y += a * c[1]
                        z += a * c[2]
                        A += a

                    xyzN[0] += weight * x / A
                    xyzN[1] += weight * y / A
                    xyzN[2] += weight * z / A
                    continue

                if smoother == 'length':
                    if lmin and lmax:
                        ep = xyz0
                        points = []

                        for nbr in network.vertex_neighbours(key):
                            sp    = key_xyz[nbr]
                            vec   = subtract_vectors(ep, sp)
                            lvec  = length_vector(vec)
                            scale = max(lmin, min(lvec, lmax))
                            p     = add_vectors(sp, scale_vector(vec, scale / lvec))
                            points.append(p)

                        xyz = centroid_points(points)

                        xyzN[0] += weight * xyz[0]
                        xyzN[1] += weight * xyz[1]
                        xyzN[2] += weight * xyz[2]
                    continue

            attr = network.vertex[key]
            attr['x'] += d * (xyzN[0] - xyz0[0])
            attr['y'] += d * (xyzN[1] - xyz0[1])
            attr['z'] += d * (xyzN[2] - xyz0[2])

        if callback:
            callback(network, k, callback_args)


def network_smooth_centroid(network, fixed=None, kmax=1, d=0.5, callback=None, callback_args=None):
    """Smooth a network using per vertex the centroid of its neighbours.

    Parameters:
        network (compas.datastructures.network.Network): The network object.
        fixed (list): Optional.
            The fixed vertices of the network. Default is ``None``.
        kmax (int): Optional.
            The maximum number of iterations. Default is ``1``.
        d (float): Optional.
            The damping factor. Default is ``0.5``.
        callback (callable): Optional.
            A user-defined callback function to be executed after every iteration.
            Default is ``None``.

    Raises:
        Exception: If a callback is provided, but not callable.

    Example:

        .. plot::
            :include-source:

            import compas
            from compas.datastructures.network import Network
            from compas.visualization.plotters import NetworkPlotter
            from compas.datastructures.network.algorithms import network_smooth_centroid

            network  = Network.from_obj(compas.get_data('grid_irregular.obj'))

            network_smooth_centroid(network, fixed=network.leaves(), kmax=10)

            plotter = NetworkPlotter(network)

            plotter.draw_vertices()
            plotter.draw_edges()

            plotter.show()

    """
    fixed = fixed or []
    fixed = set(fixed)

    if callback:
        if not callable(callback):
            raise Exception('The callback is not callable.')

    for k in range(kmax):
        key_xyz = {key: network.vertex_coordinates(key) for key in network.vertices()}

        for key in network:
            if key in fixed:
                continue

            nbrs       = network.vertex_neighbours(key)
            points     = [key_xyz[nbr] for nbr in nbrs]
            cx, cy, cz = centroid_points(points)
            x, y, z    = key_xyz[key]

            attr       = network.vertex[key]
            attr['x'] += d * (cx - x)
            attr['y'] += d * (cy - y)
            attr['z'] += d * (cz - z)

        if callback:
            callback(network, k, callback_args)


def network_smooth_area(network, fixed=None, kmax=1, d=0.5, callback=None, callback_args=None):
    """Smooth a network using per vertex the centroid of the neighbouring faces, weighted by their respective areas.

    Parameters:
        network (compas.datastructures.network.Network): The network object.
        fixed (list): Optional.
            The fixed vertices of the network. Default is ``None``.
        kmax (int): Optional.
            The maximum number of iterations. Default is ``1``.
        d (float): Optional.
            The damping factor. Default is ``0.5``.
        callback (callable): Optional.
            A user-defined callback function to be executed after every iteration.
            Default is ``None``.

    Raises:
        Exception: If a callback is provided, but not callable.

    Example:

        .. plot::
            :include-source:

            import compas
            from compas.datastructures.network import Network
            from compas.visualization.plotters import NetworkPlotter
            from compas.datastructures.network.algorithms import network_find_faces
            from compas.datastructures.network.algorithms import network_smooth_area

            network  = Network.from_obj(compas.get_data('grid_irregular.obj'))

            network_find_faces(network, network.leaves())
            network_smooth_area(network, fixed=network.leaves(), kmax=10)

            plotter = NetworkPlotter(network)

            plotter.draw_vertices()
            plotter.draw_edges()

            plotter.show()

    """
    fixed  = fixed or []
    fixed  = set(fixed)
    leaves = network.leaves()
    leaves = set(leaves)

    if callback:
        if not callable(callback):
            raise Exception('The callback is not callable.')

    for k in range(kmax):
        key_xyz       = {key: network.vertex_coordinates(key) for key in network.vertices()}
        fkey_centroid = {fkey: network.face_centroid(fkey) for fkey in network.faces()}
        fkey_area     = {fkey: network.face_area(fkey) for fkey in network.faces()}

        for key in network:
            if key in fixed:
                continue

            if key in leaves:
                nbr   = network.vertex_neighbours(key)[0]
                fkeys = [network.halfedge[key][nbr], network.halfedge[nbr][key]]
            else:
                fkeys = network.vertex_faces(key)

            A = 0
            x, y, z = 0, 0, 0

            for fkey in fkeys:
                # networks have an outside face...
                # if fkey == 0:
                #     continue

                if fkey is None:
                    continue

                a  = fkey_area[fkey]
                c  = fkey_centroid[fkey]
                x += a * c[0]
                y += a * c[1]
                z += a * c[2]
                A += a

            x /= A
            y /= A
            z /= A

            x0, y0, z0 = key_xyz[key]

            attr = network.vertex[key]
            attr['x'] += d * (x - x0)
            attr['y'] += d * (y - y0)
            attr['z'] += d * (z - z0)

        if callback:
            callback(network, k, callback_args)


def network_smooth_mass(network, fixed=None, kmax=1, d=0.5, callback=None, callback_args=None):
    """Smooth a network using per vertex the center of mass of the polygon formed by the neighbouring vertices.

    Parameters:
        network (compas.datastructures.network.Network): The network object.
        fixed (list): Optional.
            The fixed vertices of the network. Default is ``None``.
        kmax (int): Optional.
            The maximum number of iterations. Default is ``1``.
        d (float): Optional.
            The damping factor. Default is ``0.5``.
        callback (callable): Optional.
            A user-defined callback function to be executed after every iteration.
            Default is ``None``.

    Raises:
        Exception: If a callback is provided, but not callable.

    Example:

        .. plot::
            :include-source:

            import compas
            from compas.datastructures.network import Network
            from compas.visualization.plotters import NetworkPlotter
            from compas.datastructures.network.algorithms import network_find_faces
            from compas.datastructures.network.algorithms import network_smooth_mass

            network  = Network.from_obj(compas.get_data('grid_irregular.obj'))

            network_find_faces(network, network.leaves())
            network_smooth_mass(network, fixed=network.leaves(), kmax=10)

            plotter = NetworkPlotter(network)

            plotter.draw_vertices()
            plotter.draw_edges()

            plotter.show()

    """
    fixed = fixed or []
    fixed = set(fixed)

    if callback:
        if not callable(callback):
            raise Exception('The callback is not callable.')

    for k in range(kmax):
        key_xyz = {key: network.vertex_coordinates(key) for key in network.vertices()}

        for key in network:
            if key in fixed:
                continue

            nbrs       = network.vertex_neighbours(key, ordered=True)
            points     = [key_xyz[nbr] for nbr in nbrs]
            cx, cy, cz = center_of_mass_polygon(points)
            x, y, z    = key_xyz[key]
            attr       = network.vertex[key]
            attr['x'] += d * (cx - x)
            attr['y'] += d * (cy - y)
            attr['z'] += d * (cz - z)

        if callback:
            callback(network, k, callback_args)


def network_smooth_length(network, lmin, lmax, fixed=None, kmax=1, d=0.5, callback=None, callback_args=None):
    fixed = fixed or []
    fixed = set(fixed)

    if callback:
        if not callable(callback):
            raise Exception('The callback is not callable.')

    for k in range(kmax):
        key_xyz = {key: network.vertex_coordinates(key) for key in network.vertices()}

        for key in network:
            if key in fixed:
                continue

            ep = key_xyz[key]
            points = []

            for nbr in network.vertex_neighbours(key):
                sp    = key_xyz[nbr]
                vec   = subtract_vectors(ep, sp)
                lvec  = length_vector(vec)
                scale = max(lmin, min(lvec, lmax))
                p     = add_vectors(sp, scale_vector(vec, scale / lvec))
                points.append(p)

            x, y, z = centroid_points(points)

            attr = network.vertex[key]
            attr['x'] += d * (x - ep[0])
            attr['y'] += d * (y - ep[1])
            attr['z'] += d * (z - ep[2])

        if callback:
            callback(network, k, callback_args)


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':

    import compas

    from compas.datastructures.network import Network
    from compas.datastructures.network.algorithms import network_find_faces

    from compas.visualization.plotters.networkplotter import NetworkPlotter

    network = Network.from_obj(compas.get_data('grid_irregular.obj'))
    smooth = network.copy()

    fixed = smooth.leaves()

    # find_network_faces(smooth, breakpoints=fixed)

    plotter = NetworkPlotter(smooth)

    # draw the orginal network
    plotter.draw_xlines([{'start': network.vertex_coordinates(u, 'xy'),
                          'end': network.vertex_coordinates(v, 'xy'),
                          'color': '#cccccc'} for u, v in network.edges()])

    # draw the smooth network
    # and visualise the smoothing process
    plotter.draw_vertices(facecolor={key: '#ff0000' for key in fixed},
                          edgecolor='#000000',
                          radius=0.15)

    plotter.draw_edges()

    def callback(network, k, args):
        plotter, = args
        plotter.update_vertices()
        plotter.update_edges()
        plotter.update(0.1)

    network_smooth_centroid(smooth,
                            fixed=fixed,
                            kmax=10,
                            callback=callback,
                            callback_args=(plotter, ))

    plotter.show()
