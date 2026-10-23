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
from compas.geometry import Point

from .shape import Shape

if TYPE_CHECKING:
    from compas.geometry import Brep


class Sphere(Shape):
    """A sphere is defined by a point and a radius.

    Parameters
    ----------
    radius
        The radius of the sphere.
    frame
        The local coordinates system, or "frame", of the sphere.
        Default is `None`, in which case the sphere is constructed in world coordinates.
    name
        The name of the shape.

    Examples
    --------
    >>> from compas.geometry import Frame
    >>> from compas.geometry import Sphere
    >>> sphere1 = Sphere(frame=Frame.worldXY(), radius=5)
    >>> sphere1 = Sphere(radius=5)

    """

    @property
    def __data__(self) -> dict:
        return {
            "radius": self.radius,
            "frame": self.frame.__data__,
        }

    @classmethod
    def __from_data__(cls, data: dict) -> Self:
        return cls(
            radius=data["radius"],
            frame=Frame.__from_data__(data["frame"]),
        )

    def __init__(self, radius: float, frame: Frame | None = None, name: str | None = None) -> None:
        super().__init__(frame=frame, name=name)
        self._radius: float | None = None
        self.radius = radius

    def __repr__(self) -> str:
        return "{0}(radius={1}, frame={2!r})".format(
            type(self).__name__,
            self.radius,
            self.frame,
        )

    # ==========================================================================
    # Properties
    # ==========================================================================

    @property
    def base(self) -> Point:
        """The center point of the sphere."""
        return self.frame.point

    @property
    def radius(self) -> float:
        """The positive radius of the sphere."""
        if self._radius is None:
            raise ValueError("The radius of the sphere is not set.")
        return self._radius

    @radius.setter
    def radius(self, radius: float) -> None:
        if radius <= 0:
            raise ValueError("The radius of the sphere should be larger than zero.")
        self._radius = float(radius)
        self._invalidate_discretization()

    @property
    def start(self) -> Point:
        """The point at the negative end of the local z-axis."""
        return self.frame.point + self.frame.zaxis * -self.radius

    @property
    def end(self) -> Point:
        """The point at the positive end of the local z-axis."""
        return self.frame.point + self.frame.zaxis * +self.radius

    @property
    def axis(self) -> Line:
        """The diameter line along the local z-axis."""
        return Line(self.start, self.end)

    @property
    def circle(self) -> Circle:
        """The equatorial circle in the local XY plane."""
        return Circle(self.radius, frame=self.frame)

    def area(self) -> float:
        """Compute the surface area of the sphere."""
        return 4 * pi * self.radius**2

    def volume(self) -> float:
        """Compute the volume enclosed by the sphere."""
        return 4.0 / 3.0 * pi * self.radius**3

    # ==========================================================================
    # Constructors
    # ==========================================================================

    @classmethod
    def from_point_and_radius(cls, point: CoordinateType, radius: float) -> Self:
        """Construct a sphere from a point and a radius.

        Parameters
        ----------
        point
            The center of the sphere.
        radius
            The radius of the sphere.

        Returns
        -------
        Self
            The constructed sphere.

        """
        frame = Frame.worldXY()
        frame.point = point
        return cls(frame=frame, radius=radius)

    # ==========================================================================
    # Discretisation
    # ==========================================================================

    def _compute_vertices(self, u: int, v: int) -> list[CoordinateType]:
        """Compute the vertices of the discrete representation of the sphere.

        Returns
        -------
        list[list[float]]

        """
        theta = pi / v
        phi = pi * 2 / u
        hpi = pi * 0.5

        x, y, z = 0, 0, 0

        vertices: list[CoordinateType] = []
        for i in range(1, v):
            for j in range(u):
                tx = self.radius * cos(i * theta - hpi) * cos(j * phi) + x
                ty = self.radius * cos(i * theta - hpi) * sin(j * phi) + y
                tz = self.radius * sin(i * theta - hpi) + z
                vertices.append([tx, ty, tz])

        vertices.append([x, y, z + self.radius])
        vertices.append([x, y, z - self.radius])

        return vertices

    def compute_faces(self, u: int | None = None, v: int | None = None) -> list[list[int]]:
        """Compute the faces of the discrete representation of the sphere.

        Returns
        -------
        list[list[int]]

        """
        u, v = self._resolutions(u, v)

        faces = []
        vertex_count = (v - 1) * u + 2

        # south pole triangle fan
        sp = vertex_count - 1
        for j in range(u):
            faces.append([sp, (j + 1) % u, j])

        for i in range(v - 2):
            for j in range(u):
                jj = (j + 1) % u
                a = i * u + j
                b = i * u + jj
                c = (i + 1) * u + jj
                d = (i + 1) * u + j
                faces.append([a, b, c, d])

        # north pole triangle fan
        np = vertex_count - 2
        for j in range(u):
            nc = vertex_count - 3 - j
            nn = vertex_count - 3 - (j + 1) % u
            faces.append([np, nn, nc])

        return faces

    # ==========================================================================
    # Conversions
    # ==========================================================================

    def to_brep(self) -> "Brep":
        """Return a BRep representation of the sphere.

        Returns
        -------
        Brep

        """
        from compas.geometry import Brep

        return Brep.from_sphere(self)

    # =============================================================================
    # Transformations
    # =============================================================================

    def scale(self, x: float, y: float | None = None, z: float | None = None) -> None:
        """Scale the sphere.

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
            raise ValueError("A sphere only supports uniform scaling.")
        self.radius *= x

    # =============================================================================
    # Methods
    # =============================================================================

    def contains_point(self, point: CoordinateType, tol: float = 1e-6) -> bool:
        """Verify if a point is inside the sphere.

        Parameters
        ----------
        point
            The point to test.
        tol
            The tolerance for the test.

        Returns
        -------
        bool
            True if the point is inside the sphere.
            False otherwise.

        """
        return self.frame.point.distance_to_point(point) <= self.radius + tol

    def contains_points(self, points: CoordinatesType, tol: float = 1e-6) -> list[bool]:
        """Verify if a list of points are inside the sphere.

        Parameters
        ----------
        points
            The points to test.
        tol
            The tolerance for the test.

        Returns
        -------
        list[bool]
            A list of booleans indicating for each point if it is inside the sphere.

        """
        return [self.contains_point(point, tol=tol) for point in points]
