
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas

try:
    from numpy import arccos
    from numpy import array
    from numpy import isnan
    from numpy import mean
    from numpy import sin
    from numpy import sqrt
    from numpy import sum
    from numpy import zeros

    from numba import guvectorize
    from numba import f8
    from numba import i4
    from numba import i8

except ImportError:
    compas.raise_if_not_ironpython()


from compas.numerical import uvw_lengths

from compas.numerical.drx.drx_numpy import _beam_data
from compas.numerical.drx.drx_numpy import _create_arrays

from compas_hpc.geometry import cross_vectors_numba as cross
from compas_hpc.geometry import dot_vectors_numba as dot
from compas_hpc.geometry import length_vector_numba as length

from time import time


__all__ = [
    'drx_numba',
]


def _args(network, factor, summary, steps, tol):

    X, B, P, S, V, E, A, C, Ct, f0, l0, ind_c, ind_t, u, v, M, k0, m, n, rows, cols, vals, nv = _create_arrays(network)
    inds, indi, indf, EIx, EIy, beams = _beam_data(network)

    if not ind_c:
        ind_c = [-1]

    if not ind_t:
        ind_t = [-1]

    ind_c = array(ind_c)
    ind_t = array(ind_t)

    return tol, steps, summary, m, n, u, v, X, f0, l0, k0, ind_c, ind_t, B, P, S, rows, cols, vals, nv, M, factor, V, inds, indi, indf, EIx, EIy, beams, C


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
        Print summary at end (1:yes or 0:no).
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

    args = _args(network, factor, summary, steps, tol)

    toc1 = time() - tic1

    # Solver

    tic2 = time()

    tol, steps, summary, m, n, u, v, X, f0, l0, k0, ind_c, ind_t, B, P, S, rows, cols, vals, nv, M, factor, V, inds, indi, indf, EIx, EIy, beams, C = args

    drx_solver_numba(tol, steps, summary, m, n, u, v, X, f0, l0, k0, ind_c, ind_t, B, P, S, rows, cols, vals, nv,
                     M, factor, V, inds, indi, indf, EIx, EIy, beams)

    _, l = uvw_lengths(C, X)
    f    = f0 + k0 * (l.ravel() - l0)

    toc2 = time() - tic2

    # Summary

    if summary:
        print('\n\nNumba DR -------------------')
        print('Setup time: {0:.3f} s'.format(toc1))
        print('Solver time: {0:.3f} s'.format(toc2))
        print('----------------------------------')

    # Update

    if update:

        k_i  = network.key_index()
        uv_i = network.uv_index()

        for key in network.vertices():
            x, y, z = X[k_i[key], :]
            network.set_vertex_attributes(key, 'xyz', [x, y, z])

        for uv in network.edges():
            i = uv_i[uv]
            network.set_edge_attribute(uv, 'f', float(f[i]))

    return X, f, l


@guvectorize([(f8, i8, i8, i8, i8, i4[:], i4[:], f8[:, :], f8[:], f8[:], f8[:], i8[:], i8[:], f8[:, :], f8[:, :],
    f8[:, :], i4[:], i4[:], f8[:], i8, f8[:], f8, f8[:, :], i4[:], i4[:], i4[:], f8[:], f8[:], i8, f8)],
    '(),(),(),(),(),(m),(m),(n,p),(m),(m),(m),(a),(b),(n,p),(n,p),(n,p),(c),(c),(c),(),(n),(),(n,p),(k),(k),(k),(k),(k),()->()',
    nopython=True, cache=True, target='parallel')
def drx_solver_numba(tol, steps, summary, m, n, u, v, X, f0, l0, k0, ind_c, ind_t, B, P, S, rows, cols, vals, nv,
                     M, factor, V, inds, indi, indf, EIx, EIy, beams, out):

    """ Numba accelerated dynamic relaxation solver.

    Parameters
    ----------
    tol : float
        Tolerance value.
    steps : int
        Maximum number of steps.
    summary : int
        Print summary 1 or 0.
    m : int
        Number of edges.
    n : int
        Number of vertices.
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
    k0 : array
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
    nv : int
        Length of rows, cols and vals.
    M : array
        Mass matrix.
    factor : float
        Convergence factor.
    V : array
        Nodal velocities.
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
    beams : int
        Beam analysis on: 1 or off: 0.

    Returns
    -------
    None

    """

    f   = zeros(m)
    fx  = zeros(m)
    fy  = zeros(m)
    fz  = zeros(m)
    frx = zeros(n)
    fry = zeros(n)
    frz = zeros(n)
    Rn  = zeros(n)
    Una = zeros(n)

    res = 1000 * tol
    ts, Uo = 0, 0

    while (ts <= steps) and (res > tol):

        for i in range(m):

            xd    = X[v[i], 0] - X[u[i], 0]
            yd    = X[v[i], 1] - X[u[i], 1]
            zd    = X[v[i], 2] - X[u[i], 2]
            l     = sqrt(xd**2 + yd**2 + zd**2)
            f[i]  = f0[i] + k0[i] * (l - l0[i])
            q     = f[i] / l
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

        if beams:
            S *= 0

            for i in range(len(inds)):

                Xs = X[inds[i], :]
                Xi = X[indi[i], :]
                Xf = X[indf[i], :]
                Qa = Xi - Xs
                Qb = Xf - Xi
                Qc = Xf - Xs
                Qn = cross(Qa, Qb)

                mu  = 0.5 * (Xf - Xs)
                La  = length(Qa)
                Lb  = length(Qb)
                Lc  = length(Qc)
                LQn = length(Qn)
                Lmu = length(mu)

                a  = arccos((La**2 + Lb**2 - Lc**2) / (2 * La * Lb))
                k  = 2 * sin(a) / Lc
                ex = Qn / LQn
                ez = mu / Lmu
                ey = cross(ez, ex)

                K   = k * Qn / LQn
                Kx  = dot(K, ex) * ex
                Ky  = dot(K, ey) * ey
                Mc  = EIx[i] * Kx + EIy[i] * Ky
                cma = cross(Mc, Qa)
                cmb = cross(Mc, Qb)
                ua  = cma / length(cma)
                ub  = cmb / length(cmb)
                c1  = cross(Qa, ua)
                c2  = cross(Qb, ub)
                Lc1 = length(c1)
                Lc2 = length(c2)
                Ms  = Mc[0]**2 + Mc[1]**2 + Mc[2]**2

                Sa = ua * Ms * Lc1 / (La * dot(Mc, c1))
                Sb = ub * Ms * Lc2 / (Lb * dot(Mc, c2))

                if isnan(Sa).any() or isnan(Sb).any():
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

        for i in range(n):

            Rx    = (P[i, 0] - S[i, 0] - frx[i]) * B[i, 0]
            Ry    = (P[i, 1] - S[i, 1] - fry[i]) * B[i, 1]
            Rz    = (P[i, 2] - S[i, 2] - frz[i]) * B[i, 2]
            Rn[i] = sqrt(Rx**2 + Ry**2 + Rz**2)

            Mi = M[i] * factor
            V[i, 0] += Rx / Mi
            V[i, 1] += Ry / Mi
            V[i, 2] += Rz / Mi
            Una[i]  = Mi * (V[i, 0]**2 + V[i, 1]**2 + V[i, 2]**2)

        Un = sum(Una)

        if Un < Uo:
            V *= 0
        Uo = Un

        for i in range(n):

            X[i, 0] += V[i, 0]
            X[i, 1] += V[i, 1]
            X[i, 2] += V[i, 2]

        res = mean(Rn)
        ts += 1

    if summary:
        print('Step:', ts - 1, ' Residual:', res)

    out = 0.


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    # ==========================================================================
    # Example 1 (dense)
    # ==========================================================================

    from compas.datastructures import Network
    from compas.viewers import VtkViewer


    m = 150
    p = [(i / m - 0.5) * 5 for i in range(m + 1)]
    vertices = [[xi, yi, 0] for yi in p for xi in p]
    edges = []

    for i in range(m):
        for j in range(m):

            s  = (m + 1)
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

    network = Network.from_vertices_and_edges(vertices=vertices, edges=edges)
    sides = [i for i in network.vertices() if network.vertex_degree(i) <= 2]
    network.update_default_vertex_attributes({'P': [0, 0, 1000 / network.number_of_vertices()]})
    network.update_default_edge_attributes({'E': 100, 'A': 1, 'ct': 't'})
    network.set_vertices_attributes(keys=sides, names='B', values=[[0, 0, 0]])

    drx_numba(network=network, tol=0.01, summary=1, update=1)

    data = {
        'vertices': [network.vertex_coordinates(i) for i in network.vertices()],
        'edges':    [{'vertices': uv} for uv in network.edges()]
    }

    viewer = VtkViewer(data=data)
    viewer.vertex_size = 0
    viewer.setup()
    viewer.start()
