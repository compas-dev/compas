import bpy  # type: ignore

# from itertools import groupby
# from compas.geometry import Point
from compas.geometry import NurbsCurve

# from compas_blender.conversions import point_to_blender
# from compas_blender.conversions import point_to_compas
# from compas_blender.conversions import line_to_blender

from compas.geometry import Point

from .curve import BlenderCurve


def native_curve_from_parameters(points, weights, knots, multiplicities, degree, is_periodic, name="NurbsCurve"):
    """Create a Blender NurbsCurve from explicit curve parameters.

    Parameters
    ----------
    points : list[:class:`~compas.geometry.Point`]
        The control points.
    weights : list[float]
        The control point weights.
    knots : list[float]
        The curve knots, without duplicates.
    multiplicities : list[int]
        The multiplicities of the knots.
    degree : int
        The degree of the curve.
    name : str, optional
        Name of the curve.

    Returns
    -------
    :class:`bpy.types.Curve`
        A Blender NurbsCurve.

    Notes
    -----
    This will construct a Blender curve with one spline segment and the spline segment is defined as a NURBS curve.
    In Blender, you cannot edit the knot vectors directly, but you can influence them through the Endpoint and Bézier options.
    Note that, the Endpoint and Bézier settings only apply to open NURBS curves.

    """
    curve = bpy.data.curves.new(name=name, type="CURVE")
    curve.dimensions = "3D"

    spline = curve.splines.new("NURBS")
    spline.points.add(len(points) - 1)

    for i, (point, weight) in enumerate(zip(points, weights)):
        spline.points[i].co = [point[0], point[1], point[2], weight]
        spline.points[i].weight = weight

    spline.order_u = degree + 1
    spline.use_cyclic_u = is_periodic
    spline.use_endpoint_u = True
    spline.use_bezier_u = False

    return curve


class BlenderNurbsCurve(NurbsCurve, BlenderCurve):
    """Class representing a NURBS curve based on the NurbsCurve of Blender.Geometry.

    Parameters
    ----------
    name : str, optional
        Name of the curve.

    Attributes
    ----------
    points : list[:class:`~compas.geometry.Point`], read-only
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

    """

    def __init__(self, name=None):
        super(BlenderNurbsCurve, self).__init__(name=name)
        self.native_curve = None

    # ==============================================================================
    # Data
    # ==============================================================================

    # @property
    # def data(self):
    #     # add superfluous knots
    #     # for compatibility with all/most other NURBS implementations
    #     # https://developer.blender3d.com/guides/opennurbs/superfluous-knots/
    #     multiplicities = self.multiplicities[:]
    #     multiplicities[0] += 1
    #     multiplicities[-1] += 1
    #     return {
    #         "points": [point.data for point in self.points],
    #         "weights": self.weights,
    #         "knots": self.knots,
    #         "multiplicities": multiplicities,
    #         "degree": self.degree,
    #         "is_periodic": self.is_periodic,
    #     }

    # @data.setter
    # def data(self, data):
    #     points = [Point.from_data(point) for point in data["points"]]
    #     weights = data["weights"]
    #     knots = data["knots"]
    #     multiplicities = data["multiplicities"]
    #     degree = data["degree"]
    #     # is_periodic = data['is_periodic']
    #     # have not found a way to actually set this
    #     # not sure if that is actually possible...
    #     self.native_curve = native_curve_from_parameters(points, weights, knots, multiplicities, degree)

    # ==============================================================================
    # Blender Properties
    # ==============================================================================

    # ==============================================================================
    # Properties
    # ==============================================================================

    @property
    def points(self):
        if self.native_curve:
            return [Point(*point.co) for point in self.native_curve.splines[0].points]

    @property
    def weights(self):
        if self.native_curve:
            return [point.weight for point in self.native_curve.splines[0].points]

    # @property
    # def knots(self):
    #     pass

    # @property
    # def knotsequence(self):
    #     pass

    # @property
    # def multiplicities(self):
    #     pass

    @property
    def degree(self):
        if self.native_curve:
            return self.native_curve.order_u - 1

    @property
    def order(self):
        if self.native_curve:
            return self.native_curve.order_u

    # @property
    # def is_rational(self):
    #     pass

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
        :class:`~compas_blender.geometry.BlenderNurbsCurve`

        """
        curve = cls()
        curve.native_curve = native_curve_from_parameters(points, weights, None, None, degree, is_periodic)
        return curve

    @classmethod
    def from_points(cls, points, degree=3, is_periodic=False):
        """Construct a NURBS curve from control points.

        Parameters
        ----------
        points : list[:class:`~compas.geometry.Point`]
            The control points.
        degree : int, optional
            The degree of the curve.
        is_periodic : bool, optional
            Flag indicating whether the curve is periodic or not.

        Returns
        -------
        :class:`~compas_blender.geometry.BlenderNurbsCurve`

        """
        weights = [1.0 for point in points]
        knots = None
        multiplicities = None
        curve = cls()
        curve.native_curve = native_curve_from_parameters(points, weights, knots, multiplicities, degree, is_periodic)
        return curve

    # ==============================================================================
    # Conversions
    # ==============================================================================

    # ==============================================================================
    # Methods
    # ==============================================================================
