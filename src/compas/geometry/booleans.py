from math import isfinite
from operator import index as integer_index
from typing import TYPE_CHECKING
from typing import Any

import numpy as np

from compas._typing import CoordinatesType
from compas._typing import TriangleMeshInput
from compas.plugins import pluggable

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


def _validate_boolean_mesh(mesh: TriangleMeshInput, name: str, *, require_closed: bool) -> None:
    """Validate structural and topological Boolean mesh requirements."""
    try:
        vertices, triangles = mesh
    except (TypeError, ValueError):
        raise TypeError(f"{name} should be a (vertices, triangles) pair.")

    vertex_count = len(vertices)
    for vertex in vertices:
        if len(vertex) != 3:
            raise ValueError(f"{name} vertices should have exactly three coordinates.")
        for value in vertex:
            if isinstance(value, (bool, np.bool_)):
                raise TypeError(f"{name} vertex coordinates should be real numbers.")
            try:
                finite = isfinite(value)
            except (TypeError, ValueError):
                raise TypeError(f"{name} vertex coordinates should be real numbers.")
            if not finite:
                raise ValueError(f"{name} vertex coordinates should be finite.")

    incidences: dict[tuple[int, int], list[tuple[int, int]]] = {}
    unique_triangles: set[tuple[int, int, int]] = set()
    for triangle in triangles:
        if len(triangle) != 3:
            raise ValueError(f"{name} faces should have exactly three indices.")
        checked = []
        for value in triangle:
            if isinstance(value, (bool, np.bool_)):
                raise TypeError(f"{name} face indices should be integers.")
            try:
                index = integer_index(value)
            except TypeError:
                raise TypeError(f"{name} face indices should be integers.")
            if index < 0 or index >= vertex_count:
                raise IndexError(f"{name} face index is out of range.")
            checked.append(index)

        a, b, c = checked
        key = tuple(sorted((a, b, c)))
        if key in unique_triangles:
            raise ValueError(f"{name} should not contain duplicate triangles.")
        unique_triangles.add(key)
        for edge in ((a, b), (b, c), (c, a)):
            key = (min(edge), max(edge))
            incidences.setdefault(key, []).append(edge)

    if not require_closed:
        return
    if any(len(edges) > 2 for edges in incidences.values()):
        raise ValueError(f"{name} should be manifold for a Boolean operation.")
    if not incidences or any(len(edges) < 2 for edges in incidences.values()):
        raise ValueError(f"{name} should be closed for a Boolean operation.")
    if any(edges[0] != edges[1][::-1] for edges in incidences.values()):
        raise ValueError(f"{name} should be consistently oriented for a Boolean operation.")


def boolean_union_mesh_mesh(A: TriangleMeshInput, B: TriangleMeshInput) -> TriangleMeshInput:
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
    Inputs must have finite three-dimensional vertices, triangular integral
    connectivity with in-range indices, closed two-manifold edge incidence,
    and consistent orientation. Geometric degeneracy and self-intersection
    remain validity preconditions of the selected backend.

    Examples
    --------
    >>> from compas.geometry import Box, Native, Sphere, UVGrid
    >>> from compas.geometry import boolean_union_mesh_mesh  # doctest: +SKIP
    >>> box = Box.from_width_height_depth(2, 2, 2)
    >>> A = box.tessellate(Native()).to_vertices_and_triangles()

    >>> sphere = Sphere.from_point_and_radius([1, 1, 1], 1)
    >>> B = sphere.tessellate(UVGrid(30, 30)).to_vertices_and_triangles()
    >>> union = boolean_union_mesh_mesh(A, B)  # doctest: +SKIP

    """
    _validate_boolean_mesh(A, "A", require_closed=True)
    _validate_boolean_mesh(B, "B", require_closed=True)
    result = _boolean_union_mesh_mesh(A, B)
    _validate_boolean_mesh(result, "Boolean union result", require_closed=False)
    return result


@pluggable(category="booleans")
def _boolean_union_mesh_mesh(A: TriangleMeshInput, B: TriangleMeshInput) -> TriangleMeshInput:
    raise NotImplementedError


def boolean_difference_mesh_mesh(A: TriangleMeshInput, B: TriangleMeshInput) -> TriangleMeshInput:
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
    Inputs must have finite three-dimensional vertices, triangular integral
    connectivity with in-range indices, closed two-manifold edge incidence,
    and consistent orientation. Geometric degeneracy and self-intersection
    remain validity preconditions of the selected backend.

    """
    _validate_boolean_mesh(A, "A", require_closed=True)
    _validate_boolean_mesh(B, "B", require_closed=True)
    result = _boolean_difference_mesh_mesh(A, B)
    _validate_boolean_mesh(result, "Boolean difference result", require_closed=False)
    return result


@pluggable(category="booleans")
def _boolean_difference_mesh_mesh(A: TriangleMeshInput, B: TriangleMeshInput) -> TriangleMeshInput:
    raise NotImplementedError


def boolean_intersection_mesh_mesh(A: TriangleMeshInput, B: TriangleMeshInput) -> TriangleMeshInput:
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
    Inputs must have finite three-dimensional vertices, triangular integral
    connectivity with in-range indices, closed two-manifold edge incidence,
    and consistent orientation. Geometric degeneracy and self-intersection
    remain validity preconditions of the selected backend.

    """
    _validate_boolean_mesh(A, "A", require_closed=True)
    _validate_boolean_mesh(B, "B", require_closed=True)
    result = _boolean_intersection_mesh_mesh(A, B)
    _validate_boolean_mesh(result, "Boolean intersection result", require_closed=False)
    return result


@pluggable(category="booleans")
def _boolean_intersection_mesh_mesh(A: TriangleMeshInput, B: TriangleMeshInput) -> TriangleMeshInput:
    raise NotImplementedError


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
