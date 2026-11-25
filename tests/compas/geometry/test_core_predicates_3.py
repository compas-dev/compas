import random

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


B1 = [100000000.1, 100000000.2, 0.0]
B2 = [100000000.1, 100000000.2, 100000000.3]


@pytest.mark.parametrize(
    "points, expected",
    [
        # cross products with the baseline that are zero or only rounding noise
        ([[0, 0, 0], B1, [x / 4 for x in B1], [x / 2 for x in B1]], True),
        ([[0, 0, 0], B2, [x / 2 for x in B2], [x * (2.0 / 3.0) for x in B2]], True),
        # an exact normal from a point close to the baseline
        ([[0, 0, 0], [1e8, 0, 0], [5e7, 2e-8, 0], [0, 0, 1e-8]], False),
        # exactly on x + y + z = 0
        ([[0.0, 0.0, 0.0], [1.0, 0.0, -1.0], [1e8, 200000001.0, -300000001.0], [25000002.0, 50000001.25, -75000003.25]], True),
    ],
)
def test_is_coplanar_far_from_origin(points, expected):
    assert is_coplanar(points) == expected
    assert Polygon(points).is_planar == expected


def test_is_coplanar_line_with_one_point_barely_off_it():
    # A line and one point always lie in a plane, also when the point is a few
    # tolerances off a long line and the normal from their cross product is inexact.
    rng = random.Random(1536)
    for _ in range(1500):
        a = [rng.uniform(-1e4, 1e4) for _ in range(3)]
        d = [rng.uniform(-1e4, 1e4) for _ in range(3)]
        points = [[a[i] + t * d[i] for i in range(3)] for t in [rng.uniform(-1, 1) for _ in range(rng.randint(4, 9))]]
        lift = [rng.gauss(0, 1) for _ in range(3)]
        scale = 3e-9 / sum(x * x for x in lift) ** 0.5
        k = rng.randrange(len(points))
        points[k] = [points[k][i] + scale * lift[i] for i in range(3)]

        assert is_coplanar(points)
