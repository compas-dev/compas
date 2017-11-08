from copy import deepcopy
# from array import array


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
        from compas.plotters import NetworkPlotter
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

    ij_e = {(k_i[u], k_i[v]): index for index, (u, v) in enumerate(network.edges())}
    ij_e.update({(j, i): index for (i, j), index in ij_e.items()})

    i_nbrs = {k_i[key]: [k_i[nbr] for nbr in network.vertex_neighbours(key)] for key in network.vertices()}

    # initialise

    a = (1 - c * 0.5) / (1 + c * 0.5)
    b = 0.5 * (1 + a)

    n = network.number_of_vertices()

    fixed = [k_i[key] for key in network.vertices() if network.vertex[key]['is_fixed']]
    free  = list(set(range(n)) - set(fixed))

    X = network.get_vertices_attributes(('x', 'y', 'z'))
    P = network.get_vertices_attributes(('px', 'py', 'pz'), [0.0, 0.0, 0.0])

    Q = network.get_edges_attribute('qpre', 1.0)

    M = [sum(0.5 * dt ** 2 * Q[ij_e[(i, j)]] for j in i_nbrs[i]) for i in range(n)]

    V = [[0.0, 0.0, 0.0] for _ in range(n)]
    R = [[0.0, 0.0, 0.0] for _ in range(n)]

    # helpers

    def compute_Q():
        pass

    def compute_M():
        pass

    def update_R(X):
        """Compute the residual forces."""
        for i in free:
            x = X[i][0]
            y = X[i][1]
            z = X[i][2]

            f = [0.0, 0.0, 0.0]

            for j in i_nbrs[i]:
                q  = Q[ij_e[(i, j)]]

                f[0] += q * (X[j][0] - x)
                f[1] += q * (X[j][1] - y)
                f[2] += q * (X[j][2] - z)

            R[i] = [P[i][axis] + f[axis] for axis in (0, 1, 2)]

    def compute_dV(X0, V0, steps=2):
        """Compute the acceleration of the vertices, taking into account two intermediate updates.
        """
        def compute_A(V, t):
            dX = [[V[i][axis] * t for axis in (0, 1, 2)] for i in range(n)]

            for i in free:
                X[i] = [X0[i][axis] + dX[i][axis] for axis in (0, 1, 2)]

            update_R(X)

            return [[b * R[i][axis] / M[i] for axis in (0, 1, 2)] for i in range(n)]

        if steps == 2:
            B  = [0.0, 1.0]

            a0 = compute_A(V0, K[0][0] * dt)
            k0 = [[dt * a0[i][axis] for axis in (0, 1, 2)] for i in range(n)]

            a1 = compute_A(
                [[V0[i][axis] +
                  K[1][1] * k0[i][axis] for axis in (0, 1, 2)] for i in range(n)], K[1][0] * dt)

            k1 = [[dt * a1[i][axis] for axis in (0, 1, 2)] for i in range(n)]

            dV = [[B[0] * k0[i][axis] +
                   B[1] * k1[i][axis] for axis in (0, 1, 2)] for i in range(n)]

        elif steps == 4:
            B  = [1.0 / 6.0, 1.0 / 3.0, 1.0 / 3.0, 1.0 / 6.0]

            a0 = compute_A(V0, K[0][0] * dt)
            k0 = [[dt * a0[i][axis] for axis in (0, 1, 2)] for i in range(n)]

            a1 = compute_A(
                [[V0[i][axis] +
                  K[1][1] * k0[i][axis] for axis in (0, 1, 2)] for i in range(n)], K[1][0] * dt)

            k1 = [[dt * a1[i][axis] for axis in (0, 1, 2)] for i in range(n)]

            a2 = compute_A(
                [[V0[i][axis] +
                  K[2][1] * k0[i][axis] +
                  K[2][2] * k1[i][axis] for axis in (0, 1, 2)] for i in range(n)], K[2][0] * dt)

            k2 = [[dt * a2[i][axis] for axis in (0, 1, 2)] for i in range(n)]

            a3 = compute_A(
                [[V0[i][axis] +
                  K[3][1] * k0[i][axis] +
                  K[3][2] * k1[i][axis] +
                  K[3][3] * k2[i][axis] for axis in (0, 1, 2)] for i in range(n)], K[3][0] * dt)

            k3 = [[dt * a3[i][axis] for axis in (0, 1, 2)] for i in range(n)]

            dV = [[B[0] * k0[i][axis] +
                   B[1] * k1[i][axis] +
                   B[2] * k2[i][axis] +
                   B[3] * k3[i][axis] for axis in (0, 1, 2)] for i in range(n)]

        else:
            raise NotImplementedError

        return dV

    # iterate

    for k in range(kmax):

        # compute L
        # compute Qs
        # compute updated mass

        X0 = deepcopy(X)
        V0 = [[a * V[i][axis] for axis in (0, 1, 2)] for i in range(n)]

        dV = compute_dV(X0, V0, 4)

        for i in free:
            V[i] = [V0[i][axis] + dV[i][axis] for axis in (0, 1, 2)]
            X[i] = [X0[i][axis] + V[i][axis] * dt for axis in (0, 1, 2)]

        # compute residual forces
        # check convergence

        if callback:
            callback(k, callback_args)

            for key, attr in network.vertices(True):
                i = k_i[key]
                attr['x'] = X[i][0]
                attr['y'] = X[i][1]
                attr['z'] = X[i][2]

    # update

    update_R(X)

    for key, attr in network.vertices(True):
        i = k_i[key]

        attr['x']  = X[i][0]
        attr['y']  = X[i][1]
        attr['z']  = X[i][2]
        attr['rx'] = R[i][0]
        attr['ry'] = R[i][1]
        attr['rz'] = R[i][2]

    for u, v, attr in network.edges(True):
        i, j = k_i[u], k_i[v]

        l = network.edge_length(u, v)
        f = Q[ij_e[(i, j)]] * l

        attr['f'] = f
        attr['l'] = l


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    import random

    import compas
    from compas.datastructures import Network
    from compas.plotters import NetworkPlotter
    from compas.utilities import i_to_rgb

    # create a network from sample data
    # and set the default vertex and edge attributes

    network = Network.from_obj(compas.get('lines.obj'))

    dva = {
        'is_fixed': False,
        'px': 0.0,
        'py': 0.0,
        'pz': 0.0,
        'rx': 0.0,
        'ry': 0.0,
        'rz': 0.0,
    }
    dea = {
        'qpre'  : 1.0,
        'fpre'  : 0.0,
        'lpre'  : 0.0,
        'l0'    : 0.0,
        'E'     : 0.0,
        'radius': 0.0,
        'q'     : 0.0,
        'f'     : 0.0,
        'l'     : 0.0
    }

    network.update_default_vertex_attributes(dva)
    network.update_default_edge_attributes(dea)

    # fix the vertices with only one neighbour (the *leaves*)
    # assign random force densities to the edges

    for key, attr in network.vertices(True):
        attr['is_fixed'] = network.is_vertex_leaf(key)

    for index, (u, v, attr) in enumerate(network.edges(True)):
        attr['qpre'] = 1.0 * random.randint(1, 7)

    # make a plotter
    # draw the original geometry of the network as lines
    # draw the vertices and edges
    # pause for a second before starting the relaxation

    plotter = NetworkPlotter(network, figsize=(10, 7))

    lines = []
    for u, v in network.edges():
        lines.append({
            'start' : network.vertex_coordinates(u, 'xy'),
            'end'   : network.vertex_coordinates(v, 'xy'),
            'color' : '#cccccc',
            'width' : 0.5
        })

    plotter.draw_lines(lines)
    plotter.draw_vertices(facecolor={key: '#000000' for key in network.vertices_where({'is_fixed': True})})
    plotter.draw_edges()

    plotter.update(pause=1.0)

    # define a callback function for updating the plot
    # and for printing the number of the current iteration

    def callback(k, args):
        print(k)
        plotter.update_vertices()
        plotter.update_edges()
        plotter.update(pause=0.0001)

    # run the relaxation algorithm

    network_relax(network, kmax=100, callback=callback)

    # compute the maximum force in the edges
    # for normalising colors and widths

    fmax = max(network.get_edges_attribute('f'))

    # clear the vertices and edges
    # that were used for visualising the iterations

    plotter.clear_vertices()
    plotter.clear_edges()

    # draw the final geometry
    # with color and width of the edges corresponding to the internal forces

    plotter.draw_vertices(
        facecolor={key: '#000000' for key in network.vertices_where({'is_fixed': True})}
    )

    plotter.draw_edges(
        color={(u, v): i_to_rgb(attr['f'] / fmax) for u, v, attr in network.edges(True)},
        width={(u, v): 10 * attr['f'] / fmax for u, v, attr in network.edges(True)}
    )

    # update the plot

    plotter.update()
    plotter.show()
