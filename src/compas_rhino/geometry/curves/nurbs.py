from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from itertools import groupby

import Rhino.Geometry  # type: ignore

from compas.geometry import NurbsCurve
from compas.geometry import Point
from compas_rhino.conversions import point_to_compas
from compas_rhino.conversions import point_to_rhino

from .curve import RhinoCurve


def native_curve_from_parameters(points, weights, knots, multiplicities, degree):
    native_curve = Rhino.Geometry.NurbsCurve(3, True, degree + 1, len(points))
    for index, (point, weight) in enumerate(zip(points, weights)):
        native_curve.Points.SetPoint(index, point_to_rhino(point), weight)
    knotvector = [knot for knot, mult in zip(knots, multiplicities) for _ in range(mult)]
    # account for superfluous knots
    # https://developer.rhino3d.com/guides/opennurbs/superfluous-knots/
    p = len(points)
    o = degree + 1
    k = p + o
    if len(knotvector) == k:
        knotvector[:] = knotvector[1:-1]
    for index, knot in enumerate(knotvector):
        native_curve.Knots[index] = knot
    return native_curve


class RhinoNurbsCurve(RhinoCurve, NurbsCurve):
    """Class representing a NURBS curve based on the NurbsCurve of Rhino.Geometry.

    Parameters
    ----------
    name : str, optional
        Name of the curve.

    Attributes
    ----------
    points : list[:class:`compas.geometry.Point`], read-only
        The control points of the curve.
    weights : list[float], read-only
        The weights of the control points.
    knots : list[float], read-only
        The knot vector, without duplicates.
    multiplicities : list[int], read-only
        The multiplicities of the knots in the knot vector.
    knotsequence : list[float], read-only
        The knot vector, with repeating values according to the multiplicities.
    continuity : int, read-only
        The degree of continuity of the curve.
    degree : int, read-only
        The degree of the curve.
    order : int, read-only
        The order of the curve (degree + 1).
    is_rational : bool, read-only
        True is the curve is rational.

    References
    ----------
    * https://developer.rhino3d.com/api/RhinoCommon/html/T_Rhino_Geometry_NurbsCurve.htm
    * https://en.wikipedia.org/wiki/Non-uniform_rational_B-spline
    * https://developer.rhino3d.com/guides/opennurbs/nurbs-geometry-overview/

    """

    # ==============================================================================
    # Data
    # ==============================================================================

    @property
    def __data__(self):
        # add superfluous knots
        # for compatibility with all/most other NURBS implementations
        # https://developer.rhino3d.com/guides/opennurbs/superfluous-knots/
        multiplicities = self.multiplicities[:]  # type: ignore
        multiplicities[0] += 1
        multiplicities[-1] += 1
        return {
            "points": [point.__data__ for point in self.points],  # type: ignore
            "weights": self.weights,
            "knots": self.knots,
            "multiplicities": multiplicities,
            "degree": self.degree,
            "is_periodic": self.is_periodic,
        }

    @classmethod
    def __from_data__(cls, data):
        points = [Point.__from_data__(point) for point in data["points"]]
        weights = data["weights"]
        knots = data["knots"]
        multiplicities = data["multiplicities"]
        degree = data["degree"]
        # is_periodic = data['is_periodic']
        # have not found a way to actually set this
        # not sure if that is actually possible...
        native_curve = native_curve_from_parameters(points, weights, knots, multiplicities, degree)
        return cls.from_native(native_curve)

    # ==============================================================================
    # Rhino Properties
    # ==============================================================================

    # ==============================================================================
    # Properties
    # ==============================================================================

    @property
    def points(self):
        if self.native_curve:
            return [point_to_compas(point.Location) for point in self.native_curve.Points]

    @property
    def weights(self):
        if self.native_curve:
            return [point.Weight for point in self.native_curve.Points]

    @property
    def knots(self):
        if self.native_curve:
            return [key for key, _ in groupby(self.native_curve.Knots)]

    @property
    def knotsequence(self):
        if self.native_curve:
            return list(self.native_curve.Knots)

    @property
    def multiplicities(self):
        if self.native_curve:
            return [len(list(group)) for _, group in groupby(self.native_curve.Knots)]

    @property
    def degree(self):
        if self.native_curve:
            return self.native_curve.Degree

    @property
    def order(self):
        if self.native_curve:
            return self.native_curve.Order

    @property
    def is_rational(self):
        if self.native_curve:
            return self.native_curve.IsRational

    # ==============================================================================
    # Constructors
    # ==============================================================================

    @classmethod
    def from_interpolation(cls, points, precision=1e-3):
        """Construct a NURBS curve by interpolating a set of points.

        Parameters
        ----------
        points : list[:class:`compas.geometry.Point`]
            The control points.
        precision : float, optional
            The required precision of the interpolation.
            This parameter is currently not supported.

        Returns
        -------
        :class:`compas_rhino.geometry.RhinoNurbsCurve`

        """
        native_curve = Rhino.Geometry.NurbsCurve.CreateHSpline([point_to_rhino(point) for point in points])
        return cls.from_native(native_curve)

    @classmethod
    def from_native(cls, native_curve):
        """Construct a NURBS curve from an existing Rhino curve.

        Parameters
        ----------
        native_curve : Rhino.Geometry.Curve

        Returns
        -------
        :class:`compas_rhino.geometry.RhinoNurbsCurve`

        """
        return cls(native_curve)

    @classmethod
    def from_parameters(cls, points, weights, knots, multiplicities, degree, is_periodic=False):
        """Construct a NURBS curve from explicit curve parameters.

        Parameters
        ----------
        points : list[:class:`compas.geometry.Point`]
            The control points.
        weights : list[float]
            The control point weights.
        knots : list[float]
            The curve knots, without duplicates.
        multiplicities : list[int]
            The multiplicities of the knots.
        degree : int
            The degree of the curve.
        is_periodic : bool, optional
            Flag indicating whether the curve is periodic or not.
            Note that this parameters is currently not supported.

        Returns
        -------
        :class:`compas_rhino.geometry.RhinoNurbsCurve`

        """
        degree = min(degree, len(points) - 1)
        native_curve = native_curve_from_parameters(points, weights, knots, multiplicities, degree)
        return cls.from_native(native_curve)

    @classmethod
    def from_points(cls, points, degree=3, is_periodic=False):
        """Construct a NURBS curve from control points.

        Parameters
        ----------
        points : list[:class:`compas.geometry.Point`]
            The control points.
        degree : int, optional
            The degree of the curve.
        is_periodic : bool, optional
            Flag indicating whether the curve is periodic or not.

        Returns
        -------
        :class:`compas_rhino.geometry.RhinoNurbsCurve`

        """
        degree = min(degree, len(points) - 1)
        native_curve = Rhino.Geometry.NurbsCurve.Create(is_periodic, degree, [point_to_rhino(point) for point in points])
        return cls.from_native(native_curve)

    # ==============================================================================
    # Conversions
    # ==============================================================================

    # ==============================================================================
    # Methods
    # ==============================================================================
