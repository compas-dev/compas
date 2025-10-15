import pytest

from compas.geometry import Capsule


@pytest.fixture
def capsule():
    return Capsule(123.0, 13.0)


def test_capsule_discretization(capsule):
    # just checking these don't break. Could not quickly find a formula that worked to test the actual values
    # as function of the resolution
    assert capsule.edges
    assert capsule.faces
    assert capsule.vertices


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

