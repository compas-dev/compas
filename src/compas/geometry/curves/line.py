from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry import Point
from compas.geometry import Vector
from compas.geometry import Frame
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
        A unit vector parallel to the line vector.
    midpoint : :class:`~compas.geometry.Point`, read-only
        The midpoint between start and end.
    domain : tuple of float, read-only
        The parameterisation domain of the line.
        For a line, this is always ``[0, 1]``.
    frame : :class:`~compas.geometry.Frame`, read-only
        The frame of the line.
        This is alsways the world XY frame.
    transformation : :class:`~compas.geometry.Transformation`, read-only
        This is always the identity transformation.

    Examples
    --------
    >>> line = Line([0, 0, 0], [1, 1, 1])
    >>> line
    Line(Point(0.000, 0.000, 0.000), Point(1.000, 1.000, 1.000))
    >>> line.start
    Point(0.000, 0.000, 0.000)
    >>> line.midpoint
    Point(0.500, 0.500, 0.500)
    >>> line.length == math.sqrt(line.dx **2 + line.dy **2 + line.dz **2)
    True
    >>> line.direction
    Vector(0.577, 0.577, 0.577)

    """

    JSONSCHEMA = {
        "type": "object",
        "properties": {
            "start": Point.JSONSCHEMA,
            "end": Point.JSONSCHEMA,
        },
        "required": ["start", "end"],
    }

    # overwriting the __new__ method is necessary
    # to avoid triggering the plugin mechanism of the base curve class
    def __new__(cls, *args, **kwargs):
        curve = object.__new__(cls)
        curve.__init__(*args, **kwargs)
        return curve

    def __init__(self, start, end, **kwargs):
        super(Line, self).__init__(**kwargs)
        self._point = None
        self._vector = None
        self.start = start
        self.end = end

    # ==========================================================================
    # data
    # ==========================================================================

    @property
    def data(self):
        return {"start": self.start, "end": self.end}

    @data.setter
    def data(self, data):
        self.start = data["start"]
        self.end = data["end"]

    # ==========================================================================
    # properties
    # ==========================================================================

    @property
    def frame(self):
        return Frame.worldXY()

    @frame.setter
    def frame(self, frame):
        raise Exception("Setting the coordinate frame of a line is not supported.")

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

    @property
    def length(self):
        return self.vector.length

    @property
    def direction(self):
        return self.vector.unitized()

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

    @property
    def midpoint(self):
        return self.point_at(0.5)

    # ==========================================================================
    # Customization
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
        except Exception:
            return False
        return self.start == other_start and self.end == other_end

    # ==========================================================================
    # Constructors
    # ==========================================================================

    @classmethod
    def from_point_and_vector(cls, point, vector):
        """Construct a line from a point and a vector.

        Parameters
        ----------
        point : :class:`~compas.geometry.Point`
            The start point of the line.
        vector : :class:`~compas.geometry.Vector`
            The vector of the line.

        Returns
        -------
        :class:`Line`
            The constructed line.

        Examples
        --------
        >>> from compas.geometry import Point, Vector
        >>> line = Line.from_point_and_vector(Point(0, 0, 0), Vector(1, 1, 1))
        >>> line
        Line(Point(0.000, 0.000, 0.000), Point(1.000, 1.000, 1.000))

        """
        return cls(point, point + vector)

    @classmethod
    def from_point_direction_and_length(cls, point, direction, length):
        """Construct a line from a point, a direction and a length.

        Parameters
        ----------
        point : :class:`~compas.geometry.Point`
            The start point of the line.
        direction : :class:`~compas.geometry.Vector`
            The direction of the line.
        length : float
            The length of the line.

        Returns
        -------
        :class:`Line`
            The constructed line.

        Examples
        --------
        >>> from compas.geometry import Point, Vector
        >>> line = Line.from_point_direction_and_length(Point(0, 0, 0), Vector(1, 1, 1), 1)
        >>> line
        Line(Point(0.000, 0.000, 0.000), Point(0.577, 0.577, 0.577))

        """
        direction = Vector(*direction)
        direction.unitize()
        return cls(point, point + direction * length)

    # ==========================================================================
    # Transformations
    # ==========================================================================

    def transform(self, T):
        """Transform this line.

        Parameters
        ----------
        T : :class:`~compas.geometry.Transformation`
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
        self.point.transform(T)
        self.vector.transform(T)

    # ==========================================================================
    # Methods
    # ==========================================================================

    def point_at(self, t):
        """Construct a point at a specific location along the line.

        Parameters
        ----------
        t : float
            The location along the line.

        Returns
        -------
        :class:`~compas.geometry.Point`
            The point at the specified location.

        Examples
        --------
        >>> line = Line([0, 0, 0], [1, 1, 1])
        >>> line.point_at(0.5)
        Point(0.500, 0.500, 0.500)

        """
        point = self.point + self.vector * t
        return point

    def tangent_at(self, t):
        """Construct a tangent vector at a specific location along the line.

        Parameters
        ----------
        t : float
            The location along the line.

        Returns
        -------
        :class:`~compas.geometry.Vector`
            The tangent vector at the specified location.

        Examples
        --------
        >>> line = Line([0, 0, 0], [1, 1, 1])
        >>> line.tangent_at(0.5)
        Vector(0.577, 0.577, 0.577)

        """
        vector = self.direction
        return vector

    def closest_point(self, point, return_parameter=False):
        """Compute the closest point on the line to a given point.

        Parameters
        ----------
        point : :class:`~compas.geometry.Point`
            The point.
        return_parameter : bool, optional
            Return the parameter of the closest point on the line.
            Default is ``False``.

        Returns
        -------
        :class:`~compas.geometry.Point`
            The closest point on the line.
        float
            The parameter of the closest point on the line.
            Only if ``return_parameter`` is ``True``.

        """
        a = self.start
        vector = point - a
        direction = self.direction
        t = vector.dot(direction)
        c = a + direction * t
        if return_parameter:
            return c, t
        return c

    def offset(self, distance, **kwargs):
        """Offset a line by a distance.

        Parameters
        ----------
        line : :class:`~compas.geometry.Line`
            A line defined by two points.
        distance : float
            The offset distance as float.

        Returns
        -------
        list[point]
            The two points of the offseted line.

        Notes
        -----
        The offset direction is chosen such that if the line were along the positve
        X axis and the normal of the offset plane is along the positive Z axis, the
        offset line is in the direction of the postive Y axis.

        Depending of the backend used, additional parameters can be added as keyword arguments. (point somewhere in api, or list
        accepted arguments)

        """
        from compas.geometry import offset_line

        points = offset_line(self, distance, **kwargs)
        return Line(*points)
