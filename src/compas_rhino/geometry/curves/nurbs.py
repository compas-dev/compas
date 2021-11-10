from itertools import groupby
from compas.geometry import Point
# from compas.geometry import Vector
# from compas.geometry import Transformation
# from compas.geometry import Frame
# from compas.geometry import Circle
# from compas.geometry import Box
from compas.utilities import linspace

try:
    from compas.geometry import NurbsCurve
except ImportError:
    from compas.geometry import Geometry as NurbsCurve

from compas_rhino.conversions import point_to_rhino
from compas_rhino.conversions import point_to_compas
# from compas_rhino.conversions import vector_to_rhino
# from compas_rhino.conversions import vector_to_compas
from compas_rhino.conversions import circle_to_rhino
from compas_rhino.conversions import ellipse_to_rhino
from compas_rhino.conversions import line_to_rhino

import Rhino.Geometry


def rhino_curve_from_parameters(points, weights, knots, multiplicities, degree):
    rhino_curve = Rhino.Geometry.NurbsCurve(3, True, degree + 1, len(points))
    for index, (point, weight) in enumerate(zip(points, weights)):
        rhino_curve.Points.SetPoint(index, point_to_rhino(point), weight)
    knotvector = [knot for knot, mult in zip(knots, multiplicities) for _ in range(mult)]
    for index, knot in enumerate(knotvector):
        rhino_curve.Knots[index] = knot
    return rhino_curve


class RhinoNurbsCurve(NurbsCurve):
    """Class representing a NURBS curve based on the NurbsCurve of Rhino.Geometry.

    Attributes
    ----------
    points: List[Point]
        The control points of the curve.
    weights: List[float]
        The weights of the control points.
    knots: List[float]
        The knot vector, without duplicates.
    multiplicities: List[int]
        The multiplicities of the knots in the knot vector.
    knotsequence: List[float]
        The knot vector, with repeating values according to the multiplicities.
    degree: int
        The degree of the polynomials.
    order: int
        The order of the curve.
    domain: Tuple[float, float]
        The parameter domain.
    start: :class:`Point`
        The point corresponding to the start of the parameter domain.
    end: :class:`Point`
        The point corresponding to the end of the parameter domain.
    is_closed: bool
        True if the curve is closed.
    is_periodic: bool
        True if the curve is periodic.
    is_rational: bool
        True is the curve is rational.

    References
    ----------
    .. [2] https://developer.rhino3d.com/api/RhinoCommon/html/T_Rhino_Geometry_NurbsCurve.htm
    .. [3] https://en.wikipedia.org/wiki/Non-uniform_rational_B-spline
    .. [4] https://developer.rhino3d.com/guides/opennurbs/nurbs-geometry-overview/

    """

    def __init__(self, name=None):
        super(RhinoNurbsCurve, self).__init__(name=name)
        self.rhino_curve = None

    def __eq__(self, other):
        return self.rhino_curve.IsEqual(other.rhino_curve)

    # ==============================================================================
    # Data
    # ==============================================================================

    @property
    def data(self):
        return {
            'points': [point.data for point in self.points],
            'weights': self.weights,
            'knots': self.knots,
            'multiplicities': self.multiplicities,
            'degree': self.degree,
            'is_periodic': self.is_periodic,
        }

    @data.setter
    def data(self, data):
        points = [Point.from_data(point) for point in data['points']]
        weights = data['weights']
        knots = data['knots']
        multiplicities = data['multiplicities']
        degree = data['degree']
        # is_periodic = data['is_periodic']
        self.rhino_curve = rhino_curve_from_parameters(points, weights, knots, multiplicities, degree)

    @classmethod
    def from_data(cls, data):
        """Construct a NURBS curve from its data representation.

        Parameters
        ----------
        data : dict
            The data dictionary.

        Returns
        -------
        :class:`compas_occ.geometry.RhinoNurbsCurve`
            The constructed curve.

        """
        points = [Point.from_data(point) for point in data['points']]
        weights = data['weights']
        knots = data['knots']
        multiplicities = data['multiplicities']
        degree = data['degree']
        is_periodic = data['is_periodic']
        return NurbsCurve.from_parameters(points, weights, knots, multiplicities, degree, is_periodic)

    # ==============================================================================
    # Constructors
    # ==============================================================================

    @classmethod
    def from_rhino(cls, rhino_curve):
        """Construct a NURBS curve from an existing Rhino BSplineCurve."""
        curve = cls()
        curve.rhino_curve = rhino_curve
        return curve

    @classmethod
    def from_parameters(cls,
                        points,
                        weights,
                        knots,
                        multiplicities,
                        degree,
                        is_periodic=False):
        """Construct a NURBS curve from explicit curve parameters."""
        rhino_curve = rhino_curve_from_parameters(points, weights, knots, multiplicities, degree)
        # set periodicity => aparently not possible
        curve = cls()
        curve.rhino_curve = rhino_curve
        return curve

    @classmethod
    def from_points(cls, points, degree=3, is_periodic=False):
        """Construct a NURBS curve from control points.

        This construction method is similar to the method ``Create`` of the Rhino API for NURBS curves [1]_.

        References
        ----------
        .. [1] https://developer.rhino3d.com/api/RhinoCommon/html/M_Rhino_Geometry_NurbsCurve_Create.htm

        """
        # p = len(points)
        # weights = [1.0] * p
        # degree = degree if p > degree else p - 1
        # order = degree + 1
        # x = p - order
        # knots = [float(i) for i in range(2 + x)]
        # multiplicities = [order]
        # for _ in range(x):
        #     multiplicities.append(1)
        # multiplicities.append(order)
        points[:] = [point_to_rhino(point) for point in points]
        curve = cls()
        curve.rhino_curve = Rhino.Geometry.NurbsCurve.Create(is_periodic, degree, points)
        return curve

    @classmethod
    def from_interpolation(cls, points, precision=1e-3):
        """Construct a NURBS curve by interpolating a set of points.

        This construction method is similar to the method ``CreateHSpline`` of the Rhino API for NURBS curves [1]_.

        References
        ----------
        .. [1] https://developer.rhino3d.com/api/RhinoCommon/html/Overload_Rhino_Geometry_NurbsCurve_CreateHSpline.htm
        .. [2] https://dev.opencascade.org/doc/occt-7.4.0/refman/html/class_geom_a_p_i___interpolate.html

        """
        curve = cls()
        curve.rhino_curve = Rhino.Geometry.NurbsCurve.CreateHSpline([point_to_rhino(point) for point in points])
        return curve

    @classmethod
    def from_step(cls, filepath):
        """Load a NURBS curve from an STP file."""
        pass

    @classmethod
    def from_arc(cls, arc, degree, pointcount=None):
        pass

    @classmethod
    def from_circle(cls, circle):
        """Construct a NURBS curve from a circle.

        This construction method is similar to the method ``CreateFromCircle`` of the Rhino API for NURBS curves [1]_.

        References
        ----------
        .. [1] https://developer.rhino3d.com/api/RhinoCommon/html/Overload_Rhino_Geometry_NurbsCurve_CreateFromCircle.htm

        """
        curve = cls()
        curve.rhino_curve = Rhino.Geometry.NurbsCurve.CreateFromCircle(circle_to_rhino(circle))
        return curve

    @classmethod
    def from_ellipse(cls, ellipse):
        """Construct a NURBS curve from an ellipse.

        This construction method is similar to the method ``CreateFromEllipse`` of the Rhino API for NURBS curves [1]_.

        References
        ----------
        .. [1] https://developer.rhino3d.com/api/RhinoCommon/html/Overload_Rhino_Geometry_NurbsCurve_CreateFromEllipse.htm

        """
        curve = cls()
        curve.rhino_curve = Rhino.Geometry.NurbsCurve.CreateFromEllipse(ellipse_to_rhino(ellipse))
        return curve

    @classmethod
    def from_line(cls, line):
        """Construct a NURBS curve from a line.

        This construction method is similar to the method ``CreateFromLine`` of the Rhino API for NURBS curves [1]_.

        References
        ----------
        .. [1] https://developer.rhino3d.com/api/RhinoCommon/html/Overload_Rhino_Geometry_NurbsCurve_CreateFromLine.htm

        """
        curve = cls()
        curve.rhino_curve = Rhino.Geometry.NurbsCurve.CreateFromLine(line_to_rhino(line))
        return curve

    # ==============================================================================
    # Conversions
    # ==============================================================================

    def to_step(self, filepath, schema="AP203"):
        """Write the curve geometry to a STP file."""
        pass

    def to_line(self):
        pass

    def to_polyline(self):
        pass

    # ==============================================================================
    # Rhino
    # ==============================================================================

    # ==============================================================================
    # Properties
    # ==============================================================================

    @property
    def points(self):
        return [point_to_compas(point) for point in self.rhino_curve.Points]

    @property
    def weights(self):
        return [point.Weight for point in self.rhino_curve.Points]

    @property
    def knots(self):
        return [key for key, _ in groupby(self.rhino_curve.Knots)]

    @property
    def knotsequence(self):
        return list(self.rhino_curve.Knots)

    @property
    def multiplicities(self):
        return [len(list(group)) for _, group in groupby(self.rhino_curve.Knots)]

    @property
    def degree(self):
        return self.rhino_curve.Degree

    @property
    def dimension(self):
        return self.rhino_curve.Dimension

    @property
    def domain(self):
        return self.rhino_curve.Domain

    @property
    def order(self):
        return self.rhino_curve.Order

    @property
    def start(self):
        return point_to_compas(self.rhino_curve.PointAtStart)

    @property
    def end(self):
        return point_to_compas(self.rhino_curve.PointAtEnd)

    @property
    def is_closed(self):
        return self.rhino_curve.IsClosed

    @property
    def is_periodic(self):
        return self.rhino_curve.IsPeriodic

    @property
    def is_rational(self):
        return self.rhino_curve.IsRational

    # ==============================================================================
    # Methods
    # ==============================================================================

    def copy(self):
        """Make an independent copy of the current curve."""
        return RhinoNurbsCurve.from_parameters(
            self.points,
            self.weights,
            self.knots,
            self.multiplicities,
            self.degree,
            self.is_periodic
        )

    def transform(self, T):
        """Transform this curve."""
        raise NotImplementedError

    def transformed(self, T):
        """Transform a copy of the curve."""
        copy = self.copy()
        copy.transform(T)
        return copy

    def reverse(self):
        """Reverse the parametrisation of the curve."""
        raise NotImplementedError

    def space(self, n=10):
        """Compute evenly spaced parameters over the curve domain."""
        u, v = self.domain
        return linspace(u, v, n)

    def xyz(self, n=10):
        """Compute point locations corresponding to evenly spaced parameters over the curve domain."""
        return [self.point_at(param) for param in self.space(n)]

    def locus(self, resolution=100):
        """Compute the locus of the curve.

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
        return self.xyz(resolution)

    def point_at(self, u):
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
        raise NotImplementedError

    def tangent_at(self, t):
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
        raise NotImplementedError

    def curvature_at(self, t):
        """Compute the curvature at a point on the curve.

        Parameters
        ----------
        t : float
            The value of the curve parameter. Must be between 0 and 1.

        Returns
        -------
        Vector
            The corresponding curvature vector.

        """
        raise NotImplementedError

    def frame_at(self, t):
        """Compute the local frame at a point on the curve.

        Parameters
        ----------
        t : float
            The value of the curve parameter. Must be between 0 and 1.

        Returns
        -------
        Frame
            The corresponding local frame.

        """
        raise NotImplementedError

    def closest_point(self, point, parameter=False):
        """Compute the closest point on the curve to a given point.

        Parameters
        ----------
        point : Point
            The point to project orthogonally to the curve.
        parameter : bool, optional
            Return the projected point as well as the curve parameter.

        Returns
        -------
        Point or tuple
            The nearest point on the curve, if ``parameter`` is false.
            The nearest as (point, parameter) tuple, if ``parameter`` is true.
        """
        raise NotImplementedError

    def divide_by_count(self, count):
        """Divide the curve into a specific number of equal length segments."""
        raise NotImplementedError

    def divide_by_length(self, length):
        """Divide the curve into segments of specified length."""
        raise NotImplementedError

    def aabb(self, precision=0.0):
        """Compute the axis aligned bounding box of the curve."""
        raise NotImplementedError

    def obb(self, precision=0.0):
        """Compute the oriented bounding box of the curve."""
        raise NotImplementedError

    def length(self, precision=1e-3):
        """Compute the length of the curve."""
        raise NotImplementedError

    def segment(self, u, v, precision=1e-3):
        """Modifies this curve by segmenting it between the parameters u and v.

        Parameters
        ----------
        u: float
        v: float
        tol: float, optional
            default value is 1e-3

        Returns
        -------
        None

        """
        if u > v:
            u, v = v, u
        s, e = self.domain
        if u < s or v > e:
            raise ValueError('At least one of the given parameters is outside the curve domain.')
        if u == v:
            raise ValueError('The given domain is zero length.')
        raise NotImplementedError

    def segmented(self, u, v, precision=1e-3):
        """Returns a copy of this curve by segmenting it between the parameters u and v.

        Parameters
        ----------
        u: float
        v: float
        tol: float,optional
            default value is 1e-3

        Returns
        -------
        NurbsCurve

        """
        copy = self.copy()
        copy.segment(u, v, precision)
        return copy
