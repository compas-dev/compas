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
