from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from math import sqrt

from compas.plugins import pluggable
from compas.geometry import Point
from compas.geometry import Frame

from .curve import Curve


@pluggable(category='factories')
def new_nurbscurve(cls, *args, **kwargs):
    raise NotImplementedError


@pluggable(category='factories')
def new_nurbscurve_from_parameters(cls, *args, **kwargs):
    raise NotImplementedError


@pluggable(category='factories')
def new_nurbscurve_from_points(cls, *args, **kwargs):
    raise NotImplementedError


@pluggable(category='factories')
def new_nurbscurve_from_interpolation(cls, *args, **kwargs):
    raise NotImplementedError


@pluggable(category='factories')
def new_nurbscurve_from_step(cls, *args, **kwargs):
    raise NotImplementedError


class NurbsCurve(Curve):
    """A NURBS curve is defined by control points, weights, knots, and a degree.

    Parameters
    ----------
    name : str, optional
        The name of the curve.

    Attributes
    ----------
    points : list[:class:`~compas.geometry.Point`], read-only
        The control points.
    weights : list[float], read-only
        The weights of the control points.
    knots : list[float], read-only
        The knots, without multiplicity.
    knotsequence : list[float], read-only
        The complete knot vector.
    multiplicity : list[int], read-only
        The multiplicities of the knots.
    continuity : int, read-only
        The degree of continuity of the curve.
    degree : int, read-only
        The degree of the curve.
    order : int, read-only
        The order of the curve (degree + 1).

    """

    def __new__(cls, *args, **kwargs):
        return new_nurbscurve(cls, *args, **kwargs)

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
    def DATASCHEMA(self):
        """:class:`schema.Schema` : Schema of the data."""
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
        """dict : Schema of the curve data in JSON format."""
        raise NotImplementedError

    @property
    def dtype(self):
        """str : The type of the object in the form of a '2-level' import and a class name."""
        return 'compas.geometry/NurbsCurve'

    @property
    def data(self):
        """dict : Representation of the curve as a dict containing only native Python data."""
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
        :class:`~compas.geometry.NurbsCurve`
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
    # Properties
    # ==============================================================================

    @property
    def points(self):
        raise NotImplementedError

    @property
    def weights(self):
        raise NotImplementedError

    @property
    def knots(self):
        raise NotImplementedError

    @property
    def knotsequence(self):
        raise NotImplementedError

    @property
    def multiplicities(self):
        raise NotImplementedError

    @property
    def continuity(self):
        raise NotImplementedError

    @property
    def degree(self):
        raise NotImplementedError

    @property
    def order(self):
        return self.degree + 1

    @property
    def is_rational(self):
        raise NotImplementedError

    # ==============================================================================
    # Constructors
    # ==============================================================================

    @classmethod
    def from_step(cls, filepath):
        """Load a NURBS curve from an STP file.

        Parameters
        ----------
        filepath : str
            The path to the file.

        Returns
        -------
        :class:`~compas.geometry.NurbsCurve`
        """
        return new_nurbscurve_from_step(cls, filepath)

    @classmethod
    def from_parameters(cls, points, weights, knots, multiplicities, degree, is_periodic=False):
        """Construct a NURBS curve from explicit curve parameters.

        Parameters
        ----------
        points : list[[float, float, float] | :class:`~compas.geometry.Point`]
            The control points.
        weights : list[float]
            The weights of the control points.
        knots : list[float]
            The curve knots, without multiplicity.
        multiplicities : list[int]
            Multiplicity of the knots.
        degree : int
            Degree of the curve.
        is_periodic : bool, optional
            Flag indicating that the curve is periodic.

        Returns
        -------
        :class:`~compas.geometry.NurbsCurve`

        """
        return new_nurbscurve_from_parameters(cls, points, weights, knots, multiplicities, degree, is_periodic=False)

    @classmethod
    def from_points(cls, points, degree=3):
        """Construct a NURBS curve from control points.

        Parameters
        ----------
        points : list[[float, float, float] | :class:`~compas.geometry.Point`]
            The control points.
        degree : int, optional
            The degree of the curve.

        Returns
        -------
        :class:`~compas.geometry.NurbsCurve`

        """
        return new_nurbscurve_from_points(cls, points, degree=degree)

    @classmethod
    def from_interpolation(cls, points, precision=1e-3):
        """Construct a NURBS curve by interpolating a set of points.

        Parameters
        ----------
        points : list[[float, float, float] | :class:`~compas.geometry.Point`]
            A list of interpolation points.
        precision : int, optional
            The desired precision of the interpolation.

        Returns
        -------
        :class:`~compas.geometry.NurbsCurve`

        """
        return new_nurbscurve_from_interpolation(cls, points, precision=1e-3)

    @classmethod
    def from_arc(cls, arc):
        """Construct a NURBS curve from an arc.

        Parameters
        ----------
        arc : :class:`~compas.geometry.Arc`

        Returns
        -------
        :class:`~compas.geometry.NurbsCurve`

        """
        raise NotImplementedError

    @classmethod
    def from_circle(cls, circle):
        """Construct a NURBS curve from a circle.

        Parameters
        ----------
        circle : :class:`~compas.geometry.Circle`

        Returns
        -------
        :class:`~compas.geometry.NurbsCurve`

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
        ellipse : :class:`~compas.geometry.Ellipse`

        Returns
        -------
        :class:`~compas.geometry.NurbsCurve`

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
        line : :class:`~compas.geometry.Line`

        Returns
        -------
        :class:`~compas.geometry.NurbsCurve`

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

    # ==============================================================================
    # Methods
    # ==============================================================================

    def copy(self):
        """Make an independent copy of the current curve.

        Returns
        -------
        :class:`~compas.geometry.NurbsCurve`

        """
        return NurbsCurve.from_parameters(
            self.points,
            self.weights,
            self.knots,
            self.multiplicities,
            self.degree,
            self.is_periodic
        )
