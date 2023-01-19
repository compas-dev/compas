import math
import pytest

from compas.geometry import Arc
from compas.geometry import Frame
from compas.geometry import Plane
from compas.geometry import Circle
from compas.geometry import close


@pytest.fixture
def frame():
    return Frame([1.23, 0.44, -4.02], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0])


def test_create_arc(frame):
    arc = Arc(frame, 0.2, 1.14)

    assert close(arc.angle, 1.14)
    assert close(arc.start_angle, 0.0)


def test_create_arc_two_angles(frame):
    arc = Arc(frame, radius=8, start_angle=1.44, end_angle=3.14)

    assert close(arc.radius, 8.0)
    assert close(arc.angle, 1.7)
    assert close(arc.start_angle, 1.44)
    assert close(arc.end_angle, 3.14)
    assert not arc.is_circle


def test_create_from_circle(frame):
    circle = Circle(Plane(frame.point, frame.zaxis), 34.222)
    arc = Arc.from_circle(circle, 0.1, 0.443)

    assert close(arc.radius, circle.radius)
    assert close(arc.angle, 0.343)
    assert close(arc.circumference, circle.circumference)
    assert close(arc.diameter, circle.diameter)
    assert arc.center == circle.center


def test_create_from_circle_partial(frame):
    circle = Circle(Plane(frame.point, frame.zaxis), 34.222)
    arc = Arc.from_circle(circle, 0.1, 0.443)

    assert not arc.is_circle


def test_create_from_circle_full(frame):
    circle = Circle(Plane(frame.point, frame.zaxis), 34.222)
    arc = Arc.from_circle(circle, 0.0, 2.0 * math.pi)

    assert close(arc.start_angle, 0.0)
    assert close(arc.angle, 2.0 * math.pi)
    assert arc.is_circle


def test_create_invalid_arc(frame):
    with pytest.raises(ValueError):
        _ = Arc(frame, 0.2314, 7.14)
