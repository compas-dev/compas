from typing import TYPE_CHECKING

from compas._typing import CoordinatesType
from compas._typing import MeshType

if TYPE_CHECKING:
    from numpy.typing import NDArray


def _closest_point_on_segment(point: "NDArray", start: "NDArray", end: "NDArray") -> "NDArray":
    from numpy import clip
    from numpy import dot

    direction = end - start
    denominator = dot(direction, direction)
    if denominator == 0:
        return start
    factor = clip(dot(point - start, direction) / denominator, 0.0, 1.0)
    return start + factor * direction


def _closest_point_on_triangle(point: "NDArray", triangle: "NDArray") -> "NDArray":
    from numpy import cross
    from numpy import dot

    a, b, c = triangle
    ab = b - a
    ac = c - a

    if dot(cross(ab, ac), cross(ab, ac)) == 0:
        candidates = (
            _closest_point_on_segment(point, a, b),
            _closest_point_on_segment(point, b, c),
            _closest_point_on_segment(point, c, a),
        )
        return min(candidates, key=lambda candidate: dot(point - candidate, point - candidate))

    ap = point - a
    d1 = dot(ab, ap)
    d2 = dot(ac, ap)
    if d1 <= 0 and d2 <= 0:
        return a

    bp = point - b
    d3 = dot(ab, bp)
    d4 = dot(ac, bp)
    if d3 >= 0 and d4 <= d3:
        return b

    vc = d1 * d4 - d3 * d2
    if vc <= 0 and d1 >= 0 and d3 <= 0:
        return a + d1 / (d1 - d3) * ab

    cp = point - c
    d5 = dot(ab, cp)
    d6 = dot(ac, cp)
    if d6 >= 0 and d5 <= d6:
        return c

    vb = d5 * d2 - d1 * d6
    if vb <= 0 and d2 >= 0 and d6 <= 0:
        return a + d2 / (d2 - d6) * ac

    va = d3 * d6 - d5 * d4
    if va <= 0 and d4 - d3 >= 0 and d5 - d6 >= 0:
        return b + (d4 - d3) / ((d4 - d3) + (d5 - d6)) * (c - b)

    denominator = 1.0 / (va + vb + vc)
    return a + vb * denominator * ab + vc * denominator * ac


def trimesh_pull_points(mesh: MeshType, points: CoordinatesType) -> list[list[float]]:
    """Compute the closest point on a triangle mesh for each input point.

    Parameters
    ----------
    mesh
        The mesh vertex coordinates and triangular faces.
    points
        The points to pull onto the mesh.

    Returns
    -------
    list[list[float]]
        The closest point on the mesh for every input point.

    Notes
    -----
    Every triangle is considered for every point. This favors correctness over
    acceleration and provides a deterministic baseline implementation for
    moderate mesh sizes.

    """
    from numpy import asarray
    from numpy import dot

    vertices, faces = mesh
    xyz = asarray(vertices, dtype=float)
    triangles = xyz[asarray(faces, dtype=int)]
    pulled = []

    for point in asarray(points, dtype=float):
        candidates = [_closest_point_on_triangle(point, triangle) for triangle in triangles]
        closest = min(candidates, key=lambda candidate: dot(point - candidate, point - candidate))
        pulled.append(closest.tolist())

    return pulled
