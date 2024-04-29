from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from itertools import groupby

import Rhino.Geometry  # type: ignore

from compas.geometry import NurbsSurface
from compas.geometry import Point
from compas.geometry import knots_and_mults_to_knotvector
from compas.itertools import flatten
from compas_rhino.conversions import point_to_compas
from compas_rhino.conversions import point_to_rhino

from .surface import RhinoSurface


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
    knots_u,
    knots_v,
    mults_u,
    mults_v,
    degree_u,
    degree_v,
    is_periodic_u=False,
    is_periodic_v=False,
):
    order_u = degree_u + 1
    order_v = degree_v + 1
    pointcount_u = len(points)
    pointcount_v = len(points[0])
    is_rational = any(weight != 1.0 for weight in flatten(weights))
    dimensions = 3

    rhino_surface = Rhino.Geometry.NurbsSurface.Create(
        dimensions,
        is_rational,
        order_u,
        order_v,
        pointcount_u,
        pointcount_v,
    )

    if not rhino_surface:
        message = "dimensions: {} is_rational: {} order_u: {} order_v: {} u_points: {} v_points: {}".format(
            dimensions,
            is_rational,
            order_u,
            order_v,
            pointcount_u,
            pointcount_v,
        )
        raise ValueError("Failed to create NurbsSurface with params:\n{}".format(message))

    knotvector_u = knots_and_mults_to_knotvector(knots_u, mults_u)
    knotvector_v = knots_and_mults_to_knotvector(knots_v, mults_v)
    # account for superfluous knots
    # https://developer.rhino3d.com/guides/opennurbs/superfluous-knots/
    if len(knotvector_u) == pointcount_u + order_u:
        knotvector_u[:] = knotvector_u[1:-1]
    if len(knotvector_v) == pointcount_v + order_v:
        knotvector_v[:] = knotvector_v[1:-1]
    # add knots
    for index, knot in enumerate(knotvector_u):
        rhino_surface.KnotsU[index] = knot
    for index, knot in enumerate(knotvector_v):
        rhino_surface.KnotsV[index] = knot
    # add control points
    for i in range(pointcount_u):
        for j in range(pointcount_v):
            rhino_surface.Points.SetPoint(i, j, point_to_rhino(points[i][j]), weights[i][j])
    return rhino_surface


class RhinoNurbsSurface(RhinoSurface, NurbsSurface):
    """Class representing a NURBS surface.

    Attributes
    ----------
    points: list[list[:class:`compas.geometry.Point`]]
        The control points of the surface.
    weights: list[list[float]]
        The weights of the control points.
    knots_u: list[float]
        The knot vector, in the U direction, without duplicates.
    knots_v: list[float]
        The knot vector, in the V direction, without duplicates.
    mults_u: list[int]
        The multiplicities of the knots in the knot vector of the U direction.
    mults_v: list[int]
        The multiplicities of the knots in the knot vector of the V direction.
    degree_u: int
        The degree of the polynomials in the U direction.
    degree_v: int
        The degree of the polynomials in the V direction.

    """

    def __init__(self, name=None):
        super(RhinoNurbsSurface, self).__init__(name=name)
        self._points = None

    # ==============================================================================
    # Data
    # ==============================================================================

    @property
    def __data__(self):
        # add superfluous knots
        # for compatibility with all/most other NURBS implementations
        # https://developer.rhino3d.com/guides/opennurbs/superfluous-knots/
        mults_u = self.mults_u[:]  # type: ignore
        mults_v = self.mults_v[:]  # type: ignore
        mults_u[0] += 1
        mults_u[-1] += 1
        mults_v[0] += 1
        mults_v[-1] += 1
        return {
            "points": [[point.__data__ for point in row] for row in self.points],  # type: ignore
            "weights": self.weights,
            "knots_u": self.knots_u,
            "knots_v": self.knots_v,
            "mults_u": mults_u,
            "mults_v": mults_v,
            "degree_u": self.degree_u,
            "degree_v": self.degree_v,
            "is_periodic_u": self.is_periodic_u,
            "is_periodic_v": self.is_periodic_v,
        }

    @classmethod
    def __from_data__(cls, data):
        """Construct a BSpline surface from its data representation.

        Parameters
        ----------
        data : dict
            The data dictionary.

        Returns
        -------
        :class:`compas_rhino.geometry.RhinoNurbsSurface`
            The constructed surface.

        """
        points = [[Point.__from_data__(point) for point in row] for row in data["points"]]
        weights = data["weights"]
        knots_u = data["knots_u"]
        knots_v = data["knots_v"]
        mults_u = data["mults_u"]
        mults_v = data["mults_v"]
        degree_u = data["degree_u"]
        degree_v = data["degree_v"]
        is_periodic_u = data["is_periodic_u"]
        is_periodic_v = data["is_periodic_v"]
        return cls.from_parameters(
            points,
            weights,
            knots_u,
            knots_v,
            mults_u,
            mults_v,
            degree_u,
            degree_v,
            is_periodic_u,
            is_periodic_v,
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
    def knots_u(self):
        if self.rhino_surface:
            return [key for key, _ in groupby(self.rhino_surface.KnotsU)]

    @property
    def mults_u(self):
        if self.rhino_surface:
            return [len(list(group)) for _, group in groupby(self.rhino_surface.KnotsU)]

    @property
    def knotvector_u(self):
        if self.rhino_surface:
            return list(self.rhino_surface.KnotsU)

    @property
    def knots_v(self):
        if self.rhino_surface:
            return [key for key, _ in groupby(self.rhino_surface.KnotsV)]

    @property
    def mults_v(self):
        if self.rhino_surface:
            return [len(list(group)) for _, group in groupby(self.rhino_surface.KnotsV)]

    @property
    def knotvector_v(self):
        if self.rhino_surface:
            return list(self.rhino_surface.KnotsV)

    @property
    def degree_u(self):
        if self.rhino_surface:
            return self.rhino_surface.Degree(0)

    @property
    def degree_v(self):
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
        knots_u,
        knots_v,
        mults_u,
        mults_v,
        degree_u,
        degree_v,
        is_periodic_u=False,
        is_periodic_v=False,
    ):
        """Construct a NURBS surface from explicit parameters.

        Parameters
        ----------
        points : list[list[:class:`compas.geometry.Point`]]
            The control points.
        weights : list[list[float]]
            The weights of the control points.
        knots_u : list[float]
            The knots in the U direction, without multiplicity.
        knots_v : list[float]
            The knots in the V direction, without multiplicity.
        mults_u : list[int]
            Multiplicity of the knots in the U direction.
        mults_v : list[int]
            Multiplicity of the knots in the V direction.
        degree_u : int
            Degree in the U direction.
        degree_v : int
            Degree in the V direction.

        Returns
        -------
        :class:`compas_rhino.geometry.RhinoNurbsSurface`

        """
        surface = cls()
        surface.rhino_surface = rhino_surface_from_parameters(points, weights, knots_u, knots_v, mults_u, mults_v, degree_u, degree_v)
        return surface

    @classmethod
    def from_points(cls, points, degree_u=3, degree_v=3):
        """Construct a NURBS surface from control points.

        Parameters
        ----------
        points : list[list[:class:`compas.geometry.Point`]]
            The control points.
        degree_u : int
            Degree in the U direction.
        degree_v : int
            Degree in the V direction.

        Returns
        -------
        :class:`compas_rhino.geometry.RhinoNurbsSurface`

        """
        # this of course depends on the order in which the points are given.
        # with the current convention this should not be needed.
        points = list(zip(*points))

        pointcount_u = len(points)
        pointcount_v = len(points[0])
        points[:] = [point_to_rhino(point) for row in points for point in row]
        surface = cls()
        surface.rhino_surface = Rhino.Geometry.NurbsSurface.CreateFromPoints(points, pointcount_u, pointcount_v, degree_u, degree_v)
        return surface

    @classmethod
    def from_fill(cls, curve1, curve2):
        """Construct a NURBS surface from the infill between two NURBS curves.

        Parameters
        ----------
        curve1 : :class:`compas.geometry.NurbsCurve`
        curve2 : :class:`compas.geometry.NurbsCurve`

        Returns
        -------
        :class:`compas_rhino.geometry.RhinoNurbsSurface`

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
