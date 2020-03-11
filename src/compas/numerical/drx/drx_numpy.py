from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

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

    Examples
    --------
    >>>
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
    X, f, l = drx_solver_numpy(tol, steps, factor, C, Ct, X, M, k0, l0, f0, ind_c, ind_t, P, S, B, V, refresh,  # noqa: E741
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
        for key in structure.nodes():
            i = k_i[key]
            structure.node_attributes(key, 'xyz', X[i])
        uv_i = structure.uv_index()
        for uv in structure.edges():
            i = uv_i[uv]
            structure.edge_attribute(uv, 'f', float(f[i]))

    return X, f, l, structure


def drx_solver_numpy(tol, steps, factor, C, Ct, X, M, k0, l0, f0, ind_c, ind_t, P, S, B, V, refresh,
                     beams, inds, indi, indf, EIx, EIy, callback, **kwargs):
    """NumPy and SciPy dynamic relaxation solver.

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

        uvw, l = uvw_lengths(C, X)  # noqa: E741
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
    if structure.attributes.get('beams', None):
        inds, indi, indf, EIx, EIy = [], [], [], [], []
        for beam in structure.attributes['beams'].values():
            nodes = beam['nodes']
            inds.extend(nodes[:-2])
            indi.extend(nodes[1:-1])
            indf.extend(nodes[2:])
            EIx.extend([structure.node_attribute(i, 'EIx') for i in nodes[1:-1]])
            EIy.extend([structure.node_attribute(i, 'EIy') for i in nodes[1:-1]])
        inds = array(inds, dtype=int32)
        indi = array(indi, dtype=int32)
        indf = array(indf, dtype=int32)
        EIx = array(EIx, dtype=float64)
        EIy = array(EIy, dtype=float64)
        beams = 1
    else:
        inds = indi = indf = array([0], dtype=int32)
        EIx = EIy = array([0.], dtype=float64)
        beams = 0

    print(indf)

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
    La = normrow(Qa)
    Lb = normrow(Qb)
    Lc = normrow(Qc)
    LQn = normrow(Qn)
    Lmu = normrow(mu)
    a = arccos((La**2 + Lb**2 - Lc**2) / (2 * La * Lb))
    k = 2 * sin(a) / Lc
    ex = Qn / tile(LQn, (1, 3))
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
    return S


def _create_arrays(structure):
    # Vertices
    n = structure.number_of_nodes()
    B = zeros((n, 3), dtype=float64)
    P = zeros((n, 3), dtype=float64)
    X = zeros((n, 3), dtype=float64)
    S = zeros((n, 3), dtype=float64)
    V = zeros((n, 3), dtype=float64)
    k_i = structure.key_index()
    for key in structure.nodes():
        i = k_i[key]
        B[i, :] = structure.node_attribute(key, 'B')
        P[i, :] = structure.node_attribute(key, 'P')
        X[i, :] = structure.node_attributes(key, 'xyz')

    # Edges
    m = structure.number_of_edges()
    u = zeros(m, dtype=int32)
    v = zeros(m, dtype=int32)
    E = zeros(m, dtype=float64)
    A = zeros(m, dtype=float64)
    s0 = zeros(m, dtype=float64)
    l0 = zeros(m, dtype=float64)
    ind_c = []
    ind_t = []
    uv_i = structure.uv_index()
    for key in structure.edges():
        i = uv_i[key]
        E[i] = structure.edge_attribute(key, 'E')
        A[i] = structure.edge_attribute(key, 'A')
        if structure.edge_attribute(key, 'l0'):
            l0[i] = structure.edge_attribute(key, 'l0')
        else:
            l0[i] = structure.edge_length(*key)
        if structure.edge_attribute(key, 's0'):
            s0[i] = structure.edge_attribute(key, 's0')
        else:
            s0[i] = 0
        u[i] = k_i[key[0]]
        v[i] = k_i[key[1]]
        ct = structure.edge_attribute(key, 'ct')
        if ct == 'c':
            ind_c.append(i)
        elif ct == 't':
            ind_t.append(i)
    f0 = s0 * A
    k0 = E * A / l0
    q0 = f0 / l0

    print(k0)

    # Other
    C = connectivity_matrix([[k_i[i], k_i[j]] for i, j in structure.edges()], 'csr')
    Ct = C.transpose()
    M = mass_matrix(Ct=Ct, ks=k0, q=q0, c=1, tiled=False)
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
    pass
