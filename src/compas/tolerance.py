"""
The tolerance module provides functionality to deal with tolerances consistently across all other COMPAS packages.

The module provides:

- `Tolerance`: A class for tolerance settings that can be instantiated independently.
- `TOL`: The global tolerance instance used throughout COMPAS (in-process).

To modify global tolerance settings, use the explicit methods on `TOL`:

- `TOL.update(...)` - Update specific tolerance values
- `TOL.reset()` - Reset to default values
- `TOL.temporary(...)` - Context manager for temporary changes

Examples
--------
>>> from compas.tolerance import TOL, Tolerance
>>> # Create an independent tolerance instance
>>> my_tol = Tolerance(absolute=0.01)
>>> my_tol.absolute
0.01
>>> # Global TOL is unchanged
>>> TOL.absolute
1e-09
>>> # To modify global state, use update()
>>> TOL.update(absolute=0.001)
>>> TOL.absolute
0.001
>>> TOL.reset()

"""

from collections.abc import Iterable
from collections.abc import Iterator
from collections.abc import Mapping
from contextlib import contextmanager
from decimal import Decimal
from itertools import zip_longest
from typing import Any
from typing import Self
from typing import TypeGuard
from typing import cast

from compas._typing import CoordinateType
from compas.data import Data

type ToleranceValue = str | float | int
type NestedNumbers = Iterable[float | NestedNumbers]


def _is_nested_numbers(value: object) -> TypeGuard[NestedNumbers]:
    return hasattr(value, "__iter__")


class Tolerance(Data):
    """Tolerance settings for geometric operations.

    Parameters
    ----------
    unit
        The unit of the tolerance settings.
    absolute
        The absolute tolerance. Default is `ABSOLUTE`.
    relative
        The relative tolerance. Default is `RELATIVE`.
    angular
        The angular tolerance. Default is `ANGULAR`.
    approximation
        The tolerance used in approximation processes. Default is `APPROXIMATION`.
    precision
        The precision used when converting numbers to strings. Default is `PRECISION`.
    lineardeflection
        The maximum distance between a curve/surface and its polygonal approximation.
        Default is `LINEARDEFLECTION`.
    angulardeflection
        The maximum curvature deviation. Default is `ANGULARDEFLECTION`.
    name
        The name of the tolerance settings.

    Notes
    -----
    The absolute tolerance is used to determine when a number is small enough to be considered zero.
    The relative tolerance determines the allowable deviation between two values for the values to be considered equal.
    The relative tolerance is defined as a fraction of one of the two values.
    This value is called the "true value".
    By convention, the second value is considered the "true value" by the comparison functions of this class.

    Each call to `Tolerance(...)` creates an independent instance. To modify the global
    tolerance settings used throughout COMPAS, use the explicit methods on `TOL`:

    - `TOL.update(...)` - Update specific tolerance values
    - `TOL.reset()` - Reset all values to defaults
    - `TOL.temporary(...)` - Context manager for temporary changes

    Examples
    --------
    Create an independent tolerance instance:

    >>> tol = Tolerance(absolute=0.01)
    >>> tol.absolute
    0.01

    The global TOL is separate:

    >>> from compas.tolerance import TOL
    >>> TOL.absolute  # unchanged
    1e-09

    Modify global state explicitly:

    >>> TOL.update(absolute=0.001)
    >>> TOL.absolute
    0.001
    >>> TOL.reset()

    """

    SUPPORTED_UNITS = ["M", "MM"]
    """Default tolerances are defined in relation to length units.

    Currently, only meters ("M") and millimeters ("MM") are supported.

    """

    ABSOLUTE = 1e-9
    """Determines when a number is small enough to be considered zero.
    """

    RELATIVE = 1e-6
    """Determines the accuracy of comparing a computed value to a true value.
    """

    ANGULAR = 1e-6
    """Determines when the difference between two angles is effectively zero.
    """

    APPROXIMATION = 1e-3
    """The tolerance used in approximation processes.
    """

    PRECISION = 3
    """The precision used when converting numbers to strings.

    The precision used when converting numbers to strings.
    Positive numbers correspond to the number of digits after the decimal point.
    Negative numbers correspond to the number of digits before the decimal point.
    Zero precision is not allowed.

    """

    LINEARDEFLECTION = 1e-3
    """The maximum distance deviation of a polygonal approximation.

    This is used by the viewer to determine the mesh and polyline resolution of curves and surfaces for visualisation.

    """

    ANGULARDEFLECTION = 1e-1
    """The maximum curvature deviation of a polygonal approximation.

    This is used by the viewer to determine the mesh and polyline resolution of curves and surfaces for visualisation.

    """

    # =============================================================================
    # Data
    # =============================================================================

    @property
    def __data__(self) -> dict[str, Any]:
        return {
            "unit": self.unit,
            "absolute": self.absolute,
            "relative": self.relative,
            "angular": self.angular,
            "approximation": self.approximation,
            "precision": self.precision,
            "lineardeflection": self.lineardeflection,
            "angulardeflection": self.angulardeflection,
        }

    @classmethod
    def __from_data__(cls, data: dict[str, Any]) -> Self:
        tol = cls()
        tol.unit = data["unit"]
        tol.absolute = data["absolute"]
        tol.relative = data["relative"]
        tol.angular = data["angular"]
        tol.approximation = data["approximation"]
        tol.precision = data["precision"]
        tol.lineardeflection = data["lineardeflection"]
        tol.angulardeflection = data["angulardeflection"]
        return tol

    # =============================================================================
    # Dunder methods
    # =============================================================================

    def __init__(
        self,
        unit: str = "M",
        absolute: float | None = None,
        relative: float | None = None,
        angular: float | None = None,
        approximation: float | None = None,
        precision: int | None = None,
        lineardeflection: float | None = None,
        angulardeflection: float | None = None,
        name: str | None = None,
    ) -> None:
        super().__init__(name=name)
        self._unit: str | None = None
        self._absolute: float | None = None
        self._relative: float | None = None
        self._angular: float | None = None
        self._approximation: float | None = None
        self._precision: int | None = None
        self._lineardeflection: float | None = None
        self._angulardeflection: float | None = None

        if unit is not None:
            self.unit = unit
        if absolute is not None:
            self.absolute = absolute
        if relative is not None:
            self.relative = relative
        if angular is not None:
            self.angular = angular
        if approximation is not None:
            self.approximation = approximation
        if precision is not None:
            self.precision = precision
        if lineardeflection is not None:
            self.lineardeflection = lineardeflection
        if angulardeflection is not None:
            self.angulardeflection = angulardeflection

    def __repr__(self) -> str:
        return "Tolerance(unit='{}', absolute={}, relative={}, angular={}, approximation={}, precision={}, lineardeflection={}, angulardeflection={})".format(
            self.unit,
            self.absolute,
            self.relative,
            self.angular,
            self.approximation,
            self.precision,
            self.lineardeflection,
            self.angulardeflection,
        )

    # =============================================================================
    # Properties
    # =============================================================================

    @property
    def unit(self) -> str:
        """The length unit used to select default tolerance values."""
        if not self._unit:
            return "M"
        return self._unit

    @unit.setter
    def unit(self, value: str) -> None:
        if value not in ["M", "MM"]:
            raise ValueError("Invalid unit: {}".format(value))
        self._unit = value

    @property
    def absolute(self) -> float:
        """The absolute tolerance used for scalar comparisons."""
        if self._absolute is None:
            return self.ABSOLUTE
        return self._absolute

    @absolute.setter
    def absolute(self, value: float) -> None:
        self._absolute = value

    @property
    def relative(self) -> float:
        """The relative tolerance used for scalar comparisons."""
        if self._relative is None:
            return self.RELATIVE
        return self._relative

    @relative.setter
    def relative(self, value: float) -> None:
        self._relative = value

    @property
    def angular(self) -> float:
        """The absolute tolerance used for angular comparisons."""
        if self._angular is None:
            return self.ANGULAR
        return self._angular

    @angular.setter
    def angular(self, value: float) -> None:
        self._angular = value

    @property
    def approximation(self) -> float:
        """The tolerance used by approximation algorithms."""
        if self._approximation is None:
            return self.APPROXIMATION
        return self._approximation

    @approximation.setter
    def approximation(self, value: float) -> None:
        self._approximation = value

    @property
    def precision(self) -> int:
        """The decimal precision used to format numbers and geometric keys."""
        if self._precision is None:
            return self.PRECISION
        return self._precision

    @precision.setter
    def precision(self, value: int) -> None:
        if value == 0:
            raise ValueError("Precision cannot be zero.")
        self._precision = value

    @property
    def lineardeflection(self) -> float:
        """The maximum linear deviation used for discretization."""
        if self._lineardeflection is None:
            return self.LINEARDEFLECTION
        return self._lineardeflection

    @lineardeflection.setter
    def lineardeflection(self, value: float) -> None:
        self._lineardeflection = value

    @property
    def angulardeflection(self) -> float:
        """The maximum angular deviation used for discretization."""
        if self._angulardeflection is None:
            return self.ANGULARDEFLECTION
        return self._angulardeflection

    @angulardeflection.setter
    def angulardeflection(self, value: float) -> None:
        self._angulardeflection = value

    # =============================================================================
    # Methods
    # =============================================================================

    def reset(self) -> None:
        """Reset all precision settings to their default values."""
        self._absolute = None
        self._relative = None
        self._angular = None
        self._approximation = None
        self._precision = None
        self._lineardeflection = None
        self._angulardeflection = None

    def update_from_dict(self, tolerance: Mapping[str, ToleranceValue]) -> None:
        """Update the tolerance from the key-value pairs found in a dict.

        Parameters
        ----------
        tolerance
            A dictionary containing named tolerance values.

        """
        for name in tolerance:
            if hasattr(self, name):
                setattr(self, name, tolerance[name])

    def update(
        self,
        unit: str | None = None,
        absolute: float | None = None,
        relative: float | None = None,
        angular: float | None = None,
        approximation: float | None = None,
        precision: int | None = None,
        lineardeflection: float | None = None,
        angulardeflection: float | None = None,
    ) -> None:
        """Update tolerance settings.

        Only the provided parameters will be updated; others remain unchanged.
        Use this method to explicitly modify tolerance settings.

        Parameters
        ----------
        unit
            The unit of the tolerance settings.
        absolute
            The absolute tolerance.
        relative
            The relative tolerance.
        angular
            The angular tolerance.
        approximation
            The tolerance used in approximation processes.
        precision
            The precision used when converting numbers to strings.
        lineardeflection
            The maximum distance between a curve/surface and its polygonal approximation.
        angulardeflection
            The maximum curvature deviation.

        Examples
        --------
        >>> from compas.tolerance import TOL
        >>> TOL.update(absolute=0.001, precision=6)
        >>> TOL.absolute
        0.001
        >>> TOL.precision
        6
        >>> TOL.reset()

        """
        if unit is not None:
            self.unit = unit
        if absolute is not None:
            self.absolute = absolute
        if relative is not None:
            self.relative = relative
        if angular is not None:
            self.angular = angular
        if approximation is not None:
            self.approximation = approximation
        if precision is not None:
            self.precision = precision
        if lineardeflection is not None:
            self.lineardeflection = lineardeflection
        if angulardeflection is not None:
            self.angulardeflection = angulardeflection

    @contextmanager
    def temporary(
        self,
        unit: str | None = None,
        absolute: float | None = None,
        relative: float | None = None,
        angular: float | None = None,
        approximation: float | None = None,
        precision: int | None = None,
        lineardeflection: float | None = None,
        angulardeflection: float | None = None,
    ) -> Iterator[Self]:
        """Context manager for temporarily changing tolerance settings.

        The original settings are automatically restored when the context exits,
        even if an exception occurs.

        Parameters
        ----------
        unit
            The unit of the tolerance settings.
        absolute
            The absolute tolerance.
        relative
            The relative tolerance.
        angular
            The angular tolerance.
        approximation
            The tolerance used in approximation processes.
        precision
            The precision used when converting numbers to strings.
        lineardeflection
            The maximum distance between a curve/surface and its polygonal approximation.
        angulardeflection
            The maximum curvature deviation.

        Yields
        ------
        `Tolerance`
            The tolerance instance with temporary settings applied.

        Examples
        --------
        >>> from compas.tolerance import TOL
        >>> TOL.absolute
        1e-09
        >>> with TOL.temporary(absolute=0.01):
        ...     TOL.absolute
        0.01
        >>> TOL.absolute
        1e-09

        """
        # Save current state
        saved = {
            "unit": self.unit,
            "absolute": self.absolute,
            "relative": self.relative,
            "angular": self.angular,
            "approximation": self.approximation,
            "precision": self.precision,
            "lineardeflection": self.lineardeflection,
            "angulardeflection": self.angulardeflection,
        }
        try:
            # Apply temporary changes
            self.update(
                unit=unit,
                absolute=absolute,
                relative=relative,
                angular=angular,
                approximation=approximation,
                precision=precision,
                lineardeflection=lineardeflection,
                angulardeflection=angulardeflection,
            )
            yield self
        finally:
            # Restore original state
            self._unit = saved["unit"]
            self._absolute = saved["absolute"]
            self._relative = saved["relative"]
            self._angular = saved["angular"]
            self._approximation = saved["approximation"]
            self._precision = saved["precision"]
            self._lineardeflection = saved["lineardeflection"]
            self._angulardeflection = saved["angulardeflection"]

    def tolerance(self, truevalue: float, rtol: float, atol: float) -> float:
        """Compute the tolerance for a comparison.

        Parameters
        ----------
        truevalue
            The true value of the comparison.
        rtol
            The relative tolerance.
        atol
            The absolute tolerance.

        Returns
        -------
        float
            The tolerance.

        Examples
        --------
        >>> tol = Tolerance()
        >>> tol.tolerance(1.0, 0.001, 1e-06)
        0.001001
        >>> tol.tolerance(10.0, 0.001, 1e-06)
        0.010001
        >>> tol.tolerance(10.0, 0.001, 1e-08)
        0.01000001

        """
        return rtol * abs(truevalue) + atol

    def compare(self, a: float, b: float, rtol: float, atol: float) -> bool:
        """Compare two values.

        Parameters
        ----------
        a
            The first value.
        b
            The second value.
        rtol
            The relative tolerance.
        atol
            The absolute tolerance.

        Returns
        -------
        bool
            `True` if the values are close enough to be considered equal.
            `False` otherwise.

        Notes
        -----
        In this comparison, `b` is considered the "true value".
        This means that the relative part of the tolerance is computed as a fraction of `b`.

        Examples
        --------
        >>> tol = Tolerance()
        >>> tol.compare(1.0, 1.001, 0.001, 1e-06)
        True
        >>> tol.compare(1.0, 1.001, 0.0001, 1e-06)
        False

        """
        return abs(a - b) <= self.tolerance(b, rtol, atol)

    def is_zero(self, a: float, tol: float | None = None) -> bool:
        """Check if a value is close enough to zero to be considered zero.

        Parameters
        ----------
        a
            The value.
        tol
            The absolute tolerance.
            Default is `None`, in which case `self.absolute` is used.

        Returns
        -------
        bool
            `True` if the value is small enough to be considered zero.
            `False` otherwise.

        Examples
        --------
        >>> tol = Tolerance()
        >>> tol.is_zero(1e-10)
        True
        >>> tol.is_zero(1e-05)
        False

        """
        tol = self.absolute if tol is None else tol
        return abs(a) <= tol

    def is_positive(self, a: float, tol: float | None = None) -> bool:
        """Check if a value can be considered a strictly positive number.

        Parameters
        ----------
        a
            The value.
        tol
            The absolute tolerance.
            Default is `None`, in which case `self.absolute` is used.

        Returns
        -------
        bool
            `True` if the value is small enough to be considered zero.
            `False` otherwise.

        Examples
        --------
        >>> tol = Tolerance()
        >>> tol.is_positive(1e-07)
        True
        >>> tol.is_positive(1e-10)
        False

        """
        tol = self.absolute if tol is None else tol
        return a > tol

    def is_negative(self, a: float, tol: float | None = None) -> bool:
        """Check if a value can be considered a strictly negative number.

        Parameters
        ----------
        a
            The value.
        tol
            The absolute tolerance.
            Default is `None`, in which case `self.absolute` is used.

        Returns
        -------
        bool
            `True` if the value is small enough to be considered zero.
            `False` otherwise.

        Examples
        --------
        >>> tol = Tolerance()
        >>> tol.is_negative(-1e-07)
        True
        >>> tol.is_negative(-1e-10)
        False

        """
        tol = self.absolute if tol is None else tol
        return a < -tol

    def is_between(self, value: float, minval: float, maxval: float, atol: float | None = None) -> bool:
        """Check if a value is between two other values.

        Parameters
        ----------
        value
            The value.
        minval
            The minimum value.
        maxval
            The maximum value.
        atol
            The absolute tolerance.
            Default is `None`, in which case `self.absolute` is used.

        Returns
        -------
        bool
            `True` if the value is between the two other values.
            `False` otherwise.

        Examples
        --------
        >>> tol = Tolerance()
        >>> tol.is_between(0.5, 0.0, 1.0)
        True
        >>> tol.is_between(1.5, 0.0, 1.0)
        False

        """
        atol = self.absolute if atol is None else atol
        return minval - atol <= value <= maxval + atol

    def is_close(self, a: float, b: float, rtol: float | None = None, atol: float | None = None) -> bool:
        """Check if two values are close enough to be considered equal.

        Parameters
        ----------
        a
            The first value.
        b
            The second value.
        rtol
            The relative tolerance.
            Default is `None`, in which case `self.relative` is used.
        atol
            The absolute tolerance.
            Default is `None`, in which case `self.absolute` is used.

        Returns
        -------
        bool
            `True` if the values are close enough to be considered equal.
            `False` otherwise.

        Examples
        --------
        >>> tol = Tolerance()

        >>> tol.is_close(1.0, 1.0 + 1e-5)
        False
        >>> tol.is_close(1.0, 1.0 + 1e-6)
        True

        >>> tol.is_close(0.1, 0.1 + 1e-5)
        False
        >>> tol.is_close(0.1, 0.1 + 1e-6)
        False
        >>> tol.is_close(0.1, 0.1 + 1e-7)
        True

        >>> tol.is_close(0, 0 + 1e-5)
        False
        >>> tol.is_close(0, 0 + 1e-6)
        False
        >>> tol.is_close(0, 0 + 1e-7)
        False
        >>> tol.is_close(0, 0 + 1e-8)
        False
        >>> tol.is_close(0, 0 + 1e-9)
        True

        """
        rtol = self.relative if rtol is None else rtol
        atol = self.absolute if atol is None else atol
        return self.compare(a, b, rtol, atol)

    def is_allclose(self, A: NestedNumbers, B: NestedNumbers, rtol: float | None = None, atol: float | None = None) -> bool:
        """Check if two possibly nested iterables are element-wise close.

        Parameters
        ----------
        A
            The first iterable of values.
        B
            The second iterable of values.
        rtol
            The relative tolerance.
            Default is `None`, in which case `self.relative` is used.
        atol
            The absolute tolerance.
            Default is `None`, in which case `self.absolute` is used.

        Returns
        -------
        bool
            `True` if the values are close enough to be considered equal.
            `False` otherwise.

        Examples
        --------
        >>> tol = Tolerance()
        >>> tol.is_allclose([1.0, 1.0], [1.0 + 1e-5, 1.0 + 1e-6])
        False
        >>> tol.is_allclose([1.0, 1.0], [1.0 + 1e-6, 1.0 + 1e-6])
        True
        >>> tol.is_allclose([0.0, 0.0], [0.0 + 1e-8, 0.0 + 1e-9])
        False
        >>> tol.is_allclose([0.0, 0.0], [0.0 + 1e-9, 0.0 + 1e-9])
        True
        >>> tol.is_allclose([1.0], [1.0, 2.0])
        False

        """
        rtol = self.relative if rtol is None else rtol
        atol = self.absolute if atol is None else atol
        missing = object()
        for a, b in zip_longest(A, B, fillvalue=missing):
            if a is missing or b is missing:
                return False
            if _is_nested_numbers(a):
                if not _is_nested_numbers(b) or not self.is_allclose(a, b, rtol, atol):
                    return False
            elif _is_nested_numbers(b):
                return False
            elif not self.compare(cast(float, a), cast(float, b), rtol, atol):
                return False
        return True

    def is_angle_zero(self, a: float, tol: float | None = None) -> bool:
        """Check if an angle is close enough to zero to be considered zero.

        Parameters
        ----------
        a
            The angle in radians.
        tol
            The absolute tolerance.
            Default is `None`, in which case `self.angular` is used.

        Returns
        -------
        bool
            `True` if the angle is small enough to be considered zero.
            `False` otherwise.

        Examples
        --------
        >>> tol = Tolerance()
        >>> tol.is_angle_zero(1e-07)
        True
        >>> tol.is_angle_zero(1e-05)
        False

        """
        tol = self.angular if tol is None else tol
        return abs(a) <= tol

    def is_angles_close(self, a: float, b: float, tol: float | None = None) -> bool:
        """Check if two angles are close enough to be considered equal.

        Parameters
        ----------
        a
            The first angle in radians.
        b
            The second angle in radians.
        tol
            The absolute tolerance.
            Default is `None`, in which case `self.angular` is used.

        Returns
        -------
        bool
            `True` if the angles are close enough to be considered equal.
            `False` otherwise.

        Examples
        --------
        >>> tol = Tolerance()
        >>> tol.is_angles_close(0.0, 1e-07)
        True
        >>> tol.is_angles_close(0.0, 1e-05)
        False

        """
        tol = self.angular if tol is None else tol
        return abs(a - b) <= tol

    def geometric_key(self, xyz: CoordinateType, precision: int | None = None, sanitize: bool = True) -> str:
        """Compute the geometric key of a point.

        Parameters
        ----------
        xyz
            The XYZ coordinates of the point.
        precision
            The precision used when converting numbers to strings.
            Default is `None`, in which case `self.precision` is used.
        sanitize
            If `True`, minus signs ("-") will be removed from values that are equal to zero up to the given precision.

        Returns
        -------
        str
            The geometric key.

        Raises
        ------
        ValueError
            If the precision is zero.

        Examples
        --------
        >>> tol = Tolerance()
        >>> tol.geometric_key([1.0, 2.0, 3.0])
        '1.000,2.000,3.000'

        >>> tol = Tolerance()
        >>> tol.geometric_key([1.05725, 2.0195, 3.001], precision=3)
        '1.057,2.019,3.001'

        >>> tol = Tolerance()
        >>> tol.geometric_key([1.0, 2.0, 3.0], precision=-1)
        '1,2,3'

        >>> tol = Tolerance()
        >>> tol.geometric_key([1.0, 2.0, 3.0], precision=-3)
        '0,0,0'

        >>> tol = Tolerance()
        >>> tol.geometric_key([1103, 205, 30145], precision=-3)
        '1100,200,30100'

        """
        x, y, z = xyz
        if precision is None:
            precision = self.precision

        if precision == 0:
            raise ValueError("Precision cannot be zero.")

        if precision == -1:
            return "{:d},{:d},{:d}".format(int(x), int(y), int(z))

        if precision < -1:
            precision = -precision - 1
            factor = 10**precision
            return "{:d},{:d},{:d}".format(
                int(round(x / factor) * factor),
                int(round(y / factor) * factor),
                int(round(z / factor) * factor),
            )

        if sanitize:
            minzero = "-{0:.{1}f}".format(0.0, precision)
            if "{0:.{1}f}".format(x, precision) == minzero:
                x = 0.0
            if "{0:.{1}f}".format(y, precision) == minzero:
                y = 0.0
            if "{0:.{1}f}".format(z, precision) == minzero:
                z = 0.0

        return "{0:.{3}f},{1:.{3}f},{2:.{3}f}".format(x, y, z, precision)

    def geometric_key_xy(self, xy: CoordinateType, precision: int | None = None, sanitize: bool = True) -> str:
        """Compute the geometric key of a point in the XY plane.

        Parameters
        ----------
        xy
            The XY coordinates of the point.
        precision
            The precision used when converting numbers to strings.
            Default is `None`, in which case `self.precision` is used.
        sanitize
            If `True`, minus signs ("-") will be removed from values that are equal to zero up to the given precision.

        Returns
        -------
        str
            The geometric key in XY.

        Raises
        ------
        ValueError
            If the precision is zero.

        Examples
        --------
        >>> tol = Tolerance()
        >>> tol.geometric_key_xy([1.0, 2.0])
        '1.000,2.000'

        >>> tol = Tolerance()
        >>> tol.geometric_key_xy([1.05725, 2.0195], precision=3)
        '1.057,2.019'

        >>> tol = Tolerance()
        >>> tol.geometric_key_xy([1.0, 2.0], precision=-1)
        '1,2'

        >>> tol = Tolerance()
        >>> tol.geometric_key_xy([1.0, 2.0], precision=-3)
        '0,0'

        >>> tol = Tolerance()
        >>> tol.geometric_key_xy([1103, 205], precision=-3)
        '1100,200'

        """
        x = xy[0]
        y = xy[1]

        if precision is None:
            precision = self.precision

        if precision == 0:
            raise ValueError("Precision cannot be zero.")

        if precision == -1:
            return "{:d},{:d}".format(int(x), int(y))

        if precision < -1:
            precision = -precision - 1
            factor = 10**precision
            return "{:d},{:d}".format(
                int(round(x / factor) * factor),
                int(round(y / factor) * factor),
            )

        if sanitize:
            minzero = "-{0:.{1}f}".format(0.0, precision)
            if "{0:.{1}f}".format(x, precision) == minzero:
                x = 0.0
            if "{0:.{1}f}".format(y, precision) == minzero:
                y = 0.0

        return "{0:.{2}f},{1:.{2}f}".format(x, y, precision)

    def format_number(self, number: float, precision: int | None = None) -> str:
        """Format a number as a string.

        Parameters
        ----------
        number
            The number.
        precision
            The precision used when converting numbers to strings.
            Default is `None`, in which case `self.precision` is used.

        Returns
        -------
        str
            The formatted number.

        Examples
        --------
        >>> tol = Tolerance()
        >>> tol.format_number(1.0)
        '1.000'
        >>> tol.format_number(1.0, precision=3)
        '1.000'
        >>> tol.format_number(1.0, precision=-1)
        '1'
        >>> tol.format_number(1.0, precision=-3)
        '0'
        >>> tol.format_number(12345, precision=-3)
        '12300'

        """
        if precision is None:
            precision = self.precision

        if precision == 0:
            raise ValueError("Precision cannot be zero.")

        if precision == -1:
            return "{:d}".format(int(round(number)))

        if precision < -1:
            precision = -precision - 1
            factor = 10**precision
            return "{:d}".format(int(round(number / factor) * factor))

        return "{0:.{1}f}".format(number, precision)

    def precision_from_tolerance(self, tol: float | None = None) -> int:
        """Compute decimal precision from a positive sub-unit tolerance.

        Parameters
        ----------
        tol
            The tolerance.
            Default is `None`, in which case `self.absolute` is used.

        Returns
        -------
        int
            The precision.

        Raises
        ------
        ValueError
            If the tolerance is not greater than zero and smaller than one.

        Examples
        --------
        >>> tol = Tolerance()
        >>> tol.precision_from_tolerance(1e-07)
        7
        >>> tol.precision_from_tolerance(1e-05)
        5
        >>> tol.precision_from_tolerance(1e-03)
        3
        >>> tol.precision_from_tolerance(1e-01)
        1

        """
        tol = self.absolute if tol is None else tol
        if not 0 < tol < 1:
            raise ValueError("The tolerance should be greater than zero and smaller than one.")
        return abs(int(Decimal(str(tol)).as_tuple().exponent))


TOL = Tolerance()
