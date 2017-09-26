from __future__ import print_function

import time

from numpy import arccos
from numpy import array
from numpy import cross
from numpy import isnan
from numpy import mean
from numpy import newaxis
from numpy import sin
from numpy import sum
from numpy import tile
from numpy import zeros

from scipy.sparse import find

from compas.numerical.geometry import uvw_lengths
from compas.numerical.matrices import connectivity_matrix
from compas.numerical.matrices import mass_matrix
from compas.numerical.linalg import normrow


__author__     = ['Tom Van Mele <vanmelet@ethz.ch>', 'Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2016, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


__all__ = [
    'drx'
]


def drx(network, factor=1.0, tol=1, steps=10000, refresh=0, beams=None, scale=0):
    """Run dynamic relaxation analysis.

    Parameters:
        network (obj): Network to analyse.
        factor (float): Convergence factor.
        tol (float): Tolerance value.
        steps (int): Maximum number of iteration steps.
        refresh (int): Update progress every n steps.
        beams (dic): Beam members data.
        scale (float): Scale on plotting axial forces.

    Returns:
        array: Vertex co-ordinates.
        array: Edge forces.
        array: Edge lengths.
    """

    # Setup

    tic = time.time()

    B, P, Pn, S, X, V, f0, l0, ind_c, ind_t, C, Ct, ks, u, v, M, rows, cols, vals, E, A = _create_arrays(network)

    if beams:
        inds, indi, indf, EIx, EIy = _beam_data(beams, network)
    else:
        inds, indi, indf, EIx, EIy = array([0]), array([0]), array([0]), array([0.0]), array([0.0])

    if refresh:
        print('----------------------------------')
        print('Setup time: {0:.3g}s'.format(time.time() - tic))

    # Solver

    tic = time.time()

    X, f, l = drx_numpy(tol, steps, C, Ct, V, M, B, S, P, X, f0, ks, l0, ind_c, ind_t,
                        refresh, factor, beams, inds, indi, indf, EIx, EIy)

    # elif solver == 'numba':
    #     if not ind_c:
    #         ind_c = [-1]
    #     if not ind_t:
    #         ind_t = [-1]

    #     ind_c = array(ind_c)
    #     ind_t = array(ind_t)

    #     if beams:
    #         EIx = EIx.ravel()
    #         EIy = EIy.ravel()
    #         beams = 1
    #     else:
    #         beams = 0

    #     f0 = f0.ravel()
    #     ks = ks.ravel()
    #     l0 = l0.ravel()
    #     M = M.ravel()

    #     X = drx_numba(tol, steps, u, v, X, f0, ks, l0, rows, cols, vals, P, B, M,
    #                   ind_c, ind_t, factor, inds, indi, indf, EIx, EIy, beams, S, refresh)

    #     uvw, l = uvw_lengths(C, X)
    #     f = f0 + ks * (l.ravel() - l0)

    if refresh:
        print('Solver time: {0:.3g}s'.format(time.time() - tic))
        print('----------------------------------')

    return X, f, l


def drx_numpy(tol, steps, C, Ct, V, M, B, S, P, X, f0, ks, l0, ind_c, ind_t, refresh, factor=1, beams=None,
              inds=None, indi=None, indf=None, EIx=None, EIy=None):
    """ Numpy and SciPy dynamic relaxation solver.

    Parameters:
        tol (float): Tolerance limit.
        steps (int): Maximum number of iteration steps.
        C (array): Connectivity matrix.
        Ct (array): Transposed connectivity matrix.
        V (array): Nodal velocities Vx, Vy, Vz.
        M (array): Mass matrix (untiled).
        B (array): Constraint conditions.
        S (array): Sx, Sy, Sz shear force components.
        P (array): Nodal loads Px, Py, Pz.
        X (array): Nodal co-ordinates.
        f0 (array): Initial edge forces.
        ks (array): Initial edge stiffnesses.
        l0 (array): Initial edge lengths.
        ind_c (list): Compression only edges.
        ind_t (list): Tension only edges.
        refresh (int): Update progress every n steps.
        factor (float): Convergence factor.
        beams (dic): Dictionary of beam information.
        inds (list): Indices of all beam element start nodes.
        indi (list): Indices of all beam element intermediate nodes.
        indf (list): Indices of all beam element finish nodes beams.
        EIx (array): Nodal EIx flexural stiffnesses for all beams.
        EIy (array): Nodal EIy flexural stiffnesses for all beams.

    Returns:
        array: Updated nodal co-ordinates.
        array: Final forces.
        array: Final lengths.
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
        q = tile(f / l, (1, 3))
        R = (P - S - Ct.dot(uvw * q)) * B
        Rn = normrow(R)
        res = mean(Rn)
        V += R / M
        Un = sum(0.5 * M * V**2)
        if Un < Uo:
            V *= 0
        Uo = Un
        X += V
        ts += 1
    if refresh:
        print('Iterations: {0}'.format(ts - 1))
        print('Residual: {0:.3g}'.format(res))
    return X, f, l


def _beam_data(beams, network):
    """ Create data for beam element calculations.

    Parameters:
        beams (dic): Dictionary of beam information.
        network (obj): Network to be analysed.

    Returns:
        list: Indices of all beam element start nodes.
        list: Indices of all beam element intermediate nodes.
        list: Indices of all beam element finish nodes beams.
        array: Nodal EIx flexural stiffnesses for all beams.
        array: Nodal EIy flexural stiffnesses for all beams.
    """
    inds, indi, indf = [], [], []
    EIx, EIy = [], []
    for key in beams:
        nodes = beams[key]['nodes']
        inds.extend(nodes[0:-2])
        indi.extend(nodes[1:-1])
        indf.extend(nodes[2:])
        EIx.extend([network.vertex[i]['EIx'] for i in nodes[1:-1]])
        EIy.extend([network.vertex[i]['EIy'] for i in nodes[1:-1]])
    EIx = array(EIx)[:, newaxis]
    EIy = array(EIy)[:, newaxis]
    return inds, indi, indf, EIx, EIy


def _beam_shear(S, X, inds, indi, indf, EIx, EIy):
    """ Generate the beam nodal shear forces Sx, Sy and Sz.

    Parameters:
        S (array): Empty or populated beam nodal shear force array.
        X (array): Co-ordinates of nodes.
        inds (list): Indices of all beam element start nodes.
        indi (list): Indices of all beam element intermediate nodes.
        indf (list): Indices of all beam element finish nodes beams.
        EIx (array): Nodal EIx flexural stiffnesses for all beams.
        EIy (array): Nodal EIy flexural stiffnesses for all beams.

    Returns:
        array: Updated beam nodal shears.
    """
    S *= 0
    Xs = X[inds, :]
    Xi = X[indi, :]
    Xf = X[indf, :]
    Qa = Xi - Xs
    Qb = Xf - Xi
    Qc = Xf - Xs
    Qn = cross(Qa, Qb)
    Qnn = normrow(Qn)
    La = normrow(Qa)
    Lb = normrow(Qb)
    Lc = normrow(Qc)
    a = arccos((La**2 + Lb**2 - Lc**2) / (2 * La * Lb))
    k = 2 * sin(a) / Lc
    mu = -0.5 * Xs + 0.5 * Xf
    mun = normrow(mu)
    ex = Qn / tile(Qnn, (1, 3))  # Temporary simplification
    ez = mu / tile(mun, (1, 3))
    ey = cross(ez, ex)
    K = tile(k / Qnn, (1, 3)) * Qn
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
    M = sum(Mc**2, 1)[:, newaxis]
    Sa = ua * tile(M * Lc1 / (La * sum(Mc * c1, 1)[:, newaxis]), (1, 3))
    Sb = ub * tile(M * Lc2 / (Lb * sum(Mc * c2, 1)[:, newaxis]), (1, 3))
    Sa[isnan(Sa)] = 0
    Sb[isnan(Sb)] = 0
    S[inds, :] += Sa
    S[indi, :] += - Sa - Sb
    S[indf, :] += Sb
    # Add node junction duplication for when elements cross each other
    # mu[0, :] = -1.25*x[0, :] + 1.5*x[1, :] - 0.25*x[2, :]
    # mu[-1, :] = 0.25*x[-3, :] - 1.5*x[-2, :] + 1.25*x[-1, :]
    return S


def _create_arrays(network):
    """ Create arrays needed for dr_solver.

    Parameters:
        network (obj): Network to analyse.

    Returns:
        array: Constraint conditions.
        array: Nodal loads Px, Py, Pz.
        array: Resultant nodal loads.
        array: Sx, Sy, Sz shear force components.
        array: x, y, z co-ordinates.
        array: Nodal velocities Vx, Vy, Vz.
        array: Edges' initial forces.
        array: Edges' initial lengths.
        list: Compression only edges.
        list: Tension only edges.
        array: Connectivity matrix.
        array: Transposed connectivity matrix.
        array: Axial stiffnesses.
        array: Network edges' start points.
        array: Network edges' end points.
        array: Mass matrix.
        list: Edge adjacencies (rows).
        list: Edge adjacencies (columns).
        list: Edge adjacencies (values).
        array: Young's moduli.
        array: Edge areas.
    """

    # Vertices

    n = network.number_of_vertices()
    B = zeros((n, 3))
    P = zeros((n, 3))
    X = zeros((n, 3))
    S = zeros((n, 3))
    V = zeros((n, 3))
    k_i = network.key_index()
    for key in network.vertices():
        i = k_i[key]
        vertex = network.vertex[key]
        B[i, :] = vertex['B']
        P[i, :] = vertex['P']
        X[i, :] = [vertex[j] for j in 'xyz']
    Pn = normrow(P)

    # Edges

    m = len(network.edges())
    E = zeros((m, 1))
    A = zeros((m, 1))
    s0 = zeros((m, 1))
    l0 = zeros((m, 1))
    u = []
    v = []
    ind_c = []
    ind_t = []
    edges = []
    uv_i = network.uv_index()
    for ui, vi in network.edges():
        i = uv_i[(ui, vi)]
        edge = network.edge[ui][vi]
        edges.append([k_i[ui], k_i[vi]])
        u.append(k_i[ui])
        v.append(k_i[vi])
        E[i] = edge['E']
        A[i] = edge['A']
        s0[i] = edge['s0']
        if edge['l0']:
            l0[i] = edge['l0']
        else:
            l0[i] = network.edge_length(ui, vi)
        if edge['ct'] == 'c':
            ind_c.append(i)
        elif edge['ct'] == 't':
            ind_t.append(i)
    f0 = s0 * A
    ks = E * A / l0

    # Arrays

    C = connectivity_matrix(edges, 'csr')
    Ct = C.transpose()
    M = mass_matrix(Ct, E, A, l0, f0, c=1, tiled=False)
    rows, cols, vals = find(Ct)

    return B, P, Pn, S, X, V, f0, l0, ind_c, ind_t, C, Ct, ks, array(u), array(v), M, rows, cols, vals, E, A


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    import compas
    from compas.datastructures.network import Network

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

    lines = compas.get_data('lines.obj')

    network = Network.from_obj(lines)
    network.update_default_vertex_attributes(dva)
    network.update_default_edge_attributes(dea)

    for key, attr in network.vertices(True):
        attr['is_fixed'] = network.vertex_degree(key) == 1

    count = 1
    for u, v, attr in network.edges(True):
        attr['qpre'] = count
        count += 1

    res = drx(network)

    print(res)
