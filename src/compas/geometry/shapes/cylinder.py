from math import cos
from math import pi
from math import sin
from typing import TYPE_CHECKING
from typing import Self

from compas._typing import CoordinatesType
from compas._typing import CoordinateType
from compas.geometry import Circle
from compas.geometry import Frame
from compas.geometry import Line
from compas.geometry import Plane
from compas.geometry import Point

from .shape import Shape

if TYPE_CHECKING:
    from compas.geometry import Brep


class Cylinder(Shape):
    """A cylinder is defined by a frame, radius, and height.

    The cylinder is oriented along the z-axis of the frame.
    The center of the cylinder is at the origin of the frame. Half of the
    cylinder is above the local XY plane and the other half below.

    Parameters
    ----------
    radius
        The radius of the cylinder.
    height
        The height of the cylinder along the z-axis of the frame.
        Half of the cylinder is above the XY plane of the frame, the other half below.
    frame
        The local coordinate system, or "frame", of the cylinder.
        Default is `None`, in which case the world coordinate system is used.
    name
        The name of the shape.

    Examples
    --------
    >>> frame = Frame.worldXY()
    >>> cylinder = Cylinder(frame=frame, radius=0.3, height=1.0)
    >>> cylinder = Cylinder(radius=0.3, height=1.0)
    >>> cylinder = Cylinder(0.3, 1.0)

    """

    @property
    def __data__(self) -> dict:
        return {
            "radius": self.radius,
            "height": self.height,
            "frame": self.frame.__data__,
        }

    @classmethod
    def __from_data__(cls, data: dict) -> Self:
        return cls(
            radius=data["radius"],
            height=data["height"],
            frame=Frame.__from_data__(data["frame"]),
        )

    def __init__(self, radius: float, height: float, frame: Frame | None = None, name: str | None = None) -> None:
        super().__init__(frame=frame, name=name)
        self._radius: float | None = None
        self._height: float | None = None
        self.radius = radius
        self.height = height

    def __repr__(self) -> str:
        return "{0}(radius={1}, height={2}, frame={3!r})".format(
            type(self).__name__,
            self.radius,
            self.height,
            self.frame,
        )

    # ==========================================================================
    # Properties
    # ==========================================================================

    @property
    def radius(self) -> float:
        """The positive radius of the cylinder."""
        if self._radius is None:
            raise ValueError("The cylinder radius has not been set.")
        return self._radius

    @radius.setter
    def radius(self, radius: float) -> None:
        if radius <= 0:
            raise ValueError("The cylinder radius should be larger than zero.")
        self._radius = float(radius)
        self._invalidate_discretization()

    @property
    def height(self) -> float:
        """The positive height of the cylinder."""
        if self._height is None:
            raise ValueError("The cylinder height has not been set.")
        return self._height

    @height.setter
    def height(self, height: float) -> None:
        if height <= 0:
            raise ValueError("The cylinder height should be larger than zero.")
        self._height = float(height)
        self._invalidate_discretization()

    @property
    def start(self) -> Point:
        """The center point of the lower base."""
        return self.frame.point + self.frame.zaxis * (-0.5 * self.height)

    @property
    def end(self) -> Point:
        """The center point of the upper base."""
        return self.frame.point + self.frame.zaxis * (0.5 * self.height)

    @property
    def axis(self) -> Line:
        """The central axis from the lower to the upper base."""
        return Line(self.start, self.end)

    @property
    def base(self) -> Point:
        """The center point of the lower base."""
        return self.start

    @property
    def plane(self) -> Plane:
        """The plane of the lower base."""
        return Plane(self.start, self.frame.zaxis)

    @property
    def circle(self) -> Circle:
        """The circle forming the lower base."""
        frame = Frame(self.start, self.frame.xaxis, self.frame.yaxis)
        return Circle(radius=self.radius, frame=frame)

    @property
    def diameter(self) -> float:
        """The diameter of the cylinder."""
        return 2 * self.radius

    def area(self) -> float:
        """Compute the total surface area, including both bases."""
        return 2 * pi * self.radius**2 + 2 * pi * self.radius * self.height

    def volume(self) -> float:
        """Compute the volume enclosed by the cylinder."""
        return pi * self.radius**2 * self.height

    # ==========================================================================
    # Constructors
    # ==========================================================================

    @classmethod
    def from_line_and_radius(cls, line: Line, radius: float) -> Self:
        """Construct a cylinder from a line and a radius.

        Parameters
        ----------
        line
            The line.
        radius
            The radius.

        Returns
        -------
        Self
            The cylinder.

        Examples
        --------
        >>> from compas.geometry import Line
        >>> from compas.geometry import Cylinder
        >>> line = Line([0, 0, 0], [0, 0, 1])
        >>> cylinder = Cylinder.from_line_and_radius(line, radius=0.3)

        """
        frame = Frame.from_plane(Plane(line.midpoint, line.direction))
        return cls(frame=frame, height=line.length, radius=radius)

    @classmethod
    def from_circle_and_height(cls, circle: Circle, height: float) -> Self:
        """Construct a cylinder from a circle and a height.

        Parameters
        ----------
        circle
            The circle.
        height
            The height.

        Returns
        -------
        Self
            The cylinder.

        Examples
        --------
        >>> from compas.geometry import Circle
        >>> from compas.geometry import Cylinder
        >>> circle = Circle(radius=0.3)
        >>> cylinder = Cylinder.from_circle_and_height(circle, height=1.0)

        """
        center = circle.frame.point + circle.frame.zaxis * (0.5 * height)
        frame = Frame(center, circle.frame.xaxis, circle.frame.yaxis)
        return cls(frame=frame, height=height, radius=circle.radius)

    # =============================================================================
    # Discretisation
    # =============================================================================

    def _compute_vertices(self, u: int, v: int) -> list[CoordinateType]:
        """Compute the vertices of the discrete representation of the cylinder.

        Returns
        -------
        list[list[float]]

        """
        vertices: list[CoordinateType] = []
        a = 2 * pi / u
        z = self.height / 2
        for i in range(u):
            x = self.radius * cos(i * a)
            y = self.radius * sin(i * a)
            vertices.append([x, y, z])
            vertices.append([x, y, -z])
        # add v in bottom and top's circle center
        vertices.append([0, 0, z])
        vertices.append([0, 0, -z])

        return vertices

    def compute_faces(self, u: int | None = None, v: int | None = None) -> list[list[int]]:
        """Compute the faces of the discrete representation of the cylinder.

        Returns
        -------
        list[list[int]]

        """
        u, _ = self._resolutions(u, v)

        faces = []
        # side faces
        for i in range(0, u * 2, 2):
            faces.append([i, i + 1, (i + 3) % (u * 2), (i + 2) % (u * 2)])
        # top and bottom circle faces
        for i in range(0, u * 2, 2):
            top = [i, (i + 2) % (u * 2), u * 2]
            bottom = [i + 1, (i + 3) % (u * 2), u * 2 + 1]
            faces.append(top)
            faces.append(bottom[::-1])

        return faces

    # =============================================================================
    # Conversions
    # =============================================================================

    def to_brep(self) -> "Brep":
        """Return a BRep representation of the cylinder.

        Returns
        -------
        Brep

        """
        from compas.geometry import Brep

        return Brep.from_cylinder(self)

    # =============================================================================
    # Transformations
    # =============================================================================

    def scale(self, x: float, y: float | None = None, z: float | None = None) -> None:
        """Scale the cylinder by multiplying the radius and height by a factor.

        Parameters
        ----------
        x
            The uniform scaling factor.
        y
            An optional scaling factor that must equal `x`.
        z
            An optional scaling factor that must equal `x`.

        """
        if (y is not None and y != x) or (z is not None and z != x):
            raise ValueError("A cylinder only supports uniform scaling.")
        self.radius *= x
        self.height *= x

    # =============================================================================
    # Methods
    # =============================================================================

    def contains_point(self, point: CoordinateType, tol: float = 1e-6) -> bool:
        """Verify if a point is inside the cylinder.

        Parameters
        ----------
        point
            The point.
        tol
            The tolerance for the verification.

        Returns
        -------
        bool
            True if the point is inside the cylinder.
            False otherwise.

        """
        x, y, z = self.frame.to_local_coordinates(point)

        if z > self.height / 2 + tol:
            return False
        if z < -self.height / 2 - tol:
            return False

        return x**2 + y**2 <= (self.radius + tol) ** 2

    def contains_points(self, points: CoordinatesType, tol: float = 1e-6) -> list[bool]:
        """Verify whether points are inside the cylinder.

        Parameters
        ----------
        points
            The points to test.
        tol
            The tolerance for the test.

        Returns
        -------
        list[bool]

        """
        return [self.contains_point(point, tol=tol) for point in points]
