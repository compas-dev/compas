import pytest

from compas.geometry import Frame
from compas.geometry import Point
from compas.geometry import Sphere


@pytest.fixture
def sphere():
    return Sphere(450.0, Frame.worldXY())


def test_sphere_discretization(sphere):
    expected_face_count = sphere.resolution_v * sphere.resolution_u
    expected_vertex_count = (sphere.resolution_v - 1) * sphere.resolution_u + 2
    vertices, faces = sphere.to_vertices_and_faces()

    assert len(faces) == expected_face_count
    assert len(vertices) == expected_vertex_count


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


def test_sphere_requires_positive_radius():
    with pytest.raises(ValueError):
        Sphere(0.0)


def test_sphere_from_point_and_radius():
    class CustomSphere(Sphere):
        pass

    sphere = CustomSphere.from_point_and_radius([1.0, 2.0, 3.0], 4.0)

    assert isinstance(sphere, CustomSphere)
    assert sphere.base == Point(1.0, 2.0, 3.0)
    assert sphere.radius == 4.0
    assert sphere.circle.center == sphere.base
    assert sphere.circle.radius == sphere.radius


def test_sphere_faces_do_not_compute_vertices(monkeypatch):
    sphere = Sphere(1.0)

    def fail():
        raise AssertionError("Topology computation should not regenerate positions.")

    monkeypatch.setattr(sphere, "compute_vertices", fail)
    assert sphere.compute_faces()


def test_sphere_bounds_are_invalidated():
    sphere = Sphere(1.0)
    initial = sphere.aabb()
    sphere.radius = 2.0

    assert sphere.aabb() is not initial
    assert sphere.aabb().xsize == pytest.approx(4.0)


def test_sphere_rejects_nonuniform_scaling():
    sphere = Sphere(1.0)

    with pytest.raises(ValueError):
        sphere.scale(2.0, 1.0, 2.0)
