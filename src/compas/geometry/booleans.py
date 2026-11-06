from typing import TYPE_CHECKING
from typing import Any

from compas.plugins import pluggable
from compas.typing import PointsLike
from compas.typing import VerticesFaces

if TYPE_CHECKING:
    from .planar_region import PlanarRegion
    from .polygon import Polygon


def _xy_coordinates(points: Any) -> list[list[float]]:
    return [[point[0], point[1]] for point in points]


def _shapely_polygon(region: "PlanarRegion | Polygon | PointsLike") -> Any:
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


def boolean_union_mesh_mesh(A: VerticesFaces, B: VerticesFaces) -> VerticesFaces:
    """Compute the boolean union of two triangle meshes.

    Parameters
    ----------
    A
        The first triangle mesh as vertices and triangles.
    B
        The second triangle mesh as vertices and triangles.

    Returns
    -------
    tuple
        The vertices and triangles of the Boolean union.

    See Also
    --------
    [`boolean_difference_mesh_mesh`][compas.geometry.boolean_difference_mesh_mesh]
    [`boolean_intersection_mesh_mesh`][compas.geometry.boolean_intersection_mesh_mesh]

    Notes
    -----
    This function requires a Boolean plugin, such as `compas_cgal`.
    Input validity is a precondition of the selected backend. Core dispatches
    the structural buffers without converting or pre-validating them.

    Examples
    --------
    >>> from compas.geometry import Box, Sphere
    >>> from compas.geometry import boolean_union_mesh_mesh  # doctest: +SKIP
    >>> box = Box.from_width_height_depth(2, 2, 2)
    >>> A = box.to_tessellation().to_vertices_and_triangles()

    >>> sphere = Sphere.from_point_and_radius([1, 1, 1], 1)
    >>> B = sphere.to_tessellation(nu=30, nv=30).to_vertices_and_triangles()
    >>> union = boolean_union_mesh_mesh(A, B)  # doctest: +SKIP

    """
    return _boolean_union_mesh_mesh(A, B)


@pluggable(category="booleans")
def _boolean_union_mesh_mesh(A: VerticesFaces, B: VerticesFaces) -> VerticesFaces:
    raise NotImplementedError


def boolean_difference_mesh_mesh(A: VerticesFaces, B: VerticesFaces) -> VerticesFaces:
    """Compute the boolean difference of two triangle meshes.

    Parameters
    ----------
    A
        The first triangle mesh as vertices and triangles.
    B
        The second triangle mesh as vertices and triangles.

    Returns
    -------
    tuple
        The vertices and triangles of the Boolean difference.

    See Also
    --------
    [`boolean_union_mesh_mesh`][compas.geometry.boolean_union_mesh_mesh]
    [`boolean_intersection_mesh_mesh`][compas.geometry.boolean_intersection_mesh_mesh]

    Notes
    -----
    This function requires a Boolean plugin, such as `compas_cgal`.
    Input validity is a precondition of the selected backend. Core dispatches
    the structural buffers without converting or pre-validating them.

    """
    return _boolean_difference_mesh_mesh(A, B)


@pluggable(category="booleans")
def _boolean_difference_mesh_mesh(A: VerticesFaces, B: VerticesFaces) -> VerticesFaces:
    raise NotImplementedError


def boolean_intersection_mesh_mesh(A: VerticesFaces, B: VerticesFaces) -> VerticesFaces:
    """Compute the boolean intersection of two triangle meshes.

    Parameters
    ----------
    A
        The first triangle mesh as vertices and triangles.
    B
        The second triangle mesh as vertices and triangles.

    Returns
    -------
    tuple
        The vertices and triangles of the Boolean intersection.

    See Also
    --------
    [`boolean_union_mesh_mesh`][compas.geometry.boolean_union_mesh_mesh]
    [`boolean_difference_mesh_mesh`][compas.geometry.boolean_difference_mesh_mesh]

    Notes
    -----
    This function requires a Boolean plugin, such as `compas_cgal`.
    Input validity is a precondition of the selected backend. Core dispatches
    the structural buffers without converting or pre-validating them.

    """
    return _boolean_intersection_mesh_mesh(A, B)


@pluggable(category="booleans")
def _boolean_intersection_mesh_mesh(A: VerticesFaces, B: VerticesFaces) -> VerticesFaces:
    raise NotImplementedError


@pluggable(category="booleans")
def boolean_union_polygon_polygon(A: "PlanarRegion | Polygon | PointsLike", B: "PlanarRegion | Polygon | PointsLike") -> list["PlanarRegion"]:
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
def boolean_difference_polygon_polygon(A: "PlanarRegion | Polygon | PointsLike", B: "PlanarRegion | Polygon | PointsLike") -> list["PlanarRegion"]:
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
def boolean_symmetric_difference_polygon_polygon(A: "PlanarRegion | Polygon | PointsLike", B: "PlanarRegion | Polygon | PointsLike") -> list["PlanarRegion"]:
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
def boolean_intersection_polygon_polygon(A: "PlanarRegion | Polygon | PointsLike", B: "PlanarRegion | Polygon | PointsLike") -> list["PlanarRegion"]:
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
