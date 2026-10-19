from compas.geometry import is_coplanar
from compas.geometry import Polygon
import pytest


def test_is_coplanar():
    # 4 points that are colinear:
    points = [[0, 0, 0], [0, 1, 0], [0, 2, 0], [0, 4, 0]]

    try:
        is_coplanar(points)
    except IndexError:
        pytest.fail("is_coplanar raised an IndexError")


@pytest.mark.parametrize(
    "points",
    [
        [[0, 0, 0], [1, 0, 0], [2, 0, 0], [0, 0, 1], [0, 1, 1], [1, 0, 1]],
        [[0, 0, 0], [1, 0, 0], [2, 0, 0], [0, 1, 0], [1, 1, 0], [2, 1, 0], [0, 0, 1], [1, 0, 1], [2, 0, 1]],
        [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 1], [0, 1, 1], [1, 0, 1]],
    ],
)
@pytest.mark.parametrize("shift", [0, 1, 2])
def test_is_coplanar_retains_points_from_collinear_triples(points, shift):
    points = points[shift:] + points[:shift]
    original = [point[:] for point in points]

    assert not is_coplanar(points)
    assert not Polygon(points).is_planar
    assert points == original


@pytest.mark.parametrize("tol", [None, 1e-8])
@pytest.mark.parametrize("reverse", [False, True])
def test_is_coplanar_uses_well_conditioned_third_point(tol, reverse):
    epsilon = 0.22 * (1e-9 if tol is None else tol)
    remaining = [[0, 1, 0.4], [0, 0.5, -0.4]]
    if reverse:
        remaining.reverse()
    points = [[0, 0, 0], [1, 0, 0], [2, 0, 0], [10, 0, 0], [0, epsilon, 0]] + remaining
    original = [point[:] for point in points]

    assert not is_coplanar(points, tol=tol)
    assert not Polygon(points).is_planar
    assert points == original


def test_is_coplanar_normalizes_plane_distance():
    points = [[0, 0, 0], [0.05, 0, 0], [0.1, 0, 0], [0, 1e-4, 0], [0, -1e-4, 0], [0.1, 0, 0], [0, 0, 9e-5]]

    assert not is_coplanar(points)
    assert not Polygon(points).is_planar


@pytest.mark.parametrize("scale", [2.0**-20, 1.0, 2.0**20])
@pytest.mark.parametrize("tol", [None, 1e-8])
@pytest.mark.parametrize("height, expected", [(0.5, True), (2.0, False)])
def test_is_coplanar_tolerance_is_a_distance(scale, tol, height, expected):
    h = height * (1e-9 if tol is None else tol)
    points = [
        [-scale, -scale, 0],
        [0, 0, 0],
        [scale, scale, 0],
        [-scale, scale, 0],
        [scale, -scale, 0],
        [0, 0, h],
        [0, 0, -h],
    ]
    original = [point[:] for point in points]

    assert is_coplanar(points, tol=tol) == expected
    assert points == original


@pytest.mark.parametrize("tol", [None, 1e-8])
@pytest.mark.parametrize("axis", [0, 1, 2])
@pytest.mark.parametrize("reverse", [False, True])
def test_is_coplanar_fits_noisy_points(tol, axis, reverse):
    h = 0.6 * (1e-9 if tol is None else tol)
    points = [[0, 0, 0], [1, 0, 0], [0, 1, 0], [10, 10, h], [10, -10, -h], [-10, 10, -h], [-10, -10, h]]
    if reverse:
        points = points[:1] + points[:0:-1]
    points = [[point[(i + axis) % 3] for i in range(3)] for point in points]
    original = [point[:] for point in points]

    assert is_coplanar(points, tol)
    if tol is None:
        assert Polygon(points).is_planar
    assert points == original


@pytest.mark.parametrize("tol", [None, 1e-8])
@pytest.mark.parametrize("axis", [0, 1, 2])
@pytest.mark.parametrize("height, expected", [(1.8, True), (2.2, False)])
def test_is_coplanar_allows_residuals_for_every_point(tol, axis, height, expected):
    h = height * (1e-9 if tol is None else tol)
    points = [[x, y, z] for z in [0, h] for x, y in [(0, 0), (2, 0), (2, 2), (0, 2)]]
    points = [[point[(i + axis) % 3] for i in range(3)] for point in points]

    assert is_coplanar(points, tol) == expected


@pytest.mark.parametrize(
    "points",
    [
        [[0, 0, 0]] * 6,
        [[x, 0, 0] for x in range(7)],
        [[0, 0, 0], [1, 0, 0], [2, 0, 0], [2, 1, 0], [1, 1, 0], [0, 1, 0]],
        [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 1, 0], [1, 0, 0], [1, 1, 0]],
    ],
)
@pytest.mark.parametrize("offset", [[0, 0, 0], [8, -4, 2]])
def test_is_coplanar_accepts_planar_degenerate_prefixes(points, offset):
    translated = [[value + delta for value, delta in zip(point, offset)] for point in points]

    assert is_coplanar(translated)
