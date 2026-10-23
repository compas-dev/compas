import json

import pytest

from compas.geometry import PlanarRegion
from compas.geometry import Translation


@pytest.fixture
def region():
    return PlanarRegion(
        [[0, 0, 0], [4, 0, 0], [4, 4, 0], [0, 4, 0]],
        holes=[[[1, 1, 0], [1, 3, 0], [3, 3, 0], [3, 1, 0]]],
    )


def test_planar_region_triangulates_holes(region):
    vertices, triangles = region.to_vertices_and_faces()

    assert len(vertices) == 8
    assert len(triangles) == 8
    assert {index for triangle in triangles for index in triangle} == set(range(8))
    assert region.to_polygonal_surface().area() == pytest.approx(region.area())
    assert region.area() == pytest.approx(12.0)


def test_planar_region_accepts_same_winding_for_hole():
    region = PlanarRegion(
        [[0, 0, 0], [4, 0, 0], [4, 4, 0], [0, 4, 0]],
        holes=[[[1, 1, 0], [3, 1, 0], [3, 3, 0], [1, 3, 0]]],
    )

    assert region.to_polygonal_surface().area() == pytest.approx(12.0)


def test_planar_region_copies_boundaries():
    outer = [[0, 0, 0], [4, 0, 0], [4, 4, 0], [0, 4, 0]]
    region = PlanarRegion(outer)
    outer[0][0] = 10

    assert region.outer.points[0].x == 0


def test_planar_region_data_roundtrip(region):
    data = json.loads(json.dumps(region.__data__))
    reconstructed = PlanarRegion.__from_data__(data)

    assert reconstructed == region


def test_planar_region_transformation(region):
    region.transform(Translation.from_vector([1, 2, 3]))

    assert region.outer.points[0] == [1, 2, 3]
    assert region.holes[0].points[0] == [2, 3, 3]
    assert region.area() == pytest.approx(12.0)


def test_planar_region_rejects_non_coplanar_boundaries():
    with pytest.raises(ValueError, match="coplanar"):
        PlanarRegion(
            [[0, 0, 0], [4, 0, 0], [4, 4, 0], [0, 4, 0]],
            holes=[[[1, 1, 1], [1, 3, 1], [3, 3, 1], [3, 1, 1]]],
        )


def test_planar_region_rejects_short_boundaries():
    with pytest.raises(ValueError, match="at least three"):
        PlanarRegion([[0, 0, 0], [1, 0, 0]])


def test_planar_region_defers_topology_validation_until_tessellation():
    region = PlanarRegion([[0, 0, 0], [2, 2, 0], [0, 2, 0], [2, 0, 0]])

    assert len(region.outer) == 4
    with pytest.raises(ValueError, match="self-intersecting"):
        region.to_vertices_and_faces()


@pytest.mark.parametrize(
    "hole",
    [
        [[5, 1, 0], [6, 1, 0], [6, 2, 0], [5, 2, 0]],
        [[0, 1, 0], [1, 1, 0], [1, 2, 0], [0, 2, 0]],
        [[3, 1, 0], [5, 1, 0], [5, 2, 0], [3, 2, 0]],
    ],
)
def test_planar_region_rejects_holes_not_strictly_inside_outer_boundary(hole):
    region = PlanarRegion(
        [[0, 0, 0], [4, 0, 0], [4, 4, 0], [0, 4, 0]],
        holes=[hole],
    )

    with pytest.raises(ValueError, match="strictly inside"):
        region.to_vertices_and_faces()


@pytest.mark.parametrize(
    "second_hole",
    [
        [[2, 2, 0], [3.5, 2, 0], [3.5, 3.5, 0], [2, 3.5, 0]],
        [[2, 1, 0], [3, 1, 0], [3, 2, 0], [2, 2, 0]],
        [[1.25, 1.25, 0], [1.75, 1.25, 0], [1.75, 1.75, 0], [1.25, 1.75, 0]],
    ],
)
def test_planar_region_rejects_overlapping_touching_and_nested_holes(second_hole):
    region = PlanarRegion(
        [[0, 0, 0], [5, 0, 0], [5, 5, 0], [0, 5, 0]],
        holes=[
            [[1, 1, 0], [3, 1, 0], [3, 3, 0], [1, 3, 0]],
            second_hole,
        ],
    )

    with pytest.raises(ValueError, match="must not overlap, touch, or contain"):
        region.to_vertices_and_faces()


def test_planar_region_rejects_repeated_nonconsecutive_vertices():
    region = PlanarRegion([[0, 0, 0], [3, 0, 0], [3, 3, 0], [0, 3, 0], [3, 0, 0]])

    with pytest.raises(ValueError, match="duplicate vertices"):
        region.to_vertices_and_faces()
