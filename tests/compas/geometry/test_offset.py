import pytest

from compas.geometry import allclose
from compas.geometry import offset_line
from compas.geometry import offset_polygon
from compas.geometry import offset_polyline

# ==============================================================================
# polygon
# ==============================================================================


@pytest.mark.parametrize(
    ("polygon", "distance", "tol", "output_polygon"),
    [(
        [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0], [0.0, 1.0, 0.0]], 0.10, 1e-6,
        [[0.1, 0.1, 0.0], [0.9, 0.1, 0.0], [0.9, 0.9, 0.0], [0.1, 0.9, 0.0]]
    )])
def test_offset_polygon(polygon, distance, tol, output_polygon):
    output_polygon = [v for v in output_polygon]
    assert allclose(offset_polygon(polygon, distance, tol), output_polygon)


@pytest.mark.parametrize(
    ("polygon", "distance", "tol", "output_polygon"),
    [(
        [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.5, 0.0]], [0.10], 1e-6,
        [[0.1, 0.1, 0.0], [0.9, 0.1, 0.0], [0.9, 0.9, 0.0], [0.1, 0.9, 0.0], [0.1, 0.5, 0.0]]
    )])
def test_offset_colinear_polygon(polygon, distance, tol, output_polygon):
    assert allclose(offset_polygon(polygon, distance, tol), output_polygon)

# ==============================================================================
# polyline
# ==============================================================================


@pytest.mark.parametrize(
    ("polyline", "distance", "normal", "tol"),
    [(
        [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0]], 1, [0.0, 0.0, 1.0], 1e-6
    )])
def test_offset_polyline_equals_offset_line(polyline, distance, normal, tol):
    output_line = [v for v in offset_line(polyline, distance, normal)]
    assert allclose(offset_polyline(polyline, distance, normal, tol), output_line)


@pytest.mark.parametrize(
    ("polyline", "distance", "normal", "tol", "output_polyline"),
    [(
        [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [2.0, 0.0, 0.0]], [(-0.05, -0.1), (-0.1, -0.15)], [0.0, 0.0, 1.0], 1e-6,
        [[0.0, -0.05, 0.0], [1.0, -0.1, 0.0], [2.0, -0.15, 0.0]]
    )])
def test_variable_offset_on_colinear_polyline(polyline, distance, normal, tol, output_polyline):
    output_polyline = [v for v in output_polyline]
    assert allclose(offset_polyline(polyline, distance, normal, tol), output_polyline)

# ==============================================================================
# line
# ==============================================================================


@pytest.mark.parametrize(
    ("line", "distance", "normal"),
    [(
        [[1.0, 0.0, 0.0], [1.0, 0.0, 0.0]], 1, [0.0, 0.0, 1.0]
    )])
def test_offset_line_zero_length(line, distance, normal):
    output_line = offset_line(line, distance, normal)
    assert allclose(line, output_line)
