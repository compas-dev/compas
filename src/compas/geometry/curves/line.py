from typing import Iterator
from typing import Literal
from typing import Optional
from typing import Union
from typing import overload

from typing_extensions import Self

from compas._typing import Coordinates
from compas._typing import CoordinateType
from compas.geometry import Frame
from compas.geometry import Point
from compas.geometry import Vector
from compas.linalg.vectors import add_vectors

from .._typing import TransformationType
from .curve import Curve


class Line(Curve):
    """A line is a curve defined by two points.

    The first point is the start point of the line.
    The second point is the end point of the line.
    The vector between the two points defines the direction of the line.
    The length of the vector is the length of the line.
    The direction vector is the unit vector of the vector between start and end.
    The parameterisation of the line is such that the start point corresponds
    to `t = 0` and the end point to `t = 1`.

    The coordinate system of a line is always the world coordinate system (WCS).
    Transformation of a line is performed by transforming the start and end point.

    Parameters
    ----------
    start
        The first point.
    end
        The second point.
    name
        The name of the line.

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

    A line behaves as a two-item sequence containing its start and end points.

    >>> len(line)
    2
    >>> list(line) == [line.start, line.end]
    True
    >>> line[0] = [1, 0, 0]
    >>> line[1] = [2, 0, 0]
    >>> line == [[1, 0, 0], [2, 0, 0]]
    True

    Lines can also be constructed from a point and vector, or from a point,
    direction, and length.

    >>> Line.from_point_and_vector([0, 0, 0], [1, 0, 0]) == Line([0, 0, 0], [1, 0, 0])
    True
    >>> Line.from_point_direction_length([0, 0, 0], [1, 0, 0], 2) == Line([0, 0, 0], [2, 0, 0])
    True

    """

    # overwriting the __new__ method is necessary
    # to avoid triggering the plugin mechanism of the base curve class
    def __new__(cls, *args: object, **kwargs: object) -> Self:
        return object.__new__(cls)

    @property
    def __data__(self) -> dict[str, list[float]]:
        """The data representation of the line."""
        return {"start": self.start.__data__, "end": self.end.__data__}

    def __init__(self, start: CoordinateType, end: CoordinateType, name: Optional[str] = None) -> None:
        super().__init__(name=name)
        self._point: Optional[Point] = None
        self._vector: Optional[Vector] = None
        self._direction: Optional[Vector] = None
        self.start = start
        self.end = end

    def __repr__(self) -> str:
        return "{0}({1!r}, {2!r})".format(
            type(self).__name__,
            self.start,
            self.end,
        )

    def __getitem__(self, key: int) -> Point:
        if key == 0:
            return self.start
        if key == 1:
            return self.end
        raise KeyError

    def __setitem__(self, key: int, value: CoordinateType) -> None:
        if key == 0:
            self.start = value
        elif key == 1:
            self.end = value
        else:
            raise KeyError

    def __iter__(self) -> Iterator[Point]:
        return iter([self.start, self.end])

    def __len__(self) -> int:
        return 2

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Coordinates):
            return False
        if len(other) != 2:
            return False
        return self.start == other[0] and self.end == other[1]

    # ==========================================================================
    # properties
    # ==========================================================================

    @property
    def frame(self) -> Frame:
        """The world XY frame.

        Notes
        -----
        The frame of a line is fixed. Assigning a frame raises `AttributeError`.

        Examples
        --------
        >>> line = Line([0, 0, 0], [1, 0, 0])
        >>> line.frame == Frame.worldXY()
        True

        """
        return Frame.worldXY()

    @frame.setter
    def frame(self, frame: object) -> None:
        raise AttributeError("Setting the coordinate frame of a line is not supported.")

    @property
    def point(self) -> Point:
        """The base point of the line.

        Notes
        -----
        Assigning a `Point` or three-component coordinate sequence creates an
        independent `Point` with the same coordinates. The line vector is
        retained, so changing the base point translates both endpoints.

        Examples
        --------
        >>> source = Point(1, 2, 3)
        >>> line = Line([0, 0, 0], [1, 0, 0])
        >>> line.point = source
        >>> line.point == source and line.point is not source
        True
        >>> source.x = 10
        >>> line.point == [1, 2, 3]
        True
        >>> line.end == [2, 2, 3]
        True

        """
        if not self._point:
            raise ValueError("The line has no base point.")
        return self._point

    @point.setter
    def point(self, point: CoordinateType) -> None:
        self._point = Point(point[0], point[1], point[2])

    @property
    def vector(self) -> Vector:
        """The vector from the start point to the end point.

        Notes
        -----
        Assigning a `Vector` or three-component coordinate sequence creates an
        independent `Vector` with the same components. The cached direction is
        invalidated and recomputed when next requested.

        Examples
        --------
        >>> source = Vector(2, 0, 0)
        >>> line = Line([0, 0, 0], [1, 0, 0])
        >>> previous_direction = line.direction
        >>> line.vector = source
        >>> line.vector == source and line.vector is not source
        True
        >>> line.direction is not previous_direction
        True
        >>> line.end == [2, 0, 0]
        True

        """
        if not self._vector:
            raise ValueError("The line has no direction vector.")
        return self._vector

    @vector.setter
    def vector(self, vector: CoordinateType) -> None:
        self._vector = Vector(vector[0], vector[1], vector[2])
        self._direction = None

    @property
    def length(self) -> float:
        """The distance from the start point to the end point.

        Examples
        --------
        >>> Line([0, 0, 0], [3, 4, 0]).length
        5.0

        """
        return self.vector.length

    @property
    def direction(self) -> Vector:
        """The unit vector pointing from the start point to the end point.

        Notes
        -----
        The direction is computed on first access and cached until the line
        vector changes.

        Raises
        ------
        ZeroDivisionError
            If the start and end points coincide.

        Examples
        --------
        >>> line = Line([0, 0, 0], [2, 0, 0])
        >>> line.direction == [1, 0, 0]
        True
        >>> line.direction is line.direction
        True

        """
        if not self._direction:
            self._direction = self.vector.unitized()
        return self._direction

    @property
    def start(self) -> Point:
        """The start point of the line.

        Notes
        -----
        Assignment has the same copying behavior as `Line.point`. The line
        vector is retained, so assigning the start point also moves the end
        point.

        Examples
        --------
        >>> line = Line([0, 0, 0], [1, 0, 0])
        >>> line.start = [1, 2, 3]
        >>> line.start == [1, 2, 3]
        True
        >>> line.end == [2, 2, 3]
        True

        """
        return self.point

    @start.setter
    def start(self, point: CoordinateType) -> None:
        self.point = point

    @property
    def end(self) -> Point:
        """The end point of the line.

        Notes
        -----
        Assigning a `Point` or three-component coordinate sequence recomputes
        the line vector from the current start point. The assigned object is
        not retained.

        Examples
        --------
        >>> source = Point(2, 3, 4)
        >>> line = Line([0, 0, 0], [1, 0, 0])
        >>> line.end = source
        >>> line.end == source and line.end is not source
        True
        >>> line.vector == [2, 3, 4]
        True

        """
        return self.start + self.vector

    @end.setter
    def end(self, point: CoordinateType) -> None:
        end = Point(point[0], point[1], point[2])
        self._vector = Vector.from_start_end(self.start, end)
        self._direction = None

    @property
    def midpoint(self) -> Point:
        """The point halfway between the start point and the end point.

        Examples
        --------
        >>> Line([0, 0, 0], [2, 4, 6]).midpoint == [1, 2, 3]
        True

        """
        return self.point_at(0.5)

    # ==========================================================================
    # Constructors
    # ==========================================================================

    @classmethod
    def from_point_and_vector(cls, point: CoordinateType, vector: CoordinateType) -> Self:
        """Construct a line from a point and a vector.

        Parameters
        ----------
        point
            The start point of the line.
        vector
            The vector of the line.

        Returns
        -------
        Line
            The constructed line.

        See Also
        --------
        [`Line.from_point_direction_length`][compas.geometry.Line.from_point_direction_length]

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
    def from_point_direction_length(cls, point: CoordinateType, direction: CoordinateType, length: float) -> Self:
        """Construct a line from a point, a direction and a length.

        Parameters
        ----------
        point
            The start point of the line.
        direction
            The direction of the line.
        length
            The length of the line.

        Returns
        -------
        Line
            The constructed line.

        See Also
        --------
        [`Line.from_point_and_vector`][compas.geometry.Line.from_point_and_vector]

        Examples
        --------
        >>> from compas.geometry import Point, Vector
        >>> line = Line.from_point_direction_length(Point(0, 0, 0), Vector(1, 1, 1), 1)
        >>> print(line.start)
        Point(x=0.000, y=0.000, z=0.000)
        >>> print(line.end)
        Point(x=0.577, y=0.577, z=0.577)

        """
        direction = Vector(direction[0], direction[1], direction[2])
        direction.unitize()
        return cls(point, add_vectors(point, direction * length))

    # ==========================================================================
    # Transformations
    # ==========================================================================

    def transform(self, transformation: TransformationType) -> None:
        """Transform this line.

        Parameters
        ----------
        transformation
            The transformation.

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
        self.point.transform(transformation)
        self.vector.transform(transformation)

    # ==========================================================================
    # Methods
    # ==========================================================================

    def point_at(self, t: float) -> Point:
        """Construct a point along the line at a fractional position.

        Parameters
        ----------
        t
            The relative position along the line as a fraction of the length of the line.
            0.0 corresponds to the start point and 1.0 corresponds to the end point.
            Numbers outside of this range are also valid and correspond to points beyond the start and end point.

        Returns
        -------
        Point
            The point at the specified position.

        See Also
        --------
        [`Curve.tangent_at`][compas.geometry.Curve.tangent_at]

        Examples
        --------
        >>> line = Line([0, 0, 0], [1, 1, 1])
        >>> print(line.point_at(0.5))
        Point(x=0.500, y=0.500, z=0.500)

        """
        point = self.point + self.vector * t
        return point

    def point_from_start(self, distance: float) -> Point:
        """Construct a point along the line at a distance from the start point.

        Parameters
        ----------
        distance
            The distance along the line from the start point towards the end point.
            If the distance is negative, the point is constructed in the opposite direction of the end point.
            If the distance is larger than the length of the line, the point is constructed beyond the end point.

        Returns
        -------
        Point
            The point at the specified distance.

        Raises
        ------
        ZeroDivisionError
            If the start and end points coincide.

        """
        point = self.point + self.direction * distance
        return point

    def point_from_end(self, distance: float) -> Point:
        """Construct a point along the line at a distance from the end point.

        Parameters
        ----------
        distance
            The distance along the line from the end point towards the start point.
            If the distance is negative, the point is constructed in the opposite direction of the start point.
            If the distance is larger than the length of the line, the point is constructed beyond the start point.

        Returns
        -------
        Point
            The point at the specified distance.

        Raises
        ------
        ZeroDivisionError
            If the start and end points coincide.

        """
        point = self.end + self.direction * -distance
        return point

    @overload
    def closest_point(self, point: CoordinateType, return_parameter: Literal[False] = False) -> Point: ...

    @overload
    def closest_point(self, point: CoordinateType, return_parameter: Literal[True]) -> tuple[Point, float]: ...

    def closest_point(self, point: CoordinateType, return_parameter: bool = False) -> Union[Point, tuple[Point, float]]:
        """Compute the closest point on the line to a given point.

        Parameters
        ----------
        point
            The point.
        return_parameter
            Return the parameter of the closest point on the line.
            Default is `False`.

        Returns
        -------
        Point | tuple[Point, float]
            The closest point on the line, optionally paired with its line
            parameter when `return_parameter` is `True`.

        Raises
        ------
        ZeroDivisionError
            If the start and end points coincide.

        Examples
        --------
        >>> line = Line([0, 0, 0], [2, 0, 0])
        >>> line.closest_point(Point(1, 1, 0)) == [1, 0, 0]
        True
        >>> closest, parameter = line.closest_point(Point(1, 1, 0), return_parameter=True)
        >>> closest == [1, 0, 0] and parameter == 0.5
        True

        """
        point = Point(point[0], point[1], point[2])
        vector = point - self.start
        t = vector.dot(self.vector) / self.length**2
        closest = self.start + self.vector * t
        if return_parameter:
            return closest, t
        return closest

    def flip(self) -> None:
        """Flip the direction of the line.

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

    def flipped(self) -> Self:
        """Return a new line with the direction flipped.

        Returns
        -------
        Self
            A new line.

        Examples
        --------
        >>> line = Line([0, 0, 0], [1, 2, 3])
        >>> line
        Line(Point(x=0.0, y=0.0, z=0.0), Point(x=1.0, y=2.0, z=3.0))
        >>> line.flipped()
        Line(Point(x=1.0, y=2.0, z=3.0), Point(x=0.0, y=0.0, z=0.0))

        """
        return type(self)(self.end, self.start)
