import pytest

from compas.geometry import Torus
from compas.geometry import Frame


@pytest.fixture
def torus():
    return Torus(radius_axis=10.0, radius_pipe=2.0)


def test_torus_discretization(torus):
    # just checking these don't break. Could not quickly find a formula that worked to test the actual values
    # as function of the resolution
    vertices, faces = torus.to_vertices_and_faces()
    assert vertices
    assert faces


def test_torus_scaled():
    """Test that Torus.scaled() returns a scaled copy without modifying the original."""
    torus = Torus(radius_axis=10.0, radius_pipe=2.0)

    # Test uniform scaling
    scaled_torus = torus.scaled(0.5)

    # Original should be unchanged
    assert torus.radius_axis == 10.0
    assert torus.radius_pipe == 2.0

    # Scaled copy should have scaled dimensions
    assert scaled_torus.radius_axis == 5.0
    assert scaled_torus.radius_pipe == 1.0

    # Test scaling with factor > 1
    scaled_torus_2 = torus.scaled(2.0)
    assert scaled_torus_2.radius_axis == 20.0
    assert scaled_torus_2.radius_pipe == 4.0
    assert torus.radius_axis == 10.0  # Original still unchanged
    assert torus.radius_pipe == 2.0


def test_torus_scale():
    """Test that Torus.scale() modifies the torus in place."""
    torus = Torus(radius_axis=10.0, radius_pipe=2.0)

    # Test uniform scaling
    torus.scale(0.5)

    # Torus should be modified
    assert torus.radius_axis == 5.0
    assert torus.radius_pipe == 1.0


def test_torus_requires_ring_torus_radii():
    with pytest.raises(ValueError):
        Torus(0.0, 1.0)
    with pytest.raises(ValueError):
        Torus(2.0, 2.0)
    with pytest.raises(ValueError):
        Torus(2.0, 3.0)


def test_torus_can_scale_down_atomically():
    torus = Torus(10.0, 2.0)
    torus.scale(0.1)

    assert torus.radius_axis == 1.0
    assert torus.radius_pipe == 0.2


def test_torus_contains_points_in_arbitrary_frame():
    frame = Frame([10.0, 20.0, 30.0], [0.0, 1.0, 0.0], [-1.0, 0.0, 0.0])
    torus = Torus(5.0, 2.0, frame=frame)
    local = [[5.0, 0.0, 0.0], [6.9, 0.0, 0.0], [0.0, 0.0, 0.0], [8.0, 0.0, 0.0]]
    points = [frame.to_world_coordinates(point) for point in local]

    assert torus.contains_points(points) == [True, True, False, False]


def test_torus_bounds_are_invalidated():
    torus = Torus(5.0, 2.0)
    initial = torus.aabb
    torus.radius_axis = 6.0

    assert torus.aabb is not initial
    assert torus.aabb.xsize == pytest.approx(16.0)
