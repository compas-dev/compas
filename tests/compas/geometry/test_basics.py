import pytest

from math import pi

from compas.geometry import angle_vectors
from compas.geometry import angles_vectors
from compas.geometry import length_vector
from compas.geometry import subtract_vectors

from compas.geometry import centroid_points
from compas.geometry import centroid_polygon
from compas.geometry import centroid_polyhedron
from compas.geometry import volume_polyhedron

from compas.geometry import Polyhedron


# ==============================================================================
# angles
# ==============================================================================


@pytest.mark.parametrize(("u", "v", "angle"),
                         [
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


@pytest.mark.parametrize(("u", "v"),
                         [
    ([0.0, 0.0, 0.0], [0.0, 0.0, 0.0]),
    ([0.0, 0.0, 0.0], [1.0, 0.0, 0.0]),
    ([1.0, 0.0, 0.0], [0.0, 0.0, 0.0]),
]
)
def test_angle_vectors_fails_when_input_is_zero(u, v):
    with pytest.raises(ZeroDivisionError):
        angle_vectors(u, v)


@pytest.mark.parametrize(("u", "v", "angles"),
                         [
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


@pytest.mark.parametrize(("u", "v"),
                         [
    ([0.0, 0.0, 0.0], [0.0, 0.0, 0.0]),
    ([0.0, 0.0, 0.0], [1.0, 0.0, 0.0]),
    ([1.0, 0.0, 0.0], [0.0, 0.0, 0.0]),
]
)
def test_angles_vectors_fails_when_input_is_zero(u, v):
    with pytest.raises(ZeroDivisionError):
        angles_vectors(u, v)

# ==============================================================================
# average
# ==============================================================================


@pytest.mark.parametrize(("points", "centroid"),
                         [
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


@pytest.mark.parametrize(("points"),
                         [
    [0.0, 0.0, 0.0]
]
)
def test_centroid_points_fails_when_input_is_not_list_of_lists(points):
    with pytest.raises(TypeError):
        centroid_points(points)


@pytest.mark.parametrize(("points"),
                         [
    [[0.0, 0.0, 0.0], [0.0, 0.0]],
    [[0.0, 0.0]],
]
)
def test_centroid_points_fails_when_input_is_not_complete_points(points):
    with pytest.raises(ValueError):
        centroid_points(points)


@pytest.mark.parametrize(("polyhedron", "centroid"),
                         [
    (Polyhedron.generate(6), [0.0, 0.0, 0.0]),
]
)
def test_centroid_polyhedron(polyhedron, centroid):
    x, y, z = centroid
    assert centroid_polyhedron(polyhedron) == [pytest.approx(x, 0.001), pytest.approx(y, 0.001), pytest.approx(z, 0.001)]


# ==============================================================================
# size
# ==============================================================================


@pytest.mark.parametrize(("polyhedron", "volume"),
                         [
    (Polyhedron.generate(6), None)
]
)
def test_volume_polyhedron(polyhedron, volume):
    if volume is None:
        L = length_vector(subtract_vectors(
            polyhedron.vertices[0], polyhedron.vertices[1]))
        volume = L * L * L
    V = volume_polyhedron(polyhedron)
    assert V == pytest.approx(volume, 0.001)
