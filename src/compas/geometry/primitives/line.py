from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas.geometry

from compas.geometry.primitives import Primitive
from compas.geometry.primitives import Point
from compas.geometry.primitives import Vector

from compas.geometry import midpoint_point_point
from compas.geometry import intersection_line_line
from compas.geometry import intersection_line_plane
from compas.geometry import intersection_line_triangle

from compas.geometry import offset_line


class Line(Primitive):
    """A line is defined by two points.

    Parameters
    ----------
    p1 : [float, float, float] | :class:`~compas.geometry.Point`
        The first point.
    p2 : [float, float, float] | :class:`~compas.geometry.Point`
        The second point.

    Attributes
    ----------
    start : :class:`~compas.geometry.Point`
        The start point of the line.
    end : :class:`~compas.geometry.Point`
        The end point of the line.
    vector : :class:`~compas.geometry.Vector`, read-only
        A vector pointing from start to end.
    length : float, read-only
        The length of the vector from start to end.
    direction : :class:`~compas.geometry.Vector`, read-only
        A unit vector pointing from start and end.
    midpoint : :class:`~compas.geometry.Point`, read-only
        The midpoint between start and end.

    Examples
    --------
    >>> line = Line([0, 0, 0], [1, 1, 1])
    >>> line
    Line(Point(0.000, 0.000, 0.000), Point(1.000, 1.000, 1.000))
    >>> line.start
    Point(0.000, 0.000, 0.000)
    >>> line.midpoint
    Point(0.500, 0.500, 0.500)
    >>> line.length == math.sqrt(1 + 1 + 1)
    True
    >>> line.direction
    Vector(0.577, 0.577, 0.577)

    """

    __slots__ = ["_start", "_end"]

    def __init__(self, p1, p2, **kwargs):
        super(Line, self).__init__(**kwargs)
        self._start = None
        self._end = None
        self.start = p1
        self.end = p2

    # ==========================================================================
    # data
    # ==========================================================================

    @property
    def DATASCHEMA(self):
        """:class:`schema.Schema` : Schema of the data representation."""
        from schema import Schema

        return Schema({"start": Point.DATASCHEMA.fget(None), "end": Point.DATASCHEMA.fget(None)})  # type: ignore

    @property
    def JSONSCHEMANAME(self):
        """str : Name of the schema of the data representation in JSON format."""
        return "line"

    @property
    def data(self):
        """dict : The data dictionary that represents the line."""
        return {"start": self.start.data, "end": self.end.data}

    @data.setter
    def data(self, data):
        self.start = Point.from_data(data["start"])
        self.end = Point.from_data(data["end"])

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
        return cls(Point.from_data(data["start"]), Point.from_data(data["end"]))

    # ==========================================================================
    # properties
    # ==========================================================================

    @property
    def start(self):
        # type: () -> Point
        return self._start  # type: ignore

    @start.setter
    def start(self, point):
        self._start = Point(*point)

    @property
    def end(self):
        # type: () -> Point
        return self._end  # type: ignore

    @end.setter
    def end(self, point):
        self._end = Point(*point)

    @property
    def vector(self):
        # type: () -> compas.geometry.Vector
        return self.end - self.start  # type: ignore

    @property
    def length(self):
        # type: () -> float
        return self.vector.length

    @property
    def direction(self):
        # type: () -> compas.geometry.Vector
        return self.vector * (1 / self.length)

    @property
    def midpoint(self):
        # type: () -> Point
        v = self.direction * (0.5 * self.length)
        return self.start + v

    # ==========================================================================
    # customization
    # ==========================================================================

    def __repr__(self):
        return "Line({0!r}, {1!r})".format(self.start, self.end)

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
        try:
            other_start = other[0]
            other_end = other[1]
        except:  # noqa: E722
            return False
        return self.start == other_start and self.end == other_end

    # ==========================================================================
    # constructors
    # ==========================================================================

    # ==========================================================================
    # static
    # ==========================================================================

    @staticmethod
    def transform_collection(collection, X):
        """Transform a collection of Line objects.

        Parameters
        ----------
        collection : list[[point, point] | :class:`~compas.geometry.Line`]
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
        """Create a collection of transformed Line objects.

        Parameters
        ----------
        collection : list[[point, point] | :class:`~compas.geometry.Line`]
            The collection of lines.

        Returns
        -------
        list[:class:`~compas.geometry.Line`]
            The transformed lines.

        Examples
        --------
        >>> from math import radians
        >>> from compas.geometry import Vector
        >>> from compas.geometry import Point
        >>> from compas.geometry import Rotation
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
        :class:`~compas.geometry.Point`
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
        T : :class:`~compas.geometry.Transformation` | list[list[float]]
            The transformation.

        Returns
        -------
        None

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

    def intersection_with_line(self, line, tol=None, apparent=True):
        """Compute the intersection point with another line.

        Parameters
        ----------
        line : :class:`compas.geometry.Line`
            The other line.
        tol : float, optional
            Tolerance value for membership verfication.
            Defaults to the global precision setting.
        apparent : bool, optional
            If the two lines are skew, compute the apparent intersection.

        Returns
        -------
        None | :class:`compas.geometry.Point` | tuple[:class:`compas.geometry.Point`, :class:`compas.geometry.Point`]
            None if the lines are parallel.
            A point if ``apparent`` is ``True``.
            Two points if ``apparent`` is ``False``.

        """
        tol = tol or compas.precision_as_float()
        x1, x2 = intersection_line_line(self, line, tol=tol)
        if not x1 or not x2:
            return None
        if apparent:
            x = midpoint_point_point(x1, x2)
            return Point(*x)
        return Point(*x1), Point(*x2)

    def intersection_with_plane(self, plane, tol=None):
        """Compute the intersection point with another line.

        Parameters
        ----------
        plane : :class:`compas.geometry.Plane`
            The other line.
        tol : float, optional
            Tolerance value for membership verfication.
            Defaults to the global precision setting.

        Returns
        -------
        None | :class:`compas.geometry.Point`
            None if the line is parallel to the plane.
            The intersection point otherwise.

        """
        tol = tol or compas.precision_as_float()
        x = intersection_line_plane(self, plane, tol=tol)
        if not x:
            return None
        return Point(*x)

    def intersection_with_triangle(self, triangle, tol=None):
        """Compute the intersection point with another line.

        Parameters
        ----------
        plane : :class:`compas.geometry.Plane`
            The other line.
        tol : float, optional
            Tolerance value for membership verfication.
            Defaults to the global precision setting.

        Returns
        -------
        None | :class:`compas.geometry.Point`
            None if the line doesn't intersect with the triangle.
            The intersection point otherwise.

        """
        tol = tol or compas.precision_as_float()
        x = intersection_line_triangle(self, triangle, tol=tol)
        if not x:
            return None
        return Point(*x)

    def offset(self, distance, direction=None):
        """Offset the line.

        Parameters
        ----------
        distance : float
            The offset distance.
        direction : :class:`compas.geometry.Vector`, optional
            The offset direction.
            If no direction is provided, the Z-axis of the global coordinate system is used.

        Returns
        -------
        :class:`~compas.geometry.Line`

        """
        direction = direction or Vector.Zaxis()
        a, b = offset_line(self, distance=distance, normal=direction)
        return Line(a, b)
