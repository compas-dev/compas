from math import sqrt
from typing import TYPE_CHECKING
from typing import Any
from typing import Optional
from typing import Sequence
from typing import TypeVar

from typing_extensions import Self

from compas._typing import CoordinateType
from compas._typing import FilePath
from compas.plugins import PluginNotInstalledError
from compas.plugins import pluggable

from .curve import Curve

if TYPE_CHECKING:
    from compas.geometry import Arc
    from compas.geometry import Circle
    from compas.geometry import Ellipse
    from compas.geometry import Line
    from compas.geometry import Point

NurbsCurveType = TypeVar("NurbsCurveType", bound="NurbsCurve")


@pluggable(category="factories")
def nurbscurve_from_interpolation(cls: type[NurbsCurveType], points: Sequence[CoordinateType], precision: float = 1e-3) -> NurbsCurveType:
    raise PluginNotInstalledError


@pluggable(category="factories")
def nurbscurve_from_native(cls: type[NurbsCurveType], curve: object) -> NurbsCurveType:
    raise PluginNotInstalledError


@pluggable(category="factories")
def nurbscurve_from_parameters(
    cls: type[NurbsCurveType],
    points: Sequence[CoordinateType],
    weights: Sequence[float],
    knots: Sequence[float],
    multiplicities: Sequence[int],
    degree: int,
    is_periodic: bool = False,
) -> NurbsCurveType:
    raise PluginNotInstalledError


@pluggable(category="factories")
def nurbscurve_from_points(cls: type[NurbsCurveType], points: Sequence[CoordinateType], degree: int = 3, is_periodic: bool = False) -> NurbsCurveType:
    raise PluginNotInstalledError


@pluggable(category="factories")
def nurbscurve_from_step(cls: type[NurbsCurveType], filepath: FilePath) -> NurbsCurveType:
    raise PluginNotInstalledError


class NurbsCurve(Curve):
    """A NURBS curve is defined by control points, weights, knots, and a degree.

    Parameters
    ----------
    name
        The name of the curve.

    Notes
    -----
    `NurbsCurve` defines the backend contract. Concrete implementations are
    supplied through the plugin mechanism, for example by Rhino or OCC.

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
    def __from_data__(cls, data: dict[str, Any]) -> Self:
        return cls.from_parameters(
            data["points"],  # conversion is not needed because point data can be provided in raw form as well
            data["weights"],
            data["knots"],
            data["multiplicities"],
            data["degree"],
            data["is_periodic"],
        )

    def __new__(cls, *args: object, **kwargs: object) -> Self:
        if cls is NurbsCurve:
            raise TypeError("Making an instance of `NurbsCurve` using `NurbsCurve()` is not allowed. Please use one of the factory methods instead (`NurbsCurve.from_...`)")
        return object.__new__(cls)

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
    def points(self) -> list["Point"]:
        """The control points."""
        raise NotImplementedError

    @property
    def weights(self) -> list[float]:
        """The control-point weights."""
        raise NotImplementedError

    @property
    def knots(self) -> list[float]:
        """The unique knots, without multiplicity."""
        raise NotImplementedError

    @property
    def multiplicities(self) -> list[int]:
        """The multiplicity of each unique knot."""
        raise NotImplementedError

    @property
    def knotvector(self) -> list[float]:
        """The complete knot vector, including repeated knots."""
        return [knot for knot, multiplicity in zip(self.knots, self.multiplicities) for _ in range(multiplicity)]

    @property
    def continuity(self) -> int:
        """The continuity degree reported by the backend."""
        raise NotImplementedError

    @property
    def degree(self) -> int:
        """The polynomial degree."""
        raise NotImplementedError

    @property
    def order(self) -> int:
        """The polynomial order, equal to `degree + 1`."""
        return self.degree + 1

    @property
    def is_rational(self) -> bool:
        """Whether any control-point weight differs from one."""
        raise NotImplementedError

    # ==============================================================================
    # Constructors
    # ==============================================================================

    @classmethod
    def from_arc(cls, arc: "Arc") -> Self:
        """Construct a NURBS curve from an arc.

        Parameters
        ----------
        arc
            The arc to convert.

        Returns
        -------
        Self
            The constructed NURBS curve.

        Examples
        --------
        >>> from compas.geometry import Arc
        >>> curve = NurbsCurve.from_arc(Arc(1.0, 0.0, 1.0))  # doctest: +SKIP

        """
        raise NotImplementedError

    @classmethod
    def from_circle(cls, circle: "Circle") -> Self:
        """Construct a NURBS curve from a circle.

        Parameters
        ----------
        circle
            The circle to convert.

        Returns
        -------
        Self
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
        return cls.from_parameters(points=points, weights=weights, knots=knots, multiplicities=mults, degree=2)

    @classmethod
    def from_ellipse(cls, ellipse: "Ellipse") -> Self:
        """Construct a NURBS curve from an ellipse.

        Parameters
        ----------
        ellipse
            The ellipse to convert.

        Returns
        -------
        Self
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
        return cls.from_parameters(points=points, weights=weights, knots=knots, multiplicities=mults, degree=2)

    @classmethod
    def from_interpolation(cls, points: Sequence[CoordinateType], precision: float = 1e-3) -> Self:
        """Construct a NURBS curve by interpolating a set of points.

        Parameters
        ----------
        points
            A list of interpolation points.
        precision
            The desired precision of the interpolation.

        Returns
        -------
        Self
            The interpolated NURBS curve.

        Examples
        --------
        >>> points = [[0, 0, 0], [1, 1, 0], [2, 0, 0]]
        >>> curve = NurbsCurve.from_interpolation(points)  # doctest: +SKIP

        """
        return nurbscurve_from_interpolation(cls, points, precision=precision)

    @classmethod
    def from_line(cls, line: "Line") -> Self:
        """Construct a NURBS curve from a line.

        Parameters
        ----------
        line
            The line to convert.

        Returns
        -------
        Self
            The constructed NURBS curve.

        Examples
        --------
        >>> from compas.geometry import Line
        >>> curve = NurbsCurve.from_line(Line([0, 0, 0], [1, 0, 0]))  # doctest: +SKIP

        """
        return cls.from_parameters(
            points=[line.start, line.end],
            weights=[1.0, 1.0],
            knots=[0.0, 1.0],
            multiplicities=[2, 2],
            degree=1,
        )

    @classmethod
    def from_native(cls, curve: object) -> Self:
        """Construct a NURBS curve from a CAD-native curve geometry.

        Parameters
        ----------
        curve
            A CAD-native curve geometry.

        Returns
        -------
        Self
            A COMPAS NURBS curve.

        Examples
        --------
        >>> curve = NurbsCurve.from_native(native_curve)  # doctest: +SKIP

        """
        return nurbscurve_from_native(cls, curve)

    @classmethod
    def from_parameters(
        cls,
        points: Sequence[CoordinateType],
        weights: Sequence[float],
        knots: Sequence[float],
        multiplicities: Sequence[int],
        degree: int,
        is_periodic: bool = False,
    ) -> Self:
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
        Self
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
        return nurbscurve_from_parameters(cls, points, weights, knots, multiplicities, degree, is_periodic=is_periodic)

    @classmethod
    def from_points(cls, points: Sequence[CoordinateType], degree: int = 3, is_periodic: bool = False) -> Self:
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
        Self
            The constructed NURBS curve.

        Examples
        --------
        >>> curve = NurbsCurve.from_points([[0, 0, 0], [1, 0, 0]], degree=1)  # doctest: +SKIP

        """
        return nurbscurve_from_points(cls, points, degree=degree, is_periodic=is_periodic)

    @classmethod
    def from_step(cls, filepath: FilePath) -> Self:
        """Load a NURBS curve from an STP file.

        Parameters
        ----------
        filepath
            The path to the file.

        Returns
        -------
        Self
            The loaded NURBS curve.

        Examples
        --------
        >>> curve = NurbsCurve.from_step("curve.step")  # doctest: +SKIP

        """
        return nurbscurve_from_step(cls, filepath)

    # ==============================================================================
    # Conversions
    # ==============================================================================

    # ==============================================================================
    # Methods
    # ==============================================================================

    def copy(self, cls: Optional[type[Self]] = None, copy_guid: bool = False) -> Self:  # type: ignore[override]
        """Make an independent copy of the current curve.

        Parameters
        ----------
        cls
            The NURBS curve type to construct. Default is `type(self)`.
        copy_guid
            If `True`, preserve the globally unique identifier.

        Returns
        -------
        Self
            The independent copy.

        """
        curve_type = cls or type(self)
        curve = curve_type.from_parameters(
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
