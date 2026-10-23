from collections.abc import Sequence
from typing import TYPE_CHECKING
from typing import Any
from typing import Literal
from typing import overload

from compas._typing import CoordinateType
from compas._typing import FilePath
from compas.geometry import Point
from compas.itertools import linspace
from compas.itertools import meshgrid

from .._typing import TransformationType
from .nurbs_operations import from_cylinder
from .nurbs_operations import from_extrusion
from .nurbs_operations import from_fill
from .nurbs_operations import from_frame
from .nurbs_operations import from_interpolation
from .nurbs_operations import from_native
from .nurbs_operations import from_parameters
from .nurbs_operations import from_plane
from .nurbs_operations import from_points
from .nurbs_operations import from_sphere
from .nurbs_operations import from_step
from .nurbs_operations import from_torus
from .nurbs_operations import surface_boundary
from .nurbs_operations import surface_closest_point
from .nurbs_operations import surface_degree_u
from .nurbs_operations import surface_degree_v
from .nurbs_operations import surface_domain_u
from .nurbs_operations import surface_domain_v
from .nurbs_operations import surface_frame_at
from .nurbs_operations import surface_is_periodic_u
from .nurbs_operations import surface_is_periodic_v
from .nurbs_operations import surface_isocurve_u
from .nurbs_operations import surface_isocurve_v
from .nurbs_operations import surface_knots_u
from .nurbs_operations import surface_knots_v
from .nurbs_operations import surface_mults_u
from .nurbs_operations import surface_mults_v
from .nurbs_operations import surface_normal_at
from .nurbs_operations import surface_point_at
from .nurbs_operations import surface_points
from .nurbs_operations import surface_to_brep
from .nurbs_operations import surface_to_step
from .nurbs_operations import surface_transform
from .nurbs_operations import surface_weights
from .surface import Surface

if TYPE_CHECKING:
    from compas.geometry import Brep
    from compas.geometry import Curve
    from compas.geometry import Cylinder
    from compas.geometry import Frame
    from compas.geometry import Line
    from compas.geometry import NurbsCurve
    from compas.geometry import Plane
    from compas.geometry import Sphere
    from compas.geometry import Torus
    from compas.geometry import Vector

ControlPointGrid = Sequence[Sequence[CoordinateType]]
WeightGrid = Sequence[Sequence[float]]


class NurbsSurface(Surface):
    """A NURBS surface defined by control points, weights, knots, and degrees.

    Parameters
    ----------
    name
        The name of the surface.

    Notes
    -----
    `NurbsSurface` is the stable public wrapper. Backend plugins implement its
    construction, queries, evaluation, mutation, and I/O operations without
    replacing the public class.

    Knot data exposed by this contract uses the full mathematical convention.
    The complete knot vectors include all endpoint knots, including the two
    knots that openNURBS considers superfluous and omits from native Rhino knot
    lists. Rhino implementations are responsible for removing those knots when
    constructing native geometry and restoring them when exposing COMPAS knot
    data.

    Control points and weights use row-major parameter order. The outer
    sequence contains V rows and every row contains values along U; therefore a
    nested value is addressed as `control_points[v][u]` or `weights[v][u]`.

    """

    @property
    def __dtype__(self) -> str:
        return "compas.geometry/NurbsSurface"

    @property
    def __data__(self) -> dict[str, Any]:
        """The data representation of the NURBS surface."""
        return {
            "control_points": [[point.__data__ for point in row] for row in self.control_points],
            "weights": [list(row) for row in self.weights],
            "knots_u": list(self.knots_u),
            "knots_v": list(self.knots_v),
            "mults_u": list(self.mults_u),
            "mults_v": list(self.mults_v),
            "degree_u": self.degree_u,
            "degree_v": self.degree_v,
            "is_periodic_u": self.is_periodic_u,
            "is_periodic_v": self.is_periodic_v,
        }

    @classmethod
    def __from_data__(cls, data: dict[str, Any]) -> "NurbsSurface":
        return NurbsSurface.from_parameters(
            data["control_points"],
            data["weights"],
            data["knots_u"],
            data["knots_v"],
            data["mults_u"],
            data["mults_v"],
            data["degree_u"],
            data["degree_v"],
            data["is_periodic_u"],
            data["is_periodic_v"],
        )

    def __init__(self, native_surface: Any = None, name: str | None = None) -> None:
        super().__init__(name=name)
        self._native_surface = native_surface

    def __repr__(self) -> str:
        return (
            "{0}(control_points={1!r}, weights={2}, knots_u={3}, knots_v={4}, mults_u={5}, mults_v={6}, degree_u={7}, degree_v={8}, is_periodic_u={9}, is_periodic_v={10})"
        ).format(
            type(self).__name__,
            self.control_points,
            self.weights,
            self.knots_u,
            self.knots_v,
            self.mults_u,
            self.mults_v,
            self.degree_u,
            self.degree_v,
            self.is_periodic_u,
            self.is_periodic_v,
        )

    # ==============================================================================
    # Properties
    # ==============================================================================

    @property
    def native_surface(self) -> Any:
        """The backend-specific NURBS surface object."""
        return self._native_surface

    @property
    def control_points(self) -> Sequence[Sequence[Point]]:
        """The control points in V rows, with each row running along U."""
        return surface_points(self)

    @property
    def weights(self) -> Sequence[Sequence[float]]:
        """The control-point weights in the same V-by-U layout as `control_points`."""
        return surface_weights(self)

    @property
    def knots_u(self) -> Sequence[float]:
        """The unique knots in the U direction."""
        return surface_knots_u(self)

    @property
    def mults_u(self) -> Sequence[int]:
        """The canonical multiplicity of each unique U knot.

        The endpoint multiplicities include knots omitted by native openNURBS
        representations.

        """
        return surface_mults_u(self)

    @property
    def knotvector_u(self) -> list[float]:
        """The complete canonical U knot vector, including endpoint knots."""
        return [knot for knot, multiplicity in zip(self.knots_u, self.mults_u) for _ in range(multiplicity)]

    @property
    def knots_v(self) -> Sequence[float]:
        """The unique knots in the V direction."""
        return surface_knots_v(self)

    @property
    def mults_v(self) -> Sequence[int]:
        """The canonical multiplicity of each unique V knot.

        The endpoint multiplicities include knots omitted by native openNURBS
        representations.

        """
        return surface_mults_v(self)

    @property
    def knotvector_v(self) -> list[float]:
        """The complete canonical V knot vector, including endpoint knots."""
        return [knot for knot, multiplicity in zip(self.knots_v, self.mults_v) for _ in range(multiplicity)]

    @property
    def degree_u(self) -> int:
        """The polynomial degree in the U direction."""
        return surface_degree_u(self)

    @property
    def degree_v(self) -> int:
        """The polynomial degree in the V direction."""
        return surface_degree_v(self)

    @property
    def order_u(self) -> int:
        """The polynomial order in U, equal to `degree_u + 1`."""
        return self.degree_u + 1

    @property
    def order_v(self) -> int:
        """The polynomial order in V, equal to `degree_v + 1`."""
        return self.degree_v + 1

    @property
    def is_rational(self) -> bool:
        """Whether any control-point weight differs from one."""
        return any(weight != 1.0 for row in self.weights for weight in row)

    @property
    def domain_u(self) -> tuple[float, float]:
        """The parameter domain in the U direction."""
        return surface_domain_u(self)

    @property
    def domain_v(self) -> tuple[float, float]:
        """The parameter domain in the V direction."""
        return surface_domain_v(self)

    @property
    def is_periodic_u(self) -> bool:
        """Whether the surface is periodic in the U direction."""
        return surface_is_periodic_u(self)

    @property
    def is_periodic_v(self) -> bool:
        """Whether the surface is periodic in the V direction."""
        return surface_is_periodic_v(self)

    # ==============================================================================
    # Constructors
    # ==============================================================================

    @classmethod
    def from_cylinder(cls, cylinder: "Cylinder") -> "NurbsSurface":
        """Construct a surface from a cylinder.

        Parameters
        ----------
        cylinder
            The cylinder.

        Returns
        -------
        NurbsSurface
            The constructed NURBS surface.

        """
        return from_cylinder(cylinder)

    @classmethod
    def from_extrusion(cls, curve: "Curve", vector: "Vector") -> "NurbsSurface":
        """Construct a NURBS surface from an extrusion of a basis curve.

        Note that the extrusion surface is constructed by generating an infill
        between the basis curve and a translated copy with `from_fill`.

        Parameters
        ----------
        curve
            The basis curve for the extrusion.
        vector
            The extrusion vector, which serves as a translation vector for the basis curve.

        Returns
        -------
        NurbsSurface
            The constructed NURBS surface.

        """
        return from_extrusion(curve, vector)

    @classmethod
    def from_fill(
        cls,
        curve1: "NurbsCurve",
        curve2: "NurbsCurve",
        curve3: "NurbsCurve | None" = None,
        curve4: "NurbsCurve | None" = None,
        style: Literal["stretch", "coons", "curved"] = "stretch",
    ) -> "NurbsSurface":
        """Construct a NURBS surface from the infill between two, three or four contiguous NURBS curves.

        Parameters
        ----------
        curve1
            The first boundary curve.
        curve2
            The second boundary curve.
        curve3
            The optional third boundary curve.
        curve4
            The optional fourth boundary curve.
        style
            The fill style: `stretch`, `coons`, or `curved`.

        Raises
        ------
        ValueError
            If the fill style is not supported.

        Returns
        -------
        NurbsSurface
            The constructed NURBS surface.

        """
        return from_fill(curve1, curve2, curve3, curve4, style)

    @classmethod
    def from_frame(cls, frame: "Frame") -> "NurbsSurface":
        """Construct a surface from a frame.

        Parameters
        ----------
        frame
            The surface frame.

        Returns
        -------
        NurbsSurface
            The constructed NURBS surface.

        """
        return from_frame(frame)

    @classmethod
    def from_interpolation(cls, points: ControlPointGrid, precision: float = 1e-3) -> "NurbsSurface":
        """Construct a NURBS surface by interpolating a grid of points.

        Parameters
        ----------
        points
            The interpolation point grid.
        precision
            The desired interpolation precision.

        Returns
        -------
        NurbsSurface
            The interpolated NURBS surface.

        """
        return from_interpolation(points, precision=precision)

    @classmethod
    def from_meshgrid(cls, nu: int = 10, nv: int = 10) -> "NurbsSurface":
        """Construct a NURBS surface from a mesh grid.

        Parameters
        ----------
        nu
            The number of grid intervals in the U direction.
        nv
            The number of grid intervals in the V direction.

        Returns
        -------
        NurbsSurface
            The constructed NURBS surface.

        """
        if nu < 1 or nv < 1:
            raise ValueError("A NURBS mesh grid requires at least one interval in each direction.")
        UU, VV = meshgrid(linspace(0.0, float(nu), nu + 1), linspace(0.0, float(nv), nv + 1))
        points: list[list[Point]] = []
        for U, V in zip(UU, VV):
            row = []
            for u, v in zip(U, V):
                row.append(Point(u, v, 0.0))
            points.append(row)
        return NurbsSurface.from_points(points=points)

    @classmethod
    def from_native(cls, surface: object) -> "NurbsSurface":
        """Construct a NURBS surface from a native surface geometry.

        Parameters
        ----------
        surface
            A CAD native surface object.

        Returns
        -------
        NurbsSurface
            The constructed NURBS surface.

        """
        return from_native(surface)

    @classmethod
    def from_parameters(
        cls,
        points: ControlPointGrid,
        weights: WeightGrid,
        knots_u: Sequence[float],
        knots_v: Sequence[float],
        mults_u: Sequence[int],
        mults_v: Sequence[int],
        degree_u: int,
        degree_v: int,
        is_periodic_u: bool = False,
        is_periodic_v: bool = False,
    ) -> "NurbsSurface":
        """Construct a NURBS surface from explicit parameters.

        Parameters
        ----------
        points
            The control points.
        weights
            The weights of the control points.
        knots_u
            The knots in the U direction, without multiplicity.
        knots_v
            The knots in the V direction, without multiplicity.
        mults_u
            Multiplicity of the knots in the U direction.
        mults_v
            Multiplicity of the knots in the V direction.
        degree_u
            Degree in the U direction.
        degree_v
            Degree in the V direction.
        is_periodic_u
            Whether the surface is periodic in the U direction.
        is_periodic_v
            Whether the surface is periodic in the V direction.

        Returns
        -------
        NurbsSurface
            The constructed NURBS surface.

        """
        return from_parameters(
            points,
            weights,
            knots_u,
            knots_v,
            mults_u,
            mults_v,
            degree_u,
            degree_v,
            is_periodic_u=is_periodic_u,
            is_periodic_v=is_periodic_v,
        )

    @classmethod
    def from_plane(cls, plane: "Plane") -> "NurbsSurface":
        """Construct a surface from a plane.

        Parameters
        ----------
        plane
            The plane.

        Returns
        -------
        NurbsSurface
            The constructed NURBS surface.

        """
        return from_plane(plane)

    @classmethod
    def from_points(cls, points: ControlPointGrid, degree_u: int = 3, degree_v: int = 3) -> "NurbsSurface":
        """Construct a NURBS surface from control points.

        Parameters
        ----------
        points
            The control points.
        degree_u
            Degree in the U direction.
        degree_v
            Degree in the V direction.

        Returns
        -------
        NurbsSurface
            The constructed NURBS surface.

        """
        return from_points(points, degree_u=degree_u, degree_v=degree_v)

    @classmethod
    def from_sphere(cls, sphere: "Sphere") -> "NurbsSurface":
        """Construct a surface from a sphere.

        Parameters
        ----------
        sphere
            The sphere.

        Returns
        -------
        NurbsSurface
            The constructed NURBS surface.

        """
        return from_sphere(sphere)

    @classmethod
    def from_step(cls, filepath: FilePath) -> "NurbsSurface":
        """Load a NURBS surface from a STP file.

        Parameters
        ----------
        filepath
            The path to the STEP file.

        Returns
        -------
        NurbsSurface
            The loaded NURBS surface.

        """
        return from_step(filepath)

    @classmethod
    def from_torus(cls, torus: "Torus") -> "NurbsSurface":
        """Construct a surface from a torus.

        Parameters
        ----------
        torus
            The torus.

        Returns
        -------
        NurbsSurface
            The constructed NURBS surface.

        """
        return from_torus(torus)

    # ==============================================================================
    # Conversions
    # ==============================================================================

    def to_step(self, filepath: FilePath, schema: str = "AP203") -> None:
        """Write the surface to a STEP file.

        Parameters
        ----------
        filepath
            The output path.
        schema
            The STEP schema.

        """
        surface_to_step(self, filepath, schema=schema)

    def to_brep(self) -> "Brep":
        """Convert the surface to a boundary representation.

        Returns
        -------
        Brep
            The boundary representation.

        """
        return surface_to_brep(self)

    # ==============================================================================
    # Methods
    # ==============================================================================

    def transform(self, transformation: TransformationType) -> None:
        """Transform the surface geometry.

        Parameters
        ----------
        transformation
            The transformation.

        """
        surface_transform(self, transformation)
        self._invalidate_discretization()

    def isocurve_u(self, u: float) -> "Curve | Line":
        """Compute the isoparametric curve at a U parameter."""
        return surface_isocurve_u(self, u)

    def isocurve_v(self, v: float) -> "Curve | Line":
        """Compute the isoparametric curve at a V parameter."""
        return surface_isocurve_v(self, v)

    def boundary(self) -> "list[Curve | Line]":
        """Compute the oriented boundary curves."""
        return surface_boundary(self)

    def point_at(self, u: float, v: float) -> Point:
        """Compute the point at surface parameters."""
        return surface_point_at(self, u, v)

    def normal_at(self, u: float, v: float) -> "Vector":
        """Compute the normal at surface parameters."""
        return surface_normal_at(self, u, v)

    def frame_at(self, u: float, v: float) -> "Frame":
        """Compute the local frame at surface parameters."""
        return surface_frame_at(self, u, v)

    @overload
    def closest_point(self, point: CoordinateType, return_parameters: Literal[False] = False) -> Point | None: ...

    @overload
    def closest_point(
        self,
        point: CoordinateType,
        return_parameters: Literal[True],
    ) -> tuple[Point, tuple[float, float]] | None: ...

    def closest_point(
        self,
        point: CoordinateType,
        return_parameters: bool = False,
    ) -> Point | tuple[Point, tuple[float, float]] | None:
        """Compute the closest point on the surface."""
        return surface_closest_point(self, point, return_parameters=return_parameters)

    def copy(self, copy_guid: bool = False) -> "NurbsSurface":  # type: ignore[override]
        """Make an independent copy of the surface.

        Parameters
        ----------
        copy_guid
            If `True`, preserve the globally unique identifier.

        Returns
        -------
        NurbsSurface
            The independent copy.

        """
        surface = NurbsSurface.from_parameters(
            self.control_points,
            self.weights,
            self.knots_u,
            self.knots_v,
            self.mults_u,
            self.mults_v,
            self.degree_u,
            self.degree_v,
            self.is_periodic_u,
            self.is_periodic_v,
        )
        if copy_guid:
            surface._guid = self.guid
        return surface
