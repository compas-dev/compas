from compas.geometry import add_vectors
from compas.geometry import cross_vectors
from compas.geometry import normalize_vector
from compas.geometry import scale_vector
from compas.geometry import subtract_vectors

from numpy import array
from numpy import cos
from numpy import cross
from numpy import hstack
from numpy import newaxis
from numpy import ones
from numpy import sin
from numpy import tile
from numpy import zeros
from numpy.linalg import norm

from numba import float64
from numba import int64
from numba import jit

from compas.hpc import numba_cross
from compas.hpc import numba_length

from time import time


__author__     = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2017, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'liew@arch.ethz.ch'


def f(x, y):
    return sin(x) * cos(y)


@jit(float64(float64, float64), nogil=True, nopython=True)
def fj(x, y):
    return sin(x) * cos(y)


def python_normals(points, offset=0.1, delta=10**(-5)):

    tic = time()

    n = len(points)
    normals = [0] * n
    c = 0
    for x, y, z in points:
        zx = f(x + delta, y)
        zy = f(x, y + delta)
        xyz = [x, y, z]
        vecx = subtract_vectors([x + delta, y, zx], xyz)
        vecy = subtract_vectors([x, y + delta, zy], xyz)
        vecn = normalize_vector(cross_vectors(vecx, vecy))
        normals[c] = add_vectors(xyz, scale_vector(vecn, offset))
        c += 1

    toc = time() - tic

    return normals, toc


def numpy_normals(points, offset=0.1, delta=10**(-5)):

    tic = time()

    xyz = array(points)
    X = xyz[:, 0][:, newaxis]
    Y = xyz[:, 1][:, newaxis]
    Z = xyz[:, 2][:, newaxis]
    delta_ = ones(X.shape) * delta
    zeros_ = zeros(X.shape)
    zx = f(X + delta_, Y)
    zy = f(X, Y + delta_)
    vecx = hstack([delta_, zeros_, zx - Z])
    vecy = hstack([zeros_, delta_, zy - Z])
    n_ = cross(vecx, vecy)
    vecn = n_ / tile(norm(n_, ord=2, axis=1)[:, newaxis], (1, 3))
    normals = xyz + offset * vecn

    toc = time() - tic

    return [list(i) for i in list(normals)], toc


def numba_normals(points, offset=0.1, delta=10**(-5)):

    tic = time()

    n = len(points)
    normals = zeros((n, 3))
    xyz = array(points)
    X = xyz[:, 0]
    Y = xyz[:, 1]
    Z = xyz[:, 2]
    normals = njit(normals, X, Y, Z, n, delta, offset)

    toc = time() - tic

    return [list(i) for i in list(normals)], toc


@jit(float64[:, :](float64[:, :], float64[:], float64[:], float64[:], int64, float64, float64), nogil=True, nopython=True)
def njit(normals, X, Y, Z, n, delta, offset):
    vecx = array([delta, 0, 0])
    vecy = array([0, delta, 0])
    for i in range(n):
        xi = X[i]
        yi = Y[i]
        zi = Z[i]
        zx = fj(xi + delta, yi)
        zy = fj(xi, yi + delta)
        vecx[2] = zx - zi
        vecy[2] = zy - zi
        n_ = numba_cross(vecx, vecy)
        vecn = n_ / numba_length(n_)
        normals[i, 0] = xi + offset * vecn[0]
        normals[i, 1] = yi + offset * vecn[1]
        normals[i, 2] = zi + offset * vecn[2]
    return normals


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':

    points = [[1., 2., 3.], [2., 3., 4.], [5., 6., 7.]]
    normals = numba_normals(points=points)

    print(normals)
