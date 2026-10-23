import pytest

from compas.geometry import barycentric_coordinates
from compas.geometry import discrete_coons_patch
from compas.geometry import tween_points
from compas.geometry import tween_points_distance


def test_barycentric_coordinates():
    coordinates = barycentric_coordinates([0.25, 0.25, 0.0], [[0, 0, 0], [1, 0, 0], [0, 1, 0]])

    assert coordinates == pytest.approx([0.5, 0.25, 0.25])


def test_discrete_coons_patch():
    ab = [[0, 0, 0], [0, 1, 0]]
    bc = [[0, 1, 0], [1, 1, 0]]
    dc = [[1, 0, 0], [1, 1, 0]]
    ad = [[0, 0, 0], [1, 0, 0]]

    vertices, faces = discrete_coons_patch(ab, bc, dc, ad)

    assert vertices == [[0, 0, 0], [1, 0, 0], [0, 1, 0], [1, 1, 0]]
    assert faces == [[0, 1, 3, 2]]


def test_discrete_triangular_coons_patch():
    bc = [[0, 1, 0], [1, 1, 0]]
    dc = [[0, 0, 0], [1, 1, 0]]
    ad = [[0, 0, 0], [0, 1, 0]]

    vertices, faces = discrete_coons_patch(None, bc, dc, ad)

    assert len(vertices) == 4
    assert faces == [[0, 1, 3, 2]]


def test_tween_points():
    points1 = [[0, 0, 0], [0, 1, 0]]
    points2 = [[2, 0, 0], [2, 1, 0]]

    tweens = tween_points(points1, points2, 3)

    assert tweens == [
        [[0.5, 0, 0], [0.5, 1, 0]],
        [[1.0, 0, 0], [1.0, 1, 0]],
        [[1.5, 0, 0], [1.5, 1, 0]],
    ]


def test_tween_points_distance():
    points1 = [[0, 0, 0], [0, 1, 0]]
    points2 = [[2, 0, 0], [4, 1, 0]]

    tween = tween_points_distance(points1, points2, 1.0, index=1)

    assert tween == [[0.5, 0, 0], [1, 1, 0]]
