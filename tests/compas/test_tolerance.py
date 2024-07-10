from compas.tolerance import TOL
from compas.tolerance import Tolerance
from compas.geometry import Point


def test_tolerance_default_tolerance():
    assert TOL.precision == Tolerance.PRECISION
    assert TOL.precision == 3


def test_tolerance_format_number():
    assert TOL.format_number(0, precision=3) == "0.000"
    assert TOL.format_number(0.5, precision=3) == "0.500"
    assert TOL.format_number(float(0), precision=3) == "0.000"


def test_tolerance_format_number_with_default_precision():
    assert TOL.format_number(0) == "0.000"
    assert TOL.format_number(0.5) == "0.500"
    assert TOL.format_number(float(0)) == "0.000"


def test_tolerance_format_point():
    point = Point(0, 0, 0)
    assert str(point) == "Point(x=0.000, y=0.000, z=0.000)"
