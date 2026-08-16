import math
import json
import pytest
from compas.geometry import Arc
from compas.geometry import Frame
from compas.geometry import Circle
from compas.geometry import Point  # noqa: F401
from compas.geometry import Vector  # noqa: F401
from compas.tolerance import TOL


@pytest.fixture
def frame():
    return Frame([1.23, 0.44, -4.02], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0])


def test_arc_create():
    arc = Arc(radius=1.0, start_angle=0.0, end_angle=math.pi)

    assert TOL.is_close(arc.radius, 1.0)
    assert TOL.is_close(arc.angle, math.pi)
    assert TOL.is_close(arc.start_angle, 0.0)
    assert TOL.is_close(arc.end_angle, math.pi)
    assert not arc.is_circle

    assert TOL.is_allclose(arc.point_at(0.0, world=True), [1.0, 0.0, 0.0])
    assert TOL.is_allclose(arc.point_at(0.5, world=True), [0.0, 1.0, 0.0])
    assert TOL.is_allclose(arc.point_at(1.0, world=True), [-1.0, 0.0, 0.0])
    assert TOL.is_allclose(arc.point_at(0.0, world=True), arc.point_at(0.0, world=False))
    assert TOL.is_allclose(arc.point_at(0.5, world=True), arc.point_at(0.5, world=False))
    assert TOL.is_allclose(arc.point_at(1.0, world=True), arc.point_at(1.0, world=False))

    other = eval(repr(arc))
    assert arc.radius == other.radius
    assert TOL.is_close(arc.start_angle, other.start_angle)
    assert TOL.is_close(arc.end_angle, other.end_angle)
    assert arc.frame.point == other.frame.point
    assert TOL.is_allclose(arc.frame.xaxis, other.frame.xaxis)
    assert TOL.is_allclose(arc.frame.yaxis, other.frame.yaxis)


def test_arc_create_with_frame(frame):
    arc = Arc(radius=0.2, start_angle=0.0, end_angle=1.14, frame=frame)

    assert TOL.is_close(arc.radius, 0.2)
    assert TOL.is_close(arc.angle, 1.14)
    assert TOL.is_close(arc.start_angle, 0.0)
    assert TOL.is_close(arc.end_angle, 1.14)
    assert not arc.is_circle

    other = eval(repr(arc))
    assert arc.radius == other.radius
    assert TOL.is_close(arc.start_angle, other.start_angle)
    assert TOL.is_close(arc.end_angle, other.end_angle)
    assert arc.frame.point == other.frame.point
    assert TOL.is_allclose(arc.frame.xaxis, other.frame.xaxis)
    assert TOL.is_allclose(arc.frame.yaxis, other.frame.yaxis)

    assert not TOL.is_allclose(
        arc.point_at(0.0, world=True),
        arc.point_at(0.0, world=False),
    )
    assert not TOL.is_allclose(
        arc.point_at(0.5, world=True),
        arc.point_at(0.5, world=False),
    )
    assert not TOL.is_allclose(
        arc.point_at(1.0, world=True),
        arc.point_at(1.0, world=False),
    )

    assert TOL.is_allclose(
        arc.point_at(0.0, world=True),
        arc.point_at(0.0, world=False).transformed(arc.transformation),
    )
    assert TOL.is_allclose(
        arc.point_at(0.5, world=True),
        arc.point_at(0.5, world=False).transformed(arc.transformation),
    )
    assert TOL.is_allclose(
        arc.point_at(1.0, world=True),
        arc.point_at(1.0, world=False).transformed(arc.transformation),
    )


def test_arc_create_invalid():
    with pytest.raises(ValueError):
        Arc(radius=1.0, start_angle=0.2314, end_angle=7.14)


@pytest.mark.parametrize("radius", [0.0, -1.0])
def test_arc_rejects_nonpositive_radius(radius):
    with pytest.raises(ValueError, match="positive"):
        Arc(radius=radius, start_angle=0.0, end_angle=math.pi)

    arc = Arc(radius=1.0, start_angle=0.0, end_angle=math.pi)
    with pytest.raises(ValueError, match="positive"):
        arc.radius = radius


def test_arc_comparison():
    arc = Arc(radius=1.0, start_angle=0.0, end_angle=math.pi)

    assert arc == Arc(radius=1.0, start_angle=0.0, end_angle=math.pi)
    assert arc != Arc(radius=2.0, start_angle=0.0, end_angle=math.pi)
    assert arc != object()


def test_arc_decreasing_angle_range_preserves_signed_sweep():
    arc = Arc(radius=2.0, start_angle=math.pi, end_angle=0.0)

    assert TOL.is_close(arc.angle, -math.pi)
    assert TOL.is_close(arc.length, 2.0 * math.pi)
    assert TOL.is_allclose(arc.point_at(0.5), [0.0, 2.0, 0.0])


@pytest.mark.parametrize(
    "arc, expected",
    [
        (Arc(radius=2.0, start_angle=0.0, end_angle=math.pi), [0.0, 1.0, 0.0]),
        (Arc(radius=2.0, start_angle=math.pi, end_angle=0.0), [0.0, 1.0, 0.0]),
    ],
)
def test_arc_tangent_is_unitized_and_follows_parameter_direction(arc, expected):
    tangent = arc.tangent_at(0.0)

    assert TOL.is_close(tangent.length, 1.0)
    assert TOL.is_allclose(tangent, expected)


def test_full_circle_arc_is_closed_and_periodic():
    arc = Arc(radius=1.0, start_angle=0.0, end_angle=2.0 * math.pi)

    assert arc.is_circle
    assert arc.is_closed
    assert arc.is_periodic


def test_arc_reverse_preserves_geometry_and_reverses_parameter_direction():
    arc = Arc(radius=2.0, start_angle=0.0, end_angle=math.pi)
    start = arc.point_at(0.0)
    end = arc.point_at(1.0)
    length = arc.length

    arc.reverse()

    assert arc.point_at(0.0) == end
    assert arc.point_at(1.0) == start
    assert TOL.is_close(arc.angle, -math.pi)
    assert TOL.is_close(arc.length, length)


def test_full_circle_arc_remains_closed_after_reverse():
    arc = Arc(radius=1.0, start_angle=0.0, end_angle=2.0 * math.pi)

    arc.reverse()

    assert arc.is_circle
    assert arc.is_closed
    assert arc.is_periodic


def test_arc_from_circle_preserves_subclass(frame):
    class CustomArc(Arc):
        pass

    circle = Circle(radius=1.0, frame=frame)
    arc = CustomArc.from_circle(circle, 0.0, math.pi)

    assert isinstance(arc, CustomArc)
    assert arc.frame == circle.frame
    assert arc.frame is not circle.frame


# =============================================================================
# Data
# =============================================================================


def test_arc_data():
    arc = Arc(radius=1.0, start_angle=0.0, end_angle=math.pi)
    other = Arc.__from_data__(json.loads(json.dumps(arc.__data__)))

    assert arc.radius == other.radius
    assert TOL.is_close(arc.start_angle, other.start_angle)
    assert TOL.is_close(arc.end_angle, other.end_angle)
    assert arc.frame.point == other.frame.point
    assert TOL.is_allclose(arc.frame.xaxis, other.frame.xaxis)
    assert TOL.is_allclose(arc.frame.yaxis, other.frame.yaxis)


# =============================================================================
# Constructors
# =============================================================================


def test_arc_create_from_circle(frame):
    circle = Circle(radius=34.222, frame=frame)
    arc = Arc.from_circle(circle, 0.1, 0.443)

    assert TOL.is_close(arc.radius, circle.radius)
    assert TOL.is_close(arc.start_angle, 0.1)
    assert TOL.is_close(arc.end_angle, 0.443)
    assert TOL.is_close(arc.angle, 0.443 - 0.1)
    assert TOL.is_close(arc.circumference, circle.circumference)
    assert TOL.is_close(arc.diameter, circle.diameter)
    assert not arc.is_circle

    assert TOL.is_allclose(arc.center, circle.center)
    assert TOL.is_allclose(arc.frame, circle.frame)


def test_arc_create_from_full_circle(frame):
    circle = Circle(radius=34.222, frame=frame)
    arc = Arc.from_circle(circle, 0.0, 2.0 * math.pi)

    assert TOL.is_close(arc.radius, circle.radius)
    assert TOL.is_close(arc.start_angle, 0.0)
    assert TOL.is_close(arc.end_angle, 2.0 * math.pi)
    assert TOL.is_close(arc.angle, 2.0 * math.pi)
    assert TOL.is_close(arc.circumference, circle.circumference)
    assert TOL.is_close(arc.diameter, circle.diameter)
    assert arc.is_circle

    assert TOL.is_allclose(arc.center, circle.center)
    assert TOL.is_allclose(arc.frame, circle.frame)


# =============================================================================
# Properties and Geometry
# =============================================================================


def test_arc_properties():
    arc = Arc(radius=1.0, start_angle=0.0, end_angle=math.pi)

    assert TOL.is_close(arc.radius, 1.0)
    assert TOL.is_close(arc.start_angle, 0.0)
    assert TOL.is_close(arc.end_angle, math.pi)

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
