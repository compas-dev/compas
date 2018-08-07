from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from math import sin
from math import cos
from math import sqrt
from math import pi

from compas.geometry import *

from compas.geometry import transform_points
from compas.geometry import translate_points
from compas.geometry import scale_points
from compas.geometry import rotate_points
from compas.geometry import project_points_plane
from compas.geometry import project_points_line


__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


__all__ = ['Vector', ]


class Vector(object):
    """A vector in three-dimensional space.

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
    precision : integer, optional
        The number of fractional digits used in the representation of the coordinates of the vector.
        Default is ``3``.

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

    __slots__ = ['_x', '_y', '_z', '_w', '_precision']

    def __init__(self, x, y, z, w=1.0, precision=None):
        self._x = 0.0
        self._y = 0.0
        self._z = 0.0
        self._w = 1.0
        self._precision = 3
        self.x = x
        self.y = y
        self.z = z
        self.w = w
        self.precision = precision

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
        """:obj:`float`: The X coordinate of the point."""
        return self._x

    @x.setter
    def x(self, x):
        self._x = float(x)

    @property
    def y(self):
        """:obj:`float`: The Y coordinate of the point."""
        return self._y

    @y.setter
    def y(self, y):
        self._y = float(y)

    @property
    def z(self):
        """:obj:`float`: The Z coordinate of the point."""
        return self._z

    @z.setter
    def z(self, z):
        self._z = float(z)

    @property
    def w(self):
        """:obj:`float`, optional: The homegenisation factor. Default is ``1.0``"""
        return self._w

    @w.setter
    def w(self, w):
        self._w = float(w)

    @property
    def precision(self):
        """:obj:`int`: The number of fractional digits used in the representation of the coordinates of the point."""
        return self._precision

    @precision.setter
    def precision(self, value):
        if isinstance(value, int) and value > 0:
            self._precision = value

    # ==========================================================================
    # representation
    # ==========================================================================

    def __repr__(self):
        return 'Vector({0:.{4}f}, {1:.{4}f}, {2:.{4}f}, {3:.{4}f})'.format(self.x, self.y, self.z, self.w, self.precision)

    def __len__(self):
        return 3

    # ==========================================================================
    # access
    # ==========================================================================

    def __getitem__(self, key):
        if isinstance(key, slice):
            return [self[i] for i in range(*key.indices(len(self)))]
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

    def __eq__(self, other):
        """Is this vector equal to the other vector? Two vectors are considered
        equal if their XYZ components are identical.

        Parameters
        ----------
        other : vector
            The vector to compare.

        Returns
        -------
        bool
            True if the vectors are equal.
            False otherwise.

        """
        return self.x == other[0] and self.y == other[1] and self.z == other[2]

    # ==========================================================================
    # operators
    # ==========================================================================

    def __add__(self, other):
        """Return a ``Vector`` that is the the sum of this ``Vector`` and another vector.

        Parameters
        ----------
        other : vector
            The vector to add.

        Returns
        -------
        Vector
            The resulting new ``Vector``.

        """
        return Vector(self.x + other[0], self.y + other[1], self.z + other[2])

    def __sub__(self, other):
        """Return a ``Vector`` that is the the difference between this ``Vector`` and another ``Vector``.

        Parameters
        ----------
        other : vector
            The vector to subtract.

        Returns
        -------
        Vector
            The resulting new ``Vector``.

        """
        return Vector(self.x - other[0], self.y - other[1], self.z - other[2])

    def __mul__(self, n):
        """Return a ``Vector`` that is the scaled version of this ``Vector``.

        Parameters
        ----------
        n : float
            The scaling factor.

        Returns
        -------
        Vector
            The resulting new ``Vector``.

        """
        return Vector(self.x * n, self.y * n, self.z * n)

    def __pow__(self, n):
        """Create a ``Vector`` from the components of the current ``Vector`` raised
        to the given power.

        Parameters
        ----------
        n : float
            The power.

        Returns
        -------
        Vector
            A new point with raised coordinates.

        """
        return Vector(self.x ** n, self.y ** n, self.z ** n)

    # ==========================================================================
    # in-place operators
    # ==========================================================================

    def __iadd__(self, other):
        """Add the components of the other vector to this ``Vector``.

        Parameters
        ----------
        other : vector
            The vector to add.

        """
        self.x += other[0]
        self.y += other[1]
        self.z += other[2]

    def __isub__(self, other):
        """Subtract the components of the other vector from this ``Vector``.

        Parameters
        ----------
        other : vector
            The vector to subtract.

        """
        self.x -= other[0]
        self.y -= other[1]
        self.z -= other[2]

    def __imul__(self, n):
        """Multiply the components of this ``Vector`` by the given factor.

        Parameters
        ----------
        n : float
            The multiplication factor.

        """
        self.x *= n
        self.y *= n
        self.z *= n

    def __ipow__(self, n):
        """Raise the components of this ``Vector`` to the given power.

        Parameters
        ----------
        n : float
            The power.

        """
        self.x **= n
        self.y **= n
        self.z **= n

    # ==========================================================================
    # static methods
    # ==========================================================================

    @staticmethod
    def length_vectors(vectors):
        return [length_vector(vector) for vector in vectors]

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
        """:obj:`float`: The length of this ``Vector``."""
        return length_vector(self)

    # ==========================================================================
    # helpers
    # ==========================================================================

    def copy(self):
        """Make a copy of this ``Vector``.

        Returns
        -------
        Vector
            The copy.

        """
        cls = type(self)
        return cls(self.x, self.y, self.z, self.w, self.precision)

    # ==========================================================================
    # methods
    # ==========================================================================

    def unitize(self):
        """Scale this ``Vector`` to unit length."""
        l = self.length
        self.x = self.x / l
        self.y = self.y / l
        self.z = self.z / l

    def homogenise(self, w):
        """Homogenise the components of this ``Vector`` using the given homogenisation factor.

        Parameters
        ----------
        w : float
            The homogenisation factor.

        """
        self.x = self.x / w
        self.y = self.y / w
        self.z = self.z / w
        self.w = w

    def dehomogenise(self):
        """Dehomogenise the components of this vector."""
        self.x *= self.w
        self.y *= self.w
        self.z *= self.w

    def scale(self, n):
        """Scale this ``Vector`` by a factor n.

        Parameters
        ----------
        n : float
            The scaling factor.

        """
        self.x *= n
        self.y *= n
        self.z *= n

    def dot(self, other):
        """The dot product of this ``Vector`` and another vector.

        Parameters
        ----------
        other : vector
            The other vector.

        Returns
        -------
        float
            The dot product.

        """
        return dot_vectors(self, other)

    def cross(self, other):
        """The cross product of this ``Vector`` and another vector.

        Parameters
        ----------
        other : vector
            The other vector.

        Returns
        -------
        Vector
            The cross product.

        """
        return Vector(* cross_vectors(self, other))

    def angle(self, other):
        """Compute the smallest angle between this ``Vector`` and another vector.

        Parameters
        ----------
        other : vector
            The other vector.

        Returns
        -------
        float
            The smallest angle between the two vectors.

        """
        return angle_vectors(self, other)

    def angles(self, other):
        """Compute both angles between this ``Vector`` and another vector.

        Parameters
        ----------
        other : vector
            The other vector.

        Returns
        -------
        tuple of float
            The angles between the two vectors, with the snalles angle first.

        """
        return angles_vectors(self, other)

    # ==========================================================================
    # transformations
    # ==========================================================================

    def transform(self, matrix):
        """Transform this ``Vector`` using a given transformation matrix.

        Parameters
        ----------
        matrix : list of list
            The transformation matrix.

        """
        point = transform([self, ], matrix)[0]
        self.x = point[0]
        self.y = point[1]
        self.z = point[2]

    def translate(self, vector):
        """Translate this ``Vector`` by another vector.

        Parameters
        ----------
        vector : vector
            The translation vector.

        Note
        ----
        What does it mean to translate a vector?
        Should both the start and end point be moved?
        Or is the result a new vector from the origin to the new end point?

        """
        point = translate_points([self, ], vector)[0]
        self.x = point[0]
        self.y = point[1]
        self.z = point[2]

    def scale(self, factor):
        """Scale this ``Vector`` by a given factor.

        Parameters
        ----------
        factor : float
            The scale factor.

        """
        point = scale_points([self, ], factor)[0]
        self.x = point[0]
        self.y = point[1]
        self.z = point[2]

    def rotate(self, angle, axis=None, origin=None):
        """Rotate this ``Vector`` over the given angle around the specified axis
        and origin.

        Parameters
        ----------
        angle : float
            The rotation angle in radians.
        axis : vector, optional
            The rotation axis.
            Default is the Z axis (``[0.0, 0.0, 1.0]``).
        origin : point, optional
            The origin of the rotation axis.
            Default is ``[0.0, 0.0, 0.0]``.

        """
        if axis is None:
            axis = [0.0, 0.0, 1.0]
        if origin is None:
            origin = [0.0, 0.0, 0.0]

        point = rotate_points([self, ], angle, axis, origin)[0]
        self.x = point[0]
        self.y = point[1]
        self.z = point[2]


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    from compas.geometry import matrix_from_axis_and_angle

    u = Vector(0.0, 0.0, 1.0)
    v = Vector(1.0, 0.0, 0.0)

    u.rotate(pi / 4, v)

    print(u)
