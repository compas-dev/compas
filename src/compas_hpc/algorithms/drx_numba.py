
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from numpy import arccos
from numpy import array
from numpy import float64
from numpy import int64
from numpy import isnan
from numpy import mean
from numpy import sin
from numpy import sqrt
from numpy import zeros

from numba import guvectorize
from numba import f8
from numba import i8

from scipy.sparse import find

from compas.numerical import uvw_lengths
from compas.numerical.algorithms.drx_numpy import _beam_data
from compas.numerical.algorithms.drx_numpy import _create_arrays

from compas_hpc import cross_vectors_numba as cross
from compas_hpc import dot_vectors_numba as dot
from compas_hpc import length_vector_numba as length


from time import time


__author__    = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__ = 'Copyright 2018, BLOCK Research Group - ETH Zurich'
__license__   = 'MIT License'
__email__     = 'liew@arch.ethz.ch'


__all__ = [
    'drx_numba',
]


def _prepare_solver(network):

    X, B, P, Pn, S, V, E, A, C, Ct, f0, l0, ind_c, ind_t, u, v, M, ks = _create_arrays(network)
    try:
        inds, indi, indf, EIx, EIy = _beam_data(network)
        inds = array(inds)
        indi = array(indi)
        indf = array(indf)
        EIx  = EIx.ravel()
        EIy  = EIy.ravel()
        beams = 1
    except AttributeError:
        inds = indi = indf = array([0])
        EIx = EIy = array([0.])
        beams = 0

    # Arrays

    f0_ = f0.ravel()
    ks_ = ks.ravel()
    l0_ = l0.ravel()
    M_  = M.ravel()

    if not ind_c:
        ind_c = [-1]
    if not ind_t:
        ind_t = [-1]
    ind_c = array(ind_c)
    ind_t = array(ind_t)

    rows, cols, vals = find(Ct)
    rows_ = array(rows, dtype=int64)
    cols_ = array(cols, dtype=int64)
    vals_ = array(vals, dtype=float64)

    return u, v, X, f0_, l0_, ks_, ind_c, ind_t, B, P, S, rows_, cols_, vals_, M_, C, f0, ks, l0, beams, inds, indi, indf, EIx, EIy


def drx_numba(network, factor=1.0, tol=0.1, steps=10000, summary=0, update=False):

    """ Run Numba accelerated dynamic relaxation analysis.

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
    summary : int
        Print summary at end (1 or 0).
    update : bool
        Update the co-ordinates of the Network.

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

    u, v, X, f0_, l0_, ks_, ind_c, ind_t, B, P, S, rows_, cols_, vals_, M_, C, f0, ks, l0, beams, inds, indi, indf, EIx, EIy = _prepare_solver(network)

    toc1 = time() - tic1

    # Solver

    tic2 = time()

    drx_solver(tol, steps, summary, u, v, X, f0_, l0_, ks_, ind_c, ind_t, B, P, S, rows_, cols_, vals_, M_, factor,
               beams, inds, indi, indf, EIx, EIy)
    _, l = uvw_lengths(C, X)
    f = f0 + ks * (l - l0)

    toc2 = time() - tic2

    # Summary

    if summary:
        print('\n\nNumba DR -------------------')
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


@guvectorize([(f8, i8, i8, i8[:], i8[:], f8[:, :], f8[:], f8[:], f8[:], i8[:], i8[:], f8[:, :], f8[:, :], f8[:, :],
               i8[:], i8[:], f8[:], f8[:], f8, i8, i8[:], i8[:], i8[:], f8[:], f8[:], f8)],
             '(),(),(),(m),(m),(n,p),(m),(m),(m),(a),(b),(n,p),(n,p),(n,p),(c),(c),(c),(n),(),(),(k),(k),(k),(k),(k)->()',
             nopython=True, cache=True, target='parallel')
def drx_solver(tol, steps, summary, u, v, X, f0, l0, ks, ind_c, ind_t, B, P, S, rows, cols, vals, M, factor, beams,
               inds, indi, indf, EIx, EIy, out):

    """ Numba accelerated dynamic relaxation solver.

    Parameters
    ----------
    tol : float
        Tolerance limit.
    steps : int
        Maximum number of steps.
    summary : int
        Print summary 1 or 0.
    u : array
        Network edges' start points.
    v : array
        Network edges' end points.
    X : array
        Nodal co-ordinates.
    f0 : array
        Initial edge forces.
    l0 : array
        Initial edge lengths.
    ks : array
        Initial edge axial stiffnesses.
    ind_c : array
        Indices of compression only edges.
    ind_t : array
        Indices of tension only edges.
    B : array
        Constraint conditions Bx, By, Bz.
    P : array
        Nodal loads Px, Py, Pz.
    S : array
        Shear forces Sx, Sy, Sz.
    rows : array
        Edge adjacencies (rows).
    cols : array
        Edge adjacencies (columns).
    vals : array
        Edge adjacencies (values).
    M : array
        Mass matrix.
    factor : float
        Convergence factor.
    beams : int
        Beam analysis on: 1 or off: 0.
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

    Returns
    -------
    array
        Updated nodal co-ordinates.

    """
    m   = u.shape[0]
    n   = X.shape[0]
    nv  = vals.shape[0]
    f   = zeros(m)
    fx  = zeros(m)
    fy  = zeros(m)
    fz  = zeros(m)
    Vx  = zeros(n)
    Vy  = zeros(n)
    Vz  = zeros(n)
    frx = zeros(n)
    fry = zeros(n)
    frz = zeros(n)
    Rn  = zeros(n)

    res = 1000 * tol
    ts, Uo = 0, 0
    while (ts <= steps) and (res > tol):
        for i in range(m):
            xd = X[v[i], 0] - X[u[i], 0]
            yd = X[v[i], 1] - X[u[i], 1]
            zd = X[v[i], 2] - X[u[i], 2]
            l = sqrt(xd**2 + yd**2 + zd**2)
            f[i] = f0[i] + ks[i] * (l - l0[i])
            q = f[i] / l
            fx[i] = xd * q
            fy[i] = yd * q
            fz[i] = zd * q
        if ind_t[0] != -1:
            for i in ind_t:
                if f[i] < 0:
                    fx[i] = 0
                    fy[i] = 0
                    fz[i] = 0
        if ind_c[0] != -1:
            for i in ind_c:
                if f[i] > 0:
                    fx[i] = 0
                    fy[i] = 0
                    fz[i] = 0

        S *= 0
        if beams:
            for i in range(len(inds)):
                Xs = X[inds[i], :]
                Xi = X[indi[i], :]
                Xf = X[indf[i], :]
                Qa = Xi - Xs
                Qb = Xf - Xi
                Qc = Xf - Xs
                Qn = cross(Qa, Qb)
                mu = 0.5 * (Xf - Xs)
                La = length(Qa)
                Lb = length(Qb)
                Lc = length(Qc)
                LQn = length(Qn)
                Lmu = length(mu)
                a = arccos((La**2 + Lb**2 - Lc**2) / (2 * La * Lb))
                k = 2 * sin(a) / Lc
                ex = Qn / LQn
                ez = mu / Lmu
                ey = cross(ez, ex)
                K = k * Qn / LQn
                Kx = dot(K, ex) * ex
                Ky = dot(K, ey) * ey
                Mc = EIx[i] * Kx + EIy[i] * Ky
                cma = cross(Mc, Qa)
                cmb = cross(Mc, Qb)
                ua = cma / length(cma)
                ub = cmb / length(cmb)
                c1 = cross(Qa, ua)
                c2 = cross(Qb, ub)
                Lc1 = length(c1)
                Lc2 = length(c2)
                Ms = Mc[0]**2 + Mc[1]**2 + Mc[2]**2
                Sa = ua * Ms * Lc1 / (La * dot(Mc, c1))
                Sb = ub * Ms * Lc2 / (Lb * dot(Mc, c2))
                # print(isnan(Sa))
                if isnan(Sa[0]) or isnan(Sb[0]):
                    pass
                else:
                    S[inds[i], :] += Sa
                    S[indi[i], :] -= Sa + Sb
                    S[indf[i], :] += Sb

        frx *= 0
        fry *= 0
        frz *= 0
        for i in range(nv):
            frx[rows[i]] += vals[i] * fx[cols[i]]
            fry[rows[i]] += vals[i] * fy[cols[i]]
            frz[rows[i]] += vals[i] * fz[cols[i]]
        Un = 0.
        for i in range(n):
            Rx = (P[i, 0] - S[i, 0] - frx[i]) * B[i, 0]
            Ry = (P[i, 1] - S[i, 1] - fry[i]) * B[i, 1]
            Rz = (P[i, 2] - S[i, 2] - frz[i]) * B[i, 2]
            Rn[i] = sqrt(Rx**2 + Ry**2 + Rz**2)
            Mi = M[i] * factor
            Vx[i] += Rx / Mi
            Vy[i] += Ry / Mi
            Vz[i] += Rz / Mi
            Un += Mi * (Vx[i]**2 + Vy[i]**2 + Vz[i]**2)
        if Un < Uo:
            Vx *= 0
            Vy *= 0
            Vz *= 0
        Uo = Un
        for i in range(n):
            X[i, 0] += Vx[i]
            X[i, 1] += Vy[i]
            X[i, 2] += Vz[i]
        res = mean(Rn)
        ts += 1

    if summary:
        print('Step:', ts - 1, ' Residual:', res)

    out = 1.


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    # ==========================================================================
    # Example 1
    # ==========================================================================

    # def func(self):
    #     u, v, X0, f0_, l0_, ks_, ind_c, ind_t, B, P, S, rows_, cols_, vals_, M_, C, f0, ks, l0, beams, inds, indi, indf, EIx, EIy = self.args
    #     drx_solver(0.01, 1000, 0, u, v, X0, f0_, l0_, ks_, ind_c, ind_t, B, P, S, rows_, cols_, vals_, M_, 1, beams, inds, indi, indf, EIx, EIy)
    #     for i in range(X0.shape[0]):
    #         self.vertices.SetPoint(i, X0[i, :])
    #         self.vertices.Modified()
    #     self.window.Render()
    #     self.X0 = X0

    # from compas.datastructures import Mesh
    # from compas.viewers import VtkViewer

    # m = 20
    # x = y = [(i / m - 0.5) * 7 for i in range(m + 1)]
    # vertices = [[xi, yi, 0] for yi in y for xi in x]
    # faces = [[(j + 0) * (m + 1) + i + 0, (j + 0) * (m + 1) + i + 1,
    #           (j + 1) * (m + 1) + i + 1, (j + 1) * (m + 1) + i + 0]
    #          for i in range(m) for j in range(m)]
    # mesh = Mesh.from_vertices_and_faces(vertices=vertices, faces=faces)

    # pz = 30 / mesh.number_of_vertices()
    # sides = [i for i in mesh.vertices() if mesh.vertex_degree(i) == 2]
    # mesh.update_default_vertex_attributes({'P': [0, 0, pz]})
    # mesh.update_default_edge_attributes({'E': 5, 'A': 1, 'ct': 't'})
    # mesh.set_vertices_attributes(sides, {'B': [0, 0, 0]})

    # def z_up_3(self):
    #     self.X0[self.sides[3], 2] += 0.05
    #     func(self)

    # def z_down_3(self):
    #     self.X0[self.sides[3], 2] -= 0.05
    #     func(self)

    # def z_up_2(self):
    #     self.X0[self.sides[2], 2] += 0.05
    #     func(self)

    # def z_down_2(self):
    #     self.X0[self.sides[2], 2] -= 0.05
    #     func(self)


    # print('Press key S to start')

    # data = {}
    # data['vertices'] = {i: mesh.vertex_coordinates(i) for i in mesh.vertices()}
    # data['edges']    = [{'u': ui, 'v': vi} for ui, vi in mesh.edges()]
    # data['faces']    = {i: {'vertices': j} for i, j in mesh.face.items()}

    # viewer = VtkViewer(data=data)
    # viewer.args = _prepare_solver(mesh)
    # viewer.settings['draw_vertices'] = 0
    # viewer.settings['draw_edges'] = 1
    # viewer.settings['draw_faces'] = 1
    # viewer.settings['edge_width'] = 0.02
    # viewer.sides = sides
    # viewer.keycallbacks['s'] = func
    # viewer.keycallbacks['4'] = z_up_3
    # viewer.keycallbacks['5'] = z_down_3
    # viewer.keycallbacks['6'] = z_up_2
    # viewer.keycallbacks['7'] = z_down_2
    # viewer.start()


    # ==========================================================================
    # Example 2
    # ==========================================================================

    from compas.datastructures import Network
    from compas.viewers import VtkViewer

    from numpy import linspace
    from numpy import sign

    from vtk import vtkSphereWidget


    def func(self):
        u, v, X0, f0_, l0_, ks_, ind_c, ind_t, B, P, S, rows_, cols_, vals_, M_, C, f0, ks, l0, beams, inds, indi, indf, EIx, EIy = self.args
        drx_solver(0.01, 1000, 0, u, v, X0, f0_, l0_, ks_, ind_c, ind_t, B, P, S, rows_, cols_, vals_, M_, 10, beams, inds, indi, indf, EIx, EIy)
        for i in range(X0.shape[0]):
            self.vertices.SetPoint(i, X0[i, :])
            self.vertices.Modified()
        self.window.Render()
        self.X0 = X0

    # Input

    L = 12
    n = 40
    EI = 0.2

    # Network

    vertices = [[i, 1 - abs(i), 0] for i in list(linspace(-5, 5, n))]
    edges = [[i, i + 1] for i in range(n - 1)]

    network = Network.from_vertices_and_edges(vertices=vertices, edges=edges)
    leaves = network.leaves()
    network.update_default_vertex_attributes({'is_fixed': False, 'P': [0, 0, 0], 'EIx': EI, 'EIy': EI})
    network.update_default_edge_attributes({'E': 50, 'A': 1, 'l0': L / n})
    network.set_vertices_attributes(leaves, {'B': [0, 0, 0], 'is_fixed': True})
    network.beams = {'beam': {'nodes': list(range(n))}}

    data = {}
    data['vertices'] = {i: network.vertex_coordinates(i) for i in network.vertices()}
    data['edges']    = [{'u': ui, 'v': vi} for ui, vi in network.edges()]


    class RightHandle():

        def __init__(self, viewer):
            self.viewer = viewer

        def __call__(self, caller, ev):
            xyz = caller.GetCenter()
            self.viewer.X0[-1, :2] = xyz[:2]
            self.viewer.func(self.viewer)

    class LeftHandle():

        def __init__(self, viewer):
            self.viewer = viewer

        def __call__(self, caller, ev):
            xyz = caller.GetCenter()
            self.viewer.X0[0, :2] = xyz[:2]
            self.viewer.func(self.viewer)


    viewer = VtkViewer(data=data)
    viewer.args = _prepare_solver(network)
    viewer.settings['draw_axes'] = 1
    viewer.settings['vertex_size'] = 0.02
    viewer.settings['camera_pos'] = [0, 1, -5]
    viewer.keycallbacks['s'] = func
    viewer.func = func

    left_widget = vtkSphereWidget()
    left_widget.SetCenter(network.vertex_coordinates(leaves[0]))
    left_widget.SetRadius(0.1)
    left_widget.SetInteractor(viewer.interactor)
    left_widget.SetRepresentationToSurface()
    left_widget.On()
    left_widget.AddObserver("InteractionEvent", LeftHandle(viewer))

    right_widget = vtkSphereWidget()
    right_widget.SetCenter(network.vertex_coordinates(leaves[1]))
    right_widget.SetRadius(0.1)
    right_widget.SetInteractor(viewer.interactor)
    right_widget.SetRepresentationToSurface()
    right_widget.On()
    right_widget.AddObserver("InteractionEvent", RightHandle(viewer))

    viewer.start()
