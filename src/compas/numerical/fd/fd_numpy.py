from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from numpy import asarray
from scipy.sparse import diags
from scipy.sparse.linalg import spsolve

from compas.numerical import connectivity_matrix
from compas.numerical import normrow


__all__ = ['fd_numpy']


def fd_numpy(vertices, edges, fixed, q, loads, **kwargs):
    """Implementation of the force density method to compute equilibrium of axial force networks.

    Parameters
    ----------
    vertices : list
        XYZ coordinates of the vertices of the network
    edges : list
        Edges between vertices represented by
    fixed : list
        Indices of fixed vertices.
    q : list
        Force density of edges.
    loads : list
        XYZ components of the loads on the vertices.

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
    For more info, see [1]_

    References
    ----------
    .. [1] Schek H., *The Force Density Method for Form Finding and Computation of General Networks*,
           Computer Methods in Applied Mechanics and Engineering 3: 115-134, 1974.

    Examples
    --------
    >>>

    """
    v = len(vertices)
    free = list(set(range(v)) - set(fixed))
    xyz = asarray(vertices, dtype=float).reshape((-1, 3))
    q = asarray(q, dtype=float).reshape((-1, 1))
    p = asarray(loads, dtype=float).reshape((-1, 3))
    C = connectivity_matrix(edges, 'csr')
    Ci = C[:, free]
    Cf = C[:, fixed]
    Ct = C.transpose()
    Cit = Ci.transpose()
    Q = diags([q.flatten()], [0])
    A = Cit.dot(Q).dot(Ci)
    b = p[free] - Cit.dot(Q).dot(Cf).dot(xyz[fixed])

    xyz[free] = spsolve(A, b)

    l = normrow(C.dot(xyz))  # noqa: E741
    f = q * l
    r = p - Ct.dot(Q).dot(C).dot(xyz)

    return xyz, q, f, l, r


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    import doctest

    doctest.testmod(globs=globals())
