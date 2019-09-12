import pytest

from compas.geometry import bounding_box_xy


@pytest.mark.parametrize('coords,expected', [
    [[[0, 0], [1, 2], [-5, 6], [-3, 2], [0.5, -1]],
     [[-5, -1, 0.0], [1, -1, 0.0], [1, 6, 0.0], [-5, 6, 0.0]]],

    [[[6.74219, -53.57835], [6.74952, -53.57241], [6.75652, -53.56289], [6.74756, -53.56598], [6.73462, -53.57518]],
     [[6.73462, -53.57835, 0.0], [6.75652, -53.57835, 0.0], [6.75652, -53.56289, 0.0], [6.73462, -53.56289, 0.0]]]
])
def test_bounding_box_xy(coords, expected):
    assert expected == bounding_box_xy(coords)
