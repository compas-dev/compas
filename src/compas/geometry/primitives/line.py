from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry.transformations import transform_points
from compas.geometry.transformations import transform_vectors

from compas.geometry.primitives import Primitive
from compas.geometry.primitives import Point


__all__ = ['Line']


class Line(Primitive):
    """A line is defined by two points.

    Parameters
    ----------
    p1 : point
        The first point.
    p2 : point
        The second point.

    Examples
    --------
    >>> line = Line([0, 0, 0], [1, 1, 1])
    >>> line
    Line(Point(0.000, 0.000, 0.000), Point(1.000, 1.000, 1.000))
    >>> line.midpoint
    Point(0.500, 0.500, 0.500)
    >>> line.length == sqrt(1 + 1 + 1)
    True
    >>> line.direction
    Vector(0.577, 0.577, 0.577)

    >>> type(line.start) == Point
    True
    >>> type(line.midpoint) == Point
    True
    >>> type(line.direction) == Vector
    True

    Notes
    -----
    For more info on lines and linear equations, see [1]_.

    References
    ----------
    .. [1] Wikipedia. *Linear equation*.
           Available at: https://en.wikipedia.org/wiki/Linear_equation.

    """

    __slots__ = ['_start', '_end']

    def __init__(self, p1, p2):
        self._start = None
        self._end = None
        self.start = p1
        self.end = p2

    @staticmethod
    def transform_collection(collection, X):
        """Transform a collection of ``Line`` objects.

        Parameters
        ----------
        collection : list of compas.geometry.Line
            The collection of lines.

        Returns
        -------
        None
            The lines are modified in-place.

        Examples
        --------
        >>> R = Rotation.from_axis_and_angle(Vector.Zaxis(), radians(90))
        >>> a = Line(Point(0.0, 0.0, 0.0), Point(1.0, 0.0, 0.0))
        >>> lines = [a]
        >>> Line.transform_collection(lines, R)
        >>> b = lines[0]
        >>> b.end
        Point(0.000, 1.000, 0.000)
        >>> a is b
        True

        """
        points = [line.start for line in collection] + [line.end for line in collection]
        Point.transform_collection(points, X)

    @staticmethod
    def transformed_collection(collection, X):
        """Create a collection of transformed ``Line`` objects.

        Parameters
        ----------
        collection : list of compas.geometry.Line
            The collection of lines.

        Returns
        -------
        list of compas.geometry.Line
            The transformed lines.

        Examples
        --------
        >>> R = Rotation.from_axis_and_angle(Vector.Zaxis(), radians(90))
        >>> a = Line(Point(0.0, 0.0, 0.0), Point(1.0, 0.0, 0.0))
        >>> lines = [a]
        >>> lines = Line.transformed_collection(lines, R)
        >>> b = lines[0]
        >>> b.end
        Point(0.000, 1.000, 0.000)
        >>> a is b
        False

        """
        lines = [line.copy() for line in collection]
        Line.transform_collection(lines, X)
        return lines

    # ==========================================================================
    # factory
    # ==========================================================================

    # ==========================================================================
    # descriptors
    # ==========================================================================

    @property
    def start(self):
        """Point: the start point."""
        return self._start

    @start.setter
    def start(self, point):
        self._start = Point(*point)

    @property
    def end(self):
        """Point: the end point."""
        return self._end

    @end.setter
    def end(self, point):
        self._end = Point(*point)

    @property
    def vector(self):
        """Vector: A vector pointing from start to end."""
        return self.end - self.start

    @property
    def length(self):
        """float: The length of the vector from start to end."""
        return self.vector.length

    @property
    def direction(self):
        """Vector: A unit vector pointing from start and end."""
        return self.vector * (1 / self.length)

    @property
    def midpoint(self):
        """Point: The midpoint between start and end."""
        v = self.direction * (0.5 * self.length)
        return self.start + v

    # ==========================================================================
    # representation
    # ==========================================================================

    def __repr__(self):
        return 'Line({0}, {1})'.format(self.start, self.end)

    def __len__(self):
        return 2

    # ==========================================================================
    # access
    # ==========================================================================

    def __getitem__(self, key):
        if key == 0:
            return self.start
        if key == 1:
            return self.end
        raise KeyError

    def __setitem__(self, key, value):
        if key == 0:
            self.start = value
            return
        if key == 1:
            self.end = value
            return
        raise KeyError

    def __iter__(self):
        return iter([self.start, self.end])

    # ==========================================================================
    # comparison
    # ==========================================================================

    def __eq__(self, other):
        raise NotImplementedError

    # ==========================================================================
    # queries
    # ==========================================================================

    def point(self, t):
        """Point: The point from the start to the end at a specific normalized parameter."""

        if t < 0 or t > 1:
            return None

        if t == 0:
            return self.start

        if t == 1:
            return self.end

        v = self.direction * (t * self.length)
        return self.start + v

    # ==========================================================================
    # operators
    # ==========================================================================

    # ==========================================================================
    # inplace operators
    # ==========================================================================

    # ==========================================================================
    # helpers
    # ==========================================================================

    def copy(self):
        """Make a copy of this ``Line``.

        Returns
        -------
        Line
            The copy.

        """
        cls = type(self)
        return cls(self.start.copy(), self.end.copy())

    # ==========================================================================
    # methods
    # ==========================================================================

    # ==========================================================================
    # transformations
    # ==========================================================================

    def transform(self, matrix):
        """Transform this ``Plane`` using a given transformation matrix.

        Parameters
        ----------
        matrix : list of list
            The transformation matrix.

        """
        self.start.transform(matrix)
        self.end.transform(matrix)

    def transformed(self, matrix):
        """Return a transformed copy of this ``Line`` using a given transformation matrix.

        Parameters
        ----------
        matrix : list of list
            The transformation matrix.

        Returns
        -------
        Line
            The transformed copy.

        """
        line = self.copy()
        line.transform(matrix)
        return line


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    import doctest

    from math import sqrt
    from math import radians

    from compas.geometry import Rotation
    from compas.geometry import Point
    from compas.geometry import Vector

    doctest.testmod(globs=globals())
