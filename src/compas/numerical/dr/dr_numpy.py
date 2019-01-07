from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas

try:
    from numpy import array
    from numpy import isnan
    from numpy import isinf
    from numpy import ones
    from numpy import zeros
    from scipy.linalg import norm
    from scipy.sparse import diags

except ImportError:
    compas.raise_if_not_ironpython()

from compas.numerical import connectivity_matrix
from compas.numerical import normrow


__all__ = ['dr_numpy']


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


# def dr_numpy_xfunc(data):
#     # this makes no sense
#     # the network is not aware of all these attributes
#     # => define a custom network locally that meets the requirements of the algorithm
#     from compas.datastructures import Network

#     network = Network.from_data(data)

#     vertices = network.get_vertices_attributes(('x', 'y', 'z'))
#     edges    = list(network.edges())
#     fixed    = network.vertices_where({'is_fixed': True})
#     loads    = network.get_vertices_attributes(('px', 'py', 'pz'))
#     qpre     = network.get_edges_attribute('qpre')
#     fpre     = network.get_edges_attribute('fpre')
#     lpre     = network.get_edges_attribute('lpre')
#     linit    = network.get_edges_attribute('linit')
#     E        = network.get_edges_attribute('E')
#     radius   = network.get_edges_attribute('radius')

#     x, q, f, l, r = dr_numpy(vertices, edges, fixed, loads, qpre, fpre, lpre, linit, E, radius)

#     for key, attr in network.vertices(True):
#         attr['x']  = x[key, 0]
#         attr['y']  = x[key, 1]
#         attr['z']  = x[key, 2]
#         attr['rx'] = r[key, 0]
#         attr['ry'] = r[key, 1]
#         attr['rz'] = r[key, 2]

#     for index, (u, v, attr) in enumerate(network.edges(True)):
#         attr['q'] = f[index, 0]
#         attr['f'] = f[index, 0]
#         attr['l'] = l[index, 0]

#     return network.to_data()


def dr_numpy(vertices, edges, fixed, loads, qpre, fpre, lpre, linit, E, radius,
             callback=None, callback_args=None, **kwargs):
    """Implementation of the dynamic relaxation method for form findong and analysis
    of articulated networks of axial-force members.

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
    callback : callable, optional
        User-defined function that is called at every iteration.
    callback_args : tuple, optional
        Additional arguments passed to the callback.

    Notes
    -----
    For more info, see [1]_.

    References
    ----------
    .. [1] De Laet L., Veenendaal D., Van Mele T., Mollaert M. and Block P.,
           *Bending incorporated: designing tension structures by integrating bending-active elements*,
           Proceedings of Tensinet Symposium 2013,Istanbul, Turkey, 2013.

    Examples
    --------
    .. plot::
        :include-source:

        import compas
        from compas.datastructures import Network
        from compas.plotters import NetworkPlotter
        from compas.numerical import dr_numpy

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

        network = Network.from_obj(compas.get('lines.obj'))
        network.update_default_vertex_attributes(dva)
        network.update_default_edge_attributes(dea)

        for key, attr in network.vertices(True):
            attr['is_fixed'] = network.vertex_degree(key) == 1

        for index, (u, v, attr) in enumerate(network.edges(True)):
            attr['qpre'] = index + 1

        k_i = network.key_index()

        vertices = network.get_vertices_attributes(('x', 'y', 'z'))
        edges    = [(k_i[u], k_i[v]) for u, v in network.edges()]
        fixed    = [k_i[key] for key in network.vertices_where({'is_fixed': True})]
        loads    = network.get_vertices_attributes(('px', 'py', 'pz'))
        qpre     = network.get_edges_attribute('qpre')
        fpre     = network.get_edges_attribute('fpre')
        lpre     = network.get_edges_attribute('lpre')
        linit    = network.get_edges_attribute('linit')
        E        = network.get_edges_attribute('E')
        radius   = network.get_edges_attribute('radius')

        lines = []
        for u, v in network.edges():
            lines.append({
                'start': network.vertex_coordinates(u, 'xy'),
                'end'  : network.vertex_coordinates(v, 'xy'),
                'color': '#cccccc',
                'width': 1.0
            })

        plotter = NetworkPlotter(network)
        plotter.draw_lines(lines)

        xyz, q, f, l, r = dr_numpy(vertices, edges, fixed, loads, qpre, fpre, lpre, linit, E, radius)

        for key, attr in network.vertices(True):
            index = k_i[key]
            attr['x'] = xyz[index, 0]
            attr['y'] = xyz[index, 1]
            attr['z'] = xyz[index, 2]

        plotter.draw_vertices(
            facecolor={key: '#ff0000' for key in network.vertices_where({'is_fixed': True})})
        plotter.draw_edges()
        plotter.show()

    """
    # --------------------------------------------------------------------------
    # callback
    # --------------------------------------------------------------------------
    if callback:
        assert callable(callback), 'The provided callback is not callable.'
    # --------------------------------------------------------------------------
    # configuration
    # --------------------------------------------------------------------------
    kmax  = kwargs.get('kmax', 10000)
    dt    = kwargs.get('dt', 1.0)
    tol1  = kwargs.get('tol1', 1e-3)
    tol2  = kwargs.get('tol2', 1e-6)
    coeff = Coeff(kwargs.get('c', 0.1))
    ca    = coeff.a
    cb    = coeff.b
    # --------------------------------------------------------------------------
    # attribute lists
    # --------------------------------------------------------------------------
    num_v = len(vertices)
    num_e = len(edges)
    free  = list(set(range(num_v)) - set(fixed))
    # --------------------------------------------------------------------------
    # attribute arrays
    # --------------------------------------------------------------------------
    x      = array(vertices, dtype=float).reshape((-1, 3))                      # m
    p      = array(loads, dtype=float).reshape((-1, 3))                         # kN
    qpre   = array(qpre, dtype=float).reshape((-1, 1))
    fpre   = array(fpre, dtype=float).reshape((-1, 1))                          # kN
    lpre   = array(lpre, dtype=float).reshape((-1, 1))                          # m
    linit  = array(linit, dtype=float).reshape((-1, 1))                         # m
    E      = array(E, dtype=float).reshape((-1, 1))                             # kN/mm2 => GPa
    radius = array(radius, dtype=float).reshape((-1, 1))                        # mm
    # --------------------------------------------------------------------------
    # sectional properties
    # --------------------------------------------------------------------------
    A  = 3.14159 * radius ** 2                                                  # mm2
    EA = E * A                                                                  # kN
    # --------------------------------------------------------------------------
    # create the connectivity matrices
    # after spline edges have been aligned
    # --------------------------------------------------------------------------
    C   = connectivity_matrix(edges, 'csr')
    Ct  = C.transpose()
    Ci  = C[:, free]
    Cit = Ci.transpose()
    Ct2 = Ct.copy()
    Ct2.data **= 2
    # --------------------------------------------------------------------------
    # if none of the initial lengths are set,
    # set the initial lengths to the current lengths
    # --------------------------------------------------------------------------
    if all(linit == 0):
        linit = normrow(C.dot(x))
    # --------------------------------------------------------------------------
    # initial values
    # --------------------------------------------------------------------------
    q = ones((num_e, 1), dtype=float)
    l = normrow(C.dot(x))
    f = q * l
    v = zeros((num_v, 3), dtype=float)
    r = zeros((num_v, 3), dtype=float)
    # --------------------------------------------------------------------------
    # helpers
    # --------------------------------------------------------------------------

    def rk(x0, v0, steps=2):
        def a(t, v):
            dx      = v * t
            x[free] = x0[free] + dx[free]
            # update residual forces
            r[free] = p[free] - D.dot(x)
            return cb * r / mass

        if steps == 1:
            return a(dt, v0)

        if steps == 2:
            B = [0.0, 1.0]
            K0 = dt * a(K[0][0] * dt, v0)
            K1 = dt * a(K[1][0] * dt, v0 + K[1][1] * K0)
            dv = B[0] * K0 + B[1] * K1
            return dv

        if steps == 4:
            B = [1. / 6., 1. / 3., 1. / 3., 1. / 6.]
            K0 = dt * a(K[0][0] * dt, v0)
            K1 = dt * a(K[1][0] * dt, v0 + K[1][1] * K0)
            K2 = dt * a(K[2][0] * dt, v0 + K[2][1] * K0 + K[2][2] * K1)
            K3 = dt * a(K[3][0] * dt, v0 + K[3][1] * K0 + K[3][2] * K1 + K[3][3] * K2)
            dv = B[0] * K0 + B[1] * K1 + B[2] * K2 + B[3] * K3
            return dv

        raise NotImplementedError

    # --------------------------------------------------------------------------
    # start iterating
    # --------------------------------------------------------------------------
    for k in range(kmax):
        print(k)

        q_fpre = fpre / l
        q_lpre = f / lpre
        q_EA   = EA * (l - linit) / (linit * l)
        q_lpre[isinf(q_lpre)] = 0
        q_lpre[isnan(q_lpre)] = 0
        q_EA[isinf(q_EA)]     = 0
        q_EA[isnan(q_EA)]     = 0

        q    = qpre + q_fpre + q_lpre + q_EA
        Q    = diags([q[:, 0]], [0])
        D    = Cit.dot(Q).dot(C)
        mass = 0.5 * dt ** 2 * Ct2.dot(qpre + q_fpre + q_lpre + EA / linit)
        # RK
        x0      = x.copy()
        v0      = ca * v.copy()
        dv      = rk(x0, v0, steps=4)
        v[free] = v0[free] + dv[free]
        dx      = v * dt
        x[free] = x0[free] + dx[free]
        # update
        u = C.dot(x)
        l = normrow(u)
        f = q * l
        r = p - Ct.dot(Q).dot(u)
        # crits
        crit1 = norm(r[free])
        crit2 = norm(dx[free])
        # callback
        if callback:
            callback(k, x, [crit1, crit2], callback_args)
        # convergence
        if crit1 < tol1:
            break
        if crit2 < tol2:
            break
    return x, q, f, l, r


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import random

    import compas
    from compas.datastructures import Mesh
    from compas.plotters import MeshPlotter
    from compas.utilities import i_to_rgb

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

    mesh = Mesh.from_obj(compas.get('faces.obj'))

    mesh.update_default_vertex_attributes(dva)
    mesh.update_default_edge_attributes(dea)

    for key, attr in mesh.vertices(True):
        attr['is_fixed'] = mesh.vertex_degree(key) == 2

    for u, v, attr in mesh.edges(True):
        attr['qpre'] = 1.0 * random.randint(1, 7)

    k_i = mesh.key_index()

    vertices = mesh.get_vertices_attributes(('x', 'y', 'z'))
    edges    = [(k_i[u], k_i[v]) for u, v in mesh.edges()]
    fixed    = [k_i[key] for key in mesh.vertices_where({'is_fixed': True})]
    loads    = mesh.get_vertices_attributes(('px', 'py', 'pz'))
    qpre     = mesh.get_edges_attribute('qpre')
    fpre     = mesh.get_edges_attribute('fpre')
    lpre     = mesh.get_edges_attribute('lpre')
    linit    = mesh.get_edges_attribute('linit')
    E        = mesh.get_edges_attribute('E')
    radius   = mesh.get_edges_attribute('radius')

    lines = []
    for u, v in mesh.edges():
        lines.append({
            'start': mesh.vertex_coordinates(u, 'xy'),
            'end'  : mesh.vertex_coordinates(v, 'xy'),
            'color': '#cccccc',
            'width': 0.5
        })

    plotter = MeshPlotter(mesh, figsize=(10, 7), fontsize=6)

    plotter.draw_lines(lines)
    plotter.draw_vertices(facecolor={key: '#000000' for key in mesh.vertices_where({'is_fixed': True})})
    plotter.draw_edges()

    plotter.update(pause=1.0)

    def callback(k, xyz, crits, args):
        print(k)

        plotter.update_vertices()
        plotter.update_edges()
        plotter.update(pause=0.001)

        for key, attr in mesh.vertices(True):
            index = k_i[key]
            attr['x'] = xyz[index, 0]
            attr['y'] = xyz[index, 1]
            attr['z'] = xyz[index, 2]

    xyz, q, f, l, r = dr_numpy(vertices, edges, fixed, loads,
                               qpre, fpre, lpre,
                               linit, E, radius,
                               kmax=100, callback=callback)

    for index, (u, v, attr) in enumerate(mesh.edges(True)):
        attr['f'] = f[index, 0]
        attr['l'] = l[index, 0]

    fmax = max(mesh.get_edges_attribute('f'))

    plotter.clear_vertices()
    plotter.clear_edges()

    plotter.draw_vertices(
        facecolor={key: '#000000' for key in mesh.vertices_where({'is_fixed': True})}
    )

    plotter.draw_edges(
        text={(u, v): '{:.0f}'.format(attr['f']) for u, v, attr in mesh.edges(True)},
        color={(u, v): i_to_rgb(attr['f'] / fmax) for u, v, attr in mesh.edges(True)},
        width={(u, v): 10 * attr['f'] / fmax for u, v, attr in mesh.edges(True)}
    )

    plotter.update(pause=1.0)
    plotter.show()
