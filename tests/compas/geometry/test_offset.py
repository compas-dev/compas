import pytest

from compas.geometry import Line
from compas.geometry import Polyline
from compas.geometry import Polygon
from compas.geometry.offset.offset import offset_polyline as c_offset_polyline
from compas.geometry import allclose

# ==============================================================================
# polygon
# ==============================================================================


@pytest.mark.parametrize(
    ("polygon", "distance", "tol", "output_polygon"),
    [
        (
            [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0], [0.0, 1.0, 0.0]],
            0.10,
            1e-6,
            [[0.1, 0.1, 0.0], [0.9, 0.1, 0.0], [0.9, 0.9, 0.0], [0.1, 0.9, 0.0]],
        )
    ],
)
def test_offset_polygon(polygon, distance, tol, output_polygon):
    input_polygon = Polygon(polygon)
    output_polygon = [v for v in output_polygon]
    assert allclose(input_polygon.offset(distance, tol=tol), output_polygon)


@pytest.mark.parametrize(
    ("polygon", "distance", "tol", "output_polygon"),
    [
        (
            [
                [0.0, 0.0, 0.0],
                [1.0, 0.0, 0.0],
                [1.0, 1.0, 0.0],
                [0.0, 1.0, 0.0],
                [0.0, 0.5, 0.0],
            ],
            0.10,
            1e-6,
            [
                [0.1, 0.1, 0.0],
                [0.9, 0.1, 0.0],
                [0.9, 0.9, 0.0],
                [0.1, 0.9, 0.0],
                [0.1, 0.5, 0.0],
            ],
        )
    ],
)
def test_offset_colinear_polygon(polygon, distance, tol, output_polygon):
    input_polygon = Polygon(polygon)
    assert allclose(input_polygon.offset(distance, tol=tol), output_polygon)


# ==============================================================================
# polyline
# ==============================================================================


@pytest.mark.parametrize(
    ("polyline", "distance", "normal", "tol"),
    [([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0]], 1, [0.0, 0.0, 1.0], 1e-6)],
)
def test_offset_polyline_equals_offset_line(polyline, distance, normal, tol):
    input_polyline = Polyline(polyline)
    output_polyline = [v for v in input_polyline.offset(distance, normal=normal)]
    assert allclose(input_polyline.offset(distance, normal=normal, tol=tol), output_polyline)


@pytest.mark.parametrize(
    ("polyline", "distance", "normal", "tol", "output_polyline"),
    [
        (
            [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [2.0, 0.0, 0.0]],
            [(-0.05, -0.1), (-0.1, -0.15)],
            [0.0, 0.0, 1.0],
            1e-6,
            [[0.0, -0.05, 0.0], [1.0, -0.1, 0.0], [2.0, -0.15, 0.0]],
        )
    ],
)
def test_variable_offset_on_colinear_polyline(polyline, distance, normal, tol, output_polyline):
    input_polyline = Polyline(polyline)
    output_polyline = [v for v in output_polyline]
    assert allclose(c_offset_polyline(input_polyline, distance, normal=normal, tol=tol), output_polyline)


# ==============================================================================
# line
# ==============================================================================


@pytest.mark.parametrize(
    ("line", "distance", "normal"),
    [([[1.0, 0.0, 0.0], [1.0, 0.0, 0.0]], 1, [0.0, 0.0, 1.0])],
)
def test_offset_line_zero_length(line, distance, normal):
    input_line = Line(*line)
    output_line = input_line.offset(distance, normal=normal)
    assert allclose(input_line, output_line)
