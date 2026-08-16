from math import atan2
from math import cos
from math import pi
from math import sin
from typing import Any
from typing import Literal
from typing import Optional
from typing import Sequence
from typing import Union
from typing import overload

from typing_extensions import Self

from compas._typing import CoordinateType
from compas.geometry import Frame
from compas.geometry import Plane
from compas.geometry import Point
from compas.geometry import Vector

from .conic import Conic

PI2 = 2 * pi


class Circle(Conic):
    """A circle is a curve defined by a coordinate system and a radius.

    The center of the circle is at the origin of the coordinate system.
    The z-axis of the coordinate system defines the normal of the circle plane.
    The parameter domain is normalized with respect to the polar angle.
    A parameter value of `t = 0` corresponds to the point at angle `0`.
    A parameter value of `t = 1` corresponds to the point at angle `2 * pi`.
    Moving along the circle in the parameter direction corresponds to moving counter-clockwise around the origin of the local coordinate system.

    Parameters
    ----------
    radius
        The radius of the circle.
    frame
        The coordinate frame of the circle.
        If `None`, the world XY frame is used.
    name
        The name of the circle.

    See Also
    --------
    [`Ellipse`][compas.geometry.Ellipse] and [`Arc`][compas.geometry.Arc]

    Examples
    --------
    Construct a circle in the world XY plane.

    >>> from compas.geometry import Frame, Circle
    >>> circle = Circle(radius=5, frame=Frame.worldXY())
    >>> circle = Circle(radius=5)

    Construct a circle such that the Z axis of its frame such that it aligns with a given line.

    >>> from compas.geometry import Line, Frame, Plane, Circle
    >>> line = Line([0, 0, 0], [1, 1, 1])
    >>> plane = Plane(line.end, line.direction)
    >>> circle = Circle.from_plane_and_radius(plane, 5)
    >>> circle = Circle(radius=5, frame=Frame.from_plane(plane))
    """

    @property
    def __data__(self) -> dict[str, Any]:
        return {"radius": self.radius, "frame": self.frame.__data__}

    @classmethod
    def __from_data__(cls, data: dict[str, Any]) -> Self:
        return cls(radius=data["radius"], frame=Frame.__from_data__(data["frame"]))

    def __init__(self, radius: float, frame: Optional[Frame] = None, name: Optional[str] = None) -> None:
        super().__init__(frame=frame, name=name)
        self._radius: Optional[float] = None
        self.radius = radius

    def __repr__(self) -> str:
        return "{0}(radius={1!r}, frame={2!r})".format(
            type(self).__name__,
            self.radius,
            self.frame,
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Circle):
            return False
        return self.frame == other.frame and self.radius == other.radius

    # ==========================================================================
    # Properties
    # ==========================================================================

    @property
    def center(self) -> Point:
        """The center of the circle.

        Notes
        -----
        Assigning a point or three coordinates updates the frame origin and
        creates an independent point.

        Examples
        --------
        >>> circle = Circle(1.0)
        >>> circle.center = [1.0, 2.0, 3.0]
        >>> circle.center
        Point(x=1.000, y=2.000, z=3.000)

        """
        return self.frame.point

    @center.setter
    def center(self, point: CoordinateType) -> None:
        self.frame.point = point

    @property
    def radius(self) -> float:
        """The positive radius of the circle."""
        if self._radius is None:
            raise ValueError("The radius of the circle has not been set yet.")
        return self._radius

    @radius.setter
    def radius(self, radius: float) -> None:
        if radius <= 0:
            raise ValueError("The radius of a circle must be positive.")
        self._radius = float(radius)

    @property
    def diameter(self) -> float:
        """The diameter of the circle."""
        return 2 * self.radius

    @property
    def area(self) -> float:
        """The area enclosed by the circle."""
        return pi * (self.radius**2)

    @property
    def circumference(self) -> float:
        """The circumference of the circle."""
        return 2 * pi * self.radius

    @property
    def length(self) -> float:
        """The length of the circle, equal to its circumference."""
        return self.circumference

    @property
    def eccentricity(self) -> float:
        """The eccentricity of the circle, which is always zero."""
        return 0.0

    @property
    def is_closed(self) -> bool:
        """Whether the circle is closed."""
        return True

    @property
    def is_periodic(self) -> bool:
        """Whether the circle is periodic."""
        return True

    # ==========================================================================
    # Constructors
    # ==========================================================================

    @classmethod
    def from_point_and_radius(cls, point: CoordinateType, radius: float) -> Self:
        """Construct a circle from a point and a radius.

        Parameters
        ----------
        point
            The center of the circle.
        radius
            The radius of the circle.

        Returns
        -------
        Self
            The constructed circle.

        See Also
        --------
        [`Circle.from_plane_and_radius`][compas.geometry.Circle.from_plane_and_radius],
        [`Circle.from_three_points`][compas.geometry.Circle.from_three_points]

        Examples
        --------
        >>> circle = Circle.from_point_and_radius([1.0, 2.0, 3.0], 2.0)
        >>> circle.center, circle.radius
        (Point(x=1.000, y=2.000, z=3.000), 2.0)

        """
        frame = Frame(point, [1, 0, 0], [0, 1, 0])
        return cls(frame=frame, radius=radius)

    @classmethod
    def from_plane_and_radius(cls, plane: Plane, radius: float) -> Self:
        """Construct a circle from a plane and a radius.

        Parameters
        ----------
        plane
            The plane of the circle.
        radius
            The radius of the circle.

        Returns
        -------
        Self
            The constructed circle.

        See Also
        --------
        [`Circle.from_point_and_radius`][compas.geometry.Circle.from_point_and_radius],
        [`Circle.from_three_points`][compas.geometry.Circle.from_three_points]

        Examples
        --------
        >>> from compas.geometry import Plane
        >>> from compas.geometry import Circle
        >>> plane = Plane([0, 0, 0], [0, 0, 1])
        >>> circle = Circle.from_plane_and_radius(plane, 5)

        """
        frame = Frame.from_plane(plane)
        return cls(frame=frame, radius=radius)

    @classmethod
    def from_three_points(cls, a: CoordinateType, b: CoordinateType, c: CoordinateType) -> Self:
        """Construct a circle from three points.

        Parameters
        ----------
        a
            The first point.
        b
            The second point.
        c
            The third point.

        Returns
        -------
        Self
            The constructed circle.

        See Also
        --------
        [`Circle.from_point_and_radius`][compas.geometry.Circle.from_point_and_radius]

        Examples
        --------
        >>> circle = Circle.from_three_points([1, 0, 0], [0, 1, 0], [-1, 0, 0])
        >>> circle.center, circle.radius
        (Point(x=0.000, y=0.000, z=0.000), 1.0)

        """
        from compas.geometry import Plane

        a = Point(a[0], a[1], a[2])
        b = Point(b[0], b[1], b[2])
        c = Point(c[0], c[1], c[2])

        ab = b - a
        cb = b - c
        ba = a - b
        ca = a - c
        ac = c - a
        bc = c - b

        normal = ab.cross(ac).unitized()

        d = 2 * ba.cross(cb).length ** 2

        A = cb.length**2 * ba.dot(ca) / d
        B = ca.length**2 * ab.dot(cb) / d
        C = ba.length**2 * ac.dot(bc) / d
        Aa = a.scaled(A)
        Bb = b.scaled(B)
        Cc = c.scaled(C)

        point = Aa + Bb + Cc
        radius = (a - point).length
        plane = Plane(point, normal)

        return cls.from_plane_and_radius(plane, radius)

    @classmethod
    def from_points(cls, points: Sequence[CoordinateType]) -> Self:
        """Construct a circle from a list of at least three points.

        Parameters
        ----------
        points
            A list of three points defining the circle.

        Returns
        -------
        Self
            The constructed circle.

        Raises
        ------
        ValueError
            If the list of points contains less than three points.

        See Also
        --------
        [`Circle.from_three_points`][compas.geometry.Circle.from_three_points]

        Notes
        -----
        If more than three points are provided,
        the constructed circle is the one that best fits the points in the least-squares sense.

        Examples
        --------
        >>> points = [[1, 0, 0], [0, 1, 0], [-1, 0, 0]]
        >>> Circle.from_points(points).radius
        1.0

        """
        if len(points) < 3:
            raise ValueError("At least three points are required to define a circle.")

        if len(points) == 3:
            return cls.from_three_points(*points)

        # not sure if this makes sense
        # but it will only throw an error if the bestfit is actually needed
        from compas.geometry import bestfit_circle_numpy

        point, normal, radius = bestfit_circle_numpy(points)
        plane = Plane(point, normal)
        return cls.from_plane_and_radius(plane, radius)

    # =============================================================================
    # Methods
    # =============================================================================

    def point_at(self, t: float, world: bool = True) -> Point:
        """Construct a point on the circle at a specific parameter.

        Parameters
        ----------
        t
            The parameter of the point.
            The parameter is expected to be normalized,
            and is mapped to the angle interval `[0, 2 * pi]`.
        world
            If `True`, the point is returned in world coordinates.

        Returns
        -------
        Point
            The point on the circle at the specified parameter.

        See Also
        --------
        [`Circle.normal_at`][compas.geometry.Circle.normal_at] and
        [`Circle.tangent_at`][compas.geometry.Circle.tangent_at]

        Notes
        -----
        The location of the point is expressed with respect to the world coordinate system.

        Examples
        --------
        >>> Circle(2.0).point_at(0.25)
        Point(x=0.000, y=2.000, z=0.000)

        """
        t = t * PI2
        x = self.radius * cos(t)
        y = self.radius * sin(t)
        point = Point(x, y, 0)
        if world:
            point.transform(self.transformation)
        return point

    def normal_at(self, t: float, world: bool = True) -> Vector:
        """Construct a normal on the circle at a specific parameter.

        Parameters
        ----------
        t
            The parameter of the normal vector.
            The parameter is expected to be normalized,
            and is mapped to the angle interval `[0, 2 * pi]`.
        world
            If `True`, the normal is returned in world coordinates.

        Returns
        -------
        Vector
            The normal on the circle at the specified parameter.

        See Also
        --------
        [`Circle.point_at`][compas.geometry.Circle.point_at] and
        [`Circle.tangent_at`][compas.geometry.Circle.tangent_at]

        Notes
        -----
        The orientation of the vector is expressed with respect to the world coordinate system.

        Examples
        --------
        >>> Circle(2.0).normal_at(0.0)
        Vector(x=-1.000, y=0.000, z=0.000)

        """
        if world:
            normal = self.center - self.point_at(t, world=True)
            normal.unitize()
            return normal
        point = self.point_at(t, world=False)
        normal = Vector(-point.x, -point.y, 0)
        normal.unitize()
        return normal

    def tangent_at(self, t: float, world: bool = True) -> Vector:
        """Construct a tangent on the circle at a specific parameter.

        Parameters
        ----------
        t
            The parameter of the tangent vector.
            The parameter is expected to be normalized,
            and is mapped to the angle interval `[0, 2 * pi]`.
        world
            If `True`, the tangent is returned in world coordinates.

        Returns
        -------
        Vector
            The tangent on the circle at the specified parameter.

        See Also
        --------
        [`Circle.point_at`][compas.geometry.Circle.point_at] and
        [`Circle.normal_at`][compas.geometry.Circle.normal_at]

        Notes
        -----
        The orientation of the vector is expressed with respect to the world coordinate system.

        Examples
        --------
        >>> Circle(2.0).tangent_at(0.0)
        Vector(x=0.000, y=1.000, z=0.000)

        """
        t = t * PI2
        x = -self.radius * sin(t)
        y = +self.radius * cos(t)
        vector = Vector(x, y, 0)
        vector.unitize()
        if world:
            vector.transform(self.transformation)
        return vector

    @overload
    def closest_point(self, point: CoordinateType, return_parameter: Literal[False] = False) -> Point: ...

    @overload
    def closest_point(self, point: CoordinateType, return_parameter: Literal[True]) -> tuple[Point, float]: ...

    def closest_point(self, point: CoordinateType, return_parameter: bool = False) -> Union[Point, tuple[Point, float]]:
        """Compute the closest point on the circle to a given point.

        Parameters
        ----------
        point
            A point.
        return_parameter
            Return the parameter of the closest point as well.

        Returns
        -------
        Point
            The closest point if `return_parameter` is `False`.
        tuple[Point, float]
            The closest point and its normalized parameter if `return_parameter` is `True`.

        Notes
        -----
        The location of the point is expressed with respect to the world coordinate system.
        If the input projects onto the center, the point at parameter `0.0` is returned.

        Examples
        --------
        >>> circle = Circle(1.0)
        >>> circle.closest_point([2.0, 2.0, 0.0])
        Point(x=0.707, y=0.707, z=0.000)
        >>> circle.closest_point([0.0, 2.0, 0.0], return_parameter=True)
        (Point(x=0.000, y=1.000, z=0.000), 0.25)

        """
        local = self.frame.to_local_coordinates(point)
        vector = Vector(local.x, local.y, 0.0)
        if not vector.length:
            vector = Vector(self.radius, 0.0, 0.0)
        vector.unitize()
        vector *= self.radius
        closest = self.frame.to_world_coordinates(Point(vector.x, vector.y, 0.0))
        if return_parameter:
            parameter = atan2(vector.y, vector.x) / PI2
            return closest, parameter % 1.0
        return closest

    def contains_point(self, point: CoordinateType, tol: float = 1e-6, dmax: float = 1e-6) -> bool:
        """Verify that the circle contains a given point.

        Parameters
        ----------
        point
            The point.
        tol
            The tolerance for the verification.
        dmax
            The maximum allowed distance between the plane of the circle and the point.

        Returns
        -------
        bool
            True if the point is on the circle.
            False otherwise.

        Notes
        -----
        `dmax` controls the allowed distance from the circle plane.

        Examples
        --------
        >>> circle = Circle(1.0)
        >>> circle.contains_point([1.0, 0.0, 0.0])
        True
        >>> circle.contains_point([0.0, 0.0, 0.0])
        False

        """
        point = self.frame.to_local_coordinates(point)
        x, y, z = point.x, point.y, point.z
        if abs(z) > dmax:
            return False
        return abs((x**2 + y**2) ** 0.5 - self.radius) <= tol
