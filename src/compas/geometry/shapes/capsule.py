from math import cos
from math import pi
from math import sin
from typing import Self

from compas._typing import CoordinatesType
from compas._typing import CoordinateType
from compas.geometry import Circle
from compas.geometry import Frame
from compas.geometry import Line
from compas.geometry import Plane
from compas.geometry import Point
from compas.geometry import Transformation
from compas.geometry import transform_points

from .shape import Shape


class Capsule(Shape):
    """A capsule is defined by a frame, radius, and height.

    The capsule is oriented along the z-axis of the frame.
    The base point (i.e. the centre of the base circle) is at the origin of the frame.
    Half of the capsule is above the local XY plane of the frame, the other half below.

    Parameters
    ----------
    radius
        The radius of the capsule.
    height
        The height of the capsule along the z-axis of the frame.
        Half of the capsule is above the XY plane of the frame, the other half below.
    frame
        The local coordinate system, or "frame", of the capsule.
        Default is `None`, in which case the world coordinate system is used.
    name
        The name of the shape.

    Examples
    --------
    >>> frame = Frame.worldXY()
    >>> capsule = Capsule(radius=0.3, height=1.0, frame=frame)
    >>> capsule = Capsule(radius=0.3, height=1.0)
    >>> capsule = Capsule(3.0, 1.0)

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
        """The radius of the capsule."""
        if self._radius is None:
            raise ValueError("The radius of the capsule is not set.")
        return self._radius

    @radius.setter
    def radius(self, radius: float) -> None:
        if radius < 0:
            raise ValueError("The radius of the capsule should be greater than or equal to zero.")
        self._radius = float(radius)
        self._invalidate_discretization()

    @property
    def height(self) -> float:
        """The length of the cylindrical section along the local z-axis."""
        if self._height is None:
            raise ValueError("The capsule has no height.")
        return self._height

    @height.setter
    def height(self, height: float) -> None:
        if height < 0:
            raise ValueError("The height of the capsule should be greater than or equal to zero.")
        self._height = float(height)
        self._invalidate_discretization()

    @property
    def length(self) -> float:
        """The length of the cylindrical section."""
        return self.height

    @property
    def start(self) -> Point:
        """The center of the lower hemispherical cap."""
        return self.frame.point + self.frame.zaxis * (-0.5 * self.height)

    @property
    def end(self) -> Point:
        """The center of the upper hemispherical cap."""
        return self.frame.point + self.frame.zaxis * self.height / 2

    @property
    def axis(self) -> Line:
        """The axis between the centers of the hemispherical caps."""
        return Line(self.start, self.end)

    @property
    def circle(self) -> Circle:
        """The circle at the middle of the cylindrical section."""
        return Circle(self.radius, frame=self.frame)

    def volume(self) -> float:
        """Compute the volume of the capsule."""
        # cylinder plus 2 half spheres
        cylinder = self.radius**2 * pi * self.height
        caps = 4.0 / 3.0 * pi * self.radius**3
        return cylinder + caps

    def area(self) -> float:
        """Compute the surface area of the capsule."""
        # cylinder minus caps plus 2 half spheres
        cylinder = self.radius * 2 * pi * self.height
        caps = 4 * pi * self.radius**2
        return cylinder + caps

    # ==========================================================================
    # Constructors
    # ==========================================================================

    @classmethod
    def from_line_and_radius(cls, line: Line, radius: float) -> Self:
        """Construct a capsule from a line and a radius.

        Parameters
        ----------
        line
            The line.
        radius
            The radius.

        Returns
        -------
        Self
            The constructed capsule.

        See Also
        --------
        [`Capsule.from_circle_and_height`][compas.geometry.Capsule.from_circle_and_height]

        Examples
        --------
        >>> line = Line([0, 0, 0], [0, 0, 1])
        >>> capsule = Capsule.from_line_and_radius(line, 0.3)

        """
        frame = Frame.from_plane(Plane(line.midpoint, line.direction))
        return cls(frame=frame, radius=radius, height=line.length)

    @classmethod
    def from_circle_and_height(cls, circle: Circle, height: float) -> Self:
        """Construct a capsule from a circle and a height.

        Parameters
        ----------
        circle
            The circle.
        height
            The height.

        Returns
        -------
        Self
            The constructed capsule.

        See Also
        --------
        [`Capsule.from_line_and_radius`][compas.geometry.Capsule.from_line_and_radius]

        Examples
        --------
        >>> circle = Circle(0.3)
        >>> capsule = Capsule.from_circle_and_height(circle, 1.0)

        """
        return cls(frame=circle.frame, radius=circle.radius, height=height)

    # =============================================================================
    # Discretisation
    # =============================================================================

    def _compute_vertices(self, u: int, v: int) -> list[CoordinateType]:
        """Compute the vertices of the discrete representation of the capsule.

        Returns
        -------
        list[list[float]]

        """
        if v % 2 == 1:
            v += 1

        theta = pi / v
        phi = pi * 2 / u
        hpi = pi * 0.5
        halfheight = self.height / 2
        sidemult = -1
        capswitch = 0

        vertices = []
        for i in range(1, v + 1):
            for j in range(u):
                a = i + capswitch
                tx = self.radius * cos(a * theta - hpi) * cos(j * phi)
                ty = self.radius * cos(a * theta - hpi) * sin(j * phi)
                tz = self.radius * sin(a * theta - hpi) + sidemult * halfheight
                vertices.append([tx, ty, tz])
            # switch from lower pole cap to upper pole cap
            if i == v / 2 and sidemult == -1:
                capswitch = -1
                sidemult *= -1

        vertices.append([0, 0, halfheight + self.radius])
        vertices.append([0, 0, -halfheight - self.radius])

        return vertices

    def compute_faces(self, u: int | None = None, v: int | None = None) -> list[list[int]]:
        """Compute the faces of the discrete representation of the capsule.

        Returns
        -------
        list[list[int]]

        """
        u, v = self._resolutions(u, v)

        if v % 2 == 1:
            v += 1

        faces = []

        # south pole triangle fan
        vertex_count = v * u + 2
        sp = vertex_count - 1
        for j in range(u):
            faces.append([sp, (j + 1) % u, j])

        for i in range(v - 1):
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

    # =============================================================================
    # Transformations
    # =============================================================================

    def scale(self, x: float, y: float | None = None, z: float | None = None) -> None:
        """Scale the capsule.

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
            raise ValueError("A capsule only supports uniform scaling.")
        self.radius *= x
        self.height *= x

    # =============================================================================
    # Methods
    # =============================================================================

    def contains_point(self, point: CoordinateType, tol: float = 1e-6) -> bool:
        """Verify if a point is inside the capsule.

        Parameters
        ----------
        point
            The point.
        tol
            The tolerance for the test.

        Returns
        -------
        bool
            True if the point is inside the capsule.
            False otherwise.

        See Also
        --------
        contains_points

        """
        T = Transformation.from_change_of_basis(Frame.worldXY(), self.frame)
        x, y, z = transform_points([point], T)[0]
        halfheight = 0.5 * self.height
        h = halfheight + tol

        if -h <= z <= +h:
            if x**2 + y**2 > (self.radius + tol) ** 2:
                return False

        if z > +h:
            if x**2 + y**2 + (z - halfheight) ** 2 > (self.radius + tol) ** 2:
                return False

        if z < -h:
            if x**2 + y**2 + (z + halfheight) ** 2 > (self.radius + tol) ** 2:
                return False

        return True

    def contains_points(self, points: CoordinatesType, tol: float = 1e-6) -> list[bool]:
        """Verify if a list of points is inside the capsule.

        Parameters
        ----------
        points
            The points.
        tol
            The tolerance for the test.

        Returns
        -------
        list of bool
            For each point, True if the point is inside the capsule.
            False otherwise.

        See Also
        --------
        contains_point

        """
        T = Transformation.from_change_of_basis(Frame.worldXY(), self.frame)
        points = transform_points(points, T)

        halfheight = 0.5 * self.height
        h = halfheight + tol
        r2 = (self.radius + tol) ** 2
        results = [False] * len(points)

        for i, (x, y, z) in enumerate(points):
            if -h <= z <= +h:
                if x**2 + y**2 > r2:
                    continue

            if z > +h:
                if x**2 + y**2 + (z - halfheight) ** 2 > r2:
                    continue

            if z < -h:
                if x**2 + y**2 + (z + halfheight) ** 2 > r2:
                    continue

            results[i] = True

        return results
