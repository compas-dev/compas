
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.datastructures import Network

import sys

from time import time

try:
    from numpy import arccos
    from numpy import array
    from numpy import matrix
    from numpy import cross
    from numpy import int64
    from numpy import isnan
    from numpy import mean
    from numpy import newaxis
    from numpy import sin
    from numpy import cos
    from numpy import sum
    from numpy import tile
    from numpy import zeros
    from numpy import transpose
    from numpy import concatenate
    from numpy import asarray
    from numpy import sort
    from numpy import delete
    from numpy.linalg import norm
    from numpy import eye
    from numpy import trace
    from numpy import arctan
    from numpy import arcsin
    from numpy import dot
    from numpy import where
    from numpy.linalg import solve
    from numpy.linalg import inv
    from numpy.linalg import lstsq

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
    # Initialize
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

    # define indexing lists for rotational degrees of freedom
    IDXx = zeros((n, 1))
    IDXy = zeros((n, 1))
    IDXz = zeros((n, 1))
    IDXalpha = zeros((n, 1))
    IDXbeta = zeros((n, 1))
    IDXgamma = zeros((n, 1))
    counttra = 0
    countrot = 0
    for i in range(n):
        if i + 0.01 in freedof: 
            idxx = freedof.index(i + 0.01) 
        else:
            idxx = d
            counttra += 1
        if i + 0.02 in freedof: 
            idxy = freedof.index(i + 0.02)
        else:
            idxy = d
            counttra += 1
        if i + 0.03 in freedof: 
            idxz = freedof.index(i + 0.03) 
        else:
            idxz = d
            counttra += 1
        if i + 0.04 in freedof: 
            idxalpha = freedof.index(i + 0.04) 
        else:
            idxalpha = d
            countrot += 1
        if i + 0.05 in freedof: 
            idxbeta = freedof.index(i + 0.05) 
        else:
            idxbeta = d
            countrot += 1
        if i + 0.06 in freedof: 
            idxgamma = freedof.index(i + 0.06) 
        else:
            idxgamma = d
            countrot += 1
        IDXx[i] = idxx
        IDXy[i] = idxy
        IDXz[i] = idxz
        IDXalpha[i] = idxalpha
        IDXbeta[i] = idxbeta
        IDXgamma[i] = idxgamma
    IDXtra = sort(concatenate((IDXx, IDXy, IDXz)), 0)
    IDXtra = IDXtra[0:(3 * n - counttra)]
    IDXtra = array([int(round(j)) for j in IDXtra])

    IDXrot = sort(concatenate((IDXalpha, IDXbeta, IDXgamma)), 0)
    IDXrot = IDXrot[0:(3 * n - countrot)]
    IDXrot = array([int(round(j)) for j in IDXrot])
    
    ts = 0
    rnorm = tol + 1
    while ts <= steps and rnorm > tol:
        f = zeros((d, 1))
        K = zeros((d, d))

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
            alpha_u = x_[int(IDXalpha[ui])]
            beta_u = x_[int(IDXbeta[ui])]
            gamma_u = x_[int(IDXgamma[ui])]
            alpha_v = x_[int(IDXalpha[vi])]
            beta_v = x_[int(IDXbeta[vi])]
            gamma_v = x_[int(IDXgamma[vi])]

            Lambda_u = concatenate((alpha_u, beta_u, gamma_u), 0)
            lambda_u = norm(Lambda_u)
            if lambda_u == 0:
                R_u = eye(3)
            else:
                lambda_u_ = Lambda_u/lambda_u;
                S_u = skew(lambda_u_)
                """
                S_u = array([[0.0, -lambda_u_[2], lambda_u_[1]],
                    [lambda_u_[2], 0.0, -lambda_u_[0]],
                    [-lambda_u_[1], lambda_u_[0], 0.0]])
                """
                R_u = eye(3) + sin(lambda_u) * S_u + (1 - cos(lambda_u)) * dot(S_u, S_u)

            Lambda_v = concatenate((alpha_v, beta_v, gamma_v), 0)
            lambda_v = norm(Lambda_v)
            if lambda_v == 0:
                R_v = eye(3)
            else:
                lambda_v_ = Lambda_v/lambda_v;
                S_v = skew(lambda_v_)
                """
                array([[0.0, -lambda_v_[2], lambda_v_[1]],
                    [lambda_v_[2], 0.0, -lambda_v_[0]],
                    [-lambda_v_[1], lambda_v_[0], 0.0]])
                """
                R_v = eye(3) + sin(lambda_v) * S_v + (1 - cos(lambda_v)) * dot(S_v, S_v)
                

            T_u = dot(R_u, T_0[(i * 3):((i + 1) * 3), 0:3])
            T_v = dot(R_v, T_0[(i * 3):((i + 1) * 3), 0:3])

            x_u = T_u[:, 0]
            x_v = T_v[:, 0]
            y_u = T_u[:, 1]
            y_v = T_v[:, 1]
            z_u = T_u[:, 2]
            z_v = T_v[:, 2]

            # update element triad
            dR = T_v * transpose(T_u)
            
            #a = max(trace(dR), dR[0, 0], dR[1, 1], dR[2, 2])
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
            dRm = eye(3) + sin(mu / 2) * S + (1 - cos(mu / 2)) * dot(S, S);

            R_e = dot(dRm, T_u)
            
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

            u_ = [delta, theta_xu, theta_yu, theta_zu, theta_xv, theta_yv, theta_zv]
            
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
            """
            Sx = array([[0.0, -R_e[2, 0], R_e[1, 0]],
                [R_e[2, 0], 0.0, -R_e[0, 0]],
                [-R_e[1, 0], R_e[0, 0], 0.0]])
            """
            Sy = skew(R_e[:, 1])
            """
            Sy = array([[0.0, -R_e[2, 1], R_e[1, 1]],
                [R_e[2, 1], 0.0, -R_e[0, 1]],
                [-R_e[1, 1], R_e[0, 1], 0.0]])
            """
            Sz = skew(R_e[:, 2])
            """
            Sz = array([[0.0, -R_e[2, 2], R_e[1, 2]],
                [R_e[2, 2], 0.0, -R_e[0, 2]],
                [-R_e[1, 2], R_e[0, 2], 0.0]])
            """    
            
            B = 1 / l[i][0] * (eye(3) - dot(transpose([x_e]), [x_e]))

            L1_2 = dot(R_e[:, 1], x_e) / 2 * B + dot(B / 2, dot(transpose([R_e[:, 1]]), [(x_e + R_e[:, 0])]))
            L2_2 = Sy / 2 - dot(dot(R_e[:, 1], x_e) / 4, Sx) - dot(Sy / 4, dot(transpose([x_e]), [x_e + R_e[:, 0]]))
            
            L_2 = concatenate((L1_2, L2_2, -L1_2, L2_2))

            L1_3 = dot(R_e[:, 2], x_e) / 2 * B + dot(B / 2, dot(transpose([R_e[:, 2]]), [(x_e + R_e[:, 0])]))
            L2_3 = Sz / 2 - dot(dot(R_e[:, 2], x_e) / 4, Sx) - dot(Sz / 4, dot(transpose([x_e]), [x_e + R_e[:, 0]]))
            
            L_3 = concatenate((L1_3, L2_3, -L1_3, L2_3))
            
            Szu = skew(z_u)
            """
            array([[0, -z_u[2], z_u[1]],
                [z_u[2], 0, -z_u[0]],
                [-z_u[1], z_u[0], 0]])
            """
            Syu = skew(y_u)
            """
            array([[0, -y_u[2], y_u[1]],
                [y_u[2], 0, -y_u[0]],
                [-y_u[1], y_u[0], 0]])
            """
            Sxu = skew(x_u)
            """
            array([[0, -x_u[2], x_u[1]],
                [x_u[2], 0, -x_u[0]],
                [-x_u[1], x_u[0], 0]])
            """
            Szv = skew(z_v)
            """
            array([[0, -z_v[2], z_v[1]],
                [z_v[2], 0, -z_v[0]],
                [-z_v[1], z_v[0], 0]])
            """
            Syv = skew(y_v)
            """
            array([[0, -y_v[2], y_v[1]],
                [y_v[2], 0, -y_v[0]],
                [-y_v[1], y_v[0], 0]])
            """
            Sxv = skew(x_v)
            """
            array([[0, -x_v[2], x_v[1]],
                [x_v[2], 0, -x_v[0]],
                [-x_v[1], x_v[0], 0]])
            """
        
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

            for j in range(len(I[i])):
                f[I[i][j]] = f[I[i][j]] + fe[J[i][j]]

            # Stiffness matrix
            Ke_e = dot(dot(T, K_), transpose(T))

            #if i == m-1: print(K_)

            for j in range(len(I[i])):
                for k in range(len(I[i])):
                    K[I[i][j]][I[i][k]] = K[I[i][j]][I[i][k]] + Ke_e[J[i][j]][J[i][k]]
        
        #Update residual forces
        r = p - f
        rnorm = dot(transpose(r)[0], transpose(r)[0]) ** 0.5

        #Update velocities
        M = K
        vold = v
        v = (1 - xi * dt) / (1 + xi * dt) * vold + solve(M, r) / (1 + xi * dt) * dt

        #Update coordinates
        dx = dt * v
        xold = x

        x[IDXtra] = xold[IDXtra] + dx[IDXtra]
        
        Lambdaold = zeros((1, 3))
        dLambda = zeros((1, 3))
        for i in range(len(set(array(freedof_node)[IDXrot]))):
            for j in where(array(freedof_node)[IDXrot] == list(set(array(freedof_node)[IDXrot]))[i])[0]:
                Lambdaold[0][freedof_axis[IDXrot[j]] - 3] = xold[IDXrot[j]]
                dLambda[0][freedof_axis[IDXrot[j]] - 3] = dx[IDXrot[j]]
            lambdaold = norm(Lambdaold)
            if lambdaold == 0.0: Lold = Lambdaold
            else: Lold = Lambdaold / lambdaold
            qold = (sin(lambdaold / 2) * Lold)
            q0old = [cos(lambdaold / 2)]

            dlambda = norm(dLambda)
            if dlambda == 0.0: dL = dLambda
            else: dL = dLambda / dlambda
            dq = (sin(dlambda / 2) * dL)
            dq0 = [cos(dlambda / 2)]

            qnew = q0old * dq + dq0 * qold - cross(qold, dq)
            q0new = q0old[0] * dq0[0] - dot(qold[0], dq[0])

            lambdanew = 2 * arctan(norm(qnew) / q0new)
            if norm(qnew) == 0.0: Lnew = qnew
            else: Lnew = qnew / norm(qnew)
            Lambdanew = lambdanew * Lnew

            for j in where(array(freedof_node)[IDXrot] == list(set(array(freedof_node)[IDXrot]))[i])[0]:
                x[IDXrot[j]] = Lambdanew[0][freedof_axis[IDXrot[j]] - 3]


        for i in range(len(IDXtra)):       
            X[freedof_node[IDXtra[i]]][freedof_axis[IDXtra[i]]] = x[IDXtra[i]]

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
        if vertex.get('dofx', True) == True:
            freedof.append(i+0.01)
        if vertex.get('dofy', True) == True:
            freedof.append(i+0.02)
        if vertex.get('dofz', True) == True:
            freedof.append(i+0.03)
        if vertex.get('dofalpha', True) == True:
            freedof.append(i+0.04)
        if vertex.get('dofbeta', True) == True:
            freedof.append(i+0.05)
        if vertex.get('dofgamma', True) == True:
            freedof.append(i+0.06)
    return freedof

def skew(v):
    """ Constructs the skew-symmetric matrix S

    Parameters:
        v (array): A vector

    Returns:
        S (array): S of v
    """
    S = array([[0.0, -v[2], v[1]],
        [v[2], 0.0, -v[0]],
        [-v[1], v[0], 0.0]])
    return S

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
    X = dr_6dof_numpy(network, dt = 1.0, xi=1.0, tol=0.001, steps=50)
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
