import pytest

from compas.geometry import Torus


@pytest.fixture
def torus():
    return Torus(radius_axis=10.0, radius_pipe=2.0)


def test_torus_discretization(torus):
    # just checking these don't break. Could not quickly find a formula that worked to test the actual values
    # as function of the resolution
    assert torus.edges
    assert torus.faces
    assert torus.vertices


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
