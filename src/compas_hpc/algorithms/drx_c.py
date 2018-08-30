
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from ctypes import CDLL
from ctypes import c_double
from ctypes import c_int
from ctypes import POINTER

from compas.numerical.algorithms.drx_numpy import _beam_data
from compas.numerical.algorithms.drx_numpy import _create_arrays

from numpy import array
from numpy import ctypeslib
from numpy import float64
from numpy import int32
from numpy import zeros

from time import time


__author__    = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__ = 'Copyright 2018, BLOCK Research Group - ETH Zurich'
__license__   = 'MIT License'
__email__     = 'liew@arch.ethz.ch'


__all__ = [
    'drx_c',
]


def drx_c(network, factor=1.0, tol=0.1, steps=10000, summary=0, update=False):

    """ Run C accelerated dynamic relaxation analysis.

    Parameters
    ----------
    network : obj
        Network to analyse.
    factor : float
        Convergence factor.
    tol : float
        Tolerance value.
    steps : int
        Maximum number of steps.
    summary : int
        Print summary at end (1:yes or 0:no).
    update : bool
        Update the co-ordinates of the Network.

    Returns
    -------
    array
        Vertex co-ordinates.
    array
        Edge forces.
    array
        Edge lengths.

    """

    # Setup

    tic1 = time()

    X, B, P, S, V, E, A, C, Ct, f0, l0, ind_c, ind_t, u, v, M, k0, m, n, rows, cols, vals, nv = _create_arrays(network)
    inds, indi, indf, EIx, EIy, beams = _beam_data(network)

    if not ind_c:
        ind_c = array([0], dtype=int32)
        ind_c_n = 0
    else:
        ind_c = array(ind_c, dtype=int32)
        ind_c_n = len(ind_c)

    if not ind_t:
        ind_t = array([0], dtype=int32)
        ind_t_n = 0
    else:
        ind_t = array(ind_t, dtype=int32)
        ind_t_n = len(ind_t)

    toc1 = time() - tic1

    # Solver

    tic2 = time()

    drx_c = CDLL('./drx_c.so')

    f = zeros(m, dtype=float64)
    ptr1 = X.ctypes.data_as(POINTER(c_double))

    drx_c.drx_solver_c(
        c_double(tol),
        c_int(steps),
        c_int(summary),
        c_int(m),
        c_int(n),
        u.ctypes.data_as(POINTER(c_int)),
        v.ctypes.data_as(POINTER(c_int)),
        ptr1,
        f0.ctypes.data_as(POINTER(c_double)),
        l0.ctypes.data_as(POINTER(c_double)),
        k0.ctypes.data_as(POINTER(c_double)),
        ind_c.ctypes.data_as(POINTER(c_int)),
        ind_t.ctypes.data_as(POINTER(c_int)),
        c_int(ind_c_n),
        c_int(ind_t_n),
        B.ctypes.data_as(POINTER(c_double)),
        P.ctypes.data_as(POINTER(c_double)),
        S.ctypes.data_as(POINTER(c_double)),
        rows.ctypes.data_as(POINTER(c_int)),
        cols.ctypes.data_as(POINTER(c_int)),
        vals.ctypes.data_as(POINTER(c_double)),
        c_int(nv),
        M.ctypes.data_as(POINTER(c_double)),
        c_double(factor),
        V.ctypes.data_as(POINTER(c_double)),
        inds.ctypes.data_as(POINTER(c_int)),
        indi.ctypes.data_as(POINTER(c_int)),
        indf.ctypes.data_as(POINTER(c_int)),
        EIx.ctypes.data_as(POINTER(c_double)),
        EIy.ctypes.data_as(POINTER(c_double)),
        c_int(beams),
        c_int(len(inds)),
    )

    Xr = ctypeslib.as_array(ptr1, (n, 3))
    # Xr[:, 0] = X[:, 0]  # hack
    # print(X)
    # send and bring over f and l

    toc2 = time() - tic2

    # Summary

    if summary:
        print('\n\nC DR -------------------')
        print('Setup time: {0:.3f} s'.format(toc1))
        print('Solver time: {0:.3f} s'.format(toc2))
        print('----------------------------------')

    # Update

    if update:

        k_i = network.key_index()
        for key in network.vertices():
            x, y, z = Xr[k_i[key], :]
            network.set_vertex_attributes(key, 'xyz', [x, y, z])

        uv_i = network.uv_index()
        for uv in network.edges():
            i = uv_i[uv]
            network.set_edge_attribute(uv, 'f', float(f[i]))


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    # ==========================================================================
    # Example 1 (dense)
    # ==========================================================================

    # from compas.datastructures import Network
    # from compas.viewers import VtkViewer


    # m = 150
    # p = [(i / m - 0.5) * 5 for i in range(m + 1)]
    # vertices = [[xi, yi, 0] for yi in p for xi in p]
    # edges = []

    # for i in range(m):
    #     for j in range(m):
    #         s = (m + 1)
    #         p1 = (j + 0) * s + i + 0
    #         p2 = (j + 0) * s + i + 1
    #         p3 = (j + 1) * s + i + 0
    #         p4 = (j + 1) * s + i + 1
    #         edges.append([p1, p2])
    #         edges.append([p1, p3])
    #         if j == m - 1:
    #             edges.append([p4, p3])
    #         if i == m - 1:
    #             edges.append([p2, p4])

    # network = Network.from_vertices_and_edges(vertices=vertices, edges=edges)
    # sides = [i for i in network.vertices() if network.vertex_degree(i) <= 2]
    # network.update_default_vertex_attributes({'P': [0, 0, 1000 / network.number_of_vertices()]})
    # network.update_default_edge_attributes({'E': 100, 'A': 1, 'ct': 't'})
    # network.set_vertices_attributes(keys=sides, names='B', values=[[0, 0, 0]])

    # drx_c(network=network, tol=0.01, summary=1, update=1)

    # data = {
    #     'vertices': {i: network.vertex_coordinates(i) for i in network.vertices()},
    #     'edges':    [{'u': u, 'v': v} for u, v in network.edges()]
    # }

    # viewer = VtkViewer(data=data)
    # viewer.vertex_size = 0
    # viewer.edge_width  = 0.01
    # viewer.setup()
    # viewer.start()


    # ==========================================================================
    # Example 2 (beam)
    # ==========================================================================

    from compas.datastructures import Network
    from compas.viewers import VtkViewer

    from numpy import linspace


    L  = 12
    n  = 200
    EI = 0.2

    vertices = [[i, 1 - abs(i), 0] for i in list(linspace(-5, 5, n))]
    edges = [[i, i + 1] for i in range(n - 1)]

    network = Network.from_vertices_and_edges(vertices=vertices, edges=edges)
    leaves  = network.leaves()
    network.update_default_vertex_attributes({'EIx': EI, 'EIy': EI})
    network.update_default_edge_attributes({'E': 50, 'A': 1, 'l0': L / n})
    network.set_vertices_attributes(['B', 'is_fixed'], [[0, 0, 0], True], leaves)
    network.beams = {'beam': {'nodes': list(range(n))}}

    drx_c(network=network, tol=0.01, summary=1, update=1, factor=5)

    data = {
        'vertices': {i: network.vertex_coordinates(i) for i in network.vertices()},
        'edges':    [{'u': u, 'v': v} for u, v in network.edges()]
    }

    viewer = VtkViewer(data=data)
    viewer.setup()
    viewer.start()
