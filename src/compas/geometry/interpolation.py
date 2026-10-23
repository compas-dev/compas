from collections.abc import Sequence

from compas._typing import CoordinatesType
from compas._typing import CoordinateType
from compas.itertools import normalize_values
from compas.linalg.vectors import add_vectors
from compas.linalg.vectors import dot_vectors
from compas.linalg.vectors import scale_vector
from compas.linalg.vectors import subtract_vectors
from compas.linalg.vectors import sum_vectors


def barycentric_coordinates(point: CoordinateType, triangle: Sequence[CoordinateType]) -> list[float]:
    """Compute the barycentric coordinates of a point with respect to a triangle.

    Parameters
    ----------
    point
        The point location.
    triangle
        The three triangle vertices.

    Returns
    -------
    list[float]
        The three barycentric coordinates, in triangle vertex order.

    """
    a, b, c = triangle
    v0 = subtract_vectors(b, a)
    v1 = subtract_vectors(c, a)
    v2 = subtract_vectors(point, a)
    d00 = dot_vectors(v0, v0)
    d01 = dot_vectors(v0, v1)
    d11 = dot_vectors(v1, v1)
    d20 = dot_vectors(v2, v0)
    d21 = dot_vectors(v2, v1)
    denominator = d00 * d11 - d01 * d01
    v = (d11 * d20 - d01 * d21) / denominator
    w = (d00 * d21 - d01 * d20) / denominator
    u = 1.0 - v - w
    return [u, v, w]


def discrete_coons_patch(
    ab: CoordinatesType | None,
    bc: CoordinatesType | None,
    dc: CoordinatesType | None,
    ad: CoordinatesType | None,
) -> tuple[list[list[float]], list[list[int]]]:
    """Construct a discrete Coons patch from three or four boundary polylines.

    Parameters
    ----------
    ab
        Points of the first boundary polyline, ordered from A to B.
    bc
        Points of the second boundary polyline, ordered from B to C.
    dc
        Points of the third boundary polyline, ordered from D to C.
    ad
        Points of the fourth boundary polyline, ordered from A to D.

    Returns
    -------
    tuple[list[list[float]], list[list[int]]]
        The patch vertex coordinates and quad faces.

    Notes
    -----
    The boundary directions are:

    ```text
    B -----> C
    ^        ^
    |        |
    |        |
    A -----> D
    ```

    Set one boundary to `None` to construct a triangular patch. The collapsed
    boundary is represented by duplicate vertices.

    References
    ----------
    - [Coons patch](https://en.wikipedia.org/wiki/Coons_patch)
    - [Patch de Coons](https://www.mathcurve.com/surfaces/patchcoons/patchcoons.shtml)

    """
    # The other three boundaries define the collapsed edge. Invalid boundary
    # combinations are intentionally left to normal indexing and length errors.
    if not ab:
        ab = [ad[0]] * len(dc)  # type: ignore[index, arg-type]
    if not bc:
        bc = [ab[-1]] * len(ad)  # type: ignore[arg-type]
    if not dc:
        dc = [bc[-1]] * len(ab)
    if not ad:
        ad = [dc[0]] * len(bc)

    n = len(ab)
    m = len(bc)
    n_norm = normalize_values(range(n))
    m_norm = normalize_values(range(m))

    array = []
    for i, ki in enumerate(n_norm):
        row = []
        for j, kj in enumerate(m_norm):
            ab_dc = add_vectors(scale_vector(ab[i], 1 - kj), scale_vector(dc[i], kj))
            ad_bc = add_vectors(scale_vector(ad[j], 1 - ki), scale_vector(bc[j], ki))
            corners = sum_vectors(
                [
                    scale_vector(ab[0], (1 - ki) * (1 - kj)),
                    scale_vector(bc[0], ki * (1 - kj)),
                    scale_vector(dc[-1], ki * kj),
                    scale_vector(ad[-1], (1 - ki) * kj),
                ]
            )
            row.append(subtract_vectors(add_vectors(ab_dc, ad_bc), corners))
        array.append(row)

    vertices = [point for row in array for point in row]
    faces = [[i * m + j, i * m + j + 1, (i + 1) * m + j + 1, (i + 1) * m + j] for i in range(n - 1) for j in range(m - 1)]
    return vertices, faces


def tween_points(points1: CoordinatesType, points2: CoordinatesType, num: int) -> list[list[list[float]]]:
    """Compute evenly spaced interpolations between two point sets.

    Parameters
    ----------
    points1
        The first point set.
    points2
        The second point set.
    num
        Number of intermediate point sets.

    Returns
    -------
    list[list[list[float]]]
        The intermediate point sets, excluding both input sets.

    Notes
    -----
    Corresponding points are paired with `zip`; unmatched trailing points are
    ignored.

    """
    vectors = [subtract_vectors(point2, point1) for point1, point2 in zip(points1, points2)]
    return [[add_vectors(point, scale_vector(vector, (index + 1.0) / (num + 1.0))) for point, vector in zip(points1, vectors)] for index in range(num)]


def tween_points_distance(
    points1: CoordinatesType,
    points2: CoordinatesType,
    dist: float,
    index: int | None = None,
) -> list[list[float]]:
    """Interpolate two point sets at a specified reference-point distance.

    Parameters
    ----------
    points1
        The first point set.
    points2
        The second point set.
    dist
        Distance from the first point set along the interpolation.
    index
        Index of the corresponding point pair used to measure the full
        interpolation distance. The first pair is used by default.

    Returns
    -------
    list[list[float]]
        The interpolated point set.

    """
    from compas.geometry import distance_point_point

    reference = 0 if index is None else index
    total = distance_point_point(points1[reference], points2[reference])
    scale = float(dist) / total
    return [add_vectors(point1, scale_vector(subtract_vectors(point2, point1), scale)) for point1, point2 in zip(points1, points2)]
