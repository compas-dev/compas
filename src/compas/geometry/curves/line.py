from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.geometry import Frame
from compas.geometry import Point
from compas.geometry import Vector
from compas.geometry import add_vectors

from .curve import Curve


class Line(Curve):
    """A line is a curve defined by two points.

    The first point is the start point of the line.
    The second point is the end point of the line.
    The vector between the two points defines the direction of the line.
    The length of the vector is the length of the line.
    The direction vector is the unit vector of the vector between start and end.
    The parameterisation of the line is such that the start point corresponds to ``t = 0`` and the end point to ``t = 1``.

    The coordinate system of a line is always the world coordinate system (WCS).
    Transformation of a line is performed by transforming the start and end point.

    Parameters
    ----------
    start : [float, float, float] | :class:`compas.geometry.Point`
        The first point.
    end : [float, float, float] | :class:`compas.geometry.Point`
        The second point.
    name : str, optional
        The name of the line.

    Attributes
    ----------
    start : :class:`compas.geometry.Point`
        The start point of the line.
    end : :class:`compas.geometry.Point`
        The end point of the line.
    vector : :class:`compas.geometry.Vector`, read-only
        A vector pointing from start to end.
    length : float, read-only
        The length of the vector from start to end.
    direction : :class:`compas.geometry.Vector`, read-only
        A unit vector parallel to the line vector.
    midpoint : :class:`compas.geometry.Point`, read-only
        The midpoint between start and end.
    frame : :class:`compas.geometry.Frame`, read-only
        The frame of the line.
        This is alsways the world XY frame.
    transformation : :class:`compas.geometry.Transformation`, read-only
        This is always the identity transformation.

    Examples
    --------
    >>> line = Line([0, 0, 0], [1, 1, 1])
    >>> print(line.start)
    Point(x=0.000, y=0.000, z=0.000)
    >>> print(line.midpoint)
    Point(x=0.500, y=0.500, z=0.500)
    >>> line.length == line.vector.length
    True
    >>> print(line.direction)
    Vector(x=0.577, y=0.577, z=0.577)

    """

    # overwriting the __new__ method is necessary
    # to avoid triggering the plugin mechanism of the base curve class
    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    DATASCHEMA = {
        "type": "object",
        "properties": {
            "start": Point.DATASCHEMA,
            "end": Point.DATASCHEMA,
        },
        "required": ["start", "end"],
    }

    @property
    def __data__(self):
        return {"start": self.start.__data__, "end": self.end.__data__}

    def __init__(self, start, end, name=None):
        super(Line, self).__init__(name=name)
        self._point = None
        self._vector = None
        self._direction = None
        self.start = start
        self.end = end

    def __repr__(self):
        return "{0}({1!r}, {2!r})".format(
            type(self).__name__,
            self.start,
            self.end,
        )

    def __getitem__(self, key):
        if key == 0:
            return self.start
        if key == 1:
            return self.end
        raise KeyError

    def __setitem__(self, key, value):
        if key == 0:
            self.start = value
        elif key == 1:
            self.end = value
        else:
            raise KeyError

    def __iter__(self):
        return iter([self.start, self.end])

    def __len__(self):
        return 2

    def __eq__(self, other):
        try:
            return self.start == other[0] and self.end == other[1]
        except Exception:
            return False

    # ==========================================================================
    # properties
    # ==========================================================================

    @property
    def frame(self):
        return Frame.worldXY()

    @frame.setter
    def frame(self, frame):
        raise AttributeError("Setting the coordinate frame of a line is not supported.")

    @property
    def point(self):
        if not self._point:
            raise ValueError("The line has no base point.")
        return self._point

    @point.setter
    def point(self, point):
        self._point = Point(*point)

    @property
    def vector(self):
        if not self._vector:
            raise ValueError("The line has no direction vector.")
        return self._vector

    @vector.setter
    def vector(self, vector):
        self._vector = Vector(*vector)
        self._direction = None

    @property
    def length(self):
        return self.vector.length

    @property
    def direction(self):
        if not self._direction:
            self._direction = self.vector.unitized()
        return self._direction

    @property
    def start(self):
        return self.point

    @start.setter
    def start(self, point):
        self.point = point

    @property
    def end(self):
        return self.start + self.vector

    @end.setter
    def end(self, point):
        self._vector = Vector.from_start_end(self.start, point)
        self._direction = None

    @property
    def midpoint(self):
        return self.point_at(0.5)

    # ==========================================================================
    # Constructors
    # ==========================================================================

    @classmethod
    def from_point_and_vector(cls, point, vector):
        """Construct a line from a point and a vector.

        Parameters
        ----------
        point : :class:`compas.geometry.Point`
            The start point of the line.
        vector : :class:`compas.geometry.Vector`
            The vector of the line.

        Returns
        -------
        :class:`Line`
            The constructed line.

        See Also
        --------
        :meth:`Line.from_point_direction_length`

        Examples
        --------
        >>> from compas.geometry import Point, Vector
        >>> line = Line.from_point_and_vector(Point(0, 0, 0), Vector(1, 1, 1))
        >>> print(line.start)
        Point(x=0.000, y=0.000, z=0.000)
        >>> print(line.end)
        Point(x=1.000, y=1.000, z=1.000)

        """
        return cls(point, add_vectors(point, vector))

    @classmethod
    def from_point_direction_length(cls, point, direction, length):
        """Construct a line from a point, a direction and a length.

        Parameters
        ----------
        point : :class:`compas.geometry.Point`
            The start point of the line.
        direction : :class:`compas.geometry.Vector`
            The direction of the line.
        length : float
            The length of the line.

        Returns
        -------
        :class:`Line`
            The constructed line.

        See Also
        --------
        :meth:`Line.from_point_and_vector`

        Examples
        --------
        >>> from compas.geometry import Point, Vector
        >>> line = Line.from_point_direction_length(Point(0, 0, 0), Vector(1, 1, 1), 1)
        >>> print(line.start)
        Point(x=0.000, y=0.000, z=0.000)
        >>> print(line.end)
        Point(x=0.577, y=0.577, z=0.577)

        """
        direction = Vector(*direction)
        direction.unitize()
        return cls(point, add_vectors(point, direction * length))

    # ==========================================================================
    # Transformations
    # ==========================================================================

    def transform(self, T):
        """Transform this line.

        Parameters
        ----------
        T : :class:`compas.geometry.Transformation`
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
        >>> print(line.end)
        Point(x=0.000, y=1.000, z=0.000)

        """
        self.point.transform(T)
        self.vector.transform(T)

    # ==========================================================================
    # Methods
    # ==========================================================================

    def point_at(self, t):
        """Construct a point along the line at a fractional position.

        Parameters
        ----------
        t : float
            The relative position along the line as a fraction of the length of the line.
            0.0 corresponds to the start point and 1.0 corresponds to the end point.
            Numbers outside of this range are also valid and correspond to points beyond the start and end point.

        Returns
        -------
        :class:`compas.geometry.Point`
            The point at the specified position.

        See Also
        --------
        :meth:`tangent_at`

        Examples
        --------
        >>> line = Line([0, 0, 0], [1, 1, 1])
        >>> print(line.point_at(0.5))
        Point(x=0.500, y=0.500, z=0.500)

        """
        point = self.point + self.vector * t
        return point

    def point_from_start(self, distance):
        """Construct a point along the line at a distance from the start point.

        Parameters
        ----------
        distance : float
            The distance along the line from the start point towards the end point.
            If the distance is negative, the point is constructed in the opposite direction of the end point.
            If the distance is larger than the length of the line, the point is constructed beyond the end point.

        Returns
        -------
        :class:`compas.geometry.Point`
            The point at the specified distance.

        """
        point = self.point + self.direction * distance
        return point

    def point_from_end(self, distance):
        """Construct a point along the line at a distance from the end point.

        Parameters
        ----------
        distance : float
            The distance along the line from the end point towards the start point.
            If the distance is negative, the point is constructed in the opposite direction of the start point.
            If the distance is larger than the length of the line, the point is constructed beyond the start point.

        Returns
        -------
        :class:`compas.geometry.Point`
            The point at the specified distance.

        """
        point = self.end - self.direction * distance
        return point

    def closest_point(self, point, return_parameter=False):
        """Compute the closest point on the line to a given point.

        Parameters
        ----------
        point : :class:`compas.geometry.Point`
            The point.
        return_parameter : bool, optional
            Return the parameter of the closest point on the line.
            Default is ``False``.

        Returns
        -------
        :class:`compas.geometry.Point`
            The closest point on the line.
        float
            The parameter of the closest point on the line.
            Only if ``return_parameter`` is ``True``.

        """
        vector = point - self.start
        t = vector.dot(self.vector) / self.length**2
        closest = self.start + self.vector * t
        if return_parameter:
            return closest, t
        return closest

    def flip(self):
        """Flip the direction of the line.

        Returns
        -------
        None

        Examples
        --------
        >>> line = Line([0, 0, 0], [1, 2, 3])
        >>> line
        Line(Point(x=0.0, y=0.0, z=0.0), Point(x=1.0, y=2.0, z=3.0))
        >>> line.flip()
        >>> line
        Line(Point(x=1.0, y=2.0, z=3.0), Point(x=0.0, y=0.0, z=0.0))

        """
        new_vector = self.vector.inverted()
        self.start = self.end
        self.vector = new_vector

    def flipped(self):
        """Return a new line with the direction flipped.

        Returns
        -------
        :class:`Line`
            A new line.

        Examples
        --------
        >>> line = Line([0, 0, 0], [1, 2, 3])
        >>> line
        Line(Point(x=0.0, y=0.0, z=0.0), Point(x=1.0, y=2.0, z=3.0))
        >>> line.flipped()
        Line(Point(x=1.0, y=2.0, z=3.0), Point(x=0.0, y=0.0, z=0.0))

        """
        return Line(self.end, self.start)
