from itertools import groupby

from compas.plugins import plugin

from compas.geometry import Point
from compas.geometry import Vector
from compas.geometry import NurbsCurve

from compas.geometry import construct_knotvector
from compas.geometry import find_span
from compas.geometry import compute_basisfuncs
from compas.geometry import compute_basisfuncsderivs
from compas.geometry import knots_and_mults_to_knotvector


@plugin(category="factories", requires=None, tryfirst=True)
def new_nurbscurve(cls, *args, **kwargs):
    curve = object.__new__(DefaultNurbsCurve)
    curve.__init__(*args, **kwargs)
    return curve


@plugin(category="factories", requires=None, tryfirst=True)
def new_nurbscurve_from_parameters(cls, *args, **kwargs):
    return DefaultNurbsCurve.from_parameters(*args, **kwargs)


@plugin(category="factories", requires=None, tryfirst=True)
def new_nurbscurve_from_points(cls, *args, **kwargs):
    return DefaultNurbsCurve.from_points(*args, **kwargs)


class DefaultNurbsCurve(NurbsCurve):
    def __init__(self, name=None):
        super(DefaultNurbsCurve, self).__init__(name=name)
        self._points = []
        self._weights = []
        self._knotvector = []
        self._degree = 1
        self._cache = {}

    # ==============================================================================
    # Data
    # ==============================================================================

    # ==============================================================================
    # Properties
    # ==============================================================================

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, points):
        self._points = [(point if isinstance(point, Point) else Point(*point)) for point in points]

    @property
    def weights(self):
        if not self._weights:
            self._weights = [1.0] * len(self.points)
        return self._weights

    @weights.setter
    def weights(self, weights):
        if len(weights) != len(self.points):
            raise ValueError("The number of weights should be equal to the number of points.")
        self._weights = weights

    @property
    def knotvector(self):
        if not self._knotvector:
            self._cache = {}
            self._knotvector = construct_knotvector(self.degree, len(self.points))
        return self._knotvector

    @knotvector.setter
    def knotvector(self, knotvector):
        self._cache = {}
        self._knotvector = knotvector

    @property
    def knots(self):
        return [knot for knot, _ in groupby(self.knotvector)]

    @property
    def multiplicities(self):
        return [len(list(multiplicity)) for _, multiplicity in groupby(self.knotvector)]

    @property
    def degree(self):
        return self._degree

    @degree.setter
    def degree(self, degree):
        if degree < 1:
            raise ValueError("The degree of a curve should be at least 1.")
        self._cache = {}
        self._degree = degree

    @property
    def order(self):
        return self.degree + 1

    @property
    def is_rational(self):
        return any(weight != 1.0 for weight in self.weights)

    @property
    def is_periodic(self):
        return False

    @property
    def domain(self):
        return self.knotvector[self.degree], self.knotvector[-(self.degree + 1)]

    # ==============================================================================
    # Helpers
    # ==============================================================================

    # ==============================================================================
    # Constructors
    # ==============================================================================

    @classmethod
    def from_parameters(cls, points, weights, knots, multiplicities, degree, is_periodic=False):
        """Construct a NURBS curve from explicit curve parameters.

        Parameters
        ----------
        points : list[:class:`~compas.geometry.Point`]
            The control points.
        weights : list[float]
            The control point weights.
        knots : list[float]
            The curve knots, without multiplicity.
        multiplicities : list[int]
            Multiplicity of the knots.
        degree : int
            The degree of the curve.
        is_periodic : bool, optional
            Flag indicating whether the curve is periodic or not.
            Note that this parameters is currently not supported.

        Returns
        -------
        :class:`compas.geometry.DefaultNurbsCurve`

        """
        curve = cls()
        curve.points = points
        curve.weights = weights
        curve.knotvector = knots_and_mults_to_knotvector(knots, multiplicities)
        curve.degree = degree
        return curve

    @classmethod
    def from_points(cls, points, degree=3):
        """Construct a NURBS curve from a list of points.

        Parameters
        ----------
        points : list[:class:`~compas.geometry.Point`]
            The control points.
        degree : int, optional
            The degree of the curve.

        Returns
        -------
        :class:`compas.geometry.DefaultNurbsCurve`

        """
        curve = cls()
        curve.points = points
        curve.degree = degree
        return curve

    # ==============================================================================
    # Methods
    # ==============================================================================

    def compute_basis(self, t):
        """Compute the basis values for a given parameter value.

        Parameters
        ----------
        t : float
            Parameter value.

        Returns
        -------
        list[float]
            Basis values.

        """
        if t not in self._cache:
            p = self.degree
            n = len(self.points) - 1
            i = find_span(n, p, self.knotvector, t)
            N = compute_basisfuncs(p, self.knotvector, i, t)
            self._cache[t] = i, N
        return self._cache[t]

    def point_at(self, t):
        """Compute a point on the curve for a given parameter value.

        Parameters
        ----------
        t : float
            Parameter value.

        Returns
        -------
        :class:`compas.geometry.Point`
            Point on the curve.

        """
        p = self.degree
        i, N = self.compute_basis(t)

        points = self.points
        weights = self.weights

        X = 0.0
        Y = 0.0
        Z = 0.0
        W = 0.0

        for j in range(p + 1):
            x, y, z = points[i - p + j]
            b = N[j] * weights[i - p + j]
            X += x * b
            Y += y * b
            Z += z * b
            W += b

        return Point(X / W, Y / W, Z / W)

    def tangent_at(self, t, unitized=True):
        """Compute the tangent of the curve for a given parameter value.

        Parameters
        ----------
        t : float
            Parameter value.

        Returns
        -------
        :class:`compas.geometry.Vector`
            Tangent vector.

        """
        d = 1
        n = len(self.points) - 1
        p = self.degree
        du = min(d, p)
        i = find_span(n, p, self.knotvector, t)
        derivs = compute_basisfuncsderivs(
            p, self.knotvector, i, t, d
        )  # this should be cached and combined with basisfuncs
        CK = [[0.0, 0.0, 0.0] for _ in range(d + 1)]

        for k in range(du + 1):  # type: ignore
            for j in range(p + 1):
                x, y, z = self.points[i - p + j]
                deriv = derivs[k][j]
                CK[k][0] += deriv * x
                CK[k][1] += deriv * y
                CK[k][2] += deriv * z

        tangent = Vector(*CK[1])
        if unitized:
            tangent.unitize()

        return tangent
