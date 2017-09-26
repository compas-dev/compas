""""""

import time

from compas.geometry.elements.vector import Vector

from compas.geometry.hpc.cvector import CVector
from compas.geometry.hpc.cpoint import CPoint

from compas.geometry.hpc.cvector import cross
from compas.geometry import cross_vectors


__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


def _cross_vectors(u, v, n):
    cross = cross_vectors
    return [cross(u[i], v[i]) for i in range(n)]


# tic = time.time()
# for i in range(100000):
#     u = [1.0, 0.0, 0.0]
# toc = time.time()
# print(toc - tic)

# tic = time.time()
# for i in range(100000):
#     u = Vector([1.0, 0.0, 0.0])
# toc = time.time()
# print(toc - tic)

# tic = time.time()
# for i in range(100000):
#     u = CVector(1.0, 0.0, 0.0)
# toc = time.time()
# print(toc - tic)

# print('')

u = CVector(3.0, 0.0, 0.0)
v = CVector(0.0, 5.0, 0.0)
w = u.cross(v)

print(u)
print(v)
print(w)

print(u.length())
print(v.length())
print(w.length())

print(u.dot(v))
print(u.normalize())
print(u)
print(v.normalized())

a = CPoint(0.0, 0.0, 0.0)
b = CPoint(1.0, 1.0, 0.0)
c = [0.0, 1.0, 0.0]

line = a, c

print(a.distance_to_point(b))
print(b.distance_to_line(line))

n = 100000

u = [u for i in range(n)]
v = [v for i in range(n)]

tic = time.time()
cross(u, v)
toc = time.time()
print(toc - tic)

tic = time.time()
_cross_vectors(u, v, n)
toc = time.time()
print(toc - tic)
