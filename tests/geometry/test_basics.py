import pytest

from math import pi

from compas.geometry import angle_vectors
from compas.geometry import angles_vectors


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
