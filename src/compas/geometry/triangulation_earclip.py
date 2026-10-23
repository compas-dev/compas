from collections.abc import Sequence
from typing import TYPE_CHECKING

import mapbox_earcut  # pyright: ignore[reportMissingImports]
import numpy as np  # pyright: ignore[reportMissingImports]

from compas._typing import CoordinateType
from compas.linalg import cross_vectors
from compas.linalg import length_vector
from compas.linalg import subtract_vectors

if TYPE_CHECKING:
    from compas.geometry import Frame
    from compas.geometry import Polygon


def _signed_area_xy(points: Sequence[CoordinateType]) -> float:
    return 0.5 * sum(points[index][0] * points[(index + 1) % len(points)][1] - points[(index + 1) % len(points)][0] * points[index][1] for index in range(len(points)))


def _validate_boundaries_xy(boundaries: Sequence[Sequence[CoordinateType]]) -> None:
    from shapely import LinearRing  # pyright: ignore[reportMissingModuleSource]
    from shapely import Polygon as ShapelyPolygon  # pyright: ignore[reportMissingModuleSource]
    from shapely.validation import explain_validity  # pyright: ignore[reportMissingModuleSource]

    polygons = []
    for index, boundary in enumerate(boundaries):
        label = "exterior boundary" if index == 0 else f"hole {index}"
        points = [(point[0], point[1]) for point in boundary]
        if len(set(points)) != len(points):
            raise ValueError(f"The planar region's {label} contains duplicate vertices.")

        ring = LinearRing(points)
        if not ring.is_simple:
            raise ValueError(f"The planar region's {label} is self-intersecting.")

        polygon = ShapelyPolygon(points)
        if polygon.area == 0.0 or not polygon.is_valid:
            reason = explain_validity(polygon)
            raise ValueError(f"The planar region's {label} is invalid: {reason}.")
        polygons.append(polygon)

    outer = polygons[0]
    holes = polygons[1:]
    for index, hole in enumerate(holes, start=1):
        if not outer.contains(hole) or not outer.boundary.disjoint(hole):
            raise ValueError(f"Hole {index} must lie strictly inside the planar region's exterior boundary.")

    for index, hole in enumerate(holes):
        for other_index, other in enumerate(holes[index + 1 :], start=index + 1):
            if not hole.disjoint(other):
                raise ValueError(f"Holes {index + 1} and {other_index + 1} must not overlap, touch, or contain one another.")


def _projection_frame(boundary: "Polygon") -> "Frame":
    from compas.geometry import Frame

    point = boundary.points[0]
    for point_xaxis in boundary.points[1:]:
        xaxis = subtract_vectors(point_xaxis, point)
        if not length_vector(xaxis):
            continue
        for point_xyplane in boundary.points[1:]:
            xyvector = subtract_vectors(point_xyplane, point)
            if length_vector(cross_vectors(xaxis, xyvector)):
                return Frame.from_points(point, point_xaxis, point_xyplane)
    raise ValueError("The planar region's exterior boundary is degenerate.")


def _earclip_boundaries(outer: "Polygon", holes: Sequence["Polygon"] = ()) -> tuple[list[list[float]], list[list[int]]]:
    """Triangulate coplanar polygon boundaries with Mapbox Earcut.

    The returned vertex list contains the exterior vertices followed by the
    vertices of each hole. Triangle indices refer to this flattened list.

    """
    from compas.geometry import Frame
    from compas.geometry import Transformation

    boundaries = [outer, *holes]
    vertices = [[float(value) for value in point] for boundary in boundaries for point in boundary.points]
    transformation = Transformation.from_frame_to_frame(_projection_frame(outer), Frame.worldXY())
    points = [point.transformed(transformation) for boundary in boundaries for point in boundary.points]
    boundaries_xy: list[Sequence[CoordinateType]] = []
    start = 0
    for boundary in boundaries:
        end = start + len(boundary)
        boundaries_xy.append(points[start:end])
        start = end
    _validate_boundaries_xy(boundaries_xy)

    vertices_xy = np.asarray([[point.x, point.y] for point in points], dtype=np.float64)
    ring_ends = np.cumsum([len(boundary) for boundary in boundaries], dtype=np.uint32)
    indices = mapbox_earcut.triangulate_float64(vertices_xy, ring_ends).tolist()
    triangles = [indices[index : index + 3] for index in range(0, len(indices), 3)]

    # Earcut has its own winding convention. Restore the exterior boundary's
    # winding so face triangulation preserves the orientation of its source.
    outer_xy = points[: len(outer)]
    outer_sign = _signed_area_xy(outer_xy)
    for triangle in triangles:
        triangle_sign = _signed_area_xy([points[index] for index in triangle])
        if outer_sign * triangle_sign < 0.0:
            triangle[1], triangle[2] = triangle[2], triangle[1]

    return vertices, triangles


def earclip_polygon(polygon: "Polygon") -> list[list[int]]:
    """Triangulate a simple planar polygon using Mapbox Earcut.

    Parameters
    ----------
    polygon
        A non-self-intersecting polygon. Non-planar polygons are projected to
        their best-fit plane before triangulation.

    Returns
    -------
    list[list[int]]
        The triangles as indices into the polygon points.

    Raises
    ------
    ValueError
        If the polygon has fewer than three points or its boundary is invalid.

    See Also
    --------
    [`PlanarRegion`][compas.geometry.PlanarRegion] for triangulating an exterior
    boundary with holes.

    """
    if len(polygon) < 3:
        raise ValueError("A polygon requires at least three points for triangulation.")
    _, triangles = _earclip_boundaries(polygon)
    return triangles
