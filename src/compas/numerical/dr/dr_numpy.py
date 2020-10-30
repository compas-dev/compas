from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from numpy import array
from numpy import isnan
from numpy import isinf
from numpy import ones
from numpy import zeros
from scipy.linalg import norm
from scipy.sparse import diags

from compas.numerical import connectivity_matrix
from compas.numerical import normrow


__all__ = ['dr_numpy']


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


def dr_numpy(vertices, edges, fixed, loads, qpre,
             fpre=None, lpre=None, linit=None, E=None, radius=None,
             callback=None, callback_args=None, **kwargs):
    """Implementation of the dynamic relaxation method for form findong and analysis
    of articulated networks of axial-force members.

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
    lpre : list, optinonal
        Prescribed lengths of the edges.
    linit : list, optional
        Initial length of the edges.
    E : list, optional
        Stiffness of the edges.
    radius : list, optional
        Radius of the edges.
    callback : callable, optional
        User-defined function that is called at every iteration.
    callback_args : tuple, optional
        Additional arguments passed to the callback.

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

    Notes
    -----
    For more info, see [1]_.

    References
    ----------
    .. [1] De Laet L., Veenendaal D., Van Mele T., Mollaert M. and Block P.,
           *Bending incorporated: designing tension structures by integrating bending-active elements*,
           Proceedings of Tensinet Symposium 2013,Istanbul, Turkey, 2013.

    Examples
    --------
    >>>
    """
    # --------------------------------------------------------------------------
    # callback
    # --------------------------------------------------------------------------
    if callback:
        assert callable(callback), 'The provided callback is not callable.'
    # --------------------------------------------------------------------------
    # configuration
    # --------------------------------------------------------------------------
    kmax = kwargs.get('kmax', 10000)
    dt = kwargs.get('dt', 1.0)
    tol1 = kwargs.get('tol1', 1e-3)
    tol2 = kwargs.get('tol2', 1e-6)
    coeff = Coeff(kwargs.get('c', 0.1))
    ca = coeff.a
    cb = coeff.b
    # --------------------------------------------------------------------------
    # attribute lists
    # --------------------------------------------------------------------------
    num_v = len(vertices)
    num_e = len(edges)
    free = list(set(range(num_v)) - set(fixed))
    # --------------------------------------------------------------------------
    # input processing
    # --------------------------------------------------------------------------
    qpre = qpre or [0.0 for _ in range(num_e)]
    fpre = fpre or [0.0 for _ in range(num_e)]
    lpre = lpre or [0.0 for _ in range(num_e)]
    linit = linit or [0.0 for _ in range(num_e)]
    E = E or [0.0 for _ in range(num_e)]
    radius = radius or [0.0 for _ in range(num_e)]
    # --------------------------------------------------------------------------
    # attribute arrays
    # --------------------------------------------------------------------------
    x = array(vertices, dtype=float).reshape((-1, 3))                      # m
    p = array(loads, dtype=float).reshape((-1, 3))                         # kN
    qpre = array(qpre, dtype=float).reshape((-1, 1))
    fpre = array(fpre, dtype=float).reshape((-1, 1))                       # kN
    lpre = array(lpre, dtype=float).reshape((-1, 1))                       # m
    linit = array(linit, dtype=float).reshape((-1, 1))                     # m
    E = array(E, dtype=float).reshape((-1, 1))                             # kN/mm2 => GPa
    radius = array(radius, dtype=float).reshape((-1, 1))                   # mm
    # --------------------------------------------------------------------------
    # sectional properties
    # --------------------------------------------------------------------------
    A = 3.14159 * radius ** 2                                              # mm2
    EA = E * A                                                             # kN
    # --------------------------------------------------------------------------
    # create the connectivity matrices
    # after spline edges have been aligned
    # --------------------------------------------------------------------------
    C = connectivity_matrix(edges, 'csr')
    Ct = C.transpose()
    Ci = C[:, free]
    Cit = Ci.transpose()
    Ct2 = Ct.copy()
    Ct2.data **= 2
    # --------------------------------------------------------------------------
    # if none of the initial lengths are set,
    # set the initial lengths to the current lengths
    # --------------------------------------------------------------------------
    if all(linit == 0):
        linit = normrow(C.dot(x))
    # --------------------------------------------------------------------------
    # initial values
    # --------------------------------------------------------------------------
    q = ones((num_e, 1), dtype=float)
    l = normrow(C.dot(x))  # noqa: E741
    f = q * l
    v = zeros((num_v, 3), dtype=float)
    r = zeros((num_v, 3), dtype=float)
    # --------------------------------------------------------------------------
    # helpers
    # --------------------------------------------------------------------------

    def rk(x0, v0, steps=2):
        def a(t, v):
            dx = v * t
            x[free] = x0[free] + dx[free]
            # update residual forces
            r[free] = p[free] - D.dot(x)
            return cb * r / mass

        if steps == 1:
            return a(dt, v0)

        if steps == 2:
            B = [0.0, 1.0]
            K0 = dt * a(K[0][0] * dt, v0)
            K1 = dt * a(K[1][0] * dt, v0 + K[1][1] * K0)
            dv = B[0] * K0 + B[1] * K1
            return dv

        if steps == 4:
            B = [1. / 6., 1. / 3., 1. / 3., 1. / 6.]
            K0 = dt * a(K[0][0] * dt, v0)
            K1 = dt * a(K[1][0] * dt, v0 + K[1][1] * K0)
            K2 = dt * a(K[2][0] * dt, v0 + K[2][1] * K0 + K[2][2] * K1)
            K3 = dt * a(K[3][0] * dt, v0 + K[3][1] * K0 + K[3][2] * K1 + K[3][3] * K2)
            dv = B[0] * K0 + B[1] * K1 + B[2] * K2 + B[3] * K3
            return dv

        raise NotImplementedError

    # --------------------------------------------------------------------------
    # start iterating
    # --------------------------------------------------------------------------
    for k in range(kmax):
        # print(k)

        q_fpre = fpre / l
        q_lpre = f / lpre
        q_EA = EA * (l - linit) / (linit * l)
        q_lpre[isinf(q_lpre)] = 0
        q_lpre[isnan(q_lpre)] = 0
        q_EA[isinf(q_EA)] = 0
        q_EA[isnan(q_EA)] = 0

        q = qpre + q_fpre + q_lpre + q_EA
        Q = diags([q[:, 0]], [0])
        D = Cit.dot(Q).dot(C)
        mass = 0.5 * dt ** 2 * Ct2.dot(qpre + q_fpre + q_lpre + EA / linit)
        # RK
        x0 = x.copy()
        v0 = ca * v.copy()
        dv = rk(x0, v0, steps=4)
        v[free] = v0[free] + dv[free]
        dx = v * dt
        x[free] = x0[free] + dx[free]
        # update
        u = C.dot(x)
        l = normrow(u)  # noqa: E741
        f = q * l
        r = p - Ct.dot(Q).dot(u)
        # crits
        crit1 = norm(r[free])
        crit2 = norm(dx[free])
        # callback
        if callback:
            callback(k, x, [crit1, crit2], callback_args)
        # convergence
        if crit1 < tol1:
            break
        if crit2 < tol2:
            break
    return x, q, f, l, r


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
