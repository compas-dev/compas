from collections.abc import Sequence
from typing import TYPE_CHECKING
from typing import Any
from typing import Literal
from typing import Self

from compas._typing import CoordinatesType
from compas.data import Data

if TYPE_CHECKING:
    from compas.geometry import Bezier
    from compas.geometry import BrepVertex
    from compas.geometry import Circle
    from compas.geometry import Curve
    from compas.geometry import Ellipse
    from compas.geometry import Hyperbola
    from compas.geometry import Line
    from compas.geometry import NurbsCurve
    from compas.geometry import Parabola


class CurveType:
    """Geometric type of a Brep edge curve."""

    LINE = 0
    CIRCLE = 1
    ELLIPSE = 2
    HYPERBOLA = 3
    PARABOLA = 4
    BEZIER = 5
    BSPLINE = 6
    OTHER = 7
    CURVE2D = 8


class BrepEdge(Data):
    """Interface for a topological edge of a boundary representation."""

    # ==========================================================================
    # Properties
    # ==========================================================================

    @property
    def is_line(self) -> bool:
        """Whether the edge geometry is linear."""
        raise NotImplementedError

    @property
    def is_circle(self) -> bool:
        """Whether the edge geometry is circular."""
        raise NotImplementedError

    @property
    def is_ellipse(self) -> bool:
        """Whether the edge geometry is elliptical."""
        raise NotImplementedError

    @property
    def is_hyperbola(self) -> bool:
        """Whether the edge geometry is hyperbolic."""
        raise NotImplementedError

    @property
    def is_parabola(self) -> bool:
        """Whether the edge geometry is parabolic."""
        raise NotImplementedError

    @property
    def is_bezier(self) -> bool:
        """Whether the edge geometry is a Bézier curve."""
        raise NotImplementedError

    @property
    def is_bspline(self) -> bool:
        """Whether the edge geometry is a B-spline curve."""
        raise NotImplementedError

    @property
    def is_other(self) -> bool:
        """Whether the edge has another curve type."""
        raise NotImplementedError

    @property
    def is_valid(self) -> bool:
        """Whether the edge is valid according to the backend."""
        raise NotImplementedError

    @property
    def vertices(self) -> list["BrepVertex"]:
        """The vertices bounding the edge."""
        raise NotImplementedError

    @property
    def first_vertex(self) -> "BrepVertex":
        """The first vertex in the edge orientation."""
        raise NotImplementedError

    @property
    def last_vertex(self) -> "BrepVertex":
        """The last vertex in the edge orientation."""
        raise NotImplementedError

    @property
    def length(self) -> float:
        """The length of the edge geometry."""
        raise NotImplementedError

    @property
    def curve(self) -> "Curve | Line":
        """The curve geometry of the edge."""
        raise NotImplementedError

    @property
    def orientation(self) -> Literal[0, 1, 2, 3]:
        """The orientation as a `BrepOrientation` value."""
        raise NotImplementedError

    @property
    def type(self) -> Literal[0, 1, 2, 3, 4, 5, 6, 7, 8]:
        """The curve type as a `CurveType` value."""
        raise NotImplementedError

    @property
    def native_edge(self) -> Any:
        """The backend-specific edge object."""
        raise NotImplementedError

    # ==========================================================================
    # Constructors
    # ==========================================================================

    @classmethod
    def from_vertices(cls, vertices: Sequence["BrepVertex"]) -> Self:
        """Construct an edge from two vertices.

        Parameters
        ----------
        vertices
            The two endpoint vertices.

        Returns
        -------
        Self
            The constructed edge.

        """
        raise NotImplementedError

    @classmethod
    def from_points(cls, points: CoordinatesType) -> Self:
        """Construct an edge from two points.

        Parameters
        ----------
        points
            The two endpoint coordinates.

        Returns
        -------
        Self
            The constructed edge.

        """
        raise NotImplementedError

    @classmethod
    def from_line(cls, line: "Line") -> Self:
        """Construct an edge from a line segment.

        Parameters
        ----------
        line
            The line segment.

        Returns
        -------
        Self
            The constructed edge.

        """
        raise NotImplementedError

    @classmethod
    def from_circle(cls, circle: "Circle") -> Self:
        """Construct an edge from a circle.

        Parameters
        ----------
        circle
            The circle.

        Returns
        -------
        Self
            The constructed edge.

        """
        raise NotImplementedError

    @classmethod
    def from_ellipse(cls, ellipse: "Ellipse") -> Self:
        """Construct an edge from an ellipse.

        Parameters
        ----------
        ellipse
            The ellipse.

        Returns
        -------
        Self
            The constructed edge.

        """
        raise NotImplementedError

    @classmethod
    def from_curve(cls, curve: "Curve") -> Self:
        """Construct an edge from a parametric curve.

        Parameters
        ----------
        curve
            The curve.

        Returns
        -------
        Self
            The constructed edge.

        """
        raise NotImplementedError

    # ==========================================================================
    # Conversions
    # ==========================================================================

    def to_line(self) -> "Line":
        """Return the edge geometry as a line segment."""
        raise NotImplementedError

    def to_circle(self) -> "Circle":
        """Return the edge geometry as a circle."""
        raise NotImplementedError

    def to_ellipse(self) -> "Ellipse":
        """Return the edge geometry as an ellipse."""
        raise NotImplementedError

    def to_hyperbola(self) -> "Hyperbola":
        """Return the edge geometry as a hyperbola."""
        raise NotImplementedError

    def to_parabola(self) -> "Parabola":
        """Return the edge geometry as a parabola."""
        raise NotImplementedError

    def to_bezier(self) -> "Bezier":
        """Return the edge geometry as a Bézier curve."""
        raise NotImplementedError

    def to_bspline(self) -> "NurbsCurve":
        """Return the edge geometry as a NURBS curve."""
        raise NotImplementedError

    def to_curve(self) -> "Curve | Line":
        """Return the edge curve in its most specific supported form."""
        raise NotImplementedError
