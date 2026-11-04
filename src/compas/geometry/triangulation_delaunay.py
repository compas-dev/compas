from math import isfinite
from typing import TYPE_CHECKING

from compas._typing import CoordinatesCollectionInput
from compas._typing import CoordinatesInput
from compas.plugins import pluggable
from compas.tolerance import TOL

from .triangulation import ConformingDelaunay
from .triangulation import ConstrainedDelaunay
from .triangulation import Delaunay

if TYPE_CHECKING:
    from compas.geometry import Frame
    from compas.geometry import Tessellation


def _planar_coordinates(
    points: CoordinatesInput,
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


def triangulate_planar_points(
    points: CoordinatesInput,
    *,
    strategy: Delaunay,
    frame: "Frame | None" = None,
) -> "Tessellation":
    """Construct a planar Delaunay triangulation of points.

    Parameters
    ----------
    points
        The points to triangulate. Input coordinates are retained exactly.
    strategy
        The Delaunay strategy.
    frame
        The triangulation frame. If `None`, use world XY.

    Returns
    -------
    Tessellation

    Raises
    ------
    TypeError
        If the strategy is not a Delaunay strategy.
    ValueError
        If there are fewer than three points, coordinates are non-finite or
        are not three-dimensional, or an input point lies outside the
        triangulation plane within the standard COMPAS tolerance.

    """
    if not isinstance(strategy, Delaunay):
        raise TypeError("strategy should be a Delaunay strategy.")
    vertices, _ = _planar_coordinates(points, frame, "Delaunay input", 3)
    return _triangulate_planar_points(vertices, strategy=strategy, frame=frame)


@pluggable(category="triangulation")
def _triangulate_planar_points(
    points: CoordinatesInput,
    *,
    strategy: Delaunay,
    frame: "Frame | None" = None,
) -> "Tessellation":
    from scipy.spatial import Delaunay as ScipyDelaunay  # pyright: ignore[reportMissingImports]

    from compas.geometry import Tessellation

    vertices, points_xy = _planar_coordinates(points, frame, "Delaunay input", 3)
    triangles = ScipyDelaunay(points_xy).simplices.tolist()
    return Tessellation(vertices, triangles)


def triangulate_planar_domain(
    boundary: CoordinatesInput,
    *,
    holes: CoordinatesCollectionInput = (),
    constraints: CoordinatesCollectionInput = (),
    points: CoordinatesInput = (),
    strategy: ConstrainedDelaunay | ConformingDelaunay,
    frame: "Frame | None" = None,
) -> "Tessellation":
    """Triangulate a planar domain with optional holes and constraints.

    Parameters
    ----------
    boundary
        The exterior domain boundary.
    holes
        Closed interior hole boundaries.
    constraints
        Open constrained polylines.
    points
        Optional unconstrained interior points.
    strategy
        A constrained or conforming Delaunay strategy.
    frame
        The triangulation frame. If `None`, use world XY.

    Returns
    -------
    Tessellation

    Raises
    ------
    TypeError
        If the strategy is not a constrained or conforming Delaunay strategy.
    ValueError
        If coordinates are non-finite, are not three-dimensional, lie outside
        the triangulation plane, or a boundary, hole, or constraint has too few
        points.

    Notes
    -----
    This extension point has no core implementation and requires a plugin.

    """
    if not isinstance(strategy, (ConstrainedDelaunay, ConformingDelaunay)):
        raise TypeError("strategy should be a ConstrainedDelaunay or ConformingDelaunay strategy.")

    boundary_source, _ = _planar_coordinates(boundary, frame, "Boundary", 3)
    hole_sources = [_planar_coordinates(hole, frame, "Hole", 3)[0] for hole in holes]
    constraint_sources = [_planar_coordinates(constraint, frame, "Constraint", 2)[0] for constraint in constraints]
    point_source, _ = _planar_coordinates(points, frame, "Interior", 0)
    return _triangulate_planar_domain(
        boundary_source,
        holes=hole_sources,
        constraints=constraint_sources,
        points=point_source,
        strategy=strategy,
        frame=frame,
    )


@pluggable(category="triangulation")
def _triangulate_planar_domain(
    boundary: CoordinatesInput,
    *,
    holes: CoordinatesCollectionInput = (),
    constraints: CoordinatesCollectionInput = (),
    points: CoordinatesInput = (),
    strategy: ConstrainedDelaunay | ConformingDelaunay,
    frame: "Frame | None" = None,
) -> "Tessellation":
    raise NotImplementedError
