import json

import pytest

from compas.geometry import Curve
from compas.geometry import Line
from compas.geometry import LineCurve
from compas.geometry import Rotation


def test_linecurve_implements_curve_without_changing_line_primitive():
    assert issubclass(LineCurve, Curve)
    assert not issubclass(Line, Curve)


def test_linecurve_data_roundtrip():
    curve = LineCurve([0.0, 0.0, 0.0], [3.0, 4.0, 0.0])
    other = LineCurve.__from_data__(json.loads(json.dumps(curve.__data__)))

    assert other == curve
    assert other is not curve


def test_linecurve_properties_and_evaluation():
    curve = LineCurve([0.0, 0.0, 0.0], [3.0, 4.0, 0.0])

    assert curve.domain == (0.0, 1.0)
    assert curve.length == 5.0
    assert curve.direction == [0.6, 0.8, 0.0]
    assert curve.point_at(0.5) == [1.5, 2.0, 0.0]
    assert curve.tangent_at(0.5) == curve.direction
    assert curve.normal_at(0.5) is None
    assert curve.curvature_at(0.5) == [0.0, 0.0, 0.0]
    assert not curve.is_closed
    assert not curve.is_periodic

    with pytest.raises(ValueError):
        curve.point_at(-0.1)
    with pytest.raises(ValueError):
        curve.frame_at(0.5)


def test_linecurve_conversions_are_independent():
    line = Line([0.0, 0.0, 0.0], [1.0, 0.0, 0.0])
    curve = LineCurve.from_line(line)
    converted = curve.to_line()

    line.end = [2.0, 0.0, 0.0]
    converted.end = [3.0, 0.0, 0.0]

    assert curve.end == [1.0, 0.0, 0.0]


def test_linecurve_reverse_and_transform():
    curve = LineCurve([0.0, 0.0, 0.0], [1.0, 0.0, 0.0])
    curve.reverse()

    assert curve.start == [1.0, 0.0, 0.0]
    assert curve.end == [0.0, 0.0, 0.0]

    curve.transform(Rotation.from_axis_and_angle([0.0, 0.0, 1.0], 0.5 * 3.141592653589793))
    assert list(curve.start) == pytest.approx([0.0, 1.0, 0.0])
    assert list(curve.end) == pytest.approx([0.0, 0.0, 0.0])


@pytest.mark.parametrize(
    ("point", "expected", "parameter"),
    [
        ([-1.0, 1.0, 0.0], [0.0, 0.0, 0.0], 0.0),
        ([1.0, 1.0, 0.0], [1.0, 0.0, 0.0], 0.5),
        ([3.0, 1.0, 0.0], [2.0, 0.0, 0.0], 1.0),
    ],
)
def test_linecurve_closest_point_is_clamped_to_finite_domain(point, expected, parameter):
    curve = LineCurve([0.0, 0.0, 0.0], [2.0, 0.0, 0.0])

    closest, t = curve.closest_point(point, return_parameter=True)

    assert closest == expected
    assert t == parameter


def test_linecurve_division():
    curve = LineCurve([0.0, 0.0, 0.0], [4.0, 0.0, 0.0])

    parameters, points = curve.divide_by_count(2, return_points=True)
    assert parameters == [0.0, 0.5, 1.0]
    assert points == [[0.0, 0.0, 0.0], [2.0, 0.0, 0.0], [4.0, 0.0, 0.0]]

    parameters, points = curve.divide_by_length(1.5, return_points=True)
    assert parameters == [0.0, 0.375, 0.75]
    assert points == [[0.0, 0.0, 0.0], [1.5, 0.0, 0.0], [3.0, 0.0, 0.0]]

    with pytest.raises(ValueError):
        curve.divide_by_count(0)
    with pytest.raises(ValueError):
        curve.divide_by_length(0.0)


def test_linecurve_alternative_constructors_preserve_subclass():
    class CustomLineCurve(LineCurve):
        pass

    assert isinstance(CustomLineCurve.from_line(Line([0, 0, 0], [1, 0, 0])), CustomLineCurve)
    assert isinstance(CustomLineCurve.from_point_and_vector([0, 0, 0], [1, 0, 0]), CustomLineCurve)
    assert isinstance(CustomLineCurve.from_point_direction_length([0, 0, 0], [1, 0, 0], 1.0), CustomLineCurve)
