import pytest

from compas.geometry import Frame
from compas.geometry import Sphere


@pytest.fixture
def sphere():
    return Sphere(450.0, Frame.worldXY())


def test_sphere_discretization(sphere):
    expected_face_count = sphere.resolution_v * sphere.resolution_u
    expected_vertex_count = (sphere.resolution_v - 1) * sphere.resolution_u + 2
    expected_edge_count = expected_face_count * 2 - sphere.resolution_u

    assert len(sphere.edges) == expected_edge_count
    assert len(sphere.faces) == expected_face_count
    assert len(sphere.vertices) == expected_vertex_count


def test_sphere_scaled():
    """Test that Sphere.scaled() returns a scaled copy without modifying the original."""
    sphere = Sphere(radius=10.0)
    
    # Test uniform scaling
    scaled_sphere = sphere.scaled(0.5)
    
    # Original should be unchanged
    assert sphere.radius == 10.0
    
    # Scaled copy should have scaled radius
    assert scaled_sphere.radius == 5.0
    
    # Test scaling with factor > 1
    scaled_sphere_2 = sphere.scaled(2.0)
    assert scaled_sphere_2.radius == 20.0
    assert sphere.radius == 10.0  # Original still unchanged


def test_sphere_scale():
    """Test that Sphere.scale() modifies the sphere in place."""
    sphere = Sphere(radius=10.0)
    
    # Test uniform scaling
    sphere.scale(0.5)
    
    # Sphere should be modified
    assert sphere.radius == 5.0

