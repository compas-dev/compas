from math import inf
from typing import Any
from typing import Optional

from typing_extensions import Self

from compas.geometry import Frame
from compas.geometry import Point
from compas.geometry import Vector

from ..line import Line
from .conic import Conic


class Parabola(Conic):
    r"""A parabola defined by a frame and focal length.

    In local coordinates the parabola is parameterized by

    $$
    x(t) = t, \qquad y(t) = \frac{t^2}{4f},
    $$

    where $f$ is the focal length. The vertex is the frame origin and the
    positive local y-axis is the axis of symmetry. The parameter domain is the
    entire real line.

    Parameters
    ----------
    focal
        The positive focal length.
    frame
        The coordinate frame. Default is the world XY frame.
    name
        The name of the parabola.

    See Also
    --------
    [`Ellipse`][compas.geometry.Ellipse], [`Hyperbola`][compas.geometry.Hyperbola],
    and [`Circle`][compas.geometry.Circle]

    Examples
    --------
    >>> from compas.geometry import Parabola
    >>> parabola = Parabola(focal=1.0)
    >>> parabola.point_at(2.0)
    Point(x=2.000, y=1.000, z=0.000)

    """

    @property
    def __data__(self) -> dict[str, Any]:
        return {"focal": self.focal, "frame": self.frame.__data__}

    @classmethod
    def __from_data__(cls, data: dict[str, Any]) -> Self:
        return cls(focal=data["focal"], frame=Frame.__from_data__(data["frame"]))

    def __init__(self, focal: float, frame: Optional[Frame] = None, name: Optional[str] = None) -> None:
        super().__init__(frame=frame, name=name)
        self._focal: Optional[float] = None
        self.focal = focal

    def __repr__(self) -> str:
        return "{0}(focal={1}, frame={2!r})".format(type(self).__name__, self.focal, self.frame)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Parabola):
            return False
        return self.focal == other.focal and self.frame == other.frame

    # ==========================================================================
    # Properties
    # ==========================================================================

    @property
    def focal(self) -> float:
        """The positive focal length.

        Notes
        -----
        Changing the focal length changes the curvature while preserving the
        vertex and axis of symmetry.

        """
        if self._focal is None:
            raise ValueError("The focal length of the parabola is not set.")
        return self._focal

    @focal.setter
    def focal(self, focal: float) -> None:
        if focal <= 0.0:
            raise ValueError("The focal length must be positive.")
        self._focal = float(focal)

    @property
    def a(self) -> float:
        """The quadratic coefficient $a = 1 / (4f)$.

        Notes
        -----
        Assigning a positive coefficient updates the focal length.

        """
        return 1.0 / (4.0 * self.focal)

    @a.setter
    def a(self, a: float) -> None:
        if a <= 0.0:
            raise ValueError("The quadratic coefficient must be positive.")
        self.focal = 1.0 / (4.0 * a)

    @property
    def domain(self) -> tuple[float, float]:
        """The unbounded real parameter domain."""
        return -inf, inf

    @property
    def eccentricity(self) -> float:
        """The eccentricity, which is always one."""
        return 1.0

    @property
    def latus(self) -> float:
        """The length of the latus rectum."""
        return 4.0 * self.focal

    @property
    def focus(self) -> Point:
        """The focus of the parabola."""
        return self.frame.point + self.frame.yaxis * self.focal

    @property
    def vertex(self) -> Point:
        """The vertex of the parabola.

        Notes
        -----
        The returned point belongs to the parabola frame. Mutating it changes
        the parabola.

        """
        return self.frame.point

    @property
    def directix(self) -> Line:
        """The directrix of the parabola as an independent line."""
        point = self.frame.point - self.frame.yaxis * self.focal
        return Line.from_point_and_vector(point, self.frame.xaxis)

    @property
    def is_closed(self) -> bool:
        """Whether the parabola is closed."""
        return False

    @property
    def is_periodic(self) -> bool:
        """Whether the parabola is periodic."""
        return False

    # ==========================================================================
    # Methods
    # ==========================================================================

    def point_at(self, t: float, world: bool = True) -> Point:
        """Compute the point at a parameter.

        Parameters
        ----------
        t
            The real-valued parameter.
        world
            If `True`, return the point in world coordinates.

        Returns
        -------
        Point
            The point at the parameter.

        Examples
        --------
        >>> Parabola(1.0).point_at(-2.0)
        Point(x=-2.000, y=1.000, z=0.000)

        """
        point = Point(t, self.a * t**2, 0.0)
        if world:
            point.transform(self.transformation)
        return point

    def tangent_at(self, t: float, world: bool = True) -> Vector:
        """Compute the unit tangent at a parameter.

        Parameters
        ----------
        t
            The real-valued parameter.
        world
            If `True`, return the vector in world coordinates.

        Returns
        -------
        Vector
            The unit tangent in increasing parameter direction.

        Examples
        --------
        >>> Parabola(1.0).tangent_at(0.0)
        Vector(x=1.000, y=0.000, z=0.000)

        """
        tangent = Vector(1.0, 2.0 * self.a * t, 0.0)
        tangent.unitize()
        if world:
            tangent.transform(self.transformation)
        return tangent

    def normal_at(self, t: float, world: bool = True) -> Vector:
        """Compute the inward unit normal at a parameter.

        Parameters
        ----------
        t
            The real-valued parameter.
        world
            If `True`, return the vector in world coordinates.

        Returns
        -------
        Vector
            The unit normal directed towards the concave side.

        Examples
        --------
        >>> Parabola(1.0).normal_at(0.0)
        Vector(x=0.000, y=1.000, z=0.000)

        """
        normal = Vector(-2.0 * self.a * t, 1.0, 0.0)
        normal.unitize()
        if world:
            normal.transform(self.transformation)
        return normal
