""""""

try:
    from compas.numerical._backends.alglib import xalglib
except ImportError:
    import platform
    if platform.python_implementation() == 'IronPython':
        raise


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


def make_CtQC_partitioned(network, fixed, free, k_i, i_k, ij_q):
    n = len(network)
    ni = len(free)
    nf = len(fixed)

    CtQC  = [[0.0 for j in range(n)] for i in range(n)]
    _CtQC = xalglib.sparsecreate(n, n)

    i_nonzero = dict()

    for i in range(n):
        i_nonzero[i] = [i]
        key = i_k[i]
        Q = 0
        for nbr in network.neighbours(key):
            j = k_i[nbr]
            q = ij_q[(i, j)]
            Q += q
            CtQC[i][j] = -q
            #
            xalglib.sparseset(_CtQC, i, j, -q)
            #
            i_nonzero[i].append(j)
        CtQC[i][i] = Q
        #
        xalglib.sparseset(_CtQC, i, i, Q)

    CitQCi = xalglib.sparsecreate(ni, ni)

    j_col = dict((value, index) for index, value in enumerate(free))

    for row in range(ni):
        i = free[row]
        for j in i_nonzero[i]:
            if j in j_col:
                col = j_col[j]
                xalglib.sparseset(CitQCi, row, col, CtQC[i][j])

    CitQCf = xalglib.sparsecreate(ni, nf)

    j_col = dict((value, index) for index, value in enumerate(fixed))

    for row in range(ni):
        i = free[row]
        for j in i_nonzero[i]:
            if j in j_col:
                col = j_col[j]
                xalglib.sparseset(CitQCf, row, col, CtQC[i][j])

    return _CtQC, CitQCi, CitQCf


def update_equilibrium_from_qs(network):
    # --------------------------------------------------------------------------
    # preprocess
    #
    k_i     = dict((key, index) for index, key in network.vertices_enum())
    i_k     = dict(network.vertices_enum())
    xyz     = [network.vertex_coordinates(key) for key in network]
    n       = len(xyz)
    anchors = [k_i[key] for key, attr in network.vertices_iter(True) if attr['is_anchor']]
    fixed   = []
    fixed   = list(set(anchors + fixed))
    free    = list(set(range(n)) - set(fixed))
    ni      = len(free)
    p       = network.get_vertices_attributes(('px', 'py', 'pz'), (0.0, 0.0, 0.0))
    xyzf    = [xyz[i] for i in fixed]
    # --------------------------------------------------------------------------
    # force density map
    #
    ij_q = dict(((k_i[u], k_i[v]), attr['q']) for u, v, attr in network.edges_iter(True))
    ij_q.update(((k_i[v], k_i[u]), attr['q']) for u, v, attr in network.edges_iter(True))
    # --------------------------------------------------------------------------
    # CitQCi and CitQCf
    #
    CtQC, CitQCi, CitQCf = make_CtQC_partitioned(network, fixed, free, k_i, i_k, ij_q)
    # --------------------------------------------------------------------------
    # CitQCi and CitQCf conversion to better calculation format
    #
    xalglib.sparseconverttocrs(CtQC)
    xalglib.sparseconverttocrs(CitQCi)
    xalglib.sparseconverttocrs(CitQCf)
    # --------------------------------------------------------------------------
    # solve b = CitQCf * xyzf
    # this is the second part of b in
    # CitQCi.xyzi = pi - CitQCf.xyzf
    #
    b  = xalglib.sparsemm(CitQCf, xyzf, 3, [[0, 0, 0] for row in range(ni)])

    bx = [p[free[row]][0] - b[row][0] for row in range(ni)]
    by = [p[free[row]][1] - b[row][1] for row in range(ni)]
    bz = [p[free[row]][2] - b[row][2] for row in range(ni)]
    # --------------------------------------------------------------------------
    # create linear least squares problem
    #
    s = xalglib.linlsqrcreate(ni, ni)
    # --------------------------------------------------------------------------
    # solve
    #
    xalglib.linlsqrsolvesparse(s, CitQCi, bx)
    xi, _ = xalglib.linlsqrresults(s)

    xalglib.linlsqrsolvesparse(s, CitQCi, by)
    yi, _ = xalglib.linlsqrresults(s)

    xalglib.linlsqrsolvesparse(s, CitQCi, bz)
    zi, _ = xalglib.linlsqrresults(s)
    # --------------------------------------------------------------------------
    # residual forces
    #
    for row in range(ni):
        index = free[row]
        xyz[index][0] = xi[row]
        xyz[index][1] = yi[row]
        xyz[index][2] = zi[row]

    x = [temp[0] for temp in xyz]
    y = [temp[1] for temp in xyz]
    z = [temp[2] for temp in xyz]

    rx_ = [0] * n
    rx_ = xalglib.sparsemv(CtQC, x, rx_)
    rx  = [p[i][0] - rx_[i] for i in range(n)]

    ry_ = [0] * n
    ry_ = xalglib.sparsemv(CtQC, y, ry_)
    ry  = [p[i][1] - ry_[i] for i in range(n)]

    rz_ = [0] * n
    rz_ = xalglib.sparsemv(CtQC, z, rz_)
    rz  = [p[i][2] - rz_[i] for i in range(n)]
    # --------------------------------------------------------------------------
    # update vertices
    #
    for key in network.vertex:
        # index = free[row]
        # key = i_k[index]
        index = k_i[key]
        network.vertex[key]['x']  = xyz[index][0]
        network.vertex[key]['y']  = xyz[index][1]
        network.vertex[key]['z']  = xyz[index][2]
        network.vertex[key]['rx'] = rx[index]
        network.vertex[key]['ry'] = ry[index]
        network.vertex[key]['rz'] = rz[index]
    # --------------------------------------------------------------------------
    # update edges
    #
    for u, v in network.edges():
        q = ij_q[(k_i[u], k_i[v])]
        l = network.edge_length(u, v)
        f = q * l
        network.edge[u][v]['q'] = q
        network.edge[u][v]['l'] = l
        network.edge[u][v]['f'] = f


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":
    pass
