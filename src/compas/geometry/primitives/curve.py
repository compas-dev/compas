from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from math import factorial

from compas.geometry.primitives import Primitive
from compas.geometry.primitives import Point
from compas.geometry.primitives import Vector


__all__ = ['Bezier']


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


class Bezier(Primitive):
    """A Bezier curve.

    A Bezier curve of degree ``n`` is a linear combination of ``n + 1`` Bernstein
    basis polynomials of degree ``n``.

    Parameters
    ----------
    points : sequence
        A sequence of control points, represented by their location in 3D space.

    Attributes
    ----------
    data : dict
        The dictionary representation of the curve.
    points : list of :class:`compas.geometry.Point`
        The control points of the curve.
    degree : int, read-only
        The curve degree.

    Examples
    --------
    >>> curve = Bezier([[0.0, 0.0, 0.0], [0.5, 1.0, 0.0], [1.0, 0.0, 0.0]])
    >>> curve.degree
    2
    """

    __slots__ = ["_points"]

    def __init__(self, points):
        super(Bezier, self).__init__()
        self._points = []
        self.points = points

    @property
    def data(self):
        """dict: The data dictionary that represents the curve."""
        return {'points': [list(point) for point in self.points]}

    @data.setter
    def data(self, data):
        self.points = data['points']

    @property
    def points(self):
        """list of :class:`compas.geometry.Point`: The control points."""
        return self._points

    @points.setter
    def points(self, points):
        if points:
            self._points = [Point(*point) for point in points]

    @property
    def degree(self):
        """int (read-only): The degree of the curve."""
        return len(self.points) - 1

    # ==========================================================================
    # constructors
    # ==========================================================================

    @classmethod
    def from_data(cls, data):
        """Construct a curve from its data representation.

        Parameters
        ----------
        data : dict
            The data dictionary.

        Returns
        -------
        :class:`compas.geometry.Curve`
            The constructed curve.

        Examples
        --------
        >>> from compas.geometry import Curve
        >>> data = {'points': [[0.0, 0.0, 0.0], [0.5, 1.0, 0.0], [1.0, 0.0, 0.0]]}
        >>> curve = Curve.from_data(data)
        """
        return cls(data['points'])

    # ==========================================================================
    # methods
    # ==========================================================================

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

        Examples
        --------
        >>> curve = Bezier([[0.0, 0.0, 0.0], [0.5, 1.0, 0.0], [1.0, 0.0, 0.0]])
        >>> curve.point(0.0)
        Point(0.000, 0.000, 0.000)
        >>> curve.point(1.0)
        Point(1.000, 0.000, 0.000)
        """
        n = self.degree
        point = Point(0, 0, 0)
        for i, p in enumerate(self.points):
            b = bernstein(n, i, t)
            point += p * b
        return point

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

        Examples
        --------
        >>> curve = Bezier([[0.0, 0.0, 0.0], [0.5, 1.0, 0.0], [1.0, 0.0, 0.0]])
        >>> curve.tangent(0.5)
        Vector(1.000, 0.000, 0.000)
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

        Examples
        --------
        >>> curve = Bezier([[0.0, 0.0, 0.0], [0.5, 1.0, 0.0], [1.0, 0.0, 0.0]])
        >>> points = curve.locus(10)
        >>> len(points) == 10
        True
        >>> points[0]
        Point(0.000, 0.000, 0.000)
        >>> points[-1]
        Point(1.000, 0.000, 0.000)
        """
        locus = []
        divisor = float(resolution - 1)
        for i in range(resolution):
            t = i / divisor
            locus.append(self.point(t))
        return locus


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    import doctest
    doctest.testmod(globs=globals())
