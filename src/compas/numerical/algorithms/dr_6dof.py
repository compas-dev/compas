
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.datastructures import Network

from compas.hpc import cross_vectors_numba
from compas.hpc import dot_vectors_numba as vdotv
from compas.hpc import length_vector_numba
from compas.hpc import multiply_matrices_numba as mdotm
from compas.hpc import multiply_matrix_vector_numba as mdotv
from compas.hpc import norm_vector_numba

from copy import copy

from time import time

import sys

try:

    from numpy import arctan
    from numpy import arcsin
    from numpy import array
    from numpy import concatenate
    from numpy import cos
    from numpy import cross
    from numpy import diag
    from numpy import dot
    from numpy import eye
    from numpy import float64
    from numpy import int64
    from numpy import hstack
    from numpy import vstack
    from numpy import round
    from numpy import sin
    from numpy import sqrt
    from numpy import sort
    from numpy import tan
    from numpy import trace
    from numpy import zeros
    from numpy import where
    from numpy.linalg import norm

    from scipy.sparse import csc_matrix
    from scipy.sparse.linalg import spsolve

    from numba import jit
    from numba import f8
    from numba import i8
    from numba.types import Tuple

except ImportError:

    if 'ironpython' not in sys.version.lower():
        raise


__author__    = ['Jef Rombouts <jef.rombouts@kuleuven.be>', 'Andrew Liew <liew@arch.ethz.ch>']
__copyright__ = 'Copyright 2018, BLOCK Research Group - ETH Zurich'
__license__   = 'MIT License'
__email__     = 'liew@arch.ethz.ch'


__all__ = [
    'dr_6dof_numba',
]


def dr_6dof_numba(network, dt=1.0, xi=1.0, tol=0.001, steps=100, geomstiff=False):

    """ Run dynamic relaxation analysis with 6 DoF per node.

    Parameters
    ----------
    network : obj
        Network to analyse.
    dt : float
        Time step.
    xi : float
        Damping ratio.
    tol : float
        Tolerance value.
    steps : int
        Maximum number of steps.
    geomstiff : bool
        Include geometric stiffness.

    Returns
    -------
    X : array
        Node co-ordinates.
    x : array
        Positions and orientations of all free DoF.
    x0 : array
        Initial positions and orientations of all free DoF.

    """

    # Create arrays

    k_i, i_k, X, n, d, p, x0, x, v, r, fdof_node, fdof_axis, fdof = _create_vertex_arrays(network)
    edges, l, T0, l0, I, J, row, col, edgei, Kall, data = _create_edge_arrays(network, fdof, fdof_node)

    # Indexing

    ca = 0
    IDXx, ca = _indexdof(fdof, 0.01, ca, n)
    IDXy, ca = _indexdof(fdof, 0.02, ca, n)
    IDXz, ca = _indexdof(fdof, 0.03, ca, n)
    IDXtra = sort(concatenate((IDXx, IDXy, IDXz)), 0)
    nct = 3 * n - ca
    IDXtra = IDXtra[0:nct]
    IDXtra = array([int(round(j)) for j in IDXtra], dtype=int64)

    cr = 0
    IDXalpha, cr = _indexdof(fdof, 0.04, cr, n)
    IDXbeta, cr = _indexdof(fdof, 0.05, cr, n)
    IDXgamma, cr = _indexdof(fdof, 0.06, cr, n)
    IDXrot = sort(concatenate((IDXalpha, IDXbeta, IDXgamma)), 0)
    nct = 3 * n - cr
    IDXrot = IDXrot[0:nct]
    IDXrot = array([int(round(j)) for j in IDXrot], dtype=int64)

    # Initialise

    f     = zeros((d, 1))
    Szu   = zeros((3, 3))
    Syu   = zeros((3, 3))
    Sxu   = zeros((3, 3))
    Szv   = zeros((3, 3))
    Syv   = zeros((3, 3))
    Sxv   = zeros((3, 3))
    Sr2   = zeros((3, 3))
    Sr1   = zeros((3, 3))
    Sr0   = zeros((3, 3))
    Sbt   = zeros((3, 3))
    Sx    = zeros((3, 3))
    Szuzv = zeros((3, 3))
    Syvyu = zeros((3, 3))
    K     = zeros((d, d))

    eye3   = eye(3)
    zero3  = zeros(3)
    zero6  = zeros(6)
    zero9  = zeros(9)
    zero33 = zeros((3, 3))

    Lambdaold = zeros(3, dtype=float64)
    dLambda   = zeros(3, dtype=float64)

    fdof_node = array(fdof_node, dtype=int64)
    fdof_axis = array(fdof_axis, dtype=int64)
    fdof_rot  = fdof_node[IDXrot]
    fdof_rot_ = array(list(set(fdof_rot)), dtype=int64)

    ind = zeros((len(fdof_rot_), 3), dtype=int64)
    for i, value in enumerate(fdof_rot_):
        ind[i, :] = where(fdof_rot == value)[0]

    # Main loop

    ts = 0
    rnorm = tol + 1

    while ts <= steps and rnorm > tol:

        f *= 0
        count = 0
        x_ = concatenate((x, [[0.0]]), 0)

        # WRAP THIS WHOLE LOOP INTO A NUMBA FUNCTION -------------------------------------------------------------------

        for c, uv in enumerate(edges):  # edges turn into a m x 2 array, with ui and vi as the column data

            i = edgei[c]
            ui, vi = uv

            # Update lengths

            xe = (X[k_i[vi], :] - X[k_i[ui], :])  # make array for k_i for both ui and vi
            l[i] = length_vector_numba(xe)

            # Update triads

            t0t = T0[(i * 3):((i + 1) * 3), 0:3]
            Tu = _beam_triad(ui, x_, IDXalpha, IDXbeta, IDXgamma, t0t, Sbt)
            Tv = _beam_triad(vi, x_, IDXalpha, IDXbeta, IDXgamma, t0t, Sbt)
            Re = _element_rotmat(Tu, Tv)

            xu, yu, zu = Tu[:, 0], Tu[:, 1], Tu[:, 2]
            xv, yv, zv = Tv[:, 0], Tv[:, 1], Tv[:, 2]
            xe /= norm(xe)
            ye = Re[:, 1] - vdotv(Re[:, 1], xe) / 2 * (xe + Re[:, 0])
            ze = Re[:, 2] - vdotv(Re[:, 2], xe) / 2 * (xe + Re[:, 0])

            # Calculate local beam deformations

            theta = _deformations(xe, ye, ze, xu, yu, zu, xv, yv, zv)

            # Internal forces and stiffness matrix

            T = _create_T(eye3, zero3, zero6, zero9, xe, ye, ze, Re, Sr0, Sr1, Sr2, Sxu, Syu, Szu, Sxv, Syv, Szv,
                          theta, xu, yu, zu, xv, yv, zv, l[i])

            K_ = 1. / l0[i][0] * Kall[:, :, i]
            Ke_e = mdotm(mdotm(T, K_), T.transpose())
            Ke_g = 0
            if geomstiff:
                pass
#                 Ke_g = _geometric_stiffmatrix(zero3_3, zero12_3, f_, B, L_2, L_3, theta, Sr0, Sr1, Sr2, Sxu, Syu, Szu, Sxv, Syv, Szv, Sx, Szuzv, Syvyu, T, R_e, array([x_e]).transpose(), T_u, T_v, l[i][0])
            Ke = Ke_e + Ke_g

            f = _element_forces(l[i][0], l0[i][0], theta, T, f, I[i], J[i], i, K_)

            data, count = _data(Ke, I[i], J[i], data, count)

        # --------------------------------------------------------------------------------------------------------------

        K = csc_matrix((data, (row, col)), shape=(d, d))

        # Update residual forces

        r = p - f
        rnorm = mdotm(r.transpose(), r)**0.5

        # Update displacements and velocities

        ds = xi * dt
        v = (1 - ds) / (1 + ds) * v + array([spsolve(K, r)]).transpose() / (1 + ds) * dt  # find an alternative to spsolve
        x = _update(x, v, dt, IDXtra, Lambdaold, dLambda, fdof_node, fdof_axis, IDXrot, fdof_rot, fdof_rot_, ind)

        for i in range(len(IDXtra)):
            X[fdof_node[IDXtra[i]]][fdof_axis[IDXtra[i]]] = x[IDXtra[i]][0]

        ts += 1

    # Update network

    for i in network.vertices():
        network.set_vertex_attributes(i_k[i], {'x': X[i, 0], 'y': X[i, 1], 'z': X[i, 2]})

    return X#, x, x0


def _create_vertex_arrays(network):

    """ Initialise force, position, and velocity vectors

    Parameters
    ----------
    network : obj
        Network to analyse.

    Returns
    -------
    dic
        Key to index dictionary.
    dic
       Index to key dictionary.
    array
        Nodal co-ordinates.
    int
        Number of nodes.
    int
        Number of free degrees-of-freedom.
    array
        Loads on every free degree-of-freedom.
    array
        Initial values for the coordinates/rotation components describing nodal positions and orientations.
    array
        Position array.
    array
        Velocity array.
    array
        Residual force array.
    list
        Indexing list with node numbers for all fdof.
    list
        Indexing list with axis numbers for all fdof.
    list
        List containing all degrees of freedom as [node].0[axis].

    """

    k_i = network.key_index()
    i_k = network.index_key()
    n = network.number_of_vertices()

    fdof = []
    fdof_node = []
    fdof_axis = []
    X = zeros((n, 3))
    P = zeros((n, 6))

    for key, vertex in network.vertex.items():
        i = k_i[key]
        X[i, :] = network.vertex_coordinates(key=key)

        for ci, Pi in enumerate(['px', 'py', 'pz', 'palpha', 'pbeta', 'pgamma']):
            P[i, ci] = vertex.get(Pi, 0)

        for ci, dof in enumerate(['dofx', 'dofy', 'dofz', 'dofalpha', 'dofbeta', 'dofgamma'], 1):
            if vertex.get(dof, True):
                fdof.append(i + 0.01 * ci)
                fdof_node.append(i)
                fdof_axis.append(ci - 1)

    d = len(fdof)
    p  = zeros((d, 1))
    v  = zeros((d, 1))
    x0 = zeros((d, 1))

    for ci, uv in enumerate(zip(fdof_node, fdof_axis)):
        node, axis = uv
        p[ci] = P[node, axis]
        if axis <= 2:
            x0[ci] = X[node, axis]

    x = copy(x0)
    r = copy(p)

    return k_i, i_k, X, n, d, p, x0, x, v, r, fdof_node, fdof_axis, fdof


def _create_edge_arrays(network, fdof, fdof_node):

    """ Initialise local element stiffness matrices, co-ordinate systems, and other edge-related arrays

    Parameters
    ----------
    network : obj
        Network to analyse.
    fdof : list
        Degrees-of-freedom.
    fdof_node : list
        Nodes corresponding to fdof

    Returns
    -------
    list
        All edges in the network.
    list
        Edge lengths.
    list
        Initial local coordinate system for each edge.
    list
        Initial edge lengths.
    list
        Indices for accessing f.
    list
        Indices for accessing f_.
    list
        Row indices for sparse assembly of K.
    list
        Column indices for sparse assembly of K.
    list
        Initial data for sparse assembly of K.
    list
        Edge indices.
    matrix
        3D matrix of local element siffness matrices.

     """

    uv_i = network.uv_index()
    edges = list(network.edges())
    m  = len(edges)

    l  = zeros((m, 1))
    l0 = zeros((m, 1))
    T0 = zeros((m * 3, 3))
    Kall = zeros((7, 7, m))

    I = []
    J = []
    col = []
    row = []
    edgei = []

    for ui, vi in edges:

        i = uv_i[(ui, vi)]
        edgei.append(i)
        edge = network.edge[ui][vi]
        wi = edge.get('w')
        l0[i] = network.edge_length(ui, vi)
        l[i] = copy(l0[i])

        x0 = array(network.vertex_coordinates(vi)) - array(network.vertex_coordinates(ui))
        x0 /= norm(x0)
        z0 = cross(array(network.vertex_coordinates(ui)) - array(network.vertex_coordinates(wi)), x0)
        z0 /= norm(z0)
        y0 = cross(z0, x0)
        T0[i * 3:(i + 1) * 3, 0:3] = array([x0, y0, z0]).transpose()

        Ju = array([], dtype=int)
        Iu = where(array(fdof_node) == ui)[0]
        if len(Iu):
            Ju = (array(fdof)[Iu] - ui) * 100 - 1
            Ju = array([int(round(j)) for j in Ju], dtype=int64)

        Jv = array([], dtype=int)
        Iv = where(array(fdof_node) == vi)[0]
        if len(Iv):
            Jv = (array(fdof)[Iv] - vi) * 100 + 5
            Jv = array([int(round(j)) for j in Jv], dtype=int64)

        I.append(concatenate((Iu, Iv), 0))
        J.append(concatenate((Ju, Jv), 0))

        for j in range(len(I[i])):
            for k in range(len(I[i])):
                row.append(I[i][j])
                col.append(I[i][k])

        E  = edge.get('E', 0)
        A  = edge.get('A', 0)
        nu = edge.get('nu', 0)
        Ix = edge.get('Ix', 0)
        Iy = edge.get('Iy', 0)
        Iz = edge.get('Iz', 0)
        G  = E / (2. * (1. + nu))
        EA  = E * A
        GIx = G * Ix
        EIy = E * Iy
        EIz = E * Iz

        Kall[:, :, i] = array([
            [EA, 0,   0,    0,    0,   0,    0   ],
            [0, GIx,  0,    0,  -GIx,  0,    0   ],
            [0,  0,  4*EIy, 0,    0,  2*EIy, 0   ],
            [0,  0,   0,   4*EIz, 0,   0,   2*EIz],
            [0, -GIx, 0,    0,    GIx, 0,    0   ],
            [0,  0,  2*EIy, 0,    0,  4*EIy, 0   ],
            [0,  0,   0,   2*EIz, 0,   0,   4*EIz]])

    data = zeros(len(row))

    return edges, l, T0, l0, I, J, row, col, edgei, Kall, data


def _indexdof(fdof, seldof, count, n):

    """ Makes list of indices to access seldof degrees-of-freedom in fdof.

    Parameters
    ----------
    fdof : list
        All unconstrained degrees-of-freedom.
    seldof : float
        Degrees-of-freedom.
    count : int
        Counter for number of constrained dof of specific type (translations or rotations).
    n : int
        Number of vertices.

    Returns
    -------
    array
        List of indices.
    int
        Counter.

    """

    IDX = zeros(n, dtype=int64)

    for i in range(n):
        if i + seldof in fdof:
            idx = fdof.index(i + seldof)
        else:
            idx = len(fdof)
            count += 1
        IDX[i] = idx

    return IDX, count


@jit(f8[:, :](f8[:, :], f8[:]), nogil=True, nopython=True)
def _skew_(S, v):

    """ Modifies the skew-symmetric matrix S in place.

    Parameters
    ----------
    S : array
        Original skew array to edit.
    v : array
        A vector.

    Returns
    -------
    array
        S of v.

    """

    S[0, 1] = -v[2]
    S[0, 2] =  v[1]
    S[1, 0] =  v[2]
    S[1, 2] = -v[0]
    S[2, 0] = -v[1]
    S[2, 1] =  v[0]

    return S


@jit(f8[:, :](i8, f8[:, :], i8[:], i8[:], i8[:], f8[:, :], f8[:, :]), nogil=True, nopython=True)
def _beam_triad(i, x_, IDXalpha, IDXbeta, IDXgamma, T0, Sbt):

    """ Construct the current nodal beam triad for vertex 'key'.

    Parameters
    ----------
    i : int
        Index.
    x_ : array
        Extended array of displacements.
    IDXalpha : array
        Alpha-dof index.
    IDXbeta : array
        Beta-dof index.
    IDXgamma : array
        Gamma-dof index.
    T0 : array
        -
    Sbt : array
        Pre-made S.

    Returns
    -------
    array
        T matrix.

    """

    alpha = x_[IDXalpha[i]][0]
    beta  = x_[IDXbeta[i]][0]
    gamma = x_[IDXgamma[i]][0]
    Lbda = array([alpha, beta, gamma])
    lbda = norm_vector_numba(Lbda)

    if lbda == 0.:
        R = eye(3)
    else:
        lbda_ = Lbda / lbda
        S = _skew_(Sbt, lbda_)
        R = eye(3) + sin(lbda) * S + (1. - cos(lbda)) * mdotm(S, S)

    T = mdotm(R, T0)

    return T


@jit(f8[:](f8[:], f8[:], f8[:], f8[:], f8[:], f8[:], f8[:], f8[:], f8[:]),
     nogil=True, nopython=True)
def _deformations(xe, ye, ze, xu, yu, zu, xv, yv, zv):

    """ Calculate local element deformations.

     Parameters
     ----------
     xe : array
         Edge x-direction.
     ye : array
         Edge y-direction.
     ze : array
         Edge z-direction.
     xu : array
         Vertex u x-direction.
     yu : array
         Vertex u y-direction.
     zu : array
         Vertex u z-direction.
     xv : array
         Vertex v x-direction.
     yv : array
         Vertex v y-direction.
     zv : array
         Vertex v z-direction.

     Returns
     -------
     array
         Thetas

     """

    theta_xu = arcsin(0.5 * (vdotv(ze, yu) - vdotv(zu, ye)))
    theta_xv = arcsin(0.5 * (vdotv(ze, yv) - vdotv(zv, ye)))
    theta_yu = arcsin(0.5 * (vdotv(ze, xu) - vdotv(zu, xe)))
    theta_yv = arcsin(0.5 * (vdotv(ze, xv) - vdotv(zv, xe)))
    theta_zu = arcsin(0.5 * (vdotv(ye, xu) - vdotv(yu, xe)))
    theta_zv = arcsin(0.5 * (vdotv(ye, xv) - vdotv(yv, xe)))

    return array([theta_xu, theta_xv, theta_yu, theta_yv, theta_zu, theta_zv])


@jit(f8[:, :](f8[:, :], f8[:], f8[:], f8[:], f8[:], f8[:], f8[:], f8[:, :], f8[:, :], f8[:, :], f8[:, :], f8[:, :],
     f8[:, :], f8[:, :], f8[:, :], f8[:, :], f8[:, :], f8[:], f8[:], f8[:], f8[:], f8[:], f8[:], f8[:], f8[:]), nogil=True, nopython=True)
def _create_T(eye3, zero3, zero6, zero9, xe, ye, ze, Re, Sr0, Sr1, Sr2, Sxu, Syu, Szu, Sxv, Syv, Szv, theta, xu, yu, zu, xv, yv, zv, li):

    """

    Add comments

    """

    Sr0 = _skew_(Sr0, Re[:, 0])
    Sr1 = _skew_(Sr1, Re[:, 1])
    Sr2 = _skew_(Sr2, Re[:, 2])
    Szu = _skew_(Szu, zu)
    Syu = _skew_(Syu, yu)
    Sxu = _skew_(Sxu, xu)
    Szv = _skew_(Szv, zv)
    Syv = _skew_(Syv, yv)
    Sxv = _skew_(Sxv, xv)

    xe_t  = zeros((3, 1))
    Re1_t = zeros((3, 1))
    xe_Re = zeros((1, 3))
    Re2_t = zeros((3, 1))
    xe_t[:, 0]  = xe
    Re1_t[:, 0] = Re[:, 1]
    Re2_t[:, 0] = Re[:, 2]
    xe_Re[0, :] = xe + Re[:, 0]

    B = 1. / li[0] * (eye3 - mdotm(xe_t, xe_t.transpose()))
    k = mdotm(xe_t, xe_Re)
    Re1xe = vdotv(Re[:, 1], xe)
    Re2xe = vdotv(Re[:, 2], xe)

    L1_2 = 0.5 * Re1xe * B + mdotm(0.5 * B, mdotm(Re1_t, xe_Re))
    L1_3 = 0.5 * Re2xe * B + mdotm(0.5 * B, mdotm(Re2_t, xe_Re))
    L2_2 = 0.5 * Sr1 - 0.25 * Re1xe * Sr0 - mdotm(0.25 * Sr1, k)
    L2_3 = 0.5 * Sr2 - 0.25 * Re2xe * Sr0 - mdotm(0.25 * Sr2, k)
    L_2 = vstack((L1_2, L2_2, -L1_2, L2_2))
    L_3 = vstack((L1_3, L2_3, -L1_3, L2_3))

    Bzu = mdotv(B, zu)
    Byu = mdotv(B, yu)
    Bzv = mdotv(B, zv)
    Byv = mdotv(B, yv)

    h1 = hstack((zero3, (mdotv(-Szu, ye) + mdotv(Syu, ze)), zero6))
    h2 = hstack((Bzu, (mdotv(-Szu, xe) + mdotv(Sxu, ze)), -Bzu, zero3))
    h3 = hstack((Byu, (mdotv(-Syu, xe) + mdotv(Sxu, ye)), -Byu, zero3))
    h4 = hstack((zero9, (mdotv(-Szv, ye) + mdotv(Syv, ze))))
    h5 = hstack((Bzv, zero3, -Bzv, (mdotv(-Szv, xe) + mdotv(Sxv, ze))))
    h6 = hstack((Byv, zero3, -Byv, (mdotv(-Syv, xe) + mdotv(Sxv, ye))))

    T = zeros((12, 7))
    T[:, 0] = hstack((-xe, zero3, xe, zero3))
    T[:, 1] = (mdotv(L_3, yu) - mdotv(L_2, zu) + h1) / (2 * cos(theta[0]))
    T[:, 2] = (mdotv(L_3, xu) + h2) / (2 * cos(theta[2]))
    T[:, 3] = (mdotv(L_2, xu) + h3) / (2 * cos(theta[4]))
    T[:, 4] = (mdotv(L_3, yv) - mdotv(L_2, zv) + h4) / (2 * cos(theta[1]))
    T[:, 5] = (mdotv(L_3, xv) + h5) / (2 * cos(theta[3]))
    T[:, 6] = (mdotv(L_2, xv) + h6) / (2 * cos(theta[5]))

    return T


@jit(f8[:, :](f8[:, :], f8[:, :]), nogil=True, nopython=True)
def _element_rotmat(Tu, Tv):

    """ Calculates the 'average nodal rotation matrix' Re for the calculation of the element triad.

    Parameters
    ----------
    Tu : array
        Beam end triad for vertex u.
    Tv : array
        Beam end triad for vertex v.

    Returns
    -------
    array
        Re matrix.

    """

    dR = mdotm(Tv, Tu.transpose())
    q0 = 0.5 * sqrt(1. + trace(dR))
    q04 = 4. * q0
    q1 = (dR[2, 1] - dR[1, 2]) / q04
    q2 = (dR[0, 2] - dR[2, 0]) / q04
    q3 = (dR[1, 0] - dR[0, 1]) / q04
    q = array([q1, q2, q3])
    normq = norm_vector_numba(q)

    mu = 2. * abs(arctan(normq / q0))
    if mu == 0.:
        e = array([1., 1., 1.])
    else:
        e = q / normq

    S = zeros((3, 3))
    S[0, 1] = -e[2]
    S[0, 2] =  e[1]
    S[1, 0] =  e[2]
    S[1, 2] = -e[0]
    S[2, 0] = -e[1]
    S[2, 1] =  e[0]

    dRm = eye(3) + sin(0.5 * mu) * S + (1. - cos(0.5 * mu)) * mdotm(S, S)
    Re = mdotm(dRm, Tu)

    return Re


@jit(f8[:](f8[:]), nogil=True, nopython=True)
def _quaternion(Lbda):

    """ Get the quaternion formulation for a given rotation vector Lbda.

    Parameters
    ----------
    Lbda : array
        Rotation vector.

    Returns
    -------
    array
        [q, q0]

    """

    lbda = norm_vector_numba(Lbda)
    if lbda == 0.:
        L = Lbda
    else:
        L = Lbda / lbda
    q = sin(0.5 * lbda) * L
    q0 = cos(0.5 * lbda)

    return array([q[0], q[1], q[2], q0])


@jit(f8[:, :](f8, f8, f8[:], f8[:, :], f8[:, :], i8[:], i8[:], i8, f8[:, :]), nogil=True, nopython=True)
def _element_forces(li, l0i, theta, T, f, Ii, Ji, i, K_):

    """ Calculate element forces and element elastic stiffness matrix.

    Parameters
    ----------
    li : float
        Edge length.
    l0i: float
        Initial edge length.
    theta : array
        Array of thetas.
    T : array
        Transformation matrix.
    f : array
        Forces array.
    Ji : -
        -
    i: int
        Edge index.
    K_ : array
        -

    Returns
    -------

    tbc

    """

    u_ = zeros((7, 1))
    u_[0, 0] = li - l0i
    u_[1, 0] = theta[0]
    u_[2, 0] = theta[2]
    u_[3, 0] = theta[4]
    u_[4, 0] = theta[1]
    u_[5, 0] = theta[3]
    u_[6, 0] = theta[5]

    f_ = mdotm(K_, u_)
    fe = mdotm(T, f_)
    f[Ii] += fe[Ji]

    return f


@jit(Tuple((f8[:], i8))(f8[:, :], i8[:], i8[:], f8[:], i8), nogil=True, nopython=True)
def _data(Ke, Ii, Ji, data, count):

    """

    Add comments

    """

    for j in range(len(Ii)):
        for k in range(len(Ii)):
            data[count] = (Ke[Ji[j]][Ji[k]])
            count += 1

    return data, count


# this function still feels messy to me, could be reworked
@jit(f8[:, :](f8[:, :], f8[:, :], f8, i8[:], f8[:], f8[:], i8[:], i8[:], i8[:], i8[:], i8[:], i8[:, :]), nogil=True, nopython=True)
def _update(x, v, dt, IDXtra, Lambdaold, dLambda, fdof_node, fdof_axis, IDXrot, fdof_rot, fdof_rot_, ind):

    """

    Add comments

    """

    dx = dt * v
    xold = x
    x[IDXtra] = xold[IDXtra] + dx[IDXtra]
    Lambdaold *= 0.
    dLambda *= 0.

    for i in range(len(fdof_rot_)):

        for jj in range(3):
            j = ind[i, jj]
            index = fdof_axis[IDXrot[j]]
            Lambdaold[index - 3] = xold[IDXrot[j]][0]
            dLambda[index - 3] = dx[IDXrot[j]][0]

        qO = _quaternion(Lambdaold)
        qQ = _quaternion(dLambda)
        qold, q0old = qO[:3], qO[3]
        dq, dq0 = qQ[:3], qQ[3]
        qnew = q0old * dq + dq0 * qold - cross_vectors_numba(qold, dq)
        q0new = q0old * dq0 - vdotv(qold, dq)
        lambdanew = 2 * arctan(norm_vector_numba(qnew) / q0new)

        if norm(qnew) == 0.:
            Lnew = qnew
        else:
            Lnew = qnew / norm_vector_numba(qnew)
        Lambdanew = lambdanew * Lnew

        value = fdof_rot_[i]
        for j in range(len(fdof_rot)):
            if fdof_rot[j] == value:
                x[IDXrot[j]] = Lambdanew[fdof_axis[IDXrot[j]] - 3]

    return x


# @jit(f8[:, :](f8[:, :], f8[:, :], f8[:, :], f8, f8[:, :], f8[:, :], f8[:, :], f8[:, :], f8[:, :], f8[:, :], f8[:, :], f8[:, :], f8[:, :], f8[:, :], f8[:, :], f8[:, :], f8[:, :], f8[:, :]),
#      nogil=True, nopython=True)
# def K_g2(r_i, o, B, l, x, r_0, Sr0, Sx, Sri, So, riT_B, riT_xe, B_ri, B_ri_xeT, xeT_Sri, B_Sri, Sri_xe, Sx_Sri):
#     """ Calculate K_g2 for the geometric stiffness matrix

#     Parameters
#     ----------
#         ri:
#             y- or z- Direction of the element rotation vector R_e.
#         o:
#             Vector.
#         B:
#             Matrix B.
#         l:
#             Length of the element.
#         x:
#             Vector in element x-direction.
#         r_0:
#             x-Direction of the element rotation vector R_e.

#     Returns
#     -------
#         matrix
#             K_g2.

#     """
#     B_o = multiply_matrices_numba(B, o)
#     oT_xr0 = multiply_matrices_numba(o.transpose(), (x + r_0))
#     U = -1 / 2 * multiply_matrices_numba(B_o, riT_B) + (riT_xe / (2 * l)) * multiply_matrices_numba(B_o, x.transpose()) + (oT_xr0 / (2 * l)) * B_ri_xeT

#     K11 = U + U.transpose() + riT_xe * (2 * multiply_matrices_numba(x.transpose(), o) + multiply_matrices_numba(o.transpose(), r_0)) * B
#     K33 = K11
#     K13 = -K11
#     K31 = -K11

#     K12 = (multiply_matrices_numba(-B_o, xeT_Sri) - multiply_matrices_numba(B_ri, multiply_matrices_numba(o.transpose(), Sr0)) - oT_xr0 * B_Sri) / 4
#     K14 = K12
#     K32 = -K12
#     K34 = -K12
#     K21 = K12.transpose()
#     K41 = K12.transpose()
#     K23 = -K12.transpose()
#     K43 = -K12.transpose()

#     K22 = ((-riT_xe * multiply_matrices_numba(So, Sr0) + multiply_matrices_numba(multiply_matrices_numba(Sr0, o), xeT_Sri) +
#             multiply_matrices_numba(Sri_xe, multiply_matrices_numba(o.transpose(), Sr0)) - multiply_matrices_numba(x.transpose() +
#             r_0.transpose(), o) * Sx_Sri + 2 * multiply_matrices_numba(So, Sri)) / 8)
#     K24 = K22
#     K42 = K22
#     K44 = K22

#     K_g2 = vstack((hstack((K11, K12, K13, K14)), hstack((K21, K22, K23, K24)), hstack((K31, K32, K33, K34)), hstack((K41, K42, K43, K44))))
#     return K_g2


# @jit(f8[:, :](f8[:, :], f8[:, :], f8[:, :], f8[:, :], f8[:, :], f8[:, :], f8[:], f8[:, :], f8[:, :], f8[:, :], f8[:, :], f8[:, :], f8[:, :], f8[:, :], f8[:, :],
#      f8[:, :], f8[:, :], f8[:, :], f8[:, :], f8[:, :], f8[:, :], f8[:, :], f8[:, :], f8[:, :], f8),
#      nogil=True, nopython=True)
# def _geometric_stiffmatrix(zero3_3, zero12_3, f_, B, L_2, L_3, theta, Sr0, Sr1, Sr2, Sxu, Syu, Szu, Sxv, Syv, Szv, Sx, Szuzv, Syvyu, T, R_e, xe, T_u, T_v, li):

#     xu = zeros((3, 1))
#     yu = zeros((3, 1))
#     zu = zeros((3, 1))
#     xv = zeros((3, 1))
#     yv = zeros((3, 1))
#     zv = zeros((3, 1))
#     r0 = zeros((3, 1))
#     r1 = zeros((3, 1))
#     r2 = zeros((3, 1))
#     xu[:, 0] = T_u[:, 0]
#     yu[:, 0] = T_u[:, 1]
#     zu[:, 0] = T_u[:, 2]
#     xv[:, 0] = T_v[:, 0]
#     yv[:, 0] = T_v[:, 1]
#     zv[:, 0] = T_v[:, 2]
#     r0[:, 0] = R_e[:, 0]
#     r1[:, 0] = R_e[:, 1]
#     r2[:, 0] = R_e[:, 2]
#     zuzv = (zu - zv)
#     yvyu = (yv - yu)

#     M = [f_[1][0] / (2 * cos(theta[0])), f_[2][0] / (2 * cos(theta[2])), f_[3][0] / (2 * cos(theta[4])), f_[4][0] / (2 * cos(theta[1])), f_[5][0] / (2 * cos(theta[3])), f_[6][0] / (2 * cos(theta[5]))]

#     K12 = zero3_3
#     K14 = zero3_3
#     K21 = zero3_3
#     K22 = zero3_3
#     K23 = zero3_3
#     K24 = zero3_3
#     K32 = zero3_3
#     K34 = zero3_3
#     K41 = zero3_3
#     K42 = zero3_3
#     K43 = zero3_3
#     K44 = zero3_3

#     K11 = f_[0] * B
#     K33 = K11
#     K13 = -K11
#     K31 = -K11

#     K_g1 = vstack((hstack((K11, K12, K13, K14)), hstack((K21, K22, K23, K24)), hstack((K31, K32, K33, K34)), hstack((K41, K42, K43, K44))))

#     K1 = zero12_3
#     K3 = zero12_3
#     K2 = multiply_matrices_numba(-L_2, (M[3] * Szu + M[2] * Sxu)) + multiply_matrices_numba(L_3, (M[3] * Syu - M[1] * Sxu))
#     K4 = multiply_matrices_numba(L_2, (M[3] * Szv - M[5] * Sxv)) - multiply_matrices_numba(L_3, (M[3] * Syv + M[4] * Sxv))

#     K_g3 = hstack((K1, K2, K3, K4))

#     K11 = 0 * K11
#     K13 = 0 * K13
#     K31 = 0 * K31
#     K33 = 0 * K33

#     K22 = M[3] * (multiply_matrices_numba(Sr1, Szu) - multiply_matrices_numba(Sr2, Syu)) + M[2] * (multiply_matrices_numba(-Sr0, Syu) + multiply_matrices_numba(Sr1, Sxu)) + M[1] * (multiply_matrices_numba(-Sr0, Szu) + multiply_matrices_numba(Sr2, Sxu))

#     K44 = -M[3] * (multiply_matrices_numba(Sr1, Szv) - multiply_matrices_numba(Sr2, Syv)) + M[5] * (multiply_matrices_numba(-Sr0, Syv) + multiply_matrices_numba(Sr1, Sxv)) + M[4] * (multiply_matrices_numba(-Sr0, Szv) + multiply_matrices_numba(Sr2, Sxv))

#     K_g4 = vstack((hstack((K11, K12, K13, K14)), hstack((K21, K22, K23, K24)), hstack((K31, K32, K33, K34)), hstack((K41, K42, K43, K44))))

#     K22 = 0 * K22
#     K44 = 0 * K44

#     K12 = -(M[2] * multiply_matrices_numba(B, Syu) + M[1] * multiply_matrices_numba(B, Szu))
#     K32 = -K12
#     K21 = K12.transpose()
#     K23 = -K12.transpose()

#     K14 = -(M[5] * multiply_matrices_numba(B, Syv) + M[4] * multiply_matrices_numba(B, Szv))
#     K34 = -K14
#     K41 = K14.transpose()
#     K43 = -K14.transpose()

#     k = 1 / li * (M[2] * yu + M[1] * zu + M[5] * yv + M[4] * zv)
#     K11 = multiply_matrices_numba(multiply_matrices_numba(B, k), xe.transpose()) + multiply_matrices_numba(multiply_matrices_numba(xe, k.transpose()), B) + (multiply_matrices_numba(xe.transpose(), k) * B)
#     K33 = K11
#     K13 = -K11
#     K31 = -K11

#     K_g5 = vstack((hstack((K11, K12, K13, K14)), hstack((K21, K22, K23, K24)), hstack((K31, K32, K33, K34)), hstack((K41, K42, K43, K44))))

#     Df = zeros((6, 6))
#     Df[0, 0] = f_[1][0] * tan(theta[0])
#     Df[1, 1] = f_[2][0] * tan(theta[2])
#     Df[2, 2] = f_[3][0] * tan(theta[4])
#     Df[3, 3] = f_[4][0] * tan(theta[1])
#     Df[4, 4] = f_[5][0] * tan(theta[3])
#     Df[5, 5] = f_[6][0] * tan(theta[5])
#     K_g6 = multiply_matrices_numba(multiply_matrices_numba(T[:, 1:7], Df), T[:, 1:7].transpose())

#     Sx = _skew_(Sx, xe.transpose()[0])
#     Szuzv = _skew_(Szuzv, zuzv.transpose()[0])
#     Syvyu = _skew_(Syvyu, yvyu.transpose()[0])

#     r1T_B = multiply_matrices_numba(r1.transpose(), B)
#     r2T_B = multiply_matrices_numba(r2.transpose(), B)
#     r1T_xe = multiply_matrices_numba(r1.transpose(), xe)
#     r2T_xe = multiply_matrices_numba(r2.transpose(), xe)
#     B_r1 = multiply_matrices_numba(B, r1)
#     B_r2 = multiply_matrices_numba(B, r2)
#     B_r1_xeT = multiply_matrices_numba(B_r1, xe.transpose())
#     B_r2_xeT = multiply_matrices_numba(B_r2, xe.transpose())
#     r1T_xe = multiply_matrices_numba(r1.transpose(), xe) / (2 * li)
#     r2T_xe = multiply_matrices_numba(r2.transpose(), xe) / (2 * li)
#     xeT_Sr1 = multiply_matrices_numba(xe.transpose(), Sr1)
#     xeT_Sr2 = multiply_matrices_numba(xe.transpose(), Sr2)
#     B_Sr1 = multiply_matrices_numba(B, Sr1)
#     B_Sr2 = multiply_matrices_numba(B, Sr2)
#     Sr1_xe = multiply_matrices_numba(Sr1, xe)
#     Sr2_xe = multiply_matrices_numba(Sr2, xe)
#     Sx_Sr1 = multiply_matrices_numba(Sx, Sr1)
#     Sx_Sr2 = multiply_matrices_numba(Sx, Sr2)

#     K_g21 = K_g2(r1, zuzv, B, li, xe, r0, Sr0, Sx, Sr1, Szuzv, r1T_B, r1T_xe, B_r1, B_r1_xeT, xeT_Sr1, B_Sr1, Sr1_xe, Sx_Sr1)
#     K_g22 = K_g2(r2, yvyu, B, li, xe, r0, Sr0, Sx, Sr2, Syvyu, r2T_B, r2T_xe, B_r2, B_r2_xeT, xeT_Sr2, B_Sr2, Sr2_xe, Sx_Sr2)
#     K_g23 = K_g2(r1, xu, B, li, xe, r0, Sr0, Sx, Sr1, Sxu, r1T_B, r1T_xe, B_r1, B_r1_xeT, xeT_Sr1, B_Sr1, Sr1_xe, Sx_Sr1)
#     K_g24 = K_g2(r2, xu, B, li, xe, r0, Sr0, Sx, Sr2, Sxu, r2T_B, r2T_xe, B_r2, B_r2_xeT, xeT_Sr2, B_Sr2, Sr2_xe, Sx_Sr2)
#     K_g25 = K_g2(r1, xv, B, li, xe, r0, Sr0, Sx, Sr1, Sxv, r1T_B, r1T_xe, B_r1, B_r1_xeT, xeT_Sr1, B_Sr1, Sr1_xe, Sx_Sr1)
#     K_g26 = K_g2(r2, xv, B, li, xe, r0, Sr0, Sx, Sr2, Sxv, r2T_B, r2T_xe, B_r2, B_r2_xeT, xeT_Sr2, B_Sr2, Sr2_xe, Sx_Sr2)

#     Ke_g = (K_g1 + K_g6 + M[3] * (K_g21 + K_g22) + M[2] * K_g23 + M[1] * K_g24 + M[5] * K_g25 + M[4] * K_g26 + K_g3 + K_g3.transpose() + K_g4 + K_g5)
#     return Ke_g


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    from compas.viewers import NetworkViewer

    from numpy import cos
    from numpy import pi
    from numpy import sin

    m = 80
    R = 100
    at = 0.25 * pi

    network = Network()
    for i in range(m + 1):
        a = i * at / m
        x = R * sin(a)
        y = -R + R * cos(a)
        network.add_vertex(key=i, x=x, y=y)
        if i < m:
            network.add_edge(key=i, u=i, v=i+1)
    network.add_vertex(key=(m + 1), x=0, y=-R)

    network.update_default_edge_attributes({
        'w': int,
        'E': 10.0 ** 7,
        'nu': 0.0,
        'A': 1.0,
        'Ix': 2.25 * 0.5 ** 4,
        'Iy': 1.0 / 12,
        'Iz': 1.0 / 12,
    })

    bcs = {
        'dofx': False,
        'dofy': False,
        'dofz': False,
        'dofalpha': False,
        'dofbeta': False,
        'dofgamma': False,
    }

    network.set_vertices_attributes(keys=[0, m + 1], attr_dict=bcs)
    network.set_vertices_attributes([m], {'pz': 600})
    network.set_edges_attributes(attr_dict={'w': (m + 1)})

    tic = time()
    X = dr_6dof_numba(network=network, dt=1.0, xi=1., tol=0.001, steps=50)
    print(X[-2, :])
    print(time() - tic)


# # ==============================================================================
# # Main
# # ==============================================================================

# if __name__ == "__main__":

#     from compas.viewers import NetworkViewer

#     from numpy import cos
#     from numpy import pi
#     from numpy import sin

#     m = 80
#     R = 100
#     at = 0.25 * pi

#     network = Network()
#     for i in range(m + 1):
#         a = i * at / m
#         x = R * sin(a)
#         y = -R + R * cos(a)
#         network.add_vertex(key=i, x=x, y=y)
#         if i < m:
#             network.add_edge(key=i, u=i, v=i+1)
#     network.add_vertex(key=(m + 1), x=0, y=-R)

#     network.update_default_edge_attributes({
#         'w': int,
#         'E': 10.0 ** 7,
#         'nu': 0.0,
#         'A': 1.0,
#         'Ix': 2.25 * 0.5 ** 4,
#         'Iy': 1.0 / 12,
#         'Iz': 1.0 / 12,
#     })

#     bcs = {
#         'dofx': False,
#         'dofy': False,
#         'dofz': False,
#         'dofalpha': False,
#         'dofbeta': False,
#         'dofgamma': False,
#     }

#     network.set_vertices_attributes(keys=[0, m + 1], attr_dict=bcs)
#     network.set_vertices_attributes([m], {'pz': 600})
#     network.set_edges_attributes(attr_dict={'w': (m + 1)})

#     tic = time()
#     X = dr_6dof_numba(network=network, dt=1.0, xi=1., tol=0.001, steps=100, geomstiff=False)
#     print(X[-2, :])
#     print(time() - tic)

#     for i in network.vertices():
#         x, y, z = X[i, :]
#         network.set_vertex_attributes(i, {'x': x, 'y': y, 'z': z})

#     viewer = NetworkViewer(network=network, width=1600, height=800)
#     viewer.setup()
#     viewer.show()
#     """
#     m = 20
#     span = 10

#     network = Network()
#     countm = 0
#     countn = 0
#     for i in range(m + 1):
#         for j in range(m + 1):
#             x = span / m * j - span / 2
#             y = span / m * i - span / 2
#             network.add_vertex(key=countn, x=x, y=y)
#             if j < m:
#                 network.add_edge(key=countm, u=countn, v=countn+1)
#                 countm += 1
#             if i < m:
#                 network.add_edge(key=countm, u=countn, v=countn+m+1)
#                 countm += 1
#             countn += 1

#     network.add_vertex(key=countn, x=0, z=-span ** 2)

#     network.update_default_edge_attributes({
#         'w': int,
#         'E': 30.0 * 10 ** 9,
#         'nu': 0.0,
#         'A': 7.0416 * 10 ** -4,
#         'Ix': 7.9522 * 10 ** -8,
#         'Iy': 3.9761 * 10 ** -8,
#         'Iz': 3.9761 * 10 ** -8,
#     })
#     bcs = {
#         'dofx': False,
#         'dofy': False,
#         'dofz': False,
#         'dofalpha': False,
#         'dofbeta': False,
#         'dofgamma': False,
#     }

#     network.set_vertices_attributes(keys=[countn], attr_dict=bcs)
#     network.set_vertices_attributes(keys=[0, m, m * (m+1), (m+1)*(m+1) - 1], attr_dict={'dofz': False})
#     network.set_vertices_attributes(keys=[m/2, m * (m+1) + m/2], attr_dict={'dofx': False})
#     network.set_vertices_attributes(keys=[(m / 2) * (m + 1), (m / 2 + 1) * (m + 1) - 1], attr_dict={'dofy': False})
#     network.set_vertices_attributes(attr_dict={'pz': 25})
#     network.set_edges_attributes(attr_dict={'w': countn})

#     tic = time()
#     X = dr_6dof_numba(network=network, dt=1.0, xi=1., tol=0.001, steps=100, geomstiff=False)
#     print(X[int((m / 2) * m), :])
#     print(time() - tic)

#     for i in network.vertices():
#         x, y, z = X[i, :]
#         network.set_vertex_attributes(i, {'x': x, 'y': y, 'z': z})

#     viewer = NetworkViewer(network=network, width=1600, height=800)
#     viewer.setup()
#     viewer.show()
#     """
