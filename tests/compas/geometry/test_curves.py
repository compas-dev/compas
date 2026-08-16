import pytest
import math
from compas.tolerance import TOL
from compas.geometry import Frame
from compas.geometry import Arc
from compas.geometry import Circle
from compas.geometry import Ellipse
from compas.geometry import Hyperbola
from compas.geometry import Parabola


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
    curve = Arc(radius=1, start_angle=0, end_angle=math.pi)

    points = curve.to_points(n=3, domain=(0.25, 0.75))
    polyline = curve.to_polyline(n=2)

    assert TOL.is_allclose(points[0], [math.sqrt(0.5), math.sqrt(0.5), 0])
    assert TOL.is_allclose(points[1], [0, 1, 0])
    assert TOL.is_allclose(points[2], [-math.sqrt(0.5), math.sqrt(0.5), 0])
    assert len(polyline.points) == 3
    assert polyline.start == curve.point_at(0)
    assert polyline.end == curve.point_at(1)


@pytest.mark.parametrize(
    "curve",
    [
        Hyperbola(major=1.0, minor=0.5),
        Parabola(focal=1.0),
    ],
)
def test_unbounded_curve_discretization_requires_finite_domain(curve):
    with pytest.raises(ValueError, match="finite domain"):
        curve.to_points()

    with pytest.raises(ValueError, match="finite domain"):
        curve.to_polyline()

    points = curve.to_points(n=3, domain=(-1.0, 1.0))
    polyline = curve.to_polyline(n=2, domain=(-1.0, 1.0))

    assert len(points) == 3
    assert len(polyline.points) == 3
    assert all(math.isfinite(coordinate) for point in points for coordinate in point)


def test_curve_frame_requires_frame_object():
    representation = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]

    with pytest.raises(TypeError):
        Circle(radius=1.0, frame=representation)  # type: ignore[arg-type]

    circle = Circle(radius=1.0)
    with pytest.raises(TypeError):
        circle.frame = representation  # type: ignore[assignment]


def test_curve_transformation_reflects_frame_mutation():
    circle = Circle(radius=1.0)
    _ = circle.transformation

    circle.center = [10.0, 0.0, 0.0]
    assert TOL.is_allclose(circle.point_at(0.0), [11.0, 0.0, 0.0])

    circle.frame.point = [20.0, 0.0, 0.0]
    assert TOL.is_allclose(circle.point_at(0.0), [21.0, 0.0, 0.0])


def test_curve_to_polygon():
    circle = Circle(radius=1)
    polygon = circle.to_polygon(n=8)

    assert len(polygon.points) == 8

    with pytest.raises(ValueError):
        Arc(radius=1, start_angle=0, end_angle=math.pi).to_polygon()
