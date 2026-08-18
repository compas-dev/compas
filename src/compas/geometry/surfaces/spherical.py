from math import cos
from math import pi
from math import sin
from typing import Any
from typing import Optional

from typing_extensions import Self

from compas._typing import CoordinatesType
from compas._typing import CoordinateType
from compas.geometry import Arc
from compas.geometry import Circle
from compas.geometry import Frame
from compas.geometry import Plane
from compas.geometry import Point
from compas.geometry import Vector

from .surface import Surface

PI2 = 2 * pi


class SphericalSurface(Surface):
    """A spherical surface is defined by a radius and a frame.

    Parameters
    ----------
    radius
        The radius of the sphere.
    frame
        The local coordinate frame. If `None`, the world XY frame is used.
    name
        The name of the surface.

    Examples
    --------
    >>> sphere = SphericalSurface(1.0)
    >>> sphere.point_at(0.0, 0.5)
    Point(x=1.000, y=0.000, z=0.000)

    Spherical surfaces can also be constructed from a plane or three points.

    >>> sphere = SphericalSurface.from_plane_and_radius(Plane.worldXY(), 2.0)
    >>> sphere.radius
    2.0
    >>> sphere = SphericalSurface.from_three_points([1, 0, 0], [0, 1, 0], [-1, 0, 0])
    >>> sphere.radius
    1.0

    """

    @property
    def __data__(self) -> dict[str, Any]:
        """The data representation of the spherical surface."""
        return {
            "radius": self.radius,
            "frame": self.frame.__data__,
        }

    @classmethod
    def __from_data__(cls, data: dict[str, Any]) -> Self:
        return cls(
            radius=data["radius"],
            frame=Frame.__from_data__(data["frame"]),
        )

    def __init__(self, radius: float, frame: Optional[Frame] = None, name: Optional[str] = None) -> None:
        super().__init__(frame=frame, name=name)
        self._radius: Optional[float] = None
        self.radius = radius

    def __repr__(self) -> str:
        return "{0}(radius={1}, frame={2!r})".format(
            type(self).__name__,
            self.radius,
            self.frame,
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, SphericalSurface):
            return False
        return self.radius == other.radius and self.frame == other.frame

    # =============================================================================
    # Properties
    # =============================================================================

    @property
    def center(self) -> Point:
        """The center point of the sphere.

        Notes
        -----
        Assigning a point or three coordinates updates the surface frame and
        creates an independent point.

        """
        return self.frame.point

    @center.setter
    def center(self, point: CoordinateType) -> None:
        self.frame.point = point

    @property
    def radius(self) -> float:
        """The nonnegative radius of the sphere."""
        if self._radius is None:
            raise ValueError("The radius of the surface has not been set yet.")
        return self._radius

    @radius.setter
    def radius(self, radius: float) -> None:
        if radius < 0:
            raise ValueError("The radius of a sphere should be larger than or equal to zero.")
        self._radius = float(radius)

    @property
    def area(self) -> float:
        """The surface area of the sphere."""
        return 4 * pi * self.radius**2

    @property
    def volume(self) -> float:
        """The volume enclosed by the sphere."""
        return 4.0 / 3.0 * pi * self.radius**3

    @property
    def is_periodic_u(self) -> bool:
        """Whether the surface is periodic in U, which is always `True`."""
        return True

    # =============================================================================
    # Constructors
    # =============================================================================

    @classmethod
    def from_plane_and_radius(cls, plane: Plane, radius: float) -> Self:
        """Construct a sphere from a plane and a radius.

        Parameters
        ----------
        plane
            The plane of the sphere.
        radius
            The radius of the sphere.

        Returns
        -------
        SphericalSurface
            A sphere.

        """
        return cls(radius, frame=Frame.from_plane(plane))

    @classmethod
    def from_three_points(cls, a: CoordinateType, b: CoordinateType, c: CoordinateType) -> Self:
        """Construct a sphere from three points.

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
        SphericalSurface
            A sphere.

        """
        circle = Circle.from_three_points(a, b, c)
        return cls(circle.radius, frame=circle.frame)

    @classmethod
    def from_points(cls, points: CoordinatesType) -> Self:
        """Construct the sphere that best fits a set of points in the least squares sense.

        Parameters
        ----------
        points
            The points.

        Returns
        -------
        SphericalSurface
            A sphere.

        """
        if len(points) < 3:
            raise ValueError("At least three points are required to construct a sphere.")

        if len(points) == 3:
            return cls.from_three_points(points[0], points[1], points[2])

        from compas.geometry import bestfit_sphere_numpy

        center, radius = bestfit_sphere_numpy(points)
        return cls(radius, frame=Frame(center, [1, 0, 0], [0, 1, 0]))

    # =============================================================================
    # Conversions
    # =============================================================================

    # =============================================================================
    # Methods
    # =============================================================================

    def isocurve_u(self, u: float) -> Arc:
        """Compute the meridian arc at a U parameter.

        Parameters
        ----------
        u
            The U parameter.

        Returns
        -------
        Arc
            The pole-to-pole meridian arc.

        """
        angle = u * PI2
        radial = self.frame.xaxis * cos(angle) + self.frame.yaxis * sin(angle)
        frame = Frame(self.center, self.frame.zaxis, radial)
        return Arc(radius=self.radius, start_angle=0.0, end_angle=pi, frame=frame)

    def isocurve_v(self, v: float) -> Circle:
        """Compute the latitude circle at a V parameter.

        Parameters
        ----------
        v
            The V parameter.

        Returns
        -------
        Circle
            The latitude circle.

        """
        angle = v * pi
        origin = self.center + self.frame.zaxis * (self.radius * cos(angle))
        frame = Frame(origin, self.frame.xaxis, self.frame.yaxis)
        return Circle(radius=self.radius * sin(angle), frame=frame)

    def point_at(self, u: float, v: float, world: bool = True) -> Point:
        """Compute a point on the sphere.

        Parameters
        ----------
        u
            The U parameter, mapped to an azimuth in `[0, 2 * pi]`.
        v
            The V parameter, mapped to a polar angle in `[0, pi]`.
        world
            If `True`, return the point in world coordinates.

        Returns
        -------
        Point
            The point at the given parameters.

        """
        u = u * PI2
        v = v * pi
        x = self.radius * cos(u) * sin(v)
        y = self.radius * sin(u) * sin(v)
        z = self.radius * cos(v)
        point = Point(x, y, z)
        if world:
            point.transform(self.transformation)
        return point

    def normal_at(self, u: float, v: float, world: bool = True) -> Vector:
        """Compute the outward normal at a point on the sphere.

        Parameters
        ----------
        u
            The U parameter.
        v
            The V parameter.
        world
            If `True`, return the normal in world coordinates.

        Returns
        -------
        Vector
            The outward unit normal.

        """
        u = u * PI2
        v = v * pi
        x = cos(u) * sin(v)
        y = sin(u) * sin(v)
        z = cos(v)
        normal = Vector(x, y, z)
        if world:
            normal.transform(self.transformation)
        return normal
