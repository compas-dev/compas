import pytest

from compas.geometry import Cone
from compas.geometry import Frame
from compas.geometry import Line


@pytest.fixture
def cone():
    return Cone(432.0, 123.0)


def test_cone_discretization(cone):
    # just checking these don't break. Could not quickly find a formula that worked to test the actual values
    # as function of the resolution
    vertices, faces = cone.to_vertices_and_faces()
    assert vertices
    assert faces


def test_cone_scaled():
    """Test that Cone.scaled() returns a scaled copy without modifying the original."""
    cone = Cone(radius=5.0, height=10.0)

    # Test uniform scaling
    scaled_cone = cone.scaled(0.5)

    # Original should be unchanged
    assert cone.radius == 5.0
    assert cone.height == 10.0

    # Scaled copy should have scaled dimensions
    assert scaled_cone.radius == 2.5
    assert scaled_cone.height == 5.0

    # Test scaling with factor > 1
    scaled_cone_2 = cone.scaled(2.0)
    assert scaled_cone_2.radius == 10.0
    assert scaled_cone_2.height == 20.0
    assert cone.radius == 5.0  # Original still unchanged
    assert cone.height == 10.0


def test_cone_scale():
    """Test that Cone.scale() modifies the cone in place."""
    cone = Cone(radius=5.0, height=10.0)

    # Test uniform scaling
    cone.scale(0.5)

    # Cone should be modified
    assert cone.radius == 2.5
    assert cone.height == 5.0


def test_cone_requires_positive_dimensions():
    with pytest.raises(ValueError):
        Cone(0.0, 1.0)
    with pytest.raises(ValueError):
        Cone(1.0, 0.0)


def test_cone_from_line_uses_line_start_as_base():
    line = Line([1.0, 2.0, 3.0], [1.0, 2.0, 7.0])
    cone = Cone.from_line_and_radius(line, 2.0)

    assert cone.axis.start == line.start
    assert cone.axis.end == line.end
    assert cone.circle.radius == 2.0


def test_cone_contains_points_in_arbitrary_frame():
    frame = Frame([10.0, 20.0, 30.0], [0.0, 1.0, 0.0], [-1.0, 0.0, 0.0])
    cone = Cone(2.0, 4.0, frame=frame)
    local = [[0.0, 0.0, 0.0], [0.5, 0.0, 2.0], [1.5, 0.0, 2.0], [0.0, 0.0, 5.0]]
    points = [frame.to_world_coordinates(point) for point in local]

    assert cone.contains_points(points) == [True, True, False, False]


def test_cone_faces_do_not_compute_vertices(monkeypatch):
    cone = Cone(1.0, 2.0)

    def fail():
        raise AssertionError("Topology computation should not regenerate positions.")

    monkeypatch.setattr(cone, "compute_vertices", fail)
    assert cone.compute_faces()


def test_cone_bounds_are_invalidated():
    cone = Cone(1.0, 2.0)
    initial = cone.aabb
    cone.radius = 2.0

    assert cone.aabb is not initial
    assert cone.aabb.xsize == pytest.approx(4.0)
