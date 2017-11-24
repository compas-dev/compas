from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from math import sin
from math import cos
from math import sqrt
from math import pi

from compas.geometry import *


__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


__all__ = ['Vector']


class Vector(object):
    """A vector object represents a vector in three-dimensional space.

    The vector is defined as the difference vector between the start and end
    point. The start point is optional and defaults to the origin [0, 0, 0].

    Parameters
    ----------
    x : float
        The X component of the vector.
    y : float
        The Y component of the vector.
    z : float
        The Z component of the vector.
    w : float, optional
        Homogenisation factor.
        Default is ``1.0``.
    unitize : bool, optional
        Unitize the vector.
        Default is ``False``.

    Attributes
    ----------
    x : float
        The X component of the vector.
    y : float
        The Y component of the vector.
    z : float
        The Z component of the vector.
    length : float, **read-only**
        The length of the vector.

    Examples
    --------
    >>> u = Vector(1, 0, 0)
    >>> v = Vector(0, 1, 0)
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

    def __init__(self, x, y, z, w=1.0, unitize=False):
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
    # factory
    # ==========================================================================

    @classmethod
    def from_start_end(cls, start, end):
        v = subtract_vectors(end, start)
        return cls(*v)

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
    # comparison
    # ==========================================================================

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

    @staticmethod
    def sum_vectors(vectors):
        return Vector(* [sum(axis) for axis in zip(* vectors)])

    @staticmethod
    def dot_vectors(left, right):
        return [Vector.dot(u, v) for u, v in zip(left, right)]

    @staticmethod
    def cross_vectors(left, right):
        return [Vector.cross(u, v) for u, v in zip(left, right)]

    @staticmethod
    def angles_vectors(left, right):
        return [angles_vectors(u, v) for u, v in zip(left, right)]

    @staticmethod
    def angle_vectors(left, right):
        return [angle_vectors(u, v) for u, v in zip(left, right)]

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
    # properties
    # ==========================================================================

    @property
    def length(self):
        return length_vector(self)

    @property
    def norm(self):
        return length_vector(self)

    # ==========================================================================
    # helpers
    # ==========================================================================

    def copy(self):
        return Vector(self.x, self.y, self.z)

    # ==========================================================================
    # methods: none
    # ==========================================================================

    def unitize(self):
        l = self.length
        self.x = self.x / l
        self.y = self.y / l
        self.z = self.z / l

    def homogenise(self, w=1.0):
        self.x = self.x / w
        self.y = self.y / w
        self.z = self.z / w
        self.w = w

    def dehomogenise(self):
        self.x *= self.w
        self.y *= self.w
        self.z *= self.w

    def reverse(self):
        self.x = - self.x
        self.y = - self.y
        self.z = - self.z

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
    # methods: other
    # ==========================================================================

    def dot(self, other):
        """The dot product of this ``Vector`` and another ``Vector``.

        Parameters:
            other (tuple, list, Vector): The vector to dot.

        Returns:
            float: The dot product.
        """
        return dot_vectors(self, other)

    def cross(self, other):
        """The cross product of this ``Vector`` and another ``Vector``.

        Parameters:
            other (tuple, list, Vector): The vector to cross.

        Returns:
            Vector: The cross product.
        """
        return Vector(* cross_vectors(self, other))

    def angle(self, other):
        return angle_vectors(self, other)

    def angles(self, other):
        return angles_vectors(self, other)

    # ==========================================================================
    # methods: misc
    # ==========================================================================

    def transform(self, matrix):
        points = transform([self, ], matrix)
        self.x = points[0][0]
        self.y = points[0][1]
        self.z = points[0][2]

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

        axis = Vector(*axis)
        origin = Vector(*axis)

        sina = sin(angle)
        cosa = cos(angle)
        kxu  = axis.cross(self)
        v    = kxu * sina
        w    = axis.cross(kxu) * (1 - cosa)

        self.x += v[0] + w[0] + origin[0]
        self.y += v[1] + w[1] + origin[1]
        self.z += v[2] + w[2] + origin[2]

    def project(self):
        pass

    def reflect(self):
        pass


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    from compas.geometry import rotation_matrix

    u = Vector(1.0, 0.0, 0.0)
    v = Vector(0.0, 1.0, 0.0)

    print(Vector.sum_vectors([u, v]))

    print(u)

    print(u.dot(v))
    print(u.cross(v))

    u.rotate(pi / 2)

    print(u)

    R = rotation_matrix(- pi / 2, [0.0, 0.0, 1.0])
    u.transform(R)

    print(u)
