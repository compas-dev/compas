from copy import deepcopy
from array import array


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


__all__ = [
    'network_relax'
]


K = [
    [0.0, ],
    [0.5, 0.5, ],
    [0.5, 0.0, 0.5, ],
    [1.0, 0.0, 0.0, 1.0, ],
]


def relax():
    pass


def mesh_relax():
    pass


def network_relax(network, kmax=100, dt=1.0, tol1=1e-3, tol2=1e-6, c=0.1, callback=None, callback_args=None):
    """Implementation of dynamic relaxation with RK integration scheme in pure Python.

    Parameters
    ----------
    network : Network
        A network object.
    kmax : int, optional
        Maximum number of iterations.
    dt : float, optional
        The time step.
    tol1 : float, optional
        Convergence criterion for the residual forces.
    tol2 : float, optional
        Convergence criterion for the displacements in between interations.
    c : float, optional
        Damping factor for viscous damping.
    callback : callable, optional
        A user-defined callback that is called after every iteration.
    callback_args : tuple, optional
        Additional arguments to be passed to the callback.

    Example
    -------
    .. plot::
        :include-source:

        import compas
        from compas.datastructures import Network
        from compas.visualization import NetworkPlotter
        from compas.geometry import network_relax

        network = Network.from_obj(compas.get('lines.obj'))

        dva = {'is_fixed': False, 'p': [0.0, 0.0, 0.0], 'v': [0.0, 0.0, 0.0]}
        dea = {'q': 1.0}

        network.update_default_vertex_attributes(dva)
        network.update_default_edge_attributes(dea)

        for key, attr in network.vertices(True):
            attr['is_fixed'] = network.is_vertex_leaf(key)

        for index, (u, v, attr) in enumerate(network.edges(True)):
            attr['q'] = index + 1

        lines = []
        for u, v in network.edges():
            lines.append({
                'start' : network.vertex_coordinates(u, 'xy'),
                'end'   : network.vertex_coordinates(v, 'xy'),
                'color' : '#cccccc',
                'width' : 1.0
            })

        plotter = NetworkPlotter(network)
        plotter.draw_lines(lines)

        network_relax(network, kmax=100)

        plotter.draw_vertices(
            facecolor={key: '#ff0000' for key in network.vertices_where({'is_fixed': True})}
        )
        plotter.draw_edges()
        plotter.show()

    """
    if callback:
        if not callable(callback):
            raise Exception('The callback is not callable.')

    # pre-process

    k_i = network.key_index()

    ij_q = dict(zip(network.edges(), network.get_edges_attribute('q', 1.0)))
    ij_q.update({(j, i): q for (i, j), q in ij_q.items()})

    i_nbrs = {k_i[key]: [k_i[nbr] for nbr in network.vertex_neighbours(key)] for key in network.vertices()}

    # initialise

    a = (1 - c * 0.5) / (1 + c * 0.5)
    b = 0.5 * (1 + a)

    n = network.number_of_vertices()

    fixed = [k_i[key] for key in network.vertices() if network.vertex[key]['is_fixed']]
    free  = list(set(range(n)) - set(fixed))
    p     = network.get_vertices_attributes(('px', 'py', 'pz'), [0.0, 0.0, 0.0])
    v     = network.get_vertices_attributes(('vx', 'vy', 'vz'), [0.0, 0.0, 0.0])
    xyz   = network.get_vertices_attributes(('x', 'y', 'z'))

    mass = [
        sum(0.5 * dt ** 2 * network.get_edge_attribute((key, nbr), 'q') for nbr in network.vertex_neighbours(key))
        for key in network.vertices()
    ]
    mass = array('f', mass)

    # helpers

    def rk(xyz0, v0, steps=2):
        """Compute the acceleration of the vertices,
        taking into account two intermediate updates.
        """

        def residual(xyz):
            """Compute the residual forces """
            r = [None] * n
            for i in range(n):
                _x = xyz[i][0]
                _y = xyz[i][1]
                _z = xyz[i][2]

                _f = [0.0, 0.0, 0.0]
                for j in i_nbrs[i]:
                    _q  = ij_q[(i, j)]
                    _xn = xyz[j][0]
                    _yn = xyz[j][1]
                    _zn = xyz[j][2]
                    _f[0] += _q * (_xn - _x)
                    _f[1] += _q * (_yn - _y)
                    _f[2] += _q * (_zn - _z)

                if i in fixed:
                    r[i] = [_f[j] for j in range(3)]
                else:
                    r[i] = [p[i][j] + _f[j] for j in range(3)]

            return r

        def acceleration(v, t):
            dx  = [[v[i][j] * t for j in range(3)] for i in range(n)]
            xyz = [None] * n
            for i in range(n):
                if i in fixed:
                    xyz[i] = xyz0[i]
                else:
                    xyz[i] = [xyz0[i][j] + dx[i][j] for j in range(3)]

            r = residual(xyz)

            return [[b * r[i][j] / mass[i] for j in range(3)] for i in range(n)]

        # integration scheme

        if steps == 2:
            B  = [0.0, 1.0]
            a0 = acceleration(v0, K[0][0] * dt)
            k0 = [[dt * a0[i][j] for j in range(3)] for i in range(n)]
            a1 = acceleration([[v0[i][j] + K[1][1] * k0[i][j] for j in range(3)] for i in range(n)], K[1][0] * dt)
            k1 = [[dt * a1[i][j] for j in range(3)] for i in range(n)]
            dv = [[B[0] * k0[i][j] + B[1] * k1[i][j] for j in range(3)] for i in range(n)]

        elif steps == 4:
            B  = [1.0 / 6.0, 1.0 / 3.0, 1.0 / 3.0, 1.0 / 6.0]
            a0 = acceleration(v0, K[0][0] * dt)
            k0 = [[dt * a0[i][j] for j in range(3)] for i in range(n)]
            a1 = acceleration([[v0[i][j] + K[1][1] * k0[i][j] for j in range(3)] for i in range(n)], K[1][0] * dt)
            k1 = [[dt * a1[i][j] for j in range(3)] for i in range(n)]
            a2 = acceleration([[v0[i][j] + K[2][1] * k0[i][j] + K[2][2] * k1[i][j] for j in range(3)] for i in range(n)], K[2][0] * dt)
            k2 = [[dt * a2[i][j] for j in range(3)] for i in range(n)]
            a3 = acceleration([[v0[i][j] + K[3][1] * k0[i][j] + K[3][2] * k1[i][j] + K[3][3] * k2[i][j] for j in range(3)] for i in range(n)], K[3][0] * dt)
            k3 = [[dt * a3[i][j] for j in range(3)] for i in range(n)]
            dv = [[B[0] * k0[i][j] + B[1] * k1[i][j] + B[2] * k2[i][j] + B[3] * k3[i][j] for j in range(3)] for i in range(n)]

        return dv

    # iterate

    for k in range(kmax):

        xyz0 = deepcopy(xyz)
        v0   = [[a * v[i][j] for j in range(3)] for i in range(n)]
        dv   = rk(xyz0, v0, 4)
        v    = [[v0[i][j] + dv[i][j] for j in range(3)] for i in range(n)]
        dx   = [[v[i][j] * dt for j in range(3)] for i in range(n)]

        for i in free:
            xyz[i] = [xyz0[i][j] + dx[i][j] for j in range(3)]

        # compute residual forces
        # check convergence

        if callback:
            callback(k, callback_args)

            for key, attr in network.vertices(True):
                i = k_i[key]
                attr['x'] = xyz[i][0]
                attr['y'] = xyz[i][1]
                attr['z'] = xyz[i][2]

    # update

    for key, attr in network.vertices(True):
        i = k_i[key]
        attr['x'] = xyz[i][0]
        attr['y'] = xyz[i][1]
        attr['z'] = xyz[i][2]

    for u, v, attr in network.edges(True):
        l = network.edge_length(u, v)
        f = ij_q[(k_i[u], k_i[v])] * l
        attr['f'] = f
        attr['l'] = l


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    import compas
    from compas.datastructures import Network
    from compas.visualization import NetworkPlotter
    from compas.utilities import i_to_rgb

    network = Network.from_obj(compas.get('lines.obj'))

    dva = {
        'is_fixed': False,
        'px': 0.0,
        'py': 0.0,
        'pz': 0.0,
        'vx': 0.0,
        'vy': 0.0,
        'vz': 0.0,
    }
    dea = {'q': 1.0, 'f': 0.0, 'l': 0.0}

    network.update_default_vertex_attributes(dva)
    network.update_default_edge_attributes(dea)

    for key, attr in network.vertices(True):
        attr['is_fixed'] = network.is_vertex_leaf(key)

    for index, (u, v, attr) in enumerate(network.edges(True)):
        attr['q'] = index + 1

    lines = []
    for u, v in network.edges():
        lines.append({
            'start' : network.vertex_coordinates(u, 'xy'),
            'end'   : network.vertex_coordinates(v, 'xy'),
            'color' : '#cccccc',
            'width' : 0.5
        })

    plotter = NetworkPlotter(network, figsize=(10, 6))

    plotter.draw_lines(lines)
    plotter.draw_vertices(facecolor={key: '#000000' for key in network.vertices_where({'is_fixed': True})})
    plotter.draw_edges()

    plotter.update(pause=1.0)

    def callback(k, args):
        plotter.update_vertices()
        plotter.update_edges()
        plotter.update(pause=0.01)

    network_relax(network, kmax=50, callback=callback)

    fmax = max(network.get_edges_attribute('f'))

    plotter.clear_vertices()
    plotter.clear_edges()

    plotter.draw_vertices(
        facecolor={key: '#000000' for key in network.vertices_where({'is_fixed': True})}
    )

    plotter.draw_edges(
        color={(u, v): i_to_rgb(attr['f'] / fmax) for u, v, attr in network.edges(True)},
        width={(u, v): 10 * attr['f'] / fmax for u, v, attr in network.edges(True)}
    )

    plotter.update(pause=1.0)

    plotter.show()
