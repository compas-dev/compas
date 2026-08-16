from math import cos
from math import pi
from math import sin
from typing import Any
from typing import Optional

from typing_extensions import Self

from compas.geometry import Circle
from compas.geometry import Frame
from compas.geometry import Point
from compas.geometry import Vector
from compas.tolerance import TOL

from .curve import Curve

PI2 = 2.0 * pi


class Arc(Curve):
    """A circular arc defined by a frame, radius, and two angles.

    The center of the underlying circle is the origin of the frame. Angles are
    measured from the positive x-axis towards the positive y-axis.

    Parameters
    ----------
    radius
        The radius of the underlying circle.
    start_angle
        The start angle in radians, in the range `[0, 2 * pi]`.
    end_angle
        The end angle in radians, in the range `[0, 2 * pi]`.
    frame
        The local coordinate frame. Default is the world XY frame.
    name
        The name of the arc.

    See Also
    --------
    [`Circle`][compas.geometry.Circle]

    Notes
    -----
    The parameter domain is `[0, 1]`: `0.0` is the start angle, `1.0` is the
    end angle, and `0.5` is the angle halfway between them.

    Examples
    --------
    >>> from math import pi
    >>> from compas.geometry import Arc
    >>> arc = Arc(1.0, 0.0, pi)
    >>> arc.length == pi
    True
    >>> arc.point_at(0.5)
    Point(x=0.000, y=1.000, z=0.000)

    """

    @property
    def __data__(self) -> dict[str, Any]:
        return {
            "radius": self.radius,
            "start_angle": self.start_angle,
            "end_angle": self.end_angle,
            "frame": self.frame.__data__,
        }

    @classmethod
    def __from_data__(cls, data: dict[str, Any]) -> Self:
        return cls(
            radius=data["radius"],
            start_angle=data["start_angle"],
            end_angle=data["end_angle"],
            frame=Frame.__from_data__(data["frame"]),
        )

    def __init__(
        self,
        radius: float,
        start_angle: float,
        end_angle: float,
        frame: Optional[Frame] = None,
        name: Optional[str] = None,
    ) -> None:
        super().__init__(frame=frame, name=name)
        self._radius: Optional[float] = None
        self._start_angle: Optional[float] = None
        self._end_angle: Optional[float] = None
        self.radius = radius
        self.start_angle = start_angle
        self.end_angle = end_angle

    def __repr__(self) -> str:
        return "{0}(radius={1}, start_angle={2}, end_angle={3}, frame={4!r})".format(type(self).__name__, self.radius, self.start_angle, self.end_angle, self.frame)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Arc):
            return False
        return self.radius == other.radius and self.start_angle == other.start_angle and self.end_angle == other.end_angle and self.frame == other.frame

    @property
    def radius(self) -> float:
        """The radius of the underlying circle.

        Notes
        -----
        The radius must be positive.

        Examples
        --------
        >>> Arc(1.0, 0.0, pi).radius
        1.0

        """
        if self._radius is None:
            raise ValueError("Radius is not set.")
        return self._radius

    @radius.setter
    def radius(self, value: float) -> None:
        if value <= 0.0:
            raise ValueError("Radius must be positive.")
        self._radius = value

    @property
    def start_angle(self) -> float:
        """The start angle in radians.

        Examples
        --------
        >>> Arc(1.0, 0.5, 1.0).start_angle
        0.5

        """
        if self._start_angle is None:
            self._start_angle = 0.0
        return self._start_angle

    @start_angle.setter
    def start_angle(self, value: float) -> None:
        if value < 0.0 or value > PI2:
            raise ValueError("Start angle must satisfy 0 <= angle <= 2 * pi.")
        self._start_angle = value

    @property
    def end_angle(self) -> float:
        """The end angle in radians.

        Examples
        --------
        >>> Arc(1.0, 0.0, pi).end_angle == pi
        True

        """
        if self._end_angle is None:
            raise ValueError("End angle not set.")
        return self._end_angle

    @end_angle.setter
    def end_angle(self, value: float) -> None:
        if value < 0.0 or value > PI2:
            raise ValueError("End angle must satisfy 0 <= angle <= 2 * pi.")
        self._end_angle = value

    @property
    def circle(self) -> Circle:
        """The underlying circle as an independent object."""
        return Circle(radius=self.radius, frame=self.frame)

    @property
    def center(self) -> Point:
        """The center of the arc.

        Notes
        -----
        The returned point belongs to the arc frame. Mutating it changes the arc.

        """
        return self.frame.point

    @property
    def length(self) -> float:
        """The nonnegative length of the arc."""
        return self.radius * abs(self.angle)

    @property
    def angle(self) -> float:
        """The signed sweep angle in radians."""
        return self.end_angle - self.start_angle

    @property
    def diameter(self) -> float:
        """The diameter of the underlying circle."""
        return 2.0 * self.radius

    @property
    def circumference(self) -> float:
        """The circumference of the underlying circle."""
        return self.diameter * pi

    @property
    def is_circle(self) -> bool:
        """Whether the arc covers a complete circle."""
        return TOL.is_close(abs(self.angle), PI2)

    @property
    def is_closed(self) -> bool:
        """Whether the arc covers a complete circle."""
        return self.is_circle

    @property
    def is_periodic(self) -> bool:
        """Whether the arc covers a complete circle."""
        return self.is_circle

    @classmethod
    def from_circle(cls, circle: Circle, start_angle: float, end_angle: float) -> Self:
        """Construct an arc from a circle and two angles.

        Parameters
        ----------
        circle
            The circle providing the frame and radius.
        start_angle
            The start angle in radians.
        end_angle
            The end angle in radians.

        Returns
        -------
        Self
            The constructed arc.

        Notes
        -----
        The arc receives an independent copy of the circle frame.

        Examples
        --------
        >>> circle = Circle(radius=2.0)
        >>> arc = Arc.from_circle(circle, 0.0, pi)
        >>> arc.radius, arc.length
        (2.0, 6.283185307179586)

        """
        return cls(circle.radius, start_angle, end_angle, frame=circle.frame)

    def point_at(self, t: float, world: bool = True) -> Point:
        """Compute the point at a normalized parameter.

        Parameters
        ----------
        t
            The parameter in `[0, 1]`.
        world
            Return world coordinates if `True`, otherwise local coordinates.

        Returns
        -------
        Point
            The point at the parameter.

        Raises
        ------
        ValueError
            If `t` is outside `[0, 1]`.

        Examples
        --------
        >>> Arc(1.0, 0.0, pi).point_at(0.5)
        Point(x=0.000, y=1.000, z=0.000)

        """
        if t < 0.0 or t > 1.0:
            raise ValueError("Parameter t should be between 0.0 and 1.0")
        angle = self.start_angle + t * self.angle
        x = self.radius * cos(angle)
        y = self.radius * sin(angle)
        if not world:
            return Point(x, y, 0.0)
        return self.frame.point + self.frame.xaxis * x + self.frame.yaxis * y

    def normal_at(self, t: float, world: bool = True) -> Vector:
        """Compute the inward unit normal at a normalized parameter.

        Parameters
        ----------
        t
            The parameter in `[0, 1]`.
        world
            Return world coordinates if `True`, otherwise local coordinates.

        Returns
        -------
        Vector
            The inward unit normal.

        Raises
        ------
        ValueError
            If `t` is outside `[0, 1]`.

        Examples
        --------
        >>> Arc(1.0, 0.0, pi).normal_at(0.0)
        Vector(x=-1.000, y=0.000, z=0.000)

        """
        if not world:
            point = self.point_at(t, world=False)
            normal = Vector(-point.x, -point.y, 0.0)
            normal.unitize()
            return normal
        normal = self.frame.point - self.point_at(t)
        normal.unitize()
        return normal

    def tangent_at(self, t: float, world: bool = True) -> Vector:
        """Compute the unit tangent at a normalized parameter.

        Parameters
        ----------
        t
            The parameter in `[0, 1]`.
        world
            Return world coordinates if `True`, otherwise local coordinates.

        Returns
        -------
        Vector
            The unit tangent in increasing parameter direction.

        Raises
        ------
        ValueError
            If `t` is outside `[0, 1]`.

        Examples
        --------
        >>> Arc(2.0, 0.0, pi).tangent_at(0.0)
        Vector(x=0.000, y=1.000, z=0.000)
        >>> Arc(2.0, pi, 0.0).tangent_at(0.0)
        Vector(x=0.000, y=1.000, z=0.000)

        """
        if t < 0.0 or t > 1.0:
            raise ValueError("Parameter t should be between 0.0 and 1.0")
        angle = self.start_angle + t * self.angle
        direction = -1.0 if self.angle < 0.0 else 1.0
        x = -direction * sin(angle)
        y = direction * cos(angle)
        if not world:
            return Vector(x, y, 0.0)
        return self.frame.xaxis * x + self.frame.yaxis * y

    def reverse(self) -> None:
        """Reverse the parametrisation of the arc.

        Examples
        --------
        >>> arc = Arc(1.0, 0.0, pi)
        >>> start, end = arc.point_at(0.0), arc.point_at(1.0)
        >>> arc.reverse()
        >>> arc.point_at(0.0) == end and arc.point_at(1.0) == start
        True

        """
        self.start_angle, self.end_angle = self.end_angle, self.start_angle
