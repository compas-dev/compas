import pytest

from math import pi

from compas.geometry import angle_vectors
from compas.geometry import angles_vectors

from compas.geometry import centroid_points
from compas.geometry import centroid_polygon
from compas.geometry import centroid_polyhedron


# ==============================================================================
# angles
# ==============================================================================


@pytest.mark.parametrize(
    ("u", "v", "angle"), 
    [
        pytest.param([0.0, 0.0, 0.0], [0.0, 0.0, 0.0], 0.0, marks=pytest.mark.xfail(raises=ZeroDivisionError)),
        pytest.param([0.0, 0.0, 0.0], [1.0, 0.0, 0.0], 0.0, marks=pytest.mark.xfail(raises=ZeroDivisionError)),
        pytest.param([1.0, 0.0, 0.0], [0.0, 0.0, 0.0], 0.0, marks=pytest.mark.xfail(raises=ZeroDivisionError)),

        ([1.0, 0.0, 0.0], [1.0, 0.0, 0.0], 0.0),     # X - X
        ([0.0, 1.0, 0.0], [0.0, 1.0, 0.0], 0.0),     # Y - Y
        ([0.0, 0.0, 1.0], [0.0, 0.0, 1.0], 0.0),     # Z - Z

        ([1.0, 0.0, 0.0], [0.0, 1.0, 0.0], pi / 2),  # X - Y
        ([0.0, 1.0, 0.0], [1.0, 0.0, 0.0], pi / 2),  # Y - X
        ([1.0, 0.0, 0.0], [0.0, 0.0, 1.0], pi / 2),  # X - Z
        ([0.0, 0.0, 1.0], [1.0, 0.0, 0.0], pi / 2),  # Z - X
        ([0.0, 1.0, 0.0], [0.0, 0.0, 1.0], pi / 2),  # Y - Z
        ([0.0, 0.0, 1.0], [0.0, 1.0, 0.0], pi / 2),  # Z - Y
    ]
)
def test_angle_vectors(u, v, angle):
    assert angle_vectors(u, v) == pytest.approx(angle)


@pytest.mark.parametrize(
    ("u", "v", "angles"), 
    [
        pytest.param([0.0, 0.0, 0.0], [0.0, 0.0, 0.0], (0.0, 0.0), marks=pytest.mark.xfail(raises=ZeroDivisionError)),
        pytest.param([0.0, 0.0, 0.0], [1.0, 0.0, 0.0], (0.0, 0.0), marks=pytest.mark.xfail(raises=ZeroDivisionError)),
        pytest.param([1.0, 0.0, 0.0], [0.0, 0.0, 0.0], (0.0, 0.0), marks=pytest.mark.xfail(raises=ZeroDivisionError)),

        ([1.0, 0.0, 0.0], [1.0, 0.0, 0.0], (0.0, 2 * pi)),         # X - X
        ([0.0, 1.0, 0.0], [0.0, 1.0, 0.0], (0.0, 2 * pi)),         # Y - Y
        ([0.0, 0.0, 1.0], [0.0, 0.0, 1.0], (0.0, 2 * pi)),         # Z - Z

        ([1.0, 0.0, 0.0], [0.0, 1.0, 0.0], (pi / 2, 3 * pi / 2)),  # X - Y
        ([0.0, 1.0, 0.0], [1.0, 0.0, 0.0], (pi / 2, 3 * pi / 2)),  # Y - X
        ([1.0, 0.0, 0.0], [0.0, 0.0, 1.0], (pi / 2, 3 * pi / 2)),  # X - Z
        ([0.0, 0.0, 1.0], [1.0, 0.0, 0.0], (pi / 2, 3 * pi / 2)),  # Z - X
        ([0.0, 1.0, 0.0], [0.0, 0.0, 1.0], (pi / 2, 3 * pi / 2)),  # Y - Z
        ([0.0, 0.0, 1.0], [0.0, 1.0, 0.0], (pi / 2, 3 * pi / 2)),  # Z - Y
    ]
)
def test_angles_vectors(u, v, angles):
    a, b = angles
    assert angles_vectors(u, v) == (pytest.approx(a), pytest.approx(b))


# ==============================================================================
# average
# ==============================================================================


@pytest.mark.parametrize(
    ("points", "centroid"), 
    [
        pytest.param([0.0, 0.0, 0.0], None, marks=pytest.mark.xfail(raises=TypeError)),
        pytest.param([[0.0, 0.0, 0.0], [0.0, 0.0]], None, marks=pytest.mark.xfail(raises=ValueError)),
        pytest.param([[0.0, 0.0]], None, marks=pytest.mark.xfail(raises=ValueError)),

        ([[0.0, 0.0, 0.0]], [0.0, 0.0, 0.0]),
        ([[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]], [0.0, 0.0, 0.0]),

        ([[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]], [0.0, 0.0, 0.0]),
        ([[0.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.5, 1.0, 0.0]], [0.1666, 0.6666, 0.0]),

        ([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0], [0.0, 1.0, 0.0]], [0.5, 0.5, 0.0]),
        ([[0.0, 0.0, 0.0], [0.1, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.1, 0.0]], [0.35, 0.35, 0.0]),
    ]
)
def test_centroid_points(points, centroid):
    if centroid is None:
        x, y, z = 0.0, 0.0, 0.0
    else:
        x, y, z = centroid
    assert centroid_points(points) == [pytest.approx(x, 0.001), pytest.approx(y, 0.001), pytest.approx(z, 0.001)]
