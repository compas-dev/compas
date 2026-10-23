import pytest

from compas.geometry import Capsule
from compas.geometry import Frame
from compas.geometry import Line


@pytest.fixture
def capsule():
    return Capsule(123.0, 13.0)


def test_capsule_discretization(capsule):
    # just checking these don't break. Could not quickly find a formula that worked to test the actual values
    # as function of the resolution
    vertices, faces = capsule.to_vertices_and_faces()
    assert vertices
    assert faces


def test_capsule_scaled():
    """Test that Capsule.scaled() returns a scaled copy without modifying the original."""
    capsule = Capsule(radius=5.0, height=10.0)

    # Test uniform scaling
    scaled_capsule = capsule.scaled(0.5)

    # Original should be unchanged
    assert capsule.radius == 5.0
    assert capsule.height == 10.0

    # Scaled copy should have scaled dimensions
    assert scaled_capsule.radius == 2.5
    assert scaled_capsule.height == 5.0

    # Test scaling with factor > 1
    scaled_capsule_2 = capsule.scaled(2.0)
    assert scaled_capsule_2.radius == 10.0
    assert scaled_capsule_2.height == 20.0
    assert capsule.radius == 5.0  # Original still unchanged
    assert capsule.height == 10.0


def test_capsule_scale():
    """Test that Capsule.scale() modifies the capsule in place."""
    capsule = Capsule(radius=5.0, height=10.0)

    # Test uniform scaling
    capsule.scale(0.5)

    # Capsule should be modified
    assert capsule.radius == 2.5
    assert capsule.height == 5.0


def test_capsule_constructors_and_circle():
    capsule = Capsule.from_line_and_radius(Line([1.0, 2.0, 3.0], [1.0, 2.0, 7.0]), 2.0)

    assert capsule.height == 4.0
    assert capsule.radius == 2.0
    assert capsule.circle.radius == 2.0
    assert capsule.circle.frame == capsule.frame


def test_capsule_contains_points_in_arbitrary_frame():
    frame = Frame([10.0, 20.0, 30.0], [0.0, 1.0, 0.0], [-1.0, 0.0, 0.0])
    capsule = Capsule(1.0, 4.0, frame=frame)
    points = [
        frame.to_world_coordinates([0.0, 0.0, 0.0]),
        frame.to_world_coordinates([0.0, 0.0, 2.5]),
        frame.to_world_coordinates([0.0, 0.0, 3.1]),
    ]

    assert capsule.contains_point(points[1])
    assert capsule.contains_points(points) == [True, True, False]


def test_capsule_faces_do_not_compute_vertices(monkeypatch):
    capsule = Capsule(1.0, 2.0)

    def fail():
        raise AssertionError("Topology computation should not regenerate positions.")

    monkeypatch.setattr(capsule, "compute_vertices", fail)
    assert capsule.compute_faces()


def test_capsule_bounds_are_invalidated():
    capsule = Capsule(1.0, 2.0)
    initial = capsule.aabb()
    capsule.radius = 2.0

    assert capsule.aabb() is not initial
    assert capsule.aabb().xsize == pytest.approx(4.0)
