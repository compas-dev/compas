from compas.tolerance import TOL
from compas.tolerance import Tolerance
from compas.geometry import Point
import pytest


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


def test_tolerance_preserves_explicit_zero_values():
    tol = Tolerance(
        absolute=0.0,
        relative=0.0,
        angular=0.0,
        approximation=0.0,
        lineardeflection=0.0,
        angulardeflection=0.0,
    )

    assert tol.absolute == 0.0
    assert tol.relative == 0.0
    assert tol.angular == 0.0
    assert tol.approximation == 0.0
    assert tol.lineardeflection == 0.0
    assert tol.angulardeflection == 0.0
    assert not tol.is_close(1.0, 1.0 + 1e-12)
    assert not tol.is_zero(1e-12)


def test_tolerance_explicit_zero_overrides_defaults():
    tol = Tolerance()

    assert not tol.is_close(1.0, 1.0 + 1e-12, rtol=0.0, atol=0.0)
    assert not tol.is_zero(1e-12, tol=0.0)


def test_tolerance_allclose_accepts_generators():
    left = (value for value in [1.0, 2.0, 3.0])
    right = (value for value in [1.0, 2.0, 3.0])

    assert TOL.is_allclose(left, right)


@pytest.mark.parametrize(
    ("left", "right"),
    [
        ([1.0], [1.0, 2.0]),
        ([1.0, 2.0], [1.0]),
        ([[1.0]], [[1.0, 2.0]]),
        ([[1.0]], [1.0]),
        ([1.0], [[1.0]]),
    ],
)
def test_tolerance_allclose_rejects_different_shapes(left, right):
    assert not TOL.is_allclose(left, right)


def test_tolerance_deserialization_preserves_subclasses():
    class CustomTolerance(Tolerance):
        pass

    tol = CustomTolerance.__from_data__(Tolerance().__data__)

    assert type(tol) is CustomTolerance


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


def test_tolerance_rejects_zero_precision():
    with pytest.raises(ValueError):
        TOL.format_number(1.0, precision=0)

    with pytest.raises(ValueError):
        TOL.geometric_key((1.0, 2.0, 3.0), precision=0)


@pytest.mark.parametrize("tolerance", [-1.0, 0.0, 1.0, 10.0])
def test_precision_from_tolerance_rejects_values_outside_domain(tolerance):
    with pytest.raises(ValueError, match="greater than zero and smaller than one"):
        TOL.precision_from_tolerance(tolerance)


def test_tolerance_format_point():
    point = Point(0, 0, 0)
    assert str(point) == "Point(x=0.000, y=0.000, z=0.000)"
