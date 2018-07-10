
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

try:
    from numpy import arccos
    from numpy import array
    from numpy import cross
    from numpy import int64
    from numpy import isnan
    from numpy import mean
    from numpy import newaxis
    from numpy import sin
    from numpy import sum
    from numpy import tile
    from numpy import zeros
except ImportError:
    import sys
    if 'ironpython' not in sys.version.lower():
        raise

from compas.numerical import connectivity_matrix
from compas.numerical import mass_matrix
from compas.numerical import normrow
from compas.numerical import uvw_lengths


from time import time


__author__    = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__ = 'Copyright 2018, Block Research Group - ETH Zurich'
__license__   = 'MIT License'
__email__     = 'liew@arch.ethz.ch'


__all__ = [
    'drx_numpy'
]


def drx_numpy(network, factor=1.0, tol=0.1, steps=10000, refresh=0, update=False, callback=None, **kwargs):

    """Run dynamic relaxation analysis.

    Parameters
    ----------
    network : obj
        Network to analyse.
    factor : float
        Convergence factor.
    tol : float
        Tolerance value.
    steps : int
        Maximum number of steps.
    refresh : int
        Update progress every n steps.
    update : bool
        Update the co-ordinates of the Network.
    callback : callable
        Callback function.

    Returns
    -------
    array
        Vertex co-ordinates.
    array
        Edge forces.
    array
        Edge lengths.

    Examples
    --------
    .. plot::
        :include-source:

        from compas.datastructures import Network
        from compas.numerical import drx_numpy
        from compas.plotters import NetworkPlotter

        from numpy import linspace
        from numpy import sign

        # Input

        L = 2.5
        n = 40
        EI = 0.2

        # Network

        vertices = [[i, 1 - abs(i), 0] for i in list(linspace(-1, 1, n))]
        for i in range(n):
            if vertices[i][1] < 0.5:
                vertices[i][0] = sign(vertices[i][0]) * vertices[i][1]
        vertices[0][0] += 0.2
        vertices[-1][0] -= 0.2
        edges = [[i, i + 1] for i in range(n - 1)]

        network = Network.from_vertices_and_edges(vertices=vertices, edges=edges)
        network.update_default_vertex_attributes({'is_fixed': False, 'P': [0, 0, 0], 'EIx': EI, 'EIy': EI})
        network.update_default_edge_attributes({'E': 50, 'A': 1, 'l0': L / n})
        network.set_vertices_attributes(network.leaves(), {'B': [0, 0, 0], 'is_fixed': True})
        network.beams = {'beam': {'nodes': list(range(n))}}

        # Solver

        drx_numpy(network=network, tol=0.01, refresh=10, factor=30, update=1)

        # Plotter

        plotter = NetworkPlotter(network, figsize=(10, 7))
        lines = []
        for u, v in network.edges():
            lines.append({
                'start': network.vertex_coordinates(u, 'xy'),
                'end'  : network.vertex_coordinates(v, 'xy'),
                'color': '#cccccc',
                'width': 1.0})
        plotter.draw_lines(lines)

        plotter.draw_vertices(radius=0.005, facecolor={i: '#ff0000' for i in network.vertices_where({'is_fixed': True})})
        plotter.draw_edges()
        plotter.show()

    See Also
    --------
    *

    """

    # Setup

    tic1 = time()

    X, B, P, Pn, S, V, E, A, C, Ct, f0, l0, ind_c, ind_t, u, v, M, ks = _create_arrays(network)
    try:
        inds, indi, indf, EIx, EIy = _beam_data(network)
        beams = 1
    except AttributeError:
        beams = inds = indi = indf = EIx = EIy = None

    toc1 = time() - tic1

    # Solver

    tic2 = time()

    X, f, l = drx_solver(tol, steps, factor, C, Ct, X, ks, l0, f0, ind_c, ind_t, P, S, B, M, V, refresh, beams,
                         inds, indi, indf, EIx, EIy, callback, **kwargs)

    toc2 = time() - tic2

    # Summary

    if refresh:
        print('\n\nNumPy-SciPy DR -------------------')
        print('Setup time: {0:.3f} s'.format(toc1))
        print('Solver time: {0:.3f} s'.format(toc2))
        print('----------------------------------')

    # Update

    if update:

        k_i = network.key_index()
        for key in network.vertices():
            x, y, z = X[k_i[key], :]
            network.set_vertex_attributes(key, {'x': x, 'y': y, 'z': z})

        uv_i = network.uv_index()
        for uv in network.edges():
            i = uv_i[uv]
            network.set_edge_attribute(uv, 'f', float(f[i]))

    return X, f, l


def drx_solver(tol, steps, factor, C, Ct, X, ks, l0, f0, ind_c, ind_t, P, S, B, M, V, refresh, beams, inds, indi,
               indf, EIx, EIy, callback, **kwargs):

    """ NumPy and SciPy dynamic relaxation solver.

    Parameters
    ----------
    tol : float
        Tolerance limit.
    steps : int
        Maximum number of steps.
    factor : float
        Convergence factor.
    C : array
        Connectivity matrix.
    Ct : array
        Transposed connectivity matrix.
    X : array
        Nodal co-ordinates.
    ks : array
        Initial edge axial stiffnesses.
    l0 : array
        Initial edge lengths.
    f0 : array
        Initial edge forces.
    ind_c : list
        Indices of compression only edges.
    ind_t : list
        Indices of tension only edges.
    P : array
        Nodal loads Px, Py, Pz.
    S : array
        Shear forces Sx, Sy, Sz.
    B : array
        Constraint conditions Bx, By, Bz.
    M : array
        Mass matrix.
    V : array
        Nodal velocities Vx, Vy, Vz.
    refresh : int
        Update progress every n steps.
    beams : bool
        Beam data flag.
    inds : list
        Indices of beam element start nodes.
    indi : list
        Indices of beam element intermediate nodes.
    indf : list
        Indices of beam element finish nodes beams.
    EIx : array
        Nodal EIx flexural stiffnesses.
    EIy : array
        Nodal EIy flexural stiffnesses.
    callback : obj
        Callback function.

    Returns
    -------
    array
        Updated nodal co-ordinates.
    array
        Updated forces.
    array
        Updated lengths.

    """

    res = 1000 * tol
    ts, Uo = 0, 0
    M = factor * tile(M, (1, 3))
    while (ts <= steps) and (res > tol):
        uvw, l = uvw_lengths(C, X)
        f = f0 + ks * (l - l0)
        if ind_t:
            f[ind_t] *= f[ind_t] > 0
        if ind_c:
            f[ind_c] *= f[ind_c] < 0
        if beams:
            S = _beam_shear(S, X, inds, indi, indf, EIx, EIy)
        q = f / l
        qt = tile(q, (1, 3))
        R = (P - S - Ct.dot(uvw * qt)) * B
        res = mean(normrow(R))
        V += R / M
        Un = sum(M * V**2)
        if Un < Uo:
            V *= 0
        Uo = Un
        X += V
        if refresh:
            if (ts % refresh == 0) or (res < tol):
                print('Step:{0} Residual:{1:.3f}'.format(ts, res))
                if callback:
                    callback(X, **kwargs)
        ts += 1

    return X, f, l


def _beam_data(network):

    """ Create data for beam element calculations.

    Parameters
    ----------
    network : obj
        Network to be analysed.

    Returns
    -------
    list
        Indices of beam element start nodes.
    list
        Indices of beam element intermediate nodes.
    list
        Indices of beam element finish nodes beams.
    array
        Nodal EIx flexural stiffnesses of all beams.
    array
        Nodal EIy flexural stiffnesses of all beams.

    """

    inds, indi, indf, EIx, EIy = [], [], [], [], []
    for beam in network.beams.values():
        nodes = beam['nodes']
        inds.extend(nodes[:-2])
        indi.extend(nodes[1:-1])
        indf.extend(nodes[2:])
        EIx.extend([network.vertex[i]['EIx'] for i in nodes[1:-1]])
        EIy.extend([network.vertex[i]['EIy'] for i in nodes[1:-1]])
    EIx = array(EIx)[:, newaxis]
    EIy = array(EIy)[:, newaxis]

    return inds, indi, indf, EIx, EIy


def _beam_shear(S, X, inds, indi, indf, EIx, EIy):

    """ Generate the beam nodal shear forces Sx, Sy and Sz.

    Parameters
    ----------
    S : array
        Nodal shear force array Sx, Sy, Sz.
    X : array
        Co-ordinates of nodes x, y, z.
    inds : list
        Indices of beam element start nodes.
    indi : list
        Indices of beam element intermediate nodes.
    indf : list
        Indices of beam element finish nodes beams.
    EIx : array
        Nodal EIx flexural stiffnesses.
    EIy : array
        Nodal EIy flexural stiffnesses.

    Returns
    -------
    array
        Updated beam nodal shears.

    """

    S *= 0
    Xs = X[inds, :]
    Xi = X[indi, :]
    Xf = X[indf, :]
    Qa = Xi - Xs
    Qb = Xf - Xi
    Qc = Xf - Xs
    Qn = cross(Qa, Qb)
    mu = 0.5 * (Xf - Xs)
    La = normrow(Qa)
    Lb = normrow(Qb)
    Lc = normrow(Qc)
    LQn = normrow(Qn)
    Lmu = normrow(mu)
    a = arccos((La**2 + Lb**2 - Lc**2) / (2 * La * Lb))
    k = 2 * sin(a) / Lc
    ex = Qn / tile(LQn, (1, 3))  # temporary simplification
    ez = mu / tile(Lmu, (1, 3))
    ey = cross(ez, ex)
    K = tile(k / LQn, (1, 3)) * Qn
    Kx = tile(sum(K * ex, 1)[:, newaxis], (1, 3)) * ex
    Ky = tile(sum(K * ey, 1)[:, newaxis], (1, 3)) * ey
    Mc = EIx * Kx + EIy * Ky
    cma = cross(Mc, Qa)
    cmb = cross(Mc, Qb)
    ua = cma / tile(normrow(cma), (1, 3))
    ub = cmb / tile(normrow(cmb), (1, 3))
    c1 = cross(Qa, ua)
    c2 = cross(Qb, ub)
    Lc1 = normrow(c1)
    Lc2 = normrow(c2)
    Ms = sum(Mc**2, 1)[:, newaxis]
    Sa = ua * tile(Ms * Lc1 / (La * sum(Mc * c1, 1)[:, newaxis]), (1, 3))
    Sb = ub * tile(Ms * Lc2 / (Lb * sum(Mc * c2, 1)[:, newaxis]), (1, 3))
    Sa[isnan(Sa)] = 0
    Sb[isnan(Sb)] = 0
    S[inds, :] += Sa
    S[indi, :] -= Sa + Sb
    S[indf, :] += Sb
    # Add node junction duplication for when elements cross each other
    # mu[0, :] = -1.25*x[0, :] + 1.5*x[1, :] - 0.25*x[2, :]
    # mu[-1, :] = 0.25*x[-3, :] - 1.5*x[-2, :] + 1.25*x[-1, :]
    return S


def _create_arrays(network):

    """ Create arrays for dynamic relaxation solvers.

    Parameters
    ----------
    network : obj
        Network to analyse.

    Returns
    -------
    array
        Nodal co-ordinates x, y, z.
    array
        Constraint conditions Bx, By, Bz.
    array
        Nodal loads Px, Py, Pz.
    array
        Resultant nodal loads.
    array
        Shear force components Sx, Sy, Sz.
    array
        Nodal velocities Vx, Vy, Vz.
    array
        Edge Young's moduli.
    array
        Edge areas.
    array
        Connectivity matrix.
    array
        Transposed connectivity matrix.
    array
        Edge initial forces.
    array
        Edge initial lengths.
    list
        Compression only edges indices.
    list
        Tension only edges indices.
    array
        Network edges' start points.
    array
        Network edges' end points.
    array
        Mass matrix.
    array
        Edge axial stiffnesses.

    """

    # Vertices

    n = network.number_of_vertices()
    B = zeros((n, 3))
    P = zeros((n, 3))
    X = zeros((n, 3))
    S = zeros((n, 3))
    V = zeros((n, 3))
    k_i = network.key_index()
    for key, vertex in network.vertex.items():
        i = k_i[key]
        B[i, :] = vertex.get('B', [1, 1, 1])
        P[i, :] = vertex.get('P', [0, 0, 0])
        X[i, :] = [vertex[j] for j in 'xyz']
    Pn = normrow(P)

    # Edges

    uv_i = network.uv_index()
    m  = network.number_of_edges()
    u  = zeros(m, dtype=int64)
    v  = zeros(m, dtype=int64)
    E  = zeros((m, 1))
    A  = zeros((m, 1))
    s0 = zeros((m, 1))
    l0 = zeros((m, 1))
    ind_c = []
    ind_t = []

    for ui, vi in network.edges():
        i = uv_i[(ui, vi)]
        edge  = network.edge[ui][vi]
        E[i]  = edge.get('E', 0)
        A[i]  = edge.get('A', 0)
        l0[i] = edge.get('l0', network.edge_length(ui, vi))
        s0[i] = edge.get('s0', 0)
        u[i]  = k_i[ui]
        v[i]  = k_i[vi]
        ct = edge.get('ct', None)
        if ct == 'c':
            ind_c.append(i)
        elif ct == 't':
            ind_t.append(i)
    f0 = s0 * A
    ks = E * A / l0
    q0 = f0 / l0

    # Faces (testing)

    # if network.face:
    #     for face in faces:
    #         fdata = network.facedata[face]
    #         Eh = fdata.get('E', 0)
    #         th = fdata.get('t', 0)
    #         Ah = network.face_area(face)
    #         for ui, vi in network.face_edges(face):
    #             i = uv_i[(ui, vi)]
    #             ks[i] += 1.5 * Eh * Ah * th / l0[i]**2

    # Arrays

    C  = connectivity_matrix([[k_i[ui], k_i[vi]] for ui, vi in network.edges()], 'csr')
    Ct = C.transpose()
    M  = mass_matrix(Ct=Ct, ks=ks, q=q0, c=1, tiled=False)

    return X, B, P, Pn, S, V, E, A, C, Ct, f0, l0, ind_c, ind_t, u, v, M, ks


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import compas

    from compas.datastructures import Network
    from compas.plotters import NetworkPlotter
    from compas.utilities import i_to_rgb

    from numpy import linspace
    from numpy import sign


    def callback(X, k_i):
        for key in network.vertices():
            x, y, z = X[k_i[key], :]
            network.set_vertex_attributes(key, {'x': x, 'y': y, 'z': z})
        plotter.update_edges()
        plotter.update(pause=0.01)


    # ==========================================================================
    # Example 1
    # ==========================================================================

    # Load Network

    network = Network.from_obj(compas.get('lines.obj'))
    network.update_default_vertex_attributes({'is_fixed': False, 'P': [1, 1, 0]})
    network.update_default_edge_attributes({'E': 10, 'A': 1, 'ct': 't'})
    network.set_vertices_attributes(network.leaves(), {'is_fixed': True, 'B': [0, 0, 0]})

    # Plotter

    plotter = NetworkPlotter(network, figsize=(10, 7))
    lines = []
    for u, v in network.edges():
        lines.append({
            'start': network.vertex_coordinates(u, 'xy'),
            'end'  : network.vertex_coordinates(v, 'xy'),
            'color': '#cccccc',
            'width': 1.0})
    plotter.draw_lines(lines)
    plotter.draw_vertices(facecolor={key: '#ff0000' for key in network.vertices_where({'is_fixed': True})})
    plotter.draw_edges()

    # Solver

    drx_numpy(network=network, tol=0.001, refresh=1, update=True, callback=callback, k_i=network.key_index())
    fmax = max(network.get_edges_attribute('f'))

    # Forces

    plotter.draw_edges(
        color={(u, v): i_to_rgb(attr['f'] / fmax) for u, v, attr in network.edges(True)},
        width={(u, v): 10 * attr['f'] / fmax for u, v, attr in network.edges(True)})
    plotter.update()
    plotter.show()


    # ==========================================================================
    # Example 2
    # ==========================================================================

    # # Input

    L = 2.5
    n = 40
    EI = 0.2

    # Network

    vertices = [[i, 1 - abs(i), 0] for i in list(linspace(-1, 1, n))]
    for i in range(n):
        if vertices[i][1] < 0.5:
            vertices[i][0] = sign(vertices[i][0]) * vertices[i][1]
    vertices[0][0] += 0.1
    vertices[-1][0] -= 0.1
    edges = [[i, i + 1] for i in range(n - 1)]

    network = Network.from_vertices_and_edges(vertices=vertices, edges=edges)
    network.update_default_vertex_attributes({'is_fixed': False, 'P': [0, 0, 0], 'EIx': EI, 'EIy': EI})
    network.update_default_edge_attributes({'E': 50, 'A': 1, 'l0': L / n})
    network.set_vertices_attributes(network.leaves(), {'B': [0, 0, 0], 'is_fixed': True})
    network.beams = {'beam': {'nodes': list(range(n))}}

    # Plotter

    plotter = NetworkPlotter(network, figsize=(10, 7))
    lines = []
    for u, v in network.edges():
        lines.append({
            'start': network.vertex_coordinates(u, 'xy'),
            'end'  : network.vertex_coordinates(v, 'xy'),
            'color': '#cccccc',
            'width': 1.0})
    plotter.draw_lines(lines)

    plotter.draw_vertices(radius=0.005, facecolor={i: '#ff0000' for i in network.vertices_where({'is_fixed': True})})
    plotter.draw_edges()

    # Solver

    drx_numpy(network=network, tol=0.01, refresh=10, factor=30, update=1, callback=callback, k_i=network.key_index())

    plotter.show()


    # ==========================================================================
    # Example 3
    # ==========================================================================

    from compas.datastructures import Mesh
    from compas.viewers import VtkViewer


    m = 100
    x = y = [(i / m - 0.5) * 7 for i in range(m + 1)]
    vertices = [[xi, yi, 0] for yi in y for xi in x]
    faces = [[(j + 0) * (m + 1) + i + 0, (j + 0) * (m + 1) + i + 1,
              (j + 1) * (m + 1) + i + 1, (j + 1) * (m + 1) + i + 0]
             for i in range(m) for j in range(m)]
    mesh = Mesh.from_vertices_and_faces(vertices=vertices, faces=faces)

    pz = 1000 / mesh.number_of_vertices()
    sides = [i for i in mesh.vertices() if mesh.vertex_degree(i) <= 3]
    mesh.update_default_vertex_attributes({'P': [0, 0, pz]})
    mesh.update_default_edge_attributes({'E': 7, 'A': 1, 'ct': 't'})
    mesh.set_vertices_attributes(sides, {'B': [0, 0, 0]})

    data = {}
    data['vertices'] = {i: mesh.vertex_coordinates(i) for i in mesh.vertices()}
    data['edges']    = [{'u': u, 'v': v} for u, v in mesh.edges()]
    data['faces']    = {i: {'vertices': j} for i, j in mesh.face.items()}


    def callback(X, self):
        for i in range(X.shape[0]):
            self.vertices.SetPoint(i, X[i, :])
            self.vertices.Modified()
        self.window.Render()


    def func(self):
        X, f, l = drx_numpy(network=mesh, tol=0.01, update=True, refresh=1, callback=callback, self=self)

    print('Press key S to start')

    viewer = VtkViewer(data=data)
    viewer.settings['draw_vertices'] = 0
    viewer.settings['draw_edges'] = 1
    viewer.settings['draw_faces'] = 1
    viewer.settings['vertex_size'] = 0.02
    viewer.settings['edge_width'] = 0.01
    viewer.keycallbacks['s'] = func
    viewer.start()
