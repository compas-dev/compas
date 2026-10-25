import pytest
from compas.geometry import Box
from compas.geometry import Point


@pytest.fixture
def default_box():
    return Box(1.0, 2.0, 3.0)


@pytest.fixture
def unit_box():
    return Box(1.0)


def test_box_constructor(default_box):
    assert default_box.xsize == 1.0
    assert default_box.ysize == 2.0
    assert default_box.zsize == 3.0


def test_box_volume(default_box):
    assert default_box.volume() == 6.0


def test_box_area(default_box):
    assert default_box.area() == 22.0


def test_box_dimensions(default_box):
    assert default_box.dimensions == [1.0, 2.0, 3.0]


def test_box_corners(default_box):
    assert len(default_box.points) == 8


def test_box_corner(default_box):
    assert default_box.corner(0) == Point(-0.5, -1.0, -1.5)
    assert default_box.corner(1) == Point(-0.5, 1.0, -1.5)
    assert default_box.corner(2) == Point(0.5, 1.0, -1.5)
    assert default_box.corner(3) == Point(0.5, -1.0, -1.5)
    assert default_box.corner(4) == Point(-0.5, -1.0, 1.5)
    assert default_box.corner(5) == Point(0.5, -1.0, 1.5)
    assert default_box.corner(6) == Point(0.5, 1.0, 1.5)
    assert default_box.corner(7) == Point(-0.5, 1.0, 1.5)
    assert [default_box.corner(index) for index in range(8)] == default_box.points


def test_box_bounds_are_invalidated_when_dimensions_change(default_box):
    assert default_box.aabb.xsize == 1.0
    default_box.xsize = 4.0
    assert default_box.aabb.xsize == 4.0


def test_box_placement_preserves_local_discretization_and_topology(default_box, monkeypatch):
    vertices = default_box.vertices
    edges = default_box.edges
    faces = default_box.faces

    def fail_if_recomputed(u, v):
        raise AssertionError("local vertices should remain cached after a placement change")

    monkeypatch.setattr(default_box, "_compute_vertices", fail_if_recomputed)
    default_box.frame.point.x = 10.0

    assert default_box.vertices != vertices
    assert default_box.edges is edges
    assert default_box.faces is faces


def test_box_contains_point(default_box):
    assert default_box.contains_point(Point(0.0, 0.0, 0.0))
    assert not default_box.contains_point(Point(2.0, 2.0, 2.0))


def test_box_contains_points(default_box):
    points = [Point(0.0, 0.0, 0.0), Point(2.0, 2.0, 2.0)]
    results = default_box.contains_points(points)
    assert results == [True, False]


def test_box_from_width_height_depth():
    box = Box.from_width_height_depth(1.0, 2.0, 3.0)
    assert box.xsize == 1.0
    assert box.ysize == 3.0
    assert box.zsize == 2.0


def test_box_from_bounding_box():
    bbox = [
        Point(0.0, 0.0, 0.0),
        Point(1.0, 0.0, 0.0),
        Point(1.0, 1.0, 0.0),
        Point(0.0, 1.0, 0.0),
        Point(0.0, 0.0, 1.0),
        Point(1.0, 0.0, 1.0),
        Point(1.0, 1.0, 1.0),
        Point(0.0, 1.0, 1.0),
    ]
    box = Box.from_bounding_box(bbox)
    assert box.xsize == 1.0
    assert box.ysize == 1.0
    assert box.zsize == 1.0


def test_box_from_corner_corner_height():
    box = Box.from_corner_corner_height([0.0, 0.0, 0.0], [1.0, 1.0, 0.0], 1.0)
    assert box.xsize == 1.0
    assert box.ysize == 1.0
    assert box.zsize == 1.0


def test_box_from_diagonal():
    diagonal = [Point(0.0, 0.0, 0.0), Point(1.0, 1.0, 1.0)]
    box = Box.from_diagonal(diagonal)
    assert box.xsize == 1.0
    assert box.ysize == 1.0
    assert box.zsize == 1.0


def test_box_scale(default_box):
    default_box.scale(2.0)
    assert default_box.xsize == 2.0
    assert default_box.ysize == 4.0
    assert default_box.zsize == 6.0


def test_box_scaled(default_box):
    new_box = default_box.scaled(2.0, 4.0, 2.0)
    assert default_box.xsize == 1.0
    assert default_box.ysize == 2.0
    assert default_box.zsize == 3.0
    assert new_box.xsize == 2.0
    assert new_box.ysize == 8.0
    assert new_box.zsize == 6.0
