from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from copy import deepcopy
from math import sqrt

__all__ = ['dr']


K = [
    [0.0],
    [0.5, 0.5],
    [0.5, 0.0, 0.5],
    [1.0, 0.0, 0.0, 1.0],
]


class Coeff():
    def __init__(self, c):
        self.c = c
        self.a = (1 - c * 0.5) / (1 + c * 0.5)
        self.b = 0.5 * (1 + self.a)


def norm_vector(vector):
    """
    Calculate the length of a vector.

    Parameters
    ----------
    vector : list
        XYZ components of the vector.

    Returns
    -------
    float
        The L2 norm, or *length* of the vector.

    Examples
    --------
    >>>

    """
    return sqrt(sum(axis ** 2 for axis in vector))


def norm_vectors(vectors):
    """
    Calculate the norm of each vector in a list of vectors.

    Parameters
    ----------
    vectors : list
        A list of vectors

    Returns
    -------
    list
        A list with the lengths of all vectors.

    Examples
    --------
    >>>

    """
    return [norm_vector(vector) for vector in vectors]


def adjacency_from_edges(edges):
    """Construct an adjacency dictionary from a set of edges.

    Parameters
    ----------
    edges : list
        A list of index pairs.

    Returns
    -------
    dict
        A dictionary mapping each index in the list of index pairs
        to a list of adjacent indices.

    Examples
    --------
    .. code-block:: python

        #

    """
    adj = {}
    for i, j in iter(edges):
        adj.setdefault(i, []).append(j)
        adj.setdefault(j, []).append(i)
    return adj


def dr(vertices, edges, fixed, loads, qpre, fpre, lpre, linit, E, radius,
       kmax=100, dt=1.0, tol1=1e-3, tol2=1e-6, c=0.1, callback=None, callback_args=None):
    """Implementation of dynamic relaxation with RK integration scheme in pure Python.

    Parameters
    ----------
    vertices : list
        XYZ coordinates of the vertices.
    edges : list
        Connectivity of the vertices.
    fixed : list
        Indices of the fixed vertices.
    loads : list
        XYZ components of the loads on the vertices.
    qpre : list
        Prescribed force densities in the edges.
    fpre : list
        Prescribed forces in the edges.
    lpre : list
        Prescribed lengths of the edges.
    linit : list
        Initial length of the edges.
    E : list
        Stiffness of the edges.
    radius : list
        Radius of the edges.
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

    Examples
    --------
    .. plot::
        :include-source:

        import random

        import compas
        from compas.datastructures import Network
        from compas.plotters import NetworkPlotter
        from compas.utilities import i_to_rgb
        from compas.numerical import dr

        # make a network
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
            'qpre': 1.0,
            'fpre': 0.0,
            'lpre': 0.0,
            'linit': 0.0,
            'E': 0.0,
            'radius': 0.0,
        }

        network.update_default_vertex_attributes(dva)
        network.update_default_edge_attributes(dea)

        # identify the fixed vertices
        # and assign random prescribed force densities to the edges

        for key, attr in network.vertices(True):
            attr['is_fixed'] = network.vertex_degree(key) == 1

        for u, v, attr in network.edges(True):
            attr['qpre'] = 1.0 * random.randint(1, 7)

        # extract numerical data from the datastructure

        vertices = network.get_vertices_attributes(('x', 'y', 'z'))
        edges    = list(network.edges())
        fixed    = network.vertices_where({'is_fixed': True})
        loads    = network.get_vertices_attributes(('px', 'py', 'pz'))
        qpre     = network.get_edges_attribute('qpre')
        fpre     = network.get_edges_attribute('fpre')
        lpre     = network.get_edges_attribute('lpre')
        linit    = network.get_edges_attribute('linit')
        E        = network.get_edges_attribute('E')
        radius   = network.get_edges_attribute('radius')

        # make a plotter for (dynamic) visualization
        # plot the lines of the original configuration of the network as reference

        plotter = NetworkPlotter(network)

        lines = []
        for u, v in network.edges():
            lines.append({
                'start': network.vertex_coordinates(u, 'xy'),
                'end'  : network.vertex_coordinates(v, 'xy'),
                'color': '#cccccc',
                'width': 0.5
            })

        plotter.draw_lines(lines)

        # run the dynamic relaxation
        # update vertices and edges
        # visualize the final geometry
        # color the edges according to the size of the forces
        # set the width of the edges proportional to the internal forces

        xyz, q, f, l, r = dr(vertices, edges, fixed, loads, qpre, fpre, lpre, linit, E, radius,
                             kmax=100)

        for key, attr in network.vertices(True):
            attr['x'] = xyz[key][0]
            attr['y'] = xyz[key][1]
            attr['z'] = xyz[key][2]

        for index, (u, v, attr) in enumerate(network.edges(True)):
            attr['f'] = f[index]
            attr['l'] = l[index]

        fmax = max(network.get_edges_attribute('f'))

        plotter.clear_vertices()
        plotter.clear_edges()

        plotter.draw_vertices(
            facecolor={key: '#000000' for key in network.vertices_where({'is_fixed': True})}
        )

        plotter.draw_edges(
            text={(u, v): '{:.0f}'.format(attr['f']) for u, v, attr in network.edges(True)},
            color={(u, v): i_to_rgb(attr['f'] / fmax) for u, v, attr in network.edges(True)},
            width={(u, v): 10 * attr['f'] / fmax for u, v, attr in network.edges(True)}
        )

        plotter.show()


    See Also
    --------
    * :func:`compas.numerical.dr_numpy`
    * :func:`compas.numerical.drx_numpy`

    """
    if callback:
        if not callable(callback):
            raise Exception('The callback is not callable.')
    # --------------------------------------------------------------------------
    # preprocess
    # --------------------------------------------------------------------------
    n = len(vertices)

    # i_nbrs = {i: [ij[1] if ij[0] == i else ij[0] for ij in edges if i in ij] for i in range(n)}

    i_nbrs = adjacency_from_edges(edges)

    ij_e   = {(i, j): index for index, (i, j) in enumerate(edges)}
    ij_e.update({(j, i): index for (i, j), index in ij_e.items()})

    coeff = Coeff(c)
    ca    = coeff.a
    cb    = coeff.b
    free  = list(set(range(n)) - set(fixed))
    # --------------------------------------------------------------------------
    # attribute arrays
    # --------------------------------------------------------------------------
    X = vertices
    P = loads
    Q = qpre
    # --------------------------------------------------------------------------
    # initial values
    # --------------------------------------------------------------------------
    M  = [sum(0.5 * dt ** 2 * Q[ij_e[(i, j)]] for j in i_nbrs[i]) for i in range(n)]
    V  = [[0.0, 0.0, 0.0] for _ in range(n)]
    R  = [[0.0, 0.0, 0.0] for _ in range(n)]
    dX = [[0.0, 0.0, 0.0] for _ in range(n)]
    # --------------------------------------------------------------------------
    # helpers
    # --------------------------------------------------------------------------

    def update_R():
        for i in range(n):
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

    def rk(X0, V0, steps=2):
        def a(t, V):
            dX = [[V[i][axis] * t for axis in (0, 1, 2)] for i in range(n)]
            for i in free:
                X[i] = [X0[i][axis] + dX[i][axis] for axis in (0, 1, 2)]
            update_R()
            return [[cb * R[i][axis] / M[i] for axis in (0, 1, 2)] for i in range(n)]

        if steps == 2:
            B  = [0.0, 1.0]
            a0 = a(K[0][0] * dt, V0)
            k0 = [[dt * a0[i][axis] for axis in (0, 1, 2)] for i in range(n)]
            a1 = a(K[1][0] * dt, [[V0[i][axis] + K[1][1] * k0[i][axis] for axis in (0, 1, 2)] for i in range(n)])
            k1 = [[dt * a1[i][axis] for axis in (0, 1, 2)] for i in range(n)]
            return [[B[0] * k0[i][axis] + B[1] * k1[i][axis] for axis in (0, 1, 2)] for i in range(n)]

        if steps == 4:
            B  = [1.0 / 6.0, 1.0 / 3.0, 1.0 / 3.0, 1.0 / 6.0]
            a0 = a(K[0][0] * dt, V0)
            k0 = [[dt * a0[i][axis] for axis in (0, 1, 2)] for i in range(n)]
            a1 = a(K[1][0] * dt, [[V0[i][axis] + K[1][1] * k0[i][axis] for axis in (0, 1, 2)] for i in range(n)])
            k1 = [[dt * a1[i][axis] for axis in (0, 1, 2)] for i in range(n)]
            a2 = a(K[2][0] * dt, [[V0[i][axis] + K[2][1] * k0[i][axis] + K[2][2] * k1[i][axis] for axis in (0, 1, 2)] for i in range(n)])
            k2 = [[dt * a2[i][axis] for axis in (0, 1, 2)] for i in range(n)]
            a3 = a(K[3][0] * dt, [[V0[i][axis] + K[3][1] * k0[i][axis] + K[3][2] * k1[i][axis] + K[3][3] * k2[i][axis] for axis in (0, 1, 2)] for i in range(n)])
            k3 = [[dt * a3[i][axis] for axis in (0, 1, 2)] for i in range(n)]
            return [[B[0] * k0[i][axis] +
                     B[1] * k1[i][axis] +
                     B[2] * k2[i][axis] +
                     B[3] * k3[i][axis] for axis in (0, 1, 2)] for i in range(n)]

        raise NotImplementedError

    # --------------------------------------------------------------------------
    # start iterating
    # --------------------------------------------------------------------------
    for k in range(kmax):
        X0 = deepcopy(X)
        V0 = [[ca * V[i][axis] for axis in (0, 1, 2)] for i in range(n)]

        # RK
        dV = rk(X0, V0, steps=4)

        # update
        for i in free:
            V[i]  = [V0[i][axis] + dV[i][axis] for axis in (0, 1, 2)]
            dX[i] = [V[i][axis] * dt for axis in (0, 1, 2)]
            X[i]  = [X0[i][axis] + dX[i][axis] for axis in (0, 1, 2)]

        L = [sum((X[i][axis] - X[j][axis]) ** 2 for axis in (0, 1, 2)) ** 0.5 for i, j in iter(edges)]
        F = [q * l for q, l in zip(Q, L)]

        update_R()

        # crits
        crit1 = max(norm_vectors([R[i] for i in free]))
        crit2 = max(norm_vectors([dX[i] for i in free]))

        # callback
        if callback:
            callback(k, X, (crit1, crit2), callback_args)

        # convergence
        if crit1 < tol1:
            break
        if crit2 < tol2:
            break
    # --------------------------------------------------------------------------
    # update
    # --------------------------------------------------------------------------
    update_R()

    return X, Q, F, L, R


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import random

    import compas
    from compas.datastructures import Network
    from compas.plotters import NetworkPlotter
    from compas.numerical import dr
    from compas.utilities import i_to_rgb

    # make a network
    # and set the default vertex and edge attributes

    network = Network.from_obj(compas.get('lines.obj'))

    dva = {
        'is_fixed': False,
        'x': 0.0,
        'y': 0.0,
        'z': 0.0,
        'px': 0.0,
        'py': 0.0,
        'pz': 0.0,
        'rx': 0.0,
        'ry': 0.0,
        'rz': 0.0,
    }

    dea = {
        'qpre': 1.0,
        'fpre': 0.0,
        'lpre': 0.0,
        'linit': 0.0,
        'E': 0.0,
        'radius': 0.0,
    }

    network.update_default_vertex_attributes(dva)
    network.update_default_edge_attributes(dea)

    # identify the fixed vertices
    # and assign random prescribed force densities to the edges

    for key, attr in network.vertices(True):
        attr['is_fixed'] = network.vertex_degree(key) == 1

    for u, v, attr in network.edges(True):
        attr['qpre'] = 1.0 * random.randint(1, 7)

    # extract numerical data from the datastructure

    vertices = network.get_vertices_attributes(('x', 'y', 'z'))
    edges    = list(network.edges())
    fixed    = network.vertices_where({'is_fixed': True})
    loads    = network.get_vertices_attributes(('px', 'py', 'pz'))
    qpre     = network.get_edges_attribute('qpre')
    fpre     = network.get_edges_attribute('fpre')
    lpre     = network.get_edges_attribute('lpre')
    linit    = network.get_edges_attribute('linit')
    E        = network.get_edges_attribute('E')
    radius   = network.get_edges_attribute('radius')

    # make a plotter for (dynamic) visualization
    # and define a callback function
    # for plotting the intermediate configurations

    plotter = NetworkPlotter(network, figsize=(10, 7), fontsize=6)

    def callback(k, xyz, crits, args):
        print(k)

        plotter.update_vertices()
        plotter.update_edges()
        plotter.update(pause=0.001)

        for key, attr in network.vertices(True):
            attr['x'] = xyz[key][0]
            attr['y'] = xyz[key][1]
            attr['z'] = xyz[key][2]

    # plot the lines of the original configuration of the network
    # as a reference

    lines = []
    for u, v in network.edges():
        lines.append({
            'start': network.vertex_coordinates(u, 'xy'),
            'end'  : network.vertex_coordinates(v, 'xy'),
            'color': '#cccccc',
            'width': 0.5
        })

    plotter.draw_lines(lines)

    # draw the vertices and edges in the starting configuration
    # and pause for a second before starting the dynamic visualization

    plotter.draw_vertices(facecolor={key: '#000000' for key in network.vertices_where({'is_fixed': True})})
    plotter.draw_edges()

    plotter.update(pause=1.0)

    # run the dynamic relaxation

    xyz, q, f, l, r = dr(vertices, edges, fixed, loads, qpre, fpre, lpre, linit, E, radius,
                         kmax=100, callback=callback)

    # update vertices and edges to reflect the end result

    for key, attr in network.vertices(True):
        attr['x'] = xyz[key][0]
        attr['y'] = xyz[key][1]
        attr['z'] = xyz[key][2]

    for index, (u, v, attr) in enumerate(network.edges(True)):
        attr['f'] = f[index]
        attr['l'] = l[index]

    # visualize the final geometry
    # color the edges according to the size of the forces
    # set the width of the edges proportional to the internal forces

    fmax = max(network.get_edges_attribute('f'))

    plotter.clear_vertices()
    plotter.clear_edges()

    plotter.draw_vertices(
        facecolor={key: '#000000' for key in network.vertices_where({'is_fixed': True})}
    )

    plotter.draw_edges(
        text={(u, v): '{:.0f}'.format(attr['f']) for u, v, attr in network.edges(True)},
        color={(u, v): i_to_rgb(attr['f'] / fmax) for u, v, attr in network.edges(True)},
        width={(u, v): 10 * attr['f'] / fmax for u, v, attr in network.edges(True)}
    )

    plotter.update(pause=1.0)
    plotter.show()
