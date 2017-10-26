from time import time


__author__     = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2017, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'liew@arch.ethz.ch'


# ==============================================================================
# Domain
# ==============================================================================

n = 500  # number of points along x and y
ds = 0.2  # spacing of each x and y step
delta = 10**(-5)  # small finite difference
offset = 0.2  # offset between two surfaces
x = [ds * i for i in range(n)]  # domain for x
y = [ds * i for i in range(n)]  # domain for y


# ==============================================================================
# Python
# ==============================================================================

from compas.geometry import add_vectors
from compas.geometry import cross_vectors
from compas.geometry import normalize_vector
from compas.geometry import scale_vector
from compas.geometry import subtract_vectors

from math import cos
from math import sin


def f(x, y):
    return sin(x) * cos(y)


tic = time()

z = [0] * n
normals = [0] * n

for i, yi in enumerate(y):

    z[i] = [0] * n
    normals[i] = [0] * n

    for j, xi in enumerate(x):

        z[i][j] = f(xi, yi)
        zx = f(xi + delta, yi)
        zy = f(xi, yi + delta)

        xyz = [xi, yi, z[i][j]]
        vecx = subtract_vectors([xi + delta, yi, zx], xyz)
        vecy = subtract_vectors([xi, yi + delta, zy], xyz)
        vecn = normalize_vector(cross_vectors(vecx, vecy))

        normals[i][j] = add_vectors(xyz, scale_vector(vecn, offset))

print('\nPython : {0:.4f} ms'.format((time() - tic) * 1000))


# ==============================================================================
# Numpy
# ==============================================================================

from numpy import array
from numpy import cos
from numpy import cross
from numpy import dstack
from numpy import meshgrid
from numpy import newaxis
from numpy import ones
from numpy import sin
from numpy import zeros
from numpy.linalg import norm


def f(x, y):
    return sin(x) * cos(y)


tic = time()

X, Y = meshgrid(x, y)
delta_ = ones(X.shape) * delta
Z = f(X, Y)
zx = f(X + delta_, Y)
zy = f(X, Y + delta_)

vecx = dstack([delta_, zeros(X.shape), zx - Z])
vecy = dstack([zeros(X.shape), delta_, zy - Z])
n_ = cross(vecx, vecy)
vecn = n_ / norm(n_, ord=2, axis=2)[:, :, newaxis]

normals = dstack([X, Y, Z]) + offset * vecn

print('Numpy : {0:.4f} ms'.format((time() - tic) * 1000))


# ==============================================================================
# Numba
# ==============================================================================

from numba import float64
from numba import int64
from numba import jit

from compas.hpc import numba_cross
from compas.hpc import numba_length


@jit(float64(float64, float64), nogil=True, nopython=True)
def f(x, y):
    return sin(x) * cos(y)


@jit(float64[:, :, :](float64[:], float64[:], int64, float64, float64), nogil=True, nopython=True)
def njit(x, y, n, delta, offset):

    normals = zeros((n, n, 3))
    vecx = array([delta, 0, 0])
    vecy = array([0, delta, 0])

    i = 0
    for i in range(n):

        xi = x[i]

        for j in range(n):

            yi = y[i]

            zij = f(xi, yi)
            zx = f(xi + delta, yi)
            zy = f(xi, yi + delta)

            vecx[2] = zx - zij
            vecy[2] = zy - zij
            n_ = numba_cross(vecx, vecy)
            vecn = n_ / numba_length(n_)

            normals[i, j, 0] = xi + offset * vecn[0]
            normals[i, j, 1] = yi + offset * vecn[1]
            normals[i, j, 2] = zij + offset * vecn[2]

    return normals


tic = time()
njit(array(x), array(y), n, delta, offset)
print('Numba : {0:.4f} ms'.format((time() - tic) * 1000))


# ==============================================================================
# Plot
# ==============================================================================

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

normals = array(normals)
Xn = normals[:, :, 0]
Yn = normals[:, :, 1]
Zn = normals[:, :, 2]

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.plot_surface(X, Y, Z)
ax.plot_surface(Xn, Yn, Zn)
plt.show()
