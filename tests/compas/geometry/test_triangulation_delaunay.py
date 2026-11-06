import numpy as np
import pytest

import compas.geometry as geometry
from compas.geometry import Frame
from compas.geometry import conforming_delaunay_triangulation
from compas.geometry import constrained_delaunay_triangulation
from compas.geometry import delaunay_triangulation


def test_removed_planar_strategy_paths_are_not_exported():
    for name in (
        "Delaunay",
        "ConstrainedDelaunay",
        "ConformingDelaunay",
        "TriangulationQuality",
        "triangulate_planar_points",
        "triangulate_planar_domain",
    ):
        assert not hasattr(geometry, name)


def test_delaunay_returns_structural_buffers_and_preserves_coordinates():
    points = [[0.0, 0.0, 0.0], [2.0, 0.0, 0.0], [2.0, 1.0, 0.0], [0.0, 1.0, 0.0]]
    vertices, triangles = delaunay_triangulation(points)
    assert vertices == points
    assert len(triangles) == 2
    assert all(len(triangle) == 3 for triangle in triangles)


def test_delaunay_coalesces_repeated_source_locations():
    points = [[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 0]]
    vertices, triangles = delaunay_triangulation(points)
    assert vertices == points[:3]
    assert triangles == [[1, 2, 0]]


@pytest.mark.parametrize("dtype", [np.float32, np.float64, np.int32, np.int64])
@pytest.mark.parametrize("layout", ["c", "f", "sliced", "readonly"])
def test_delaunay_accepts_numpy_without_mutation(dtype, layout):
    values = np.asarray([[0, 0, 0], [2, 0, 0], [2, 1, 0], [0, 1, 0]], dtype=dtype)
    if layout == "f":
        points = np.asfortranarray(values)
    elif layout == "sliced":
        points = np.pad(values, ((0, 0), (0, 1)))[:, :3]
    else:
        points = values.copy()
    if layout == "readonly":
        points.flags.writeable = False
    before = points.copy()
    _, triangles = delaunay_triangulation(points)
    assert len(triangles) == 2
    np.testing.assert_array_equal(points, before)


def test_delaunay_supports_explicit_frame_and_orients_results():
    frame = Frame.worldYZ()
    points = [[0, 0, 0], [0, 2, 0], [0, 2, 1], [0, 0, 1]]
    vertices, triangles = delaunay_triangulation(points, frame=frame)
    assert vertices == points
    for triangle in triangles:
        local = [frame.to_local_coordinates(vertices[index]) for index in triangle]
        signed_area = sum(local[index].x * local[(index + 1) % 3].y - local[(index + 1) % 3].x * local[index].y for index in range(3))
        assert signed_area > 0


def test_domain_functions_normalize_numpy_and_dispatch_named_hooks(monkeypatch):
    boundary = np.asarray([[0, 0, 0], [3, 0, 0], [3, 3, 0], [0, 3, 0]], dtype=np.float32)
    boundary.flags.writeable = False
    before = boundary.copy()
    captured = {}

    def constrained(boundary, *, holes, constraints, points, frame):
        captured["constrained"] = (boundary, holes, constraints, points, frame)
        return boundary, [[0, 1, 2], [0, 2, 3]]

    def conforming(boundary, *, holes, constraints, points, max_edge_length, frame):
        captured["conforming"] = max_edge_length
        return boundary, [[0, 1, 2], [0, 2, 3]]

    monkeypatch.setattr("compas.geometry.triangulation_delaunay._constrained_delaunay_triangulation", constrained)
    monkeypatch.setattr("compas.geometry.triangulation_delaunay._conforming_delaunay_triangulation", conforming)
    assert len(constrained_delaunay_triangulation(boundary)[1]) == 2
    assert len(conforming_delaunay_triangulation(boundary, max_edge_length=1.0)[1]) == 2
    assert captured["constrained"][0] == boundary.tolist()
    assert captured["conforming"] == 1.0
    np.testing.assert_array_equal(boundary, before)


def test_domain_result_must_preserve_every_source_coordinate(monkeypatch):
    boundary = [[0, 0, 0], [2, 0, 0], [0, 2, 0]]
    points = [[0.5, 0.5, 0]]

    def omit_point(boundary, *, holes, constraints, points, frame):
        return boundary, [[0, 1, 2]]

    monkeypatch.setattr("compas.geometry.triangulation_delaunay._constrained_delaunay_triangulation", omit_point)
    with pytest.raises(ValueError, match="omitted or changed"):
        constrained_delaunay_triangulation(boundary, points=points)


def test_domain_validation_rejects_invalid_rings_and_crossing_constraints(monkeypatch):
    boundary = [[0, 0, 0], [4, 0, 0], [4, 4, 0], [0, 4, 0]]

    def should_not_run(*args, **kwargs):
        raise AssertionError("The plugin should not run for invalid input.")

    monkeypatch.setattr("compas.geometry.triangulation_delaunay._constrained_delaunay_triangulation", should_not_run)
    with pytest.raises(ValueError, match="strictly inside"):
        constrained_delaunay_triangulation(
            boundary,
            holes=[[[5, 5, 0], [6, 5, 0], [5, 6, 0]]],
        )
    with pytest.raises(ValueError, match="shared endpoints"):
        constrained_delaunay_triangulation(
            boundary,
            constraints=[[[1, 1, 0], [3, 3, 0]], [[1, 3, 0], [3, 1, 0]]],
        )


@pytest.mark.parametrize("value", [True, "1"])
def test_conforming_max_edge_length_rejects_non_real(value):
    boundary = [[0, 0, 0], [1, 0, 0], [0, 1, 0]]
    with pytest.raises(TypeError):
        conforming_delaunay_triangulation(boundary, max_edge_length=value)  # pyright: ignore[reportArgumentType]


@pytest.mark.parametrize("value", [0.0, -1.0, float("inf")])
def test_conforming_max_edge_length_requires_positive_finite(value):
    boundary = [[0, 0, 0], [1, 0, 0], [0, 1, 0]]
    with pytest.raises(ValueError):
        conforming_delaunay_triangulation(boundary, max_edge_length=value)


def test_planarity_is_validated_before_dispatch():
    with pytest.raises(ValueError, match="world XY"):
        delaunay_triangulation([[0, 0, 1], [1, 0, 1], [0, 1, 1]])
