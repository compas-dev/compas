from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

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

    Attributes
    ----------
    data : dict
        The data representation of the line.
    start : :class:`compas.geometry.Point`
        The first point of the line.
    end : :class:`compas.geometry.Point`
        The second point of the line.
    vector : :class:`compas.geometry.Vector`
        A vector pointing from ``start`` to ``end``.
    direction : :class:`compas.geometry.Vector`
        A unit vector pointing from ``start`` to ``end``.
    midpoint : :class:`compas.geometry.Point`
        A point half way between ``start`` and ``end``.
    length : float, read-only
        The length of the line segment between ``start`` and ``end``.

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
    """

    __slots__ = ['_start', '_end']

    def __init__(self, p1, p2):
        super(Line, self).__init__()
        self._start = None
        self._end = None
        self.start = p1
        self.end = p2

    @property
    def data(self):
        """dict : The data dictionary that represents the line."""
        return {'start': list(self.start), 'end': list(self.end)}

    @data.setter
    def data(self, data):
        self.start = data['start']
        self.end = data['end']

    @property
    def start(self):
        """:class:`compas.geometry.Point` : The start point of the line."""
        return self._start

    @start.setter
    def start(self, point):
        self._start = Point(*point)

    @property
    def end(self):
        """:class:`compas.geometry.Point` : The end point of the line."""
        return self._end

    @end.setter
    def end(self, point):
        self._end = Point(*point)

    @property
    def vector(self):
        """:class:`compas.geometry.Vector` : A vector pointing from start to end."""
        return self.end - self.start

    @property
    def length(self):
        """float : The length of the vector from start to end."""
        return self.vector.length

    @property
    def direction(self):
        """:class:`compas.geometry.Vector` : A unit vector pointing from start and end."""
        return self.vector * (1 / self.length)

    @property
    def midpoint(self):
        """:class:`compas.geometry.Point` : The midpoint between start and end."""
        v = self.direction * (0.5 * self.length)
        return self.start + v

    # ==========================================================================
    # customization
    # ==========================================================================

    def __repr__(self):
        return 'Line({0}, {1})'.format(self.start, self.end)

    def __len__(self):
        return 2

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

    def __eq__(self, other):
        raise NotImplementedError

    # ==========================================================================
    # constructors
    # ==========================================================================

    @classmethod
    def from_data(cls, data):
        """Construct a frame from a data dict.

        Parameters
        ----------
        data : dict
            The data dictionary.

        Examples
        --------
        >>> line = Line.from_data({'start': [0.0, 0.0, 0.0], 'end': [1.0, 0.0, 0.0]})
        >>> line.end
        Point(1.000, 0.000, 0.000)
        """
        return cls(data['start'], data['end'])

    # ==========================================================================
    # static
    # ==========================================================================

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
        >>> from math import radians
        >>> from compas.geometry import Point
        >>> from compas.geometry import Vector
        >>> from compas.geometry import Rotation
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
        >>> from math import radians
        >>> from compas.geometry import Vector
        >>> from compas.geometry import Point
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
    # methods
    # ==========================================================================

    def point(self, t):
        """A point between start and end at a specific normalized parameter.

        Parameters
        ----------
        t : float
            The line parameter.

        Returns
        -------
        Point
            A point on the line.

        Examples
        --------
        >>> line = Line([0.0, 0.0, 0.0], [1.0, 0.0, 0.0])
        >>> line.point(0.5)
        Point(0.500, 0.000, 0.000)
        """
        if t == 0:
            return self.start
        if t == 1:
            return self.end
        v = self.direction * (t * self.length)
        return self.start + v

    def transform(self, T):
        """Transform this line.

        Parameters
        ----------
        T : :class:`compas.geometry.Transformation` or list of list
            The transformation.

        Examples
        --------
        >>> from math import radians
        >>> from compas.geometry import Rotation
        >>> line = Line([0.0, 0.0, 0.0], [1.0, 0.0, 0.0])
        >>> R = Rotation.from_axis_and_angle([0.0, 0.0, 1.0], radians(90))
        >>> line.transform(R)
        >>> line.end
        Point(0.000, 1.000, 0.000)
        """
        self.start.transform(T)
        self.end.transform(T)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    import doctest

    from math import sqrt     # noqa F401
    from math import radians  # noqa F401

    from compas.geometry import Rotation  # noqa F401
    from compas.geometry import Point     # noqa F401
    from compas.geometry import Vector    # noqa F401

    doctest.testmod(globs=globals())
