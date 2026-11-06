from math import isfinite
from numbers import Real
from typing import Literal

from compas.data import Data
from compas.tolerance import TOL
from compas.typing import PointsLike

__all__ = [
    "ConformingDelaunay",
    "ConstrainedDelaunay",
    "Delaunay",
    "DiagonalSplit",
    "EarClipping",
    "FaceTriangulation",
    "MinimumAreaTriangulation",
    "ProjectedEarClipping",
    "TriangulationQuality",
    "TriangulationStrategy",
]


def _positive_finite(value: float, name: str) -> float:
    if not isinstance(value, Real) or isinstance(value, bool):
        raise TypeError(f"{name} should be a real number.")
    value = float(value)
    if not isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} should be positive and finite.")
    return value


class _ImmutableData(Data):
    def __init__(self) -> None:
        super().__init__()
        self._frozen = False

    def __setattr__(self, name: str, value: object) -> None:
        if getattr(self, "_frozen", False) and name not in {"_guid", "_name"}:
            raise AttributeError(f"{type(self).__name__} is immutable.")
        super().__setattr__(name, value)

    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and isinstance(other, _ImmutableData) and self.__data__ == other.__data__

    def __hash__(self) -> int:
        return hash((type(self), tuple(self.__data__.items())))

    def _freeze(self) -> None:
        self._frozen = True


class TriangulationStrategy(_ImmutableData):
    """Base class for serializable polygon-face triangulation strategies."""


class DiagonalSplit(TriangulationStrategy):
    """Split triangular and quadrilateral faces without inserting vertices.

    Parameters
    ----------
    diagonal
        The quad diagonal selection: `"shortest"`, `"02"`, or `"13"`.

    """

    @property
    def __data__(self) -> dict:
        return {"diagonal": self.diagonal}

    def __init__(self, diagonal: Literal["shortest", "02", "13"] = "shortest") -> None:
        super().__init__()
        if diagonal not in {"shortest", "02", "13"}:
            raise ValueError('diagonal should be "shortest", "02", or "13".')
        self.diagonal = diagonal
        self._freeze()


class EarClipping(TriangulationStrategy):
    """Triangulate planar polygonal faces without inserting vertices."""

    @property
    def __data__(self) -> dict:
        return {}

    def __init__(self) -> None:
        super().__init__()
        self._freeze()


class ProjectedEarClipping(TriangulationStrategy):
    """Triangulate a near-planar polygon through its best-fit plane.

    Parameters
    ----------
    max_deviation
        The maximum permitted distance from a vertex to the best-fit plane.

    Notes
    -----
    The strategy projects the polygon to its best-fit plane, triangulates the
    projected boundary, and returns indices into the original 3D vertices. It
    rejects degenerate and self-intersecting projections and never inserts
    vertices.

    """

    @property
    def __data__(self) -> dict:
        return {"max_deviation": self.max_deviation}

    def __init__(self, max_deviation: float) -> None:
        super().__init__()
        if not isinstance(max_deviation, Real) or isinstance(max_deviation, bool):
            raise TypeError("max_deviation should be a real number.")
        max_deviation = float(max_deviation)
        if not isfinite(max_deviation) or max_deviation < 0.0:
            raise ValueError("max_deviation should be nonnegative and finite.")
        self.max_deviation = max_deviation
        self._freeze()


class MinimumAreaTriangulation(TriangulationStrategy):
    """Triangulate an ordered 3D polygon with minimum total triangle area.

    Notes
    -----
    This strategy uses the dynamic program of Barequet and Sharir for additive
    per-triangle weights. It performs no projection, inserts no vertices, and
    takes $O(n^3)$ time and $O(n^2)$ space.

    The result is a combinatorially manifold disk, but its triangles are not
    guaranteed to form an intersection-free surface in 3D.

    References
    ----------
    Barequet, G. and Sharir, M. *Filling gaps in the boundary of a polyhedron*.
    Computer Aided Geometric Design 12(2), 1995.
    https://doi.org/10.1016/0167-8396(94)00011-G

    """

    @property
    def __data__(self) -> dict:
        return {}

    def __init__(self) -> None:
        super().__init__()
        self._freeze()


class FaceTriangulation(TriangulationStrategy):
    """Triangulate mixed polygonal faces with arity-specific policies.

    Parameters
    ----------
    quad
        The strategy for quadrilateral faces. Supported policies are
        :class:`DiagonalSplit`, :class:`EarClipping`,
        :class:`ProjectedEarClipping`, and :class:`MinimumAreaTriangulation`.
        Defaults to :class:`DiagonalSplit` with its shortest-diagonal policy.
    ngon
        The strategy for faces with five or more vertices. Supported policies
        are :class:`EarClipping`, :class:`ProjectedEarClipping`, and
        :class:`MinimumAreaTriangulation`. Defaults to :class:`EarClipping`.

    Notes
    -----
    Triangular faces pass through unchanged. A :class:`DiagonalSplit` may be
    used for non-planar quads because its selected diagonal explicitly defines
    the piecewise-planar surface. :class:`EarClipping` requires planar input.
    Projection and twisted-polygon triangulation are available only when their
    corresponding explicit strategies are selected.

    """

    @property
    def __data__(self) -> dict:
        return {"quad": self.quad, "ngon": self.ngon}

    def __init__(
        self,
        quad: DiagonalSplit | EarClipping | ProjectedEarClipping | MinimumAreaTriangulation | None = None,
        ngon: EarClipping | ProjectedEarClipping | MinimumAreaTriangulation | None = None,
    ) -> None:
        super().__init__()
        quad = DiagonalSplit() if quad is None else quad
        ngon = EarClipping() if ngon is None else ngon
        if not isinstance(quad, (DiagonalSplit, EarClipping, ProjectedEarClipping, MinimumAreaTriangulation)):
            raise TypeError("quad should be a DiagonalSplit, EarClipping, ProjectedEarClipping, or MinimumAreaTriangulation strategy.")
        if not isinstance(ngon, (EarClipping, ProjectedEarClipping, MinimumAreaTriangulation)):
            raise TypeError("ngon should be an EarClipping, ProjectedEarClipping, or MinimumAreaTriangulation strategy.")
        self.quad = quad
        self.ngon = ngon
        self._freeze()

    def __hash__(self) -> int:
        return hash((type(self), self.quad, self.ngon))


class _PlanarTriangulationStrategy(_ImmutableData):
    pass


class Delaunay(_PlanarTriangulationStrategy):
    """Construct an unconstrained planar Delaunay triangulation."""

    @property
    def __data__(self) -> dict:
        return {}

    def __init__(self) -> None:
        super().__init__()
        self._freeze()


class ConstrainedDelaunay(_PlanarTriangulationStrategy):
    """Construct a planar Delaunay triangulation with constraints."""

    @property
    def __data__(self) -> dict:
        return {}

    def __init__(self) -> None:
        super().__init__()
        self._freeze()


class TriangulationQuality(_ImmutableData):
    """Quality targets for conforming planar triangulation.

    Parameters
    ----------
    min_angle
        The optional minimum triangle angle in degrees, below 60.
    max_area
        The optional maximum triangle area in model units squared.
    max_edge_length
        The optional maximum triangle edge length in model units.

    """

    @property
    def __data__(self) -> dict:
        return {
            "min_angle": self.min_angle,
            "max_area": self.max_area,
            "max_edge_length": self.max_edge_length,
        }

    def __init__(
        self,
        min_angle: float | None = None,
        max_area: float | None = None,
        max_edge_length: float | None = None,
    ) -> None:
        super().__init__()
        if min_angle is None and max_area is None and max_edge_length is None:
            raise ValueError("At least one triangulation-quality target is required.")
        self.min_angle = None if min_angle is None else _positive_finite(min_angle, "min_angle")
        if self.min_angle is not None and self.min_angle >= 60.0:
            raise ValueError("min_angle should be less than 60 degrees.")
        self.max_area = None if max_area is None else _positive_finite(max_area, "max_area")
        self.max_edge_length = None if max_edge_length is None else _positive_finite(max_edge_length, "max_edge_length")
        self._freeze()


class ConformingDelaunay(_PlanarTriangulationStrategy):
    """Construct a conforming planar Delaunay triangulation.

    Parameters
    ----------
    quality
        Optional quality targets.

    """

    @property
    def __data__(self) -> dict:
        return {"quality": None if self.quality is None else self.quality.__data__}

    @classmethod
    def __from_data__(cls, data: dict) -> "ConformingDelaunay":
        quality = data.get("quality")
        return cls(None if quality is None else TriangulationQuality.__from_data__(quality))

    def __init__(self, quality: TriangulationQuality | None = None) -> None:
        super().__init__()
        if quality is not None and not isinstance(quality, TriangulationQuality):
            raise TypeError("quality should be a TriangulationQuality or None.")
        self.quality = quality
        self._freeze()

    def __hash__(self) -> int:
        return hash((type(self), self.quality))


def _validate_finite_polygon(vertices: PointsLike) -> None:
    for vertex in vertices:
        if len(vertex) != 3 or any(not isfinite(vertex[axis]) for axis in range(3)):
            raise ValueError("Polygon vertices should have exactly three finite coordinates.")


def _validate_polygon_boundary(vertices: PointsLike) -> None:
    from compas.geometry import distance_point_point

    for index, vertex in enumerate(vertices):
        if TOL.is_zero(distance_point_point(vertex, vertices[(index + 1) % len(vertices)])):
            raise ValueError("A polygon should not contain zero-length boundary edges.")
    for index, vertex in enumerate(vertices):
        for other_index in range(index + 1, len(vertices)):
            other = vertices[other_index]
            if TOL.is_allclose(vertex, other):
                raise ValueError("A polygon should not contain repeated vertices.")


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


def _projected_ear_clipping(vertices: PointsLike, strategy: ProjectedEarClipping) -> list[list[int]]:
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
    if deviation > strategy.max_deviation and not TOL.is_close(deviation, strategy.max_deviation, rtol=0.0):
        raise ValueError(f"The polygon deviates from its best-fit plane by {deviation}, exceeding max_deviation={strategy.max_deviation}.")
    transformation = Transformation.from_frame_to_frame(Frame.from_plane(plane), Frame.worldXY())
    projected = transform_points(vertices, transformation)
    for point in projected:
        point[2] = 0.0
    return earclip_polygon(Polygon(projected))


def triangulate_polygon(vertices: PointsLike, strategy: TriangulationStrategy) -> list[list[int]]:
    """Triangulate one polygon represented by ordered vertex coordinates.

    Parameters
    ----------
    vertices
        The ordered polygon vertex coordinates.
    strategy
        The polygon triangulation strategy.

    Returns
    -------
    list[list[int]]
        Triangle indices into `vertices`.

    """
    source = [[float(value) for value in vertex] for vertex in vertices]
    return _triangulate_polygon(source, strategy)


def _triangulate_polygon(vertices: PointsLike, strategy: TriangulationStrategy) -> list[list[int]]:
    """Triangulate normalized polygon coordinates."""
    count = len(vertices)
    if count < 3:
        raise ValueError("A polygon requires at least three vertices for triangulation.")
    _validate_finite_polygon(vertices)
    if isinstance(strategy, FaceTriangulation):
        if count == 3:
            return [[0, 1, 2]]
        if count == 4:
            return _triangulate_polygon(vertices, strategy.quad)
        return _triangulate_polygon(vertices, strategy.ngon)
    if isinstance(strategy, DiagonalSplit):
        if count == 3:
            return [[0, 1, 2]]
        if count != 4:
            raise ValueError("DiagonalSplit applies only to triangular and quadrilateral faces.")
        diagonal = strategy.diagonal
        if diagonal == "shortest":
            length_02 = sum((vertices[0][axis] - vertices[2][axis]) ** 2 for axis in range(3))
            length_13 = sum((vertices[1][axis] - vertices[3][axis]) ** 2 for axis in range(3))
            diagonal = "02" if length_02 <= length_13 else "13"
        if diagonal == "02":
            return [[0, 1, 2], [0, 2, 3]]
        return [[0, 1, 3], [1, 2, 3]]
    if isinstance(strategy, EarClipping):
        from compas.geometry import Polygon
        from compas.geometry import earclip_polygon
        from compas.geometry import is_coplanar

        _validate_polygon_boundary(vertices)
        if not is_coplanar(vertices):
            raise ValueError("EarClipping requires a planar polygon.")
        return earclip_polygon(Polygon(vertices))
    if isinstance(strategy, ProjectedEarClipping):
        return _projected_ear_clipping(vertices, strategy)
    if isinstance(strategy, MinimumAreaTriangulation):
        return _minimum_area_triangulation(vertices)
    raise TypeError("Unsupported triangulation strategy.")
