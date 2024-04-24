import json
import compas

from compas.tolerance import TOL
from compas.geometry import Circle
from compas.geometry import Frame
from compas.geometry import Plane


def test_circle_create():
    circle = Circle(radius=1.0)

    assert TOL.is_close(circle.radius, 1.0)
    assert TOL.is_close(circle.area, 3.141592653589793)
    assert TOL.is_close(circle.circumference, 6.283185307179586)
    assert TOL.is_close(circle.diameter, 2.0)

    assert circle.is_closed
    assert circle.is_periodic

    assert circle.frame == Frame.worldXY()

    assert TOL.is_allclose(circle.point_at(0.0), [1.0, 0.0, 0.0])
    assert TOL.is_allclose(circle.point_at(0.25), [0.0, 1.0, 0.0])
    assert TOL.is_allclose(circle.point_at(0.5), [-1.0, 0.0, 0.0])
    assert TOL.is_allclose(circle.point_at(0.75), [0.0, -1.0, 0.0])
    assert TOL.is_allclose(circle.point_at(1.0), [1.0, 0.0, 0.0])


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

    if not compas.IPY:
        assert Circle.validate_data(circle.__data__)
        assert Circle.validate_data(other.__data__)


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
    pass


def test_circle_create_from_points():
    pass


# =============================================================================
# Properties and Geometry
# =============================================================================


def test_circle_geometry():
    pass


def test_circle_properties():
    pass


# =============================================================================
# Accessors
# =============================================================================

# =============================================================================
# Comparison
# =============================================================================

# =============================================================================
# Other Methods
# =============================================================================
