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
