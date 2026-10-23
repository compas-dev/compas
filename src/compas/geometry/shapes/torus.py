from math import cos
from math import pi
from math import sin
from math import sqrt
from typing import TYPE_CHECKING
from typing import Self

from compas._typing import CoordinatesType
from compas._typing import CoordinateType
from compas.geometry import Frame
from compas.geometry import Plane
from compas.geometry import Point

from .shape import Shape

if TYPE_CHECKING:
    from compas.geometry import Brep


class Torus(Shape):
    """A torus is defined by a plane and two radii.

    Parameters
    ----------
    radius_axis
        The radius of the axis.
    radius_pipe
        The radius of the pipe.
    frame
        The local coordinate system of the torus.
        Default is `None`, in which case the torus is constructed in the world XY plane.
    name
        The name of the shape.

    Examples
    --------
    >>> from compas.geometry import Frame
    >>> from compas.geometry import Torus
    >>> torus = Torus(frame=Frame.worldXY(), radius_axis=5.0, radius_pipe=2.0)
    >>> torus = Torus(radius_axis=5.0, radius_pipe=2.0)

    """

    @property
    def __data__(self) -> dict:
        return {
            "radius_axis": self.radius_axis,
            "radius_pipe": self.radius_pipe,
            "frame": self.frame.__data__,
        }

    @classmethod
    def __from_data__(cls, data: dict) -> Self:
        return cls(
            radius_axis=data["radius_axis"],
            radius_pipe=data["radius_pipe"],
            frame=Frame.__from_data__(data["frame"]),
        )

    def __init__(
        self,
        radius_axis: float,
        radius_pipe: float,
        frame: Frame | None = None,
        name: str | None = None,
    ) -> None:
        super().__init__(frame=frame, name=name)
        self._radius_axis: float | None = None
        self._radius_pipe: float | None = None
        self.radius_axis = radius_axis
        self.radius_pipe = radius_pipe

    def __repr__(self) -> str:
        return "Torus(frame={0!r}, radius_axis={1!r}, radius_pipe={2!r})".format(
            self.frame,
            self.radius_axis,
            self.radius_pipe,
        )

    # ==========================================================================
    # Properties
    # ==========================================================================

    @property
    def plane(self) -> Plane:
        """The equatorial plane of the torus."""
        return Plane(self.frame.point, self.frame.zaxis)

    @property
    def radius_axis(self) -> float:
        """The radius from the torus axis to the pipe center."""
        if self._radius_axis is None:
            raise ValueError("The torus has no axis radius.")
        return self._radius_axis

    @radius_axis.setter
    def radius_axis(self, radius: float) -> None:
        if radius <= 0:
            raise ValueError("The axis radius of a torus should be larger than zero.")
        if self._radius_pipe is not None and radius <= self._radius_pipe:
            raise ValueError("The axis radius of a ring torus should be larger than its pipe radius.")
        self._radius_axis = float(radius)
        self._invalidate_discretization()

    @property
    def radius_pipe(self) -> float:
        """The positive radius of the torus pipe."""
        if self._radius_pipe is None:
            raise ValueError("The torus has no pipe radius.")
        return self._radius_pipe

    @radius_pipe.setter
    def radius_pipe(self, radius: float) -> None:
        if radius <= 0:
            raise ValueError("The pipe radius of a torus should be larger than zero.")
        if self._radius_axis is not None and radius >= self._radius_axis:
            raise ValueError("The pipe radius of a ring torus should be smaller than its axis radius.")
        self._radius_pipe = float(radius)
        self._invalidate_discretization()

    @property
    def center(self) -> Point:
        """The center point of the torus."""
        return self.frame.point

    def area(self) -> float:
        """Compute the surface area of the torus."""
        return (2 * pi * self.radius_pipe) * (2 * pi * self.radius_axis)

    def volume(self) -> float:
        """Compute the volume enclosed by the torus."""
        return (pi * self.radius_pipe**2) * (2 * pi * self.radius_axis)

    # ==========================================================================
    # Constructors
    # ==========================================================================

    @classmethod
    def from_plane_and_radii(cls, plane: Plane, radius_axis: float, radius_pipe: float) -> Self:
        """Construct a torus from a plane and two radii.

        Parameters
        ----------
        plane
            The plane of the torus.
        radius_axis
            The radius of the axis.
        radius_pipe
            The radius of the pipe.

        Returns
        -------
        Self
            The constructed torus.

        Examples
        --------
        >>> from compas.geometry import Plane
        >>> from compas.geometry import Torus
        >>> plane = Plane.worldXY()
        >>> torus = Torus.from_plane_and_radii(plane, 5.0, 2.0)

        """
        frame = Frame.from_plane(plane)
        return cls(radius_axis=radius_axis, radius_pipe=radius_pipe, frame=frame)

    # ==========================================================================
    # Discretisation
    # ==========================================================================

    def _compute_vertices(self, u: int, v: int) -> list[CoordinateType]:
        """Compute the vertices of the discrete representation of the torus.

        Returns
        -------
        list[list[float]]

        """
        theta = pi * 2 / u
        phi = pi * 2 / v

        vertices: list[CoordinateType] = []
        for i in range(u):
            for j in range(v):
                x = cos(i * theta) * (self.radius_axis + self.radius_pipe * cos(j * phi))
                y = sin(i * theta) * (self.radius_axis + self.radius_pipe * cos(j * phi))
                z = self.radius_pipe * sin(j * phi)
                vertices.append([x, y, z])

        return vertices

    def compute_faces(self, u: int | None = None, v: int | None = None) -> list[list[int]]:
        """Compute the faces of the discrete representation of the torus.

        Returns
        -------
        list[list[int]]

        """
        u, v = self._resolutions(u, v)

        faces = []
        for i in range(u):
            ii = (i + 1) % u
            for j in range(v):
                jj = (j + 1) % v
                a = i * v + j
                b = ii * v + j
                c = ii * v + jj
                d = i * v + jj
                faces.append([a, b, c, d])

        return faces

    # ==========================================================================
    # Conversions
    # ==========================================================================

    def to_brep(self) -> "Brep":
        """Return a BRep representation of the torus.

        Returns
        -------
        Brep

        """
        from compas.geometry import Brep

        return Brep.from_torus(self)

    # ==========================================================================
    # Transformations
    # ==========================================================================

    def scale(self, x: float, y: float | None = None, z: float | None = None) -> None:
        """Scale the torus by multiplying the axis radius and pipe radius by a factor.

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
            raise ValueError("A torus only supports uniform scaling.")
        if x <= 0:
            raise ValueError("The scaling factor should be larger than zero.")
        # Update both radii atomically so the ring-torus invariant is preserved
        # while scaling down as well as while scaling up.
        self._radius_axis = self.radius_axis * x
        self._radius_pipe = self.radius_pipe * x

    # ==========================================================================
    # Methods
    # ==========================================================================

    def contains_point(self, point: CoordinateType, tol: float = 1e-6) -> bool:
        """Verify whether a point is inside the torus.

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
        radial = sqrt(x**2 + y**2) - self.radius_axis
        return radial**2 + z**2 <= (self.radius_pipe + tol) ** 2

    def contains_points(self, points: CoordinatesType, tol: float = 1e-6) -> list[bool]:
        """Verify whether points are inside the torus.

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
