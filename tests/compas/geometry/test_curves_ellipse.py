import pytest
import json
import compas

from compas.geometry import close
from compas.geometry import allclose
from compas.geometry import Frame
from compas.geometry import Ellipse
from compas.geometry import Plane


def test_ellipse_create():
    ellipse = Ellipse(major=1.0, minor=0.5)

    assert close(ellipse.major, 1.0, tol=1e-12)
    assert close(ellipse.minor, 0.5, tol=1e-12)
    assert close(ellipse.area, 1.5707963267948966, tol=1e-12)
    assert close(ellipse.semifocal, 0.8660254037844386, tol=1e-12)
    assert close(ellipse.eccentricity, 0.8660254037844386, tol=1e-12)
    assert close(ellipse.focal, 1.7320508075688772, tol=1e-12)

    assert ellipse.is_closed
    assert ellipse.is_periodic

    assert ellipse.frame == Frame.worldXY()

    assert allclose(ellipse.point_at(0.0), [1.0, 0.0, 0.0], tol=1e-12)
    assert allclose(ellipse.point_at(0.25), [0.0, 0.5, 0.0], tol=1e-12)
    assert allclose(ellipse.point_at(0.5), [-1.0, 0.0, 0.0], tol=1e-12)
    assert allclose(ellipse.point_at(0.75), [0.0, -0.5, 0.0], tol=1e-12)
    assert allclose(ellipse.point_at(1.0), [1.0, 0.0, 0.0], tol=1e-12)

    assert allclose(ellipse.point_at(0.0), ellipse.point_at(0.0, world=False), tol=1e-12)
    assert allclose(ellipse.point_at(0.25), ellipse.point_at(0.25, world=False), tol=1e-12)
    assert allclose(ellipse.point_at(0.5), ellipse.point_at(0.5, world=False), tol=1e-12)
    assert allclose(ellipse.point_at(0.75), ellipse.point_at(0.75, world=False), tol=1e-12)
    assert allclose(ellipse.point_at(1.0), ellipse.point_at(1.0, world=False), tol=1e-12)


def test_ellipse_create_with_frame():
    ellipse = Ellipse(major=1.0, minor=0.5, frame=Frame.worldZX())

    assert close(ellipse.major, 1.0, tol=1e-12)
    assert close(ellipse.minor, 0.5, tol=1e-12)
    assert close(ellipse.area, 1.5707963267948966, tol=1e-12)
    assert close(ellipse.semifocal, 0.8660254037844386, tol=1e-12)
    assert close(ellipse.eccentricity, 0.8660254037844386, tol=1e-12)
    assert close(ellipse.focal, 1.7320508075688772, tol=1e-12)

    assert ellipse.is_closed
    assert ellipse.is_periodic

    assert ellipse.frame == Frame.worldZX()

    assert allclose(ellipse.point_at(0.0), [0.0, 0.0, 1.0], tol=1e-12)
    assert allclose(ellipse.point_at(0.25), [0.5, 0.0, 0.0], tol=1e-12)
    assert allclose(ellipse.point_at(0.5), [0.0, 0.0, -1.0], tol=1e-12)
    assert allclose(ellipse.point_at(0.75), [-0.5, 0.0, 0.0], tol=1e-12)
    assert allclose(ellipse.point_at(1.0), [0.0, 0.0, 1.0], tol=1e-12)

    assert allclose(ellipse.point_at(0.0, world=False), [1.0, 0.0, 0.0], tol=1e-12)
    assert allclose(ellipse.point_at(0.25, world=False), [0.0, 0.5, 0.0], tol=1e-12)
    assert allclose(ellipse.point_at(0.5, world=False), [-1.0, 0.0, 0.0], tol=1e-12)
    assert allclose(ellipse.point_at(0.75, world=False), [0.0, -0.5, 0.0], tol=1e-12)
    assert allclose(ellipse.point_at(1.0, world=False), [1.0, 0.0, 0.0], tol=1e-12)

    assert allclose(
        ellipse.point_at(0.0),
        ellipse.point_at(0.0, world=False).transformed(ellipse.transformation),
        tol=1e-12,
    )
    assert allclose(
        ellipse.point_at(0.25),
        ellipse.point_at(0.25, world=False).transformed(ellipse.transformation),
        tol=1e-12,
    )
    assert allclose(
        ellipse.point_at(0.50),
        ellipse.point_at(0.50, world=False).transformed(ellipse.transformation),
        tol=1e-12,
    )
    assert allclose(
        ellipse.point_at(0.75),
        ellipse.point_at(0.75, world=False).transformed(ellipse.transformation),
        tol=1e-12,
    )
    assert allclose(
        ellipse.point_at(1.00),
        ellipse.point_at(1.00, world=False).transformed(ellipse.transformation),
        tol=1e-12,
    )


# =============================================================================
# Data
# =============================================================================


def test_ellipse_data():
    ellipse = Ellipse(major=1.0, minor=0.5)
    other = Ellipse.from_data(json.loads(json.dumps(ellipse.data)))

    assert ellipse.major == other.major
    assert ellipse.minor == other.minor
    assert ellipse.frame.point == other.frame.point
    assert allclose(ellipse.frame.xaxis, other.frame.xaxis, tol=1e-12)
    assert allclose(ellipse.frame.yaxis, other.frame.yaxis, tol=1e-12)

    if not compas.IPY:
        assert Ellipse.validate_data(ellipse.data)
        assert Ellipse.validate_data(other.data)


# =============================================================================
# Constructors
# =============================================================================


def test_ellipse_create_from_point_major_minor():
    ellipse = Ellipse.from_point_major_minor([1.0, 2.0, 3.0], 1.0, 0.5)

    assert close(ellipse.major, 1.0, tol=1e-12)
    assert close(ellipse.minor, 0.5, tol=1e-12)
    assert close(ellipse.area, 1.5707963267948966, tol=1e-12)
    assert close(ellipse.semifocal, 0.8660254037844386, tol=1e-12)
    assert close(ellipse.eccentricity, 0.8660254037844386, tol=1e-12)
    assert close(ellipse.focal, 1.7320508075688772, tol=1e-12)

    assert ellipse.is_closed
    assert ellipse.is_periodic

    assert allclose(ellipse.frame.point, [1, 2, 3], tol=1e-12)
    assert allclose(ellipse.frame.xaxis, Frame.worldXY().xaxis, tol=1e-12)
    assert allclose(ellipse.frame.yaxis, Frame.worldXY().yaxis, tol=1e-12)
    assert allclose(ellipse.frame.zaxis, Frame.worldXY().zaxis, tol=1e-12)


def test_ellipse_create_from_plane_major_minor():
    plane = Plane([1.0, 2.0, 3.0], [0.0, 0.0, 1.0])
    frame = Frame.from_plane(plane)
    ellipse = Ellipse.from_plane_major_minor(plane, 1.0, 0.5)

    assert close(ellipse.major, 1.0, tol=1e-12)
    assert close(ellipse.minor, 0.5, tol=1e-12)
    assert close(ellipse.area, 1.5707963267948966, tol=1e-12)
    assert close(ellipse.semifocal, 0.8660254037844386, tol=1e-12)
    assert close(ellipse.eccentricity, 0.8660254037844386, tol=1e-12)
    assert close(ellipse.focal, 1.7320508075688772, tol=1e-12)

    assert ellipse.is_closed
    assert ellipse.is_periodic

    assert allclose(ellipse.frame.point, frame.point, tol=1e-12)
    assert allclose(ellipse.frame.xaxis, frame.xaxis, tol=1e-12)
    assert allclose(ellipse.frame.yaxis, frame.yaxis, tol=1e-12)
    assert allclose(ellipse.frame.zaxis, frame.zaxis, tol=1e-12)


# =============================================================================
# Properties and Geometry
# =============================================================================


def test_ellipse_major():
    ellipse = Ellipse(major=1.0, minor=0.5)

    assert close(ellipse.major, 1.0, tol=1e-12)

    ellipse._major = None
    with pytest.raises(ValueError):
        ellipse.major

    with pytest.raises(ValueError):
        ellipse.major = -1.0


def test_ellipse_minor():
    ellipse = Ellipse(major=1.0, minor=0.5)

    assert close(ellipse.minor, 0.5, tol=1e-12)

    ellipse._minor = None
    with pytest.raises(ValueError):
        ellipse.minor

    with pytest.raises(ValueError):
        ellipse.minor = -1.0


# =============================================================================
# Accessors
# =============================================================================

# =============================================================================
# Comparison
# =============================================================================

# =============================================================================
# Other Methods
# =============================================================================
