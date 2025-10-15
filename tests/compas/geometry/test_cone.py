import pytest

from compas.geometry import Cone


@pytest.fixture
def cone():
    return Cone(432.0, 123.0)


def test_cone_discretization(cone):
    # just checking these don't break. Could not quickly find a formula that worked to test the actual values
    # as function of the resolution
    assert cone.edges
    assert cone.faces
    assert cone.vertices


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

