from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas import PRECISION

from compas.geometry import distance_point_point
from compas.geometry import distance_point_line
from compas.geometry import distance_point_plane
from compas.geometry import is_point_on_line
from compas.geometry import is_point_on_segment
from compas.geometry import is_point_on_polyline
from compas.geometry import is_point_in_triangle
from compas.geometry import is_point_in_circle
from compas.geometry import is_polygon_convex_xy
from compas.geometry import is_point_in_polygon_xy
from compas.geometry import is_point_in_convex_polygon_xy
from compas.geometry import transform_points

from compas.geometry._primitives import Primitive
from compas.geometry._primitives import Vector


__all__ = ['Point']


class Point(Primitive):
    """A point is defined by XYZ coordinates.

    Parameters
    ----------
    x : float
        The X coordinate of the point.
    y : float
        The Y coordinate of the point.
    z : float, optional
        The Z coordinate of the point.
        Default is ``0.0``.

    Attributes
    ----------
    data : dict
        The data representation of the point.
    x : float
        The X coordinate of the point.
    y : float
        The Y coordinate of the point.
    z : float
        The Z coordinate of the point.

    Notes
    -----
    A ``Point`` object supports direct access to its xyz coordinates through
    the dot notation, as well list-style access using indices. Indexed
    access is implemented such that the ``Point`` behaves like a circular
    list [1]_.

    References
    ----------
    .. [1] Stack Overflow. *Pythonic Circular List*.
           Available at: https://stackoverflow.com/questions/8951020/pythonic-circular-list.

    Examples
    --------
    >>> p1 = Point(1, 2, 3)
    >>> p2 = Point(4, 5, 6)

    The XYZ coordinates of point objects can be accessed as object attributes or by trating the points as lists.

    >>> p1.x
    1.0
    >>> p1.y
    2.0
    >>> p1.z
    3.0
    >>> p1[0]
    1.0
    >>> p1[1]
    2.0
    >>> p1[2]
    3.0

    Point objects support basic arithmetic operations.

    >>> p1 + p2
    Point(5.000, 7.000, 9.000)
    >>> p1 * 2
    Point(2.000, 4.000, 6.000)
    >>> p1 ** 2
    Point(1.000, 4.000, 9.000)
    >>> p1
    Point(1.000, 2.000, 3.000)

    Points and lists can be used interchangeably.

    >>> p1 + [4, 5, 6]
    Point(5.000, 7.000, 9.000)

    Arithmetic operations can also be applied to modify a point object in-place.

    >>> p1 += p2
    >>> p1 *= 2
    >>> p1 **= 2
    >>> p1
    Point(100.000, 196.000, 324.000)
    """

    __module__ = "compas.geometry"

    __slots__ = ['_x', '_y', '_z']

    def __init__(self, x, y, z=0.0):
        self._x = 0.0
        self._y = 0.0
        self._z = 0.0
        self.x = x
        self.y = y
        self.z = z

    @property
    def data(self):
        """dict : The data representing the point."""
        return list(self)

    @data.setter
    def data(self, data):
        self.x = data[0]
        self.y = data[1]
        self.z = data[2]

    @property
    def x(self):
        """float : The X coordinate of the point."""
        return self._x

    @x.setter
    def x(self, x):
        self._x = float(x)

    @property
    def y(self):
        """float : The Y coordinate of the point."""
        return self._y

    @y.setter
    def y(self, y):
        self._y = float(y)

    @property
    def z(self):
        """float : The Z coordinate of the point."""
        return self._z

    @z.setter
    def z(self, z):
        self._z = float(z)

    # ==========================================================================
    # customization
    # ==========================================================================

    def __repr__(self):
        return 'Point({0:.{3}f}, {1:.{3}f}, {2:.{3}f})'.format(self.x, self.y, self.z, PRECISION[:1])

    def __len__(self):
        return 3

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

    def __eq__(self, other):
        """Is this point equal to the other point?

        Two points are considered equal if their XYZ coordinates are identical.

        Parameters
        ----------
        other : :class:`compas.geometry.Point` or list
            The point to compare.

        Returns
        -------
        bool
            True if the points are equal.
            False otherwise.
        """
        return self.x == other[0] and self.y == other[1] and self.z == other[2]

    def __add__(self, other):
        """Return a point that is the sum of this point and another point.

        Parameters
        ----------
        other : :class:`compas.geometry.Point` or list
            The point to add.

        Returns
        -------
        :class:`compas.geometry.Point`
            The resulting new point.
        """
        return Point(self.x + other[0], self.y + other[1], self.z + other[2])

    def __sub__(self, other):
        """Return a vector` that is the the difference between this point
        and another point.

        Parameters
        ----------
        other : :class:`compas.geometry.Point` or list
            The point to subtract.

        Returns
        -------
        :class:`compas.geometry.Vector`
            A vector from other to self.
        """
        x = self.x - other[0]
        y = self.y - other[1]
        z = self.z - other[2]
        return Vector(x, y, z)

    def __mul__(self, n):
        """Create a point from the coordinates of the current point multiplied
        by the given factor.

        Parameters
        ----------
        n : float
            The multiplication factor.

        Returns
        -------
        :class:`compas.geometry.Point`
            The resulting new point.
        """
        return Point(n * self.x, n * self.y, n * self.z)

    def __truediv__(self, n):
        """Create a point from the coordinates of the current point
        divided by the given factor.

        Parameters
        ----------
        n : float
            The multiplication factor.

        Returns
        -------
        :class:`compas.geometry.Point`
            The resulting new point.
        """
        return Point(self.x / n, self.y / n, self.z / n)

    def __pow__(self, n):
        """Create a point from the coordinates of the current point raised
        to the given power.

        Parameters
        ----------
        n : float
            The power.

        Returns
        -------
        :class:`compas.geometry.Point`
            A new point with raised coordinates.
        """
        return Point(self.x ** n, self.y ** n, self.z ** n)

    def __iadd__(self, other):
        """Add the coordinates of the other point to this point.

        Parameters
        ----------
        other : :class:`compas.geometry.Point` or list
            The point to add.
        """
        self.x += other[0]
        self.y += other[1]
        self.z += other[2]
        return self

    def __isub__(self, other):
        """Subtract the coordinates of the other point from this point.

        Parameters
        ----------
        other : :class:`compas.geometry.Point` or list
            The point to subtract.
        """
        self.x -= other[0]
        self.y -= other[1]
        self.z -= other[2]
        return self

    def __imul__(self, n):
        """Multiply the coordinates of this point by the given factor.

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
        """Divide the coordinates of this point by the given factor.

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
        """Raise the coordinates of this point to the given power.

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
    # static
    # ==========================================================================

    @classmethod
    def from_data(cls, data):
        """Construct a point from a data dict.

        Parameters
        ----------
        data : dict
            The data dictionary.

        Returns
        -------
        :class:`compas.geometry.Point`
            The constructed point.

        Examples
        --------
        >>> point = Point.from_data([0.0, 0.0, 0.0])
        >>> point
        Point(0.000, 0.000, 0.000)
        """
        return cls(*data)

    @staticmethod
    def transform_collection(collection, X):
        """Transform a collection of points.

        Parameters
        ----------
        collection : list of :class:`compas.geometry.Point`
            The collection of points.

        Returns
        -------
        None
            The points are modified in-place.

        Examples
        --------
        >>> T = Translation([1.0, 2.0, 3.0])
        >>> a = Point(0.0, 0.0, 0.0)
        >>> points = [a]
        >>> Point.transform_collection(points, T)
        >>> b = points[0]
        >>> b
        Point(1.000, 2.000, 3.000)
        >>> a is b
        True
        """
        data = transform_points(collection, X)
        for point, xyz in zip(collection, data):
            point.x = xyz[0]
            point.y = xyz[1]
            point.z = xyz[2]

    @staticmethod
    def transformed_collection(collection, X):
        """Create a collection of transformed points.

        Parameters
        ----------
        collection : list of :class:`compas.geometry.Point`
            The collection of points.

        Returns
        -------
        list of :class:`compas.geometry.Point`
            The transformed points.

        Examples
        --------
        >>> T = Translation([1.0, 2.0, 3.0])
        >>> a = Point(0.0, 0.0, 0.0)
        >>> points = [a]
        >>> points = Point.transformed_collection(points, T)
        >>> b = points[0]
        >>> b
        Point(1.000, 2.000, 3.000)
        >>> a is b
        False
        """
        points = [point.copy() for point in collection]
        Point.transform_collection(points, X)
        return points

    # ==========================================================================
    # helpers
    # ==========================================================================

    def update(self, data):
        """Update the coordinates of this point.

        Parameters
        ----------
        data : list
            New XYZ coordinates.

        Examples
        --------
        >>> point = Point(0.0, 0.0, 0.0)
        >>> point.update([1.0, 1.0, 1.0])
        >>> point
        Point(1.000, 1.000, 1.000)
        """
        self.x = data[0]
        self.y = data[1]
        self.z = data[2]

    def copy(self):
        """Make a copy of this point.

        Returns
        -------
        :class:`compas.geometry.Point`
            The copy.

        Examples
        --------
        >>> a = Point(0.0, 0.0, 0.0)
        >>> b = a.copy()
        >>> b[0] += 1
        >>> a == b
        False
        """
        cls = type(self)
        return cls(self.x, self.y, self.z)

    # ==========================================================================
    # methods
    # ==========================================================================

    def distance_to_point(self, point):
        """Compute the distance to another point.

        Parameters
        ----------
        point : :class:`compas.geometry.Point` or list
            The other point.

        Returns
        -------
        float
            The distance.

        Examples
        --------
        >>> a = Point(0.0, 0.0, 0.0)
        >>> b = Point(1.0, 0.0, 0.0)
        >>> a.distance_to_point(b)
        1.0
        """
        return distance_point_point(self, point)

    def distance_to_line(self, line):
        """Compute the distance to a line.

        Parameters
        ----------
        line : :class:`compas.geometry.Line` or tuple of points.
            The line.

        Returns
        -------
        float
            The distance.

        Examples
        --------
        >>> from compas.geometry import Line
        >>> point = Point(0.0, 0.0, 0.0)
        >>> line = Line(Point(1.0, 0.0, 0.0), Point(1.0, 1.0, 0.0))
        >>> point.distance_to_line(line)
        1.0
        """
        return distance_point_line(self, line)

    def distance_to_plane(self, plane):
        """Compute the distance to a plane.

        Parameters
        ----------
        plane : :class:`compas.geometry.Plane` or tuple of point and normal
            The plane.

        Returns
        -------
        float
            The distance.

        Examples
        --------
        >>> from compas.geometry import Plane
        >>> from compas.geometry import Vector
        >>> point = Point(0.0, 0.0, 0.0)
        >>> plane = Plane(Point(1.0, 0.0, 0.0), Vector(1.0, 0.0, 0.0))
        >>> point.distance_to_plane(plane)
        1.0
        """
        return distance_point_plane(self, plane)

    def on_line(self, line):
        """Determine if the point lies on the given line.

        Parameters
        ----------
        line : :class:`compas.geometry.Line` or tuple of points.
            The line.

        Returns
        -------
        bool
            True, if the point lies on the line.
            False, otherwise.

        Examples
        --------
        >>> from compas.geometry import Line
        >>> line = Line(Point(1.0, 0.0, 0.0), Point(1.0, 1.0, 0.0))
        >>> point = line.point(1.5)
        >>> point.on_line(line)
        True
        """
        return is_point_on_line(self, line)

    def on_segment(self, segment):
        """Determine if the point lies on the given segment.

        Parameters
        ----------
        segment : :class:`compas.geometry.Line` or tuple of points.
            The segment.

        Returns
        -------
        bool
            True, if the point lies on the segment.
            False, otherwise.

        Examples
        --------
        >>> from compas.geometry import Line
        >>> line = Line(Point(1.0, 0.0, 0.0), Point(1.0, 1.0, 0.0))
        >>> point = line.point(1.5)
        >>> point.on_segment(line)
        False
        """
        return is_point_on_segment(self, segment)

    def on_polyline(self, polyline):
        """Determine if the point lies on the given polyline.

        Parameters
        ----------
        polyline : :class:`compas.geometry.Polyline` or list of points.
            The polyline.

        Returns
        -------
        bool
            True, if the point lies on the polyline.
            False, otherwise.

        Examples
        --------
        >>> from compas.geometry import Polyline
        >>> poly = Polyline([Point(0.0, 0.0, 0.0), Point(1.0, 0.0, 0.0), Point(2.0, 0.0, 0.0)])
        >>> point = poly.point(0.5)
        >>> point.on_polyline(poly)
        True
        """
        return is_point_on_polyline(self, polyline)

    def on_circle(self, circle):
        """Determine if the point lies on the given circle.

        Parameters
        ----------
        circle : :class:`compas.geometry.Circle` or tuple of plane and radius.
            The circle.

        Returns
        -------
        bool
            True, if the point lies on the circle.
            False, otherwise.
        """
        raise NotImplementedError

    def in_triangle(self, triangle):
        """Determine if the point lies inside the given triangle.

        Parameters
        ----------
        triangle : :class:`compas.geometry.Polygon` or list of three points.
            The triangle.

        Returns
        -------
        bool
            True, if the point lies in the triangle.
            False, otherwise.

        Examples
        --------
        >>> from compas.geometry import Polygon
        >>> tri = Polygon([Point(0.0, 0.0, 0.0), Point(1.0, 0.0, 0.0), Point(0.5, 1.0, 0.0)])
        >>> point = Point(0.5, 0.5, 0.0)
        >>> point.in_triangle(tri)
        True
        """
        return is_point_in_triangle(self, triangle)

    def in_polygon(self, polygon):
        """Determine if the point lies inside the given polygon.

        Parameters
        ----------
        polygon : :class:`compas.geometry.Polygon` or list of points.
            The polygon.

        Returns
        -------
        bool
            True, if the point lies in the polygon.
            False, otherwise.

        Examples
        --------
        >>> from compas.geometry import Polygon
        >>> poly = Polygon([Point(0.0, 0.0, 0.0), Point(1.0, 0.0, 0.0), Point(1.0, 1.0, 0.0), Point(0.0, 1.0, 0.0)])
        >>> point = Point(0.5, 0.5, 0.0)
        >>> point.in_polygon(poly)
        True
        """
        if is_polygon_convex_xy(polygon):
            return is_point_in_convex_polygon_xy(self, polygon)
        return is_point_in_polygon_xy(self, polygon)

    def in_circle(self, circle):
        """Determine if the point lies inside the given circle.

        Parameters
        ----------
        circle : :class:`compas.geometry.Circle` or tuple of plane and radius.
            The circle.

        Returns
        -------
        bool
            True, if the point lies inside the circle.
            False, otherwise.

        Examples
        --------
        >>> from compas.geometry import Vector
        >>> from compas.geometry import Plane
        >>> from compas.geometry import Circle
        >>> circle = Circle(Plane(Point(0.0, 0.0, 0.0), Vector(0.0, 0.0, 1.0)), 1.0)
        >>> point = Point(0.5, 0.0, 0.0)
        >>> point.in_circle(circle)
        True
        """
        return is_point_in_circle(self, circle)

    def in_polyhedron(self, polyhedron):
        """Determine if the point lies inside the given polyhedron.

        Parameters
        ----------
        polyhedron : :class:`compas.geometry.Polyhedron` or tuple of vertices and faces.
            The polyhedron.

        Returns
        -------
        bool
            True, if the point lies on the polyline.
            False, otherwise.
        """
        raise NotImplementedError

    def transform(self, T):
        """Transform this point.

        Parameters
        ----------
        T : :class:`compas.geometry.Transformation` or list of list
            The transformation matrix.

        Examples
        --------
        >>> from compas.geometry import Translation
        >>> point = Point(0.0, 0.0, 0.0)
        >>> T = Translation([1.0, 1.0, 1.0])
        >>> point.transform(T)
        >>> point.x == 1.0
        True
        """
        point = transform_points([self], T)[0]
        self.x = point[0]
        self.y = point[1]
        self.z = point[2]

    def transformed(self, T):
        """Return a transformed copy of this point.

        Parameters
        ----------
        T : :class:`compas.geometry.Transformation` or list of list
            The transformation matrix.

        Returns
        -------
        :class:`compas.geometry.Point`
            The transformed copy.

        Examples
        --------
        >>> from compas.geometry import Translation
        >>> a = Point(0.0, 0.0, 0.0)
        >>> T = Translation([1.0, 1.0, 1.0])
        >>> b = a.transformed(T)
        >>> a == b
        False
        """
        point = self.copy()
        point.transform(T)
        return point


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    import doctest

    from compas.geometry import Translation  # noqa F401

    doctest.testmod(globs=globals())
