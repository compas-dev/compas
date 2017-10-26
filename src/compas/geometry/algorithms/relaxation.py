from math import sqrt
from copy import deepcopy
from array import array


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


__all__ = []


K = [
    [0.0, ],
    [0.5, 0.5, ],
    [0.5, 0.0, 0.5, ],
    [1.0, 0.0, 0.0, 1.0, ],
]

# ==============================================================================
# An implementation of DR
# that simply resolves the residual forces at the nodes
# by moving along a damped residual force/movement vector.
# ==============================================================================


# class ForceNetwork(object):

#     # def __init__(self):
#     #     super(ForceNetwork, self).__init__()
#     #     self.update_default_vertex_attributes({
#     #         'p' : [0.0, 0.0, 0.0],
#     #         'v' : [0.0, 0.0, 0.0],
#     #     })
#     #     self.update_default_edge_attributes({})
#     #     self.dt = 1.0

#     def mass(self, key):
#         t = self.dt
#         m = 0.0
#         for nbr in self.vertex_neighbours(key):
#             q = self.get_edge_attribute((key, nbr), 'q')
#             m += 0.5 * t ** 2 * q
#         m = m or 1.0
#         return m

#     def residual(self, key, key_xyz, b, dt=1.0):
#         """Compute the residual force at a vertex with respect to a specific state
#         of the geometry.
#         """
#         nbrs = self.vertex_neighbours(key)

#         # get the coordinates of the node in the frozen geometric state
#         x0, y0, z0 = key_xyz[key]

#         # get the load on the node
#         px, py, pz = self.vertex[key]['p']

#         # initialise the components of the residual force at the node
#         # with the components of the external load
#         rx, ry, rz = px, py, pz

#         for nbr in nbrs:
#             # make sure all edges are from the node to its neighbours
#             if nbr in self.edge[key]:
#                 u, v = key, nbr
#             else:
#                 u, v = nbr, key

#             # get the coordinates of the neighbour
#             # in the frozen geometric state
#             xn, yn, zn = key_xyz[nbr]

#             # compute the length of the vector from the node to the neighbour
#             l = sqrt((xn - x0) ** 2 + (yn - y0) ** 2 + (zn - z0) ** 2)

#             # get the force density of the edge
#             q = self.edge[u][v]['q']

#             # compute the force in the connected edge
#             f = q * l

#             # compute the components of the force vector
#             fx = f * (xn - x0) / l
#             fy = f * (yn - y0) / l
#             fz = f * (zn - z0) / l

#             # add the internal forces to the residual force
#             rx += fx
#             ry += fy
#             rz += fz

#         # set the mass to 1.0 if the mass is zero
#         m = self.mass(key)

#         # compute the acceleration of the point
#         # by dividing the residual force vector by the mass of the node
#         ax = rx / m
#         ay = ry / m
#         az = rz / m

#         return ax, ay, az


# def dr(network, kmax=100, dt=1.0, tol1=1e-3, tol2=1e-6, c=0.1):
#     a = (1 - c * 0.5) / (1 + c * 0.5)
#     b = 0.5 * (1 + a)

#     network.dt = dt

#     fixed = set([key for key in network.vertices() if network.vertex[key]['is_fixed']])

#     for k in range(kmax):
#         key_xyz = {key: network.vertex_coordinates(key) for key in network.vertices()}

#         for key, attr in network.vertices(True):

#             if key in fixed:
#                 continue

#             rx, ry, rz = network.residual(key, key_xyz, b)

#             attr['x'] += c * rx
#             attr['y'] += c * ry
#             attr['z'] += c * rz


def dr(network, kmax=100, dt=1.0, tol1=1e-3, tol2=1e-6, c=0.1):
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

    Example
    -------
    .. plot::
        :include-source:

        import compas
        from compas.datastructures import Network
        from compas.visualization import NetworkPlotter
        from compas.geometry import dr

        network = Network.from_obj(compas.get('lines.obj'))

        dva = {'is_fixed': False, 'p': [0.0, 0.0, 0.0], 'v': [0.0, 0.0, 0.0]}
        dea = {'q': 1.0}

        network.update_default_vertex_attributes(dva)
        network.update_default_edge_attributes(dea)

        for key, attr in network.vertices(True):
            attr['is_fixed'] = network.is_vertex_leaf(key)

        for index, (u, v, attr) in enumerate(network.edges(True)):
            if index % 2 == 0:
                attr['q'] = 5.0

        lines = []
        for u, v in network.edges():
            lines.append({
                'start' : network.vertex_coordinates(u, 'xy'),
                'end'   : network.vertex_coordinates(v, 'xy'),
                'color' : '#cccccc',
                'width' : 1.0
            })

        dr(network, kmax=100)

        plotter = NetworkPlotter(network)

        plotter.draw_lines(lines)
        plotter.draw_vertices(
            facecolor={key: '#ff0000' for key in network.vertices_where({'is_fixed': True})}
        )
        plotter.draw_edges()

        plotter.show()


    """

    # pre-process

    k_i = network.key_index()

    ij_q = dict(zip(network.edges(), network.get_edges_attribute('q')))
    ij_q.update({(j, i): q for (i, j), q in ij_q.items()})

    i_nbrs  = {k_i[key]: [k_i[nbr] for nbr in network.vertex_neighbours(key)] for key in network.vertices()}

    # initialise

    a = (1 - c * 0.5) / (1 + c * 0.5)
    b = 0.5 * (1 + a)

    n = network.number_of_vertices()

    fixed = [k_i[key] for key in network.vertices() if network.vertex[key]['is_fixed']]
    free  = list(set(range(n)) - set(fixed))
    p     = [array('f', attr['p']) for key, attr in network.vertices(True)]
    xyz   = [array('f', [attr['x'], attr['y'], attr['z']]) for key, attr in network.vertices(True)]
    v     = [array('f', attr['v']) for key, attr in network.vertices(True)]

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

    # update

    for key, attr in network.vertices(True):
        i = k_i[key]
        attr['x'] = xyz[i][0]
        attr['y'] = xyz[i][1]
        attr['z'] = xyz[i][2]


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    import compas
    from compas.datastructures import Network
    from compas.visualization import NetworkPlotter

    network = Network.from_obj(compas.get('lines.obj'))

    dva = {'is_fixed': False, 'p': [0.0, 0.0, 0.0], 'v': [0.0, 0.0, 0.0]}
    dea = {'q': 1.0}

    network.update_default_vertex_attributes(dva)
    network.update_default_edge_attributes(dea)

    for key, attr in network.vertices(True):
        attr['is_fixed'] = network.is_vertex_leaf(key)

    for index, (u, v, attr) in enumerate(network.edges(True)):
        if index % 2 == 0:
            attr['q'] = 5.0

    lines = []
    for u, v in network.edges():
        lines.append({
            'start' : network.vertex_coordinates(u, 'xy'),
            'end'   : network.vertex_coordinates(v, 'xy'),
            'color' : '#cccccc',
            'width' : 1.0
        })

    dr(network, kmax=100)

    plotter = NetworkPlotter(network)

    plotter.draw_lines(lines)
    plotter.draw_vertices(
        facecolor={key: '#ff0000' for key in network.vertices_where({'is_fixed': True})}
    )
    plotter.draw_edges()

    plotter.show()
