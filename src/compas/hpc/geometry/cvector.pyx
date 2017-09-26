""""""

from math import sin
from math import cos
from math import sqrt

from itertools import chain

from compas.geometry import dot_vectors

from cpython.array cimport array
from cpython.array cimport clone

# from cython.view cimport varray
# from libcpp.vector cimport vector


__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


def cross(list a, list b):
    n  = len(a)
    _a = chain.from_iterable(a)
    _b = chain.from_iterable(b)
    return _cross(_a, _b, n)


# http://www.codeguru.com/cpp/cpp/cpp_mfc/stl/article.php/c4027/C-Tutorial-A-Beginners-Guide-to-stdvector-Part-1.htm
# http://cython.readthedocs.io/en/latest/src/tutorial/array.html
# http://cython.readthedocs.io/en/latest/src/userguide/memoryviews.html
# https://groups.google.com/forum/#!topic/cython-users/CwtU_jYADgM
# http://cython.readthedocs.io/en/latest/src/userguide/language_basics.html#differences-between-c-and-cython-expressions
# http://docs.cython.org/en/latest/src/userguide/wrapping_CPlusPlus.html#standard-library
# http://notes-on-cython.readthedocs.io/en/latest/index.html
# http://en.cppreference.com/w/cpp/container/vector
# https://docs.python.org/2/library/array.html
# https://stackoverflow.com/questions/2672085/static-array-vs-dynamic-array-in-c
# http://www.cplusplus.com/forum/general/833/
cdef array _cross(object a, object b, int n):
    cdef array _a = array('d', a)
    cdef array _b = array('d', b)
    cdef array _r = clone(array('d', []), n * 3, zero=True)

    cdef double[:] a_view = _a
    cdef double[:,:] a_view2 = <double[:n, :3]> &a_view[0]

    cdef double[:] b_view = _b
    cdef double[:,:] b_view2 = <double[:n, :3]> &b_view[0]

    cdef double[:] r_view = _r
    cdef double[:,:] r_view2 = <double[:n, :3]> &r_view[0]

    cdef int i
    cdef int j

    for i in range(n):
        r_view2[i, 0] = a_view2[i, 1] * b_view2[i, 2] - a_view2[i, 2] * b_view2[i, 1]
        r_view2[i, 1] = a_view2[i, 2] * b_view2[i, 0] - a_view2[i, 0] * b_view2[i, 2]
        r_view2[i, 2] = a_view2[i, 0] * b_view2[i, 1] - a_view2[i, 1] * b_view2[i, 0]

    return _r


cdef class CVector:
    
    def __cinit__(self, x, y, z):
        self._x = 0.0
        self._y = 0.0
        self._z = 0.0
        self.x = x
        self.y = y
        self.z = z

    # ==========================================================================
    # descriptors
    # ==========================================================================

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        self._x = float(x)

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        self._y = float(y)

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, z):
        self._z = float(z)

    # ==========================================================================
    # magic methods
    # ==========================================================================

    def __str__(self):
        return "CVector({}, {}, {})".format(self.x, self.y, self.z)

    def __repr__(self):
        return "CVector({}, {}, {})".format(self.x, self.y, self.z)

    def __getitem__(CVector self, int key):
        i = key % 3
        if i == 0:
            return self.x
        if i == 1:
            return self.y
        if i == 2:
            return self.z
        raise KeyError

    def __setitem__(CVector self, int key, float value):
        i = key % 3
        if i == 0:
            self.x = value
            return
        if i == 1:
            self.y = value
            return
        if i == 2:
            self.z = value
            return
        raise KeyError

    def __iter__(self):
        return iter([self.x, self.y, self.z])

    def __add__(self, other):
        return CVector(self[0] + other[0], self[1] + other[1], self[2] + other[2])

    def __iadd__(self, other):
        self.x += other[0]
        self.y += other[1]
        self.z += other[2]
        return self

    def __sub__(self, other):
        return CVector(self[0] - other[0], self[1] - other[1], self[2] - other[2])

    def __isub__(self, other):
        self.x -= other[0]
        self.y -= other[1]
        self.z -= other[2]
        return self

    def __mul__(self, double n):
        return CVector(self.x * n, self.y * n, self.z * n)

    def __imul__(self, double n):
        self.x *= n
        self.y *= n
        self.z *= n
        return self

    def __pow__(x, y, z):
        return CVector(pow(x[0], y, z), pow(x[1], y, z), pow(x[2], y, z))

    # def __ipow__(self, n):
    #     self.x **= n
    #     self.y **= n
    #     self.z **= n
    #     return self

    # ==========================================================================
    # constructors
    # ==========================================================================

    @classmethod
    def from_points(cls, a, b):
        return cls(b[0] - a[0], b[1] - a[1], b[2] - a[2])

    # ==========================================================================
    # methods
    # ==========================================================================

    cpdef double length(CVector self):
        return sqrt(self.x ** 2 + self.y ** 2 + self.z **2)

    cpdef double dot(CVector u, object v):
        return dot_vectors(u, v)

    cpdef CVector cross(CVector u, object v):
        cdef double x, y, z
        x = u[1] * v[2] - u[2] * v[1]
        y = u[2] * v[0] - u[0] * v[2]
        z = u[0] * v[1] - u[1] * v[0]
        return CVector(x, y, z)

    cpdef CVector normalize(CVector self):
        cdef double l
        l = self.length()
        self.x = self.x / l
        self.y = self.y / l
        self.z = self.z / l

    cpdef CVector normalized(CVector self):
        cdef double l
        l = self.length()
        x = self.x / l
        y = self.y / l
        z = self.z / l
        return CVector(x, y, z)

    # def translate(self, vector):
    #     raise NotImplementedError

    # def translated(self, vector):
    #     raise NotImplementedError

    # def rotate(self, angle, axis=None, origin=None):
    #     """Rotate a vector u over an angle a around an axis k."""
    #     if axis is None:
    #         axis = (0, 0, 1.0)
    #     if origin is None:
    #         origin = (0, 0, 0)
    #     sina = sin(angle)
    #     cosa = cos(angle)
    #     kxu  = self.cross(axis) * -1
    #     v    = [sina * x for x in kxu]
    #     w    = [x * (1 - cosa) for x in cross_vectors(axis, kxu)]
    #     return [self[_] + v[_] + w[_] + origin[_] for _ in range(3)]

    # def rotated(self, angle, axis=None, origin=None):
    #     raise NotImplementedError

    # def scale(self, n):
    #     """Scale this ``Vector`` by a factor ``n``.

    #     Parameters:
    #         n (int, float): The scaling factor.

    #     Note:
    #         This is an alias for self \*= n
    #     """
    #     self *= n

    # def scaled(self, n):
    #     raise NotImplementedError


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':

    pass
