import compas
import pytest

from compas.geometry import DiagonalSplit
from compas.geometry import EarClipping
from compas.geometry import FaceTriangulation
from compas.geometry import MinimumAreaTriangulation
from compas.geometry import PolygonalSurface
from compas.geometry import ProjectedEarClipping
from compas.geometry import TriangulationStrategy
from compas.geometry.triangulation import triangulate_polygon


@pytest.mark.parametrize(
    "strategy",
    [
        DiagonalSplit(),
        DiagonalSplit("02"),
        DiagonalSplit("13"),
        EarClipping(),
        FaceTriangulation(),
        FaceTriangulation(quad=EarClipping()),
        MinimumAreaTriangulation(),
        ProjectedEarClipping(0.01),
        FaceTriangulation(quad=MinimumAreaTriangulation(), ngon=ProjectedEarClipping(0.01)),
    ],
)
def test_face_triangulation_strategies_roundtrip_as_data(strategy):
    assert isinstance(strategy, TriangulationStrategy)
    other = compas.json_loads(compas.json_dumps(strategy))
    assert other == strategy
    assert hash(other) == hash(strategy)


def test_face_triangulation_strategies_are_immutable():
    strategy = DiagonalSplit()
    with pytest.raises(AttributeError):
        strategy.diagonal = "13"


def test_diagonal_split_validates_diagonal():
    with pytest.raises(ValueError):
        DiagonalSplit("longest")  # type: ignore[arg-type]


def test_face_triangulation_validates_leaf_strategies():
    with pytest.raises(TypeError, match="quad"):
        FaceTriangulation(quad=object())  # type: ignore[arg-type]

    with pytest.raises(TypeError, match="ngon"):
        FaceTriangulation(ngon=DiagonalSplit())  # type: ignore[arg-type]


def test_projected_ear_clipping_validates_max_deviation():
    with pytest.raises(TypeError, match="real number"):
        ProjectedEarClipping(True)  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="nonnegative and finite"):
        ProjectedEarClipping(-1.0)
    with pytest.raises(ValueError, match="nonnegative and finite"):
        ProjectedEarClipping(float("inf"))


def test_face_triangulation_dispatches_by_face_arity():
    strategy = FaceTriangulation(quad=DiagonalSplit("13"), ngon=EarClipping())

    assert triangulate_polygon([[0, 0, 0], [1, 0, 0], [0, 1, 0]], strategy) == [[0, 1, 2]]
    assert triangulate_polygon([[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]], strategy) == [
        [0, 1, 3],
        [1, 2, 3],
    ]

    ngon = [[0, 0, 0], [2, 0, 0], [2, 2, 0], [1, 1, 0], [0, 2, 0]]
    triangles = triangulate_polygon(ngon, strategy)
    assert len(triangles) == 3
    assert {index for triangle in triangles for index in triangle} == set(range(5))


def test_face_triangulation_nonplanar_contract():
    warped_quad = [[0, 0, 0], [1, 0, 0], [1, 1, 1], [0, 1, 0]]
    assert triangulate_polygon(warped_quad, FaceTriangulation(quad=DiagonalSplit("02"))) == [
        [0, 1, 2],
        [0, 2, 3],
    ]

    with pytest.raises(ValueError, match="planar"):
        triangulate_polygon(warped_quad, FaceTriangulation(quad=EarClipping()))

    warped_ngon = [[0, 0, 0], [2, 0, 0], [2, 2, 0], [1, 1, 1], [0, 2, 0]]
    with pytest.raises(ValueError, match="planar"):
        triangulate_polygon(warped_ngon, FaceTriangulation())


def test_face_triangulation_rejects_degenerate_face_arity():
    with pytest.raises(ValueError, match="at least three"):
        triangulate_polygon([[0, 0, 0], [1, 0, 0]], FaceTriangulation())


def test_diagonal_split_shortest_uses_02_for_equal_diagonals():
    vertices = [[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]]
    surface = PolygonalSurface(vertices, [[0, 1, 2, 3]])

    assert surface.triangulated(FaceTriangulation(quad=DiagonalSplit())).triangles == [[0, 1, 2], [0, 2, 3]]


def test_ear_clipping_rejects_nonplanar_faces():
    vertices = [[0, 0, 0], [1, 0, 0], [1, 1, 1], [0, 1, 0]]
    surface = PolygonalSurface(vertices, [[0, 1, 2, 3]])

    with pytest.raises(ValueError, match="planar"):
        surface.triangulated(FaceTriangulation(quad=EarClipping()))


def test_ear_clipping_preserves_original_indices():
    vertices = [[0, 0, 0], [2, 0, 0], [2, 2, 0], [1, 1, 0], [0, 2, 0]]
    triangles = triangulate_polygon(vertices, EarClipping())

    assert len(triangles) == len(vertices) - 2
    assert {index for triangle in triangles for index in triangle} == set(range(len(vertices)))


@pytest.mark.parametrize("strategy", [EarClipping(), ProjectedEarClipping(0.1)])
@pytest.mark.parametrize(
    "vertices",
    [
        [[0, 0, 0], [2, 0, 0], [2, 0, 0], [2, 2, 0], [0, 2, 0]],
        [[0, 0, 0], [2, 0, 0], [2, 2, 0], [0, 2, 0], [0, 0, 0]],
    ],
)
def test_ear_clipping_strategies_reject_zero_length_boundary_edges_before_polygon_normalization(strategy, vertices):
    with pytest.raises(ValueError, match="zero-length boundary edges"):
        triangulate_polygon(vertices, strategy)


@pytest.mark.parametrize("strategy", [EarClipping(), ProjectedEarClipping(0.1)])
def test_ear_clipping_strategies_reject_repeated_vertices_before_polygon_normalization(strategy):
    vertices = [[0, 0, 0], [2, 0, 0], [2, 2, 0], [2, 0, 0], [0, 2, 0]]
    with pytest.raises(ValueError, match="repeated vertices"):
        triangulate_polygon(vertices, strategy)


@pytest.mark.parametrize("strategy", [EarClipping(), ProjectedEarClipping(0.1)])
@pytest.mark.parametrize(
    "vertices",
    [
        [[0, 0], [1, 0], [0, 1]],
        [[0, 0, 0, 1], [1, 0, 0, 1], [0, 1, 0, 1]],
    ],
)
def test_ear_clipping_strategies_require_exact_finite_xyz_coordinates(strategy, vertices):
    with pytest.raises(ValueError, match="exactly three finite coordinates"):
        triangulate_polygon(vertices, strategy)


def test_projected_ear_clipping_accepts_only_bounded_deviation():
    vertices = [[0, 0, 0], [2, 0, 0.01], [2, 2, 0], [1, 1, 0.02], [0, 2, 0]]

    triangles = triangulate_polygon(vertices, ProjectedEarClipping(0.1))
    assert len(triangles) == 3
    assert {index for triangle in triangles for index in triangle} == set(range(5))

    with pytest.raises(ValueError, match="max_deviation"):
        triangulate_polygon(vertices, ProjectedEarClipping(1e-6))


def test_projected_ear_clipping_rejects_self_intersecting_projection():
    vertices = [[0, 0, 0], [2, 2, 0.01], [0, 2, 0], [2, 0, -0.01]]
    with pytest.raises(ValueError, match="self-intersecting"):
        triangulate_polygon(vertices, ProjectedEarClipping(0.1))


def test_minimum_area_triangulation_is_deterministic_for_equal_costs():
    vertices = [[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]]
    expected = [[0, 1, 3], [1, 2, 3]]
    assert triangulate_polygon(vertices, MinimumAreaTriangulation()) == expected
    assert triangulate_polygon(vertices, MinimumAreaTriangulation()) == expected


def test_minimum_area_triangulation_handles_twisted_polygon_without_projection():
    vertices = [[0, 0, 0], [2, 0, 1], [3, 1, -1], [2, 3, 2], [0, 2, -1]]
    triangles = triangulate_polygon(vertices, MinimumAreaTriangulation())

    assert len(triangles) == 3
    assert {index for triangle in triangles for index in triangle} == set(range(5))


def test_minimum_area_triangulation_selects_the_lower_area_diagonal():
    vertices = [[0, 0, 0], [2, 0, 1], [2, 2, 0], [0, 2, 0]]
    assert triangulate_polygon(vertices, MinimumAreaTriangulation()) == [[0, 2, 3], [0, 1, 2]]


@pytest.mark.parametrize(
    "vertices, message",
    [
        ([[0, 0, 0], [1, 0, 0], [0, 0, 0]], "zero-length boundary edges"),
        ([[0, 0, 0], [2, 0, 0], [2, 2, 0], [2, 0, 0], [0, 2, 0]], "repeated vertices"),
        ([[0, 0, 0], [1, 0, 0], [2, 0, 0]], "no nondegenerate"),
        ([[0, 0, 0], [1, 0, 0], [0, float("nan"), 0]], "three finite coordinates"),
    ],
)
def test_minimum_area_triangulation_rejects_invalid_polygon(vertices, message):
    with pytest.raises(ValueError, match=message):
        triangulate_polygon(vertices, MinimumAreaTriangulation())
