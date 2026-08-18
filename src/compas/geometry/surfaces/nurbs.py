from typing import TYPE_CHECKING
from typing import Any
from typing import Literal
from typing import Optional
from typing import Sequence
from typing import TypeVar

from typing_extensions import Self

from compas._typing import CoordinateType
from compas._typing import FilePath
from compas.geometry import Point
from compas.itertools import linspace
from compas.itertools import meshgrid
from compas.plugins import PluginNotInstalledError
from compas.plugins import pluggable

from .surface import Surface

if TYPE_CHECKING:
    from compas.geometry import Curve
    from compas.geometry import Cylinder
    from compas.geometry import Frame
    from compas.geometry import NurbsCurve
    from compas.geometry import Plane
    from compas.geometry import Sphere
    from compas.geometry import Torus
    from compas.geometry import Vector

ControlPointGrid = Sequence[Sequence[CoordinateType]]
WeightGrid = Sequence[Sequence[float]]
NurbsSurfaceType = TypeVar("NurbsSurfaceType", bound="NurbsSurface")


@pluggable(category="factories")
def nurbssurface_from_cylinder(cls: type[NurbsSurfaceType], cylinder: "Cylinder") -> NurbsSurfaceType:
    raise PluginNotInstalledError


@pluggable(category="factories")
def nurbssurface_from_extrusion(cls: type[NurbsSurfaceType], curve: "Curve", vector: "Vector") -> NurbsSurfaceType:
    raise PluginNotInstalledError


@pluggable(category="factories")
def nurbssurface_from_fill(
    cls: type[NurbsSurfaceType],
    curve1: "NurbsCurve",
    curve2: "NurbsCurve",
    curve3: Optional["NurbsCurve"] = None,
    curve4: Optional["NurbsCurve"] = None,
    style: Literal["stretch", "coons", "curved"] = "stretch",
) -> NurbsSurfaceType:
    raise PluginNotInstalledError


@pluggable(category="factories")
def nurbssurface_from_frame(cls: type[NurbsSurfaceType], frame: "Frame") -> NurbsSurfaceType:
    raise PluginNotInstalledError


@pluggable(category="factories")
def nurbssurface_from_interpolation(
    cls: type[NurbsSurfaceType],
    points: ControlPointGrid,
    precision: float = 1e-3,
) -> NurbsSurfaceType:
    raise PluginNotInstalledError


@pluggable(category="factories")
def nurbssurface_from_native(cls: type[NurbsSurfaceType], surface: object) -> NurbsSurfaceType:
    raise PluginNotInstalledError


@pluggable(category="factories")
def nurbssurface_from_parameters(
    cls: type[NurbsSurfaceType],
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
) -> NurbsSurfaceType:
    raise PluginNotInstalledError


@pluggable(category="factories")
def nurbssurface_from_plane(cls: type[NurbsSurfaceType], plane: "Plane") -> NurbsSurfaceType:
    raise PluginNotInstalledError


@pluggable(category="factories")
def nurbssurface_from_points(
    cls: type[NurbsSurfaceType],
    points: ControlPointGrid,
    degree_u: int = 3,
    degree_v: int = 3,
) -> NurbsSurfaceType:
    raise PluginNotInstalledError


@pluggable(category="factories")
def nurbssurface_from_sphere(cls: type[NurbsSurfaceType], sphere: "Sphere") -> NurbsSurfaceType:
    raise PluginNotInstalledError


@pluggable(category="factories")
def nurbssurface_from_step(cls: type[NurbsSurfaceType], filepath: FilePath) -> NurbsSurfaceType:
    raise PluginNotInstalledError


@pluggable(category="factories")
def nurbssurface_from_torus(cls: type[NurbsSurfaceType], torus: "Torus") -> NurbsSurfaceType:
    raise PluginNotInstalledError


class NurbsSurface(Surface):
    """A NURBS surface defined by control points, weights, knots, and degrees.

    Parameters
    ----------
    name
        The name of the surface.

    Notes
    -----
    `NurbsSurface` defines a backend contract. Concrete implementations are
    supplied through the plugin mechanism, for example by Rhino or OCC.

    Knot data exposed by this contract uses the full mathematical convention.
    The complete knot vectors include all endpoint knots, including the two
    knots that openNURBS considers superfluous and omits from native Rhino knot
    lists. Rhino implementations are responsible for removing those knots when
    constructing native geometry and restoring them when exposing COMPAS knot
    data.

    Control points and weights use row-major parameter order. The outer
    sequence contains V rows and every row contains values along U; therefore a
    nested value is addressed as `points[v][u]` or `weights[v][u]`.

    """

    @property
    def __dtype__(self) -> str:
        return "compas.geometry/NurbsSurface"

    @property
    def __data__(self) -> dict[str, Any]:
        """The data representation of the NURBS surface."""
        return {
            "points": [[point.__data__ for point in row] for row in self.points],
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
    def __from_data__(cls, data: dict[str, Any]) -> Self:
        return cls.from_parameters(
            data["points"],
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

    def __new__(cls, *args: object, **kwargs: object) -> Self:
        if cls is NurbsSurface:
            raise TypeError("Making an instance of `NurbsSurface` using `NurbsSurface()` is not allowed. Please use one of the factory methods instead (`NurbsSurface.from_...`)")
        return object.__new__(cls)

    def __repr__(self) -> str:
        return "{0}(points={1!r}, weights={2}, knots_u={3}, knots_v={4}, mults_u={5}, mults_v={6}, degree_u={7}, degree_v={8}, is_periodic_u={9}, is_periodic_v={10})".format(
            type(self).__name__,
            self.points,
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
    def points(self) -> Sequence[Sequence[Point]]:
        """The control points in V rows, with each row running along U."""
        raise NotImplementedError

    @property
    def weights(self) -> Sequence[Sequence[float]]:
        """The control-point weights in the same V-by-U layout as `points`."""
        raise NotImplementedError

    @property
    def knots_u(self) -> Sequence[float]:
        """The unique knots in the U direction."""
        raise NotImplementedError

    @property
    def mults_u(self) -> Sequence[int]:
        """The canonical multiplicity of each unique U knot.

        The endpoint multiplicities include knots omitted by native openNURBS
        representations.

        """
        raise NotImplementedError

    @property
    def knotvector_u(self) -> list[float]:
        """The complete canonical U knot vector, including endpoint knots."""
        return [knot for knot, multiplicity in zip(self.knots_u, self.mults_u) for _ in range(multiplicity)]

    @property
    def knots_v(self) -> Sequence[float]:
        """The unique knots in the V direction."""
        raise NotImplementedError

    @property
    def mults_v(self) -> Sequence[int]:
        """The canonical multiplicity of each unique V knot.

        The endpoint multiplicities include knots omitted by native openNURBS
        representations.

        """
        raise NotImplementedError

    @property
    def knotvector_v(self) -> list[float]:
        """The complete canonical V knot vector, including endpoint knots."""
        return [knot for knot, multiplicity in zip(self.knots_v, self.mults_v) for _ in range(multiplicity)]

    @property
    def degree_u(self) -> int:
        """The polynomial degree in the U direction."""
        raise NotImplementedError

    @property
    def degree_v(self) -> int:
        """The polynomial degree in the V direction."""
        raise NotImplementedError

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
        raise NotImplementedError

    @property
    def domain_v(self) -> tuple[float, float]:
        """The parameter domain in the V direction."""
        raise NotImplementedError

    # ==============================================================================
    # Constructors
    # ==============================================================================

    @classmethod
    def from_cylinder(cls, cylinder: "Cylinder") -> Self:
        """Construct a surface from a cylinder.

        Parameters
        ----------
        cylinder
            The cylinder.

        Returns
        -------
        Self
            The constructed NURBS surface.

        """
        return nurbssurface_from_cylinder(cls, cylinder)

    @classmethod
    def from_extrusion(cls, curve: "Curve", vector: "Vector") -> Self:
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
        Self
            The constructed NURBS surface.

        """
        return nurbssurface_from_extrusion(cls, curve, vector)

    @classmethod
    def from_fill(
        cls,
        curve1: "NurbsCurve",
        curve2: "NurbsCurve",
        curve3: Optional["NurbsCurve"] = None,
        curve4: Optional["NurbsCurve"] = None,
        style: Literal["stretch", "coons", "curved"] = "stretch",
    ) -> Self:
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
        Self
            The constructed NURBS surface.

        """
        return nurbssurface_from_fill(cls, curve1, curve2, curve3, curve4, style)

    @classmethod
    def from_frame(cls, frame: "Frame") -> Self:
        """Construct a surface from a frame.

        Parameters
        ----------
        frame
            The surface frame.

        Returns
        -------
        Self
            The constructed NURBS surface.

        """
        return nurbssurface_from_frame(cls, frame)

    @classmethod
    def from_interpolation(cls, points: ControlPointGrid, precision: float = 1e-3) -> Self:
        """Construct a NURBS surface by interpolating a grid of points.

        Parameters
        ----------
        points
            The interpolation point grid.
        precision
            The desired interpolation precision.

        Returns
        -------
        Self
            The interpolated NURBS surface.

        """
        return nurbssurface_from_interpolation(cls, points, precision=precision)

    @classmethod
    def from_meshgrid(cls, nu: int = 10, nv: int = 10) -> Self:
        """Construct a NURBS surface from a mesh grid.

        Parameters
        ----------
        nu
            The number of grid intervals in the U direction.
        nv
            The number of grid intervals in the V direction.

        Returns
        -------
        Self
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
        return cls.from_points(points=points)

    @classmethod
    def from_native(cls, surface: object) -> Self:
        """Construct a NURBS surface from a native surface geometry.

        Parameters
        ----------
        surface
            A CAD native surface object.

        Returns
        -------
        Self
            The constructed NURBS surface.

        """
        return nurbssurface_from_native(cls, surface)

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
    ) -> Self:
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
        Self
            The constructed NURBS surface.

        """
        return nurbssurface_from_parameters(
            cls,
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
    def from_plane(cls, plane: "Plane") -> Self:
        """Construct a surface from a plane.

        Parameters
        ----------
        plane
            The plane.

        Returns
        -------
        Self
            The constructed NURBS surface.

        """
        return nurbssurface_from_plane(cls, plane)

    @classmethod
    def from_points(cls, points: ControlPointGrid, degree_u: int = 3, degree_v: int = 3) -> Self:
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
        Self
            The constructed NURBS surface.

        """
        return nurbssurface_from_points(cls, points, degree_u=degree_u, degree_v=degree_v)

    @classmethod
    def from_sphere(cls, sphere: "Sphere") -> Self:
        """Construct a surface from a sphere.

        Parameters
        ----------
        sphere
            The sphere.

        Returns
        -------
        Self
            The constructed NURBS surface.

        """
        return nurbssurface_from_sphere(cls, sphere)

    @classmethod
    def from_step(cls, filepath: FilePath) -> Self:
        """Load a NURBS surface from a STP file.

        Parameters
        ----------
        filepath
            The path to the STEP file.

        Returns
        -------
        Self
            The loaded NURBS surface.

        """
        return nurbssurface_from_step(cls, filepath)

    @classmethod
    def from_torus(cls, torus: "Torus") -> Self:
        """Construct a surface from a torus.

        Parameters
        ----------
        torus
            The torus.

        Returns
        -------
        Self
            The constructed NURBS surface.

        """
        return nurbssurface_from_torus(cls, torus)

    # ==============================================================================
    # Conversions
    # ==============================================================================

    # ==============================================================================
    # Methods
    # ==============================================================================

    def copy(self, cls: Optional[type[Self]] = None, copy_guid: bool = False) -> Self:  # type: ignore[override]
        """Make an independent copy of the surface.

        Parameters
        ----------
        cls
            The NURBS surface type to construct. Default is `type(self)`.
        copy_guid
            If `True`, preserve the globally unique identifier.

        Returns
        -------
        Self
            The independent copy.

        """
        surface_type = cls or type(self)
        surface = surface_type.from_parameters(
            self.points,
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
