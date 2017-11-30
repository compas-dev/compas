from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from numpy import abs
from numpy import array
from numpy import ceil
from numpy import dot
from numpy import hstack
from numpy import kron
from numpy import max
from numpy import maximum
from numpy import min
from numpy import minimum
from numpy import newaxis
from numpy import ones
from numpy import ravel
from numpy import reshape
from numpy import sqrt
from numpy import squeeze
from numpy import sum
from numpy import tile
from numpy import vstack
from numpy import zeros

from scipy.sparse import coo_matrix
from scipy.sparse.linalg import spsolve

from matplotlib import pyplot as plt


__author__    = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__ = 'Copyright 2017, BLOCK Research Group - ETH Zurich'
__license__   = 'MIT License'
__email__     = 'liew@arch.ethz.ch'


__all__ = [
    'topop2d_numpy'
]


def topop2d_numpy(nelx, nely, loads, supports, volfrac=0.5, penal=3, rmin=1.5):
    """ Topology optimisation in 2D using NumPy and SciPy [andreassen2011]_.

    Parameters
    ----------
    nelx : int
        Number of elements in x.
    nely : int
        Number of elements in y.
    loads : dict
        {'i-j': [Px, Py]}.
    supports : dict
        {'i-j': [Bx, By]} 1=fixed, 0=free.
    volfrac : float
        Volume fraction.
    penal : float
        Penalisation power.
    rmin : float
        Filter radius.

    Returns
    -------
    array
        Density array.

    """
    nx = nelx + 1
    ny = nely + 1
    nn = nx * ny
    ne = nelx * nely
    ndof = 2 * nn
    dv = ones((nely, nelx))

    # Finite element analysis

    v = 0.3
    E = 1.
    Emin = 10**(-10)

    A11 = array([[12, +3, -6, -3], [+3, 12, +3, +0], [-6, +3, 12, -3], [-3, +0, -3, 12]])
    A12 = array([[-6, -3, +0, +3], [-3, -6, -3, -6], [+0, -3, -6, +3], [+3, -6, +3, -6]])
    B11 = array([[-4, +3, -2, +9], [+3, -4, -9, +4], [-2, -9, -4, -3], [+9, +4, -3, -4]])
    B12 = array([[+2, -3, +4, -9], [-3, +2, +9, -2], [+4, +9, +2, +3], [-9, -2, +3, +2]])
    A21 = A12.transpose()
    B21 = B12.transpose()
    A = vstack([hstack([A11, A12]), hstack([A21, A11])])
    B = vstack([hstack([B11, B12]), hstack([B21, B11])])

    Ke = 1 / (1 - v**2) / 24 * (A + v * B)
    Ker = ravel(Ke, order='F')[:, newaxis]
    nodes = reshape(range(1, nn + 1), (ny, nx), order='F')
    eVec = tile(reshape(2 * nodes[:-1, :-1], (ne, 1), order='F'), (1, 8))
    edof = eVec + tile(hstack([array([0, 1]), 2 * nely + array([2, 3, 0, 1]), array([-2, -1])]), (ne, 1))
    iK = reshape(kron(edof, ones((8, 1))).transpose(), (64 * ne), order='F')
    jK = reshape(kron(edof, ones((1, 8))).transpose(), (64 * ne), order='F')

    # Supports

    U = zeros((ndof, 1))
    fixed = []
    for support, B in supports.items():
        ib, jb = [int(i) for i in support.split('-')]
        Bx, By = B
        node = int(jb * (nely + 1) + ib)
        if Bx:
            fixed.append(2 * node)
        if By:
            fixed.append(2 * node + 1)
    free = list(set(range(ndof)) - set(fixed))

    # Loads

    data = []
    rows = []
    cols = []
    for load, P in loads.items():
        ip, jp = [int(i) for i in load.split('-')]
        Px, Py = P
        node = int(jp * (nely + 1) + ip)
        data.extend([Px, Py])
        rows.extend([2 * node, 2 * node + 1])
        cols.extend([0, 0])
    F = coo_matrix((data, (rows, cols)), shape=(ndof, 1))
    Find = F.tocsr()[free]

    # Filter

    iH = zeros(ne * (2 * (int(ceil(rmin)) - 1) + 1)**2)
    jH = zeros(iH.shape)
    sH = zeros(iH.shape)

    k = 0
    for i1 in range(nelx):
        for j1 in range(nely):

            e1 = i1 * nely + j1
            max_i = int(max([i1 - (ceil(rmin) - 1), 0]))
            min_i = int(min([i1 + (ceil(rmin) - 1), nelx - 1]))

            for i2 in range(max_i, min_i + 1):
                max_j = int(max([j1 - (ceil(rmin) - 1), 0]))
                min_j = int(min([j1 + (ceil(rmin) - 1), nely - 1]))

                for j2 in range(max_j, min_j + 1):
                    k += 1
                    e2 = i2 * nely + j2
                    iH[k] = e1
                    jH[k] = e2
                    sH[k] = max([0, rmin - sqrt((i1 - i2)**2 + (j1 - j2)**2)])

    H = coo_matrix((sH, (iH, jH)))
    Hs = sum(H.toarray(), 1)

    # Set-up plot

    plt.axis([0, nelx, 0, nely])
    plt.ion()

    # Main loop

    iteration = 0
    change = 1
    move = 0.2
    x = tile(volfrac, (nely, nelx))
    xP = x * 1.
    nones = ones((ne)) * 0.001

    while change > 0.1:

        # FE

        xrav = ravel(xP, order='F').transpose()
        sK = reshape(Ker * (Emin + xrav**penal * (E - Emin)), (64 * ne), order='F')
        K = coo_matrix((sK, (iK, jK))).tocsr()
        Kind = (K.tocsc()[:, free]).tocsr()[free, :]
        U[free] = spsolve(Kind, Find)[:, newaxis]

        # Objective functions

        ce = reshape(sum(dot(squeeze(U[edof]), Ke) * squeeze(U[edof]), 1), (nely, nelx), order='F')
        c = sum(sum((Emin + xP**penal * (E - Emin)) * ce))
        dc = -penal * (E - Emin) * xP**(penal - 1) * ce
        xdc = squeeze(H.dot(ravel(x * dc, order='F')[:, newaxis]))
        dc = reshape(xdc / Hs / maximum(nones, ravel(x, order='F')), (nely, nelx), order='F')

        # Lagrange mulipliers

        l1 = 0
        l2 = 10**9
        while (l2 - l1) / (l1 + l2) > 0.001:
            lmid = 0.5 * (l2 + l1)
            sdv = sqrt(-dc / dv / lmid)
            min1 = minimum(x + move, x * sdv)
            xn = maximum(0, maximum(x - move, minimum(1, min1)))
            xP = xn * 1.
            if sum(xP) > volfrac * ne:
                l1 = lmid
            else:
                l2 = lmid
        change = max(abs(xn - x))

        # Update

        x = xn * 1.
        plt.imshow(1 - x, cmap='gray', origin='lower')
        plt.pause(0.001)

        iteration += 1

        print('Iteration: {0}  Compliance: {1:.4g}'.format(iteration, c))

    return x


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    loads = {
        '40-200': [0, -1]}

    supports = {
        '0-0': [1, 1],
        '0-400': [0, 1]}

    x = topop2d_numpy(nelx=400, nely=40, loads=loads, supports=supports, volfrac=0.5)
