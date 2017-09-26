""""""
from compas.geometry.hpc.cvector cimport CVector


__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


cdef class CPoint:

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
    # magic methods: representation
    # ==========================================================================

    def __str__(CPoint self):
        return "CPoint({}, {}, {})".format(self.x, self.y, self.z)

    def __repr__(CPoint self):
        return "CPoint({}, {}, {})".format(self.x, self.y, self.z)

    # ==========================================================================
    # magic methods: access
    # ==========================================================================

    def __getitem__(CPoint self, int key):
        cdef int i

        i = key % 3
        if i == 0:
            return self.x
        if i == 1:
            return self.y
        if i == 2:
            return self.z

        raise KeyError

    def __setitem__(CPoint self, int key, float value):
        cdef int i

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

    def __iter__(CPoint self):
        return iter([self.x, self.y, self.z])

    # ==========================================================================
    # magic methods: math
    # ==========================================================================

    def __add__(CPoint u, object v):
        return CPoint(u.x + v[0], u.y + v[1], u.z + v[2])

    def __iadd__(CPoint u, object v):
        u.x += v[0]
        u.y += v[1]
        u.z += v[2]
        return u

    def __sub__(CPoint u, object v):
        return CPoint(u.x - v[0], u.y - v[1], u.z - v[2])

    def __isub__(CPoint u, object v):
        u.x -= v[0]
        u.y -= v[1]
        u.z -= v[2]
        return u

    def __mul__(CPoint u, float n):
        return CPoint(u.x * n, u.y * n, u.z * n)

    def __imul__(CPoint u, float n):
        u.x *= n
        u.y *= n
        u.z *= n
        return u

    def __pow__(CPoint u, float n, m):
        return CPoint(pow(u[0], n), pow(u[1], n), pow(u[2], n))

    # ==========================================================================
    # methods
    # ==========================================================================

    cpdef double distance_to_point(CPoint a, object b):
        cdef CVector ab = CVector.from_points(a, b)
        return ab.length()

    cpdef double distance_to_line(CPoint point, object line):
        cdef object a
        cdef object b
        cdef CVector ab
        cdef CVector pa
        cdef CVector pb
        cdef CVector pa_pb
        cdef double l_pa_pb
        cdef double l_ab

        a, b = line
        ab = CVector.from_points(a, b)
        pa = CVector.from_points(point, a)
        pb = CVector.from_points(point, b)

        return pa.cross(pb).length() / ab.length()


