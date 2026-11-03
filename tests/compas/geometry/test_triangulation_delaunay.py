import compas
import compas.geometry as geometry
import pytest

from compas.geometry import ConformingDelaunay
from compas.geometry import ConstrainedDelaunay
from compas.geometry import Delaunay
from compas.geometry import Frame
from compas.geometry import Tessellation
from compas.geometry import TriangulationQuality
from compas.geometry import triangulate_planar_domain
from compas.geometry import triangulate_planar_points


def test_unqualified_planar_operation_names_are_not_exported():
    assert not hasattr(geometry, "triangulate_points")
    assert not hasattr(geometry, "triangulate_domain")


def test_planar_strategies_roundtrip_as_data():
    strategies = [
        Delaunay(),
        ConstrainedDelaunay(),
        ConformingDelaunay(),
        ConformingDelaunay(TriangulationQuality(min_angle=20.0, max_area=1.0, max_edge_length=2.0)),
    ]
    for strategy in strategies:
        other = compas.json_loads(compas.json_dumps(strategy))
        assert other == strategy
        assert hash(other) == hash(strategy)


def test_triangulation_quality_validation():
    with pytest.raises(ValueError):
        TriangulationQuality()
    with pytest.raises(ValueError):
        TriangulationQuality(min_angle=60.0)
    with pytest.raises(ValueError):
        TriangulationQuality(max_area=0.0)


def test_triangulate_planar_points_returns_tessellation_and_preserves_coordinates():
    points = [[0.0, 0.0, 0.0], [2.0, 0.0, 0.0], [2.0, 1.0, 0.0], [0.0, 1.0, 0.0]]

    result = triangulate_planar_points(points, strategy=Delaunay())

    assert isinstance(result, Tessellation)
    assert result.vertices == points
    assert len(result.triangles) == 2
    assert {int(index) for triangle in result.triangles for index in triangle} == {0, 1, 2, 3}


def test_triangulate_planar_points_requires_world_xy_without_frame():
    with pytest.raises(ValueError):
        triangulate_planar_points([[0, 0, 1], [1, 0, 1], [0, 1, 1]], strategy=Delaunay())


def test_triangulate_planar_points_accepts_explicit_frame_and_preserves_coordinates():
    frame = Frame.worldYZ()
    points = [[0.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, 2.0, 1.0], [0.0, 0.0, 1.0]]

    result = triangulate_planar_points(points, strategy=Delaunay(), frame=frame)

    assert result.vertices == points
    assert len(result.triangles) == 2


def test_triangulate_planar_points_rejects_off_frame_input():
    frame = Frame.worldYZ()
    with pytest.raises(ValueError):
        triangulate_planar_points([[1, 0, 0], [0, 1, 0], [0, 0, 1]], strategy=Delaunay(), frame=frame)


def test_triangulate_planar_points_requires_delaunay_strategy():
    with pytest.raises(TypeError):
        triangulate_planar_points(
            [[0, 0, 0], [1, 0, 0], [0, 1, 0]],
            strategy=ConstrainedDelaunay(),  # type: ignore[arg-type]
        )


@pytest.mark.parametrize(
    ("points", "message"),
    [
        ([[0, 0, 0], [1, 0, 0]], "requires at least 3 points"),
        ([[0, 0], [1, 0, 0], [0, 1, 0]], "exactly three coordinates"),
        ([[0, 0, 0], [1, 0, 0], [0, float("inf"), 0]], "finite coordinates"),
    ],
)
def test_triangulate_planar_points_validates_coordinates(points, message):
    with pytest.raises(ValueError, match=message):
        triangulate_planar_points(points, strategy=Delaunay())


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        ({"boundary": [[0, 0, 0], [1, 0, 0]]}, "Boundary requires at least 3 points"),
        (
            {
                "boundary": [[0, 0, 0], [1, 0, 0], [0, 1, 0]],
                "holes": [[[0.1, 0.1, 0], [0.2, 0.1, 0]]],
            },
            "Hole requires at least 3 points",
        ),
        (
            {
                "boundary": [[0, 0, 0], [1, 0, 0], [0, 1, 0]],
                "constraints": [[[0.1, 0.1, 0]]],
            },
            "Constraint requires at least 2 points",
        ),
    ],
)
def test_triangulate_planar_domain_validates_groups_before_dispatch(kwargs, message):
    with pytest.raises(ValueError, match=message):
        triangulate_planar_domain(strategy=ConstrainedDelaunay(), **kwargs)
