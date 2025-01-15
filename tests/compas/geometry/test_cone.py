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
