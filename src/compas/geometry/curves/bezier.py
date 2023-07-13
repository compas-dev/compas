from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from math import factorial

from compas.geometry import Vector
from compas.geometry import Point
from compas.geometry import Frame

from .curve import Curve


def binomial_coefficient(n, k):
    """Returns the binomial coefficient of the :math:`x^k` term in the
    polynomial expansion of the binomial power :math:`(1 + x)^n`.

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

    Notes
    -----
    Arranging binomial coefficients into rows for successive values of `n`,
    and in which `k` ranges from 0 to `n`, gives a triangular array known as
    Pascal's triangle.

    """
    return int(factorial(n) / float(factorial(k) * factorial(n - k)))


def bernstein_value(n, k, t):
    """The k:sup:`th` of ``n + 1`` Bernstein basis polynomials of degree ``n``.

    A weighted linear combination of these basis polynomials is called a Bernstein polynomial.

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

    Notes
    -----
    When constructing Bezier curves, the weights are simply the coordinates
    of the control points of the curve.

    References
    ----------
    More info at [1]_.

    .. [1] https://en.wikipedia.org/wiki/Bernstein_polynomial

    Examples
    --------
    >>> bernstein(3, 2, 0.5)
    0.375

    """
    if k < 0:
        return 0
    if k > n:
        return 0
    return binomial_coefficient(n, k) * t**k * (1 - t) ** (n - k)


class Bezier(Curve):
    """A Bezier curve is defined by control points and a degree.

    A Bezier curve of degree ``n`` is a linear combination of ``n + 1`` Bernstein
    basis polynomials of degree ``n``.

    Parameters
    ----------
    points : sequence[point]
        A sequence of control points, represented by their location in 3D space.

    Attributes
    ----------
    points : list[:class:`~compas.geometry.Point`]
        The control points.
    degree : int, read-only
        The degree of the curve.

    Examples
    --------
    >>> curve = Bezier([[0.0, 0.0, 0.0], [0.5, 1.0, 0.0], [1.0, 0.0, 0.0]])
    >>> curve.degree
    2

    """

    JSONSCHEMA = {
        "type": "object",
        "properties": {
            "points": {"type": "array", "minItems": 2, "items": Point.JSONSCHEMA},
        },
        "required": ["points"],
    }

    # overwriting the __new__ method is necessary
    # to avoid triggering the plugin mechanism of the base curve class
    def __new__(cls, *args, **kwargs):
        curve = object.__new__(cls)
        curve.__init__(*args, **kwargs)
        return curve

    def __init__(self, points, **kwargs):
        super(Bezier, self).__init__(**kwargs)
        self._points = []
        self.points = points

    # ==========================================================================
    # Data
    # ==========================================================================

    @property
    def data(self):
        return {"points": self.points}

    @data.setter
    def data(self, data):
        self.points = data["points"]

    @classmethod
    def from_data(cls, data):
        """Construct a curve from its data representation.

        Parameters
        ----------
        data : dict
            The data dictionary.

        Returns
        -------
        :class:`~compas.geometry.Bezier`
            The constructed bezier curve.

        Examples
        --------
        >>> from compas.geometry import Bezier
        >>> data = {'points': [[0.0, 0.0, 0.0], [0.5, 1.0, 0.0], [1.0, 0.0, 0.0]]}
        >>> curve = Bezier.from_data(data)

        """
        return cls(data["points"])

    # ==========================================================================
    # Properties
    # ==========================================================================

    @property
    def frame(self):
        if not self._frame:
            self._frame = Frame.worldXY()
        return self._frame

    @frame.setter
    def frame(self, frame):
        raise NotImplementedError

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, points):
        if points:
            self._points = [Point(*point) for point in points]

    @property
    def degree(self):
        return len(self.points) - 1

    # ==========================================================================
    # Constructors
    # ==========================================================================

    # ==========================================================================
    # Transformations
    # ==========================================================================

    def transform(self, T):
        """Transform this curve.

        Parameters
        ----------
        T : :class:`~compas.geometry.Transformation`
            The transformation.

        Returns
        -------
        None

        """
        for point in self.points:
            point.transform(T)

    # ==========================================================================
    # Methods
    # ==========================================================================

    def point_at(self, t):
        """Compute the point on the curve at the given parameter.

        Parameters
        ----------
        t : float
            The value of the curve parameter.
            Must be between 0 and 1.

        Returns
        -------
        :class:`~compas.geometry.Point`
            the corresponding point on the curve.

        See Also
        --------
        :meth:`compas.geometry.Bezier.tangent_at`

        Examples
        --------
        >>> curve = Bezier([[0.0, 0.0, 0.0], [0.5, 1.0, 0.0], [1.0, 0.0, 0.0]])
        >>> curve.point_at(0.0)
        Point(0.000, 0.000, 0.000)
        >>> curve.point_at(1.0)
        Point(1.000, 0.000, 0.000)

        """
        n = self.degree
        point = Point(0, 0, 0)
        for i, p in enumerate(self.points):
            b = bernstein_value(n, i, t)
            point += p * b
        return point

    def tangent_at(self, t):
        """Compute the tangent vector to the curve at the point at the given parameter.

        Parameters
        ----------
        t : float
            The value of the curve parameter. Must be between 0 and 1.

        Returns
        -------
        :class:`~compas.geometry.Vector`
            The corresponding tangent vector.

        Examples
        --------
        >>> curve = Bezier([[0.0, 0.0, 0.0], [0.5, 1.0, 0.0], [1.0, 0.0, 0.0]])
        >>> curve.tangent_at(0.5)
        Vector(1.000, 0.000, 0.000)

        """
        p = 1
        n = self.degree
        vector = Vector(0, 0, 0)
        for i, point in enumerate(self.points):
            # a = bernstein_value(n - 1, i - 1, t)
            # b = bernstein_value(n - 1, i, t)
            # c = n * (a - b)
            c = 0
            for k in range(max(0, i + p - n), min(i, p) + 1):
                c += (-1) ** (k + p) * binomial_coefficient(p, k) * bernstein_value(n - p, i - k, t)
            c = factorial(n) / factorial(n - p) * c
            vector += point * c
        vector.unitize()
        return vector

    def normal_at(self, t):
        """Compute the normal vector to the curve at the point at the given parameter.

        Parameters
        ----------
        t : float
            The value of the curve parameter. Must be between 0 and 1.

        Returns
        -------
        :class:`~compas.geometry.Vector`
            The corresponding normal vector.

        Examples
        --------
        >>> curve = Bezier([[0.0, 0.0, 0.0], [0.5, 1.0, 0.0], [1.0, 0.0, 0.0]])
        >>> curve.normal_at(0.5)
        Vector(0.000, 0.000, 1.000)

        """
        tangent = self.tangent_at(t)
        p = 2
        n = self.degree
        vector = Vector(0, 0, 0)
        f = factorial(n) / factorial(n - p)
        for i, point in enumerate(self.points):
            c = 0
            for k in range(max(0, i + p - n), min(i, p) + 1):
                c += (-1) ** (k + p) * binomial_coefficient(p, k) * bernstein_value(n - p, i - k, t)
            vector += point * (f * c)
        if vector.length < 1e-6:
            return None
        vector.unitize()
        normal = tangent.cross(vector.cross(tangent))
        return normal
