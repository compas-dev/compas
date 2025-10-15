import pytest
from compas.geometry import Cylinder


@pytest.fixture
def cylinder():
    return Cylinder(radius=0.3, height=1.6)


def test_cylinder_discretization(cylinder):
    # just checking these don't break. Could not quickly find a formula that worked to test the actual values
    # as function of the resolution
    assert cylinder.edges
    assert cylinder.faces
    assert cylinder.vertices


def test_cylinder_scaled():
    """Test that Cylinder.scaled() returns a scaled copy without modifying the original."""
    cylinder = Cylinder(radius=5.0, height=10.0)
    
    # Test uniform scaling
    scaled_cylinder = cylinder.scaled(0.5)
    
    # Original should be unchanged
    assert cylinder.radius == 5.0
    assert cylinder.height == 10.0
    
    # Scaled copy should have scaled dimensions
    assert scaled_cylinder.radius == 2.5
    assert scaled_cylinder.height == 5.0
    
    # Test scaling with factor > 1
    scaled_cylinder_2 = cylinder.scaled(2.0)
    assert scaled_cylinder_2.radius == 10.0
    assert scaled_cylinder_2.height == 20.0
    assert cylinder.radius == 5.0  # Original still unchanged
    assert cylinder.height == 10.0


def test_cylinder_scale():
    """Test that Cylinder.scale() modifies the cylinder in place."""
    cylinder = Cylinder(radius=5.0, height=10.0)
    
    # Test uniform scaling
    cylinder.scale(0.5)
    
    # Cylinder should be modified
    assert cylinder.radius == 2.5
    assert cylinder.height == 5.0

