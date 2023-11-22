from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


from compas.data import Data


class Tolerance(Data):
    """Tolerance settings for geometric operations."""

    ABSOLUTE_TOLERANCE = 1e-6
    """float: Determines when a number is small enough to be considered zero.
    """

    RELATIVE_TOLERANCE = 1e-3
    """float: Determines the accuracy of comparing a "computed value" to a "true value", as a fraction of the "true value".
    """

    ANGLE_TOLERANCE = 1e-3
    """float: An absolute value that determines when the difference between two angles is small enough to be considered zero.
    """

    def __init__(self, unit="M"):
        self._unit = None
        self._absolute = None
        self._relative = None
        self._angle = None
        self.unit = unit

    @property
    def data(self):
        pass

    @classmethod
    def from_data(cls, data):
        pass

    def reset(self):
        """Reset all precision settings to their default values."""
        self._absolute = None
        self._relative = None
        self._angle = None

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
        """float: The absolute tolerance."""
        if not self._absolute:
            return self.ABSOLUTE_TOLERANCE
        return self._absolute

    @absolute.setter
    def absolute(self, value):
        self._absolute = value

    @property
    def relative(self):
        """float: The relative tolerance."""
        if not self._relative:
            return self.RELATIVE_TOLERANCE
        return self._relative

    @relative.setter
    def relative(self, value):
        self._relative = value

    @property
    def angle(self):
        """float: The angle tolerance."""
        if not self._angle:
            return self.ANGLE_TOLERANCE
        return self._angle

    @angle.setter
    def angle(self, value):
        self._angle = value

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

        """
        return rtol * truevalue + atol

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

        """
        return abs(a - b) <= self.tolerance(b, rtol, atol)

    def zero(self, a, tol=None):
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

        """
        tol = tol or self.absolute
        return abs(a) <= tol

    def close(self, a, b, rtol=None, atol=None):
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

        """
        rtol = rtol or self.relative
        atol = atol or self.absolute
        return self.compare(a, b, rtol, atol)

    def allclose(self, A, B, rtol=None, atol=None):
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

        """
        rtol = rtol or self.relative
        atol = atol or self.absolute
        return all(self.compare(a, b, rtol, atol) for a, b in zip(A, B))


tol = Tolerance()
