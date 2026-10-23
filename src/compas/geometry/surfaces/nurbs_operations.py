"""Pluggable operations for the backend-neutral NURBS surface wrapper."""

from collections.abc import Sequence
from typing import TYPE_CHECKING
from typing import Literal

from compas._typing import CoordinateType
from compas._typing import FilePath
from compas.geometry._typing import TransformationType
from compas.plugins import PluginNotInstalledError
from compas.plugins import pluggable

if TYPE_CHECKING:
    from compas.geometry import Brep
    from compas.geometry import Curve
    from compas.geometry import Cylinder
    from compas.geometry import Frame
    from compas.geometry import Line
    from compas.geometry import NurbsCurve
    from compas.geometry import Plane
    from compas.geometry import Point
    from compas.geometry import Sphere
    from compas.geometry import Torus
    from compas.geometry import Vector

    from .nurbs import NurbsSurface

type ControlPointGrid = Sequence[Sequence[CoordinateType]]
type WeightGrid = Sequence[Sequence[float]]


@pluggable(category="nurbssurface-factories")
def from_cylinder(cylinder: "Cylinder") -> "NurbsSurface":
    raise PluginNotInstalledError


@pluggable(category="nurbssurface-factories")
def from_extrusion(curve: "Curve", vector: "Vector") -> "NurbsSurface":
    raise PluginNotInstalledError


@pluggable(category="nurbssurface-factories")
def from_fill(
    curve1: "NurbsCurve",
    curve2: "NurbsCurve",
    curve3: "NurbsCurve | None" = None,
    curve4: "NurbsCurve | None" = None,
    style: Literal["stretch", "coons", "curved"] = "stretch",
) -> "NurbsSurface":
    raise PluginNotInstalledError


@pluggable(category="nurbssurface-factories")
def from_frame(frame: "Frame") -> "NurbsSurface":
    raise PluginNotInstalledError


@pluggable(category="nurbssurface-factories")
def from_interpolation(points: ControlPointGrid, precision: float = 1e-3) -> "NurbsSurface":
    raise PluginNotInstalledError


@pluggable(category="nurbssurface-factories")
def from_native(native_surface: object) -> "NurbsSurface":
    raise PluginNotInstalledError


@pluggable(category="nurbssurface-factories")
def from_parameters(
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
    raise PluginNotInstalledError


@pluggable(category="nurbssurface-factories")
def from_plane(plane: "Plane") -> "NurbsSurface":
    raise PluginNotInstalledError


@pluggable(category="nurbssurface-factories")
def from_points(points: ControlPointGrid, degree_u: int = 3, degree_v: int = 3) -> "NurbsSurface":
    raise PluginNotInstalledError


@pluggable(category="nurbssurface-factories")
def from_sphere(sphere: "Sphere") -> "NurbsSurface":
    raise PluginNotInstalledError


@pluggable(category="nurbssurface-io")
def from_step(filepath: FilePath) -> "NurbsSurface":
    raise PluginNotInstalledError


@pluggable(category="nurbssurface-factories")
def from_torus(torus: "Torus") -> "NurbsSurface":
    raise PluginNotInstalledError


@pluggable(category="nurbssurface-queries")
def surface_points(surface: "NurbsSurface") -> Sequence[Sequence["Point"]]:
    raise PluginNotInstalledError


@pluggable(category="nurbssurface-queries")
def surface_weights(surface: "NurbsSurface") -> Sequence[Sequence[float]]:
    raise PluginNotInstalledError


@pluggable(category="nurbssurface-queries")
def surface_knots_u(surface: "NurbsSurface") -> Sequence[float]:
    raise PluginNotInstalledError


@pluggable(category="nurbssurface-queries")
def surface_knots_v(surface: "NurbsSurface") -> Sequence[float]:
    raise PluginNotInstalledError


@pluggable(category="nurbssurface-queries")
def surface_mults_u(surface: "NurbsSurface") -> Sequence[int]:
    raise PluginNotInstalledError


@pluggable(category="nurbssurface-queries")
def surface_mults_v(surface: "NurbsSurface") -> Sequence[int]:
    raise PluginNotInstalledError


@pluggable(category="nurbssurface-queries")
def surface_degree_u(surface: "NurbsSurface") -> int:
    raise PluginNotInstalledError


@pluggable(category="nurbssurface-queries")
def surface_degree_v(surface: "NurbsSurface") -> int:
    raise PluginNotInstalledError


@pluggable(category="nurbssurface-queries")
def surface_domain_u(surface: "NurbsSurface") -> tuple[float, float]:
    raise PluginNotInstalledError


@pluggable(category="nurbssurface-queries")
def surface_domain_v(surface: "NurbsSurface") -> tuple[float, float]:
    raise PluginNotInstalledError


@pluggable(category="nurbssurface-queries")
def surface_is_periodic_u(surface: "NurbsSurface") -> bool:
    raise PluginNotInstalledError


@pluggable(category="nurbssurface-queries")
def surface_is_periodic_v(surface: "NurbsSurface") -> bool:
    raise PluginNotInstalledError


@pluggable(category="nurbssurface-evaluation")
def surface_isocurve_u(surface: "NurbsSurface", u: float) -> "Curve | Line":
    raise PluginNotInstalledError


@pluggable(category="nurbssurface-evaluation")
def surface_isocurve_v(surface: "NurbsSurface", v: float) -> "Curve | Line":
    raise PluginNotInstalledError


@pluggable(category="nurbssurface-evaluation")
def surface_boundary(surface: "NurbsSurface") -> "list[Curve | Line]":
    raise PluginNotInstalledError


@pluggable(category="nurbssurface-evaluation")
def surface_point_at(surface: "NurbsSurface", u: float, v: float) -> "Point":
    raise PluginNotInstalledError


@pluggable(category="nurbssurface-evaluation")
def surface_normal_at(surface: "NurbsSurface", u: float, v: float) -> "Vector":
    raise PluginNotInstalledError


@pluggable(category="nurbssurface-evaluation")
def surface_frame_at(surface: "NurbsSurface", u: float, v: float) -> "Frame":
    raise PluginNotInstalledError


@pluggable(category="nurbssurface-evaluation")
def surface_closest_point(
    surface: "NurbsSurface", point: CoordinateType, return_parameters: bool = False
) -> "Point | tuple[Point, tuple[float, float]] | None":
    raise PluginNotInstalledError


@pluggable(category="nurbssurface-operations")
def surface_transform(surface: "NurbsSurface", transformation: TransformationType) -> None:
    raise PluginNotInstalledError


@pluggable(category="nurbssurface-operations")
def surface_to_brep(surface: "NurbsSurface") -> "Brep":
    raise PluginNotInstalledError


@pluggable(category="nurbssurface-io")
def surface_to_step(surface: "NurbsSurface", filepath: FilePath, schema: str = "AP203") -> None:
    raise PluginNotInstalledError
