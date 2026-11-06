import pytest

from compas.geometry import Frame
from compas.geometry import Point
from compas.geometry import Sphere


@pytest.fixture
def sphere():
    return Sphere(450.0, Frame.worldXY())


def test_sphere_discretization(sphere):
    u = 16
    v = 16
    expected_face_count = v * u
    expected_vertex_count = (v - 1) * u + 2
    surface = sphere.to_polygonal_surface(nu=u, nv=v)

    assert len(surface.faces) == expected_face_count
    assert len(surface.vertices) == expected_vertex_count


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

    monkeypatch.setattr(sphere, "_compute_local_vertices", fail)
    assert sphere._compute_faces((6, 4))


def test_sphere_bounds_are_invalidated():
    sphere = Sphere(1.0)
    initial = sphere.aabb
    sphere.radius = 2.0

    assert sphere.aabb is not initial
    assert sphere.aabb.xsize == pytest.approx(4.0)


def test_sphere_rejects_nonuniform_scaling():
    sphere = Sphere(1.0)

    with pytest.raises(ValueError):
        sphere.scale(2.0, 1.0, 2.0)
