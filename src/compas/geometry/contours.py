from collections.abc import Sequence
from typing import TYPE_CHECKING

from compas._typing import CoordinatesType

if TYPE_CHECKING:
    from numpy.typing import NDArray


def _interpolate_edge(
    a: tuple[float, float],
    b: tuple[float, float],
    value_a: float,
    value_b: float,
    level: float,
) -> tuple[float, float]:
    factor = (level - value_a) / (value_b - value_a)
    return a[0] + factor * (b[0] - a[0]), a[1] + factor * (b[1] - a[1])


def _join_segments(segments: list[tuple[tuple[float, float], tuple[float, float]]]) -> list[list[list[float]]]:
    adjacency: dict[tuple[float, float], list[tuple[int, tuple[float, float]]]] = {}
    for index, (a, b) in enumerate(segments):
        adjacency.setdefault(a, []).append((index, b))
        adjacency.setdefault(b, []).append((index, a))

    unused = set(range(len(segments)))
    paths = []
    while unused:
        segment = next(iter(unused))
        a, b = segments[segment]
        start = a if len(adjacency[a]) == 1 else b if len(adjacency[b]) == 1 else a
        path = [start]
        current = start

        while True:
            candidates = [(index, other) for index, other in adjacency[current] if index in unused]
            if not candidates:
                break
            index, current = candidates[0]
            unused.remove(index)
            path.append(current)
            if current == start:
                break

        paths.append([[x, y] for x, y in path])
    return paths


def _contours_from_grid(x: "NDArray", y: "NDArray", values: "NDArray", level: float) -> list[list[list[float]]]:
    from numpy import isfinite

    # Edges are ordered counterclockwise: bottom, right, top, left.
    cases = {
        1: ((3, 0),),
        2: ((0, 1),),
        3: ((3, 1),),
        4: ((1, 2),),
        6: ((0, 2),),
        7: ((3, 2),),
        8: ((2, 3),),
        9: ((0, 2),),
        11: ((1, 2),),
        12: ((3, 1),),
        13: ((0, 1),),
        14: ((3, 0),),
    }
    segments = []

    for row in range(len(y) - 1):
        for column in range(len(x) - 1):
            corners = (
                (float(x[column]), float(y[row])),
                (float(x[column + 1]), float(y[row])),
                (float(x[column + 1]), float(y[row + 1])),
                (float(x[column]), float(y[row + 1])),
            )
            scalar = (
                float(values[row, column]),
                float(values[row, column + 1]),
                float(values[row + 1, column + 1]),
                float(values[row + 1, column]),
            )
            if not all(isfinite(value) for value in scalar):
                continue

            case = sum(1 << index for index, value in enumerate(scalar) if value >= level)
            if case in (0, 15):
                continue

            pairs = cases.get(case)
            if pairs is None:
                center_is_high = sum(scalar) / 4 >= level
                if case == 5:
                    pairs = ((0, 1), (2, 3)) if center_is_high else ((3, 0), (1, 2))
                else:
                    pairs = ((3, 0), (1, 2)) if center_is_high else ((0, 1), (2, 3))

            edge_corners = ((0, 1), (1, 2), (2, 3), (3, 0))
            intersections = {}
            for edge in {edge for pair in pairs for edge in pair}:
                i, j = edge_corners[edge]
                point = _interpolate_edge(corners[i], corners[j], scalar[i], scalar[j], level)
                intersections[edge] = tuple(round(coordinate, 14) for coordinate in point)
            segments.extend(
                (intersections[a], intersections[b]) for a, b in pairs if intersections[a] != intersections[b]
            )

    return _join_segments(segments)


def scalarfield_contours(
    xy: CoordinatesType,
    s: Sequence[float],
    levels: int | Sequence[float] = 50,
    density: int = 100,
) -> tuple[list[float], list[list[list[list[float]]]]]:
    """Compute contour lines of a scalar field sampled at scattered XY points.

    Parameters
    ----------
    xy
        XY(Z) coordinates at which the scalar field is sampled.
    s
        Scalar value at every sample point.
    levels
        Number of evenly spaced contour levels, or the explicit level values.
    density
        Number of samples along each axis of the interpolation grid.

    Returns
    -------
    tuple[list[float], list[list[list[list[float]]]]]
        The contour levels and their paths. Each level contains zero or more
        paths, and every path is a list of XY coordinates. Closed paths repeat
        their first coordinate at the end.

    Notes
    -----
    The scattered values are linearly interpolated with
    `scipy.interpolate.griddata`. Contour paths are then extracted from the
    regular grid with marching squares. Cells outside the convex hull of the
    sample points are ignored.

    """
    from numpy import asarray
    from numpy import linspace
    from numpy import meshgrid
    from scipy.interpolate import griddata

    points = asarray(xy, dtype=float)
    scalars = asarray(s, dtype=float)
    x = linspace(points[:, 0].min(), points[:, 0].max(), density)
    y = linspace(points[:, 1].min(), points[:, 1].max(), density)
    grid_x, grid_y = meshgrid(x, y)
    values = griddata(points[:, :2], scalars, (grid_x, grid_y), method="linear")

    if isinstance(levels, int):
        contour_levels = linspace(scalars.min(), scalars.max(), levels + 2)[1:-1].tolist()
    else:
        contour_levels = [float(level) for level in levels]

    contours = [_contours_from_grid(x, y, values, level) for level in contour_levels]
    return contour_levels, contours
