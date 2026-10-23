from collections.abc import Sequence
from math import sqrt
from typing import TYPE_CHECKING
from typing import Any
from typing import Literal
from typing import overload

from compas._typing import CoordinateType
from compas._typing import FilePath

from .._typing import TransformationType
from .curve import Curve
from .nurbs_operations import curve_closest_point
from .nurbs_operations import curve_continuity
from .nurbs_operations import curve_curvature_at
from .nurbs_operations import curve_degree
from .nurbs_operations import curve_divide_by_count
from .nurbs_operations import curve_divide_by_length
from .nurbs_operations import curve_domain
from .nurbs_operations import curve_is_closed
from .nurbs_operations import curve_is_periodic
from .nurbs_operations import curve_is_rational
from .nurbs_operations import curve_knots
from .nurbs_operations import curve_length
from .nurbs_operations import curve_multiplicities
from .nurbs_operations import curve_normal_at
from .nurbs_operations import curve_point_at
from .nurbs_operations import curve_points
from .nurbs_operations import curve_reverse
from .nurbs_operations import curve_tangent_at
from .nurbs_operations import curve_to_obj
from .nurbs_operations import curve_to_step
from .nurbs_operations import curve_transform
from .nurbs_operations import curve_weights
from .nurbs_operations import from_arc
from .nurbs_operations import from_interpolation
from .nurbs_operations import from_native
from .nurbs_operations import from_parameters
from .nurbs_operations import from_points
from .nurbs_operations import from_step

if TYPE_CHECKING:
    from compas.geometry import Arc
    from compas.geometry import Circle
    from compas.geometry import Ellipse
    from compas.geometry import Line
    from compas.geometry import Point
    from compas.geometry import Vector


class NurbsCurve(Curve):
    """A NURBS curve is defined by control points, weights, knots, and a degree.

    Parameters
    ----------
    name
        The name of the curve.

    Notes
    -----
    `NurbsCurve` is the stable public wrapper. Backend plugins implement its
    construction, queries, evaluation, mutation, and I/O operations without
    replacing the public class.

    """

    @property
    def __dtype__(self) -> str:
        return "compas.geometry/NurbsCurve"

    @property
    def __data__(self) -> dict[str, Any]:
        return {
            "points": [point.__data__ for point in self.points],
            "weights": self.weights,
            "knots": self.knots,
            "multiplicities": self.multiplicities,
            "degree": self.degree,
            "is_periodic": self.is_periodic,
        }

    @classmethod
    def __from_data__(cls, data: dict[str, Any]) -> "NurbsCurve":
        return NurbsCurve.from_parameters(
            data["points"],  # conversion is not needed because point data can be provided in raw form as well
            data["weights"],
            data["knots"],
            data["multiplicities"],
            data["degree"],
            data["is_periodic"],
        )

    def __init__(self, native_curve: Any = None, name: str | None = None) -> None:
        super().__init__(name=name)
        self._native_curve = native_curve

    def __repr__(self) -> str:
        return "{0}(points={1!r}, weights={2}, knots={3}, multiplicities={4}, degree={5}, is_periodic={6})".format(
            type(self).__name__,
            self.points,
            self.weights,
            self.knots,
            self.multiplicities,
            self.degree,
            self.is_periodic,
        )

    # ==============================================================================
    # Properties
    # ==============================================================================

    @property
    def native_curve(self) -> Any:
        """The backend-specific NURBS curve object."""
        return self._native_curve

    @property
    def points(self) -> list["Point"]:
        """The control points."""
        return curve_points(self)

    @property
    def weights(self) -> list[float]:
        """The control-point weights."""
        return curve_weights(self)

    @property
    def knots(self) -> list[float]:
        """The unique knots, without multiplicity."""
        return curve_knots(self)

    @property
    def multiplicities(self) -> list[int]:
        """The multiplicity of each unique knot."""
        return curve_multiplicities(self)

    @property
    def knotvector(self) -> list[float]:
        """The complete knot vector, including repeated knots."""
        return [knot for knot, multiplicity in zip(self.knots, self.multiplicities) for _ in range(multiplicity)]

    @property
    def continuity(self) -> int:
        """The continuity degree reported by the backend."""
        return curve_continuity(self)

    @property
    def degree(self) -> int:
        """The polynomial degree."""
        return curve_degree(self)

    @property
    def order(self) -> int:
        """The polynomial order, equal to `degree + 1`."""
        return self.degree + 1

    @property
    def is_rational(self) -> bool:
        """Whether any control-point weight differs from one."""
        return curve_is_rational(self)

    @property
    def domain(self) -> tuple[float, float]:
        """The parameter domain of the curve."""
        return curve_domain(self)

    @property
    def length(self) -> float:
        """The length of the curve."""
        return curve_length(self)

    @property
    def is_closed(self) -> bool:
        """Whether the curve is closed."""
        return curve_is_closed(self)

    @property
    def is_periodic(self) -> bool:
        """Whether the curve is periodic."""
        return curve_is_periodic(self)

    # ==============================================================================
    # Constructors
    # ==============================================================================

    @classmethod
    def from_arc(cls, arc: "Arc") -> "NurbsCurve":
        """Construct a NURBS curve from an arc.

        Parameters
        ----------
        arc
            The arc to convert.

        Returns
        -------
        NurbsCurve
            The constructed NURBS curve.

        Examples
        --------
        >>> from compas.geometry import Arc
        >>> curve = NurbsCurve.from_arc(Arc(1.0, 0.0, 1.0))  # doctest: +SKIP

        """
        return from_arc(arc)

    @classmethod
    def from_circle(cls, circle: "Circle") -> "NurbsCurve":
        """Construct a NURBS curve from a circle.

        Parameters
        ----------
        circle
            The circle to convert.

        Returns
        -------
        NurbsCurve
            The constructed NURBS curve.

        Examples
        --------
        >>> from compas.geometry import Circle
        >>> curve = NurbsCurve.from_circle(Circle(1.0))  # doctest: +SKIP

        """
        frame = circle.frame
        w = 0.5 * sqrt(2)
        dx = frame.xaxis * circle.radius
        dy = frame.yaxis * circle.radius
        points = [
            frame.point - dy,
            frame.point - dy - dx,
            frame.point - dx,
            frame.point + dy - dx,
            frame.point + dy,
            frame.point + dy + dx,
            frame.point + dx,
            frame.point - dy + dx,
            frame.point - dy,
        ]
        knots = [0, 1 / 4, 1 / 2, 3 / 4, 1]
        mults = [3, 2, 2, 2, 3]
        weights = [1, w, 1, w, 1, w, 1, w, 1]
        return NurbsCurve.from_parameters(points=points, weights=weights, knots=knots, multiplicities=mults, degree=2)

    @classmethod
    def from_ellipse(cls, ellipse: "Ellipse") -> "NurbsCurve":
        """Construct a NURBS curve from an ellipse.

        Parameters
        ----------
        ellipse
            The ellipse to convert.

        Returns
        -------
        NurbsCurve
            The constructed NURBS curve.

        Examples
        --------
        >>> from compas.geometry import Ellipse
        >>> curve = NurbsCurve.from_ellipse(Ellipse(2.0, 1.0))  # doctest: +SKIP

        """
        frame = ellipse.frame
        w = 0.5 * sqrt(2)
        dx = frame.xaxis * ellipse.major
        dy = frame.yaxis * ellipse.minor
        points = [
            frame.point - dy,
            frame.point - dy - dx,
            frame.point - dx,
            frame.point + dy - dx,
            frame.point + dy,
            frame.point + dy + dx,
            frame.point + dx,
            frame.point - dy + dx,
            frame.point - dy,
        ]
        knots = [0, 1 / 4, 1 / 2, 3 / 4, 1]
        mults = [3, 2, 2, 2, 3]
        weights = [1, w, 1, w, 1, w, 1, w, 1]
        return NurbsCurve.from_parameters(points=points, weights=weights, knots=knots, multiplicities=mults, degree=2)

    @classmethod
    def from_interpolation(cls, points: Sequence[CoordinateType], precision: float = 1e-3) -> "NurbsCurve":
        """Construct a NURBS curve by interpolating a set of points.

        Parameters
        ----------
        points
            A list of interpolation points.
        precision
            The desired precision of the interpolation.

        Returns
        -------
        NurbsCurve
            The interpolated NURBS curve.

        Examples
        --------
        >>> points = [[0, 0, 0], [1, 1, 0], [2, 0, 0]]
        >>> curve = NurbsCurve.from_interpolation(points)  # doctest: +SKIP

        """
        return from_interpolation(points, precision=precision)

    @classmethod
    def from_line(cls, line: "Line") -> "NurbsCurve":
        """Construct a NURBS curve from a line.

        Parameters
        ----------
        line
            The line to convert.

        Returns
        -------
        NurbsCurve
            The constructed NURBS curve.

        Examples
        --------
        >>> from compas.geometry import Line
        >>> curve = NurbsCurve.from_line(Line([0, 0, 0], [1, 0, 0]))  # doctest: +SKIP

        """
        return NurbsCurve.from_parameters(
            points=[line.start, line.end],
            weights=[1.0, 1.0],
            knots=[0.0, 1.0],
            multiplicities=[2, 2],
            degree=1,
        )

    @classmethod
    def from_native(cls, curve: object) -> "NurbsCurve":
        """Construct a NURBS curve from a CAD-native curve geometry.

        Parameters
        ----------
        curve
            A CAD-native curve geometry.

        Returns
        -------
        NurbsCurve
            A COMPAS NURBS curve.

        Examples
        --------
        >>> curve = NurbsCurve.from_native(native_curve)  # doctest: +SKIP

        """
        return from_native(curve)

    @classmethod
    def from_parameters(
        cls,
        points: Sequence[CoordinateType],
        weights: Sequence[float],
        knots: Sequence[float],
        multiplicities: Sequence[int],
        degree: int,
        is_periodic: bool = False,
    ) -> "NurbsCurve":
        """Construct a NURBS curve from explicit curve parameters.

        Parameters
        ----------
        points
            The control points.
        weights
            The weights of the control points.
        knots
            The curve knots, without multiplicity.
        multiplicities
            Multiplicity of the knots.
        degree
            Degree of the curve.
        is_periodic
            Flag indicating that the curve is periodic.

        Returns
        -------
        NurbsCurve
            The constructed NURBS curve.

        Examples
        --------
        >>> curve = NurbsCurve.from_parameters(  # doctest: +SKIP
        ...     points=[[0, 0, 0], [1, 0, 0]],
        ...     weights=[1.0, 1.0],
        ...     knots=[0.0, 1.0],
        ...     multiplicities=[2, 2],
        ...     degree=1,
        ... )

        """
        return from_parameters(points, weights, knots, multiplicities, degree, is_periodic=is_periodic)

    @classmethod
    def from_points(cls, points: Sequence[CoordinateType], degree: int = 3, is_periodic: bool = False) -> "NurbsCurve":
        """Construct a NURBS curve from control points.

        Parameters
        ----------
        points
            The control points.
        degree
            The degree of the curve.
        is_periodic
            Whether the curve is periodic.

        Returns
        -------
        NurbsCurve
            The constructed NURBS curve.

        Examples
        --------
        >>> curve = NurbsCurve.from_points([[0, 0, 0], [1, 0, 0]], degree=1)  # doctest: +SKIP

        """
        return from_points(points, degree=degree, is_periodic=is_periodic)

    @classmethod
    def from_step(cls, filepath: FilePath) -> "NurbsCurve":
        """Load a NURBS curve from an STP file.

        Parameters
        ----------
        filepath
            The path to the file.

        Returns
        -------
        NurbsCurve
            The loaded NURBS curve.

        Examples
        --------
        >>> curve = NurbsCurve.from_step("curve.step")  # doctest: +SKIP

        """
        return from_step(filepath)

    # ==============================================================================
    # Conversions
    # ==============================================================================

    def to_step(self, filepath: FilePath, schema: str = "AP203") -> None:
        """Write the curve to a STEP file.

        Parameters
        ----------
        filepath
            The output path.
        schema
            The STEP schema.

        """
        curve_to_step(self, filepath, schema=schema)

    def to_obj(self, filepath: FilePath) -> None:
        """Write the curve to an OBJ file.

        Parameters
        ----------
        filepath
            The output path.

        """
        curve_to_obj(self, filepath)

    # ==============================================================================
    # Methods
    # ==============================================================================

    def transform(self, transformation: TransformationType) -> None:
        """Transform the curve geometry.

        Parameters
        ----------
        transformation
            The transformation.

        """
        curve_transform(self, transformation)

    def point_at(self, t: float, world: bool = True) -> "Point":
        """Compute the point at a curve parameter."""
        return curve_point_at(self, t, world=world)

    def normal_at(self, t: float, world: bool = True) -> "Vector | None":
        """Compute the normal at a curve parameter."""
        return curve_normal_at(self, t, world=world)

    def tangent_at(self, t: float, world: bool = True) -> "Vector":
        """Compute the tangent at a curve parameter."""
        return curve_tangent_at(self, t, world=world)

    def curvature_at(self, t: float) -> "Vector":
        """Compute the curvature vector at a curve parameter."""
        return curve_curvature_at(self, t)

    def reverse(self) -> None:
        """Reverse the curve parametrization."""
        curve_reverse(self)

    @overload
    def closest_point(self, point: CoordinateType, return_parameter: Literal[False] = False) -> "Point": ...

    @overload
    def closest_point(self, point: CoordinateType, return_parameter: Literal[True]) -> tuple["Point", float]: ...

    def closest_point(self, point: CoordinateType, return_parameter: bool = False) -> "Point | tuple[Point, float]":
        """Compute the closest point on the curve."""
        return curve_closest_point(self, point, return_parameter=return_parameter)

    @overload
    def divide_by_count(self, count: int, return_points: Literal[False] = False) -> list[float]: ...

    @overload
    def divide_by_count(self, count: int, return_points: Literal[True]) -> tuple[list[float], list["Point"]]: ...

    def divide_by_count(self, count: int, return_points: bool = False) -> "list[float] | tuple[list[float], list[Point]]":
        """Divide the curve into a number of equal-length segments."""
        return curve_divide_by_count(self, count, return_points=return_points)

    @overload
    def divide_by_length(self, length: float, return_points: Literal[False] = False) -> list[float]: ...

    @overload
    def divide_by_length(self, length: float, return_points: Literal[True]) -> tuple[list[float], list["Point"]]: ...

    def divide_by_length(self, length: float, return_points: bool = False) -> "list[float] | tuple[list[float], list[Point]]":
        """Divide the curve into segments of a target length."""
        return curve_divide_by_length(self, length, return_points=return_points)

    def copy(self, copy_guid: bool = False) -> "NurbsCurve":  # type: ignore[override]
        """Make an independent copy of the current curve.

        Parameters
        ----------
        copy_guid
            If `True`, preserve the globally unique identifier.

        Returns
        -------
        NurbsCurve
            The independent copy.

        """
        curve = NurbsCurve.from_parameters(
            self.points,
            self.weights,
            self.knots,
            self.multiplicities,
            self.degree,
            self.is_periodic,
        )
        if copy_guid:
            curve._guid = self.guid
        return curve
