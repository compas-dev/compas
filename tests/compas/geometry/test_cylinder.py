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
