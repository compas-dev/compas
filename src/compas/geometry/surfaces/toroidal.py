from math import cos
from math import pi
from math import sin
from typing import Any
from typing import Optional

from typing_extensions import Self

from compas._typing import CoordinateType
from compas.geometry import Circle
from compas.geometry import Frame
from compas.geometry import Plane
from compas.geometry import Point
from compas.geometry import Vector

from .surface import Surface

PI2 = 2 * pi


class ToroidalSurface(Surface):
    """A ring torus defined by an axis radius, pipe radius, and frame.

    Parameters
    ----------
    radius_axis
        The distance from the torus axis to the center of the pipe.
    radius_pipe
        The radius of the pipe. It must be smaller than `radius_axis`.
    frame
        The local coordinate frame. If `None`, the world XY frame is used.
    name
        The name of the surface.

    Examples
    --------
    >>> torus = ToroidalSurface(radius_axis=2.0, radius_pipe=0.5)
    >>> torus.point_at(0.0, 0.0)
    Point(x=2.500, y=0.000, z=0.000)

    A toroidal surface can also be constructed from a plane.

    >>> torus = ToroidalSurface.from_plane_and_radii(Plane.worldXY(), 2.0, 0.5)
    >>> torus.radius_axis, torus.radius_pipe
    (2.0, 0.5)

    """


    @property
    def __data__(self) -> dict[str, Any]:
        """The data representation of the toroidal surface."""
        return {
            "radius_axis": self.radius_axis,
            "radius_pipe": self.radius_pipe,
            "frame": self.frame.__data__,
        }

    @classmethod
    def __from_data__(cls, data: dict[str, Any]) -> Self:
        return cls(
            radius_axis=data["radius_axis"],
            radius_pipe=data["radius_pipe"],
            frame=Frame.__from_data__(data["frame"]),
        )

    def __init__(
        self,
        radius_axis: float,
        radius_pipe: float,
        frame: Optional[Frame] = None,
        name: Optional[str] = None,
    ) -> None:
        super().__init__(frame=frame, name=name)
        self._radius_axis: Optional[float] = None
        self._radius_pipe: Optional[float] = None
        self.radius_axis = radius_axis
        self.radius_pipe = radius_pipe

    def __repr__(self) -> str:
        return "{0}(radius_axis={1}, radius_pipe={2}, frame={3!r})".format(
            type(self).__name__,
            self.radius_axis,
            self.radius_pipe,
            self.frame,
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ToroidalSurface):
            return False
        return self.radius_axis == other.radius_axis and self.radius_pipe == other.radius_pipe and self.frame == other.frame

    # =============================================================================
    # Properties
    # =============================================================================

    @property
    def center(self) -> Point:
        """The center point on the torus axis.

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
    def radius_axis(self) -> float:
        """The radius from the torus axis to the pipe center."""
        if self._radius_axis is None:
            raise ValueError("The radius of the surface main axis has not been set yet.")
        return self._radius_axis

    @radius_axis.setter
    def radius_axis(self, radius: float) -> None:
        if radius <= 0:
            raise ValueError("The axis radius of a torus should be larger than zero.")
        if self._radius_pipe is not None and radius <= self._radius_pipe:
            raise ValueError("The axis radius of a ring torus should be larger than its pipe radius.")
        self._radius_axis = float(radius)

    @property
    def radius_pipe(self) -> float:
        """The positive radius of the torus pipe."""
        if self._radius_pipe is None:
            raise ValueError("The pipe radius of the surface has not been set yet.")
        return self._radius_pipe

    @radius_pipe.setter
    def radius_pipe(self, radius: float) -> None:
        if radius <= 0:
            raise ValueError("The pipe radius of a torus should be larger than zero.")
        if self._radius_axis is not None and radius >= self._radius_axis:
            raise ValueError("The pipe radius of a ring torus should be smaller than its axis radius.")
        self._radius_pipe = float(radius)

    @property
    def area(self) -> float:
        """The surface area of the torus."""
        return 4.0 * pi**2 * self.radius_axis * self.radius_pipe

    @property
    def volume(self) -> float:
        """The volume enclosed by the torus."""
        return 2.0 * pi**2 * self.radius_axis * self.radius_pipe**2

    # =============================================================================
    # Constructors
    # =============================================================================

    @classmethod
    def from_plane_and_radii(cls, plane: Plane, radius_axis: float, radius_pipe: float) -> Self:
        """Construct a toroidal surface from a plane and two radii.

        Parameters
        ----------
        plane
            The plane of the torus.
        radius_axis
            The distance from the torus axis to the pipe center.
        radius_pipe
            The radius of the pipe.

        Returns
        -------
        ToroidalSurface
            The constructed toroidal surface.

        """
        return cls(radius_axis, radius_pipe, frame=Frame.from_plane(plane))

    # =============================================================================
    # Conversions
    # =============================================================================

    # =============================================================================
    # Methods
    # =============================================================================

    def isocurve_u(self, u: float) -> Circle:
        """Compute a pipe circle at a U parameter.

        Parameters
        ----------
        u
            The U parameter.

        Returns
        -------
        Circle
            The pipe circle.

        """
        angle = u * PI2
        radial = self.frame.xaxis * cos(angle) + self.frame.yaxis * sin(angle)
        origin = self.center + radial * self.radius_axis
        return Circle(self.radius_pipe, frame=Frame(origin, radial, self.frame.zaxis))

    def isocurve_v(self, v: float) -> Circle:
        """Compute a circle around the torus axis at a V parameter.

        Parameters
        ----------
        v
            The V parameter.

        Returns
        -------
        Circle
            The circular isocurve around the torus axis.

        """
        angle = v * PI2
        radius = self.radius_axis + self.radius_pipe * cos(angle)
        origin = self.center + self.frame.zaxis * (self.radius_pipe * sin(angle))
        return Circle(radius, frame=Frame(origin, self.frame.xaxis, self.frame.yaxis))

    def point_at(self, u: float, v: float, world: bool = True) -> Point:
        """Compute a point on the toroidal surface.

        Parameters
        ----------
        u
            The U parameter around the torus axis, mapped to `[0, 2 * pi]`.
        v
            The V parameter around the pipe, mapped to `[0, 2 * pi]`.
        world
            If `True`, return the point in world coordinates.

        Returns
        -------
        Point
            The point at the given parameters.

        """
        u = u * PI2
        v = v * PI2
        x = (self.radius_axis + self.radius_pipe * cos(v)) * cos(u)
        y = (self.radius_axis + self.radius_pipe * cos(v)) * sin(u)
        z = self.radius_pipe * sin(v)
        point = Point(x, y, z)
        if world:
            point.transform(self.transformation)
        return point

    def normal_at(self, u: float, v: float, world: bool = True) -> Vector:
        """Compute the outward normal at a point on the toroidal surface.

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
        v = v * PI2
        normal = Vector(cos(v) * cos(u), cos(v) * sin(u), sin(v))
        if world:
            normal.transform(self.transformation)
        return normal

    def frame_at(self, u: float, v: float, world: bool = True) -> Frame:
        """Compute a frame at a point on the toroidal surface.

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
            its Y-axis follows increasing V, and its Z-axis is outward.

        """
        angle_u = u * PI2
        angle_v = v * PI2
        point = self.point_at(u, v, world=False)
        tangent_u = Vector(-sin(angle_u), cos(angle_u), 0.0)
        tangent_v = Vector(-cos(angle_u) * sin(angle_v), -sin(angle_u) * sin(angle_v), cos(angle_v))
        frame = Frame(point, tangent_u, tangent_v)
        if world:
            frame.transform(self.transformation)
        return frame
