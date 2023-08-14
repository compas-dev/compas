import math
import json
import pytest
import compas

from compas.geometry import Arc
from compas.geometry import Point  # noqa: F401
from compas.geometry import Vector  # noqa: F401
from compas.geometry import Frame
from compas.geometry import Circle
from compas.geometry import close, allclose


@pytest.fixture
def frame():
    return Frame([1.23, 0.44, -4.02], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0])


def test_arc_create():
    arc = Arc(radius=1.0, start_angle=0.0, end_angle=math.pi)

    assert close(arc.radius, 1.0)
    assert close(arc.angle, math.pi)
    assert close(arc.start_angle, 0.0)
    assert close(arc.end_angle, math.pi)
    assert not arc.is_circle

    assert allclose(arc.point_at(0.0, world=True), [1.0, 0.0, 0.0], tol=1e-12)
    assert allclose(arc.point_at(0.5, world=True), [0.0, 1.0, 0.0], tol=1e-12)
    assert allclose(arc.point_at(1.0, world=True), [-1.0, 0.0, 0.0], tol=1e-12)
    assert allclose(arc.point_at(0.0, world=True), arc.point_at(0.0, world=False), tol=1e-12)
    assert allclose(arc.point_at(0.5, world=True), arc.point_at(0.5, world=False), tol=1e-12)
    assert allclose(arc.point_at(1.0, world=True), arc.point_at(1.0, world=False), tol=1e-12)

    other = eval(repr(arc))
    assert arc.radius == other.radius
    assert arc.start_angle == other.start_angle
    assert arc.end_angle == other.end_angle
    assert arc.frame.point == other.frame.point
    assert allclose(arc.frame.xaxis, other.frame.xaxis, tol=1e-12)
    assert allclose(arc.frame.yaxis, other.frame.yaxis, tol=1e-12)


def test_arc_create_with_frame(frame):
    arc = Arc(radius=0.2, start_angle=0.0, end_angle=1.14, frame=frame)

    assert close(arc.radius, 0.2)
    assert close(arc.angle, 1.14)
    assert close(arc.start_angle, 0.0)
    assert close(arc.end_angle, 1.14)
    assert not arc.is_circle

    other = eval(repr(arc))
    assert arc.radius == other.radius
    assert arc.start_angle == other.start_angle
    assert arc.end_angle == other.end_angle
    assert arc.frame.point == other.frame.point
    assert allclose(arc.frame.xaxis, other.frame.xaxis, tol=1e-12)
    assert allclose(arc.frame.yaxis, other.frame.yaxis, tol=1e-12)

    assert not allclose(
        arc.point_at(0.0, world=True),
        arc.point_at(0.0, world=False),
        tol=1e-12,
    )
    assert not allclose(
        arc.point_at(0.5, world=True),
        arc.point_at(0.5, world=False),
        tol=1e-12,
    )
    assert not allclose(
        arc.point_at(1.0, world=True),
        arc.point_at(1.0, world=False),
        tol=1e-12,
    )

    assert allclose(
        arc.point_at(0.0, world=True),
        arc.point_at(0.0, world=False).transformed(arc.transformation),
        tol=1e-12,
    )
    assert allclose(
        arc.point_at(0.5, world=True),
        arc.point_at(0.5, world=False).transformed(arc.transformation),
        tol=1e-12,
    )
    assert allclose(
        arc.point_at(1.0, world=True),
        arc.point_at(1.0, world=False).transformed(arc.transformation),
        tol=1e-12,
    )


def test_arc_create_invalid():
    with pytest.raises(ValueError):
        Arc(radius=1.0, start_angle=0.2314, end_angle=7.14)


# =============================================================================
# Data
# =============================================================================


def test_arc_data():
    arc = Arc(radius=1.0, start_angle=0.0, end_angle=math.pi)
    other = Arc.from_data(json.loads(json.dumps(arc.data)))

    assert arc.radius == other.radius
    assert arc.start_angle == other.start_angle
    assert arc.end_angle == other.end_angle
    assert arc.frame.point == other.frame.point
    assert allclose(arc.frame.xaxis, other.frame.xaxis, tol=1e-12)
    assert allclose(arc.frame.yaxis, other.frame.yaxis, tol=1e-12)

    if not compas.IPY:
        assert Arc.validate_data(arc.data)
        assert Arc.validate_data(other.data)


# =============================================================================
# Constructors
# =============================================================================


def test_arc_create_from_circle(frame):
    circle = Circle(radius=34.222, frame=frame)
    arc = Arc.from_circle(circle, 0.1, 0.443)

    assert close(arc.radius, circle.radius)
    assert close(arc.start_angle, 0.1)
    assert close(arc.end_angle, 0.443)
    assert close(arc.angle, 0.443 - 0.1)
    assert close(arc.circumference, circle.circumference)
    assert close(arc.diameter, circle.diameter)
    assert not arc.is_circle

    assert allclose(arc.center, circle.center)
    assert allclose(arc.frame, circle.frame)


def test_arc_create_from_full_circle(frame):
    circle = Circle(radius=34.222, frame=frame)
    arc = Arc.from_circle(circle, 0.0, 2.0 * math.pi)

    assert close(arc.radius, circle.radius)
    assert close(arc.start_angle, 0.0)
    assert close(arc.end_angle, 2.0 * math.pi)
    assert close(arc.angle, 2.0 * math.pi)
    assert close(arc.circumference, circle.circumference)
    assert close(arc.diameter, circle.diameter)
    assert arc.is_circle

    assert allclose(arc.center, circle.center)
    assert allclose(arc.frame, circle.frame)


# =============================================================================
# Properties and Geometry
# =============================================================================


def test_arc_properties():
    arc = Arc(radius=1.0, start_angle=0.0, end_angle=math.pi)

    assert close(arc.radius, 1.0)
    assert close(arc.start_angle, 0.0)
    assert close(arc.end_angle, math.pi)

    arc._radius = None
    arc._end_angle = None

    with pytest.raises(ValueError):
        arc.radius

    with pytest.raises(ValueError):
        arc.end_angle


def test_arc_geometry():
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
