import json

import pytest

from compas.tolerance import TOL
from compas.geometry import Circle
from compas.geometry import Frame
from compas.geometry import Plane


def test_circle_create():
    circle = Circle(radius=1.0)

    assert TOL.is_close(circle.radius, 1.0)
    assert TOL.is_close(circle.area, 3.141592653589793)
    assert TOL.is_close(circle.circumference, 6.283185307179586)
    assert TOL.is_close(circle.length, circle.circumference)
    assert TOL.is_close(circle.diameter, 2.0)

    assert circle.is_closed
    assert circle.is_periodic

    assert circle.frame == Frame.worldXY()

    assert TOL.is_allclose(circle.point_at(0.0), [1.0, 0.0, 0.0])
    assert TOL.is_allclose(circle.point_at(0.25), [0.0, 1.0, 0.0])
    assert TOL.is_allclose(circle.point_at(0.5), [-1.0, 0.0, 0.0])
    assert TOL.is_allclose(circle.point_at(0.75), [0.0, -1.0, 0.0])
    assert TOL.is_allclose(circle.point_at(1.0), [1.0, 0.0, 0.0])


@pytest.mark.parametrize("radius", [0.0, -1.0])
def test_circle_rejects_nonpositive_radius(radius):
    with pytest.raises(ValueError, match="positive"):
        Circle(radius=radius)

    circle = Circle(radius=1.0)
    with pytest.raises(ValueError, match="positive"):
        circle.radius = radius


def test_circle_create_with_frame():
    circle = Circle(radius=1.0, frame=Frame.worldZX())

    assert TOL.is_close(circle.radius, 1.0)
    assert TOL.is_close(circle.area, 3.141592653589793)
    assert TOL.is_close(circle.circumference, 6.283185307179586)
    assert TOL.is_close(circle.diameter, 2.0)

    assert circle.is_closed
    assert circle.is_periodic

    assert circle.frame == Frame.worldZX()

    assert TOL.is_allclose(circle.point_at(0.0, world=False), [1.0, 0.0, 0.0])
    assert TOL.is_allclose(circle.point_at(0.25, world=False), [0.0, 1.0, 0.0])
    assert TOL.is_allclose(circle.point_at(0.5, world=False), [-1.0, 0.0, 0.0])
    assert TOL.is_allclose(circle.point_at(0.75, world=False), [0.0, -1.0, 0.0])
    assert TOL.is_allclose(circle.point_at(1.0, world=False), [1.0, 0.0, 0.0])

    assert TOL.is_allclose(circle.point_at(0.0, world=True), [0.0, 0.0, 1.0])
    assert TOL.is_allclose(circle.point_at(0.25, world=True), [1.0, 0.0, 0.0])
    assert TOL.is_allclose(circle.point_at(0.5, world=True), [0.0, 0.0, -1.0])
    assert TOL.is_allclose(circle.point_at(0.75, world=True), [-1.0, 0.0, 0.0])
    assert TOL.is_allclose(circle.point_at(1.0, world=True), [0.0, 0.0, 1.0])

    assert TOL.is_allclose(
        circle.point_at(0.0, world=True),
        circle.point_at(0.0, world=False).transformed(circle.transformation),
    )
    assert TOL.is_allclose(
        circle.point_at(0.25, world=True),
        circle.point_at(0.25, world=False).transformed(circle.transformation),
    )
    assert TOL.is_allclose(
        circle.point_at(0.5, world=True),
        circle.point_at(0.5, world=False).transformed(circle.transformation),
    )
    assert TOL.is_allclose(
        circle.point_at(0.75, world=True),
        circle.point_at(0.75, world=False).transformed(circle.transformation),
    )
    assert TOL.is_allclose(
        circle.point_at(1.0, world=True),
        circle.point_at(1.0, world=False).transformed(circle.transformation),
    )


# =============================================================================
# Data
# =============================================================================


def test_circle_data():
    circle = Circle(radius=1.0)
    other = Circle.__from_data__(json.loads(json.dumps(circle.__data__)))

    assert circle.radius == other.radius
    assert circle.frame.point == other.frame.point
    assert TOL.is_allclose(circle.frame.xaxis, other.frame.xaxis)
    assert TOL.is_allclose(circle.frame.yaxis, other.frame.yaxis)


# =============================================================================
# Constructors
# =============================================================================


def test_circle_create_from_point_and_radius():
    circle = Circle.from_point_and_radius([1.0, 2.0, 3.0], 1.0)

    assert TOL.is_close(circle.radius, 1.0)
    assert TOL.is_close(circle.area, 3.141592653589793)
    assert TOL.is_close(circle.circumference, 6.283185307179586)
    assert TOL.is_close(circle.diameter, 2.0)

    assert circle.is_closed
    assert circle.is_periodic

    assert TOL.is_allclose(circle.frame.point, [1, 2, 3])
    assert TOL.is_allclose(circle.frame.xaxis, Frame.worldXY().xaxis)
    assert TOL.is_allclose(circle.frame.yaxis, Frame.worldXY().yaxis)
    assert TOL.is_allclose(circle.frame.zaxis, Frame.worldXY().zaxis)


def test_circle_create_from_plane_and_radius():
    plane = Plane([1.0, 2.0, 3.0], [0.0, 0.0, 1.0])
    frame = Frame.from_plane(plane)
    circle = Circle.from_plane_and_radius(plane, 1.0)

    assert TOL.is_close(circle.radius, 1.0)
    assert TOL.is_close(circle.area, 3.141592653589793)
    assert TOL.is_close(circle.circumference, 6.283185307179586)
    assert TOL.is_close(circle.diameter, 2.0)

    assert circle.is_closed
    assert circle.is_periodic

    assert TOL.is_allclose(circle.frame.point, [1, 2, 3])
    assert TOL.is_allclose(circle.frame.xaxis, frame.xaxis)
    assert TOL.is_allclose(circle.frame.yaxis, frame.yaxis)
    assert TOL.is_allclose(circle.frame.zaxis, frame.zaxis)


def test_circle_create_from_three_points():
    circle = Circle.from_three_points([1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [-1.0, 0.0, 0.0])

    assert TOL.is_allclose(circle.center, [0.0, 0.0, 0.0])
    assert TOL.is_close(circle.radius, 1.0)


def test_circle_create_from_points():
    circle = Circle.from_points([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [-1.0, 0.0, 0.0]])

    assert TOL.is_allclose(circle.center, [0.0, 0.0, 0.0])
    assert TOL.is_close(circle.radius, 1.0)


def test_circle_constructors_preserve_subclass():
    class CustomCircle(Circle):
        pass

    assert isinstance(CustomCircle.from_point_and_radius([0.0, 0.0, 0.0], 1.0), CustomCircle)
    assert isinstance(CustomCircle.from_plane_and_radius(Plane.worldXY(), 1.0), CustomCircle)
    assert isinstance(CustomCircle.from_three_points([1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [-1.0, 0.0, 0.0]), CustomCircle)
    assert isinstance(CustomCircle.from_points([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [-1.0, 0.0, 0.0]]), CustomCircle)


# =============================================================================
# Properties and Geometry
# =============================================================================


def test_circle_geometry():
    circle = Circle(radius=2.0)

    assert TOL.is_allclose(circle.normal_at(0.0, world=False), [-1.0, 0.0, 0.0])
    assert TOL.is_close(circle.normal_at(0.0, world=False).length, 1.0)
    assert TOL.is_close(circle.normal_at(0.0, world=True).length, 1.0)
    assert TOL.is_close(circle.tangent_at(0.0, world=False).length, 1.0)


def test_circle_properties():
    circle = Circle(radius=1.0)
    source = [1.0, 2.0, 3.0]
    circle.center = source
    source[0] = 4.0

    assert TOL.is_allclose(circle.center, [1.0, 2.0, 3.0])
    assert circle.eccentricity == 0.0


def test_circle_comparison():
    circle = Circle(radius=1.0)

    assert circle == Circle(radius=1.0)
    assert circle != Circle(radius=2.0)
    assert circle != object()


def test_circle_closest_point():
    circle = Circle(radius=1.0)

    point, parameter = circle.closest_point([0.0, 2.0, 3.0], return_parameter=True)
    assert TOL.is_allclose(point, [0.0, 1.0, 0.0])
    assert TOL.is_close(parameter, 0.25)
    assert TOL.is_allclose(circle.closest_point([0.0, 0.0, 0.0]), [1.0, 0.0, 0.0])


def test_circle_contains_point():
    circle = Circle(radius=1.0)

    assert circle.contains_point([1.0, 0.0, 0.0])
    assert circle.contains_point([1.0, 0.0, 0.5e-6])
    assert not circle.contains_point([1.0, 0.0, 2e-6])
    assert not circle.contains_point([0.0, 0.0, 0.0])
    assert not circle.contains_point([2.0, 0.0, 0.0])


def test_circle_rejects_2d_constructor_inputs():
    with pytest.raises(IndexError):
        Circle.from_three_points([1.0, 0.0], [0.0, 1.0, 0.0], [-1.0, 0.0, 0.0])


# =============================================================================
# Accessors
# =============================================================================

# =============================================================================
# Comparison
# =============================================================================

# =============================================================================
# Other Methods
# =============================================================================
