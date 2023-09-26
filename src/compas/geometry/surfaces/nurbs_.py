from itertools import groupby

from compas.plugins import plugin
from compas.utilities import flatten

from compas.geometry import Point
from compas.geometry import NurbsSurface
from compas.geometry import construct_knotvector
from compas.geometry import find_span
from compas.geometry import compute_basisfuncs

# from compas.geometry import compute_basisfuncsderivs


@plugin(category="factories", requires=None, tryfirst=True)
def new_nurbssurface(cls, *args, **kwargs):
    curve = object.__new__(DefaultNurbsSurface)
    curve.__init__(*args, **kwargs)
    return curve


@plugin(category="factories", requires=None, tryfirst=True)
def new_nurbssurface_from_parameters(cls, *args, **kwargs):
    return DefaultNurbsSurface.from_parameters(*args, **kwargs)


@plugin(category="factories", requires=None, tryfirst=True)
def new_nurbssurface_from_points(cls, *args, **kwargs):
    return DefaultNurbsSurface.from_points(*args, **kwargs)


class DefaultNurbsSurface(NurbsSurface):
    def __init__(self, name=None):
        super(DefaultNurbsSurface, self).__init__(name=name)
        self._points = []
        self._weights = []
        self._knotvector_u = []
        self._knotvector_v = []
        self._degree_u = 1
        self._degree_v = 1
        self._cache_u = {}
        self._cache_v = {}

    # ==============================================================================
    # Data
    # ==============================================================================

    # ==============================================================================
    # Properties
    # ==============================================================================

    @property
    def points(self):
        """list of list of :class:`compas.geometry.Point`:

        The structure of this list is as follows:

        - assuming a surface with its U and V directions parallel to the X and Y axes, respectively; and
        - assuming the U domain is [0.0, 1.0] and the V domain is [0.0, 1.0];
        - then the list of points at position points[0] defines the control points of an isocurve on the surface with fixed parameter value u = 0.0 and v going from 0.0 to 1.0.

        """
        return self._points

    @points.setter
    def points(self, points):
        temp = []
        for column in points:
            temp.append([])
            for point in column:
                if isinstance(point, Point):
                    temp[-1].append(point)
                else:
                    temp[-1].append(Point(*point))
        self._points = temp

    @property
    def weights(self):
        if not self._weights:
            self._weights = [[1.0 for point in column] for column in self.points]
        return self._weights

    @weights.setter
    def weights(self, weights):
        self._weights = weights

    @property
    def degree_u(self):
        return self._degree_u

    @degree_u.setter
    def degree_u(self, degree):
        if degree < 1:
            raise ValueError("The degree of a curve should be at least 1.")
        self._cache_u = {}
        self._degree_u = degree

    @property
    def degree_v(self):
        return self._degree_v

    @degree_v.setter
    def degree_v(self, degree):
        if degree < 1:
            raise ValueError("The degree of a curve should be at least 1.")
        self._cache_v = {}
        self._degree_v = degree

    @property
    def knotvector_u(self):
        if not self._knotvector_u:
            self.knotvector_u = construct_knotvector(self.degree_u, len(self.points))
        return self._knotvector_u

    @knotvector_u.setter
    def knotvector_u(self, knotvector):
        self._cache_u = {}
        self._knotvector_u = knotvector

    @property
    def knotvector_v(self):
        if not self._knotvector_v:
            self.knotvector_v = construct_knotvector(self.degree_v, len(self.points[0]))
        return self._knotvector_v

    @knotvector_v.setter
    def knotvector_v(self, knotvector):
        self._cache_v = {}
        self._knotvector_v = knotvector

    @property
    def knots_u(self):
        return [knot for knot, _ in groupby(self.knotvector_u)]

    @property
    def mults_u(self):
        return [len(list(multiplicity)) for _, multiplicity in groupby(self.knotvector_u)]

    @property
    def knots_v(self):
        return [knot for knot, _ in groupby(self.knotvector_v)]

    @property
    def mults_v(self):
        return [len(list(multiplicity)) for _, multiplicity in groupby(self.knotvector_v)]

    @property
    def order_u(self):
        return self.degree_u + 1

    @property
    def order_v(self):
        return self.degree_v + 1

    @property
    def domain_u(self):
        return self.knotvector_u[self.degree_u], self.knotvector_u[-(self.degree_u + 1)]

    @property
    def domain_v(self):
        return self.knotvector_v[self.degree_v], self.knotvector_v[-(self.degree_v + 1)]

    @property
    def is_rational(self):
        return any(weight != 1.0 for weight in flatten(self.weights))

    @property
    def is_periodic_u(self):
        return False

    @property
    def is_periodic_v(self):
        return False

    # ==============================================================================
    # Constructors
    # ==============================================================================

    @classmethod
    def from_parameters(cls, points, weights, degree_u, degree_v, knotvector_u, knotvector_v):
        """Construct a NURBS surface from explicit surface parameters.

        Parameters
        ----------
        points : list[list[:class:`compas.geometry.Point`]]
            The control points of the surface.
        weights : list[list[float]]
            The weights of the control points.
        degree_u : int
            The degree of the surface in the u direction.
        degree_v : int
            The degree of the surface in the v direction.
        knotvector_u : list[int | float]
            The knot vector of the surface in the u direction.
        knotvector_v : list[int | float]
            The knot vector of the surface in the v direction.

        Returns
        -------
        :class:`compas.geometry.DefaultNurbsSurface`

        """
        surface = cls()
        surface.points = points
        surface.weights = weights
        surface.degree_u = degree_u
        surface.degree_v = degree_v
        surface.knotvector_u = knotvector_u
        surface.knotvector_v = knotvector_v
        return surface

    @classmethod
    def from_points(cls, points, degree_u=3, degree_v=3, weights=None):
        """Construct a NURBS surface from a grid of points.

        Parameters
        ----------
        points : list[list[:class:`compas.geometry.Point`]]
            The control points of the surface.
        degree_u : int, optional
            The degree of the surface in the u direction.
        degree_v : int, optional
            The degree of the surface in the v direction.
        weights : list[list[float]], optional
            The weights of the control points.
            Default is ``None``, in which case all weights are set to 1.0.

        Returns
        -------
        :class:`compas.geometry.DefaultNurbsSurface`

        """
        surface = cls()
        surface.points = points
        surface.degree_u = degree_u
        surface.degree_v = degree_v
        surface.weights = weights
        return surface

    # ==============================================================================
    # Methods
    # ==============================================================================

    def point_at(self, u, v):
        """Compute a point on the surface for a given parameter value.

        Parameters
        ----------
        u : float
            Parameter value in the u direction.
        v : float
            Parameter value in the v direction.

        Returns
        -------
        :class:`compas.geometry.Point`
            Point on the surface.

        """
        n = len(self.points) - 1
        m = len(self.points[0]) - 1

        span_u = find_span(n, self.degree_u, self.knotvector_u, u)
        span_v = find_span(m, self.degree_v, self.knotvector_v, v)

        bases_u = compute_basisfuncs(self.degree_u, self.knotvector_u, span_u, u)
        bases_v = compute_basisfuncs(self.degree_v, self.knotvector_v, span_v, v)

        Sx = 0.0
        Sy = 0.0
        Sz = 0.0

        for j in range(self.degree_v + 1):
            X = 0.0
            Y = 0.0
            Z = 0.0

            for i in range(self.degree_u + 1):
                x, y, z = self.points[span_u - self.degree_u + i][span_v - self.degree_v + j]

                X += x * bases_u[i]
                Y += y * bases_u[i]
                Z += z * bases_u[i]

            Sx += X * bases_v[j]
            Sy += Y * bases_v[j]
            Sz += Z * bases_v[j]

        return Point(Sx, Sy, Sz)

    def normal_at(self, u, v):
        """Compute the normal vector at a point on the surface for a given parameter value.

        Parameters
        ----------
        u : float
            Parameter value in the u direction.
        v : float
            Parameter value in the v direction.

        Returns
        -------
        :class:`compas.geometry.Vector`
            Normal vector at the point.

        """
        # n = len(self.points) - 1
        # m = len(self.points[0]) - 1

        # span_u = find_span(n, self.degree_u, self.knotvector_u, u)
        # span_v = find_span(m, self.degree_v, self.knotvector_v, v)

        # _, _, ders_u = compute_basisfuncsderivs(self.degree_u, self.knotvector_u, span_u, u, 1)
        # _, _, ders_v = compute_basisfuncsderivs(self.degree_v, self.knotvector_v, span_v, v, 1)

        # du = min(self.degree_u, 1)
        # dv = min(self.degree_v, 1)

        # Su = Vector(0.0, 0.0, 0.0)
        # Sv = Vector(0.0, 0.0, 0.0)

        # for i in range(du + 1):
        #     Su += self.points[span_u - self.degree_u + i][span_v] * ders_u[i][0]

        # for j in range(dv + 1):
        #     Sv += self.points[span_u][span_v - self.degree_v + j] * ders_v[j][0]

        # return Su.cross(Sv).unitized()

    def isocurve_u(self, v):
        """Construct an isocurve in the u direction at a fixed parameter value in the v direction.

        Parameters
        ----------
        v : float
            Parameter value in the v direction.

        Returns
        -------
        :class:`compas.geometry.NurbsCurve`

        """
        # see p 110 to get started.
