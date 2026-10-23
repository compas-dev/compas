from math import cos
from math import pi
from math import sin
from math import sqrt
from typing import TYPE_CHECKING
from typing import Self

from compas._typing import CoordinatesType
from compas._typing import CoordinateType
from compas.geometry import Circle
from compas.geometry import Frame
from compas.geometry import Line
from compas.geometry import Plane

from .shape import Shape

if TYPE_CHECKING:
    from compas.geometry import Brep


class Cone(Shape):
    """A cone is defined by a frame, radius, and height.

    The cone is oriented along the z-axis of the frame.
    The base point of the cone (i.e. the centre of the base circle) is at the origin of the frame.
    The entire cone is in the positive z-direction.

    Parameters
    ----------
    frame
        The local coordinate system of the cone.
        Default is `None`, in which case the world coordinate system is used.
    radius
        The radius of the base of the cone.
    height
        The height of the cone along the z-axis of the frame.
        The base of the cone is at the origin of the frame.
        The entire cone is above the XY plane of the frame.
    name
        The name of the shape.

    Examples
    --------
    >>> frame = Frame.worldXY()
    >>> cone = Cone(frame=frame, radius=0.3, height=1.0)
    >>> cone = Cone(radius=0.3, height=1.0)
    >>> cone = Cone(0.3, 1.0)

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
        """The positive radius of the cone base."""
        if self._radius is None:
            raise ValueError("The cone radius has not been set.")
        return self._radius

    @radius.setter
    def radius(self, radius: float) -> None:
        if radius <= 0:
            raise ValueError("The cone radius should be larger than zero.")
        self._radius = float(radius)
        self._invalidate_discretization()

    @property
    def height(self) -> float:
        """The positive distance from the base to the apex."""
        if self._height is None:
            raise ValueError("The cone height has not been set.")
        return self._height

    @height.setter
    def height(self, height: float) -> None:
        if height <= 0:
            raise ValueError("The cone height should be larger than zero.")
        self._height = float(height)
        self._invalidate_discretization()

    @property
    def axis(self) -> Line:
        """The axis from the center of the base to the apex."""
        return Line(self.frame.point, self.frame.point + self.frame.normal * self.height)

    @property
    def circle(self) -> Circle:
        """The circle forming the base of the cone."""
        return Circle(self.radius, frame=self.frame)

    @property
    def diameter(self) -> float:
        """The diameter of the cone base."""
        return 2 * self.radius

    def area(self) -> float:
        """Compute the total surface area, including the base."""
        r = self.radius
        h = self.height
        return pi * r * (r + sqrt(h**2 + r**2))

    def volume(self) -> float:
        """Compute the volume enclosed by the cone."""
        r = self.radius
        h = self.height
        return pi * r**2 * (h / 3)

    # ==========================================================================
    # Constructors
    # ==========================================================================

    @classmethod
    def from_line_and_radius(cls, line: Line, radius: float) -> Self:
        """Construct a cone from a line and a radius.

        Parameters
        ----------
        line
            The axis of the cone.
        radius
            The radius of the base circle of the cone.

        Returns
        -------
        Self
            The cone.

        See Also
        --------
        [`Cone.from_circle_and_height`][compas.geometry.Cone.from_circle_and_height]

        Examples
        --------
        >>> from compas.geometry import Line
        >>> line = Line([0, 0, 0], [0, 0, 1])
        >>> cone = Cone.from_line_and_radius(line, 0.3)

        """
        frame = Frame.from_plane(Plane(line.start, line.direction))
        return cls(frame=frame, radius=radius, height=line.length)

    @classmethod
    def from_circle_and_height(cls, circle: Circle, height: float) -> Self:
        """Construct a cone from a circle and a height.

        Parameters
        ----------
        circle
            The base circle of the cone.
        height
            The height of the cone.

        Returns
        -------
        Self
            The cone.

        See Also
        --------
        [`Cone.from_line_and_radius`][compas.geometry.Cone.from_line_and_radius]

        Examples
        --------
        >>> circle = Circle(0.3)
        >>> cone = Cone.from_circle_and_height(circle, 1.0)

        """
        frame = circle.frame
        return cls(frame=frame, radius=circle.radius, height=height)

    # =============================================================================
    # Discretisation
    # =============================================================================

    def _compute_vertices(self, u: int, v: int) -> list[CoordinateType]:
        """Compute the vertices of the discrete representation of the cone.

        Returns
        -------
        list[list[float]]

        """
        vertices: list[CoordinateType] = [[0, 0, 0]]
        a = 2 * pi / u
        radius = self.circle.radius
        for i in range(u):
            x = radius * cos(i * a)
            y = radius * sin(i * a)
            vertices.append([x, y, 0])
        vertices.append([0, 0, self.height])

        return vertices

    def compute_faces(self, u: int | None = None, v: int | None = None) -> list[list[int]]:
        """Compute the faces of the discrete representation of the cone.

        Returns
        -------
        list[list[int]]

        """
        u, _ = self._resolutions(u, v)
        faces = []
        first = 0
        last = u + 1
        for i in range(1, last - 1):
            j = i + 1
            faces.append([i, j, last])
            faces.append([j, i, first])
        faces.append([last - 1, 1, last])
        faces.append([1, last - 1, first])

        return faces

    # ==========================================================================
    # Conversions
    # ==========================================================================

    def to_brep(self) -> "Brep":
        """Return a BRep representation of the cone.

        Returns
        -------
        Brep

        """
        from compas.geometry import Brep

        return Brep.from_cone(self)

    # ==========================================================================
    # Transformations
    # ==========================================================================

    def scale(self, x: float, y: float | None = None, z: float | None = None) -> None:
        """Scale the cone by multiplying the radius and height by a factor.

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
            raise ValueError("A cone only supports uniform scaling.")
        self.radius *= x
        self.height *= x

    # ==========================================================================
    # Methods
    # ==========================================================================

    def contains_point(self, point: CoordinateType, tol: float = 1e-6) -> bool:
        """Verify whether a point is inside the cone.

        Parameters
        ----------
        point
            The point to test.
        tol
            The tolerance for the test.

        Returns
        -------
        bool

        """
        x, y, z = self.frame.to_local_coordinates(point)
        if z < -tol or z > self.height + tol:
            return False
        radius = self.radius * max(0.0, 1.0 - z / self.height) + tol
        return x**2 + y**2 <= radius**2

    def contains_points(self, points: CoordinatesType, tol: float = 1e-6) -> list[bool]:
        """Verify whether points are inside the cone.

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
