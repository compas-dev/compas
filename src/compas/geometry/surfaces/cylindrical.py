from math import cos
from math import pi
from math import sin
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


class CylindricalSurface(Surface):
    """A cylindrical surface is defined by a radius and a local coordinate system.

    Parameters
    ----------
    radius
        The radius of the cylinder.
    frame
        The local coordinate frame. If `None`, the world XY frame is used.
    name
        The name of the surface.

    Examples
    --------
    >>> cylinder = CylindricalSurface(2.0)
    >>> cylinder.point_at(0.0, 0.5)
    Point(x=2.000, y=0.000, z=0.500)

    Cylindrical surfaces can also be constructed from a plane or three points.

    >>> cylinder = CylindricalSurface.from_plane_and_radius(Plane.worldXY(), 2.0)
    >>> cylinder.radius
    2.0

    """

    @property
    def __data__(self) -> dict[str, Any]:
        """The data representation of the cylindrical surface."""
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
        if not isinstance(other, CylindricalSurface):
            return False
        return self.radius == other.radius and self.frame == other.frame

    # =============================================================================
    # Properties
    # =============================================================================

    @property
    def center(self) -> Point:
        """The point on the cylinder axis at V parameter zero.

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
        """The positive radius of the cylinder."""
        if self._radius is None:
            raise ValueError("The radius of the surface has not been set yet.")
        return self._radius

    @radius.setter
    def radius(self, radius: float) -> None:
        if radius <= 0:
            raise ValueError("The radius of a cylinder should be larger than zero.")
        self._radius = float(radius)

    @property
    def area(self) -> float:
        """The lateral area over the surface V domain.

        Notes
        -----
        This excludes the areas of the two circular caps.

        """
        vmin, vmax = self.domain_v
        height = abs(vmax - vmin)
        return 2.0 * pi * self.radius * height

    @property
    def volume(self) -> float:
        """The volume of the capped cylinder over the surface V domain.

        Although the surface itself has no caps, this property reports the
        volume of the corresponding solid cylinder bounded at the ends of the
        V domain.

        """
        vmin, vmax = self.domain_v
        height = abs(vmax - vmin)
        return pi * self.radius**2 * height

    @property
    def is_periodic_u(self) -> bool:
        """Whether the surface is periodic in U, which is always `True`."""
        return True

    # =============================================================================
    # Constructors
    # =============================================================================

    @classmethod
    def from_plane_and_radius(cls, plane: Plane, radius: float) -> Self:
        """Construct a cylindrical surface from a plane and a radius.

        Parameters
        ----------
        plane
            The plane of the surface.
        radius
            The radius of the surface.

        Returns
        -------
        CylindricalSurface
            A cylindrical surface.

        """
        return cls(radius, frame=Frame.from_plane(plane))

    @classmethod
    def from_three_points(cls, a: CoordinateType, b: CoordinateType, c: CoordinateType) -> Self:
        """Construct a cylindrical from three points.

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
        CylindricalSurface
            A cylindrical surface.

        """
        circle = Circle.from_three_points(a, b, c)
        return cls(circle.radius, frame=circle.frame)

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
        """Compute the generator line at a U parameter.

        Parameters
        ----------
        u
            The U parameter.

        Returns
        -------
        Line
            The generator over the surface V domain.

        """
        return Line(self.point_at(u, self.domain_v[0]), self.point_at(u, self.domain_v[1]))

    def isocurve_v(self, v: float) -> Circle:
        """Compute the circular isocurve at a V parameter.

        Parameters
        ----------
        v
            The V parameter.

        Returns
        -------
        Circle
            The circular isocurve.

        """
        point = self.center + self.frame.zaxis * v
        xaxis = self.frame.xaxis
        yaxis = self.frame.yaxis
        frame = Frame(point, xaxis, yaxis)
        return Circle(radius=self.radius, frame=frame)

    def point_at(self, u: float, v: float, world: bool = True) -> Point:
        """Compute a point on the surface at the given parameters.

        Parameters
        ----------
        u
            The U parameter, mapped to an angle in `[0, 2 * pi]`.
        v
            The V parameter along the cylinder axis.
        world
            If `True`, return the point in world coordinates.

        Returns
        -------
        Point
            The point at the given parameters.

        """
        u = u * PI2
        x = self.radius * cos(u)
        y = self.radius * sin(u)
        z = v
        point = Point(x, y, z)
        if world:
            point.transform(self.transformation)
        return point

    def normal_at(self, u: float, v: float, world: bool = True) -> Vector:
        """Compute the normal at a point on the surface at the given parameters.

        Parameters
        ----------
        u
            The U parameter.
        v
            The V parameter. The normal is independent of this parameter.
        world
            If `True`, return the normal in world coordinates.

        Returns
        -------
        Vector
            The outward unit normal at the given parameters.

        """
        u = u * PI2
        vector = Vector(cos(u), sin(u), 0.0)
        if world:
            vector.transform(self.transformation)
        return vector

    def frame_at(self, u: float, v: float, world: bool = True) -> Frame:
        """Compute the frame at a point on the surface at the given parameters.

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
            its Y-axis follows increasing V, and its Z-axis is the outward normal.

        """
        point = self.point_at(u, v, world=False)
        zaxis = self.normal_at(u, v, world=False)
        yaxis = Vector(0.0, 0.0, 1.0)
        xaxis = yaxis.cross(zaxis)
        frame = Frame(point, xaxis, yaxis)
        if world:
            frame.transform(self.transformation)
        return frame
