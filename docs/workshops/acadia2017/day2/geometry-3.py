from random import random as rnd
import time

from compas.geometry import Vector

from compas.geometry import add_vectors
from compas.geometry import sum_vectors
from compas.geometry import vector_from_points


# create random points
points = [(rnd(), rnd(), rnd()) for _ in range(10000)]
# define origin
origin = [1., 2., 3.]


# Object-based method
tic = time.time()
#-------------------------
vecs = [Vector.from_start_end(origin, pt) for pt in points]
res = Vector(0., 0., 0.)
for v in vecs:
    res += v
#-------------------------
toc = time.time()
print('{0} seconds to compute for object-based method'.format(toc - tic))
print(res)
print('------------------')


# Function-based method A
tic = time.time()
#-------------------------
vecs = [vector_from_points(origin, pt) for pt in points]
res = [0., 0., 0.]
for v in vecs:
    res = add_vectors(res, v)
#-------------------------
toc = time.time()
print('{0} seconds to compute for function-based method A'.format(toc - tic))
print(res)
print('------------------')


# Function-based method B
tic = time.time()
#-------------------------
vecs = [vector_from_points(origin, pt) for pt in points]
res = sum_vectors(vecs)
#-------------------------
toc = time.time()
print('{0} seconds to compute for function-based method B'.format(toc - tic))
print(res)
print('------------------')