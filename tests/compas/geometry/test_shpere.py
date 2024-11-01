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
