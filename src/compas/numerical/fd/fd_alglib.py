from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import sys
import compas

from copy import deepcopy
from functools import partial

from compas.geometry import cross_vectors
from compas.geometry import length_vector
from compas.geometry import centroid_points

try:
    from compas.numerical.alglib.core import xalglib
except ImportError:
    compas.raise_if_ironpython()


__all__ = ['mesh_fd_alglib']


def mesh_fd_alglib(mesh, density=1.0, kmax=10):
    key_index = {key: index for index, key in enumerate(mesh.vertices())}

    xyz     = mesh.get_vertices_attributes('xyz')
    loads   = mesh.get_vertices_attributes(('px', 'py', 'pz'))
    n       = mesh.number_of_vertices()
    anchors = [key_index[key] for key, attr in mesh.vertices(True) if attr['is_anchor']]
    fixed   = []
    fixed   = list(set(anchors + fixed))
    free    = list(set(range(n)) - set(fixed))
    ni      = len(free)
    nf      = len(fixed)
    xyzf    = [xyz[i] for i in fixed]

    selfweight = _selfweight_calculator(mesh, density=density)

    adjacency = {key_index[key]: [key_index[nbr] for nbr in mesh.vertex_neighbors(key)] for key in mesh.vertices()}

    ij_q = {uv: mesh.get_edge_attribute(uv, 'q', 1.0) for uv in mesh.edges()}
    ij_q.update({(v, u): q for (u, v), q in ij_q.items()})

    for u, v in ij_q:
        if mesh.halfedge[u][v] is None or mesh.halfedge[v][u] is None:
            ij_q[u, v] = 0.0

    ij_q = {(key_index[u], key_index[v]): ij_q[u, v] for u, v in ij_q}

    nonzero_fixed, nonzero_free = _nonzero(adjacency, fixed, free)

    CtQC = xalglib.sparsecreate(n, n)
    CitQCi = xalglib.sparsecreate(ni, ni)
    CitQCf = xalglib.sparsecreate(ni, nf)

    s = xalglib.linlsqrcreate(ni, ni)

    _update_matrices(adjacency, free, nonzero_fixed, nonzero_free, CtQC, CitQCf, CitQCi, ij_q)

    for k in range(kmax):
        _compute_xyz_free(s, xyz, xyzf, loads, free, ni, CitQCf, CitQCi, selfweight=selfweight)

    p  = deepcopy(loads)
    sw = selfweight(xyz)

    for i in range(len(p)):
        p[i][2] -= sw[i]

    rx, ry, rz = _compute_residuals(xyz, p, n, CtQC)

    for key, attr in mesh.vertices(True):
        index = key_index[key]

        mesh.vertex[key]['x']  = xyz[index][0]
        mesh.vertex[key]['y']  = xyz[index][1]
        mesh.vertex[key]['z']  = xyz[index][2]
        mesh.vertex[key]['rx'] = rx[index]
        mesh.vertex[key]['ry'] = ry[index]
        mesh.vertex[key]['rz'] = rz[index]

    for u, v in mesh.edges():
        i, j = key_index[u], key_index[v]

        q = ij_q[i, j]
        l = mesh.edge_length(u, v)
        f = q * l
        mesh.set_edge_attributes((u, v), ('q', 'f', 'l'), (q, f, l))


def fd_alglib(vertices, edges, fixed, q, loads, **kwargs):
    pass


# ==============================================================================
# helpers
# ==============================================================================


def _selfweight_calculator(mesh, density=1.0):
    key_index = mesh.key_index()

    sw = [0] * mesh.number_of_vertices()
    ro = [attr['t'] * density for key, attr in mesh.vertices(True)]

    def calculate_selfweight(xyz):
        fkey_centroid = {fkey: mesh.face_centroid(fkey) for fkey in mesh.faces()}

        for u in mesh.vertices():
            i  = key_index[u]
            p0 = xyz[i]
            a  = 0

            for v in mesh.halfedge[u]:
                j   = key_index[v]
                p1  = xyz[j]
                p01 = [p1[axis] - p0[axis] for axis in range(3)]

                fkey = mesh.halfedge[u][v]
                if fkey in fkey_centroid:
                    p2  = fkey_centroid[fkey]
                    p02 = [p2[axis] - p0[axis] for axis in range(3)]
                    a  += 0.25 * length_vector(cross_vectors(p01, p02))

                fkey = mesh.halfedge[v][u]
                if fkey in fkey_centroid:
                    p3  = fkey_centroid[fkey]
                    p03 = [p3[axis] - p0[axis] for axis in range(3)]
                    a  += 0.25 * length_vector(cross_vectors(p01, p03))

            sw[i] = a * ro[i]

        return sw

    return calculate_selfweight


def _nonzero(adjacency, fixed, free):
    n = len(adjacency)

    j_col_free = {value: index for index, value in enumerate(free)}
    j_col_fixed = {value: index for index, value in enumerate(fixed)}
    i_nonzero_free = {i: [] for i in range(n)}
    i_nonzero_fixed = {i: [] for i in range(n)}

    fixed = set(fixed)

    for i in range(n):
        if i in fixed:
            i_nonzero_fixed[i].append((i, j_col_fixed[i]))
        else:
            i_nonzero_free[i].append((i, j_col_free[i]))

        for j in adjacency[i]:
            if j in fixed:
                i_nonzero_fixed[i].append((j, j_col_fixed[j]))
            else:
                i_nonzero_free[i].append((j, j_col_free[j]))

    return i_nonzero_fixed, i_nonzero_free


def _update_matrices(adjacency, free, nonzero_fixed, nonzero_free, CtQC, CitQCf, CitQCi, ij_q):
    xalglib.sparseconverttohash(CtQC)
    xalglib.sparseconverttohash(CitQCi)
    xalglib.sparseconverttohash(CitQCf)

    n = len(adjacency)
    ni = len(free)

    for i in range(n):
        Q = 0
        for j in adjacency[i]:
            q = ij_q[(i, j)]
            Q += q
            xalglib.sparseset(CtQC, i, j, -q)
        xalglib.sparseset(CtQC, i, i, Q)

    for row in range(ni):
        i = free[row]
        for j, col in nonzero_fixed[i]:
            xalglib.sparseset(CitQCf, row, col, xalglib.sparseget(CtQC, i, j))
        for j, col in nonzero_free[i]:
            xalglib.sparseset(CitQCi, row, col, xalglib.sparseget(CtQC, i, j))


def _compute_xyz_free(s, xyz, xyzf, loads, free, ni, CitQCf, CitQCi, selfweight=None):
    xalglib.sparseconverttocrs(CitQCi)
    xalglib.sparseconverttocrs(CitQCf)

    p = deepcopy(loads)

    if selfweight:
        sw = selfweight(xyz)
        for i in range(len(p)):
            p[i][2] -= sw[i]

    out = [[0, 0, 0] for row in range(ni)]

    b  = xalglib.sparsemm(CitQCf, xyzf, 3, out)
    bx = [p[free[row]][0] - b[row][0] for row in range(ni)]
    by = [p[free[row]][1] - b[row][1] for row in range(ni)]
    bz = [p[free[row]][2] - b[row][2] for row in range(ni)]

    xalglib.linlsqrsolvesparse(s, CitQCi, bx)
    xi, _ = xalglib.linlsqrresults(s)

    xalglib.linlsqrsolvesparse(s, CitQCi, by)
    yi, _ = xalglib.linlsqrresults(s)

    xalglib.linlsqrsolvesparse(s, CitQCi, bz)
    zi, _ = xalglib.linlsqrresults(s)

    for row in range(ni):
        index = free[row]
        xyz[index][0] = xi[row]
        xyz[index][1] = yi[row]
        xyz[index][2] = zi[row]


def _compute_residuals(xyz, p, n, CtQC):
    xalglib.sparseconverttocrs(CtQC)

    x, y, z = zip(*xyz)
    x = list(x)
    y = list(y)
    z = list(z)

    rx_ = [0] * n
    rx_ = xalglib.sparsemv(CtQC, x, rx_)
    rx  = [p[i][0] - rx_[i] for i in range(n)]

    ry_ = [0] * n
    ry_ = xalglib.sparsemv(CtQC, y, ry_)
    ry  = [p[i][1] - ry_[i] for i in range(n)]

    rz_ = [0] * n
    rz_ = xalglib.sparsemv(CtQC, z, rz_)
    rz  = [p[i][2] - rz_[i] for i in range(n)]

    return rx, ry, rz


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
