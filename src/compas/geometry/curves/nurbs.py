from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from math import sqrt

from compas.geometry import Frame
from compas.geometry import Point
from compas.plugins import PluginNotInstalledError
from compas.plugins import pluggable

from .curve import Curve


@pluggable(category="factories")
def nurbscurve_from_interpolation(cls, *args, **kwargs):
    raise PluginNotInstalledError


@pluggable(category="factories")
def nurbscurve_from_native(cls, *args, **kwargs):
    raise PluginNotInstalledError


@pluggable(category="factories")
def nurbscurve_from_parameters(cls, *args, **kwargs):
    raise PluginNotInstalledError


@pluggable(category="factories")
def nurbscurve_from_points(cls, *args, **kwargs):
    raise PluginNotInstalledError


@pluggable(category="factories")
def nurbscurve_from_step(cls, *args, **kwargs):
    raise PluginNotInstalledError


class NurbsCurve(Curve):
    """A NURBS curve is defined by control points, weights, knots, and a degree.

    Parameters
    ----------
    name : str, optional
        The name of the curve.

    Attributes
    ----------
    points : list[:class:`compas.geometry.Point`], read-only
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

    DATASCHEMA = {
        "type": "object",
        "properties": {
            "points": {"type": "array", "minItems": 2, "items": Point.DATASCHEMA},
            "weights": {"type": "array", "items": {"type": "number"}},
            "knots": {"type": "array", "items": {"type": "number"}},
            "multiplicities": {"type": "array", "items": {"type": "integer"}},
            "degree": {"type": "integer", "exclusiveMinimum": 0},
            "is_periodic": {"type": "boolean"},
        },
        "additionalProperties": False,
        "minProperties": 6,
    }

    @property
    def __dtype__(self):
        return "compas.geometry/NurbsCurve"

    @property
    def __data__(self):
        return {
            "points": [point.__data__ for point in self.points],
            "weights": self.weights,
            "knots": self.knots,
            "multiplicities": self.multiplicities,
            "degree": self.degree,
            "is_periodic": self.is_periodic,
        }

    @classmethod
    def __from_data__(cls, data):
        return cls.from_parameters(
            data["points"],  # conversion is not needed because point data can be provided in raw form as well
            data["weights"],
            data["knots"],
            data["multiplicities"],
            data["degree"],
            data["is_periodic"],
        )

    def __new__(cls, *args, **kwargs):
        if cls is NurbsCurve:
            raise TypeError("Making an instance of `NurbsCurve` using `NurbsCurve()` is not allowed. Please use one of the factory methods instead (`NurbsCurve.from_...`)")
        return object.__new__(cls)

    def __repr__(self):
        return "{0}(points={1!r}, weigths={2}, knots={3}, multiplicities={4}, degree={5}, is_periodic={6})".format(
            type(self).__name__,
            self.points,
            self.weights,
            self.knots,
            self.multiplicities,
            self.degree,
            self.is_periodic,
        )

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
    def multiplicities(self):
        raise NotImplementedError

    @property
    def knotvector(self):
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
    def from_arc(cls, arc):
        """Construct a NURBS curve from an arc.

        Parameters
        ----------
        arc : :class:`compas.geometry.Arc`

        Returns
        -------
        :class:`compas.geometry.NurbsCurve`

        """
        raise NotImplementedError

    @classmethod
    def from_circle(cls, circle):
        """Construct a NURBS curve from a circle.

        Parameters
        ----------
        circle : :class:`compas.geometry.Circle`

        Returns
        -------
        :class:`compas.geometry.NurbsCurve`

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
            frame.point - dy,
        ]
        knots = [0, 1 / 4, 1 / 2, 3 / 4, 1]
        mults = [3, 2, 2, 2, 3]
        weights = [1, w, 1, w, 1, w, 1, w, 1]
        return cls.from_parameters(points=points, weights=weights, knots=knots, multiplicities=mults, degree=2)

    @classmethod
    def from_ellipse(cls, ellipse):
        """Construct a NURBS curve from an ellipse.

        Parameters
        ----------
        ellipse : :class:`compas.geometry.Ellipse`

        Returns
        -------
        :class:`compas.geometry.NurbsCurve`

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
            frame.point - dy,
        ]
        knots = [0, 1 / 4, 1 / 2, 3 / 4, 1]
        mults = [3, 2, 2, 2, 3]
        weights = [1, w, 1, w, 1, w, 1, w, 1]
        return cls.from_parameters(points=points, weights=weights, knots=knots, multiplicities=mults, degree=2)

    @classmethod
    def from_interpolation(cls, points, precision=1e-3):
        """Construct a NURBS curve by interpolating a set of points.

        Parameters
        ----------
        points : list[[float, float, float] | :class:`compas.geometry.Point`]
            A list of interpolation points.
        precision : int, optional
            The desired precision of the interpolation.

        Returns
        -------
        :class:`compas.geometry.NurbsCurve`

        """
        return nurbscurve_from_interpolation(cls, points, precision=1e-3)

    @classmethod
    def from_line(cls, line):
        """Construct a NURBS curve from a line.

        Parameters
        ----------
        line : :class:`compas.geometry.Line`

        Returns
        -------
        :class:`compas.geometry.NurbsCurve`

        """
        return cls.from_parameters(
            points=[line.start, line.end],
            weights=[1.0, 1.0],
            knots=[0.0, 1.0],
            multiplicities=[2, 2],
            degree=1,
        )

    @classmethod
    def from_native(cls, curve):
        """Construct a NURBS curve from a CAD-native curve geometry.

        Parameters
        ----------
        curve
            A CAD-native curve geometry.

        Returns
        -------
        :class:`compas.geometry.NurbsCurve`
            A COMPAS NURBS curve.

        """
        return nurbscurve_from_native(cls, curve)

    @classmethod
    def from_parameters(cls, points, weights, knots, multiplicities, degree, is_periodic=False):
        """Construct a NURBS curve from explicit curve parameters.

        Parameters
        ----------
        points : list[[float, float, float] | :class:`compas.geometry.Point`]
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
        :class:`compas.geometry.NurbsCurve`

        """
        return nurbscurve_from_parameters(cls, points, weights, knots, multiplicities, degree, is_periodic=False)

    @classmethod
    def from_points(cls, points, degree=3):
        """Construct a NURBS curve from control points.

        Parameters
        ----------
        points : list[[float, float, float] | :class:`compas.geometry.Point`]
            The control points.
        degree : int, optional
            The degree of the curve.

        Returns
        -------
        :class:`compas.geometry.NurbsCurve`

        """
        return nurbscurve_from_points(cls, points, degree=degree)

    @classmethod
    def from_step(cls, filepath):
        """Load a NURBS curve from an STP file.

        Parameters
        ----------
        filepath : str
            The path to the file.

        Returns
        -------
        :class:`compas.geometry.NurbsCurve`
        """
        return nurbscurve_from_step(cls, filepath)

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
        :class:`compas.geometry.NurbsCurve`

        """
        return NurbsCurve.from_parameters(
            self.points,
            self.weights,
            self.knots,
            self.multiplicities,
            self.degree,
            self.is_periodic,
        )

    def insert_knot(self):
        pass

    def refine_knot(self):
        pass

    def remove_knot(self):
        pass

    def elevate_degree(self):
        pass

    def reduce_degree(self):
        pass
