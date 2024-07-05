from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from math import factorial

from compas.geometry import Frame
from compas.geometry import Point
from compas.geometry import Vector

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


def bernstein_polynomial(n, k, t):
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

    See Also
    --------
    :func:`compas.geometry.bernstein_derivative`
    :func:`compas.geometry.binomial_coefficient`

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
    >>> bernstein_polynomial(3, 2, 0.5)
    0.375

    """
    if k < 0:
        return 0
    if k > n:
        return 0
    return binomial_coefficient(n, k) * t**k * (1 - t) ** (n - k)


def bernstein_derivative(n, k, t, p=1):
    """The p:sup:`th` derivative of the k:sup:`th` of ``n + 1`` Bernstein basis polynomials of degree ``n``.

    Parameters
    ----------
    n : int
        The degree of the polynomial.
    k : int
        The number of the basis polynomial.
    t : float
        The variable.
    p : int, optional
        The order of the derivative.

    Returns
    -------
    float
        The value of the derivative of the Bernstein basis polynomial at `t`.

    See Also
    --------
    :func:`compas.geometry.bernstein_polynomial`

    """
    c = 0
    for i in range(max(0, k + p - n), min(k, p) + 1):
        c += (-1) ** (i + p) * binomial_coefficient(p, i) * bernstein_polynomial(n - p, k - i, t)
    c = factorial(n) / factorial(n - p) * c
    return c


class Bezier(Curve):
    """A Bezier curve is defined by control points and a degree.

    A Bezier curve of degree ``n`` is a linear combination of ``n + 1`` Bernstein
    basis polynomials of degree ``n``.

    Parameters
    ----------
    points : sequence[point]
        A sequence of control points, represented by their location in 3D space.
    name : str, optional
        The name of the curve.

    Attributes
    ----------
    points : list[:class:`compas.geometry.Point`]
        The control points.
    degree : int, read-only
        The degree of the curve.
    frame : :class:`compas.geometry.Frame`, read-only
        The frame of the curve.
        This is always the world coordinate system.

    See Also
    --------
    :class:`compas.geometry.NubrsCurve`

    Examples
    --------
    Construct a Bezier curve from control points.

    >>> points = [[0.0, 0.0, 0.0], [0.5, 1.0, 0.0], [1.0, 0.0, 0.0]]
    >>> curve = Bezier(points)

    The degree of the curve is equal to the number of control points minus one.

    >>> curve.degree
    2

    Note that the input control points are automatically converted to COMPAS points.

    >>> print(curve.points)
    [Point(x=0.000, y=0.000, z=0.000), Point(x=0.500, y=1.000, z=0.000), Point(x=1.000, y=0.000, z=0.000)]

    """

    DATASCHEMA = {
        "type": "object",
        "properties": {
            "points": {"type": "array", "minItems": 2, "items": Point.DATASCHEMA},
        },
        "required": ["points"],
    }

    @property
    def __data__(self):
        return {"points": [point.__data__ for point in self.points]}

    def __init__(self, points, name=None):
        super(Bezier, self).__init__(name=name)
        self._points = []
        self.points = points

    def __repr__(self):
        return "{0}(points={1!r})".format(type(self).__name__, self.points)

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
        raise Exception("Setting the coordinate frame of a Bezier curve is not supported.")

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
        T : :class:`compas.geometry.Transformation`
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
        :class:`compas.geometry.Point`
            the corresponding point on the curve.

        See Also
        --------
        :meth:`compas.geometry.Bezier.tangent_at`, :meth:`compas.geometry.Bezier.normal_at`

        Examples
        --------
        >>> curve = Bezier([[0.0, 0.0, 0.0], [0.5, 1.0, 0.0], [1.0, 0.0, 0.0]])
        >>> print(curve.point_at(0.0))
        Point(x=0.000, y=0.000, z=0.000)
        >>> print(curve.point_at(1.0))
        Point(x=1.000, y=0.000, z=0.000)

        """
        n = self.degree
        point = Point(0, 0, 0)
        for i, p in enumerate(self.points):
            b = bernstein_polynomial(n, i, t)
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
        :class:`compas.geometry.Vector`
            The corresponding tangent vector.

        See Also
        --------
        :meth:`compas.geometry.Bezier.point_at`, :meth:`compas.geometry.Bezier.normal_at`

        Examples
        --------
        >>> curve = Bezier([[0.0, 0.0, 0.0], [0.5, 1.0, 0.0], [1.0, 0.0, 0.0]])
        >>> print(curve.tangent_at(0.5))
        Vector(x=1.000, y=0.000, z=0.000)

        """
        n = self.degree
        vector = Vector(0, 0, 0)
        for i, point in enumerate(self.points):
            vector += point * bernstein_derivative(n, i, t, 1)
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
        :class:`compas.geometry.Vector`
            The corresponding normal vector.

        See Also
        --------
        :meth:`compas.geometry.Bezier.point_at`, :meth:`compas.geometry.Bezier.tangent_at`

        Examples
        --------
        >>> curve = Bezier([[0.0, 0.0, 0.0], [0.5, 1.0, 0.0], [1.0, 0.0, 0.0]])
        >>> print(curve.normal_at(0.5))
        Vector(x=0.000, y=-1.000, z=0.000)

        """
        tangent = self.tangent_at(t)
        n = self.degree
        vector = Vector(0, 0, 0)
        for i, point in enumerate(self.points):
            vector += point * bernstein_derivative(n, i, t, 2)
        if vector.length < 1e-6:
            return None
        vector.unitize()
        normal = tangent.cross(vector.cross(tangent))
        return normal
