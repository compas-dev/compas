from compas.geometry.objects.point import Point


__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


class Line(object):
    r"""A line object is defined by two points in three-dimensional space.

    Parameters:
        p1 (tuple, list, Point): The xyz coordinates of the first point.
        p2 (tuple, list, Point): The xyz coordinates of the second point.

    Attributes:
        start (Point): The start point.
        end (Point): The end point.
        length (float): (**read-only**) The length of the line between start and end.
        midpoint (Point): (**read-only**) The midpoint between start and end.
        direction (Vector): (**read-only**) A unit vector pointing from start to end.

    Note:
        For convenience, this class implements the following *magic* methods:

        * ``__repr__``
        * ``__len__``
        * ``__getitem__``
        * ``__setitem__``
        * ``__iter__``
        * ``__mul__``
        * ``__imul__``

    Examples:
        >>> line = Line([0,0,0], [1,1,1])
        >>> line.midpoint
        [0.5, 0.5, 0.0]
        >>> line.length
        1.73205080757
        >>> line.direction
        [0.57735026919, 0.57735026919, 0.57735026919]

        >>> type(line.start)
        <class 'point.Point'>
        >>> type(line.midpoint)
        <class 'point.Point'>
        >>> type(line.direction)
        <class 'vector.Vector'>

    References:
        https://en.wikipedia.org/wiki/Linear_equation


    """
    def __init__(self, p1, p2):
        self.start = Point(* p1)
        self.end = Point(* p2)

    def __repr__(self):
        return '({0}, {1})'.format(self.start, self.end)

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
            self.start = Point(value)
            return
        if key == 1:
            self.end = Point(value)
            return
        raise KeyError

    def __iter__(self):
        return iter([self.start, self.end])

    def __mul__(self, n):
        """Create a line with the same start point and direction, but scaled
        length.

        Parameters:
            n (int, float): The scaling factor.

        Returns:
            Line: A line with the same start point and direction, but scaled length.
        """
        v = self.direction * (n * self.length)
        return Line(self.start, self.start + v)

    def __imul__(self, n):
        v = self.direction * (n * self.length)
        self.end = self.start + v
        return self

    # --------------------------------------------------------------------------
    # descriptors
    # --------------------------------------------------------------------------

    @property
    def vector(self):
        """A vector pointing from start to end.

        Returns:
            Vector: The vector.
        """
        return self.end - self.start

    @property
    def length(self):
        """The length of the vector from start to end.

        Returns:
            float: The length.
        """
        return self.vector.length

    @property
    def midpoint(self):
        """The midpoint between start and end.

        Returns:
            Point: The midpoint.
        """
        v = self.direction * (0.5 * self.length)
        return self.start + v

    @property
    def direction(self):
        """A unit vector pointing from start and end.

        Returns:
            Vector: The direction.
        """
        return self.vector * (1 / self.length)

    # --------------------------------------------------------------------------
    # transformations
    # --------------------------------------------------------------------------

    def translate(self, vector):
        """Translate the line by a vector."""
        self.start.translate(vector)
        self.end.translate(vector)

    def rotate(self, angle, origin=None):
        """Rotate the line around the origin, or around a specified origin."""
        if not origin:
            origin = [0, 0, 0]
        origin = Point(origin)

    def scale(self, n):
        """Increase the distance between start and end by a factor n, while
        keeping the start point fixed.

        Parameters:
            n (int, float): The scaling factor.

        Note:
            This is an alias for self \*= n
        """
        self *= n


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':

    l1 = Line([0, 0, 0], [1, 1, 1])

    print(type(l1.start))
    print(l1.midpoint)
    print(type(l1.midpoint))
    print(l1.length)
    print(l1.direction)
    print(type(l1.direction))

    l2 = l1 * 2
    print(l2.start)
    print(l2.end)
    print(l1.end)
    l1 *= 2
    print(l1.end)
