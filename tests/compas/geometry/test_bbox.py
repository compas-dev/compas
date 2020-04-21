import pytest

from compas.geometry import allclose
from compas.geometry import bounding_box
from compas.geometry import bounding_box_xy
from compas.geometry import oriented_bounding_box_numpy
from compas.geometry import oriented_bounding_box_xy_numpy


@pytest.mark.parametrize('coords,expected', [
    [[[0, 0], [1, 2], [-5, 6], [-3, 2], [0.5, -1]],
     [[-5, -1, 0.0], [1, -1, 0.0], [1, 6, 0.0], [-5, 6, 0.0]]],

    [[[6.74219, -53.57835], [6.74952, -53.57241], [6.75652, -53.56289], [6.74756, -53.56598], [6.73462, -53.57518]],
     [[6.73462, -53.57835, 0.0], [6.75652, -53.57835, 0.0], [6.75652, -53.56289, 0.0], [6.73462, -53.56289, 0.0]]]
])
def test_bounding_box_xy(coords, expected):
    assert expected == bounding_box_xy(coords)


@pytest.mark.parametrize('coords,expected', [
    [
        [[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]],
        [[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0], [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]]
    ]
])
def test_bounding_box(coords, expected):
    assert expected == bounding_box(coords)


@pytest.mark.parametrize('coords,expected', [
    [[[0, 0], [1, 2], [-5, 6], [-3, 2], [0.5, -1]],
     [[-6.129411764705883, 4.682352941176471], [0.5, -1.0], [2.1941176470588237, 0.976470588235294], [-4.435294117647059, 6.658823529411765]]],

    [[[6.74219, -53.57835], [6.74952, -53.57241], [6.75652, -53.56289], [6.74756, -53.56598], [6.73462, -53.57518]],
     [[6.754970846941253, -53.56071108254564], [6.73462, -53.57518], [6.738658767139154, -53.58086061378051], [6.759009614080408, -53.56639169632614]]]
])
def test_oriented_bounding_box_xy_numpy(coords, expected):
    assert expected == oriented_bounding_box_xy_numpy(coords)


@pytest.mark.parametrize('coords,expected', [
    [
        [[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]],
        [
            [0.0, 0.0, 1.0], [0.0, 1.0, 0.0], [1.0, 0.5, -0.5], [1.0, -0.5, 0.5],
            [-0.3333333333333333, -0.3333333333333333, 0.6666666666666667], [-0.3333333333333333, 0.6666666666666667, -0.33333333333333326],
            [0.6666666666666667, 0.1666666666666667, -0.8333333333333333], [0.6666666666666667, -0.8333333333333333, 0.16666666666666674]
        ]
    ]
])
def test_oriented_bounding_box_numpy(coords, expected):
    results = oriented_bounding_box_numpy(coords).tolist()
    for result, expected_values in zip(results, expected):
        assert allclose(result, expected_values, tol=1e-3)
