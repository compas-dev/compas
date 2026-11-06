from collections.abc import Callable
from collections.abc import Iterable
from math import isfinite
from numbers import Real
from operator import index as integer_index
from typing import Literal
from typing import SupportsIndex
from typing import TypeAlias

from compas.tolerance import TOL
from compas.typing import PointsLike

__all__ = [
    "Triangulator",
    "triangulate_polygon",
    "triangulate_polygon_earclip",
    "triangulate_polygon_minimum_area",
    "triangulate_polygon_projected",
    "triangulate_quadrilateral",
]

Triangulator: TypeAlias = Callable[[PointsLike], Iterable[Iterable[SupportsIndex]]]


def _validate_triangulation(
    triangles: Iterable[Iterable[SupportsIndex]],
    vertices: PointsLike,
) -> list[list[int]]:
    """Validate and normalize a complete local triangulation."""
    vertex_count = len(vertices)
    validated: list[list[int]] = []
    for triangle in triangles:
        indices = list(triangle)
        if len(indices) != 3:
            raise ValueError("A triangulator should return triangles with exactly three indices.")
        try:
            normalized = [integer_index(index) for index in indices]
        except TypeError:
            raise TypeError("Triangulation indices should support integer indexing.") from None
        if len(set(normalized)) != 3:
            raise ValueError("A triangulator should return three distinct indices per triangle.")
        if any(index < 0 or index >= vertex_count for index in normalized):
            raise ValueError("Triangulation indices should refer to vertices of the input polygon.")
        validated.append(normalized)

    if len(validated) != vertex_count - 2:
        raise ValueError("A triangulator should return exactly n - 2 triangles for n polygon vertices.")

    from compas.geometry import area_triangle

    for triangle in validated:
        if TOL.is_zero(area_triangle([vertices[index] for index in triangle])):
            raise ValueError("A triangulator should not return degenerate triangles.")

    boundary_edges = {frozenset((index, (index + 1) % vertex_count)): (index, (index + 1) % vertex_count) for index in range(vertex_count)}
    edge_directions: dict[frozenset[int], list[tuple[int, int]]] = {}
    for a, b, c in validated:
        for edge in ((a, b), (b, c), (c, a)):
            edge_directions.setdefault(frozenset(edge), []).append(edge)

    for edge, directions in edge_directions.items():
        boundary = boundary_edges.get(edge)
        if boundary is not None:
            if directions != [boundary]:
                raise ValueError("A triangulator should preserve every directed polygon boundary edge exactly once.")
            continue
        if len(directions) != 2 or directions[0] != directions[1][::-1]:
            raise ValueError("A triangulator should use every interior edge exactly twice in opposite directions.")

    if any(edge not in edge_directions for edge in boundary_edges):
        raise ValueError("A triangulator should preserve every directed polygon boundary edge exactly once.")
    return validated


def _positive_finite(value: float, name: str) -> float:
    if not isinstance(value, Real) or isinstance(value, bool):
        raise TypeError(f"{name} should be a real number.")
    value = float(value)
    if not isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} should be positive and finite.")
    return value


def _validate_finite_polygon(vertices: PointsLike) -> None:
    for vertex in vertices:
        if len(vertex) != 3 or any(not isfinite(vertex[axis]) for axis in range(3)):
            raise ValueError("Polygon vertices should have exactly three finite coordinates.")


def _validate_polygon_boundary(vertices: PointsLike) -> None:
    from compas.geometry import distance_point_point
    from compas.geometry import intersection_segment_segment
    from compas.geometry import is_point_on_segment

    for index, vertex in enumerate(vertices):
        if TOL.is_zero(distance_point_point(vertex, vertices[(index + 1) % len(vertices)])):
            raise ValueError("A polygon should not contain zero-length boundary edges.")
    for index, vertex in enumerate(vertices):
        for other_index in range(index + 1, len(vertices)):
            other = vertices[other_index]
            if TOL.is_zero(distance_point_point(vertex, other)):
                raise ValueError("A polygon should not contain repeated vertices.")
    count = len(vertices)
    for index in range(count):
        segment = (vertices[index], vertices[(index + 1) % count])
        for other_index in range(index + 1, count):
            if other_index == index + 1 or (index == 0 and other_index == count - 1):
                continue
            other = (vertices[other_index], vertices[(other_index + 1) % count])
            if (
                intersection_segment_segment(segment, other)
                or is_point_on_segment(segment[0], other)
                or is_point_on_segment(segment[1], other)
                or is_point_on_segment(other[0], segment)
                or is_point_on_segment(other[1], segment)
            ):
                raise ValueError("A polygon boundary should not self-intersect.")


def _minimum_area_triangulation(vertices: PointsLike) -> list[list[int]]:
    from compas.geometry import area_triangle

    _validate_polygon_boundary(vertices)
    count = len(vertices)
    costs = [[float("inf")] * count for _ in range(count)]
    splits: list[list[int | None]] = [[None] * count for _ in range(count)]
    for index in range(count):
        costs[index][index] = 0.0
        if index + 1 < count:
            costs[index][index + 1] = 0.0

    for span in range(2, count):
        for start in range(count - span):
            end = start + span
            best_cost = float("inf")
            best_split = None
            for split in range(start + 1, end):
                area = area_triangle([vertices[start], vertices[split], vertices[end]])
                if TOL.is_zero(area):
                    continue
                if not isfinite(costs[start][split]) or not isfinite(costs[split][end]):
                    continue
                cost = costs[start][split] + costs[split][end] + area
                if cost < best_cost:
                    best_cost = cost
                    best_split = split
            if best_split is not None:
                costs[start][end] = best_cost
                splits[start][end] = best_split

    if splits[0][count - 1] is None:
        raise ValueError("The polygon has no nondegenerate minimum-area triangulation.")

    triangles: list[list[int]] = []

    def collect(start: int, end: int) -> None:
        if end - start < 2:
            return
        split = splits[start][end]
        if split is None:
            raise ValueError("The polygon has no nondegenerate minimum-area triangulation.")
        triangles.append([start, split, end])
        collect(start, split)
        collect(split, end)

    collect(0, count - 1)
    return triangles


def _projected_ear_clipping(vertices: PointsLike, max_deviation: float) -> list[list[int]]:
    from compas.geometry import Frame
    from compas.geometry import Plane
    from compas.geometry import Polygon
    from compas.geometry import Transformation
    from compas.geometry import bestfit_plane
    from compas.geometry import distance_point_plane
    from compas.geometry import earclip_polygon
    from compas.geometry import transform_points

    _validate_polygon_boundary(vertices)
    origin, normal = bestfit_plane(vertices)
    plane = Plane(origin.tolist(), normal.tolist())
    deviation = max(distance_point_plane(vertex, plane) for vertex in vertices)
    if deviation > max_deviation and not TOL.is_close(deviation, max_deviation, rtol=0.0):
        raise ValueError(f"The polygon deviates from its best-fit plane by {deviation}, exceeding max_deviation={max_deviation}.")
    transformation = Transformation.from_frame_to_frame(Frame.from_plane(plane), Frame.worldXY())
    projected = transform_points(vertices, transformation)
    for point in projected:
        point[2] = 0.0
    return earclip_polygon(Polygon(projected))


def triangulate_quadrilateral(
    vertices: PointsLike,
    *,
    diagonal: Literal["shortest", "02", "13"] = "shortest",
) -> list[list[int]]:
    """Triangulate a quadrilateral without inserting vertices.

    Parameters
    ----------
    vertices
        Four ordered XYZ coordinates.
    diagonal
        The diagonal selection. `"02"` connects vertices 0 and 2, `"13"`
        connects vertices 1 and 3, and `"shortest"` selects the shortest valid
        interior diagonal for a planar quadrilateral.

    Returns
    -------
    list[list[int]]
        Two triangles indexing the input vertices.

    Raises
    ------
    ValueError
        If the boundary is invalid, the selected diagonal produces a
        degenerate triangle, or an explicitly selected diagonal lies outside
        a planar concave quadrilateral.

    """
    source = [[float(value) for value in vertex] for vertex in vertices]
    if len(source) != 4:
        raise ValueError("A quadrilateral requires exactly four vertices.")
    if diagonal not in {"shortest", "02", "13"}:
        raise ValueError('diagonal should be "shortest", "02", or "13".')
    _validate_finite_polygon(source)
    _validate_polygon_boundary(source)
    candidates: dict[Literal["02", "13"], list[list[int]]] = {
        "02": [[0, 1, 2], [0, 2, 3]],
        "13": [[0, 1, 3], [1, 2, 3]],
    }
    diagonal_vertices: dict[Literal["02", "13"], tuple[int, int]] = {"02": (0, 2), "13": (1, 3)}
    from compas.geometry import area_polygon
    from compas.geometry import area_triangle
    from compas.geometry import is_coplanar

    polygon_area = area_polygon(source)
    planar = is_coplanar(source)

    def is_valid(candidate: list[list[int]]) -> bool:
        areas = [area_triangle([source[index] for index in triangle]) for triangle in candidate]
        if any(TOL.is_zero(area) for area in areas):
            return False
        return not planar or bool(TOL.is_close(sum(areas), polygon_area))

    if diagonal == "shortest":
        valid_diagonals: list[Literal["02", "13"]] = [candidate for candidate, triangles in candidates.items() if is_valid(triangles)]
        if not valid_diagonals:
            raise ValueError("The quadrilateral has no valid nondegenerate triangulation.")

        def diagonal_length_squared(candidate: Literal["02", "13"]) -> float:
            start, end = diagonal_vertices[candidate]
            return sum((source[start][axis] - source[end][axis]) ** 2 for axis in range(3))

        selected_diagonal = min(
            valid_diagonals,
            key=diagonal_length_squared,
        )
    else:
        selected_diagonal = diagonal

    triangles = candidates[selected_diagonal]

    if any(TOL.is_zero(area_triangle([source[index] for index in triangle])) for triangle in triangles):
        raise ValueError("The quadrilateral triangulation contains a degenerate triangle.")
    if planar and not is_valid(triangles):
        raise ValueError("The selected diagonal lies outside the planar quadrilateral.")
    return triangles


def triangulate_polygon_earclip(vertices: PointsLike) -> list[list[int]]:
    """Triangulate an ordered planar polygon by ear clipping.

    Parameters
    ----------
    vertices
        Ordered planar XYZ coordinates.

    Returns
    -------
    list[list[int]]
        Triangle indices into `vertices`.

    """
    source = [[float(value) for value in vertex] for vertex in vertices]
    if len(source) < 3:
        raise ValueError("A polygon requires at least three vertices for triangulation.")
    _validate_finite_polygon(source)
    _validate_polygon_boundary(source)
    from compas.geometry import Polygon
    from compas.geometry import earclip_polygon
    from compas.geometry import is_coplanar

    if not is_coplanar(source):
        raise ValueError("Ear clipping requires a planar polygon.")
    return earclip_polygon(Polygon(source))


def triangulate_polygon_projected(vertices: PointsLike, *, max_deviation: float) -> list[list[int]]:
    """Triangulate a near-planar polygon through its best-fit plane.

    Parameters
    ----------
    vertices
        Ordered XYZ coordinates.
    max_deviation
        Positive finite maximum distance from the best-fit plane.

    Returns
    -------
    list[list[int]]
        Triangle indices into `vertices`.

    """
    checked_deviation = _positive_finite(max_deviation, "max_deviation")
    source = [[float(value) for value in vertex] for vertex in vertices]
    if len(source) < 3:
        raise ValueError("A polygon requires at least three vertices for triangulation.")
    _validate_finite_polygon(source)
    return _projected_ear_clipping(source, checked_deviation)


def triangulate_polygon_minimum_area(vertices: PointsLike) -> list[list[int]]:
    """Triangulate an ordered 3D polygon with minimum total triangle area.

    Parameters
    ----------
    vertices
        Ordered XYZ coordinates.

    Returns
    -------
    list[list[int]]
        Triangle indices into `vertices`.

    Notes
    -----
    The dynamic program takes $O(n^3)$ time and $O(n^2)$ space. It performs
    no projection and inserts no vertices.

    References
    ----------
    Barequet, G. and Sharir, M. *Filling gaps in the boundary of a polyhedron*.
    Computer Aided Geometric Design 12(2), 1995.
    <https://doi.org/10.1016/0167-8396(94)00011-G>

    """
    source = [[float(value) for value in vertex] for vertex in vertices]
    if len(source) < 3:
        raise ValueError("A polygon requires at least three vertices for triangulation.")
    _validate_finite_polygon(source)
    return _minimum_area_triangulation(source)


def triangulate_polygon(vertices: PointsLike) -> list[list[int]]:
    """Triangulate one polygon represented by ordered vertex coordinates.

    Parameters
    ----------
    vertices
        The ordered polygon vertex coordinates.

    Returns
    -------
    list[list[int]]
        Triangle indices into `vertices`.

    """
    count = len(vertices)
    if count < 3:
        raise ValueError("A polygon requires at least three vertices for triangulation.")
    source = [[float(value) for value in vertex] for vertex in vertices]
    _validate_finite_polygon(source)
    if count == 3:
        _validate_polygon_boundary(source)
        from compas.geometry import area_triangle

        if TOL.is_zero(area_triangle(source)):
            raise ValueError("The polygon triangle is degenerate.")
        return [[0, 1, 2]]
    if count == 4:
        return triangulate_quadrilateral(source)
    return triangulate_polygon_earclip(source)
