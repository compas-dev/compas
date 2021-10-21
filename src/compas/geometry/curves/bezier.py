from compas.geometry import Point
from compas.geometry import Vector
from .curve import Curve

from math import factorial


def binomial_coefficient(n, k):
    """Returns the binomial coefficient of the :math:`x^k` term in the
    polynomial expansion of the binomial power :math:`(1 + x)^n`.

    Notes
    -----
    Arranging binomial coefficients into rows for successive values of `n`,
    and in which `k` ranges from 0 to `n`, gives a triangular array known as
    Pascal's triangle.

    Parameters
    ----------
    n : int
        The number of terms.
    k : int
        The index of the coefficient.

    Returns
    -------
    int
        The coefficient.
    """
    return int(factorial(n) / float(factorial(k) * factorial(n - k)))


def bernstein(n, k, t):
    """k:sup:`th` of `n` + 1 Bernstein basis polynomials of degree `n`. A
    weighted linear combination of these basis polynomials is called a Bernstein
    polynomial [wikipedia2017k]_.

    Notes
    -----
    When constructing Bezier curves, the weights are simply the coordinates
    of the control points of the curve.

    Parameters
    ----------
    n : int
        The degree of the polynomial.
    k : int
        The number of the basis polynomial.
    t : float
        The variable.

    Returns
    -------
    float
        The value of the Bernstein basis polynomial at `t`.

    Examples
    --------
    >>> bernstein(3, 2, 0.5)
    0.375
    """
    if k < 0:
        return 0
    if k > n:
        return 0
    return binomial_coefficient(n, k) * t ** k * (1 - t) ** (n - k)


class BezierCurve(Curve):
    """Class representing a Bezier curve."""

    # __slots__ = ('points', )

    @property
    def DATASCHEMA(self):
        from schema import Schema
        from compas.data import is_float3
        return Schema({
            'points': lambda points: all(is_float3(point) for point in points)
        })

    @property
    def JSONSCHEMANAME(self):
        return 'bezier'

    def __init__(self, points, **kwargs):
        super(BezierCurve, self).__init__(**kwargs)
        self._points = None
        self.points = points

    @property
    def data(self):
        return {'points': [point.data for point in self.points]}

    @data.setter
    def data(self, data):
        self.points = [Point.from_data(point) for point in data['points']]

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, points):
        self._points = [Point(x, y, z) for x, y, z in points]

    @property
    def degree(self):
        return len(self.points) - 1

    @classmethod
    def from_data(cls, data):
        """Construct a Bezier curve from its data representation.

        Parameters
        ----------
        data : dict
            The data dictionary.

        Returns
        -------
        :class:`compas.geometry.BezierCurve`
            The constructed bezier curve.

        """
        return cls([Point.from_data(point) for point in data['points']])

    def point(self, t):
        """Compute a point on the curve.

        Parameters
        ----------
        t : float
            The value of the curve parameter. Must be between 0 and 1.

        Returns
        -------
        Point
            the corresponding point on the curve.
        """
        n = self.degree
        point = Point(0, 0, 0)
        for i, p in enumerate(self.points):
            b = bernstein(n, i, t)
            point += p * b
        return point

    def locus(self, resolution=100):
        """Compute the locus of all points on the curve.

        Parameters
        ----------
        resolution : int
            The number of intervals at which a point on the
            curve should be computed. Defaults to 100.

        Returns
        -------
        list
            Points along the curve.

        """
        locus = []
        divisor = float(resolution - 1)
        for i in range(resolution):
            t = i / divisor
            locus.append(self.point(t))
        return locus

    def tangent(self, t):
        """Compute the tangent vector at a point on the curve.

        Parameters
        ----------
        t : float
            The value of the curve parameter. Must be between 0 and 1.

        Returns
        -------
        Vector
            The corresponding tangent vector.

        """
        n = self.degree
        v = Vector(0, 0, 0)
        for i, p in enumerate(self.points):
            a = bernstein(n - 1, i - 1, t)
            b = bernstein(n - 1, i, t)
            c = n * (a - b)
            v += p * c
        v.unitize()
        return v
