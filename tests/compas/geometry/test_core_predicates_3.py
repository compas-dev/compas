from compas.geometry import is_coplanar
import pytest


def test_is_coplanar():
    # 4 points that are colinear:
    points = [[0, 0, 0], [0, 1, 0], [0, 2, 0], [0, 4, 0]]

    try:
        is_coplanar(points)
    except IndexError:
        pytest.fail("is_coplanar raised an IndexError")
