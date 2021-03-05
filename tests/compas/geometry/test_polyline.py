import compas
import pytest
from compas.geometry import Polyline, Point
import math


@pytest.mark.parametrize('coords,expected', [
    ([[0.0, 0.0, 0.0], [100.0, 0.0, 0.0]], [[0.0, 0.0, 0.0], [20.0, 0.0, 0.0], [40.0, 0.0, 0.0], [60.0, 0.0, 0.0], [80.0, 0.0, 0.0], [100.0, 0.0, 0.0]]),
    ([[0.0, 0.0, 0.0], [100.0, 0.0, 0.0], [300.0, 0.0, 0.0]], [[0.0, 0.0, 0.0], [60.0, 0.0, 0.0], [120.0, 0.0, 0.0], [180.0, 0.0, 0.0], [240.0, 0.0, 0.0], [300.0, 0.0, 0.0]]),
    ([[0.0, 0.0, 0.0], [200.0, 0.0, 0.0], [200.0, 200.0, 0.0], [0.0, 200.0, 0.0], [0.0, 0.0, 0.0]], [
     [0.0, 0.0, 0.0], [160.0, 0.0, 0.0], [200.0, 120.0, 0.0], [120.0, 200.0, 0.0], [0.0, 160.0, 0.0], [0.0, 0.0, 0.0]])
])
def test_polyline_divide(coords, expected):
    assert expected == Polyline(coords).divide_polyline(5)


@pytest.mark.parametrize('coords,expected', [
    ([[0.0, 0.0, 0.0], [100.0, 0.0, 0.0]], [[0.0, 0.0, 0.0], [100.0, 0.0, 0.0]]),
    ([[0.0, 0.0, 0.0], [100.0, 0.0, 0.0], [300.0, 0.0, 0.0]], [[0, 0, 0], [100, 0, 0], [200, 0, 0], [300, 0, 0]]),
    ([[0.0, 0.0, 0.0], [200.0, 0.0, 0.0], [200.0, 200.0, 0.0], [0.0, 200.0, 0.0], [0.0, 0.0, 0.0]], [[0, 0, 0], [
     100, 0, 0], [200, 0, 0], [200, 100, 0], [200, 200, 0], [100.0, 200, 0], [0, 200, 0], [0, 100.0, 0], [0, 0, 0]])
])
def test_polyline_divide_length(coords, expected):
    assert expected == Polyline(coords).divide_polyline_by_length(100)


@pytest.mark.parametrize('coords,expected', [
    ([[0.0, 0.0, 0.0], [100.0, 0.0, 0.0]], [[0.0, 0.0, 0.0], [80.0, 0.0, 0.0]]),
])
def test_polyline_divide_length_strict1(coords, expected):
    assert expected == Polyline(coords).divide_polyline_by_length(80)


@pytest.mark.parametrize('coords,expected', [
    ([[0.0, 0.0, 0.0], [100.0, 0.0, 0.0]], [[0.0, 0.0, 0.0], [80.0, 0.0, 0.0], [100.0, 0.0, 0.0]]),
])
def test_polyline_divide_length_strict2(coords, expected):
    assert expected == Polyline(coords).divide_polyline_by_length(80, False)


@pytest.mark.parametrize('coords, input, expected', [
    ([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 0.0]], math.pi/2, [Polyline([[0.0, 0.0, 0.0], [1, 0.0, 0.0]]),
                                                                                                        Polyline([[1, 0.0, 0.0], [1, 1, 0.0]]), Polyline([[1, 1, 0.0], [0.0, 1, 0.0]]), Polyline([[0.0, 1, 0.0], [0.0, 0.0, 0.0]])]),
])
def test_polyline_split_at_corners(coords, input, expected):
    assert expected == Polyline(coords).split_at_corners(input)


@pytest.mark.parametrize('coords, input, expected', [
    ([[0.0, 0.0, 0.0], [100.0, 0.0, 0.0]], [50, 0, 0], [1.0, 0.0, 0.0]),
    ([[0.0, 0.0, 0.0], [50.0, 0.0, 0.0], [100.0, 100.0, 0.0]], [50, 0, 0], [1.0, 0.0, 0.0]),
])
def test_polyline_tangent_at_point(coords, input, expected):
    assert expected == Polyline(coords).tangent_at_point_on_polyline(input)
