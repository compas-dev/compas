"""Pluggable operations for the backend-neutral Brep wrapper."""

from collections.abc import Sequence
from os import PathLike
from typing import TYPE_CHECKING
from typing import Any
from typing import Literal
from typing import TypedDict

from compas.plugins import PluginNotInstalledError
from compas.plugins import pluggable

if TYPE_CHECKING:
    from compas.datastructures import Mesh
    from compas.geometry import Box
    from compas.geometry import Cone
    from compas.geometry import Curve
    from compas.geometry import Cylinder
    from compas.geometry import Frame
    from compas.geometry import Plane
    from compas.geometry import Point
    from compas.geometry import Polygon
    from compas.geometry import Polyline
    from compas.geometry import Sphere
    from compas.geometry import Surface
    from compas.geometry import Torus
    from compas.geometry import Vector

    from .brep import Brep
    from .edge import BrepEdge
    from .face import BrepFace
    from .loop import BrepLoop
    from .trim import BrepTrim
    from .vertex import BrepVertex


class BrepClassification(TypedDict):
    """Backend-independent classification values for a Brep."""

    orientation: Literal[0, 1, 2, 3]
    type: Literal[0, 1, 2, 3, 4, 5, 6, 7, 8]
    is_valid: bool
    is_orientable: bool
    is_closed: bool
    is_infinite: bool
    is_convex: bool
    is_manifold: bool
    is_surface: bool
    is_compound: bool
    is_compoundsolid: bool
    is_shell: bool
    is_solid: bool


class BrepTopology(TypedDict):
    """Backend-independent topology extracted from a Brep."""

    vertices: list["BrepVertex"]
    edges: list["BrepEdge"]
    trims: list["BrepTrim"]
    loops: list["BrepLoop"]
    faces: list["BrepFace"]
    shells: list["Brep"]
    solids: list["Brep"]


@pluggable(category="brep-factories")
def from_box(box: "Box") -> "Brep":
    raise PluginNotInstalledError


@pluggable(category="brep-factories")
def from_brepfaces(faces: Sequence["BrepFace"]) -> "Brep":
    raise PluginNotInstalledError


@pluggable(category="brep-factories")
def from_breps(breps: Sequence["Brep"], *args: Any, **kwargs: Any) -> "Brep":
    raise PluginNotInstalledError


@pluggable(category="brep-factories")
def from_cone(cone: "Cone", *args: Any, **kwargs: Any) -> "Brep":
    raise PluginNotInstalledError


@pluggable(category="brep-factories")
def from_curves(curves: Sequence["Curve"]) -> "Brep":
    raise PluginNotInstalledError


@pluggable(category="brep-factories")
def from_cylinder(cylinder: "Cylinder") -> "Brep":
    raise PluginNotInstalledError


@pluggable(category="brep-factories")
def from_extrusion(curve: "Curve | Polyline", vector: "Vector", cap_ends: bool = True) -> "Brep":
    raise PluginNotInstalledError


@pluggable(category="brep-io")
def from_iges(filename: str | PathLike[str]) -> "Brep":
    raise PluginNotInstalledError


@pluggable(category="brep-factories")
def from_loft(curves: Sequence["Curve"]) -> "Brep":
    raise PluginNotInstalledError


@pluggable(category="brep-factories")
def from_mesh(mesh: "Mesh") -> "Brep":
    raise PluginNotInstalledError


@pluggable(category="brep-factories")
def from_native(native_brep: Any) -> "Brep":
    raise PluginNotInstalledError


@pluggable(category="brep-factories")
def from_pipe(path: "Curve", radius: float, *args: Any, **kwargs: Any) -> "Brep":
    raise PluginNotInstalledError


@pluggable(category="brep-factories")
def from_plane(plane: "Plane", domain_u: tuple[float, float] = (-1, 1), domain_v: tuple[float, float] = (-1, 1)) -> "Brep":
    raise PluginNotInstalledError


@pluggable(category="brep-factories")
def from_planes(planes: Sequence["Plane"]) -> "Brep":
    raise PluginNotInstalledError


@pluggable(category="brep-factories")
def from_polygons(polygons: Sequence["Polygon"], *args: Any, **kwargs: Any) -> "Brep":
    raise PluginNotInstalledError


@pluggable(category="brep-factories")
def from_sphere(sphere: "Sphere") -> "Brep":
    raise PluginNotInstalledError


@pluggable(category="brep-io")
def from_step(filename: str | PathLike[str]) -> "Brep":
    raise PluginNotInstalledError


@pluggable(category="brep-factories")
def from_sweep(profile: "BrepEdge | BrepFace", path: "BrepLoop", *args: Any, **kwargs: Any) -> "Brep":
    raise PluginNotInstalledError


@pluggable(category="brep-factories")
def from_torus(torus: "Torus") -> "Brep":
    raise PluginNotInstalledError


@pluggable(category="brep-operations")
def from_boolean_difference(brep_a: "Brep | list[Brep]", brep_b: "Brep | list[Brep]") -> "Brep":
    raise PluginNotInstalledError


@pluggable(category="brep-operations")
def from_boolean_intersection(brep_a: "Brep | list[Brep]", brep_b: "Brep | list[Brep]") -> "Brep":
    raise PluginNotInstalledError


@pluggable(category="brep-operations")
def from_boolean_union(brep_a: "Brep | list[Brep]", brep_b: "Brep | list[Brep]") -> "Brep":
    raise PluginNotInstalledError


@pluggable(category="brep-serialization")
def brep_rebuild(brep: "Brep", data: dict[str, Any]) -> None:
    raise PluginNotInstalledError


@pluggable(category="brep-serialization")
def brep_to_data(brep: "Brep") -> dict[str, Any]:
    raise PluginNotInstalledError


@pluggable(category="brep-queries")
def brep_area(brep: "Brep") -> float:
    raise PluginNotInstalledError


@pluggable(category="brep-queries")
def brep_centroid(brep: "Brep") -> "Point":
    raise PluginNotInstalledError


@pluggable(category="brep-queries")
def brep_classification(brep: "Brep") -> BrepClassification:
    raise PluginNotInstalledError


@pluggable(category="brep-queries")
def brep_frame(brep: "Brep") -> "Frame":
    raise PluginNotInstalledError


@pluggable(category="brep-queries")
def brep_topology(brep: "Brep") -> BrepTopology:
    raise PluginNotInstalledError


@pluggable(category="brep-queries")
def brep_volume(brep: "Brep") -> float:
    raise PluginNotInstalledError


@pluggable(category="brep-operations")
def brep_contains(brep: "Brep", object: "Point | Curve | Surface") -> bool:
    raise PluginNotInstalledError


@pluggable(category="brep-operations")
def brep_contours(brep: "Brep", planes: Sequence["Plane"]) -> list[list["Polyline"]]:
    raise PluginNotInstalledError


@pluggable(category="brep-operations")
def brep_tessellate(
    brep: "Brep",
    linear_deflection: float | None = None,
    angular_deflection: float | None = None,
    **kwargs: Any,
) -> tuple["Mesh", list["Polyline"]]:
    raise PluginNotInstalledError


@pluggable(category="brep-operations")
def brep_cap_planar_holes(brep: "Brep", tolerance: float | None = None) -> "Brep":
    raise PluginNotInstalledError


@pluggable(category="brep-operations")
def brep_cull_unused_edges(brep: "Brep") -> "Brep":
    raise PluginNotInstalledError


@pluggable(category="brep-operations")
def brep_cull_unused_faces(brep: "Brep") -> "Brep":
    raise PluginNotInstalledError


@pluggable(category="brep-operations")
def brep_cull_unused_loops(brep: "Brep") -> "Brep":
    raise PluginNotInstalledError


@pluggable(category="brep-operations")
def brep_cull_unused_vertices(brep: "Brep") -> "Brep":
    raise PluginNotInstalledError


@pluggable(category="brep-operations")
def brep_fillet(brep: "Brep", radius: float, exclude: Sequence["BrepEdge"] | None = None) -> "Brep":
    raise PluginNotInstalledError


@pluggable(category="brep-operations")
def brep_fix(brep: "Brep") -> "Brep":
    raise PluginNotInstalledError


@pluggable(category="brep-operations")
def brep_flip(brep: "Brep") -> "Brep":
    raise PluginNotInstalledError


@pluggable(category="brep-operations")
def brep_heal(brep: "Brep") -> "Brep":
    raise PluginNotInstalledError


@pluggable(category="brep-operations")
def brep_make_solid(brep: "Brep") -> "Brep":
    raise PluginNotInstalledError


@pluggable(category="brep-operations")
def brep_overlap(
    brep_a: "Brep",
    brep_b: "Brep",
    linear_deflection: float | None = None,
    angular_deflection: float | None = None,
    tolerance: float = 0.0,
    relative: bool = False,
) -> tuple[list["BrepFace"], list["BrepFace"]]:
    raise PluginNotInstalledError


@pluggable(category="brep-operations")
def brep_sew(brep: "Brep") -> "Brep":
    raise PluginNotInstalledError


@pluggable(category="brep-operations")
def brep_slice(brep: "Brep", plane: "Plane | Frame") -> "Brep | None":
    raise PluginNotInstalledError


@pluggable(category="brep-operations")
def brep_split(brep: "Brep", cutter: "Brep") -> list["Brep"]:
    raise PluginNotInstalledError


@pluggable(category="brep-operations")
def brep_trimmed(brep: "Brep", plane: "Plane | Frame") -> "Brep":
    raise PluginNotInstalledError


@pluggable(category="brep-io")
def brep_to_iges(brep: "Brep", filepath: str | PathLike[str]) -> bool:
    raise PluginNotInstalledError


@pluggable(category="brep-io")
def brep_to_step(brep: "Brep", filepath: str | PathLike[str]) -> None:
    raise PluginNotInstalledError


@pluggable(category="brep-io")
def brep_to_stl(brep: "Brep", filepath: str | PathLike[str]) -> bool:
    raise PluginNotInstalledError
