from itertools import groupby
from compas.geometry import Point
from compas.utilities import linspace

try:
    from compas.geometry import NurbsCurve
except ImportError:
    from compas.geometry import Geometry as NurbsCurve

from compas_rhino.conversions import point_to_rhino
from compas_rhino.conversions import point_to_compas
from compas_rhino.conversions import vector_to_compas
from compas_rhino.conversions import circle_to_rhino
from compas_rhino.conversions import ellipse_to_rhino
from compas_rhino.conversions import line_to_rhino
from compas_rhino.conversions import xform_to_rhino
from compas_rhino.conversions import plane_to_compas_frame
from compas_rhino.conversions import box_to_compas

import Rhino.Geometry


def rhino_curve_from_parameters(points, weights, knots, multiplicities, degree):
    rhino_curve = Rhino.Geometry.NurbsCurve(3, True, degree + 1, len(points))
    for index, (point, weight) in enumerate(zip(points, weights)):
        rhino_curve.Points.SetPoint(index, point_to_rhino(point), weight)
    knotvector = [knot for knot, mult in zip(knots, multiplicities) for _ in range(mult)]
    # account for superfluous knots
    # https://developer.rhino3d.com/guides/opennurbs/superfluous-knots/
    p = len(points)
    o = degree + 1
    k = p + o
    if len(knotvector) == k:
        knotvector[:] = knotvector[1:-1]
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
        # add superfluous knots
        # for compatibility with all/most other NURBS implementations
        # https://developer.rhino3d.com/guides/opennurbs/superfluous-knots/
        multiplicities = self.multiplicities[:]
        multiplicities[0] += 1
        multiplicities[-1] += 1
        return {
            'points': [point.data for point in self.points],
            'weights': self.weights,
            'knots': self.knots,
            'multiplicities': multiplicities,
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
        # have not found a way to actually set this
        # not sure if that is actually possible...
        self.rhino_curve = rhino_curve_from_parameters(points, weights, knots, multiplicities, degree)

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
        curve = cls()
        # set periodicity => aparently not possible
        curve.rhino_curve = rhino_curve_from_parameters(points, weights, knots, multiplicities, degree)
        return curve

    @classmethod
    def from_points(cls, points, degree=3, is_periodic=False):
        """Construct a NURBS curve from control points.

        This construction method is similar to the method ``Create`` of the Rhino API for NURBS curves [1]_.

        References
        ----------
        .. [1] https://developer.rhino3d.com/api/RhinoCommon/html/M_Rhino_Geometry_NurbsCurve_Create.htm

        """
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
        raise NotImplementedError

    @classmethod
    def from_arc(cls, arc):
        """Construct a NURBS curve from an arc.

        This construction method is similar to the method ``CreateFromArc`` of the Rhino API for NURBS curves [1]_.

        References
        ----------
        .. [1] https://developer.rhino3d.com/api/RhinoCommon/html/Overload_Rhino_Geometry_NurbsCurve_CreateFromArc.htm

        """
        # curve = cls()
        # curve.rhino_curve = Rhino.Geometry.NurbsCurve.CreateFromArc(arc_to_rhino(arc))
        # return curve
        raise NotImplementedError

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
        raise NotImplementedError

    def to_line(self):
        """Convert the NURBS curve to a line."""
        raise NotImplementedError

    def to_polyline(self):
        """Convert the NURBS curve to a polyline."""
        raise NotImplementedError

    # ==============================================================================
    # Rhino
    # ==============================================================================

    # ==============================================================================
    # Properties
    # ==============================================================================

    @property
    def points(self):
        """list of :class:`compas.geometry.Point`: The control points."""
        return [point_to_compas(point) for point in self.rhino_curve.Points]

    @property
    def weights(self):
        """list of float: The weights of the control points."""
        return [point.Weight for point in self.rhino_curve.Points]

    @property
    def knots(self):
        """list of float: Knots without repeating elements."""
        return [key for key, _ in groupby(self.rhino_curve.Knots)]

    @property
    def knotsequence(self):
        """list of float: Knots with multiplicities."""
        return list(self.rhino_curve.Knots)

    @property
    def multiplicities(self):
        """list of int: Multiplicities of the knots."""
        return [len(list(group)) for _, group in groupby(self.rhino_curve.Knots)]

    @property
    def degree(self):
        """int: The degree of the curve (degree = order - 1)."""
        return self.rhino_curve.Degree

    @property
    def dimension(self):
        """int: The dimension of the curve."""
        return self.rhino_curve.Dimension

    @property
    def domain(self):
        """tuple of float: The parameter domain of the curve."""
        return self.rhino_curve.Domain.T0, self.rhino_curve.Domain.T1

    @property
    def order(self):
        """int: The order of the curve (order = degree + 1)."""
        return self.rhino_curve.Order

    @property
    def start(self):
        """:class:`compas.geometry.Point`: The point at the start of the curve."""
        return point_to_compas(self.rhino_curve.PointAtStart)

    @property
    def end(self):
        """:class:`compas.geometry.Point`: The point at the end of the curve."""
        return point_to_compas(self.rhino_curve.PointAtEnd)

    @property
    def is_closed(self):
        """bool"""
        return self.rhino_curve.IsClosed

    @property
    def is_periodic(self):
        """bool"""
        return self.rhino_curve.IsPeriodic

    @property
    def is_rational(self):
        """bool"""
        return self.rhino_curve.IsRational

    # ==============================================================================
    # Methods
    # ==============================================================================

    def copy(self):
        """Make an independent copy of the current curve."""
        # return RhinoNurbsCurve.from_parameters(
        #     self.points,
        #     self.weights,
        #     self.knots,
        #     self.multiplicities,
        #     self.degree,
        #     self.is_periodic
        # )
        cls = type(self)
        curve = cls()
        curve.rhino_curve = self.rhino_curve.Duplicate()
        return curve

    def transform(self, T):
        """Transform this curve."""
        self.rhino_curve.Transform(xform_to_rhino(T))

    def transformed(self, T):
        """Transform a copy of the curve."""
        copy = self.copy()
        copy.transform(T)
        return copy

    def reverse(self):
        """Reverse the parametrisation of the curve."""
        self.rhino_curve.Reverse()

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

    def point_at(self, t):
        """Compute a point on the curve.

        Parameters
        ----------
        t : float
            The value of the curve parameter. Must be between 0 and 1.

        Returns
        -------
        :class:`compas.geometry.Point`
            the corresponding point on the curve.
        """
        point = self.rhino_curve.PointAt(t)
        return point_to_compas(point)

    def tangent_at(self, t):
        """Compute the tangent vector at a point on the curve.

        Parameters
        ----------
        t : float
            The value of the curve parameter. Must be between 0 and 1.

        Returns
        -------
        :class:`compas.geometry.Vector`
            The corresponding tangent vector.

        """
        vector = self.rhino_curve.TangentAt(t)
        return vector_to_compas(vector)

    def curvature_at(self, t):
        """Compute the curvature at a point on the curve.

        Parameters
        ----------
        t : float
            The value of the curve parameter. Must be between 0 and 1.

        Returns
        -------
        :class:`compas.geometry.Vector`
            The corresponding curvature vector.

        """
        vector = self.rhino_curve.CurvatureAt(t)
        return vector_to_compas(vector)

    def frame_at(self, t):
        """Compute the local frame at a point on the curve.

        Parameters
        ----------
        t : float
            The value of the curve parameter. Must be between 0 and 1.

        Returns
        -------
        :class:`compas.geometry.Frame`
            The corresponding local frame.

        """
        plane = self.rhino_curve.FrameAt(t)
        return plane_to_compas_frame(plane)

    def closest_point(self, point, return_parameter=False):
        """Compute the closest point on the curve to a given point.

        Parameters
        ----------
        point : Point
            The point to project orthogonally to the curve.
        return_parameter : bool, optional
            Return the curve parameter in addition to the projected point.

        Returns
        -------
        :class:`compas.geometry.Point` or tuple of :class:`compas.geometry.Point` and float
            The nearest point on the curve, if ``parameter`` is false.
            The nearest as (point, parameter) tuple, if ``parameter`` is true.
        """
        point, t = self.rhino_curve.ClosestPoint(point)
        point = point_to_compas(point)
        if return_parameter:
            return point, t
        return point

    def divide_by_count(self, count, return_points=False):
        """Divide the curve into a specific number of equal length segments.

        Parameters
        ----------
        count : int
            The number of segments.
        return_points : bool, optional
            If ``True``, return the list of division parameters,
            and the points corresponding to those parameters.
            If ``False``, return only the list of parameters.

        Returns
        -------
        list of float or tuple of list of float and list of :class:`compas.geometry.Point`
            The parameters defining the discretisation,
            and potentially the points corresponding to those parameters.
        """
        params = self.rhino_curve.DivideByCount(count, True)
        if return_points:
            points = [self.point_at(t) for t in params]
            return params, points
        return params

    def divide_by_length(self, length, return_points=False):
        """Divide the curve into segments of specified length.

        Parameters
        ----------
        length : float
            The length of the segments.
        return_points : bool, optional
            If ``True``, return the list of division parameters,
            and the points corresponding to those parameters.
            If ``False``, return only the list of parameters.

        Returns
        -------
        list of float or tuple of list of float and list of :class:`compas.geometry.Point`
            The parameters defining the discretisation,
            and potentially the points corresponding to those parameters.
        """
        params = self.rhino_curve.DivideByLength(length, True)
        if return_points:
            points = [self.point_at(t) for t in params]
            return params, points
        return params

    def aabb(self):
        """Compute the axis aligned bounding box of the curve.

        Returns
        -------
        :class:`compas.geometry.Box`
        """
        box = self.rhino_curve.getBoundingBox(True)
        return box_to_compas(box)

    def obb(self, precision=0.0):
        """Compute the oriented bounding box of the curve."""
        raise NotImplementedError

    def length(self, precision=1e-8):
        """Compute the length of the curve."""
        return self.rhino_curve.GetLength(precision)

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
