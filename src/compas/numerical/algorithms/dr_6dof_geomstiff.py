
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.datastructures import Network

from compas.hpc import cross_vectors_numba
from compas.hpc import dot_vectors_numba
from compas.hpc import length_vector_numba
from compas.hpc import multiply_matrices_numba
from compas.hpc import multiply_matrix_vector_numba
from compas.hpc import norm_vector_numba

from time import time

import sys

try:

    from numpy import arctan
    from numpy import arcsin
    from numpy import array
    from numpy import concatenate
    from numpy import cos
    from numpy import tan
    from numpy import cross
    from numpy import eye
    from numpy import float64
    from numpy import int64
    from numpy import hstack
    from numpy import vstack
    from numpy import round
    from numpy import sin
    from numpy import sqrt
    from numpy import sort
    from numpy import trace
    from numpy import zeros
    from numpy import where
    from numpy.linalg import norm

    from numpy import diag

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


def _create_vertex_arrays(network):

    """ Initialize force, position, and velocity vectors

    Parameters
    ----------
    network : obj
        Network to analyse.

    Returns
    -------
    dictionary
        Key from index dictionary.
    matrix
        Nodal coordinates.
    integer
        Number of nodes.
    integer
        Number of free degrees of freedom.
    array
        Loads on every free degree of freedom.
    array
        Initial values for the coordinates/rotation components describing nodal positions and orientations.
    array
        Position array.
    array
        Velocity array.
    array
        Residual force array.
    list
        Indexing list with node numbers for all freedof.
    list
        Indexing list with axis numbers for all freedof.
    list
        List containing all degrees of freedom as [node].0[axis].

    """

    k_i = network.key_index()
    n = network.number_of_vertices()
    X = zeros((n, 3))
    P = zeros((n, 6))
    freedof = []
    freedof_node = []
    freedof_axis = []

    for key, vertex in network.vertex.items():
        i = k_i[key]

        X[i, :] = network.vertex_coordinates(key=key)
        for ci, Pi in enumerate(['px', 'py', 'pz', 'palpha', 'pbeta', 'pgamma']):
            P[i, ci] = vertex.get(Pi, 0)

        for ci, dof in enumerate(['dofx', 'dofy', 'dofz', 'dofalpha', 'dofbeta', 'dofgamma'], 1):
            if vertex.get(dof, True):
                freedof.append(i + 0.01 * ci)  # we should think of a better dof storage method boolean array
                freedof_node.append(i)
                freedof_axis.append(ci - 1)  # remove the 1 if changed above

    d = len(freedof)
    p  = zeros((d, 1))  # might be better to make these 2D
    x  = zeros((d, 1))
    v  = zeros((d, 1))
    x0 = zeros((d, 1))

    for ci, uv in enumerate(zip(freedof_node, freedof_axis)):
        node, axis = uv
        p[ci] = P[node, axis]
        if axis <= 2:
            x0[ci] = X[node, axis]
    x = x0 * 1
    r = p * 1

    return k_i, X, n, d, p, x0, x, v, r, freedof_node, freedof_axis, freedof  # remove some


def _create_edge_arrays(network, freedof, freedof_node):

    """ Initialize local element stiffness matrices, coordinate systems, and other edge-related arrays

    Parameters
    ----------
    network : obj
        Network to analyse.
    freedof : list
        Degreed of freedom.
    freedof_node : list
        Nodes corresponding to freedof

    Returns
    -------
    list
        All edges in the network.
    dictionary
        vertexnumbers to index dictionary.
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
        Row indices for sparse assembly of K
    list
        Column indices for sparse assembly of K
    list
        Initial data for sparse assembly of K
    list
        Edge indices
    matrix
        3D matrix of local element siffness matricess

    """

    uv_i = network.uv_index()
    edges = list(network.edges())

    m  = len(edges)
    l  = zeros((m, 1))
    l0 = zeros((m, 1))
    T_0 = zeros((m * 3, 3))
    E  = zeros(m)
    A  = zeros(m)
    G  = zeros(m)
    nu = zeros(m)
    Ix = zeros(m)
    Iy = zeros(m)
    Iz = zeros(m)
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
        l[i] = network.edge_length(ui, vi)

        vertexu = network.vertex[ui]
        vertexv = network.vertex[vi]
        vertexw = network.vertex[wi]

        x_0 = (array([vertexv[j] for j in 'xyz']) - array([vertexu[j] for j in 'xyz']))  # should make xyzs first then fetch them here
        x_0 = x_0 / norm(x_0)
        z_0 = cross(array([vertexu[j] for j in 'xyz']) - array([vertexw[j] for j in 'xyz']), x_0)  # same as above
        z_0 = z_0 / norm(z_0)
        y_0 = cross(z_0, x_0)

        T_0[(i * 3):((i + 1) * 3), 0:3] = array([x_0, y_0, z_0]).transpose()

        Ju = array([], dtype=int)
        Jv = array([], dtype=int)

        Iu = where(array(freedof_node) == ui)[0]
        if not len(Iu) == 0:
            Ju = (array(freedof)[Iu] - ui) * 100 - 1
            Ju = array([int(round(j)) for j in Ju])

        Iv = where(array(freedof_node) == vi)[0]
        if not len(Iv) == 0:
            Jv = (array(freedof)[Iv] - vi) * 100 + 5
            Jv = array([int(round(j)) for j in Jv])

        I.append(concatenate((Iu, Iv), 0))
        J.append(concatenate((Ju, Jv), 0))

        for j in range(len(I[i])):
            for k in range(len(I[i])):
                row.append(I[i][j])
                col.append(I[i][k])

        E[i] = edge.get('E', 0)
        A[i] = edge.get('A', 0)
        nu[i] = edge.get('nu', 0)
        G[i] = E[i] / (2 * (1 + nu[i]))
        Ix[i] = edge.get('Ix', 0)
        Iy[i] = edge.get('Iy', 0)
        Iz[i] = edge.get('Iz', 0)

        EA = E[i] * A[i]
        GIx = G[i] * Ix[i]
        EIy = E[i] * Iy[i]
        EIz = E[i] * Iz[i]

        Kall[:, :, i] = array([
            [EA, 0, 0, 0, 0, 0, 0],
            [0, GIx, 0, 0, -GIx, 0, 0],
            [0, 0, 4 * EIy, 0, 0, 2 * EIy, 0],
            [0, 0, 0, 4 * EIz, 0, 0, 2 * EIz],
            [0, -GIx, 0, 0, GIx, 0, 0],
            [0, 0, 2 * EIy, 0, 0, 4 * EIy, 0],
            [0, 0, 0, 2 * EIz, 0, 0, 4 * EIz]
        ])

        data = zeros(len(row))

    return edges, uv_i, l, T_0, l0, I, J, row, col, data, edgei, Kall


def _indexdof(freedof, seldof, count, n):

    """ Makes list of indices to access seldof degrees-of-freedom in freedof.

    Parameters
    ----------
    freedof : list
        All unconstrained degrees of freedom.
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

    """

    IDX = zeros(n, dtype=int64)

    for i in range(n):
        if i + seldof in freedof:
            idx = freedof.index(i + seldof)
        else:
            idx = len(freedof)
            count += 1
        IDX[i] = idx

    return IDX, count


@jit(f8[:, :](f8[:, :], f8[:]), nogil=True, nopython=True)
def _skew_(S, v):

    """ Modifies the skew-symmetric matrix S in place.

    Parameters
    ----------
    S : array
        Original array to edit.
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
def _beam_triad(i, x_, IDXalpha, IDXbeta, IDXgamma, T_0, Sbt):

    """ Construct the current nodal beam triad for vertex 'key'.

    Parameters
    ----------
    i : int
        Index.
    x_ : array
        Extended array of displacements.
    IDXalpha : list
        Alpha-dof index.
    IDXbeta : list
        Beta-dof index.
    IDXgamma : list
        Gamma-dof index.
    T_0 : array
        -
    Sbt : array
        Pre-made S.

    Returns
    -------
    array
        T matrix

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
        R = eye(3) + sin(lbda) * S + (1. - cos(lbda)) * multiply_matrices_numba(S, S)

    T = multiply_matrices_numba(R, T_0)

    return T


@jit(f8[:](f8[:], f8[:], f8[:], f8[:], f8[:], f8[:], f8[:], f8[:], f8[:]),
     nogil=True, nopython=True)
def _deformations(x_e, y_e, z_e, x_u, y_u, z_u, x_v, y_v, z_v):

    """ Calculate local element deformations.

    Parameters
    ----------
    x_e : array
        Eedge x-direction.
    y_e : array
        Eedge y-direction.
    z_e : array
        Edge z-direction.
    x_u : array
        Vertex u x-direction.
    y_u : array
        Vertex u y-direction.
    z_u : array
        Vertex u z-direction.
    x_v : array
        Vertex v x-direction.
    y_v : array
        Vertex v y-direction.
    z_v : array
        Vertex v z-direction.

    Returns
    -------
    array
        T matrix
    """

    theta_xu = arcsin((dot_vectors_numba(z_e, y_u) - dot_vectors_numba(z_u, y_e)) / 2)
    theta_xv = arcsin((dot_vectors_numba(z_e, y_v) - dot_vectors_numba(z_v, y_e)) / 2)
    theta_yu = arcsin((dot_vectors_numba(z_e, x_u) - dot_vectors_numba(z_u, x_e)) / 2)
    theta_yv = arcsin((dot_vectors_numba(z_e, x_v) - dot_vectors_numba(z_v, x_e)) / 2)
    theta_zu = arcsin((dot_vectors_numba(y_e, x_u) - dot_vectors_numba(y_u, x_e)) / 2)
    theta_zv = arcsin((dot_vectors_numba(y_e, x_v) - dot_vectors_numba(y_v, x_e)) / 2)

    return array([theta_xu, theta_xv, theta_yu, theta_yv, theta_zu, theta_zv])


@jit(Tuple((f8[:, :], f8[:, :], f8[:, :], f8[:, :]))(f8[:, :], f8[:], f8[:], f8[:], f8[:], f8[:], f8[:], f8[:, :], f8[:, :], f8[:, :], f8[:, :], f8[:, :], f8[:, :], f8[:, :], f8[:, :],
     f8[:, :], f8[:, :], f8[:], f8[:], f8[:], f8[:], f8[:], f8[:], f8[:], f8[:]), nogil=True, nopython=True)
def _create_T(eye3, zero3, zero6, zero9, x_e, y_e, z_e, R_e, Sr0, Sr1, Sr2, Sxu, Syu, Szu, Sxv, Syv, Szv, theta, x_u, y_u, z_u, x_v, y_v, z_v, li):

    """

    Add comments

    """

    Sr0 = _skew_(Sr0, R_e[:, 0])
    Sr1 = _skew_(Sr1, R_e[:, 1])
    Sr2 = _skew_(Sr2, R_e[:, 2])
    Szu = _skew_(Szu, z_u)
    Syu = _skew_(Syu, y_u)
    Sxu = _skew_(Sxu, x_u)
    Szv = _skew_(Szv, z_v)
    Syv = _skew_(Syv, y_v)
    Sxv = _skew_(Sxv, x_v)

    x_e_t = zeros((3, 1))
    x_e_t[0, 0] = x_e[0]
    x_e_t[1, 0] = x_e[1]
    x_e_t[2, 0] = x_e[2]

    x_e_h = x_e_t.transpose()

    R_e1_t = zeros((3, 1))
    R_e1_t[0, 0] = R_e[0, 1]
    R_e1_t[1, 0] = R_e[1, 1]
    R_e1_t[2, 0] = R_e[2, 1]

    xe_Re0 = zeros((1, 3))
    xe_Re0[0, 0] = x_e[0] + R_e[0, 0]
    xe_Re0[0, 1] = x_e[1] + R_e[1, 0]
    xe_Re0[0, 2] = x_e[2] + R_e[2, 0]

    R_e2_t = zeros((3, 1))
    R_e2_t[0, 0] = R_e[0, 2]
    R_e2_t[1, 0] = R_e[1, 2]
    R_e2_t[2, 0] = R_e[2, 2]

    B = 1. / li[0] * (eye3 - multiply_matrices_numba(x_e_t, x_e_h))
    XX = multiply_matrices_numba(x_e_t, xe_Re0)

    L1_2 = 0.5 * dot_vectors_numba(R_e[:, 1], x_e) * B + multiply_matrices_numba(0.5 * B, multiply_matrices_numba(R_e1_t, xe_Re0))
    L1_3 = 0.5 * dot_vectors_numba(R_e[:, 2], x_e) * B + multiply_matrices_numba(0.5 * B, multiply_matrices_numba(R_e2_t, xe_Re0))
    L2_2 = 0.5 * Sr1 - 0.25 * dot_vectors_numba(R_e[:, 1], x_e) * Sr0 - multiply_matrices_numba(0.25 * Sr1, XX)
    L2_3 = 0.5 * Sr2 - 0.25 * dot_vectors_numba(R_e[:, 2], x_e) * Sr0 - multiply_matrices_numba(0.25 * Sr2, XX)

    L_2 = vstack((L1_2, L2_2, -L1_2, L2_2))
    L_3 = vstack((L1_3, L2_3, -L1_3, L2_3))

    Bzu = multiply_matrix_vector_numba(B, z_u)
    Byu = multiply_matrix_vector_numba(B, y_u)
    Bzv = multiply_matrix_vector_numba(B, z_v)
    Byv = multiply_matrix_vector_numba(B, y_v)

    h_1 = hstack((zero3, (multiply_matrix_vector_numba(-Szu, y_e) + multiply_matrix_vector_numba(Syu, z_e)), zero6))
    h_2 = hstack((Bzu, (multiply_matrix_vector_numba(-Szu, x_e) + multiply_matrix_vector_numba(Sxu, z_e)), -Bzu, zero3))
    h_3 = hstack((Byu, (multiply_matrix_vector_numba(-Syu, x_e) + multiply_matrix_vector_numba(Sxu, y_e)), -Byu, zero3))
    h_4 = hstack((zero9, (multiply_matrix_vector_numba(-Szv, y_e) + multiply_matrix_vector_numba(Syv, z_e))))
    h_5 = hstack((Bzv, zero3, -Bzv, (multiply_matrix_vector_numba(-Szv, x_e) + multiply_matrix_vector_numba(Sxv, z_e))))
    h_6 = hstack((Byv, zero3, -Byv, (multiply_matrix_vector_numba(-Syv, x_e) + multiply_matrix_vector_numba(Sxv, y_e))))

    t_1 = (multiply_matrix_vector_numba(L_3, y_u) - multiply_matrix_vector_numba(L_2, z_u) + h_1) / (2 * cos(theta[0]))
    t_2 = (multiply_matrix_vector_numba(L_3, x_u) + h_2) / (2 * cos(theta[2]))
    t_3 = (multiply_matrix_vector_numba(L_2, x_u) + h_3) / (2 * cos(theta[4]))
    t_4 = (multiply_matrix_vector_numba(L_3, y_v) - multiply_matrix_vector_numba(L_2, z_v) + h_4) / (2 * cos(theta[1]))
    t_5 = (multiply_matrix_vector_numba(L_3, x_v) + h_5) / (2 * cos(theta[3]))
    t_6 = (multiply_matrix_vector_numba(L_2, x_v) + h_6) / (2 * cos(theta[5]))

    g = hstack((-x_e, zero3, x_e, zero3))

    T = zeros((12, 7))
    T[:, 0] = g
    T[:, 1] = t_1
    T[:, 2] = t_2
    T[:, 3] = t_3
    T[:, 4] = t_4
    T[:, 5] = t_5
    T[:, 6] = t_6

    return T, B, L_2, L_3


@jit(f8[:, :](f8[:, :], f8[:, :]), nogil=True, nopython=True)
def _element_rotmat(T_u, T_v):

    """ Calculates the 'average nodal rotation matrix' R_e for the calculation of the element triad.

    Parameters
    ----------
    T_u : array
        Beam end triad for vertex u.
    T_v : array
        Beam end triad for vertex v.

    Returns
    -------
    array
        R_e matrix.

    """

    dR = multiply_matrices_numba(T_v, T_u.transpose())

    q_0 = 0.5 * sqrt(1. + trace(dR))
    q04 = 4. * q_0
    q_1 = (dR[2, 1] - dR[1, 2]) / q04
    q_2 = (dR[0, 2] - dR[2, 0]) / q04
    q_3 = (dR[1, 0] - dR[0, 1]) / q04
    q = array([q_1, q_2, q_3])
    normq = norm_vector_numba(q)

    mu = 2. * abs(arctan(normq / q_0))
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

    dRm = eye(3) + sin(0.5 * mu) * S + (1. - cos(0.5 * mu)) * multiply_matrices_numba(S, S)
    R_e = multiply_matrices_numba(dRm, T_u)

    return R_e


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


@jit(Tuple((f8[:], i8))(f8[:, :], i8[:], i8[:], f8[:], i8),
     nogil=True, nopython=True)
def _data(Ke, Ii, Ji, data, count):

    """

    Add comments

    """
    for j in range(len(Ii)):
        for k in range(len(Ii)):
            data[count] = (Ke[Ji[j]][Ji[k]])
            count += 1
    return data, count


@jit(Tuple((f8[:, :], f8[:, :]))(f8, f8, f8[:], f8[:, :, :], f8[:, :], f8[:, :], i8[:], i8[:], i8),
     nogil=True, nopython=True)
def _element_forces(li, l0i, theta, Kall, T, f, Ii, Ji, i):

    """

    Add comments

    """
    delta = li - l0i
    u_ = zeros((7, 1))
    u_[0, 0] = delta
    u_[1, 0] = theta[0]
    u_[2, 0] = theta[2]
    u_[3, 0] = theta[4]
    u_[4, 0] = theta[1]
    u_[5, 0] = theta[3]
    u_[6, 0] = theta[5]

    K_ = 1. / l0i * Kall[:, :, i]
    f_ = multiply_matrices_numba(K_, u_)
    fe = multiply_matrices_numba(T, f_)
    f[Ii] += fe[Ji]

    return f, f_


@jit(f8[:, :](f8, f8[:, :, :], f8[:, :], i8),
     nogil=True, nopython=True)
def _elastic_stiffmatrix(l0i, Kall, T, i):

    """ Calculate element elastic stiffness matrix

    Parameters
    ----------
        l0i: float
            Initial edge length.
        Kall: matrix
            3D Matrix of element local stiffness matrices.
        T: matrix
            Transformation matrix.
        i: integer
            Edge index.

    Returns
    -------
        matrix 
            Element elastic stiffness matrix.

    """
    K_ = 1. / l0i * Kall[:, :, i]
    Ke_e = multiply_matrices_numba(multiply_matrices_numba(T, K_), T.transpose())

    return Ke_e


@jit(f8[:, :](f8[:, :], f8[:, :], f8[:, :], f8, f8[:, :], f8[:, :], f8[:, :], f8[:, :], f8[:, :], f8[:, :], f8[:, :], f8[:, :], f8[:, :], f8[:, :], f8[:, :], f8[:, :], f8[:, :], f8[:, :]),
     nogil=True, nopython=True)
def K_g2(r_i, o, B, l, x, r_0, Sr0, Sx, Sri, So, riT_B, riT_xe, B_ri, B_ri_xeT, xeT_Sri, B_Sri, Sri_xe, Sx_Sri):
    """ Calculate K_g2 for the geometric stiffness matrix

    Parameters
    ----------
        ri:
            y- or z- Direction of the element rotation vector R_e.
        o:
            Vector.
        B:
            Matrix B.
        l:
            Length of the element.
        x:
            Vector in element x-direction.
        r_0:
            x-Direction of the element rotation vector R_e.

    Returns
    -------
        matrix 
            K_g2.

    """
    B_o = multiply_matrices_numba(B, o)
    oT_xr0 = multiply_matrices_numba(o.transpose(), (x + r_0))
    U = -1 / 2 * multiply_matrices_numba(B_o, riT_B) + (riT_xe / (2 * l)) * multiply_matrices_numba(B_o, x.transpose()) + (oT_xr0 / (2 * l)) * B_ri_xeT

    K11 = U + U.transpose() + riT_xe * (2 * multiply_matrices_numba(x.transpose(), o) + multiply_matrices_numba(o.transpose(), r_0)) * B
    K33 = K11
    K13 = -K11
    K31 = -K11

    K12 = (multiply_matrices_numba(-B_o, xeT_Sri) - multiply_matrices_numba(B_ri, multiply_matrices_numba(o.transpose(), Sr0)) - oT_xr0 * B_Sri) / 4
    K14 = K12
    K32 = -K12
    K34 = -K12
    K21 = K12.transpose()
    K41 = K12.transpose()
    K23 = -K12.transpose()
    K43 = -K12.transpose()

    K22 = ((-riT_xe * multiply_matrices_numba(So, Sr0) + multiply_matrices_numba(multiply_matrices_numba(Sr0, o), xeT_Sri) +
            multiply_matrices_numba(Sri_xe, multiply_matrices_numba(o.transpose(), Sr0)) - multiply_matrices_numba(x.transpose() +
            r_0.transpose(), o) * Sx_Sri + 2 * multiply_matrices_numba(So, Sri)) / 8)
    K24 = K22
    K42 = K22
    K44 = K22

    K_g2 = vstack((hstack((K11, K12, K13, K14)), hstack((K21, K22, K23, K24)), hstack((K31, K32, K33, K34)), hstack((K41, K42, K43, K44))))
    return K_g2


@jit(f8[:, :](f8[:, :], f8[:, :], f8[:, :], f8[:, :], f8[:, :], f8[:, :], f8[:], f8[:, :], f8[:, :], f8[:, :], f8[:, :], f8[:, :], f8[:, :], f8[:, :], f8[:, :], 
     f8[:, :], f8[:, :], f8[:, :], f8[:, :], f8[:, :], f8[:, :], f8[:, :], f8[:, :], f8[:, :], f8),
     nogil=True, nopython=True)
def _geometric_stiffmatrix(zero3_3, zero12_3, f_, B, L_2, L_3, theta, Sr0, Sr1, Sr2, Sxu, Syu, Szu, Sxv, Syv, Szv, Sx, Szuzv, Syvyu, T, R_e, xe, T_u, T_v, li):

    xu = zeros((3, 1))
    yu = zeros((3, 1))
    zu = zeros((3, 1))
    xv = zeros((3, 1))
    yv = zeros((3, 1))
    zv = zeros((3, 1))
    r0 = zeros((3, 1))
    r1 = zeros((3, 1))
    r2 = zeros((3, 1))
    xu[:, 0] = T_u[:, 0]
    yu[:, 0] = T_u[:, 1]
    zu[:, 0] = T_u[:, 2]
    xv[:, 0] = T_v[:, 0]
    yv[:, 0] = T_v[:, 1]
    zv[:, 0] = T_v[:, 2]
    r0[:, 0] = R_e[:, 0]
    r1[:, 0] = R_e[:, 1]
    r2[:, 0] = R_e[:, 2]
    zuzv = (zu - zv)
    yvyu = (yv - yu)

    M = [f_[1][0] / (2 * cos(theta[0])), f_[2][0] / (2 * cos(theta[2])), f_[3][0] / (2 * cos(theta[4])), f_[4][0] / (2 * cos(theta[1])), f_[5][0] / (2 * cos(theta[3])), f_[6][0] / (2 * cos(theta[5]))]

    K12 = zero3_3
    K14 = zero3_3
    K21 = zero3_3
    K22 = zero3_3
    K23 = zero3_3
    K24 = zero3_3
    K32 = zero3_3
    K34 = zero3_3
    K41 = zero3_3
    K42 = zero3_3
    K43 = zero3_3
    K44 = zero3_3

    K11 = f_[0] * B
    K33 = K11
    K13 = -K11
    K31 = -K11

    K_g1 = vstack((hstack((K11, K12, K13, K14)), hstack((K21, K22, K23, K24)), hstack((K31, K32, K33, K34)), hstack((K41, K42, K43, K44))))

    K1 = zero12_3
    K3 = zero12_3
    K2 = multiply_matrices_numba(-L_2, (M[3] * Szu + M[2] * Sxu)) + multiply_matrices_numba(L_3, (M[3] * Syu - M[1] * Sxu))
    K4 = multiply_matrices_numba(L_2, (M[3] * Szv - M[5] * Sxv)) - multiply_matrices_numba(L_3, (M[3] * Syv + M[4] * Sxv))

    K_g3 = hstack((K1, K2, K3, K4))

    K11 = 0 * K11
    K13 = 0 * K13
    K31 = 0 * K31
    K33 = 0 * K33

    K22 = M[3] * (multiply_matrices_numba(Sr1, Szu) - multiply_matrices_numba(Sr2, Syu)) + M[2] * (multiply_matrices_numba(-Sr0, Syu) + multiply_matrices_numba(Sr1, Sxu)) + M[1] * (multiply_matrices_numba(-Sr0, Szu) + multiply_matrices_numba(Sr2, Sxu))

    K44 = -M[3] * (multiply_matrices_numba(Sr1, Szv) - multiply_matrices_numba(Sr2, Syv)) + M[5] * (multiply_matrices_numba(-Sr0, Syv) + multiply_matrices_numba(Sr1, Sxv)) + M[4] * (multiply_matrices_numba(-Sr0, Szv) + multiply_matrices_numba(Sr2, Sxv))

    K_g4 = vstack((hstack((K11, K12, K13, K14)), hstack((K21, K22, K23, K24)), hstack((K31, K32, K33, K34)), hstack((K41, K42, K43, K44))))

    K22 = 0 * K22
    K44 = 0 * K44

    K12 = -(M[2] * multiply_matrices_numba(B, Syu) + M[1] * multiply_matrices_numba(B, Szu))
    K32 = -K12
    K21 = K12.transpose()
    K23 = -K12.transpose()

    K14 = -(M[5] * multiply_matrices_numba(B, Syv) + M[4] * multiply_matrices_numba(B, Szv))
    K34 = -K14
    K41 = K14.transpose()
    K43 = -K14.transpose()

    k = 1 / li * (M[2] * yu + M[1] * zu + M[5] * yv + M[4] * zv)
    K11 = multiply_matrices_numba(multiply_matrices_numba(B, k), xe.transpose()) + multiply_matrices_numba(multiply_matrices_numba(xe, k.transpose()), B) + (multiply_matrices_numba(xe.transpose(), k) * B)
    K33 = K11
    K13 = -K11
    K31 = -K11

    K_g5 = vstack((hstack((K11, K12, K13, K14)), hstack((K21, K22, K23, K24)), hstack((K31, K32, K33, K34)), hstack((K41, K42, K43, K44))))

    Df = zeros((6, 6))
    Df[0, 0] = f_[1][0] * tan(theta[0])
    Df[1, 1] = f_[2][0] * tan(theta[2])
    Df[2, 2] = f_[3][0] * tan(theta[4])
    Df[3, 3] = f_[4][0] * tan(theta[1])
    Df[4, 4] = f_[5][0] * tan(theta[3])
    Df[5, 5] = f_[6][0] * tan(theta[5])
    K_g6 = multiply_matrices_numba(multiply_matrices_numba(T[:, 1:7], Df), T[:, 1:7].transpose())

    Sx = _skew_(Sx, xe.transpose()[0])
    Szuzv = _skew_(Szuzv, zuzv.transpose()[0])
    Syvyu = _skew_(Syvyu, yvyu.transpose()[0])

    r1T_B = multiply_matrices_numba(r1.transpose(), B)
    r2T_B = multiply_matrices_numba(r2.transpose(), B)
    r1T_xe = multiply_matrices_numba(r1.transpose(), xe)
    r2T_xe = multiply_matrices_numba(r2.transpose(), xe)
    B_r1 = multiply_matrices_numba(B, r1)
    B_r2 = multiply_matrices_numba(B, r2)
    B_r1_xeT = multiply_matrices_numba(B_r1, xe.transpose())
    B_r2_xeT = multiply_matrices_numba(B_r2, xe.transpose())
    r1T_xe = multiply_matrices_numba(r1.transpose(), xe) / (2 * li)
    r2T_xe = multiply_matrices_numba(r2.transpose(), xe) / (2 * li)
    xeT_Sr1 = multiply_matrices_numba(xe.transpose(), Sr1)
    xeT_Sr2 = multiply_matrices_numba(xe.transpose(), Sr2)
    B_Sr1 = multiply_matrices_numba(B, Sr1)
    B_Sr2 = multiply_matrices_numba(B, Sr2)
    Sr1_xe = multiply_matrices_numba(Sr1, xe)
    Sr2_xe = multiply_matrices_numba(Sr2, xe)
    Sx_Sr1 = multiply_matrices_numba(Sx, Sr1)
    Sx_Sr2 = multiply_matrices_numba(Sx, Sr2)

    K_g21 = K_g2(r1, zuzv, B, li, xe, r0, Sr0, Sx, Sr1, Szuzv, r1T_B, r1T_xe, B_r1, B_r1_xeT, xeT_Sr1, B_Sr1, Sr1_xe, Sx_Sr1)
    K_g22 = K_g2(r2, yvyu, B, li, xe, r0, Sr0, Sx, Sr2, Syvyu, r2T_B, r2T_xe, B_r2, B_r2_xeT, xeT_Sr2, B_Sr2, Sr2_xe, Sx_Sr2)
    K_g23 = K_g2(r1, xu, B, li, xe, r0, Sr0, Sx, Sr1, Sxu, r1T_B, r1T_xe, B_r1, B_r1_xeT, xeT_Sr1, B_Sr1, Sr1_xe, Sx_Sr1)
    K_g24 = K_g2(r2, xu, B, li, xe, r0, Sr0, Sx, Sr2, Sxu, r2T_B, r2T_xe, B_r2, B_r2_xeT, xeT_Sr2, B_Sr2, Sr2_xe, Sx_Sr2)
    K_g25 = K_g2(r1, xv, B, li, xe, r0, Sr0, Sx, Sr1, Sxv, r1T_B, r1T_xe, B_r1, B_r1_xeT, xeT_Sr1, B_Sr1, Sr1_xe, Sx_Sr1)
    K_g26 = K_g2(r2, xv, B, li, xe, r0, Sr0, Sx, Sr2, Sxv, r2T_B, r2T_xe, B_r2, B_r2_xeT, xeT_Sr2, B_Sr2, Sr2_xe, Sx_Sr2)

    Ke_g = (K_g1 + K_g6 + M[3] * (K_g21 + K_g22) + M[2] * K_g23 + M[1] * K_g24 + M[5] * K_g25 + M[4] * K_g26 + K_g3 + K_g3.transpose() + K_g4 + K_g5)
    return Ke_g


@jit(f8[:, :](f8[:, :], f8[:, :], f8, i8[:], f8[:], f8[:], i8[:], i8[:], i8[:], i8[:], i8[:], i8[:, :]),
     nogil=True, nopython=True)
def _update(x, v, dt, IDXtra, Lambdaold, dLambda, freedof_node_array, freedof_axis_array, IDXrot, FNA, setFNA, ind):

    dx = dt * v
    xold = x
    x[IDXtra] = xold[IDXtra] + dx[IDXtra]

    Lambdaold *= 0.
    dLambda *= 0.

    for i in range(len(setFNA)):

        for jj in range(3):  # is this always len 3?
            j = ind[i, jj]
            index = freedof_axis_array[IDXrot[j]]
            Lambdaold[index - 3] = xold[IDXrot[j]][0]
            dLambda[index - 3] = dx[IDXrot[j]][0]

        qO = _quaternion(Lambdaold)
        qQ = _quaternion(dLambda)
        qold = qO[:3]
        q0old = qO[3]
        dq = qQ[:3]
        dq0 = qQ[3]

        qnew = q0old * dq + dq0 * qold - cross_vectors_numba(qold, dq)
        q0new = q0old * dq0 - dot_vectors_numba(qold, dq)
        lambdanew = 2 * arctan(norm_vector_numba(qnew) / q0new)

        if norm(qnew) == 0.0:
            Lnew = qnew
        else:
            Lnew = qnew / norm_vector_numba(qnew)
        Lambdanew = lambdanew * Lnew

        value = setFNA[i]
        for j in range(len(FNA)):
            if FNA[j] == value:
                x[IDXrot[j]] = Lambdanew[freedof_axis_array[IDXrot[j]] - 3]

    return x


def dr_6dof_numba(network, dt=1.0, xi=1.0, tol=0.001, steps=100, geomstiff=False):

    """Run dynamic relaxation analysis with 6 DoF per node.

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

    Returns
    -------
    X : array
        Node co-ordinates.
    x : array
        Positions and orientations of all free DoF.
    x0 : array
        Initial positions and orientations of all free DoF.

    """
    toc1 = 0
    toc2 = 0

    k_i, X, n, d, p, x0, x, v, r, freedof_node, freedof_axis, freedof = _create_vertex_arrays(network)

    edges, uv_i, l, T_0, l0, I, J, row, col, data, edgei, Kall = _create_edge_arrays(network, freedof, freedof_node)

    # Indexing

    counttra = 0
    IDXx, counttra = _indexdof(freedof, 0.01, counttra, n)
    IDXy, counttra = _indexdof(freedof, 0.02, counttra, n)
    IDXz, counttra = _indexdof(freedof, 0.03, counttra, n)
    IDXtra = sort(concatenate((IDXx, IDXy, IDXz)), 0)
    nct = 3 * n - counttra
    IDXtra = IDXtra[0:nct]
    IDXtra = array([int(round(j)) for j in IDXtra])

    countrot = 0
    IDXalpha, countrot = _indexdof(freedof, 0.04, countrot, n)
    IDXbeta, countrot = _indexdof(freedof, 0.05, countrot, n)
    IDXgamma, countrot = _indexdof(freedof, 0.06, countrot, n)
    IDXrot = sort(concatenate((IDXalpha, IDXbeta, IDXgamma)), 0)
    nct = 3 * n - countrot
    IDXrot = IDXrot[0:nct]
    IDXrot = array([int(round(j)) for j in IDXrot])

    # DR-loop

    ts = 0
    rnorm = tol + 1

    f = zeros((d, 1))
    Szu = zeros((3, 3))
    Syu = zeros((3, 3))
    Sxu = zeros((3, 3))
    Szv = zeros((3, 3))
    Syv = zeros((3, 3))
    Sxv = zeros((3, 3))
    Sr2 = zeros((3, 3))
    Sr1 = zeros((3, 3))
    Sr0 = zeros((3, 3))
    Sbt = zeros((3, 3))
    Sx = zeros((3, 3))
    Szuzv = zeros((3, 3))
    Syvyu = zeros((3, 3))

    eye3 = eye(3)
    zero3 = zeros(3)
    zero6 = zeros(6)
    zero9 = zeros(9)
    zero3_3 = zeros((3, 3))
    zero12_3 = zeros((12, 3))
    Lambdaold = zeros(3, dtype=float64)
    dLambda = zeros(3, dtype=float64)

    freedof_node_array = array(freedof_node)
    freedof_axis_array = array(freedof_axis)
    FNA = freedof_node_array[IDXrot]
    setFNA = array(list(set(FNA)))

    ind = zeros((len(setFNA), 3), dtype=int)
    for i, value in enumerate(setFNA):
        ind[i, :] = where(FNA == value)[0]

#    K = zeros((d, d))  # isnt currently used, is overwritten later

    while ts <= steps and rnorm > tol:

        f *= 0
        count = 0
        x_ = concatenate((x, [[0.0]]), 0)
        tic1 = time()
        for c, uv in enumerate(edges):

            i = edgei[c]
            ui, vi = uv

            # Update lengths

            vertexu = k_i[ui]
            vertexv = k_i[vi]
            x_e = (X[vertexv, :] - X[vertexu, :])
            l[i] = length_vector_numba(x_e)

            # Update triads

            t0t = T_0[(i * 3):((i + 1) * 3), 0:3]
            T_u = _beam_triad(ui, x_, IDXalpha, IDXbeta, IDXgamma, t0t, Sbt)
            T_v = _beam_triad(vi, x_, IDXalpha, IDXbeta, IDXgamma, t0t, Sbt)
            R_e = _element_rotmat(T_u, T_v)

            x_u = T_u[:, 0]
            y_u = T_u[:, 1]
            z_u = T_u[:, 2]
            x_v = T_v[:, 0]
            y_v = T_v[:, 1]
            z_v = T_v[:, 2]

            x_e /= norm(x_e)
            y_e = R_e[:, 1] - dot_vectors_numba(R_e[:, 1], x_e) / 2 * (x_e + R_e[:, 0])
            z_e = R_e[:, 2] - dot_vectors_numba(R_e[:, 2], x_e) / 2 * (x_e + R_e[:, 0])

            # Calculate local beam deformations

            theta = _deformations(x_e, y_e, z_e, x_u, y_u, z_u, x_v, y_v, z_v)

            # Internal forces

            T, B, L_2, L_3 = _create_T(eye3, zero3, zero6, zero9, x_e, y_e, z_e, R_e, Sr0, Sr1, Sr2, Sxu, Syu, Szu, Sxv, Syv, Szv, theta, x_u, y_u, z_u, x_v, y_v, z_v, l[i])

            f, f_ = _element_forces(l[i][0], l0[i][0], theta, Kall, T, f, I[i], J[i], i)
            Ke_e = _elastic_stiffmatrix(l0[i][0], Kall, T, i)

            if geomstiff:
                Ke_g = _geometric_stiffmatrix(zero3_3, zero12_3, f_, B, L_2, L_3, theta, Sr0, Sr1, Sr2, Sxu, Syu, Szu, Sxv, Syv, Szv, Sx, Szuzv, Syvyu, T, R_e, array([x_e]).transpose(), T_u, T_v, l[i][0])
                Ke = Ke_e + Ke_g
            else: Ke = Ke_e

            data, count = _data(Ke, I[i], J[i], data, count)
        toc1 = toc1 + time()-tic1
        tic2 = time()
        K = csc_matrix((data, (row, col)), shape=(d, d))  # could dis-assemble and use own Sparse indexing in Numba

        # Update residual forces

        r = p - f
        rnorm = multiply_matrices_numba(r.transpose(), r)**0.5

        # Update velocities
        M = 1 * K
        vold = 1 * v
        v = (1 - xi * dt) / (1 + xi * dt) * vold + array([spsolve(M, r)]).transpose() / (1 + xi * dt) * dt
        toc2 = toc2 + time()-tic2
        x = _update(x, v, dt, IDXtra, Lambdaold, dLambda, freedof_node_array, freedof_axis_array, IDXrot, FNA, setFNA, ind)

        for i in range(len(IDXtra)):
            X[freedof_node[IDXtra[i]]][freedof_axis[IDXtra[i]]] = x[IDXtra[i]][0]

        ts += 1
    print(toc1, toc2)
    # Update network

    i_k = network.index_key()
    for i in sorted(list(network.vertices()), key=int):
        xx, yy, zz = X[i, :]
        network.set_vertex_attributes(i_k[i], {'x': xx, 'y': yy, 'z': zz})

    return X#, x, x0


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
    X = dr_6dof_numba(network=network, dt=1.0, xi=1., tol=0.001, steps=100, geomstiff=False)
    print(X[-2, :])
    print(time() - tic)

    for i in network.vertices():
        x, y, z = X[i, :]
        network.set_vertex_attributes(i, {'x': x, 'y': y, 'z': z})

    viewer = NetworkViewer(network=network, width=1600, height=800)
    viewer.setup()
    viewer.show()
    """
    m = 20
    span = 10

    network = Network()
    countm = 0
    countn = 0
    for i in range(m + 1):
        for j in range(m + 1):
            x = span / m * j - span / 2
            y = span / m * i - span / 2
            network.add_vertex(key=countn, x=x, y=y)
            if j < m:
                network.add_edge(key=countm, u=countn, v=countn+1)
                countm += 1
            if i < m:
                network.add_edge(key=countm, u=countn, v=countn+m+1)
                countm += 1
            countn += 1

    network.add_vertex(key=countn, x=0, z=-span ** 2)

    network.update_default_edge_attributes({
        'w': int,
        'E': 30.0 * 10 ** 9,
        'nu': 0.0,
        'A': 7.0416 * 10 ** -4,
        'Ix': 7.9522 * 10 ** -8,
        'Iy': 3.9761 * 10 ** -8,
        'Iz': 3.9761 * 10 ** -8,
    })
    bcs = {
        'dofx': False,
        'dofy': False,
        'dofz': False,
        'dofalpha': False,
        'dofbeta': False,
        'dofgamma': False,
    }

    network.set_vertices_attributes(keys=[countn], attr_dict=bcs)
    network.set_vertices_attributes(keys=[0, m, m * (m+1), (m+1)*(m+1) - 1], attr_dict={'dofz': False})
    network.set_vertices_attributes(keys=[m/2, m * (m+1) + m/2], attr_dict={'dofx': False})
    network.set_vertices_attributes(keys=[(m / 2) * (m + 1), (m / 2 + 1) * (m + 1) - 1], attr_dict={'dofy': False})
    network.set_vertices_attributes(attr_dict={'pz': 25})
    network.set_edges_attributes(attr_dict={'w': countn})

    tic = time()
    X = dr_6dof_numba(network=network, dt=1.0, xi=1., tol=0.001, steps=100, geomstiff=False)
    print(X[int((m / 2) * m), :])
    print(time() - tic)

    for i in network.vertices():
        x, y, z = X[i, :]
        network.set_vertex_attributes(i, {'x': x, 'y': y, 'z': z})

    viewer = NetworkViewer(network=network, width=1600, height=800)
    viewer.setup()
    viewer.show()
    """