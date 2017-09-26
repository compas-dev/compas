from __future__ import print_function

from math import sin
from math import cos
from math import sqrt
from math import pi

from compas.geometry.basic import *


__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


class Vector(object):
    """A vector object represents a vector in three-dimensional space.

    The vector is defined as the difference vector between the start and end
    point. The start point is optional and defaults to the origin [0, 0, 0].

    Parameters:
        end (list): The xyz coordinates of the end point.
        start (list): The xyz coordinates of the start point, defaults to [0, 0, 0].

    Attributes:
        x (float): The x-coordinate of the coordinate difference vector.
        y (float): The y-coordinate of the coordinate difference vector.
        z (float): The z-coordinate of the coordinate difference vector.
        length (float): (**read-only**) The length of the vector.

    Examples:
        >>> u = Vector([1, 0, 0])
        >>> v = Vector([0, 2, 0], [0, 1, 0])
        >>> u
        [1.0, 0.0, 0.0]
        >>> v
        [0.0, 1.0, 0.0]
        >>> u.x
        1.0
        >>> u[0]
        1.0
        >>> u.length
        1.0
        >>> u + v
        [1.0, 1.0, 0.0]
        >>> u + [0.0, 1.0, 0.0]
        [1.0, 1.0, 0.0]
        >>> u * 2
        [2.0, 0.0, 0.0]
        >>> u.dot(v)
        0.0
        >>> u.cross(v)
        [0.0, 0.0, 1.0]

    """

    __slots__ = ['_x', '_y', '_z', '_w']

    def __init__(self, x=0.0, y=0.0, z=0.0, w=1.0, unitize=False):
        self._x = 0.0
        self._y = 0.0
        self._z = 0.0
        self._w = 1.0
        self.x = x
        self.y = y
        self.z = z
        self.w = w
        if unitize:
            self.unitize()

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

    @property
    def w(self):
        return self._w

    @w.setter
    def w(self, w):
        self._w = float(w)

    # ==========================================================================
    # representation
    # ==========================================================================

    def __repr__(self):
        return '[{0}, {1}, {2}]'.format(self.x, self.y, self.z)

    # ==========================================================================
    # access
    # ==========================================================================

    def __getitem__(self, key):
        i = key % 3
        if i == 0:
            return self.x
        if i == 1:
            return self.y
        if i == 2:
            return self.z
        raise KeyError

    def __setitem__(self, key, value):
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

    # ==========================================================================
    # operators
    # ==========================================================================

    def __add__(self, other):
        """Compute the sum of this ``Vector`` and another ``Vector``.

        Parameters:
            other (tuple, list, Vector): The vector to add.

        Returns:
            Vector: The vector sum.
        """
        return Vector(self.x + other[0], self.y + other[1], self.z + other[2])

    def __sub__(self, other):
        """Compute the difference between this ``Vector`` and another ``Vector``.

        Parameters:
            other (tuple, list, Vector): The vector to subtract.

        Returns:
            Vector: The vector difference.
        """
        return Vector(self.x - other[0], self.y - other[1], self.z - other[2])

    def __mul__(self, n):
        """Scale this ``Vector`` by a factor.

        Parameters:
            n (int, float): The scaling factor.

        Returns:
            Vector: The scaled vector.

        Examples:
            >>> u = Vector([1, 0, 0])
            >>> v = u * 2
        """
        return Vector(self.x * n, self.y * n, self.z * n)

    def __pow__(self, n):
        return Vector(self.x ** n, self.y ** n, self.z ** n)

    # ==========================================================================
    # in-place operators
    # ==========================================================================

    def __iadd__(self, other):
        self.x += other[0]
        self.y += other[1]
        self.z += other[2]
        return self

    def __isub__(self, other):
        self.x -= other[0]
        self.y -= other[1]
        self.z -= other[2]
        return self

    def __imul__(self, n):
        self.x *= n
        self.y *= n
        self.z *= n
        return self

    def __ipow__(self, n):
        self.x **= n
        self.y **= n
        self.z **= n
        return self

    # ==========================================================================
    # methods: static
    # ==========================================================================

    @staticmethod
    def length_vectors(vectors):
        return [length_vector(vector) for vector in vectors]

    @staticmethod
    def norm_vectors(vectors):
        return [norm_vector(vector) for vector in vectors]

    # @staticmethod
    # def sum_vectors(vectors):
    #     pass

    # @staticmethod
    # def add_vectors(vectors):
    #     pass

    @staticmethod
    def dot(u, v):
        """The dot product of this ``Vector`` and another ``Vector``.

        Parameters:
            other (tuple, list, Vector): The vector to dot.

        Returns:
            float: The dot product.
        """
        return dot_vectors(u, v)

    @staticmethod
    def dot_vectors(left, right):
        return [dot_vectors(u, v) for u, v in zip(left, right)]

    @staticmethod
    def cross(u, v):
        """The cross product of this ``Vector`` and another ``Vector``.

        Parameters:
            other (tuple, list, Vector): The vector to cross.

        Returns:
            Vector: The cross product.
        """
        return Vector(* cross_vectors(u, v))

    @staticmethod
    def cross_vectors(left, right):
        return [Vector.cross(u, v) for u, v in zip(left, right)]

    @staticmethod
    def angles(u, v):
        pass

    @staticmethod
    def angle(u, v):
        pass

    @staticmethod
    def homogenise_vectors(vectors):
        pass

    @staticmethod
    def dehomogenise_vectors(vectors):
        pass

    @staticmethod
    def orthonormalise_vectors(vectors):
        pass

    # ==========================================================================
    # helpers
    # ==========================================================================

    def copy(self):
        return Vector(self.x, self.y, self.z)

    # ==========================================================================
    # properties
    # ==========================================================================

    def length(self):
        return sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def norm(self):
        return sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    # ==========================================================================
    # methods: none
    # ==========================================================================

    def unitize(self):
        l = self.length()
        self.x = self.x / l
        self.y = self.y / l
        self.z = self.z / l

    def homogenise(self):
        pass

    def dehomogenise(self):
        pass

    def reverse(self):
        pass

    # ==========================================================================
    # methods: float
    # ==========================================================================

    def scale(self, n):
        """Scale this vector by a factor n.

        Parameters:
            n (int, float): The scaling factor.

        Note:
            This is an alias for self \*= n
        """
        self *= n

    # ==========================================================================
    # methods: misc
    # ==========================================================================

    def transform(self, matrix):
        points = transform([self, ], matrix)
        self.x = points[0][0]
        self.y = points[0][1]
        self.z = points[0][2]

    def translate(self, other):
        self.x += other[0]
        self.y += other[1]
        self.z += other[2]

    def rotate(self, angle, axis=None, origin=None):
        """Rotate a vector u over an angle a around an axis k.

        Parameters
        ----------
        angle : float
            The rotation angle in radians.
        axis : list, Vector
            The rotation axis.
            Default is the Z axis (``[0.0, 0.0, 1.0]``).
        origin : list, Point
            The origin of the rotation axis.
            Default is ``[0.0, 0.0, 0.0]``.

        """
        if axis is None:
            axis = [0.0, 0.0, 1.0]
        if origin is None:
            origin = [0.0, 0.0, 0.0]

        sina = sin(angle)
        cosa = cos(angle)
        kxu  = Vector.cross(axis, self)
        v    = kxu * sina
        w    = Vector.cross(axis, kxu) * (1 - cosa)

        self.x += v[0] + w[0] + origin[0]
        self.y += v[1] + w[1] + origin[1]
        self.z += v[2] + w[2] + origin[2]

    def project(self):
        pass

    def reflect(self):
        pass


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':

    u = Vector(1.0, 0.0, 0.0)
    v = Vector(0.0, 1.0, 0.0)

    print(u)

    print(Vector.dot(u, v))
    print(Vector.cross(u, v))

    u.rotate(pi / 2)

    print(u)

    R = rotation_matrix(- pi / 2, [0.0, 0.0, 1.0])
    u.transform(R)

    print(u)
