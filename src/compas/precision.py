from compas.data import Data


DEFAULT_ANGULAR = 1e-12
DEFAULT_CONFUSION = {
    "M": 1e-7,
    "MM": 1e-4,
}


class Precision(Data):
    """Precision settings for geometric operations.

    Attributes
    ----------
    angular : float
        The angular precision.
        The default is 1e-12.
    approximation : float
        The approximation precision.
        The default is ``precision.confusion * 10``.
    confusion : float
        The confusion precision.
        The default is 1e-7 for unit "M", and 1e-4 for unit "MM".
    intersection : float
        The intersection precision.
        The default is ``precision.confusion / 100``.
    squareconfusion : float
        The square confusion precision.
    unit : {'M', 'MM'}
        The unit of the precision settings.

    Notes
    -----
    The functionality of this package is entirely based on the Precision Package of the CAD kernel OpenCascade:
    https://dev.opencascade.org/doc/occt-7.4.0/refman/html/class_precision.html

    Examples
    --------
    >>> from compas.precision import Precision
    >>> precision = Precision()
    >>> precision.angular
    1e-12
    >>> precision.approximation
    1e-07
    >>> precision.confusion
    1e-07
    >>> precision.intersection
    1e-09
    >>> precision.squareconfusion
    1e-14

    >>> precision = Precision(unit="MM")
    >>> precision.angular
    1e-12
    >>> precision.approximation
    0.0001
    >>> precision.confusion
    0.0001
    >>> precision.intersection
    1e-06
    >>> precision.squareconfusion
    1e-08

    >>> from compas.geometry import Point
    >>> a = Point(0, 0, 0)
    >>> b = Point(1e-8, 0, 0)
    >>> if distance_point_point(a, b) < precision.confusion:
    ...     print("The points are too close to distinguish.")

    >>> def is_equal(a, b):
    ...     return (
    ...         fabs(a.x - b.x) <= precision.confusion
    ...         and fabs(a.y - b.y) <= precision.confusion
    ...         and fabs(a.z - b.z) <= precision.confusion
    ...     )
    >>> a = Point(0, 0, 0)
    >>> b = Point(1e-8, 0, 0)
    >>> is_equal(a, b)
    True

    >>> def is_equal2(a, b):
    ...     return (
    ...         (a.x - b.x) ** 2 <= precision.squareconfusion
    ...         and (a.y - b.y) ** 2 <= precision.squareconfusion
    ...         and (a.z - b.z) ** 2 <= precision.squareconfusion
    ...     )
    >>> a = Point(0, 0, 0)
    >>> b = Point(1e-8, 0, 0)
    >>> is_equal2(a, b)
    True


    """

    def __init__(self, unit="M"):
        self._unit = None
        self._angular = None
        self._approximation = None
        self._confusion = None
        self._intersection = None
        self.unit = unit

    @property
    def data(self):
        return {
            "unit": self.unit,
            "angular": self.angular,
            "approximation": self.approximation,
            "confusion": self.confusion,
            "intersection": self.intersection,
        }

    def reset(self):
        """Reset all precision settings to their default values."""
        self._angular = None
        self._approximation = None
        self._confusion = None
        self._intersection = None

    @property
    def units(self):
        return self._unit

    @units.setter
    def units(self, value):
        if value not in ["M", "MM"]:
            raise ValueError("Invalid unit: {}".format(value))
        self._unit = value

    @property
    def angular(self):
        if self._angular is None:
            return DEFAULT_ANGULAR
        return self._angular

    @angular.setter
    def angular(self, value):
        self._angular = value

    @property
    def approximation(self):
        if self._approximation is None:
            return self.confusion * 10
        return self._approximation

    @approximation.setter
    def approximation(self, value):
        self._approximation = value

    @property
    def confusion(self):
        if self._confusion is None:
            return DEFAULT_CONFUSION[self.unit]
        return self._confusion

    @confusion.setter
    def confusion(self, value):
        self._confusion = value

    @property
    def intersection(self):
        if self._intersection is None:
            return self.confusion / 100
        return self._intersection

    @intersection.setter
    def intersection(self, value):
        self._intersection = value

    @property
    def squareconfusion(self):
        return self.confusion * self.confusion
