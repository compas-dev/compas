from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from copy import deepcopy
from math import sqrt

__all__ = ['dr']


K = [
    [0.0],
    [0.5, 0.5],
    [0.5, 0.0, 0.5],
    [1.0, 0.0, 0.0, 1.0],
]


class Coeff():
    def __init__(self, c):
        self.c = c
        self.a = (1 - c * 0.5) / (1 + c * 0.5)
        self.b = 0.5 * (1 + self.a)


def norm_vector(vector):
    """
    Calculate the length of a vector.

    Parameters
    ----------
    vector : list
        XYZ components of the vector.

    Returns
    -------
    float
        The L2 norm, or *length* of the vector.

    Examples
    --------
    >>>
    """
    return sqrt(sum(axis ** 2 for axis in vector))


def norm_vectors(vectors):
    """
    Calculate the norm of each vector in a list of vectors.

    Parameters
    ----------
    vectors : list
        A list of vectors

    Returns
    -------
    list
        A list with the lengths of all vectors.

    Examples
    --------
    >>>
    """
    return [norm_vector(vector) for vector in vectors]


def adjacency_from_edges(edges):
    """Construct an adjacency dictionary from a set of edges.

    Parameters
    ----------
    edges : list
        A list of index pairs.

    Returns
    -------
    dict
        A dictionary mapping each index in the list of index pairs
        to a list of adjacent indices.

    Examples
    --------
    >>>
    """
    adj = {}
    for i, j in iter(edges):
        adj.setdefault(i, []).append(j)
        adj.setdefault(j, []).append(i)
    return adj


def dr(vertices, edges, fixed, loads, qpre,
       fpre=None, lpre=None,
       linit=None, E=None, radius=None,
       kmax=100, dt=1.0, tol1=1e-3, tol2=1e-6, c=0.1, callback=None, callback_args=None):
    """Implementation of dynamic relaxation with RK integration scheme in pure Python.

    Parameters
    ----------
    vertices : list
        XYZ coordinates of the vertices.
    edges : list
        Connectivity of the vertices.
    fixed : list
        Indices of the fixed vertices.
    loads : list
        XYZ components of the loads on the vertices.
    qpre : list
        Prescribed force densities in the edges.
    fpre : list, optional
        Prescribed forces in the edges.
    lpre : list, optional
        Prescribed lengths of the edges.
    linit : list, optoional
        Initial length of the edges.
    E : list, optional
        Stiffness of the edges.
    radius : list, optional
        Radius of the edges.
    kmax : int, optional
        Maximum number of iterations.
    dt : float, optional
        The time step.
    tol1 : float, optional
        Convergence criterion for the residual forces.
    tol2 : float, optional
        Convergence criterion for the displacements in between interations.
    c : float, optional
        Damping factor for viscous damping.
    callback : callable, optional
        A user-defined callback that is called after every iteration.
        The callback will be called with ``k`` the current iteration,
        ``X`` the coordinates at iteration ``k``,
        ``crit1, crit2`` the values of the stoppage criteria at iteration ``k``,
        and ``callback_args`` the optional additional arguments.
    callback_args : tuple, optional
        Additional arguments to be passed to the callback.

    Returns
    -------
    xyz : array
        XYZ coordinates of the equilibrium geometry.
    q : array
        Force densities in the edges.
    f : array
        Forces in the edges.
    l : array
        Lengths of the edges
    r : array
        Residual forces.

    Examples
    --------
    >>>
    """
    if callback:
        if not callable(callback):
            raise Exception('The callback is not callable.')
    # --------------------------------------------------------------------------
    # preprocess
    # --------------------------------------------------------------------------
    n = len(vertices)
    e = len(edges)

    # i_nbrs = {i: [ij[1] if ij[0] == i else ij[0] for ij in edges if i in ij] for i in range(n)}

    i_nbrs = adjacency_from_edges(edges)

    ij_e = {(i, j): index for index, (i, j) in enumerate(edges)}
    ij_e.update({(j, i): index for (i, j), index in ij_e.items()})

    coeff = Coeff(c)
    ca = coeff.a
    cb = coeff.b
    free = list(set(range(n)) - set(fixed))
    # --------------------------------------------------------------------------
    # attribute arrays
    # --------------------------------------------------------------------------
    X = vertices
    P = loads
    Qpre = qpre or [0.0 for _ in range(e)]
    Fpre = fpre or [0.0 for _ in range(e)]
    Lpre = lpre or [0.0 for _ in range(e)]
    # --------------------------------------------------------------------------
    # initial values
    # --------------------------------------------------------------------------
    Q = [1.0 for _ in range(e)]
    L = [sum((X[i][axis] - X[j][axis]) ** 2 for axis in (0, 1, 2)) ** 0.5 for i, j in iter(edges)]
    F = [q * l for q, l in zip(Q, L)]
    M = [sum(0.5 * dt ** 2 * Q[ij_e[(i, j)]] for j in i_nbrs[i]) for i in range(n)]
    V = [[0.0, 0.0, 0.0] for _ in range(n)]
    R = [[0.0, 0.0, 0.0] for _ in range(n)]
    dX = [[0.0, 0.0, 0.0] for _ in range(n)]
    # --------------------------------------------------------------------------
    # helpers
    # --------------------------------------------------------------------------

    def update_R():
        for i in range(n):
            x = X[i][0]
            y = X[i][1]
            z = X[i][2]
            f = [0.0, 0.0, 0.0]
            for j in i_nbrs[i]:
                q = Q[ij_e[(i, j)]]
                f[0] += q * (X[j][0] - x)
                f[1] += q * (X[j][1] - y)
                f[2] += q * (X[j][2] - z)
            R[i] = [P[i][axis] + f[axis] for axis in (0, 1, 2)]

    def rk(X0, V0, steps=2):
        def a(t, V):
            dX = [[V[i][axis] * t for axis in (0, 1, 2)] for i in range(n)]
            for i in free:
                X[i] = [X0[i][axis] + dX[i][axis] for axis in (0, 1, 2)]
            update_R()
            return [[cb * R[i][axis] / M[i] for axis in (0, 1, 2)] for i in range(n)]

        if steps == 2:
            B = [0.0, 1.0]
            a0 = a(K[0][0] * dt, V0)
            k0 = [[dt * a0[i][axis] for axis in (0, 1, 2)] for i in range(n)]
            a1 = a(K[1][0] * dt, [[V0[i][axis] + K[1][1] * k0[i][axis] for axis in (0, 1, 2)] for i in range(n)])
            k1 = [[dt * a1[i][axis] for axis in (0, 1, 2)] for i in range(n)]
            return [[B[0] * k0[i][axis] + B[1] * k1[i][axis] for axis in (0, 1, 2)] for i in range(n)]

        if steps == 4:
            B = [1.0 / 6.0, 1.0 / 3.0, 1.0 / 3.0, 1.0 / 6.0]
            a0 = a(K[0][0] * dt, V0)
            k0 = [[dt * a0[i][axis] for axis in (0, 1, 2)] for i in range(n)]
            a1 = a(K[1][0] * dt, [[V0[i][axis] + K[1][1] * k0[i][axis] for axis in (0, 1, 2)] for i in range(n)])
            k1 = [[dt * a1[i][axis] for axis in (0, 1, 2)] for i in range(n)]
            a2 = a(K[2][0] * dt, [[V0[i][axis] + K[2][1] * k0[i][axis] + K[2][2] * k1[i][axis] for axis in (0, 1, 2)] for i in range(n)])
            k2 = [[dt * a2[i][axis] for axis in (0, 1, 2)] for i in range(n)]
            a3 = a(K[3][0] * dt, [[V0[i][axis] + K[3][1] * k0[i][axis] + K[3][2] * k1[i][axis] + K[3][3] * k2[i][axis] for axis in (0, 1, 2)] for i in range(n)])
            k3 = [[dt * a3[i][axis] for axis in (0, 1, 2)] for i in range(n)]
            return [[B[0] * k0[i][axis] +
                     B[1] * k1[i][axis] +
                     B[2] * k2[i][axis] +
                     B[3] * k3[i][axis] for axis in (0, 1, 2)] for i in range(n)]

        raise NotImplementedError

    # --------------------------------------------------------------------------
    # start iterating
    # --------------------------------------------------------------------------
    for k in range(kmax):
        Qfpre = [a / b if b else 0 for a, b in zip(Fpre, L)]
        Qlpre = [a / b if b else 0 for a, b in zip(F, Lpre)]

        Q = [a + b + c for a, b, c in zip(Qpre, Qfpre, Qlpre)]
        M = [sum(0.5 * dt ** 2 * Q[ij_e[(i, j)]] for j in i_nbrs[i]) for i in range(n)]

        X0 = deepcopy(X)
        V0 = [[ca * V[i][axis] for axis in (0, 1, 2)] for i in range(n)]

        # RK
        dV = rk(X0, V0, steps=4)

        # update
        for i in free:
            V[i] = [V0[i][axis] + dV[i][axis] for axis in (0, 1, 2)]
            dX[i] = [V[i][axis] * dt for axis in (0, 1, 2)]
            X[i] = [X0[i][axis] + dX[i][axis] for axis in (0, 1, 2)]

        L = [sum((X[i][axis] - X[j][axis]) ** 2 for axis in (0, 1, 2)) ** 0.5 for i, j in iter(edges)]
        F = [q * l for q, l in zip(Q, L)]

        update_R()

        # crits
        crit1 = max(norm_vectors([R[i] for i in free]))
        crit2 = max(norm_vectors([dX[i] for i in free]))

        # callback
        if callback:
            callback(k, X, (crit1, crit2), callback_args)

        # convergence
        if crit1 < tol1:
            break
        if crit2 < tol2:
            break
    # --------------------------------------------------------------------------
    # update
    # --------------------------------------------------------------------------
    update_R()

    return X, Q, F, L, R


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
