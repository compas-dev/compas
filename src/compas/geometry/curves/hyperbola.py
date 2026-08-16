from math import cosh
from math import inf
from math import sinh
from math import sqrt
from typing import Any
from typing import Literal
from typing import Optional

from typing_extensions import Self

from compas._typing import CoordinateType
from compas.geometry import Frame
from compas.geometry import Point
from compas.geometry import Vector

from ..line import Line
from .conic import Conic


class Hyperbola(Conic):
    r"""A single branch of a hyperbola.

    In local coordinates the branch is parameterized by

    $$
    x(u) = s a \cosh(u), \qquad y(u) = b \sinh(u),
    $$

    where $a$ and $b$ are the semi-major and semi-minor axis lengths and
    $s$ is the branch sign. The parameter domain is the entire real line.

    Parameters
    ----------
    major
        The positive semi-major axis length.
    minor
        The positive semi-minor axis length.
    branch
        `1` for the positive-x branch or `-1` for the negative-x branch.
    frame
        The local coordinate frame. Default is the world XY frame.
    name
        The name of the hyperbola.

    See Also
    --------
    [`Circle`][compas.geometry.Circle], [`Ellipse`][compas.geometry.Ellipse],
    and [`Parabola`][compas.geometry.Parabola]

    Examples
    --------
    >>> from compas.geometry import Frame, Hyperbola
    >>> hyperbola = Hyperbola(major=3, minor=2, branch=1)
    >>> hyperbola.point_at(0.0)
    Point(x=3.000, y=0.000, z=0.000)

    """

    @property
    def __data__(self) -> dict[str, Any]:
        return {
            "major": self.major,
            "minor": self.minor,
            "branch": self.branch,
            "frame": self.frame.__data__,
        }

    @classmethod
    def __from_data__(cls, data: dict[str, Any]) -> Self:
        return cls(
            major=data["major"],
            minor=data["minor"],
            branch=data["branch"],
            frame=Frame.__from_data__(data["frame"]),
        )

    def __init__(
        self,
        major: float,
        minor: float,
        branch: Literal[-1, 1] = 1,
        frame: Optional[Frame] = None,
        name: Optional[str] = None,
    ) -> None:
        super().__init__(frame=frame, name=name)
        self._major: Optional[float] = None
        self._minor: Optional[float] = None
        self._branch: Literal[-1, 1] = 1
        self.major = major
        self.minor = minor
        self.branch = branch

    def __repr__(self) -> str:
        return "{0}(major={1}, minor={2}, branch={3}, frame={4!r})".format(
            type(self).__name__,
            self.major,
            self.minor,
            self.branch,
            self.frame,
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Hyperbola):
            return False
        return self.major == other.major and self.minor == other.minor and self.branch == other.branch and self.frame == other.frame

    # ==========================================================================
    # Properties
    # ==========================================================================

    @property
    def center(self) -> Point:
        """The center of the hyperbola."""
        return self.frame.point

    @center.setter
    def center(self, point: CoordinateType) -> None:
        self.frame.point = point

    @property
    def major(self) -> float:
        """The positive semi-major axis length."""
        if self._major is None:
            raise ValueError("Length of major axis is not set.")
        return self._major

    @major.setter
    def major(self, major: float) -> None:
        if major <= 0:
            raise ValueError("Major axis length must be positive.")
        self._major = float(major)

    @property
    def minor(self) -> float:
        """The positive semi-minor axis length."""
        if self._minor is None:
            raise ValueError("Length of minor axis is not set.")
        return self._minor

    @minor.setter
    def minor(self, minor: float) -> None:
        if minor <= 0:
            raise ValueError("Minor axis length must be positive.")
        self._minor = float(minor)

    @property
    def branch(self) -> Literal[-1, 1]:
        """The branch sign: `1` for positive x and `-1` for negative x."""
        return self._branch

    @branch.setter
    def branch(self, branch: Literal[-1, 1]) -> None:
        if branch not in (-1, 1):
            raise ValueError("Branch must be either -1 or 1.")
        self._branch = branch

    @property
    def domain(self) -> tuple[float, float]:
        """The unbounded real parameter domain."""
        return -inf, inf

    @property
    def semifocal(self) -> float:
        """The distance from the center to either focus."""
        return sqrt(self.major**2 + self.minor**2)

    @property
    def focal(self) -> float:
        """The distance between the two foci."""
        return 2 * self.semifocal

    @property
    def eccentricity(self) -> float:
        """The eccentricity of the hyperbola."""
        return self.semifocal / self.major

    @property
    def focus1(self) -> Point:
        """The focus on the positive x-axis."""
        return self.frame.point + self.frame.xaxis * self.semifocal

    @property
    def focus2(self) -> Point:
        """The focus on the negative x-axis."""
        return self.frame.point + self.frame.xaxis * -self.semifocal

    @property
    def vertex1(self) -> Point:
        """The vertex on the positive x-axis."""
        return self.frame.point + self.frame.xaxis * self.major

    @property
    def vertex2(self) -> Point:
        """The vertex on the negative x-axis."""
        return self.frame.point + self.frame.xaxis * -self.major

    @property
    def asymptote1(self) -> Line:
        """The asymptote with positive local y direction."""
        return Line.from_point_and_vector(self.center, self.frame.xaxis * self.major + self.frame.yaxis * self.minor)

    @property
    def asymptote2(self) -> Line:
        """The asymptote with negative local y direction."""
        return Line.from_point_and_vector(self.center, self.frame.xaxis * self.major - self.frame.yaxis * self.minor)

    @property
    def is_closed(self) -> bool:
        """Whether the branch is closed."""
        return False

    @property
    def is_periodic(self) -> bool:
        """Whether the branch is periodic."""
        return False

    # ==========================================================================
    # Constructors
    # ==========================================================================

    # ==========================================================================
    # Methods
    # ==========================================================================

    def point_at(self, t: float, world: bool = True) -> Point:
        """Compute the point at a parameter.

        Parameters
        ----------
        t
            The real-valued hyperbolic parameter.
        world
            If `True`, return the point in world coordinates.

        Returns
        -------
        Point
            The point at the parameter.

        See Also
        --------
        [`Hyperbola.tangent_at`][compas.geometry.Hyperbola.tangent_at] and
        [`Hyperbola.normal_at`][compas.geometry.Hyperbola.normal_at]

        Examples
        --------
        >>> Hyperbola(2, 1).point_at(0.0)
        Point(x=2.000, y=0.000, z=0.000)

        """
        x = self.branch * self.major * cosh(t)
        y = self.minor * sinh(t)
        point = Point(x, y, 0)
        if world:
            point.transform(self.transformation)
        return point

    def tangent_at(self, t: float, world: bool = True) -> Vector:
        """Compute the unit tangent at a parameter.

        Parameters
        ----------
        t
            The real-valued hyperbolic parameter.
        world
            If `True`, return the vector in world coordinates.

        Returns
        -------
        Vector
            The unit tangent at the parameter.

        See Also
        --------
        [`Hyperbola.point_at`][compas.geometry.Hyperbola.point_at] and
        [`Hyperbola.normal_at`][compas.geometry.Hyperbola.normal_at]

        Examples
        --------
        >>> Hyperbola(2, 1).tangent_at(0.0)
        Vector(x=0.000, y=1.000, z=0.000)

        """
        tangent = Vector(self.branch * self.major * sinh(t), self.minor * cosh(t), 0.0)
        tangent.unitize()
        if world:
            tangent.transform(self.transformation)
        return tangent

    def normal_at(self, t: float, world: bool = True) -> Vector:
        """Compute the inward unit normal at a parameter.

        Parameters
        ----------
        t
            The real-valued hyperbolic parameter.
        world
            If `True`, return the vector in world coordinates.

        Returns
        -------
        Vector
            The inward unit normal at the parameter.

        See Also
        --------
        [`Hyperbola.point_at`][compas.geometry.Hyperbola.point_at] and
        [`Hyperbola.tangent_at`][compas.geometry.Hyperbola.tangent_at]

        Examples
        --------
        >>> Hyperbola(2, 1).normal_at(0.0)
        Vector(x=-1.000, y=0.000, z=0.000)

        """
        normal = Vector(-self.branch * self.minor * cosh(t), self.major * sinh(t), 0.0)
        normal.unitize()
        if world:
            normal.transform(self.transformation)
        return normal
