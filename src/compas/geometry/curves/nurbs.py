from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from math import sqrt

from compas.plugins import pluggable
from compas.geometry import Point
from compas.geometry import Frame
from compas.utilities import linspace

from .curve import Curve


@pluggable(category='factories')
def new_nurbscurve(*args, **kwargs):
    raise NotImplementedError


@pluggable(category='factories')
def new_nurbscurve_from_parameters(*args, **kwargs):
    raise NotImplementedError


@pluggable(category='factories')
def new_nurbscurve_from_points(*args, **kwargs):
    raise NotImplementedError


@pluggable(category='factories')
def new_nurbscurve_from_interpolation(*args, **kwargs):
    raise NotImplementedError


@pluggable(category='factories')
def new_nurbscurve_from_step(*args, **kwargs):
    raise NotImplementedError


class NurbsCurve(Curve):
    """Class representing a NURBS curve.

    Parameters
    ----------
    name : str, optional
        The name of the curve.
    """

    @property
    def DATASCHEMA(self):
        """:class:`schema.Schema` - Schema of the data."""
        from schema import Schema
        from compas.data import is_float3
        from compas.data import is_sequence_of_int
        from compas.data import is_sequence_of_float
        return Schema({
            'points': lambda points: all(is_float3(point) for point in points),
            'weights': is_sequence_of_float,
            'knots': is_sequence_of_float,
            'multiplicities': is_sequence_of_int,
            'degree': int,
            'is_periodic': bool
        })

    @property
    def JSONSCHEMANAME(self):
        """dict - Schema of the curve data in JSON format."""
        raise NotImplementedError

    def __new__(cls, *args, **kwargs):
        return new_nurbscurve(*args, **kwargs)

    def __init__(self, name=None):
        super(NurbsCurve, self).__init__(name=name)

    def __eq__(self, other):
        raise NotImplementedError

    def __str__(self):
        lines = [
            'NurbsCurve',
            '----------',
            'Points: {}'.format(self.points),
            'Weights: {}'.format(self.weights),
            'Knots: {}'.format(self.knots),
            'Mults: {}'.format(self.multiplicities),
            'Degree: {}'.format(self.degree),
            'Order: {}'.format(self.order),
            'Domain: {}'.format(self.domain),
            'Closed: {}'.format(self.is_closed),
            'Periodic: {}'.format(self.is_periodic),
            'Rational: {}'.format(self.is_rational),
        ]
        return "\n".join(lines)

    # ==============================================================================
    # Data
    # ==============================================================================

    @property
    def dtype(self):
        """str - The type of the object in the form of a '2-level' import and a class name."""
        return 'compas.geometry/NurbsCurve'

    @property
    def data(self):
        """dict - Representation of the curve as a dict containing only native Python data."""
        return {
            'points': [point.data for point in self.points],
            'weights': self.weights,
            'knots': self.knots,
            'multiplicities': self.multiplicities,
            'degree': self.degree,
            'is_periodic': self.is_periodic
        }

    @data.setter
    def data(self, data):
        raise NotImplementedError

    @classmethod
    def from_data(cls, data):
        """Construct a NURBS curve from its data representation.

        Parameters
        ----------
        data : dict
            The data dictionary.

        Returns
        -------
        :class:`compas.geometry.NurbsCurve`
            The constructed curve.

        """
        points = [Point.from_data(point) for point in data['points']]
        weights = data['weights']
        knots = data['knots']
        multiplicities = data['multiplicities']
        degree = data['degree']
        is_periodic = data['is_periodic']
        return cls.from_parameters(points, weights, knots, multiplicities, degree, is_periodic)

    # ==============================================================================
    # Constructors
    # ==============================================================================

    @classmethod
    def from_parameters(cls, points, weights, knots, multiplicities, degree, is_periodic=False):
        """Construct a NURBS curve from explicit curve parameters.

        Parameters
        ----------
        points : List[:class:`compas.geometry.Point`]
            The control points.
        weights : List[float]
            The weights of the control points.
        knots : List[float]
            The curve knots, without multiplicity.
        multiplicities : List[int]
            Multiplicity of the knots.
        degree : int
            Degree of the curve.
        is_periodic : bool, optional
            Flag indicating that the curve is periodic.

        Returns
        -------
        :class:`NurbsCurve`
        """
        return new_nurbscurve_from_parameters(points, weights, knots, multiplicities, degree, is_periodic=False)

    @classmethod
    def from_points(cls, points, degree=3):
        """Construct a NURBS curve from control points.

        Parameters
        ----------
        points : List[:class:`compas.geometry.Point`]
            The control points.
        degree : int, optional
            The degree of the curve.

        Returns
        -------
        :class:`NurbsCurve`

        References
        ----------
        * https://developer.rhino3d.com/api/RhinoCommon/html/M_Rhino_Geometry_NurbsCurve_Create.htm

        """
        return new_nurbscurve_from_points(points, degree=degree)

    @classmethod
    def from_interpolation(cls, points, precision=1e-3):
        """Construct a NURBS curve by interpolating a set of points.

        Parameters
        ----------
        points : List[:class:`compas.geometry.Point`]
            A list of interpolation points.
        precision : int, optional
            The desired precision of the interpolation.

        Returns
        -------
        :class:`NurbsCurve`

        References
        ----------
        * https://developer.rhino3d.com/api/RhinoCommon/html/Overload_Rhino_Geometry_NurbsCurve_CreateHSpline.htm

        """
        return new_nurbscurve_from_interpolation(points, precision=1e-3)

    @classmethod
    def from_step(cls, filepath):
        """Load a NURBS curve from an STP file.

        Parameters
        ----------
        filepath : str
            The path to the file.

        Returns
        -------
        :class:`NurbsCurve`
        """
        return new_nurbscurve_from_step(filepath)

    @classmethod
    def from_arc(cls, arc):
        raise NotImplementedError

    @classmethod
    def from_circle(cls, circle):
        """Construct a NURBS curve from a circle.

        Parameters
        ----------
        circle : :class:`compas.geometry.Circle`

        Returns
        -------
        :class:`NurbsCurve`

        References
        ----------
        * https://developer.rhino3d.com/api/RhinoCommon/html/Overload_Rhino_Geometry_NurbsCurve_CreateFromCircle.htm

        """
        frame = Frame.from_plane(circle.plane)
        w = 0.5 * sqrt(2)
        dx = frame.xaxis * circle.radius
        dy = frame.yaxis * circle.radius
        points = [
            frame.point - dy,
            frame.point - dy - dx,
            frame.point - dx,
            frame.point + dy - dx,
            frame.point + dy,
            frame.point + dy + dx,
            frame.point + dx,
            frame.point - dy + dx,
            frame.point - dy
        ]
        knots = [0, 1/4, 1/2, 3/4, 1]
        mults = [3, 2, 2, 2, 3]
        weights = [1, w, 1, w, 1, w, 1, w, 1]
        return cls.from_parameters(
            points=points, weights=weights, knots=knots, multiplicities=mults, degree=2
        )

    @classmethod
    def from_ellipse(cls, ellipse):
        """Construct a NURBS curve from an ellipse.

        Parameters
        ----------
        ellipse : :class:`compas.geometry.Ellipse`

        Returns
        -------
        :class:`NurbsCurve`

        References
        ----------
        * https://developer.rhino3d.com/api/RhinoCommon/html/Overload_Rhino_Geometry_NurbsCurve_CreateFromEllipse.htm

        """
        frame = Frame.from_plane(ellipse.plane)
        frame = Frame.worldXY()
        w = 0.5 * sqrt(2)
        dx = frame.xaxis * ellipse.major
        dy = frame.yaxis * ellipse.minor
        points = [
            frame.point - dy,
            frame.point - dy - dx,
            frame.point - dx,
            frame.point + dy - dx,
            frame.point + dy,
            frame.point + dy + dx,
            frame.point + dx,
            frame.point - dy + dx,
            frame.point - dy
        ]
        knots = [0, 1/4, 1/2, 3/4, 1]
        mults = [3, 2, 2, 2, 3]
        weights = [1, w, 1, w, 1, w, 1, w, 1]
        return cls.from_parameters(
            points=points, weights=weights, knots=knots, multiplicities=mults, degree=2
        )

    @classmethod
    def from_line(cls, line):
        """Construct a NURBS curve from a line.

        Parameters
        ----------
        line : :class:`compas.geometry.Line`

        Returns
        -------
        :class:`NurbsCurve`

        References
        ----------
        * https://developer.rhino3d.com/api/RhinoCommon/html/Overload_Rhino_Geometry_NurbsCurve_CreateFromLine.htm

        """
        return cls.from_parameters(
            points=[line.start, line.end],
            weights=[1.0, 1.0],
            knots=[0.0, 1.0],
            multiplicities=[2, 2],
            degree=1
        )

    # ==============================================================================
    # Conversions
    # ==============================================================================

    def to_step(self, filepath, schema="AP203"):
        """Write the curve geometry to a STP file.

        Parameters
        ----------
        filepath : str
            The path of the output file.
        """
        raise NotImplementedError

    # ==============================================================================
    # Properties
    # ==============================================================================

    @property
    def points(self):
        """List[:class:`compas.geometry.Point`] - The control points."""
        raise NotImplementedError

    @property
    def weights(self):
        """List[float] - The weights of the control points."""
        raise NotImplementedError

    @property
    def knots(self):
        """List[float] - The knots, without multiplicity."""
        raise NotImplementedError

    @property
    def knotsequence(self):
        """List[float] - The complete knot vector."""
        raise NotImplementedError

    @property
    def multiplicities(self):
        """List[int] - The multiplicities of the knots."""
        raise NotImplementedError

    @property
    def degree(self):
        """int - The degree of the curve."""
        raise NotImplementedError

    @property
    def dimension(self):
        """int - The spatial dimension of the curve."""
        raise NotImplementedError

    @property
    def domain(self):
        """Tuple[float, float] - The domain of the parameter space of the curve."""
        raise NotImplementedError

    @property
    def order(self):
        """int - The order of the curve (degree + 1)."""
        return self.degree + 1

    @property
    def start(self):
        """:class:`compas.geometry.Point` - The start point of the curve."""
        raise NotImplementedError

    @property
    def end(self):
        """:class:`compas.geometry.Point` - The end point of the curve."""
        raise NotImplementedError

    @property
    def is_closed(self):
        """bool - Flag indicating that the curve is closed."""
        raise NotImplementedError

    @property
    def is_periodic(self):
        """bool - Flag indicating that the curve is periodic."""
        raise NotImplementedError

    @property
    def is_rational(self):
        """bool - Flag indicating that the curve is rational.
        If the curve is rational, the weights of the control points are rational numbers."""
        raise NotImplementedError

    @property
    def bounding_box(self):
        """:class:`compas.geometry.Box` - The axis aligned bounding box of the curve."""
        raise NotImplementedError

    @property
    def length(self):
        """float - The length of the curve."""
        raise NotImplementedError

    # ==============================================================================
    # Methods
    # ==============================================================================

    def copy(self):
        """Make an independent copy of the current curve.

        Returns
        -------
        :class:`NurbsCurve`
        """
        return NurbsCurve.from_parameters(
            self.points,
            self.weights,
            self.knots,
            self.multiplicities,
            self.degree,
            self.is_periodic
        )

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
        raise NotImplementedError

    def transformed(self, T):
        """Transform a copy of the curve.

        Parameters
        ----------
        T : :class:`compas.geometry.Transformation`
            The transformation.

        Returns
        -------
        :class:`NurbsCurve`
        """
        copy = self.copy()
        copy.transform(T)
        return copy

    def space(self, n=10):
        """Compute evenly spaced parameters over the curve domain.

        Parameters
        ----------
        n : int, optional
            The number of values in the parameter space.

        Returns
        -------
        List[float]
        """
        start, end = self.domain
        return linspace(start, end, n)

    def xyz(self, n=10):
        """Compute point locations corresponding to evenly spaced parameters over the curve domain.

        Parameters
        ----------
        n : int, optional
            The number of points in the discretisation.

        Returns
        -------
        List[:class:`compas.geometry.Point`]
        """
        return [self.point_at(t) for t in self.space(n)]

    def locus(self, resolution=100):
        """Compute the locus of all points on the curve.

        Parameters
        ----------
        resolution : int
            The number of intervals at which a point on the
            curve should be computed. Defaults to 100.

        Returns
        -------
        List[:class:`compas.geometry.Point`]
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
        raise NotImplementedError

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
        raise NotImplementedError

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
        raise NotImplementedError

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
        raise NotImplementedError

    def closest_point(self, point, return_parameter=False):
        """Compute the closest point on the curve to a given point.

        Parameters
        ----------
        point : :class:`compas.geometry.Point`
            The test point.
        return_parameter : bool, optional
            Flag to indicate that the parameter corresponding to the closest point
            should be returned as well.

        Returns
        -------
        :class:`compas.geometry.Point`
            If ``return_parameter`` is false.
        (:class:`compas.geometry.Point`, float)
            If ``return_parameter`` is true.
        """
        raise NotImplementedError

    def divide_by_count(self, count):
        """Divide the curve into a specific number of equal length segments.

        Parameters
        ----------
        count : int
            The number of segments.

        Returns
        -------
        List[:class:`NurbsCurve`]
        """
        raise NotImplementedError

    def divide_by_length(self, length):
        """Divide the curve into segments of specified length.

        Parameters
        ----------
        length : float
            The length of the segments.

        Returns
        -------
        List[:class:`NurbsCurve`]
        """
        raise NotImplementedError

    def fair(self):
        raise NotImplementedError
