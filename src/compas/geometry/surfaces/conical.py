from math import cos
from math import pi
from math import sin
from math import sqrt
from typing import Any
from typing import Optional

from typing_extensions import Self

from compas._typing import CoordinateType
from compas.geometry import Circle
from compas.geometry import Frame
from compas.geometry import Line
from compas.geometry import Plane
from compas.geometry import Point
from compas.geometry import Vector

from .surface import Surface

PI2 = 2 * pi


class ConicalSurface(Surface):
    """A conical surface defined by a base radius, height, and frame.

    Parameters
    ----------
    radius
        The radius at the base of the cone.
    height
        The distance from the base to the apex.
    frame
        The local coordinate frame at the base. If `None`, the world XY frame
        is used.
    name
        The name of the surface.

    Examples
    --------
    >>> cone = ConicalSurface(radius=2.0, height=3.0)
    >>> cone.point_at(0.0, 0.0)
    Point(x=2.000, y=0.000, z=0.000)
    >>> cone.point_at(0.0, 1.0)
    Point(x=0.000, y=0.000, z=3.000)

    A conical surface can also be constructed from a plane.

    >>> cone = ConicalSurface.from_plane_and_radius_height(Plane.worldXY(), 2.0, 3.0)
    >>> cone.radius, cone.height
    (2.0, 3.0)

    """

    @property
    def __data__(self) -> dict[str, Any]:
        """The data representation of the conical surface."""
        return {
            "radius": self.radius,
            "height": self.height,
            "frame": self.frame.__data__,
        }

    @classmethod
    def __from_data__(cls, data: dict[str, Any]) -> Self:
        return cls(
            radius=data["radius"],
            height=data["height"],
            frame=Frame.__from_data__(data["frame"]),
        )

    def __init__(
        self,
        radius: float,
        height: float,
        frame: Optional[Frame] = None,
        name: Optional[str] = None,
    ) -> None:
        super().__init__(frame=frame, name=name)
        self._radius: Optional[float] = None
        self._height: Optional[float] = None
        self.radius = radius
        self.height = height

    def __repr__(self) -> str:
        return "{0}(radius={1}, height={2}, frame={3!r})".format(
            type(self).__name__,
            self.radius,
            self.height,
            self.frame,
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ConicalSurface):
            return False
        return self.radius == other.radius and self.height == other.height and self.frame == other.frame

    # =============================================================================
    # Properties
    # =============================================================================

    @property
    def center(self) -> Point:
        """The center point of the cone base.

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
        """The positive radius at the cone base."""
        if self._radius is None:
            raise ValueError("The radius of the surface has not been set yet.")
        return self._radius

    @radius.setter
    def radius(self, radius: float) -> None:
        if radius <= 0:
            raise ValueError("The radius of a cone should be larger than zero.")
        self._radius = float(radius)

    @property
    def height(self) -> float:
        """The positive distance from the base to the apex."""
        if self._height is None:
            raise ValueError("The height of the surface has not been set yet.")
        return self._height

    @height.setter
    def height(self, height: float) -> None:
        if height <= 0:
            raise ValueError("The height of a cone should be larger than zero.")
        self._height = float(height)

    @property
    def area(self) -> float:
        """The lateral area of the cone, excluding its circular base."""
        slant_height = sqrt(self.radius**2 + self.height**2)
        return pi * self.radius * slant_height

    @property
    def volume(self) -> float:
        """The volume of the corresponding cone with a circular base."""
        return pi * self.radius**2 * self.height / 3.0

    @property
    def is_periodic_u(self) -> bool:
        """Whether the surface is periodic in U, which is always `True`."""
        return True

    # =============================================================================
    # Constructors
    # =============================================================================

    @classmethod
    def from_plane_and_radius_height(cls, plane: Plane, radius: float, height: float) -> Self:
        """Construct a conical surface from a plane, radius, and height.

        Parameters
        ----------
        plane
            The plane of the cone base.
        radius
            The radius at the base.
        height
            The distance from the base to the apex.

        Returns
        -------
        ConicalSurface
            The constructed conical surface.

        """
        return cls(radius=radius, height=height, frame=Frame.from_plane(plane))

    # =============================================================================
    # Conversions
    # =============================================================================

    # =============================================================================
    # Transformations
    # =============================================================================

    # =============================================================================
    # Methods
    # =============================================================================

    def isocurve_u(self, u: float) -> Line:
        """Compute a generator line at a U parameter.

        Parameters
        ----------
        u
            The U parameter.

        Returns
        -------
        Line
            The line from the cone base to its apex.

        """
        return Line(self.point_at(u, self.domain_v[0]), self.point_at(u, self.domain_v[1]))

    def isocurve_v(self, v: float) -> Circle:
        """Compute the circular isocurve at a V parameter.

        Parameters
        ----------
        v
            The V parameter. It should be smaller than `1.0`; the isocurve at
            the apex degenerates to a point.

        Returns
        -------
        Circle
            The circular isocurve.

        Raises
        ------
        ValueError
            If `v` is `1.0` because the apex has no nondegenerate isocurve.

        """
        radius = (1.0 - v) * self.radius
        if radius <= 0.0:
            raise ValueError("The isocurve at or beyond the cone apex is degenerate.")
        origin = self.center + self.frame.zaxis * (v * self.height)
        return Circle(radius=radius, frame=Frame(origin, self.frame.xaxis, self.frame.yaxis))

    def point_at(self, u: float, v: float, world: bool = True) -> Point:
        """Compute a point on the surface at the given parameters.

        Parameters
        ----------
        u
            The U parameter, mapped to an angle in `[0, 2 * pi]`.
        v
            The V parameter from the base at `0.0` to the apex at `1.0`.
        world
            If `True`, return the point in world coordinates.

        Returns
        -------
        Point
            The point at the given parameters.

        """
        u = u * PI2
        radius = (1 - v) * self.radius
        x = radius * cos(u)
        y = radius * sin(u)
        z = v * self.height
        point = Point(x, y, z)
        if world:
            point.transform(self.transformation)
        return point

    def normal_at(self, u: float, v: float, world: bool = True) -> Vector:
        """Compute the outward normal at a point on the conical surface.

        Parameters
        ----------
        u
            The U parameter.
        v
            The V parameter. The limiting normal at the apex depends on U.
        world
            If `True`, return the normal in world coordinates.

        Returns
        -------
        Vector
            The outward unit normal.

        """
        angle = u * PI2
        normal = Vector(self.height * cos(angle), self.height * sin(angle), self.radius)
        normal.unitize()
        if world:
            normal.transform(self.transformation)
        return normal

    def frame_at(self, u: float, v: float, world: bool = True) -> Frame:
        """Compute a frame at a point on the conical surface.

        Parameters
        ----------
        u
            The U parameter.
        v
            The V parameter.
        world
            If `True`, return the frame in world coordinates.

        Returns
        -------
        Frame
            The frame at the given parameters. Its X-axis follows increasing U,
            its Y-axis points towards the apex, and its Z-axis is outward.

        """
        angle = u * PI2
        point = self.point_at(u, v, world=False)
        tangent_u = Vector(-sin(angle), cos(angle), 0.0)
        tangent_v = Vector(-self.radius * cos(angle), -self.radius * sin(angle), self.height)
        frame = Frame(point, tangent_u, tangent_v)
        if world:
            frame.transform(self.transformation)
        return frame
