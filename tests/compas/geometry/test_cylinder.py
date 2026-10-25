import pytest
from compas.geometry import Circle
from compas.geometry import Cylinder
from compas.geometry import Frame
from compas.geometry import Line
from compas.geometry import Point


@pytest.fixture
def cylinder():
    return Cylinder(radius=0.3, height=1.6)


def test_cylinder_discretization(cylinder):
    # just checking these don't break. Could not quickly find a formula that worked to test the actual values
    # as function of the resolution
    vertices, faces = cylinder.to_vertices_and_faces()
    assert vertices
    assert faces


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


def test_cylinder_requires_positive_dimensions():
    with pytest.raises(ValueError):
        Cylinder(0.0, 1.0)
    with pytest.raises(ValueError):
        Cylinder(1.0, 0.0)


def test_cylinder_axis_spans_full_height():
    cylinder = Cylinder.from_line_and_radius(Line([1.0, 2.0, 3.0], [1.0, 2.0, 7.0]), 2.0)

    assert cylinder.axis.start == Point(1.0, 2.0, 3.0)
    assert cylinder.axis.end == Point(1.0, 2.0, 7.0)
    assert cylinder.base == cylinder.axis.start
    assert cylinder.circle.center == cylinder.base


def test_cylinder_from_circle_uses_circle_as_lower_base():
    circle = Circle(2.0, frame=Frame([1.0, 2.0, 3.0], [0.0, 1.0, 0.0], [-1.0, 0.0, 0.0]))
    cylinder = Cylinder.from_circle_and_height(circle, 4.0)

    assert cylinder.circle == circle
    assert cylinder.axis.start == circle.center
    assert cylinder.axis.length == 4.0


def test_cylinder_contains_points_in_arbitrary_frame():
    frame = Frame([10.0, 20.0, 30.0], [0.0, 1.0, 0.0], [-1.0, 0.0, 0.0])
    cylinder = Cylinder(2.0, 4.0, frame=frame)
    local = [[0.0, 0.0, 0.0], [1.5, 0.0, 2.0], [2.5, 0.0, 0.0], [0.0, 0.0, 3.0]]
    points = [frame.to_world_coordinates(point) for point in local]

    assert cylinder.contains_points(points) == [True, True, False, False]


def test_cylinder_faces_do_not_compute_vertices(monkeypatch):
    cylinder = Cylinder(1.0, 2.0)

    def fail():
        raise AssertionError("Topology computation should not regenerate positions.")

    monkeypatch.setattr(cylinder, "compute_vertices", fail)
    assert cylinder.compute_faces()


def test_cylinder_bounds_are_invalidated():
    cylinder = Cylinder(1.0, 2.0)
    initial = cylinder.aabb
    cylinder.radius = 2.0

    assert cylinder.aabb is not initial
    assert cylinder.aabb.xsize == pytest.approx(4.0)
