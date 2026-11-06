from math import isfinite
from numbers import Integral
from numbers import Real
from typing import TYPE_CHECKING

from compas.plugins import pluggable
from compas.tolerance import TOL
from compas.typing import PointGroupsLike
from compas.typing import PointsLike
from compas.typing import VerticesFaces

if TYPE_CHECKING:
    from compas.geometry import Frame


def _planar_coordinates(
    points: PointsLike,
    frame: "Frame | None",
    name: str,
    minimum: int,
) -> tuple[list[list[float]], list[list[float]]]:
    from compas.geometry import Frame
    from compas.geometry import distance_point_plane

    source = []
    for point in points:
        if len(point) != 3:
            raise ValueError(f"{name} points should have exactly three coordinates.")
        coordinates = [float(value) for value in point]
        if not all(isfinite(value) for value in coordinates):
            raise ValueError(f"{name} points should contain finite coordinates.")
        source.append(coordinates)
    if len(source) < minimum:
        raise ValueError(f"{name} requires at least {minimum} points.")

    plane = Frame.worldXY() if frame is None else frame
    for point in source:
        if not TOL.is_zero(distance_point_plane(point, (plane.point, plane.normal))):
            location = "world XY" if frame is None else "the triangulation frame"
            raise ValueError(f"{name} points should lie on {location} within tolerance.")
    xy = []
    for point in source:
        vector = [point[index] - plane.point[index] for index in range(3)]
        xy.append(
            [
                sum(vector[index] * plane.xaxis[index] for index in range(3)),
                sum(vector[index] * plane.yaxis[index] for index in range(3)),
            ]
        )
    return source, xy


def _coalesce_points(
    points: list[list[float]],
    frame: "Frame | None",
    registry: list[tuple[list[float], list[float]]],
) -> list[list[float]]:
    from compas.geometry import distance_point_point

    _, points_xy = _planar_coordinates(points, frame, "Planar input", 0)
    coalesced = []
    for point, xy in zip(points, points_xy, strict=True):
        for known_xy, known_point in registry:
            planar_distance = ((xy[0] - known_xy[0]) ** 2 + (xy[1] - known_xy[1]) ** 2) ** 0.5
            if TOL.is_zero(planar_distance):
                if not TOL.is_zero(distance_point_point(point, known_point)):
                    raise ValueError("Points at the same planar location should have identical 3D coordinates.")
                coalesced.append(known_point)
                break
        else:
            registry.append((xy, point))
            coalesced.append(point)
    return coalesced


def _validate_domain(
    boundary: list[list[float]],
    holes: list[list[list[float]]],
    constraints: list[list[list[float]]],
    points: list[list[float]],
    frame: "Frame | None",
) -> None:
    from shapely import LineString  # pyright: ignore[reportMissingModuleSource]
    from shapely import Point  # pyright: ignore[reportMissingModuleSource]
    from shapely import Polygon  # pyright: ignore[reportMissingModuleSource]

    from compas.geometry.triangulation_earclip import _validate_boundaries_xy

    boundary_xy = _planar_coordinates(boundary, frame, "Boundary", 3)[1]
    holes_xy = [_planar_coordinates(hole, frame, "Hole", 3)[1] for hole in holes]
    constraints_xy = [_planar_coordinates(constraint, frame, "Constraint", 2)[1] for constraint in constraints]
    points_xy = _planar_coordinates(points, frame, "Interior", 0)[1]
    _validate_boundaries_xy([boundary_xy, *holes_xy])
    domain = Polygon(boundary_xy, holes_xy)

    lines = [LineString(constraint) for constraint in constraints_xy]
    for index, line in enumerate(lines):
        if not line.is_simple:
            raise ValueError(f"Constraint {index + 1} should not self-intersect.")
        if not domain.covers(line):
            raise ValueError(f"Constraint {index + 1} should remain inside the triangulation domain.")
        boundary_intersection = line.intersection(domain.boundary)
        endpoints = [Point(constraints_xy[index][0]), Point(constraints_xy[index][-1])]
        parts = getattr(boundary_intersection, "geoms", None)
        intersections = list(parts) if parts is not None else [boundary_intersection]
        if any(not intersection.is_empty and not any(intersection.equals(endpoint) for endpoint in endpoints) for intersection in intersections):
            raise ValueError(f"Constraint {index + 1} may meet the domain boundary only at an endpoint.")

    for index, line in enumerate(lines):
        endpoints = [Point(constraints_xy[index][0]), Point(constraints_xy[index][-1])]
        for other_index, other in enumerate(lines[index + 1 :], start=index + 1):
            other_endpoints = [Point(constraints_xy[other_index][0]), Point(constraints_xy[other_index][-1])]
            intersection = line.intersection(other)
            if intersection.is_empty:
                continue
            parts = getattr(intersection, "geoms", None)
            intersections = list(parts) if parts is not None else [intersection]
            shared_endpoints = [point for point in endpoints if any(point.equals(other_point) for other_point in other_endpoints)]
            if not shared_endpoints or any(not any(part.equals(endpoint) for endpoint in shared_endpoints) for part in intersections):
                raise ValueError("Constraints may meet only at shared endpoints.")

    for point in points_xy:
        if not domain.contains(Point(point)):
            raise ValueError("Interior points should lie strictly inside the triangulation domain.")


def _validated_result(
    result: VerticesFaces,
    frame: "Frame | None",
    required_vertices: list[list[float]],
    *,
    allow_steiner: bool,
) -> tuple[list[list[float]], list[list[int]]]:
    vertices, triangles = result
    vertex_source, vertex_xy = _planar_coordinates(vertices, frame, "Result", 3)
    triangle_source: list[list[int]] = []
    for triangle in triangles:
        if len(triangle) != 3:
            raise ValueError("Delaunay results should contain only triangles.")
        indices = []
        for index in triangle:
            if not isinstance(index, Integral) or isinstance(index, bool):
                raise TypeError("Triangle indices should be integers.")
            indices.append(int(index))
        if len(set(indices)) != 3 or any(index < 0 or index >= len(vertex_source) for index in indices):
            raise ValueError("Triangle indices should be distinct and in range.")
        a, b, c = [vertex_xy[index] for index in indices]
        signed_area = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
        if TOL.is_zero(signed_area):
            raise ValueError("Delaunay results should not contain degenerate triangles.")
        if signed_area < 0:
            indices[1], indices[2] = indices[2], indices[1]
        triangle_source.append(indices)
    for required in required_vertices:
        if required not in vertex_source:
            raise ValueError("A Delaunay result omitted or changed an accepted source coordinate.")
    if not allow_steiner and (len(vertex_source) != len(required_vertices) or any(vertex not in required_vertices for vertex in vertex_source)):
        raise ValueError("This Delaunay operation should not insert vertices.")
    return vertex_source, triangle_source


def delaunay_triangulation(points: PointsLike, *, frame: "Frame | None" = None) -> VerticesFaces:
    """Construct a planar Delaunay triangulation of points.

    Parameters
    ----------
    points
        Planar XYZ coordinates.
    frame
        The plane in which to interpret the coordinates. If `None`, use world
        XY.

    Returns
    -------
    tuple[PointsLike, IndexGroupsLike]
        Structural vertex and triangle buffers. Repeated source locations are
        coalesced and no vertices are inserted.

    Notes
    -----
    Input coordinates are retained in the structural vertex buffer. Triangles
    are counterclockwise in the supplied frame, or world XY when no frame is
    supplied.

    """
    source, _ = _planar_coordinates(points, frame, "Delaunay input", 3)
    registry: list[tuple[list[float], list[float]]] = []
    source = _coalesce_points(source, frame, registry)
    unique = [point for _, point in registry]
    if len(unique) < 3:
        raise ValueError("Delaunay input requires at least 3 distinct points.")
    return _validated_result(
        _delaunay_triangulation(unique, frame=frame),
        frame,
        unique,
        allow_steiner=False,
    )


@pluggable(category="triangulation")
def _delaunay_triangulation(points: PointsLike, *, frame: "Frame | None" = None) -> VerticesFaces:
    from scipy.spatial import Delaunay as ScipyDelaunay  # pyright: ignore[reportMissingImports]

    vertices, points_xy = _planar_coordinates(points, frame, "Delaunay input", 3)
    triangles = ScipyDelaunay(points_xy).simplices.tolist()
    return vertices, triangles


def constrained_delaunay_triangulation(
    boundary: PointsLike,
    *,
    holes: PointGroupsLike = (),
    constraints: PointGroupsLike = (),
    points: PointsLike = (),
    frame: "Frame | None" = None,
) -> VerticesFaces:
    """Triangulate a constrained planar domain without inserting vertices.

    Parameters
    ----------
    boundary
        The exterior planar boundary.
    holes
        Closed interior boundaries.
    constraints
        Open constrained polylines.
    points
        Additional interior points.
    frame
        The plane in which to interpret the coordinates. If `None`, use world
        XY.

    Returns
    -------
    tuple[PointsLike, IndexGroupsLike]
        Structural vertex and triangle buffers with counterclockwise winding
        in the triangulation frame.

    Notes
    -----
    This operation requires a triangulation plugin. It preserves every
    accepted source coordinate and introduces no Steiner vertices.

    """
    boundary_source, _ = _planar_coordinates(boundary, frame, "Boundary", 3)
    hole_sources = [_planar_coordinates(hole, frame, "Hole", 3)[0] for hole in holes]
    constraint_sources = [_planar_coordinates(constraint, frame, "Constraint", 2)[0] for constraint in constraints]
    point_source, _ = _planar_coordinates(points, frame, "Interior", 0)
    registry: list[tuple[list[float], list[float]]] = []
    boundary_source = _coalesce_points(boundary_source, frame, registry)
    hole_sources = [_coalesce_points(hole, frame, registry) for hole in hole_sources]
    constraint_sources = [_coalesce_points(constraint, frame, registry) for constraint in constraint_sources]
    point_source = _coalesce_points(point_source, frame, registry)
    _validate_domain(boundary_source, hole_sources, constraint_sources, point_source, frame)
    result = _constrained_delaunay_triangulation(
        boundary_source,
        holes=hole_sources,
        constraints=constraint_sources,
        points=point_source,
        frame=frame,
    )
    return _validated_result(result, frame, [point for _, point in registry], allow_steiner=False)


@pluggable(category="triangulation")
def _constrained_delaunay_triangulation(
    boundary: PointsLike,
    *,
    holes: PointGroupsLike = (),
    constraints: PointGroupsLike = (),
    points: PointsLike = (),
    frame: "Frame | None" = None,
) -> VerticesFaces:
    raise NotImplementedError


def conforming_delaunay_triangulation(
    boundary: PointsLike,
    *,
    holes: PointGroupsLike = (),
    constraints: PointGroupsLike = (),
    points: PointsLike = (),
    max_edge_length: float | None = None,
    frame: "Frame | None" = None,
) -> VerticesFaces:
    """Triangulate and optionally refine a constrained planar domain.

    Parameters
    ----------
    boundary
        The exterior planar boundary.
    holes
        Closed interior boundaries.
    constraints
        Open constrained polylines.
    points
        Additional interior points.
    max_edge_length
        A positive finite edge-length refinement target. If `None`, no edge
        length target is requested.
    frame
        The plane in which to interpret the coordinates. If `None`, use world
        XY.

    Returns
    -------
    tuple[PointsLike, IndexGroupsLike]
        Structural vertex and triangle buffers with counterclockwise winding
        in the triangulation frame.

    Notes
    -----
    This operation requires a triangulation plugin. It preserves every
    accepted source coordinate and may insert planar Steiner vertices.

    """
    if max_edge_length is not None:
        if not isinstance(max_edge_length, Real) or isinstance(max_edge_length, bool):
            raise TypeError("max_edge_length should be a real number.")
        max_edge_length = float(max_edge_length)
        if not isfinite(max_edge_length) or max_edge_length <= 0:
            raise ValueError("max_edge_length should be positive and finite.")
    boundary_source, _ = _planar_coordinates(boundary, frame, "Boundary", 3)
    hole_sources = [_planar_coordinates(hole, frame, "Hole", 3)[0] for hole in holes]
    constraint_sources = [_planar_coordinates(constraint, frame, "Constraint", 2)[0] for constraint in constraints]
    point_source, _ = _planar_coordinates(points, frame, "Interior", 0)
    registry: list[tuple[list[float], list[float]]] = []
    boundary_source = _coalesce_points(boundary_source, frame, registry)
    hole_sources = [_coalesce_points(hole, frame, registry) for hole in hole_sources]
    constraint_sources = [_coalesce_points(constraint, frame, registry) for constraint in constraint_sources]
    point_source = _coalesce_points(point_source, frame, registry)
    _validate_domain(boundary_source, hole_sources, constraint_sources, point_source, frame)
    result = _conforming_delaunay_triangulation(
        boundary_source,
        holes=hole_sources,
        constraints=constraint_sources,
        points=point_source,
        max_edge_length=max_edge_length,
        frame=frame,
    )
    return _validated_result(result, frame, [point for _, point in registry], allow_steiner=True)


@pluggable(category="triangulation")
def _conforming_delaunay_triangulation(
    boundary: PointsLike,
    *,
    holes: PointGroupsLike = (),
    constraints: PointGroupsLike = (),
    points: PointsLike = (),
    max_edge_length: float | None = None,
    frame: "Frame | None" = None,
) -> VerticesFaces:
    raise NotImplementedError
