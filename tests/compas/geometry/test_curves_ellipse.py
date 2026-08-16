import pytest
import json

from compas.tolerance import TOL
from compas.geometry import Frame
from compas.geometry import Ellipse
from compas.geometry import Plane


def test_ellipse_create():
    ellipse = Ellipse(major=1.0, minor=0.5)

    assert TOL.is_close(ellipse.major, 1.0)
    assert TOL.is_close(ellipse.minor, 0.5)
    assert TOL.is_close(ellipse.area, 1.5707963267948966)
    assert TOL.is_close(ellipse.circumference, 4.844224110273838)
    assert TOL.is_close(ellipse.length, ellipse.circumference)
    assert TOL.is_close(ellipse.semifocal, 0.8660254037844386)
    assert TOL.is_close(ellipse.eccentricity, 0.8660254037844386)
    assert TOL.is_close(ellipse.focal, 1.7320508075688772)

    assert ellipse.is_closed
    assert ellipse.is_periodic

    assert ellipse.frame == Frame.worldXY()

    assert TOL.is_allclose(ellipse.point_at(0.0), [1.0, 0.0, 0.0])
    assert TOL.is_allclose(ellipse.point_at(0.25), [0.0, 0.5, 0.0])
    assert TOL.is_allclose(ellipse.point_at(0.5), [-1.0, 0.0, 0.0])
    assert TOL.is_allclose(ellipse.point_at(0.75), [0.0, -0.5, 0.0])
    assert TOL.is_allclose(ellipse.point_at(1.0), [1.0, 0.0, 0.0])

    assert TOL.is_allclose(ellipse.point_at(0.0), ellipse.point_at(0.0, world=False))
    assert TOL.is_allclose(ellipse.point_at(0.25), ellipse.point_at(0.25, world=False))
    assert TOL.is_allclose(ellipse.point_at(0.5), ellipse.point_at(0.5, world=False))
    assert TOL.is_allclose(ellipse.point_at(0.75), ellipse.point_at(0.75, world=False))
    assert TOL.is_allclose(ellipse.point_at(1.0), ellipse.point_at(1.0, world=False))


def test_ellipse_create_with_frame():
    ellipse = Ellipse(major=1.0, minor=0.5, frame=Frame.worldZX())

    assert TOL.is_close(ellipse.major, 1.0)
    assert TOL.is_close(ellipse.minor, 0.5)
    assert TOL.is_close(ellipse.area, 1.5707963267948966)
    assert TOL.is_close(ellipse.semifocal, 0.8660254037844386)
    assert TOL.is_close(ellipse.eccentricity, 0.8660254037844386)
    assert TOL.is_close(ellipse.focal, 1.7320508075688772)

    assert ellipse.is_closed
    assert ellipse.is_periodic

    assert ellipse.frame == Frame.worldZX()

    assert TOL.is_allclose(ellipse.point_at(0.0), [0.0, 0.0, 1.0])
    assert TOL.is_allclose(ellipse.point_at(0.25), [0.5, 0.0, 0.0])
    assert TOL.is_allclose(ellipse.point_at(0.5), [0.0, 0.0, -1.0])
    assert TOL.is_allclose(ellipse.point_at(0.75), [-0.5, 0.0, 0.0])
    assert TOL.is_allclose(ellipse.point_at(1.0), [0.0, 0.0, 1.0])

    assert TOL.is_allclose(ellipse.point_at(0.0, world=False), [1.0, 0.0, 0.0])
    assert TOL.is_allclose(ellipse.point_at(0.25, world=False), [0.0, 0.5, 0.0])
    assert TOL.is_allclose(ellipse.point_at(0.5, world=False), [-1.0, 0.0, 0.0])
    assert TOL.is_allclose(ellipse.point_at(0.75, world=False), [0.0, -0.5, 0.0])
    assert TOL.is_allclose(ellipse.point_at(1.0, world=False), [1.0, 0.0, 0.0])

    assert TOL.is_allclose(
        ellipse.point_at(0.0),
        ellipse.point_at(0.0, world=False).transformed(ellipse.transformation),
    )
    assert TOL.is_allclose(
        ellipse.point_at(0.25),
        ellipse.point_at(0.25, world=False).transformed(ellipse.transformation),
    )
    assert TOL.is_allclose(
        ellipse.point_at(0.50),
        ellipse.point_at(0.50, world=False).transformed(ellipse.transformation),
    )
    assert TOL.is_allclose(
        ellipse.point_at(0.75),
        ellipse.point_at(0.75, world=False).transformed(ellipse.transformation),
    )
    assert TOL.is_allclose(
        ellipse.point_at(1.00),
        ellipse.point_at(1.00, world=False).transformed(ellipse.transformation),
    )


# =============================================================================
# Data
# =============================================================================


def test_ellipse_data():
    ellipse = Ellipse(major=1.0, minor=0.5)
    other = Ellipse.__from_data__(json.loads(json.dumps(ellipse.__data__)))

    assert ellipse.major == other.major
    assert ellipse.minor == other.minor
    assert ellipse.frame.point == other.frame.point
    assert TOL.is_allclose(ellipse.frame.xaxis, other.frame.xaxis)
    assert TOL.is_allclose(ellipse.frame.yaxis, other.frame.yaxis)


# =============================================================================
# Constructors
# =============================================================================


def test_ellipse_create_from_point_major_minor():
    ellipse = Ellipse.from_point_major_minor([1.0, 2.0, 3.0], 1.0, 0.5)

    assert TOL.is_close(ellipse.major, 1.0)
    assert TOL.is_close(ellipse.minor, 0.5)
    assert TOL.is_close(ellipse.area, 1.5707963267948966)
    assert TOL.is_close(ellipse.semifocal, 0.8660254037844386)
    assert TOL.is_close(ellipse.eccentricity, 0.8660254037844386)
    assert TOL.is_close(ellipse.focal, 1.7320508075688772)

    assert ellipse.is_closed
    assert ellipse.is_periodic

    assert TOL.is_allclose(ellipse.frame.point, [1, 2, 3])
    assert TOL.is_allclose(ellipse.frame.xaxis, Frame.worldXY().xaxis)
    assert TOL.is_allclose(ellipse.frame.yaxis, Frame.worldXY().yaxis)
    assert TOL.is_allclose(ellipse.frame.zaxis, Frame.worldXY().zaxis)


def test_ellipse_create_from_plane_major_minor():
    plane = Plane([1.0, 2.0, 3.0], [0.0, 0.0, 1.0])
    frame = Frame.from_plane(plane)
    ellipse = Ellipse.from_plane_major_minor(plane, 1.0, 0.5)

    assert TOL.is_close(ellipse.major, 1.0)
    assert TOL.is_close(ellipse.minor, 0.5)
    assert TOL.is_close(ellipse.area, 1.5707963267948966)
    assert TOL.is_close(ellipse.semifocal, 0.8660254037844386)
    assert TOL.is_close(ellipse.eccentricity, 0.8660254037844386)
    assert TOL.is_close(ellipse.focal, 1.7320508075688772)

    assert ellipse.is_closed
    assert ellipse.is_periodic

    assert TOL.is_allclose(ellipse.frame.point, frame.point)
    assert TOL.is_allclose(ellipse.frame.xaxis, frame.xaxis)
    assert TOL.is_allclose(ellipse.frame.yaxis, frame.yaxis)
    assert TOL.is_allclose(ellipse.frame.zaxis, frame.zaxis)


# =============================================================================
# Properties and Geometry
# =============================================================================


def test_ellipse_major():
    ellipse = Ellipse(major=1.0, minor=0.5)

    assert TOL.is_close(ellipse.major, 1.0)

    ellipse._major = None
    with pytest.raises(ValueError):
        ellipse.major

    with pytest.raises(ValueError):
        ellipse.major = -1.0

    with pytest.raises(ValueError):
        ellipse.major = 0.0


def test_ellipse_minor():
    ellipse = Ellipse(major=1.0, minor=0.5)

    assert TOL.is_close(ellipse.minor, 0.5)

    ellipse._minor = None
    with pytest.raises(ValueError):
        ellipse.minor

    with pytest.raises(ValueError):
        ellipse.minor = -1.0

    with pytest.raises(ValueError):
        ellipse.minor = 0.0

    with pytest.raises(ValueError):
        ellipse.minor = 2.0


def test_ellipse_major_cannot_be_smaller_than_minor():
    ellipse = Ellipse(major=1.0, minor=0.5)

    with pytest.raises(ValueError):
        ellipse.major = 0.25


@pytest.mark.parametrize("major, minor", [(0.0, 0.5), (1.0, 0.0)])
def test_ellipse_rejects_degenerate_axes(major, minor):
    with pytest.raises(ValueError, match="positive"):
        Ellipse(major=major, minor=minor)


def test_circle_shaped_ellipse_circumference_is_exact():
    ellipse = Ellipse(major=2.0, minor=2.0)

    assert TOL.is_close(ellipse.circumference, 4.0 * 3.141592653589793)


def test_ellipse_comparison():
    ellipse = Ellipse(major=1.0, minor=0.5)

    assert ellipse == Ellipse(major=1.0, minor=0.5)
    assert ellipse != Ellipse(major=2.0, minor=0.5)
    assert ellipse != Ellipse(major=1.0, minor=0.25)
    assert ellipse != object()


def test_ellipse_constructors_preserve_subclass():
    class CustomEllipse(Ellipse):
        pass

    assert isinstance(CustomEllipse.from_point_major_minor([0.0, 0.0, 0.0], 2.0, 1.0), CustomEllipse)
    assert isinstance(CustomEllipse.from_plane_major_minor(Plane.worldXY(), 2.0, 1.0), CustomEllipse)


# =============================================================================
# Accessors
# =============================================================================

# =============================================================================
# Comparison
# =============================================================================

# =============================================================================
# Other Methods
# =============================================================================
