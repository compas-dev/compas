from numpy import arccos
from numpy import mean
from numpy import sin
from numpy import sqrt
from numpy import zeros

from numba import jit

from compas.hpc.numba_.geometry import numba_cross
from compas.hpc.numba_.geometry import numba_vdot
from compas.hpc.numba_.geometry import numba_length


__author__     = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2017, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'liew@arch.ethz.ch'


# @jit(float64[:](float64[:], float64[:]), nogil=True, nopython=True)
# def cross_numba(a, b):
#     c = zeros(3)
#     c[0] = a[1] * b[2] - a[2] * b[1]
#     c[1] = a[2] * b[0] - a[0] * b[2]
#     c[2] = a[0] * b[1] - a[1] * b[0]
#     return c


# @jit(float64[:,:](float64, int64, int64[:], int64[:], float64[:,:], float64[:], float64[:], float64[:], int32[:],
#      int32[:], float64[:], float64[:,:], float64[:,:], float64[:], int64[:], int64[:], float64, int64[:], int64[:],
#      int64[:], float64[:], float64[:], int64, float64[:,:], int64), nogil=True, nopython=True)
# def dr_solver_numba(tol, steps, u, v, X, f0, ks, l0, rows, cols, vals, P, B, M, ind_c, ind_t, factor, inds, indi, indf,
#                     EIx, EIy, beams, S, refresh):
#     """ Numba accelerated dynamic relaxation solver.

#     Parameters:
#         tol (float64): Tolerance limit.
#         steps (int64): Maximum number of iteration steps.
#         u (int64[:]): Network edges' start points.
#         v (int64[:]): Network edges' end points.
#         X (float64[:,:]): Nodal co-ordinates.
#         f0 (float64[:]): Initial edge forces.
#         ks (float64[:]): Initial edge stiffnesses.
#         l0 (float64[:]): Initial edge lengths.
#         rows (int32[:]): Edge adjacencies (rows).
#         cols (int32[:]): Edge adjacencies (columns).
#         vals (float64[:]): Edge adjacencies (values).
#         P (float64[:,:]): Nodal loads Px, Py, Pz.
#         B (float64[:,:]): Constraint conditions.
#         M (float64[:]): Mass matrix.
#         ind_c (int64[:]): Compression only edges.
#         ind_t (int64[:]): Tension only edges.
#         factor (float64): Convergence factor.
#         inds (int64[:]): Indices of all beam element start nodes.
#         indi (int64[:]): Indices of all beam element intermediate nodes.
#         indf (int64[:]): Indices of all beam element finish nodes beams.
#         EIx (float64[:]): Nodal EIx flexural stiffnesses for all beams.
#         EIy (float64[:]): Nodal EIy flexural stiffnesses for all beams.
#         beams (int64): Beam analysis on: 1 or off: 0.
#         S (float64[:,:]): Empty shear force array.

#     Returns:
#         float64[:,:]: Updated nodal co-ordinates.
#     """
#     m = len(u)
#     n = X.shape[0]
#     f = zeros(m)
#     fx = zeros(m)
#     fy = zeros(m)
#     fz = zeros(m)
#     Vx = zeros(n)
#     Vy = zeros(n)
#     Vz = zeros(n)
#     Rx = zeros(n)
#     Ry = zeros(n)
#     Rz = zeros(n)
#     Rn = zeros(n)
#     res = 1000 * tol
#     ts = 0
#     Uo = 0.0
#     while (ts <= steps) and (res > tol):
#         S *= 0
#         if beams:
#             for i in range(len(inds)):
#                 Xs = X[inds[i], :]
#                 Xi = X[indi[i], :]
#                 Xf = X[indf[i], :]
#                 Qa = Xi - Xs
#                 Qb = Xf - Xi
#                 Qc = Xf - Xs
#                 Qn = cross_numba(Qa, Qb)
#                 Qnn = sqrt(Qn[0]**2 + Qn[1]**2 + Qn[2]**2)
#                 La = sqrt(Qa[0]**2 + Qa[1]**2 + Qa[2]**2)
#                 Lb = sqrt(Qb[0]**2 + Qb[1]**2 + Qb[2]**2)
#                 Lc = sqrt(Qc[0]**2 + Qc[1]**2 + Qc[2]**2)
#                 a = arccos((La**2 + Lb**2 - Lc**2) / (2 * La * Lb))
#                 k = 2 * sin(a) / Lc
#                 mu = -0.5 * Xs + 0.5 * Xf
#                 mun = sqrt(mu[0]**2 + mu[1]**2 + mu[2]**2)
#                 ex = Qn / Qnn
#                 ez = mu / mun
#                 ey = cross_numba(ez, ex)
#                 K = k * Qn / Qnn
#                 Kx = (K[0] * ex[0] + K[1] * ex[1] + K[2] * ex[2]) * ex
#                 Ky = (K[0] * ey[0] + K[1] * ey[1] + K[2] * ey[2]) * ey
#                 Mc = EIx[i] * Kx + EIy[i] * Ky
#                 cma = cross_numba(Mc, Qa)
#                 cmb = cross_numba(Mc, Qb)
#                 ua = cma / sqrt(cma[0]**2 + cma[1]**2 + cma[2]**2)
#                 ub = cmb / sqrt(cmb[0]**2 + cmb[1]**2 + cmb[2]**2)
#                 c1 = cross_numba(Qa, ua)
#                 c2 = cross_numba(Qb, ub)
#                 Lc1 = sqrt(c1[0]**2 + c1[1]**2 + c1[2]**2)
#                 Lc2 = sqrt(c2[0]**2 + c2[1]**2 + c2[2]**2)
#                 Ms = Mc[0]**2 + Mc[1]**2 + Mc[2]**2
#                 Sa = ua * Ms * Lc1 / (La * (Mc[0] * c1[0] + Mc[1] * c1[1] + Mc[2] * c1[2]))
#                 Sb = ub * Ms * Lc2 / (Lb * (Mc[0] * c2[0] + Mc[1] * c2[1] + Mc[2] * c2[2]))
#                 S[inds[i], :] += Sa
#                 S[indi[i], :] += - Sa - Sb
#                 S[indf[i], :] += Sb
#         for i in range(m):
#             ui = u[i]
#             vi = v[i]
#             xd = X[vi, 0] - X[ui, 0]
#             yd = X[vi, 1] - X[ui, 1]
#             zd = X[vi, 2] - X[ui, 2]
#             l = sqrt(xd**2 + yd**2 + zd**2)
#             f[i] = f0[i] + ks[i] * (l - l0[i])
#             q = f[i] / l
#             fx[i] = xd * q
#             fy[i] = yd * q
#             fz[i] = zd * q
#         if ind_t[0] != -1:
#             for i in ind_t:
#                 if f[i] < 0:
#                     fx[i] = 0
#                     fy[i] = 0
#                     fz[i] = 0
#         if ind_c[0] != -1:
#             for i in ind_c:
#                 if f[i] > 0:
#                     fx[i] = 0
#                     fy[i] = 0
#                     fz[i] = 0
#         Rx *= 0
#         Ry *= 0
#         Rz *= 0
#         for i in range(len(vals)):
#             r_i = rows[i]
#             c_i = cols[i]
#             v_i = vals[i]
#             Rx[r_i] += - v_i * fx[c_i]
#             Ry[r_i] += - v_i * fy[c_i]
#             Rz[r_i] += - v_i * fz[c_i]
#         Un = 0.0
#         for i in range(n):
#             Mi = M[i] * factor
#             Rx[i] += P[i, 0] - S[i, 0]
#             Ry[i] += P[i, 1] - S[i, 1]
#             Rz[i] += P[i, 2] - S[i, 2]
#             Rx[i] *= B[i, 0]
#             Ry[i] *= B[i, 1]
#             Rz[i] *= B[i, 2]
#             Rn[i] = sqrt(Rx[i]**2 + Ry[i]**2 + Rz[i]**2)
#             Vx[i] += Rx[i] / Mi
#             Vy[i] += Ry[i] / Mi
#             Vz[i] += Rz[i] / Mi
#             Un += Mi * (Vx[i]**2 + Vy[i]**2 + Vz[i]**2)
#         res = mean(Rn)
#         if Un < Uo:
#             Vx *= 0
#             Vy *= 0
#             Vz *= 0
#         Uo = Un
#         for i in range(n):
#             X[i, 0] += Vx[i]
#             X[i, 1] += Vy[i]
#             X[i, 2] += Vz[i]
#         ts += 1
#     if refresh:
#         print('Iterations: ', ts - 1)
#         print('Residual: ', res)
#     return X


@jit(nogil=True, nopython=True)
def numba_drx(tol, steps, factor, u, v, X, ks, l0, f0, ind_c, ind_t, rows, cols, vals, P, S, B, M, summary,
              inds, indi, indf, EIx, EIy, beams):
    """ Numba accelerated dynamic relaxation solver.

    Parameters:
        tol (float): Tolerance limit.
        steps (int): Maximum number of iteration steps.
        factor (float): Convergence factor.
        u (array): Network edges' start points.
        v (array): Network edges' end points.
        X (array): Nodal co-ordinates.
        ks (array): Initial edge axial stiffnesses.
        l0 (array) Initial edge lengths.
        f0 (array): Initial edge forces.
        ind_c (array): Compression only edges.
        ind_t (array): Tension only edges.
        rows (array): Edge adjacencies (rows).
        cols (array): Edge adjacencies (columns).
        vals (array): Edge adjacencies (values).
        P (array): Nodal loads Px, Py, Pz.
        S (array): Empty shear force array.
        B (array): Constraint conditions.
        M (array): Mass matrix.
        summary (int): Print summary 1 or 0.
        inds (array): Indices of beam element start nodes.
        indi (array): Indices of beam element intermediate nodes.
        indf (array): Indices of beam element finish nodes beams.
        EIx (array): Nodal EIx flexural stiffnesses.
        EIy (array): Nodal EIy flexural stiffnesses.
        beams (int): Beam analysis on: 1 or off: 0.

    Returns:
        array: Updated nodal co-ordinates.
    """
    m = len(u)
    n = X.shape[0]
    nv = len(vals)
    f = zeros(m)
    fx = zeros(m)
    fy = zeros(m)
    fz = zeros(m)
    Vx = zeros(n)
    Vy = zeros(n)
    Vz = zeros(n)
    frx = zeros(n)
    fry = zeros(n)
    frz = zeros(n)
    Rn = zeros(n)
    res = 1000 * tol
    ts = 0
    Uo = 0
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
                Qn = numba_cross(Qa, Qb)
                mu = 0.5 * (Xf - Xs)
                La = numba_length(Qa)
                Lb = numba_length(Qb)
                Lc = numba_length(Qc)
                LQn = numba_length(Qn)
                Lmu = numba_length(mu)
                a = arccos((La**2 + Lb**2 - Lc**2) / (2 * La * Lb))
                k = 2 * sin(a) / Lc
                ex = Qn / LQn
                ez = mu / Lmu
                ey = numba_cross(ez, ex)
                K = k * Qn / LQn
                Kx = numba_vdot(K, ex) * ex
                Ky = numba_vdot(K, ey) * ey
                Mc = EIx[i] * Kx + EIy[i] * Ky
                cma = numba_cross(Mc, Qa)
                cmb = numba_cross(Mc, Qb)
                ua = cma / numba_length(cma)
                ub = cmb / numba_length(cmb)
                c1 = numba_cross(Qa, ua)
                c2 = numba_cross(Qb, ub)
                Lc1 = numba_length(c1)
                Lc2 = numba_length(c2)
                Ms = Mc[0]**2 + Mc[1]**2 + Mc[2]**2
                Sa = ua * Ms * Lc1 / (La * numba_vdot(Mc, c1))
                Sb = ub * Ms * Lc2 / (Lb * numba_vdot(Mc, c2))
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
        print('Step:', ts, 'Residual:', res)
    return X


# def numba_dr_run(network, factor=1.0, tol=0.1, steps=10000, summary=0, bmesh=False, scale=0, update=False):
#     """ Run Numba accelerated dynamic relaxation analysis.

#     Parameters:
#         network (obj): Network to analyse.
#         factor (float): Convergence factor.
#         tol (float): Tolerance value.
#         steps (int): Maximum number of iteration steps.
#         summary (bool): Print summary at end.
#         bmesh (bool): Draw Blender mesh on or off.
#         scale (float): Scale on plotting axial forces.
#         update (bool): Update the co-ordinates of the Network.

#     Returns:
#         array: Vertex co-ordinates.
#         array: Edge forces.
#         array: Edge lengths.
#     """

#     # Setup

#     tic1 = time.time()
#     X, B, P, Pn, S, V, E, A, C, Ct, f0, l0, ind_c, ind_t, u, v, M, ks = create_arrays(network)
#     f0_, ks_, l0_, M_ = f0.ravel(), ks.ravel(), l0.ravel(), M.ravel()
#     try:
#         beams = 1
#         inds, indi, indf, EIx, EIy = beam_data(network.beams, network)
#         inds = array(inds)
#         indi = array(indi)
#         indf = array(indf)
#         EIx = EIx.ravel()
#         EIy = EIy.ravel()
#     except AttributeError:
#         beams = 0
#         z0 = array([0])
#         z1 = array([0.])
#         inds, indi, indf, EIx, EIy = z0, z0, z0, z1, z1
#     if not ind_c:
#         ind_c = [-1]
#     if not ind_t:
#         ind_t = [-1]
#     ind_c = array(ind_c)
#     ind_t = array(ind_t)
#     rows, cols, vals = find(Ct)
#     toc1 = time.time() - tic1

#     # Solver

#     if summary:
#         print('\n\nNumba DR -------------------------')
#     tic2 = time.time()
#     X = numba_dr_solver(tol, steps, factor, u, v, X, ks_, l0_, f0_, ind_c, ind_t, rows, cols, vals, P, S, B, M_, summary,
#                         inds, indi, indf, EIx, EIy, beams)
#     uvw, l = uvw_lengths(C, X)
#     f = f0 + ks * (l - l0)
#     toc2 = time.time() - tic2

#     # Plot results

#     # if bmesh:
#     #     edges = list(zip(u, v))
#     #     bmesh = draw_bmesh('network', vertices=X, edges=edges, layer=19)

#     # if scale:
#     #     fsc = abs(f) / max(abs(f))
#     #     log = (f > 0) * 1
#     #     colours = ['blue' if i else 'red' for i in log]
#     #     pipes = []
#     #     sp = X[u, :]
#     #     ep = X[v, :]
#     #     for c in range(len(f)):
#     #         r = scale * fsc[c]
#     #         pipes.append({'radius': r, 'start': sp[c, :], 'end': ep[c, :], 'colour': colours[c], 'name': str(f[c]), 'layer': 19})
#     #     xdraw_pipes(pipes, div=4)

#     # Summary

#     if summary:
#         print('Setup time: {0:.3g}s'.format(toc1))
#         print('Solver time: {0:.3g}s'.format(toc2))
#         print('----------------------------------')

#     # Update

#     if update:
#         k_i = network.key_index()
#         for key in list(network.vertices()):
#             i = k_i[key]
#             x, y, z = X[i, :]
#             network.set_vertex_attributes(i, {'x': x, 'y': y, 'z': z})

#     return X, f, l


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    pass
