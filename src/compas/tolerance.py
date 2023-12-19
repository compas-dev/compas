from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


from compas.data import Data


class Tolerance(Data):
    """Tolerance settings for geometric operations.

    Parameters
    ----------
    unit : {"M", "MM"}, optional
        The unit of the tolerance settings.

    Attributes
    ----------
    unit : {"M", "MM"}
        The unit of the tolerance settings.
    absolute : float
        The absolute tolerance.
    relative : float
        The relative tolerance.
    angular : float
        The angular tolerance.

    Notes
    -----
    The absolute tolerance is used to determine when a number is small enough to be considered zero.
    The relative tolerance determines the allowable deviation between two values for the values to be considered equal.
    The relative tolerance is defined as a fraction of one of the two values.
    This value is called the "true value".
    By convention, the second value is considered the "true value" by the comparison functions of this class.

    Examples
    --------
    >>> tol = Tolerance()
    >>> tol.unit
    'M'
    >>> tol.absolute
    1e-09
    >>> tol.relative
    1e-06
    >>> tol.angular
    1e-06

    """

    ABSOLUTE = 1e-9
    """float: Determines when a number is small enough to be considered zero.
    """

    RELATIVE = 1e-6
    """float: Determines the accuracy of comparing a "computed value" to a "true value", as a fraction of the "true value".
    """

    ANGULAR = 1e-6
    """float: An absolute value that determines when the difference between two angles is small enough to be considered zero.
    """

    APPROXIMATION = 1e-3
    """float: The tolerance used in approximation processes.
    """

    def __init__(self, unit="M"):
        self._unit = None
        self._absolute = None
        self._relative = None
        self._angular = None
        self._approximation = None
        self.unit = unit

    @property
    def data(self):
        return {
            "unit": self.unit,
            "absolute": self.absolute,
            "relative": self.relative,
            "angular": self.angular,
            "approximation": self.approximation,
        }

    @classmethod
    def from_data(cls, data):
        tol = cls()
        tol.unit = data["unit"]
        tol.absolute = data["absolute"]
        tol.relative = data["relative"]
        tol.angular = data["angular"]
        tol.approximation = data["approximation"]
        return tol

    def reset(self):
        """Reset all precision settings to their default values."""
        self._absolute = None
        self._relative = None
        self._angular = None
        self._approximation = None

    @property
    def units(self):
        return self._unit

    @units.setter
    def units(self, value):
        if value not in ["M", "MM"]:
            raise ValueError("Invalid unit: {}".format(value))
        self._unit = value

    @property
    def absolute(self):
        if not self._absolute:
            return self.ABSOLUTE
        return self._absolute

    @absolute.setter
    def absolute(self, value):
        self._absolute = value

    @property
    def relative(self):
        if not self._relative:
            return self.RELATIVE
        return self._relative

    @relative.setter
    def relative(self, value):
        self._relative = value

    @property
    def angular(self):
        if not self._angular:
            return self.ANGULAR
        return self._angular

    @angular.setter
    def angular(self, value):
        self._angular = value

    @property
    def approximation(self):
        if not self._approximation:
            return self.APPROXIMATION
        return self._approximation

    @approximation.setter
    def approximation(self, value):
        self._approximation = value

    def tolerance(self, truevalue, rtol, atol):
        """Compute the tolerance for a comparison.

        Parameters
        ----------
        truevalue : float
            The true value of the comparison.
        rtol : float
            The relative tolerance.
        atol : float
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

    def compare(self, a, b, rtol, atol):
        """Compare two values.

        Parameters
        ----------
        a : float
            The first value.
        b : float
            The second value.
        rtol : float
            The relative tolerance.
        atol : float
            The absolute tolerance.

        Returns
        -------
        bool
            ``True`` if the values are close enough to be considered equal.
            ``False`` otherwise.

        Notes
        -----
        In this comparison, ``b`` is considered the "true value".
        This means that the relative part of the tolerance is computed as a fraction of ``b``.

        Examples
        --------
        >>> tol = Tolerance()
        >>> tol.compare(1.0, 1.001, 0.001, 1e-06)
        True
        >>> tol.compare(1.0, 1.001, 0.0001, 1e-06)
        False

        """
        return abs(a - b) <= self.tolerance(b, rtol, atol)

    def is_zero(self, a, tol=None):
        """Check if a value is close enough to zero to be considered zero.

        Parameters
        ----------
        a : float
            The value.
        tol : float, optional
            The absolute tolerance.
            Default is ``None``, in which case ``self.absolute`` is used.

        Returns
        -------
        bool
            ``True`` if the value is small enough to be considered zero.
            ``False`` otherwise.

        Examples
        --------
        >>> tol = Tolerance()
        >>> tol.is_zero(1e-10)
        True
        >>> tol.is_zero(1e-05)
        False

        """
        tol = tol or self.absolute
        return abs(a) <= tol

    def is_positive(self, a, tol=None):
        """Check if a value can be considered a strictly positive number.

        Parameters
        ----------
        a : float
            The value.
        tol : float, optional
            The absolute tolerance.
            Default is ``None``, in which case ``self.absolute`` is used.

        Returns
        -------
        bool
            ``True`` if the value is small enough to be considered zero.
            ``False`` otherwise.

        Examples
        --------
        >>> tol = Tolerance()
        >>> tol.is_positive(1e-07)
        True
        >>> tol.is_positive(1e-10)
        False

        """
        tol = tol or self.absolute
        return a > tol

    def is_negative(self, a, tol=None):
        """Check if a value can be considered a strictly negative number.

        Parameters
        ----------
        a : float
            The value.
        tol : float, optional
            The absolute tolerance.
            Default is ``None``, in which case ``self.absolute`` is used.

        Returns
        -------
        bool
            ``True`` if the value is small enough to be considered zero.
            ``False`` otherwise.

        Examples
        --------
        >>> tol = Tolerance()
        >>> tol.is_negative(-1e-07)
        True
        >>> tol.is_negative(-1e-10)
        False

        """
        tol = tol or self.absolute
        return a < -tol

    def is_close(self, a, b, rtol=None, atol=None):
        """Check if two values are close enough to be considered equal.

        Parameters
        ----------
        a : float
            The first value.
        b : float
            The second value.
        rtol : float, optional
            The relative tolerance.
            Default is ``None``, in which case ``self.relative`` is used.
        atol : float, optional
            The absolute tolerance.
            Default is ``None``, in which case ``self.absolute`` is used.

        Returns
        -------
        bool
            ``True`` if the values are close enough to be considered equal.
            ``False`` otherwise.

        Examples
        --------
        >>> tol = Tolerance()
        >>> tol.is_close(1.0, 1.000001)
        True
        >>> tol.is_close(1.0, 1.00001)
        True
        >>> tol.is_close(1.0, 1.0001)
        True
        >>> tol.is_close(1.0, 1.001)
        True
        >>> tol.is_close(1.0, 1.01)
        False

        """
        rtol = rtol or self.relative
        atol = atol or self.absolute
        return self.compare(a, b, rtol, atol)

    def is_allclose(self, A, B, rtol=None, atol=None):
        """Check if two lists of values are element-wise close enough to be considered equal.

        Parameters
        ----------
        A : list of float
            The first list of values.
        B : list of float
            The second list of values.
        rtol : float, optional
            The relative tolerance.
            Default is ``None``, in which case ``self.relative`` is used.
        atol : float, optional
            The absolute tolerance.
            Default is ``None``, in which case ``self.absolute`` is used.

        Returns
        -------
        bool
            ``True`` if the values are close enough to be considered equal.
            ``False`` otherwise.

        Examples
        --------
        >>> tol = Tolerance()
        >>> tol.is_allclose([0.0, 0.0], [1e-7, 1e-7])
        True
        >>> tol.is_allclose([0.0, 0.0], [1e-6, 1e-6])
        True
        >>> tol.is_allclose([0.0, 0.0], [1e-6, 1e-5])
        False

        """
        rtol = rtol or self.relative
        atol = atol or self.absolute
        return all(
            self.is_allclose(a, b, rtol, atol) if hasattr(a, "__iter__") else self.compare(a, b, rtol, atol)
            for a, b in zip(A, B)
        )

    def is_angle_zero(self, a, tol=None):
        """Check if an angle is close enough to zero to be considered zero.

        Parameters
        ----------
        a : float
            The angle in radians.
        tol : float, optional
            The absolute tolerance.
            Default is ``None``, in which case ``self.angular`` is used.

        Returns
        -------
        bool
            ``True`` if the angle is small enough to be considered zero.
            ``False`` otherwise.

        Examples
        --------
        >>> tol = Tolerance()
        >>> tol.is_zero_angle(1e-07)
        True
        >>> tol.is_zero_angle(1e-05)
        False

        """
        tol = tol or self.angular
        return abs(a) <= tol

    def is_angles_close(self, a, b, tol=None):
        """Check if two angles are close enough to be considered equal.

        Parameters
        ----------
        a : float
            The first angle in radians.
        b : float
            The second angle in radians.
        tol : float, optional
            The absolute tolerance.
            Default is ``None``, in which case ``self.angular`` is used.

        Returns
        -------
        bool
            ``True`` if the angles are close enough to be considered equal.
            ``False`` otherwise.

        Examples
        --------
        >>> tol = Tolerance()
        >>> tol.is_angles_close(0.0, 1e-07)
        True
        >>> tol.is_angles_close(0.0, 1e-05)
        False

        """
        tol = tol or self.angular
        return abs(a - b) <= tol


TOL = Tolerance()
