from compas.tolerance import TOL
from compas.tolerance import Tolerance
from compas.geometry import Point


def test_tolerance_default_tolerance():
    assert TOL.precision == Tolerance.PRECISION
    assert TOL.precision == 3


def test_tolerance_creates_independent_instances():
    """Test that Tolerance() creates independent instances, not the singleton."""
    tol1 = Tolerance(absolute=0.01)
    tol2 = Tolerance(absolute=0.02)

    # Each instance is independent
    assert tol1 is not tol2
    assert tol1.absolute == 0.01
    assert tol2.absolute == 0.02

    # TOL is unchanged
    assert TOL.absolute == Tolerance.ABSOLUTE


def test_tolerance_update():
    """Test that TOL.update() explicitly modifies global state."""
    original = TOL.absolute
    try:
        TOL.update(absolute=0.001)
        assert TOL.absolute == 0.001
    finally:
        TOL.reset()
        assert TOL.absolute == original


def test_tolerance_temporary_context_manager():
    """Test that TOL.temporary() provides scoped changes."""
    original = TOL.absolute
    assert TOL.absolute == Tolerance.ABSOLUTE

    with TOL.temporary(absolute=0.01, precision=6):
        assert TOL.absolute == 0.01
        assert TOL.precision == 6

    # After context exit, values are restored
    assert TOL.absolute == original
    assert TOL.precision == Tolerance.PRECISION


def test_tolerance_temporary_restores_on_exception():
    """Test that temporary() restores values even if an exception occurs."""
    original = TOL.absolute

    try:
        with TOL.temporary(absolute=0.01):
            assert TOL.absolute == 0.01
            raise ValueError("test exception")
    except ValueError:
        pass

    # Values are restored despite the exception
    assert TOL.absolute == original


def test_tolerance_temporary_restores_unit():
    """Test that temporary() restores values even if an exception occurs."""
    original = TOL.unit

    with TOL.temporary(unit="MM"):
        assert TOL.unit == "MM"

    assert TOL.unit == original


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
