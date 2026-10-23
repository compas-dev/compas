from collections.abc import Sequence
from math import fabs
from math import sqrt
from typing import Literal

from compas._typing import CoordinatesType
from compas._typing import CoordinateType
from compas._typing import SphereType
from compas.linalg.vectors import add_vectors
from compas.linalg.vectors import cross_vectors
from compas.linalg.vectors import dot_vectors
from compas.linalg.vectors import length_vector
from compas.linalg.vectors import length_vector_xy
from compas.linalg.vectors import normalize_vector
from compas.linalg.vectors import scale_vector
from compas.linalg.vectors import subtract_vectors
from compas.linalg.vectors import subtract_vectors_xy
from compas.tolerance import TOL

from .distance import distance_point_point
from .predicates_3 import is_point_in_triangle

__all__ = [
    "closest_points_line_line",
    "intersection_line_plane",
    "intersection_line_line_xy",
    "intersection_line_triangle",
    "intersection_circle_circle_xy",
    "intersection_ellipse_line_xy",
    "intersection_plane_circle",
    "intersection_plane_plane",
    "intersection_segment_plane",
    "intersection_sphere_line",
    "intersection_sphere_sphere",
]

PointCoordinates = tuple[float, float, float]
SphereSphereIntersection = (
    tuple[Literal["point"], list[float]] | tuple[Literal["circle"], tuple[list[float], float, list[float]]] | tuple[Literal["sphere"], tuple[list[float], float]]
)
CircleCircleXYIntersection = (
    tuple[Literal["point"], PointCoordinates]
    | tuple[Literal["points"], tuple[PointCoordinates, PointCoordinates]]
    | tuple[Literal["circle"], tuple[PointCoordinates, float, PointCoordinates]]
)


def closest_points_line_line(
    line1: Sequence[CoordinateType],
    line2: Sequence[CoordinateType],
    tol: float | None = None,
) -> tuple[list[float] | None, list[float] | None]:
    a, b = line1
    c, d = line2
    ab = subtract_vectors(b, a)
    cd = subtract_vectors(d, c)
    normal = cross_vectors(ab, cd)

    if TOL.is_zero(length_vector(normal), tol):
        return None, None

    normal1 = normalize_vector(cross_vectors(ab, normal))
    normal2 = normalize_vector(cross_vectors(cd, normal))
    point1 = intersection_line_plane((a, b), (c, normal2), tol=tol)
    point2 = intersection_line_plane((c, d), (a, normal1), tol=tol)
    return point1, point2


def intersection_line_plane(
    line: Sequence[CoordinateType],
    plane: Sequence[CoordinateType],
    tol: float | None = None,
) -> list[float] | None:
    a, b = line
    o, n = plane
    ab = subtract_vectors(b, a)
    cosa = dot_vectors(n, ab)

    if TOL.is_zero(cosa, tol):
        return None

    oa = subtract_vectors(a, o)
    ratio = -dot_vectors(n, oa) / cosa
    return add_vectors(a, scale_vector(ab, ratio))


def intersection_line_line_xy(
    line1: CoordinatesType,
    line2: CoordinatesType,
    tol: float | None = None,
) -> PointCoordinates | None:
    a, b = line1
    c, d = line2
    x1, y1 = a[0], a[1]
    x2, y2 = b[0], b[1]
    x3, y3 = c[0], c[1]
    x4, y4 = d[0], d[1]

    denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if TOL.is_zero(denominator, tol):
        return None

    determinant1 = x1 * y2 - y1 * x2
    determinant2 = x3 * y4 - y3 * x4
    x = (determinant1 * (x3 - x4) - (x1 - x2) * determinant2) / denominator
    y = (determinant1 * (y3 - y4) - (y1 - y2) * determinant2) / denominator
    return x, y, 0.0


def intersection_circle_circle_xy(
    circle1: tuple[CoordinatesType, float],
    circle2: tuple[CoordinatesType, float],
    tol: float | None = None,
) -> CircleCircleXYIntersection | None:
    plane1, radius1 = circle1
    plane2, radius2 = circle2
    center1, normal1 = plane1
    center2, _ = plane2

    if radius1 <= 0.0 or radius2 <= 0.0:
        raise ValueError("Circle radii must be positive.")

    distance = length_vector_xy(subtract_vectors_xy(center2, center1))
    if TOL.is_zero(distance, tol):
        if not TOL.is_close(radius1, radius2, atol=tol):
            return None
        center = center1[0], center1[1], center1[2] if len(center1) > 2 else 0.0
        normal = normal1[0], normal1[1], normal1[2]
        return "circle", (center, radius1, normal)
    if distance > radius1 + radius2 and not TOL.is_close(distance, radius1 + radius2, atol=tol):
        return None
    if distance < fabs(radius1 - radius2) and not TOL.is_close(distance, fabs(radius1 - radius2), atol=tol):
        return None

    x1, y1 = center1[0], center1[1]
    x2, y2 = center2[0], center2[1]
    midpoint_x = 0.5 * (x1 + x2)
    midpoint_y = 0.5 * (y2 + y1)
    distance2 = distance * distance
    factor = (radius1 * radius1 - radius2 * radius2) / (2 * distance2)
    discriminant = 2 * (radius1 * radius1 + radius2 * radius2) / distance2 - (radius1 * radius1 - radius2 * radius2) ** 2 / (distance2 * distance2) - 1
    offset = 0.5 * sqrt(max(0.0, discriminant))
    point1 = (
        midpoint_x + factor * (x2 - x1) + offset * (y2 - y1),
        midpoint_y + factor * (y2 - y1) + offset * (x1 - x2),
        0.0,
    )
    if TOL.is_zero(discriminant, tol):
        return "point", point1
    point2 = (
        midpoint_x + factor * (x2 - x1) - offset * (y2 - y1),
        midpoint_y + factor * (y2 - y1) - offset * (x1 - x2),
        0.0,
    )
    return "points", (point1, point2)


def intersection_ellipse_line_xy(
    ellipse: tuple[float, float],
    line: CoordinatesType,
    tol: float | None = None,
) -> PointCoordinates | tuple[PointCoordinates, PointCoordinates] | None:
    x1, y1 = line[0][0], line[0][1]
    x2, y2 = line[1][0], line[1][1]
    major, minor = ellipse

    if major <= 0.0 or minor <= 0.0:
        raise ValueError("Ellipse semi-axis lengths must be positive.")

    quadratic = (x2 - x1) ** 2 / major**2 + (y2 - y1) ** 2 / minor**2
    if TOL.is_zero(quadratic, tol):
        raise ValueError("A line requires two distinct points.")
    linear = 2 * x1 * (x2 - x1) / major**2 + 2 * y1 * (y2 - y1) / minor**2
    constant = x1**2 / major**2 + y1**2 / minor**2 - 1
    discriminant = linear**2 - 4 * quadratic * constant

    if TOL.is_zero(discriminant, tol):
        parameter = -linear / (2 * quadratic)
        return x1 + (x2 - x1) * parameter, y1 + (y2 - y1) * parameter, 0.0
    if discriminant < 0:
        return None

    root = sqrt(discriminant)
    parameter1 = (-linear + root) / (2 * quadratic)
    parameter2 = (-linear - root) / (2 * quadratic)
    point1 = x1 + (x2 - x1) * parameter1, y1 + (y2 - y1) * parameter1, 0.0
    point2 = x1 + (x2 - x1) * parameter2, y1 + (y2 - y1) * parameter2, 0.0
    return point1, point2


def intersection_plane_plane(
    plane1: Sequence[CoordinateType],
    plane2: Sequence[CoordinateType],
    tol: float | None = None,
) -> tuple[list[float], list[float]] | None:
    o1, n1 = plane1
    o2, n2 = plane2
    direction = cross_vectors(n1, n2)
    if TOL.is_zero(length_vector(direction), tol):
        return None

    perpendicular = cross_vectors(direction, n1)
    point = add_vectors(o1, perpendicular)
    intersection = intersection_line_plane((o1, point), (o2, n2), tol=tol)
    if intersection is None:
        return None
    return intersection, add_vectors(intersection, direction)


def intersection_sphere_sphere(
    sphere1: SphereType,
    sphere2: SphereType,
    tol: float | None = None,
) -> SphereSphereIntersection | None:
    center1, radius1 = sphere1
    center2, radius2 = sphere2

    if radius1 < 0.0 or radius2 < 0.0:
        raise ValueError("Sphere radii cannot be negative.")

    distance = distance_point_point(center1, center2)
    if distance > radius1 + radius2 and not TOL.is_close(distance, radius1 + radius2, atol=tol):
        return None
    if distance + min(radius1, radius2) < max(radius1, radius2) and not TOL.is_close(distance + min(radius1, radius2), max(radius1, radius2), atol=tol):
        return None
    if TOL.is_zero(distance, tol) and TOL.is_close(radius1, radius2, atol=tol):
        return "sphere", ([center1[0], center1[1], center1[2]], float(radius1))
    if TOL.is_close(radius1 + radius2, distance, atol=tol):
        point = add_vectors(center1, scale_vector(subtract_vectors(center2, center1), radius1 / distance))
        return "point", point
    if TOL.is_close(distance + min(radius1, radius2), max(radius1, radius2), atol=tol):
        if radius1 > radius2:
            point = add_vectors(center1, scale_vector(subtract_vectors(center2, center1), radius1 / distance))
        else:
            point = add_vectors(center2, scale_vector(subtract_vectors(center1, center2), radius2 / distance))
        return "point", point

    distance_factor = 0.5 + (radius1**2 - radius2**2) / (2 * distance**2)
    center = add_vectors(center1, scale_vector(subtract_vectors(center2, center1), distance_factor))
    radius = sqrt(max(0.0, radius1**2 - distance_factor**2 * distance**2))
    normal = scale_vector(subtract_vectors(center2, center1), 1 / distance)
    return "circle", (center, radius, normal)


def intersection_sphere_line(
    sphere: SphereType,
    line: Sequence[CoordinateType],
    tol: float | None = None,
) -> PointCoordinates | tuple[PointCoordinates, PointCoordinates] | None:
    start, end = line
    center, radius = sphere

    if radius < 0.0:
        raise ValueError("The sphere radius cannot be negative.")

    a = (end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2 + (end[2] - start[2]) ** 2
    if TOL.is_zero(a, tol):
        raise ValueError("A line requires two distinct points.")
    b = 2.0 * ((end[0] - start[0]) * (start[0] - center[0]) + (end[1] - start[1]) * (start[1] - center[1]) + (end[2] - start[2]) * (start[2] - center[2]))
    c = (
        center[0] ** 2
        + center[1] ** 2
        + center[2] ** 2
        + start[0] ** 2
        + start[1] ** 2
        + start[2] ** 2
        - 2.0 * (center[0] * start[0] + center[1] * start[1] + center[2] * start[2])
        - radius**2
    )
    discriminant = b * b - 4.0 * a * c
    if TOL.is_zero(discriminant, tol):
        discriminant = 0.0
    elif discriminant < 0.0:
        return None

    if discriminant == 0.0:
        parameter = -b / (2.0 * a)
        return (
            start[0] + parameter * (end[0] - start[0]),
            start[1] + parameter * (end[1] - start[1]),
            start[2] + parameter * (end[2] - start[2]),
        )

    root = sqrt(discriminant)
    parameter1 = (-b + root) / (2.0 * a)
    parameter2 = (-b - root) / (2.0 * a)
    point1 = (
        start[0] + parameter1 * (end[0] - start[0]),
        start[1] + parameter1 * (end[1] - start[1]),
        start[2] + parameter1 * (end[2] - start[2]),
    )
    point2 = (
        start[0] + parameter2 * (end[0] - start[0]),
        start[1] + parameter2 * (end[1] - start[1]),
        start[2] + parameter2 * (end[2] - start[2]),
    )
    return point1, point2


def intersection_plane_circle(
    plane: Sequence[CoordinateType],
    circle: tuple[Sequence[CoordinateType], float],
    tol: float | None = None,
) -> PointCoordinates | tuple[PointCoordinates, PointCoordinates] | None:
    circle_plane, circle_radius = circle
    line = intersection_plane_plane(plane, circle_plane, tol=tol)
    if line is None:
        return None
    return intersection_sphere_line((circle_plane[0], circle_radius), line, tol=tol)


def intersection_segment_plane(
    segment: Sequence[CoordinateType],
    plane: Sequence[CoordinateType],
    tol: float | None = None,
) -> list[float] | None:
    a, b = segment
    o, n = plane
    ab = subtract_vectors(b, a)
    cosa = dot_vectors(n, ab)

    if TOL.is_zero(cosa, tol):
        return None

    oa = subtract_vectors(a, o)
    ratio = -dot_vectors(n, oa) / cosa
    if 0.0 <= ratio <= 1.0:
        return add_vectors(a, scale_vector(ab, ratio))
    return None


def intersection_line_triangle(
    line: Sequence[CoordinateType],
    triangle: Sequence[CoordinateType],
    tol: float | None = None,
) -> list[float] | None:
    a, b, c = triangle
    ab = subtract_vectors(b, a)
    ac = subtract_vectors(c, a)
    plane = a, cross_vectors(ab, ac)
    point = intersection_line_plane(line, plane, tol=tol)

    if point is not None and is_point_in_triangle(point, triangle):
        return point
    return None
