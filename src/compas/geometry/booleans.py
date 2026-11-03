from typing import TYPE_CHECKING
from typing import Any

from compas._typing import CoordinatesType
from compas.plugins import PluginNotInstalledError
from compas.plugins import pluggable

from ._tessellation_plugin import tessellation_pluggable
from .tessellation import Tessellation

if TYPE_CHECKING:
    from .planar_region import PlanarRegion
    from .polygon import Polygon


def _xy_coordinates(points: Any) -> list[list[float]]:
    return [[point[0], point[1]] for point in points]


def _shapely_polygon(region: "PlanarRegion | Polygon | CoordinatesType") -> Any:
    from shapely.geometry import Polygon  # pyright: ignore[reportMissingModuleSource]

    outer = getattr(region, "outer", None)
    if outer is not None:
        return Polygon(
            _xy_coordinates(outer.points),
            [_xy_coordinates(hole.points) for hole in getattr(region, "holes")],
        )
    return Polygon(_xy_coordinates(getattr(region, "points", region)))


def _planar_regions(geometry: Any) -> list["PlanarRegion"]:
    from compas.geometry import PlanarRegion

    def polygons_of(item: Any) -> list[Any]:
        if item.is_empty:
            return []
        if item.geom_type == "Polygon":
            return [item]
        if item.geom_type in {"MultiPolygon", "GeometryCollection"}:
            return [polygon for part in item.geoms for polygon in polygons_of(part)]
        return []

    return [
        PlanarRegion(
            [[x, y, 0.0] for x, y in polygon.exterior.coords[:-1]],
            holes=[[[x, y, 0.0] for x, y in ring.coords[:-1]] for ring in polygon.interiors],
        )
        for polygon in polygons_of(geometry)
    ]


@tessellation_pluggable(category="booleans", inputs=("A", "B"), result=True)
def boolean_union_mesh_mesh(A: "Tessellation", B: "Tessellation") -> "Tessellation":
    """Compute the boolean union of two triangle meshes.

    Parameters
    ----------
    A
        The first triangle tessellation.
    B
        The second triangle tessellation.

    Returns
    -------
    Tessellation
        The triangle geometry of the boolean union.

    See Also
    --------
    [`boolean_difference_mesh_mesh`][compas.geometry.boolean_difference_mesh_mesh]
    [`boolean_intersection_mesh_mesh`][compas.geometry.boolean_intersection_mesh_mesh]

    Notes
    -----
    This function requires a Boolean plugin, such as `compas_cgal`.

    Examples
    --------
    >>> from compas.geometry import Box, Native, Sphere, UVGrid
    >>> from compas.geometry import boolean_union_mesh_mesh  # doctest: +SKIP
    >>> from compas.geometry import trimesh_remesh  # doctest: +SKIP

    >>> box = Box.from_width_height_depth(2, 2, 2)
    >>> A = box.tessellate(Native())

    >>> sphere = Sphere.from_point_and_radius([1, 1, 1], 1)
    >>> B = sphere.tessellate(UVGrid(30, 30))

    >>> B = trimesh_remesh(B, 0.3, 10)  # doctest: +SKIP
    >>> union = boolean_union_mesh_mesh(A, B)  # doctest: +SKIP

    """
    raise PluginNotInstalledError("No plugin was found for the boolean_union_mesh_mesh pluggable. A plugin is available in compas_cgal...")


@tessellation_pluggable(category="booleans", inputs=("A", "B"), result=True)
def boolean_difference_mesh_mesh(A: "Tessellation", B: "Tessellation") -> "Tessellation":
    """Compute the boolean difference of two triangle meshes.

    Parameters
    ----------
    A
        The first triangle tessellation.
    B
        The second triangle tessellation.

    Returns
    -------
    Tessellation
        The triangle geometry of the boolean difference.

    See Also
    --------
    [`boolean_union_mesh_mesh`][compas.geometry.boolean_union_mesh_mesh]
    [`boolean_intersection_mesh_mesh`][compas.geometry.boolean_intersection_mesh_mesh]

    Notes
    -----
    This function requires a Boolean plugin, such as `compas_cgal`.

    """
    raise PluginNotInstalledError("No plugin was found for the boolean_difference_mesh_mesh pluggable. A plugin is available in compas_cgal...")


@tessellation_pluggable(category="booleans", inputs=("A", "B"), result=True)
def boolean_intersection_mesh_mesh(A: "Tessellation", B: "Tessellation") -> "Tessellation":
    """Compute the boolean intersection of two triangle meshes.

    Parameters
    ----------
    A
        The first triangle tessellation.
    B
        The second triangle tessellation.

    Returns
    -------
    Tessellation
        The triangle geometry of the boolean intersection.

    See Also
    --------
    [`boolean_union_mesh_mesh`][compas.geometry.boolean_union_mesh_mesh]
    [`boolean_difference_mesh_mesh`][compas.geometry.boolean_difference_mesh_mesh]

    Notes
    -----
    This function requires a Boolean plugin, such as `compas_cgal`.

    """
    raise PluginNotInstalledError("No plugin was found for the boolean_intersection_mesh_mesh pluggable. A plugin is available in compas_cgal...")


@pluggable(category="booleans")
def boolean_union_polygon_polygon(A: "PlanarRegion | Polygon | CoordinatesType", B: "PlanarRegion | Polygon | CoordinatesType") -> list["PlanarRegion"]:
    """Compute the Boolean union of two planar regions.

    The polygons are assumed to lie in the XY plane. Z coordinates are ignored.

    Parameters
    ----------
    A
        The first polygon, planar region, or exterior coordinate loop.
    B
        The second polygon, planar region, or exterior coordinate loop.

    Returns
    -------
    list[PlanarRegion]
        The connected components of the union. The list is empty if the result
        is empty.

    See Also
    --------
    [`boolean_difference_polygon_polygon`][compas.geometry.boolean_difference_polygon_polygon]
    [`boolean_intersection_polygon_polygon`][compas.geometry.boolean_intersection_polygon_polygon]
    [`boolean_symmetric_difference_polygon_polygon`][compas.geometry.boolean_symmetric_difference_polygon_polygon]

    Notes
    -----
    The default implementation uses `shapely`. A registered plugin may override
    it.

    """
    return _planar_regions(_shapely_polygon(A).union(_shapely_polygon(B)))


@pluggable(category="booleans")
def boolean_difference_polygon_polygon(A: "PlanarRegion | Polygon | CoordinatesType", B: "PlanarRegion | Polygon | CoordinatesType") -> list["PlanarRegion"]:
    """Compute the Boolean difference of two planar regions.

    The polygons are assumed to lie in the XY plane. Z coordinates are ignored.

    Parameters
    ----------
    A
        The first polygon, planar region, or exterior coordinate loop.
    B
        The second polygon, planar region, or exterior coordinate loop.

    Returns
    -------
    list[PlanarRegion]
        The connected components of the difference. Interior rings are
        preserved as holes.

    See Also
    --------
    [`boolean_union_polygon_polygon`][compas.geometry.boolean_union_polygon_polygon]
    [`boolean_intersection_polygon_polygon`][compas.geometry.boolean_intersection_polygon_polygon]
    [`boolean_symmetric_difference_polygon_polygon`][compas.geometry.boolean_symmetric_difference_polygon_polygon]

    Notes
    -----
    The default implementation uses `shapely`. A registered plugin may override
    it.

    """
    return _planar_regions(_shapely_polygon(A).difference(_shapely_polygon(B)))


@pluggable(category="booleans")
def boolean_symmetric_difference_polygon_polygon(A: "PlanarRegion | Polygon | CoordinatesType", B: "PlanarRegion | Polygon | CoordinatesType") -> list["PlanarRegion"]:
    """Compute the Boolean symmetric difference of two planar regions.

    The polygons are assumed to lie in the XY plane. Z coordinates are ignored.

    Parameters
    ----------
    A
        The first polygon, planar region, or exterior coordinate loop.
    B
        The second polygon, planar region, or exterior coordinate loop.

    Returns
    -------
    list[PlanarRegion]
        The connected components of the symmetric difference, including any
        interior holes.

    See Also
    --------
    [`boolean_union_polygon_polygon`][compas.geometry.boolean_union_polygon_polygon]
    [`boolean_intersection_polygon_polygon`][compas.geometry.boolean_intersection_polygon_polygon]
    [`boolean_difference_polygon_polygon`][compas.geometry.boolean_difference_polygon_polygon]

    Notes
    -----
    The default implementation uses `shapely`. A registered plugin may override
    it.

    """
    return _planar_regions(_shapely_polygon(A).symmetric_difference(_shapely_polygon(B)))


@pluggable(category="booleans")
def boolean_intersection_polygon_polygon(A: "PlanarRegion | Polygon | CoordinatesType", B: "PlanarRegion | Polygon | CoordinatesType") -> list["PlanarRegion"]:
    """Compute the Boolean intersection of two planar regions.

    The polygons are assumed to lie in the XY plane. Z coordinates are ignored.

    Parameters
    ----------
    A
        The first polygon, planar region, or exterior coordinate loop.
    B
        The second polygon, planar region, or exterior coordinate loop.

    Returns
    -------
    list[PlanarRegion]
        The connected components of the intersection. The list is empty if
        the regions do not overlap with positive area.

    See Also
    --------
    [`boolean_union_polygon_polygon`][compas.geometry.boolean_union_polygon_polygon]
    [`boolean_difference_polygon_polygon`][compas.geometry.boolean_difference_polygon_polygon]
    [`boolean_symmetric_difference_polygon_polygon`][compas.geometry.boolean_symmetric_difference_polygon_polygon]

    Notes
    -----
    The default implementation uses `shapely`. A registered plugin may override
    it.

    """
    return _planar_regions(_shapely_polygon(A).intersection(_shapely_polygon(B)))
