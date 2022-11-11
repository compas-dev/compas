from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from itertools import groupby

from compas.geometry import Point
from compas.geometry import NurbsSurface

from compas_rhino.conversions import point_to_rhino
from compas_rhino.conversions import point_to_compas

from .surface import RhinoSurface

import Rhino.Geometry


class ControlPoints(object):
    def __init__(self, surface):
        self.rhino_surface = surface

    @property
    def points(self):
        points = []
        for i in range(self.rhino_surface.Points.CountU):
            row = []
            for j in range(self.rhino_surface.Points.CountV):
                row.append(point_to_compas(self.rhino_surface.Points.GetControlPoint(i, j).Location))
            points.append(row)
        return points

    def __getitem__(self, index):
        try:
            u, v = index
        except TypeError:
            return self.points[index]
        else:
            point = self.rhino_surface.Points.GetControlPoint(u, v).Location
            return point_to_compas(point)

    def __setitem__(self, index, point):
        u, v = index
        self.rhino_surface.Points.SetControlPoint(u, v, Rhino.Geometry.ControlPoint(point_to_rhino(point)))

    def __len__(self):
        return self.rhino_surface.Points.CountU

    def __iter__(self):
        return iter(self.points)


def rhino_surface_from_parameters(
    points,
    weights,
    u_knots,
    v_knots,
    u_mults,
    v_mults,
    u_degree,
    v_degree,
    is_u_periodic=False,
    is_v_periodic=False,
):
    u_order = u_degree + 1
    v_order = v_degree + 1
    u_point_count = len(points)
    v_point_count = len(points[0])
    is_rational = True  # TODO: check if all weights are equal? https://developer.rhino3d.com/guides/opennurbs/nurbs-geometry-overview/
    dimensions = 3
    rhino_surface = Rhino.Geometry.NurbsSurface.Create(
        dimensions, is_rational, u_order, v_order, u_point_count, v_point_count
    )

    if not rhino_surface:
        message = "dimensions: {} is_rational: {} u_order: {} v_order: {} u_points: {} v_points: {}".format(
            dimensions, is_rational, u_order, v_order, u_point_count, v_point_count
        )
        raise ValueError("Failed to create NurbsSurface with params:\n{}".format(message))

    u_knotvector = [knot for knot, mult in zip(u_knots, u_mults) for _ in range(mult)]
    v_knotvector = [knot for knot, mult in zip(v_knots, v_mults) for _ in range(mult)]
    # account for superfluous knots
    # https://developer.rhino3d.com/guides/opennurbs/superfluous-knots/
    if len(u_knotvector) == u_point_count + u_order:
        u_knotvector[:] = u_knotvector[1:-1]
    if len(v_knotvector) == v_point_count + v_order:
        v_knotvector[:] = v_knotvector[1:-1]
    # add knots
    for index, knot in enumerate(u_knotvector):
        rhino_surface.KnotsU[index] = knot
    for index, knot in enumerate(v_knotvector):
        rhino_surface.KnotsV[index] = knot
    # add control points
    for i in range(u_point_count):
        for j in range(v_point_count):
            rhino_surface.Points.SetPoint(i, j, point_to_rhino(points[i][j]), weights[i][j])
    return rhino_surface


class RhinoNurbsSurface(RhinoSurface, NurbsSurface):
    """Class representing a NURBS surface.

    Attributes
    ----------
    points: list[list[:class:`~compas.geometry.Point`]]
        The control points of the surface.
    weights: list[list[float]]
        The weights of the control points.
    u_knots: list[float]
        The knot vector, in the U direction, without duplicates.
    v_knots: list[float]
        The knot vector, in the V direction, without duplicates.
    u_mults: list[int]
        The multiplicities of the knots in the knot vector of the U direction.
    v_mults: list[int]
        The multiplicities of the knots in the knot vector of the V direction.
    u_degree: int
        The degree of the polynomials in the U direction.
    v_degree: int
        The degree of the polynomials in the V direction.

    """

    def __init__(self, name=None):
        super(RhinoNurbsSurface, self).__init__(name=name)
        self._points = None

    # ==============================================================================
    # Data
    # ==============================================================================

    @property
    def data(self):
        # add superfluous knots
        # for compatibility with all/most other NURBS implementations
        # https://developer.rhino3d.com/guides/opennurbs/superfluous-knots/
        u_mults = self.u_mults[:]
        v_mults = self.v_mults[:]
        u_mults[0] += 1
        u_mults[-1] += 1
        v_mults[0] += 1
        v_mults[-1] += 1
        return {
            "points": [[point.data for point in row] for row in self.points],
            "weights": self.weights,
            "u_knots": self.u_knots,
            "v_knots": self.v_knots,
            "u_mults": u_mults,
            "v_mults": v_mults,
            "u_degree": self.u_degree,
            "v_degree": self.v_degree,
            "is_u_periodic": self.is_u_periodic,
            "is_v_periodic": self.is_v_periodic,
        }

    @data.setter
    def data(self, data):
        points = [[Point.from_data(point) for point in row] for row in data["points"]]
        weights = data["weights"]
        u_knots = data["u_knots"]
        v_knots = data["v_knots"]
        u_mults = data["u_mults"]
        v_mults = data["v_mults"]
        u_degree = data["u_degree"]
        v_degree = data["v_degree"]
        is_u_periodic = data["is_u_periodic"]
        is_v_periodic = data["is_v_periodic"]
        self.rhino_surface = NurbsSurface.from_parameters(
            points,
            weights,
            u_knots,
            v_knots,
            u_mults,
            v_mults,
            u_degree,
            v_degree,
            is_u_periodic,
            is_v_periodic,
        )

    @classmethod
    def from_data(cls, data):
        """Construct a BSpline surface from its data representation.

        Parameters
        ----------
        data : dict
            The data dictionary.

        Returns
        -------
        :class:`~compas_rhino.geometry.RhinoNurbsSurface`
            The constructed surface.

        """
        points = [[Point.from_data(point) for point in row] for row in data["points"]]
        weights = data["weights"]
        u_knots = data["u_knots"]
        v_knots = data["v_knots"]
        u_mults = data["u_mults"]
        v_mults = data["v_mults"]
        u_degree = data["u_degree"]
        v_degree = data["v_degree"]
        is_u_periodic = data["is_u_periodic"]
        is_v_periodic = data["is_v_periodic"]
        return cls.from_parameters(
            points,
            weights,
            u_knots,
            v_knots,
            u_mults,
            v_mults,
            u_degree,
            v_degree,
            is_u_periodic,
            is_v_periodic,
        )

    # ==============================================================================
    # Properties
    # ==============================================================================

    @property
    def points(self):
        if self.rhino_surface:
            if not self._points:
                self._points = ControlPoints(self.rhino_surface)
            return self._points

    @property
    def weights(self):
        if self.rhino_surface:
            weights = []
            for i in range(self.rhino_surface.Points.CountU):
                row = []
                for j in range(self.rhino_surface.Points.CountV):
                    row.append(self.rhino_surface.Points.GetWeight(i, j))
                weights.append(row)
            return weights

    @property
    def u_knots(self):
        if self.rhino_surface:
            return [key for key, _ in groupby(self.rhino_surface.KnotsU)]

    @property
    def u_knotsequence(self):
        if self.rhino_surface:
            return list(self.rhino_surface.KnotsU)

    @property
    def v_knots(self):
        if self.rhino_surface:
            return [key for key, _ in groupby(self.rhino_surface.KnotsV)]

    @property
    def v_knotsequence(self):
        if self.rhino_surface:
            return list(self.rhino_surface.KnotsV)

    @property
    def u_mults(self):
        if self.rhino_surface:
            return [len(list(group)) for _, group in groupby(self.rhino_surface.KnotsU)]

    @property
    def v_mults(self):
        if self.rhino_surface:
            return [len(list(group)) for _, group in groupby(self.rhino_surface.KnotsV)]

    @property
    def u_degree(self):
        if self.rhino_surface:
            return self.rhino_surface.Degree(0)

    @property
    def v_degree(self):
        if self.rhino_surface:
            return self.rhino_surface.Degree(1)

    # ==============================================================================
    # Constructors
    # ==============================================================================

    @classmethod
    def from_parameters(
        cls,
        points,
        weights,
        u_knots,
        v_knots,
        u_mults,
        v_mults,
        u_degree,
        v_degree,
        is_u_periodic=False,
        is_v_periodic=False,
    ):
        """Construct a NURBS surface from explicit parameters.

        Parameters
        ----------
        points : list[list[:class:`~compas.geometry.Point`]]
            The control points.
        weights : list[list[float]]
            The weights of the control points.
        u_knots : list[float]
            The knots in the U direction, without multiplicity.
        v_knots : list[float]
            The knots in the V direction, without multiplicity.
        u_mults : list[int]
            Multiplicity of the knots in the U direction.
        v_mults : list[int]
            Multiplicity of the knots in the V direction.
        u_degree : int
            Degree in the U direction.
        v_degree : int
            Degree in the V direction.

        Returns
        -------
        :class:`~compas_rhino.geometry.RhinoNurbsSurface`

        """
        surface = cls()
        surface.rhino_surface = rhino_surface_from_parameters(
            points, weights, u_knots, v_knots, u_mults, v_mults, u_degree, v_degree
        )
        return surface

    @classmethod
    def from_points(cls, points, u_degree=3, v_degree=3):
        """Construct a NURBS surface from control points.

        Parameters
        ----------
        points : list[list[:class:`~compas.geometry.Point`]]
            The control points.
        u_degree : int
            Degree in the U direction.
        v_degree : int
            Degree in the V direction.

        Returns
        -------
        :class:`~compas_rhino.geometry.RhinoNurbsSurface`

        """
        points = list(zip(*points))
        u_count = len(points[0])
        v_count = len(points)
        points[:] = [point_to_rhino(point) for row in points for point in row]
        surface = cls()
        surface.rhino_surface = Rhino.Geometry.NurbsSurface.CreateFromPoints(
            points, v_count, u_count, u_degree, v_degree
        )
        return surface

    @classmethod
    def from_fill(cls, curve1, curve2):
        """Construct a NURBS surface from the infill between two NURBS curves.

        Parameters
        ----------
        curve1 : :class:`~compas.geometry.NurbsCurve`
        curve2 : :class:`~compas.geometry.NurbsCurve`

        Returns
        -------
        :class:`~compas_rhino.geometry.RhinoNurbsSurface`

        """
        surface = cls()
        # these curves probably need to be processed first
        surface.rhino_surface = Rhino.Geometry.NurbsSurface.CreateRuledSurface(curve1, curve2)
        return surface

    # ==============================================================================
    # Conversions
    # ==============================================================================

    # ==============================================================================
    # Methods
    # ==============================================================================
