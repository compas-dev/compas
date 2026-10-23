"""Pluggable operations for the backend-neutral NURBS curve wrapper."""

from collections.abc import Sequence
from typing import TYPE_CHECKING

from compas._typing import CoordinateType
from compas._typing import FilePath
from compas.geometry._typing import TransformationType
from compas.plugins import PluginNotInstalledError
from compas.plugins import pluggable

if TYPE_CHECKING:
    from compas.geometry import Arc
    from compas.geometry import Point
    from compas.geometry import Vector

    from .nurbs import NurbsCurve


@pluggable(category="nurbscurve-factories")
def from_arc(arc: "Arc") -> "NurbsCurve":
    raise PluginNotInstalledError


@pluggable(category="nurbscurve-factories")
def from_interpolation(points: Sequence[CoordinateType], precision: float = 1e-3) -> "NurbsCurve":
    raise PluginNotInstalledError


@pluggable(category="nurbscurve-factories")
def from_native(native_curve: object) -> "NurbsCurve":
    raise PluginNotInstalledError


@pluggable(category="nurbscurve-factories")
def from_parameters(
    points: Sequence[CoordinateType],
    weights: Sequence[float],
    knots: Sequence[float],
    multiplicities: Sequence[int],
    degree: int,
    is_periodic: bool = False,
) -> "NurbsCurve":
    raise PluginNotInstalledError


@pluggable(category="nurbscurve-factories")
def from_points(points: Sequence[CoordinateType], degree: int = 3, is_periodic: bool = False) -> "NurbsCurve":
    raise PluginNotInstalledError


@pluggable(category="nurbscurve-io")
def from_step(filepath: FilePath) -> "NurbsCurve":
    raise PluginNotInstalledError


@pluggable(category="nurbscurve-queries")
def curve_points(curve: "NurbsCurve") -> list["Point"]:
    raise PluginNotInstalledError


@pluggable(category="nurbscurve-queries")
def curve_weights(curve: "NurbsCurve") -> list[float]:
    raise PluginNotInstalledError


@pluggable(category="nurbscurve-queries")
def curve_knots(curve: "NurbsCurve") -> list[float]:
    raise PluginNotInstalledError


@pluggable(category="nurbscurve-queries")
def curve_multiplicities(curve: "NurbsCurve") -> list[int]:
    raise PluginNotInstalledError


@pluggable(category="nurbscurve-queries")
def curve_continuity(curve: "NurbsCurve") -> int:
    raise PluginNotInstalledError


@pluggable(category="nurbscurve-queries")
def curve_degree(curve: "NurbsCurve") -> int:
    raise PluginNotInstalledError


@pluggable(category="nurbscurve-queries")
def curve_is_rational(curve: "NurbsCurve") -> bool:
    raise PluginNotInstalledError


@pluggable(category="nurbscurve-queries")
def curve_domain(curve: "NurbsCurve") -> tuple[float, float]:
    raise PluginNotInstalledError


@pluggable(category="nurbscurve-queries")
def curve_length(curve: "NurbsCurve") -> float:
    raise PluginNotInstalledError


@pluggable(category="nurbscurve-queries")
def curve_is_closed(curve: "NurbsCurve") -> bool:
    raise PluginNotInstalledError


@pluggable(category="nurbscurve-queries")
def curve_is_periodic(curve: "NurbsCurve") -> bool:
    raise PluginNotInstalledError


@pluggable(category="nurbscurve-evaluation")
def curve_point_at(curve: "NurbsCurve", t: float, world: bool = True) -> "Point":
    raise PluginNotInstalledError


@pluggable(category="nurbscurve-evaluation")
def curve_normal_at(curve: "NurbsCurve", t: float, world: bool = True) -> "Vector | None":
    raise PluginNotInstalledError


@pluggable(category="nurbscurve-evaluation")
def curve_tangent_at(curve: "NurbsCurve", t: float, world: bool = True) -> "Vector":
    raise PluginNotInstalledError


@pluggable(category="nurbscurve-evaluation")
def curve_curvature_at(curve: "NurbsCurve", t: float) -> "Vector":
    raise PluginNotInstalledError


@pluggable(category="nurbscurve-operations")
def curve_transform(curve: "NurbsCurve", transformation: TransformationType) -> None:
    raise PluginNotInstalledError


@pluggable(category="nurbscurve-operations")
def curve_reverse(curve: "NurbsCurve") -> None:
    raise PluginNotInstalledError


@pluggable(category="nurbscurve-operations")
def curve_closest_point(
    curve: "NurbsCurve", point: CoordinateType, return_parameter: bool = False
) -> "Point | tuple[Point, float]":
    raise PluginNotInstalledError


@pluggable(category="nurbscurve-operations")
def curve_divide_by_count(
    curve: "NurbsCurve", count: int, return_points: bool = False
) -> "list[float] | tuple[list[float], list[Point]]":
    raise PluginNotInstalledError


@pluggable(category="nurbscurve-operations")
def curve_divide_by_length(
    curve: "NurbsCurve", length: float, return_points: bool = False
) -> "list[float] | tuple[list[float], list[Point]]":
    raise PluginNotInstalledError


@pluggable(category="nurbscurve-io")
def curve_to_step(curve: "NurbsCurve", filepath: FilePath, schema: str = "AP203") -> None:
    raise PluginNotInstalledError


@pluggable(category="nurbscurve-io")
def curve_to_obj(curve: "NurbsCurve", filepath: FilePath) -> None:
    raise PluginNotInstalledError
