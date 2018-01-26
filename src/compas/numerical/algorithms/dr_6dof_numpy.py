
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.datastructures import Network

import sys

from time import time

try:
    from numpy import array
    from numpy import matrix
    from numpy import cross
    from numpy import int64
    from numpy import sin
    from numpy import cos
    from numpy import arctan
    from numpy import arcsin
    from numpy import sum
    from numpy import zeros
    from numpy import transpose
    from numpy import concatenate
    from numpy import sort
    from numpy import eye
    from numpy import trace
    from numpy import dot
    from numpy import where
    from numpy import ravel_multi_index
    from numpy import reshape
    from numpy.linalg import norm
    from numpy.linalg import solve
    from scipy.sparse import csc_matrix
    from scipy.sparse.linalg import spsolve

except ImportError:
    if 'ironpython' not in sys.version.lower():
        raise

__author__    = ['Andrew Liew <liew@arch.ethz.ch>', 'Jef Rombouts <jef.rombouts@kuleuven.be>']
__copyright__ = 'Copyright 2018, BLOCK Research Group - ETH Zurich'
__license__   = 'MIT License'
__email__     = 'liew@arch.ethz.ch'


__all__ = [
    'dr_6dof_numpy',
]


def dr_6dof_numpy(network, dt = 1.0, xi=1.0, tol=0.001, steps=100):
    """Run dynamic relaxation analysis, 6 DoF per node.

    Parameters
    ----------
    network : Network
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
        List of node coordinares.
    x : array
        List of positions and orientations of all free DoF.
    x0 : array
        List of initial positions and orientations of all free DoF.

    """
    # Setup
    # Vertices
    k_i = network.key_index()
    n = network.number_of_vertices()
    X = zeros((n, 3))
    P = zeros((n, 6))

    for key in network.vertices():
        i = k_i[key]
        vertex  = network.vertex[key]
        X[i, :] = [vertex[j] for j in 'xyz']
        P[i, 0] = vertex.get('px', 0)
        P[i, 1] = vertex.get('py', 0)
        P[i, 2] = vertex.get('pz', 0)
        P[i, 3] = vertex.get('palpha', 0)
        P[i, 4] = vertex.get('pbeta', 0)
        P[i, 5] = vertex.get('pgamma', 0)

    # Degrees of freedom
    freedof = free_dof(network)
    d = len(freedof)
    p = zeros((d, 1))
    x0 = zeros((d, 1))
    x = zeros((d, 1))
    v = zeros((d, 1))
    freedof_node = []
    freedof_axis = []
    for i in range(d):
        node = int(round(freedof[i], 0))
        axis = int(round((freedof[i] - node) * 100 - 1, 0))
        freedof_node.append(node)
        freedof_axis.append(axis)
        p[i] = P[node, axis]
        if axis < 2.5:
            x0[i] = X[node , axis]
    x = x0
    r = p

    # Edges
    uv_i = network.uv_index()
    edges = list(network.edges())
    m = len(edges)
    l0 = zeros((m, 1))
    l = zeros((m, 1))
    T_0 = zeros((m * 3,3));
    iK = []
    jK = []
    I = []
    J = []
    col = []
    row = []
    for c, uv in enumerate(edges):
        ui, vi = uv
        i = uv_i[(ui, vi)]
        edge = network.edge[ui][vi]
        wi = edge.get('w')
        l0[i] = network.edge_length(ui, vi)
        l[i] = network.edge_length(ui, vi)

        vertexu = network.vertex[ui]
        vertexv = network.vertex[vi]
        vertexw = network.vertex[wi]
        x_0 = (array([vertexv[j] for j in 'xyz']) - array([vertexu[j] for j in 'xyz']))
        x_0 = x_0 / norm(x_0)
        z_0 = cross(array([vertexu[j] for j in 'xyz']) - array([vertexw[j] for j in 'xyz']), x_0)
        z_0 = z_0 / norm(z_0)
        y_0 = cross(z_0, x_0)

        T_0[(i * 3):((i + 1) * 3), 0:3] = transpose(array([x_0, y_0, z_0]))

        Ju = array([], dtype = int)
        Jv = array([], dtype = int)
        Iu = where(array(freedof_node) == ui)[0]
        if not len(Iu) == 0:
            Ju = (array(freedof)[Iu] - ui) * 100 - 1
            Ju = array([int(round(j)) for j in Ju])

        Iv = where(array(freedof_node) == vi)[0]
        if not len(Iv) == 0:
            Jv = (array(freedof)[Iv] - vi) * 100 + 5
            Jv = array([int(round(j)) for j in Jv])

        I.append(concatenate((Iu, Iv),0))
        J.append(concatenate((Ju, Jv),0))
        for j in range(len(I[i])):
            for k in range(len(I[i])):
                row.append(I[i][j])
                col.append(I[i][k])

    # Define indexing lists for accessing certain degrees of freedom
    counttra = 0
    IDXx, counttra = indexdof(freedof, 0.01, counttra, n)
    IDXy, counttra = indexdof(freedof, 0.02, counttra, n)
    IDXz, counttra = indexdof(freedof, 0.03, counttra, n)
    IDXtra = sort(concatenate((IDXx, IDXy, IDXz)), 0)
    IDXtra = IDXtra[0:(3 * n - counttra)]
    IDXtra = array([int(round(j)) for j in IDXtra])

    countrot = 0
    IDXalpha, countrot = indexdof(freedof, 0.04, countrot, n)
    IDXbeta, countrot = indexdof(freedof, 0.05, countrot, n)
    IDXgamma, countrot = indexdof(freedof, 0.06, countrot, n)
    IDXrot = sort(concatenate((IDXalpha, IDXbeta, IDXgamma)), 0)
    IDXrot = IDXrot[0:(3 * n - countrot)]
    IDXrot = array([int(round(j)) for j in IDXrot])

    ts = 0
    rnorm = tol + 1

    # DR-loop
    while ts <= steps and rnorm > tol:
        f = zeros((d, 1))
        K = zeros((d, d))
        data = []

        x_ = concatenate((x, [[0.0]]), 0)

        for c, uv in enumerate(edges):
            ui, vi = uv
            i = uv_i[(ui, vi)]
            vertexu = network.vertex[ui]
            vertexv = network.vertex[vi]
            vertexw = network.vertex[wi]

            # update lengths
            l[i] = network.edge_length(ui, vi)

            # update beam end triads
            T_u = beam_triad(k_i, ui, x_, IDXalpha, IDXbeta, IDXgamma, T_0[(i * 3):((i + 1) * 3), 0:3])
            x_u = T_u[:, 0]
            y_u = T_u[:, 1]
            z_u = T_u[:, 2]

            T_v = beam_triad(k_i, vi, x_, IDXalpha, IDXbeta, IDXgamma, T_0[(i * 3):((i + 1) * 3), 0:3])
            x_v = T_v[:, 0]
            y_v = T_v[:, 1]
            z_v = T_v[:, 2]

            # update element triad
            R_e = element_rotmat(T_u, T_v)

            x_e = (array([vertexv[j] for j in 'xyz']) - array([vertexu[j] for j in 'xyz']))
            x_e = x_e / norm(x_e)
            y_e = R_e[:, 1] - dot(R_e[:, 1], x_e) / 2 * (x_e + R_e[:, 0])
            z_e = R_e[:, 2] - dot(R_e[:, 2], x_e) / 2 * (x_e + R_e[:, 0])

            T_e = transpose([x_e, y_e, z_e])

            # Calculate local beam deformations
            delta = l[i][0] - l0[i][0]
            theta_xu = arcsin((dot(z_e, y_u) - dot(z_u, y_e)) / 2)
            theta_xv = arcsin((dot(z_e, y_v) - dot(z_v, y_e)) / 2)
            theta_yu = arcsin((dot(z_e, x_u) - dot(z_u, x_e)) / 2)
            theta_yv = arcsin((dot(z_e, x_v) - dot(z_v, x_e)) / 2)
            theta_zu = arcsin((dot(y_e, x_u) - dot(y_u, x_e)) / 2)
            theta_zv = arcsin((dot(y_e, x_v) - dot(y_v, x_e)) / 2)

            u_ = transpose(array([[delta, theta_xu, theta_yu, theta_zu, theta_xv, theta_yv, theta_zv]]))

            # Beam properties
            edge = network.edge[ui][vi]
            E = edge.get('E', 0)
            A = edge.get('A', 0)
            nu = edge.get('nu', 0)
            G = E / (2 * (1 + nu))
            Ix = edge.get('Ix', 0)
            Iy = edge.get('Iy', 0)
            Iz = edge.get('Iz', 0)

            # Internal forces
            Sx = skew(R_e[:, 0])
            Sy = skew(R_e[:, 1])
            Sz = skew(R_e[:, 2])

            B = 1 / l[i][0] * (eye(3) - dot(transpose([x_e]), [x_e]))

            L1_2 = dot(R_e[:, 1], x_e) / 2 * B + dot(B / 2, dot(transpose([R_e[:, 1]]), [(x_e + R_e[:, 0])]))
            L2_2 = Sy / 2 - dot(dot(R_e[:, 1], x_e) / 4, Sx) - dot(Sy / 4, dot(transpose([x_e]), [x_e + R_e[:, 0]]))
            L_2 = concatenate((L1_2, L2_2, -L1_2, L2_2))

            L1_3 = dot(R_e[:, 2], x_e) / 2 * B + dot(B / 2, dot(transpose([R_e[:, 2]]), [(x_e + R_e[:, 0])]))
            L2_3 = Sz / 2 - dot(dot(R_e[:, 2], x_e) / 4, Sx) - dot(Sz / 4, dot(transpose([x_e]), [x_e + R_e[:, 0]]))
            L_3 = concatenate((L1_3, L2_3, -L1_3, L2_3))

            Szu = skew(z_u)
            Syu = skew(y_u)
            Sxu = skew(x_u)
            Szv = skew(z_v)
            Syv = skew(y_v)
            Sxv = skew(x_v)

            h_1 = concatenate((array([0.0, 0.0, 0.0]), (dot(-Szu, y_e) + dot(Syu, z_e)), array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])))
            h_2 = concatenate((dot(B, z_u), (dot(-Szu, x_e) + dot(Sxu, z_e)), -dot(B, z_u), array([0.0, 0.0, 0.0])))
            h_3 = concatenate((dot(B, y_u), (dot(-Syu, x_e) + dot(Sxu, y_e)), -dot(B, y_u), array([0.0, 0.0, 0.0])))
            h_4 = concatenate((array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]), (dot(-Szv, y_e) + dot(Syv, z_e))))
            h_5 = concatenate((dot(B, z_v), array([0.0, 0.0, 0.0]), -dot(B, z_v), (dot(-Szv, x_e) + dot(Sxv, z_e))))
            h_6 = concatenate((dot(B, y_v), array([0.0, 0.0, 0.0]), -dot(B, y_v), (dot(-Syv, x_e) + dot(Sxv, y_e))))

            t_1 = (dot(L_3, y_u) - dot(L_2, z_u) + h_1) / (2 * cos(theta_xu))
            t_2 = (dot(L_3, x_u) + h_2) / (2 * cos(theta_yu));
            t_3 = (dot(L_2, x_u) + h_3) / (2 * cos(theta_zu));
            t_4 = (dot(L_3, y_v) - dot(L_2, z_v) + h_4) / (2 * cos(theta_xv))
            t_5 = (dot(L_3, x_v) + h_5) / (2 * cos(theta_yv));
            t_6 = (dot(L_2, x_v) + h_6) / (2 * cos(theta_zv));

            g = concatenate([-x_e, array([0.0, 0.0, 0.0]), x_e, array([0.0, 0.0, 0.0])])

            T = transpose([g, t_1, t_2, t_3, t_4, t_5, t_6])

            K_ = 1 / l0[i] * array([[E * A, 0, 0, 0, 0, 0, 0],
                [0, G * Ix, 0, 0, -G * Ix, 0, 0],
                [0, 0, 4 * E * Iy, 0, 0, 2 * E * Iy, 0],
                [0, 0, 0, 4 * E * Iz, 0, 0, 2 * E * Iz],
                [0, -G * Ix, 0, 0, G * Ix, 0, 0],
                [0, 0, 2 * E * Iy, 0, 0, 4 * E * Iy, 0],
                [0, 0, 0, 2 * E * Iz, 0, 0, 4 * E * Iz]])

            f_ = dot(K_, u_)

            fe = dot(T, f_)

            f[I[i]] = f[I[i]] + fe[J[i]]

            # Stiffness matrix
            Ke_e = dot(dot(T, K_), transpose(T))

            for j in range(len(I[i])):
                for k in range(len(I[i])):
                    data.append(Ke_e[J[i][j]][J[i][k]])
                    #K[I[i][j]][I[i][k]] = K[I[i][j]][I[i][k]] + Ke_e[J[i][j]][J[i][k]]

        K = csc_matrix((data, (row, col)), shape=(d, d))

        # Update residual forces
        r = p - f
        rnorm = dot(transpose(r)[0], transpose(r)[0]) ** 0.5

        # Update velocities
        M = K
        vold = v
        v = (1 - xi * dt) / (1 + xi * dt) * vold + transpose([spsolve(M, r)]) / (1 + xi * dt) * dt

        # Update coordinates
        dx = dt * v
        xold = x

        x[IDXtra] = xold[IDXtra] + dx[IDXtra]

        Lambdaold = zeros((1, 3))
        dLambda = zeros((1, 3))
        for i in range(len(set(array(freedof_node)[IDXrot]))):
            for j in where(array(freedof_node)[IDXrot] == list(set(array(freedof_node)[IDXrot]))[i])[0]:
                Lambdaold[0][freedof_axis[IDXrot[j]] - 3] = xold[IDXrot[j]]
                dLambda[0][freedof_axis[IDXrot[j]] - 3] = dx[IDXrot[j]]
            qold, q0old = quaternion(Lambdaold)
            dq, dq0 = quaternion(dLambda)
            qnew = q0old * dq + dq0 * qold - cross(qold, dq)
            q0new = q0old[0] * dq0[0] - dot(qold[0], dq[0])

            lambdanew = 2 * arctan(norm(qnew) / q0new)
            if norm(qnew) == 0.0: Lnew = qnew
            else: Lnew = qnew / norm(qnew)
            Lambdanew = lambdanew * Lnew

            for j in where(array(freedof_node)[IDXrot] == list(set(array(freedof_node)[IDXrot]))[i])[0]:
                x[IDXrot[j]] = Lambdanew[0][freedof_axis[IDXrot[j]] - 3]

        # Update X
        for i in range(len(IDXtra)):
            X[freedof_node[IDXtra[i]]][freedof_axis[IDXtra[i]]] = x[IDXtra[i]]

        # Update network
        i_k = network.index_key()
        for i in sorted(list(network.vertices()), key=int):
            xx, yy, zz = X[i, :]
            network.set_vertex_attributes(i_k[i], {'x': xx, 'y': yy, 'z': zz})

        ts += 1
        print(ts)
    return X#, x, x0


def free_dof(network):
    """ Collect all free DoF.

    Parameters:
        network (obj): Network to be analysed.

    Returns:
        list: Degrees of Freedom that are not fixed
    """
    freedof = []
    k_i = network.key_index()
    for key in network.vertices():
        i = k_i[key]
        vertex  = network.vertex[key]
        if vertex.get('dofx', True):
            freedof.append(i+0.01)
        if notvertex.get('dofy', True):
            freedof.append(i+0.02)
        if vertex.get('dofz', True):
            freedof.append(i+0.03)
        if vertex.get('dofalpha', True):
            freedof.append(i+0.04)
        if vertex.get('dofbeta', True):
            freedof.append(i+0.05)
        if vertex.get('dofgamma', True):
            freedof.append(i+0.06)
    return freedof


def skew(v):
    """ Constructs the skew-symmetric matrix S

    Parameters:
        v: A vector

    Returns:
        array: S of v
    """
    S = array([[0.0, -v[2], v[1]],
        [v[2], 0.0, -v[0]],
        [-v[1], v[0], 0.0]])
    return S


def beam_triad(k_i, key, x_, IDXalpha, IDXbeta, IDXgamma, T_0):
    """ Construct the current nodal beam triad for vertex 'key'

    Parameters:
        k_i: key from index dictionary
        key: key of vertex
        x_: extended array of displacements
        IDXalpha: list of alpha-dof index
        IDXbeta: list of beta-dof index
        IDXgamma: list of gamma-dof index

    Returns:
        array: T matrix
    """
    alpha = x_[int(IDXalpha[k_i[key]])]
    beta = x_[int(IDXbeta[k_i[key]])]
    gamma = x_[int(IDXgamma[k_i[key]])]

    Lbda = concatenate((alpha, beta, gamma), 0)
    lbda = norm(Lbda)
    if lbda == 0:
        R = eye(3)
    else:
        lbda_ = Lbda / lbda;
        S = skew(lbda_)
        R = eye(3) + sin(lbda) * S + (1 - cos(lbda)) * dot(S, S)

    T = dot(R, T_0)
    return T


def element_rotmat(T_u, T_v):
    """ calculates the 'average nodal rotation matrix' R_e for the calculation of the element triad

    Parameters:
        T_u: beam end triad for vertex u
        T_v: beam end triad for vertex v

    Return:
        array: R_e matrix
    """
    dR = T_v * transpose(T_u)

    q_0 = (1 + trace(dR)) ** 0.5 / 2
    q_1 = (dR[2, 1] - dR[1, 2]) / (4 * q_0)
    q_2 = (dR[0, 2] - dR[2, 0]) / (4 * q_0)
    q_3 = (dR[1, 0] - dR[0, 1]) / (4 * q_0)

    q = array([q_1, q_2, q_3])

    mu = 2 * abs(arctan(norm(q) / q_0))
    if mu == 0:
        e = array([1, 1, 1])
    else:
        e = q / norm(q)

    S = array([[0.0, -e[2], e[1]],
               [e[2], 0.0, -e[0]],
               [-e[1], e[0], 0.0]])
    dRm = eye(3) + sin(mu / 2) * S + (1 - cos(mu / 2)) * dot(S, S)

    R_e = dot(dRm, T_u)
    return R_e


def indexdof(freedof, seldof, count, n):
    """ makes list of indices to access seldof degrees of freedom in freedof

    Parameters:
        freedof: list of all unconstrained degrees of freedom
        seldof (float): degrees of freedom
        count: counter for number of constrained dof of specific type (translations or rotations)
        n: number of vertices

    Return:
        array: IDX list of indices
    """
    IDX = zeros((n, 1))
    for i in range(n):
        if i + seldof in freedof:
            idx = freedof.index(i + seldof)
        else:
            idx = len(freedof)
            count += 1
        IDX[i] = idx
    return IDX, count


def quaternion(Lbda):
    """ get the quaternion formulation for a given rotation vector Lbda

    Parameters:
        Lbda: rotation vector

    Return:
        array: q
        list: q0
    """
    lbda = norm(Lbda)
    L = Lbda if lbda == 0.0 else Lbda / lbda
    q = (sin(lbda / 2) * L)
    q0 = [cos(lbda / 2)]
    return q, q0


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    from compas.viewers import NetworkViewer
    #from compas.plotters import NetworkPlotter

    R = 100
    alphatot = 3.14159265359 / 4
    m = 80

    network = Network()
    for i in range(m + 1):
        alpha = i * alphatot / m
        x = R * sin(alpha)
        y = -R + R * cos(alpha)
        network.add_vertex(key=i, x=x, y=y)
        if i < m:
            network.add_edge(key=i, u=i, v=i+1)
    network.add_vertex(key = (m + 1), x = 0, y = -R)

    network.update_default_vertex_attributes({
        'dofx': True,
        'dofy': True,
        'dofz': True,
        'dofalpha': True,
        'dofbeta': True,
        'dofgamma': True,
        'px': 0.0,
        'py': 0.0,
        'pz': 0.0,
        'palpha': 0.0,
        'pbeta': 0.0,
        'pgamma': 0.0,
        })
    network.update_default_edge_attributes({
        'w': int,
        'E': 10.0 ** 7,
        'nu': 0.0,
        'A': 1.0,
        'Ix': 2.25 * 0.5 ** 4,
        'Iy': 1.0 / 12,
        'Iz': 1.0 / 12,
        })
    network.set_vertices_attributes([0, m + 1], {'dofx': False, 'dofy': False, 'dofz': False,
        'dofalpha': False, 'dofbeta': False, 'dofgamma': False,})
    network.set_vertices_attributes([m], {'pz': 600})

    network.set_edges_attributes(attr_dict = {'w': (m + 1)})

    #viewer = NetworkViewer(network=network, width=1600, height=800)
    #viewer.setup()
    #viewer.show()

    #plotter = NetworkPlotter(network, figsize=(10, 7))

    lines = []
    for u, v in network.edges():
        lines.append({
            'start': network.vertex_coordinates(u, 'xy'),
            'end'  : network.vertex_coordinates(v, 'xy'),
            'color': '#cccccc',
            'width': 1.0})

    #plotter.draw_lines(lines)

    tic = time()
    X = dr_6dof_numpy(network, dt = 1. , xi = 1. , tol=0.001, steps=50)
    toc = time() - tic
    print(toc)
    print(X)

    for i in network.vertices():
        x, y, z = X[i, :]
        network.set_vertex_attributes(i, {'x': x, 'y': y, 'z': z})

    #plotter.draw_vertices(radius=0.005, facecolor={key: '#ff0000' for key in network.vertices_where({'is_fixed': True})})
    #plotter.draw_edges()
    #plotter.show()

    #viewer.show()
