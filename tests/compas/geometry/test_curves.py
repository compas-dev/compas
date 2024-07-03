import pytest
import math
from compas.tolerance import TOL
from compas.geometry import Frame
from compas.geometry import Arc
from compas.geometry import Circle
from compas.geometry import Ellipse
from compas.geometry import Hyperbola


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
