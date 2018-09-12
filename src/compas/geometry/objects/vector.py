from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from math import sin
from math import cos
from math import sqrt
from math import pi

from compas.geometry.basic import length_vector
from compas.geometry.basic import cross_vectors
from compas.geometry.basic import subtract_vectors
from compas.geometry.angles import angle_vectors

from compas.geometry.transformations import transform_vectors


__all__ = ['Vector']


class Vector(object):
    """A vector is defined by XYZ components and a homogenisation factor.

    Parameters
    ----------
    x : float
        The X component of the vector.
    y : float
        The Y component of the vector.
    z : float
        The Z component of the vector.
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

    __slots__ = ['_x', '_y', '_z', '_precision']

    def __init__(self, x, y, z, precision=None):
        self._x = 0.0
        self._y = 0.0
        self._z = 0.0
        self._precision = 3
        self.x = x
        self.y = y
        self.z = z
        self.precision = precision

    # ==========================================================================
    # factory
    # ==========================================================================

    @classmethod
    def from_start_end(cls, start, end):
        """Construct a ``Vector`` from start and end points.

        Parameters
        ----------
        start : point
            The start point.
        end : point
            The end point.

        Returns
        -------
        Vector
            The vector from start to end.

        """
        v = subtract_vectors(end, start)
        return cls(*v)

    # ==========================================================================
    # descriptors
    # ==========================================================================

    @property
    def x(self):
        """float: The X coordinate of the point."""
        return self._x

    @x.setter
    def x(self, x):
        self._x = float(x)

    @property
    def y(self):
        """float: The Y coordinate of the point."""
        return self._y

    @y.setter
    def y(self, y):
        self._y = float(y)

    @property
    def z(self):
        """float: The Z coordinate of the point."""
        return self._z

    @z.setter
    def z(self, z):
        self._z = float(z)

    @property
    def precision(self):
        """int: The number of fractional digits used in the representation of the coordinates of the point."""
        return self._precision

    @precision.setter
    def precision(self, value):
        if isinstance(value, int) and value > 0:
            self._precision = value

    # ==========================================================================
    # representation
    # ==========================================================================

    def __repr__(self):
        return 'Vector({0:.{3}f}, {1:.{3}f}, {2:.{3}f})'.format(self.x, self.y, self.z, self.precision)

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

    def __truediv__(self, n):
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
        return Vector(self.x / n, self.y / n, self.z / n)

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
        return self

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
        return self

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
        return self

    def __itruediv__(self, n):
        """Divide the components of this ``Vector`` by the given factor.

        Parameters
        ----------
        n : float
            The multiplication factor.

        """
        self.x /= n
        self.y /= n
        self.z /= n
        return self

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
        return self

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
    def orthonormalize_vectors(vectors):
        pass

    # ==========================================================================
    # properties
    # ==========================================================================

    @property
    def length(self):
        """float: The length of this ``Vector``."""
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
        return cls(self.x, self.y, self.z, self.precision)

    # ==========================================================================
    # methods
    # ==========================================================================

    def unitize(self):
        """Scale this ``Vector`` to unit length."""
        l = self.length
        self.x = self.x / l
        self.y = self.y / l
        self.z = self.z / l

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
        point = transform_vectors([self], matrix)[0]
        self.x = point[0]
        self.y = point[1]
        self.z = point[2]

    def transformed(self, matrix):
        """Return a transformed copy of this ``Vector`` using a given transformation matrix.

        Parameters
        ----------
        matrix : list of list
            The transformation matrix.

        Returns
        -------
        Vector
            The transformed copy.

        """
        vector = self.copy()
        vector.transform(matrix)
        return vector


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    from compas.geometry import matrix_from_axis_and_angle

    u = Vector(0.0, 0.0, 1.0)
    v = Vector(1.0, 0.0, 0.0)

    print(u.angle(v))
    print(3.14159 / 2)

    w = Vector.from_start_end(u, v)

    print(w)

    M = matrix_from_axis_and_angle(v, pi / 4)

    u.transform(M)

    print(u)
