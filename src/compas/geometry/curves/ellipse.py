from math import cos
from math import pi
from math import sin
from math import sqrt
from typing import Any
from typing import Optional

from typing_extensions import Self

from compas._typing import CoordinateType
from compas.geometry import Frame
from compas.geometry import Plane
from compas.geometry import Point
from compas.geometry import Vector

from ..line import Line
from .conic import Conic

PI2 = 2 * pi


class Ellipse(Conic):
    """An ellipse is a curve defined by a coordinate system and a major and minor axis.

    The center of the ellipse is at the origin of the coordinate system.
    The major axis is parallel to the local x-axis.
    The minor axis is parallel to the local y-axis.
    The normalized parameter domain is `[0, 1]`.
    Moving along the ellipse in the parameter direction corresponds to moving counter-clockwise around the origin of the local coordinate system.

    Parameters
    ----------
    major
        The major of the ellipse.
    minor
        The minor of the ellipse.
    frame
        The local coordinate system of the ellipse.
        If `None`, the world XY frame is used.
    name
        The name of the ellipse.

    See Also
    --------
    [`Circle`][compas.geometry.Circle], [`Hyperbola`][compas.geometry.Hyperbola],
    and [`Parabola`][compas.geometry.Parabola]

    Examples
    --------
    Construct an ellipse in the world XY plane.

    >>> from compas.geometry import Frame, Ellipse
    >>> ellipse = Ellipse(major=3, minor=2, frame=Frame.worldXY())
    >>> ellipse = Ellipse(major=3, minor=2)

    Construct an ellipse such that its normal aligns with a given line.

    >>> from compas.geometry import Line, Frame, Plane, Ellipse
    >>> line = Line([0, 0, 0], [1, 1, 1])
    >>> plane = Plane(line.end, line.direction)
    >>> ellipse = Ellipse.from_plane_major_minor(plane, 3, 2)
    >>> ellipse = Ellipse(major=3, minor=2, frame=Frame.from_plane(plane))

    """

    @property
    def __data__(self) -> dict[str, Any]:
        return {
            "major": self.major,
            "minor": self.minor,
            "frame": self.frame.__data__,
        }

    @classmethod
    def __from_data__(cls, data: dict[str, Any]) -> Self:
        return cls(
            major=data["major"],
            minor=data["minor"],
            frame=Frame.__from_data__(data["frame"]),
        )

    def __init__(
        self,
        major: float = 1.0,
        minor: float = 1.0,
        frame: Optional[Frame] = None,
        name: Optional[str] = None,
    ) -> None:
        super().__init__(frame=frame, name=name)
        self._major: Optional[float] = None
        self._minor: Optional[float] = None
        self.major = major
        self.minor = minor

    def __repr__(self) -> str:
        return "{0}(major={1!r}, minor={2}, frame={3!r})".format(
            type(self).__name__,
            self.major,
            self.minor,
            self.frame,
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Ellipse):
            return False
        return self.major == other.major and self.minor == other.minor and self.frame == other.frame

    # ==========================================================================
    # Properties
    # ==========================================================================

    @property
    def center(self) -> Point:
        """The center of the ellipse.

        Notes
        -----
        Assigning a point or three coordinates updates the frame origin and
        creates an independent point.

        """
        return self.frame.point

    @center.setter
    def center(self, point: CoordinateType) -> None:
        self.frame.point = point

    @property
    def major(self) -> float:
        """The positive semi-major axis length."""
        if self._major is None:
            raise ValueError("Length of major axis is not set.")
        return self._major

    @major.setter
    def major(self, major: float) -> None:
        if major <= 0:
            raise ValueError("Major axis length must be positive.")
        if self._minor is not None and major < self._minor:
            raise ValueError("Major axis length cannot be smaller than the minor axis length.")
        self._major = float(major)

    @property
    def minor(self) -> float:
        """The positive semi-minor axis length."""
        if self._minor is None:
            raise ValueError("Length of minor axis is not set.")
        return self._minor

    @minor.setter
    def minor(self, minor: float) -> None:
        if minor <= 0:
            raise ValueError("Minor axis length must be positive.")
        if self._major is not None and minor > self._major:
            raise ValueError("Minor axis length cannot be larger than the major axis length.")
        self._minor = float(minor)

    @property
    def semifocal(self) -> float:
        """The distance from the center to either focus."""
        return sqrt(self.major**2 - self.minor**2)

    @property
    def focal(self) -> float:
        """The distance between the two foci."""
        return 2 * self.semifocal

    @property
    def eccentricity(self) -> float:
        """The eccentricity of the ellipse."""
        return self.semifocal / self.major

    @property
    def focus1(self) -> Point:
        """The focus in the positive major-axis direction."""
        return self.frame.point + self.frame.xaxis * +self.semifocal

    @property
    def focus2(self) -> Point:
        """The focus in the negative major-axis direction."""
        return self.frame.point + self.frame.xaxis * -self.semifocal

    @property
    def vertex1(self) -> Point:
        """The vertex in the positive major-axis direction."""
        return self.frame.point + self.frame.xaxis * self.major

    @property
    def vertex2(self) -> Point:
        """The vertex in the negative major-axis direction."""
        return self.frame.point + self.frame.xaxis * -self.major

    @property
    def directix1(self) -> Line:
        """The directrix in the positive major-axis direction."""
        d1 = self.major**2 / self.semifocal
        p1 = self.frame.point + self.frame.xaxis * +d1
        return Line.from_point_and_vector(p1, self.frame.yaxis)

    @property
    def directix2(self) -> Line:
        """The directrix in the negative major-axis direction."""
        d2 = self.major**2 / self.semifocal
        p2 = self.frame.point + self.frame.xaxis * -d2
        return Line.from_point_and_vector(p2, self.frame.yaxis)

    @property
    def area(self) -> float:
        """The area enclosed by the ellipse."""
        return pi * self.major * self.minor

    @property
    def circumference(self) -> float:
        """The approximate circumference of the ellipse.

        Notes
        -----
        The circumference is computed with Ramanujan's second approximation,
        using `h = ((a - b) / (a + b)) ** 2`.

        Examples
        --------
        >>> round(Ellipse(1.0, 0.5).circumference, 6)
        4.844224

        """
        h = ((self.major - self.minor) / (self.major + self.minor)) ** 2
        return pi * (self.major + self.minor) * (1.0 + 3.0 * h / (10.0 + sqrt(4.0 - 3.0 * h)))

    @property
    def length(self) -> float:
        """The length of the ellipse, equal to its circumference."""
        return self.circumference

    @property
    def is_circle(self) -> bool:
        """Whether the major and minor axes are equal."""
        return self.major == self.minor

    @property
    def is_closed(self) -> bool:
        """Whether the ellipse is closed."""
        return True

    @property
    def is_periodic(self) -> bool:
        """Whether the ellipse is periodic."""
        return True

    # ==========================================================================
    # Constructors
    # ==========================================================================

    @classmethod
    def from_point_major_minor(cls, point: CoordinateType, major: float, minor: float) -> Self:
        """Construct a ellipse from a point and major and minor axis lengths.

        Parameters
        ----------
        point
            The center point of the ellipse.
        major
            The major axis length.
        minor
            The minor axis length.

        Returns
        -------
        Self
            The constructed ellipse.

        Examples
        --------
        >>> ellipse = Ellipse.from_point_major_minor([1, 2, 3], 3, 2)
        >>> ellipse.center
        Point(x=1.000, y=2.000, z=3.000)

        """
        frame = Frame(point, [1, 0, 0], [0, 1, 0])
        return cls(major=major, minor=minor, frame=frame)

    @classmethod
    def from_plane_major_minor(cls, plane: Plane, major: float, minor: float) -> Self:
        """Construct a ellipse from a point and major and minor axis lengths.

        Parameters
        ----------
        plane
            The plane of the ellipse.
        major
            The major axis length.
        minor
            The minor axis length.

        Returns
        -------
        Self
            The constructed ellipse.

        Examples
        --------
        >>> plane = Plane.worldXY()
        >>> Ellipse.from_plane_major_minor(plane, 3, 2).plane == plane
        True

        """
        frame = Frame.from_plane(plane)
        return cls(major=major, minor=minor, frame=frame)

    # ==========================================================================
    # Methods
    # ==========================================================================

    def point_at(self, t: float, world: bool = True) -> Point:
        """Compute the point at a specific parameter.

        Parameters
        ----------
        t
            The parameter value.
        world
            If `True`, the point is returned in world coordinates.

        Returns
        -------
        Point
            The point at the parameter.

        See Also
        --------
        [`Ellipse.normal_at`][compas.geometry.Ellipse.normal_at] and
        [`Ellipse.tangent_at`][compas.geometry.Ellipse.tangent_at]

        Notes
        -----
        The location of the point is expressed with respect to the world coordinate system.

        Examples
        --------
        >>> Ellipse(3, 2).point_at(0.25)
        Point(x=0.000, y=2.000, z=0.000)

        """
        t = t * PI2
        x = self.major * cos(t)
        y = self.minor * sin(t)
        point = Point(x, y, 0)
        if world:
            point.transform(self.transformation)
        return point

    def tangent_at(self, t: float, world: bool = True) -> Vector:
        """Compute the tangent at a specific parameter.

        Parameters
        ----------
        t
            The parameter value.
        world
            If `True`, the tangent is returned in world coordinates.

        Returns
        -------
        Vector
            The tangent vector at the parameter.

        See Also
        --------
        [`Ellipse.point_at`][compas.geometry.Ellipse.point_at] and
        [`Ellipse.normal_at`][compas.geometry.Ellipse.normal_at]

        Notes
        -----
        The orientation of the vector is expressed with respect to the world coordinate system.

        Examples
        --------
        >>> Ellipse(3, 2).tangent_at(0.0)
        Vector(x=0.000, y=1.000, z=0.000)

        """
        normal = self.normal_at(t, world=False)
        zaxis = Vector(0, 0, 1)
        tangent = normal.cross(zaxis)
        tangent.unitize()
        if world:
            tangent.transform(self.transformation)
        return tangent

    def normal_at(self, t: float, world: bool = True) -> Vector:
        """Compute the normal at a specific parameter.

        Parameters
        ----------
        t
            The parameter value.
        world
            If `True`, the normal is returned in world coordinates.

        Returns
        -------
        Vector
            The normal vector at the parameter.

        See Also
        --------
        [`Ellipse.point_at`][compas.geometry.Ellipse.point_at] and
        [`Ellipse.tangent_at`][compas.geometry.Ellipse.tangent_at]

        Notes
        -----
        The orientation of the vector is expressed with respect to the world coordinate system.

        Examples
        --------
        >>> Ellipse(3, 2).normal_at(0.0)
        Vector(x=-1.000, y=0.000, z=0.000)

        """
        point = self.point_at(t, world=False)
        f1 = Point(+self.semifocal, 0, 0)
        f2 = Point(-self.semifocal, 0, 0)
        normal = (f1 - point).unitized() + (f2 - point).unitized()
        normal.unitize()
        if world:
            normal.transform(self.transformation)
        return normal
