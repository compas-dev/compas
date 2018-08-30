from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry.objects import Point

from compas.geometry.transformations import transform_points
from compas.geometry.transformations import transform_vectors


__all__ = ['Line']


class Line(object):
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
    >>> line.midpoint
    Point(0.500, 0.500, 0.500)
    >>> line.length
    1.73205080757
    >>> line.direction
    Vector(0.577, 0.577, 0.577, 1.000)

    >>> type(line.start)
    <class 'compas.geometry.objects.point.Point'>
    >>> type(line.midpoint)
    <class 'compas.geometry.objects.point.Point'>
    >>> type(line.direction)
    <class 'compas.geometry.objects.vector.Vector'>

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
        self.start = transform_points([self.start], matrix)[0]
        self.end = transform_points([self.end], matrix)[0]

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

    l1 = Line([0, 0, 0], [1, 1, 1])

    print(l1)

    print(type(l1.start))
    print(l1.midpoint)
    print(type(l1.midpoint))
    print(l1.length)
    print(l1.direction)
    print(type(l1.direction))
