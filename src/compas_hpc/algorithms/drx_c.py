
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from ctypes import CDLL
from ctypes import c_double
from ctypes import c_float
from ctypes import c_int
from ctypes import POINTER

from compas.numerical.algorithms.drx_numpy import _create_arrays

from numpy import array
from numpy import int32

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
    # array
    #     Vertex co-ordinates.
    # array
    #     Edge forces.
    # array
    #     Edge lengths.

    """

    # Setup

    tic1 = time()

    X, B, P, S, V, E, A, C, Ct, f0, l0, ind_c, ind_t, u, v, M, k0, m, n = _create_arrays(network)

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

    # print(k0.ctypes.strides[:])
    # print(l0.ctypes.data)
    # print(l0.ctypes.shape[:])
    # print(l0.ctypes.strides[:])

    drx_c.drx_solver_c(
        c_double(tol),
        c_int(steps),
        c_int(summary),
        c_int(m),
        c_int(n),
        u.ctypes.data_as(POINTER(c_int)),
        v.ctypes.data_as(POINTER(c_int)),
        X.ctypes.data_as(POINTER(c_double)),
        f0.ctypes.data_as(POINTER(c_double)),
        l0.ctypes.data_as(POINTER(c_double)),
        k0.ctypes.data_as(POINTER(c_double)),
        ind_c.ctypes.data_as(POINTER(c_int)),
        ind_t.ctypes.data_as(POINTER(c_int)),
        c_int(ind_c_n),
        c_int(ind_t_n),
    )

    toc2 = time() - tic2

    # Summary

    if summary:
        print('\n\nC DR -------------------')
        print('Setup time: {0:.3f} s'.format(toc1))
        print('Solver time: {0:.3f} s'.format(toc2))
        print('----------------------------------')

# ctypes_module.add_float.restype = c_double
# res_float = ctypes_module.add_float(a, b)
# print(res_float)


if __name__ == "__main__":

    # ==========================================================================
    # Example 1
    # ==========================================================================

    from compas.datastructures import Network
    from compas.viewers import VtkViewer

    m = 2
    x = y = [(i / m - 0.5) * 5 for i in range(m + 1)]

    vertices = [[xi, yi, 0] for yi in y for xi in x]
    edges = []

    for i in range(m):
        for j in range(m):
            edges.append([(j + 0) * (m + 1) + i + 0, (j + 0) * (m + 1) + i + 1])
            edges.append([(j + 0) * (m + 1) + i + 0, (j + 1) * (m + 1) + i + 0])
            if j == m - 1:
                edges.append([(j + 1) * (m + 1) + i + 1, (j + 1) * (m + 1) + i + 0])
            if i == m - 1:
                edges.append([(j + 0) * (m + 1) + i + 1, (j + 1) * (m + 1) + i + 1])

    network = Network.from_vertices_and_edges(vertices=vertices, edges=edges)
    pz = 1000 / network.number_of_vertices()
    sides = [i for i in network.vertices() if network.vertex_degree(i) <= 3]
    network.update_default_vertex_attributes({'P': [0, 0, pz]})
    network.update_default_edge_attributes({'E': 10, 'A': 1, 'ct': 't'})
    network.set_vertices_attributes(sides, {'B': [0, 0, 0]})

    drx_c(network=network, tol=0.01, summary=1)

    data = {}
    data['vertices'] = {i: network.vertex_coordinates(i) for i in network.vertices()}
    data['edges']    = [{'u': u, 'v': v} for u, v in network.edges()]

    viewer = VtkViewer(data=data)
    viewer.settings['draw_vertices'] = 0
    viewer.settings['edge_width']    = 0.01
    # viewer.start()
