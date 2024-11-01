import pytest

from compas.geometry import Frame
from compas.geometry import Sphere


@pytest.fixture
def sphere():
    return Sphere(450.0, Frame.worldXY())


def test_sphere_discretization(sphere):
    assert len(sphere.edges) == 496
    assert len(sphere.faces) == 256
    assert len(sphere.vertices) == 242
