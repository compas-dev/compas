
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

try:
    from numpy import arccos
    from numpy import array
    from numpy import cross
    from numpy import float64
    from numpy import int32
    from numpy import isnan
    from numpy import mean
    from numpy import newaxis
    from numpy import sin
    from numpy import sum
    from numpy import tile
    from numpy import zeros

    from scipy.sparse import find

except ImportError:
    import sys
    if 'ironpython' not in sys.version.lower():
        raise

from compas.numerical import connectivity_matrix
from compas.numerical import mass_matrix
from compas.numerical import normrow
from compas.numerical import uvw_lengths

from time import time


__all__ = ['drx_numpy']


def drx_numpy(structure, factor=1.0, tol=0.1, steps=10000, refresh=100, update=False, callback=None, **kwargs):
    """Run dynamic relaxation analysis.

    Parameters
    ----------
    structure : compas.datastructures.Datastructure
        The structure to analyse.
    factor : float
        Convergence factor.
    tol : float
        Tolerance value.
    steps : int
        Maximum number of steps.
    refresh : int
        Update progress every nth step.
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

    """

    # Setup

    tic1 = time()

    X, B, P, S, V, E, A, C, Ct, f0, l0, ind_c, ind_t, u, v, M, k0, m, n, rows, cols, vals, nv = _create_arrays(structure)
    inds, indi, indf, EIx, EIy, beams = _beam_data(structure)
    EIx = EIx.reshape(-1, 1)
    EIy = EIy.reshape(-1, 1)

    toc1 = time() - tic1

    # Solver

    tic2 = time()

    X, f, l = drx_solver_numpy(tol, steps, factor, C, Ct, X, M, k0, l0, f0, ind_c, ind_t, P, S, B, V, refresh,
                               beams, inds, indi, indf, EIx, EIy, callback, **kwargs)

    toc2 = time() - tic2

    # Summary

    if refresh:
        print('\n\nNumPy-SciPy DR -------------------')
        print('Setup time: {0:.3f} s'.format(toc1))
        print('Solver time: {0:.3f} s'.format(toc2))
        print('----------------------------------')

    # Update

    if update:

        k_i = structure.key_index()
        for key in structure.vertices():
            x, y, z = X[k_i[key], :]
            structure.set_vertex_attributes(key, 'xyz', [x, y, z])

        uv_i = structure.uv_index()
        for uv in structure.edges():
            i = uv_i[uv]
            structure.set_edge_attribute(uv, 'f', float(f[i]))

    return X, f, l


def drx_solver_numpy(tol, steps, factor, C, Ct, X, M, k0, l0, f0, ind_c, ind_t, P, S, B, V, refresh,
                     beams, inds, indi, indf, EIx, EIy, callback, **kwargs):

    """ NumPy and SciPy dynamic relaxation solver.

    Parameters
    ----------
    tol : float
        Tolerance value.
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
    M : array
        Mass matrix.
    k0 : array
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
    V : array
        Nodal velocities Vx, Vy, Vz.
    refresh : int
        Update progress every n steps.
    beams : int
        Beam data flag 1 or 0.
    inds : array
        Indices of beam element start nodes.
    indi : array
        Indices of beam element intermediate nodes.
    indf : array
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
        Vertex co-ordinates.
    array
        Edge forces.
    array
        Edge lengths.

    """

    res = 1000 * tol
    ts, Uo = 0, 0
    M = factor * tile(M.reshape((-1, 1)), (1, 3))

    while (ts <= steps) and (res > tol):

        uvw, l = uvw_lengths(C, X)
        f = f0 + k0 * (l.ravel() - l0)

        if ind_t:
            f[ind_t] *= f[ind_t] > 0
        if ind_c:
            f[ind_c] *= f[ind_c] < 0

        if beams:
            S = _beam_shear(S, X, inds, indi, indf, EIx, EIy)

        q = f[:, newaxis] / l
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


def _beam_data(structure):

    if getattr(structure, 'beams', None):
        inds, indi, indf, EIx, EIy = [], [], [], [], []
        for beam in structure.beams.values():
            nodes = beam['nodes']
            inds.extend(nodes[:-2])
            indi.extend(nodes[1:-1])
            indf.extend(nodes[2:])
            EIx.extend([structure.vertex[i]['EIx'] for i in nodes[1:-1]])
            EIy.extend([structure.vertex[i]['EIy'] for i in nodes[1:-1]])
        inds = array(inds, dtype=int32)
        indi = array(indi, dtype=int32)
        indf = array(indf, dtype=int32)
        EIx  = array(EIx, dtype=float64)
        EIy  = array(EIy, dtype=float64)
        beams = 1

    else:
        inds = indi = indf = array([0], dtype=int32)
        EIx = EIy = array([0.], dtype=float64)
        beams = 0

    return inds, indi, indf, EIx, EIy, beams


def _beam_shear(S, X, inds, indi, indf, EIx, EIy):

    S *= 0

    Xs = X[inds, :]
    Xi = X[indi, :]
    Xf = X[indf, :]
    Qa = Xi - Xs
    Qb = Xf - Xi
    Qc = Xf - Xs
    Qn = cross(Qa, Qb)
    mu = 0.5 * (Xf - Xs)

    La  = normrow(Qa)
    Lb  = normrow(Qb)
    Lc  = normrow(Qc)
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


def _create_arrays(structure):

    # Vertices

    n = structure.number_of_vertices()
    B = zeros((n, 3), dtype=float64)
    P = zeros((n, 3), dtype=float64)
    X = zeros((n, 3), dtype=float64)
    S = zeros((n, 3), dtype=float64)
    V = zeros((n, 3), dtype=float64)

    k_i = structure.key_index()
    for key, vertex in structure.vertex.items():
        i = k_i[key]
        B[i, :] = vertex.get('B', [1, 1, 1])
        P[i, :] = vertex.get('P', [0, 0, 0])
        X[i, :] = [vertex[j] for j in 'xyz']

    # Edges

    m  = structure.number_of_edges()
    u  = zeros(m, dtype=int32)
    v  = zeros(m, dtype=int32)
    E  = zeros(m, dtype=float64)
    A  = zeros(m, dtype=float64)
    s0 = zeros(m, dtype=float64)
    l0 = zeros(m, dtype=float64)
    ind_c = []
    ind_t = []

    uv_i = structure.uv_index()
    for ui, vi in structure.edges():
        i = uv_i[(ui, vi)]
        edge  = structure.edge[ui][vi]
        E[i]  = edge.get('E', 0)
        A[i]  = edge.get('A', 0)
        l0[i] = edge.get('l0', structure.edge_length(ui, vi))
        s0[i] = edge.get('s0', 0)
        u[i]  = k_i[ui]
        v[i]  = k_i[vi]
        ct = edge.get('ct', None)
        if ct == 'c':
            ind_c.append(i)
        elif ct == 't':
            ind_t.append(i)
    f0 = s0 * A
    k0 = E * A / l0
    q0 = f0 / l0

    # Faces (testing)

    # if structure.face:
    #     for face in faces:
    #         fdata = structure.facedata[face]
    #         Eh = fdata.get('E', 0)
    #         th = fdata.get('t', 0)
    #         Ah = structure.face_area(face)
    #         for ui, vi in structure.face_edges(face):
    #             i = uv_i[(ui, vi)]
    #             ks[i] += 1.5 * Eh * Ah * th / l0[i]**2

    # Arrays

    C  = connectivity_matrix([[k_i[i], k_i[j]] for i, j in structure.edges()], 'csr')
    Ct = C.transpose()
    M  = mass_matrix(Ct=Ct, ks=k0, q=q0, c=1, tiled=False)
    rows, cols, vals = find(Ct)
    rows = array(rows, dtype=int32)
    cols = array(cols, dtype=int32)
    vals = array(vals, dtype=float64)
    nv = vals.shape[0]

    return X, B, P, S, V, E, A, C, Ct, f0, l0, ind_c, ind_t, u, v, M, k0, m, n, rows, cols, vals, nv


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    # ==========================================================================
    # Example 1 (Dense)
    # ==========================================================================

    from compas.datastructures import Network
    from compas.viewers import VtkViewer


    m = 70
    p = [(i / m - 0.5) * 5 for i in range(m + 1)]
    vertices = [[xi, yi, 0] for yi in p for xi in p]
    edges = []

    for i in range(m):
        for j in range(m):
            s = (m + 1)
            p1 = (j + 0) * s + i + 0
            p2 = (j + 0) * s + i + 1
            p3 = (j + 1) * s + i + 0
            p4 = (j + 1) * s + i + 1
            edges.append([p1, p2])
            edges.append([p1, p3])
            if j == m - 1:
                edges.append([p4, p3])
            if i == m - 1:
                edges.append([p2, p4])

    structure = Network.from_vertices_and_edges(vertices=vertices, edges=edges)
    sides = [i for i in structure.vertices() if structure.vertex_degree(i) <= 2]
    structure.update_default_vertex_attributes({'P': [0, 0, 1000 / structure.number_of_vertices()]})
    structure.update_default_edge_attributes({'E': 100, 'A': 1, 'ct': 't'})
    structure.set_vertices_attributes(keys=sides, names='B', values=[[0, 0, 0]])

    data = {
        'vertices': {i: structure.vertex_coordinates(i) for i in structure.vertices()},
        'edges':    [{'u': u, 'v': v} for u, v in structure.edges()]
    }


    def callback(X, self):
        self.update_vertices_coordinates({i: X[i, :] for i in range(X.shape[0])})

    def func(self):
        drx_numpy(structure=structure, tol=0.05, update=True, refresh=5, callback=callback, self=self)


    print('Press key S to start')

    viewer = VtkViewer(data=data)
    viewer.vertex_size = 1
    viewer.edge_width  = 10
    viewer.keycallbacks['s'] = func
    viewer.setup()
    viewer.start()


    # ==========================================================================
    # Example 2 (grid)
    # ==========================================================================

    # import compas

    # from compas.datastructures import Network
    # from compas.plotters import NetworkPlotter


    # structure = Network.from_obj(compas.get('lines.obj'))
    # structure.update_default_vertex_attributes({'is_fixed': False, 'P': [1, 1, 0]})
    # structure.update_default_edge_attributes({'E': 10, 'A': 1, 'ct': 't'})
    # structure.set_vertices_attributes(['is_fixed', 'B'], [True, [0, 0, 0]], structure.leaves())

    # lines = []
    # for u, v in structure.edges():
    #     lines.append({
    #         'start': structure.vertex_coordinates(u, 'xy'),
    #         'end'  : structure.vertex_coordinates(v, 'xy'),
    #         'color': '#cccccc'
    #     })

    # plotter = NetworkPlotter(structure, figsize=(10, 7))
    # plotter.draw_vertices(facecolor={key: '#ff0000' for key in structure.vertices_where({'is_fixed': True})})
    # plotter.draw_lines(lines)
    # plotter.draw_edges()


    # def callback(X, k_i):
    #
    #     for key in structure.vertices():
    #         x, y, z = X[k_i[key], :]
    #         structure.set_vertex_attributes(key, 'xyz', [x, y, z])
    #     plotter.update_edges()
    #     plotter.update(pause=0.01)


    # drx_numpy(structure=structure, tol=0.001, refresh=1, update=True, callback=callback, k_i=structure.key_index())

    # plotter.show()


    # ==========================================================================
    # Example 3 (beam)
    # ==========================================================================

    # from numpy import linspace
    # from numpy import sign

    # from compas.datastructures import Network
    # from compas.plotters import NetworkPlotter


    # L  = 2.5
    # n  = 100
    # EI = 0.2

    # vertices = [[i, 1 - abs(i), 0] for i in list(linspace(-1, 1, n))]
    # for i in range(n):
    #     if vertices[i][1] < 0.5:
    #         vertices[i][0] = sign(vertices[i][0]) * vertices[i][1]
    # edges = [[i, i + 1] for i in range(n - 1)]

    # structure = Network.from_vertices_and_edges(vertices=vertices, edges=edges)
    # structure.update_default_vertex_attributes({'is_fixed': False, 'EIx': EI, 'EIy': EI})
    # structure.update_default_edge_attributes({'E': 50, 'A': 1, 'l0': L / n})
    # structure.set_vertices_attributes(['B', 'is_fixed'], [[0, 0, 0], True], structure.leaves())
    # structure.beams = {'beam': {'nodes': list(range(n))}}

    # lines = []
    # for u, v in structure.edges():
    #     lines.append({
    #         'start': structure.vertex_coordinates(u, 'xy'),
    #         'end'  : structure.vertex_coordinates(v, 'xy'),
    #         'color': '#cccccc'
    #     })

    # plotter = NetworkPlotter(structure, figsize=(10, 7))
    # plotter.draw_vertices(radius=0.005, facecolor={i: '#ff0000' for i in structure.vertices_where({'is_fixed': True})})
    # plotter.draw_lines(lines)
    # plotter.draw_edges()


    # def callback(X, k_i):
    #
    #     for key in structure.vertices():
    #         x, y, z = X[k_i[key], :]
    #         structure.set_vertex_attributes(key, 'xyz', [x, y, z])
    #     plotter.update_edges()
    #     plotter.update(pause=0.01)


    # drx_numpy(structure=structure, tol=0.01, refresh=20, factor=30, update=1, callback=callback, k_i=structure.key_index())

    # plotter.show()
