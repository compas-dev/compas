import pytest
import math
from compas.tolerance import TOL
from compas.geometry import Frame
from compas.geometry import Arc
from compas.geometry import Circle
from compas.geometry import Ellipse
from compas.geometry import Hyperbola
from compas.geometry import Line
from compas.geometry import Point


@pytest.mark.parametrize(
    "curve",
    [
        Arc(radius=1.0, start_angle=0, end_angle=math.pi, frame=Frame.worldZX()),
        Circle(radius=1.0, frame=Frame.worldZX()),
        Ellipse(major=1.0, minor=0.5, frame=Frame.worldZX()),
        Hyperbola(major=1.0, minor=0.5, frame=Frame.worldZX()),
    ],
)
def test_curve_geometry(curve):
    assert curve.frame == Frame.worldZX()

    if curve.is_closed:
        assert TOL.is_allclose(curve.point_at(0.0), curve.point_at(1.0))
    else:
        assert not TOL.is_allclose(curve.point_at(0.0), curve.point_at(1.0))

    assert TOL.is_allclose(
        curve.point_at(0.0, world=True),
        curve.point_at(0.0, world=False).transformed(curve.transformation),
    )
    assert TOL.is_allclose(
        curve.point_at(0.25, world=True),
        curve.point_at(0.25, world=False).transformed(curve.transformation),
    )
    assert TOL.is_allclose(
        curve.point_at(0.5, world=True),
        curve.point_at(0.5, world=False).transformed(curve.transformation),
    )
    assert TOL.is_allclose(
        curve.point_at(0.75, world=True),
        curve.point_at(0.75, world=False).transformed(curve.transformation),
    )
    assert TOL.is_allclose(
        curve.point_at(1.0, world=True),
        curve.point_at(1.0, world=False).transformed(curve.transformation),
    )


def test_curve_discretization():
    curve = Line([0, 0, 0], [2, 0, 0])

    points = curve.to_points(n=3, domain=(0.25, 0.75))
    polyline = curve.to_polyline(n=2)

    assert points == [Point(0.5, 0, 0), Point(1, 0, 0), Point(1.5, 0, 0)]
    assert len(polyline.points) == 3
    assert polyline.start == curve.start
    assert polyline.end == curve.end


def test_curve_to_polygon():
    circle = Circle(radius=1)
    polygon = circle.to_polygon(n=8)

    assert len(polygon.points) == 8

    with pytest.raises(ValueError):
        Arc(radius=1, start_angle=0, end_angle=math.pi).to_polygon()
