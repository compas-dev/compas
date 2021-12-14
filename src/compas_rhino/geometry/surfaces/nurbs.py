from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from itertools import groupby

from compas.geometry import Point
from compas.geometry import NurbsSurface

from compas_rhino.conversions import point_to_rhino
from compas_rhino.conversions import point_to_compas
from compas_rhino.conversions import vector_to_compas
from compas_rhino.conversions import plane_to_compas_frame
from compas_rhino.conversions import box_to_compas
from compas_rhino.conversions import RhinoCurve

import Rhino.Geometry


def rhino_surface_from_parameters(points, weights, u_knots, v_knots, u_mults, v_mults, u_degree, v_degree, is_u_periodic=False, is_v_periodic=False):
    rhino_surface = Rhino.Geometry.NurbsSurface.Create(
        3,
        True,
        u_degree + 1,
        v_degree + 1,
        len(points[0]),
        len(points)
    )
    u_knotvector = [knot for knot, mult in zip(u_knots, u_mults) for _ in range(mult)]
    v_knotvector = [knot for knot, mult in zip(v_knots, v_mults) for _ in range(mult)]
    u_count = len(points[0])
    v_count = len(points)
    u_order = u_degree + 1
    v_order = v_degree + 1
    # account for superfluous knots
    # https://developer.rhino3d.com/guides/opennurbs/superfluous-knots/
    if len(u_knotvector) == u_count + u_order:
        u_knotvector[:] = u_knotvector[1:-1]
    if len(v_knotvector) == v_count + v_order:
        v_knotvector[:] = v_knotvector[1:-1]
    # add knots
    for index, knot in enumerate(u_knotvector):
        rhino_surface.KnotsU[index] = knot
    for index, knot in enumerate(v_knotvector):
        rhino_surface.KnotsV[index] = knot
    # add control points
    for i in range(v_count):
        for j in range(u_count):
            rhino_surface.Points.SetPoint(i, j, point_to_rhino(points[i][j]), weights[i][j])
    return rhino_surface


class RhinoNurbsSurface(NurbsSurface):
    """Class representing a NURBS surface.

    Attributes
    ----------
    points: List[List[Point]]
        The control points of the surface.
    weights: List[List[float]]
        The weights of the control points.
    u_knots: List[float]
        The knot vector, in the U direction, without duplicates.
    v_knots: List[float]
        The knot vector, in the V direction, without duplicates.
    u_mults: List[int]
        The multiplicities of the knots in the knot vector of the U direction.
    v_mults: List[int]
        The multiplicities of the knots in the knot vector of the V direction.
    u_degree: int
        The degree of the polynomials in the U direction.
    v_degree: int
        The degree of the polynomials in the V direction.
    u_domain: Tuple[float, float]
        The parameter domain in the U direction.
    v_domain: Tuple[float, float]
        The parameter domain in the V direction.
    is_u_periodic: bool
        True if the surface is periodic in the U direction.
    is_v_periodic: bool
        True if the surface is periodic in the V direction.
    """

    def __init__(self, name=None):
        super(RhinoNurbsSurface, self).__init__(name=name)
        self.rhino_surface = None

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
            'points': [[point.data for point in row] for row in self.points],
            'weights': self.weights,
            'u_knots': self.u_knots,
            'v_knots': self.v_knots,
            'u_mults': u_mults,
            'v_mults': v_mults,
            'u_degree': self.u_degree,
            'v_degree': self.v_degree,
            'is_u_periodic': self.is_u_periodic,
            'is_v_periodic': self.is_v_periodic
        }

    @data.setter
    def data(self, data):
        points = [[Point.from_data(point) for point in row] for row in data['points']]
        weights = data['weights']
        u_knots = data['u_knots']
        v_knots = data['v_knots']
        u_mults = data['u_mults']
        v_mults = data['v_mults']
        u_degree = data['u_degree']
        v_degree = data['v_degree']
        is_u_periodic = data['is_u_periodic']
        is_v_periodic = data['is_v_periodic']
        self.rhino_surface = NurbsSurface.from_parameters(
            points, weights, u_knots, v_knots, u_mults, v_mults, u_degree, v_degree, is_u_periodic, is_v_periodic
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
        :class:`compas.geometry.NurbsSurface`
            The constructed surface.

        """
        points = [[Point.from_data(point) for point in row] for row in data['points']]
        weights = data['weights']
        u_knots = data['u_knots']
        v_knots = data['v_knots']
        u_mults = data['u_mults']
        v_mults = data['v_mults']
        u_degree = data['u_degree']
        v_degree = data['v_degree']
        is_u_periodic = data['is_u_periodic']
        is_v_periodic = data['is_v_periodic']
        return cls.from_parameters(
            points, weights, u_knots, v_knots, u_mults, v_mults, u_degree, v_degree, is_u_periodic, is_v_periodic
        )

    # ==============================================================================
    # Constructors
    # ==============================================================================

    @classmethod
    def from_rhino(cls, rhino_surface):
        """Construct a NURBS surface from an existing Rhino surface.

        Parameters
        ----------
        rhino_surface : Rhino.Geometry.NurbsSurface

        Returns
        -------
        :class:`compas_rhino.geometry.RhinoNurbsSurface`

        """
        curve = cls()
        curve.rhino_surface = rhino_surface
        return curve

    @classmethod
    def from_parameters(cls, points, weights, u_knots, v_knots, u_mults, v_mults, u_degree, v_degree, is_u_periodic=False, is_v_periodic=False):
        """Construct a NURBS surface from explicit parameters.

        Parameters
        ----------
        points : List[List[:class:`compas.geometry.Point`]]
            The control points.
        weights : List[List[float]]
            The weights of the control points.
        u_knots : List[float]
            The knots in the U direction, without multiplicity.
        v_knots : List[float]
            The knots in the V direction, without multiplicity.
        u_mults : List[int]
            Multiplicity of the knots in the U direction.
        v_mults : List[int]
            Multiplicity of the knots in the V direction.
        u_degree : int
            Degree in the U direction.
        v_degree : int
            Degree in the V direction.

        Returns
        -------
        :class:`compas.geometry.NurbsSurface`
        """
        surface = cls()
        surface.rhino_surface = rhino_surface_from_parameters(points, weights, u_knots, v_knots, u_mults, v_mults, u_degree, v_degree)
        return surface

    @classmethod
    def from_points(cls, points, u_degree=3, v_degree=3):
        """Construct a NURBS surface from control points.

        Parameters
        ----------
        points : List[List[:class:`compas.geometry.Point`]]
            The control points.
        u_degree : int
            Degree in the U direction.
        v_degree : int
            Degree in the V direction.

        Returns
        -------
        :class:`compas.geometry.NurbsSurface`
        """
        points = list(zip(*points))
        u_count = len(points[0])
        v_count = len(points)
        points[:] = [point_to_rhino(point) for row in points for point in row]
        surface = cls()
        surface.rhino_surface = Rhino.Geometry.NurbsSurface.CreateFromPoints(points, v_count, u_count, u_degree, v_degree)
        return surface

    @classmethod
    def from_step(cls, filepath):
        """Load a NURBS surface from a STP file.

        Parameters
        ----------
        filepath : str

        Returns
        -------
        :class:`compas.geometry.NurbsSurface`
        """
        raise NotImplementedError

    @classmethod
    def from_fill(cls, curve1, curve2):
        """Construct a NURBS surface from the infill between two NURBS curves.

        Parameters
        ----------
        curve1 : :class:`compas.geometry.NurbsCurve`
        curve2 : :class:`compas.geometry.NurbsCurve`

        Returns
        -------
        :class:`compas.geometry.NurbsSurface`
        """
        surface = cls()
        # these curves probably need to be processed first
        surface.rhino_surface = Rhino.Geometry.NurbsSurface.CreateRuledSurface(curve1, curve2)
        return surface

    # ==============================================================================
    # Conversions
    # ==============================================================================

    def to_step(self, filepath, schema="AP203"):
        """Write the surface geometry to a STP file."""
        raise NotImplementedError

    # ==============================================================================
    # Properties
    # ==============================================================================

    @property
    def points(self):
        if self.rhino_surface:
            points = []
            for i in range(self.rhino_surface.Points.CountU):
                row = []
                for j in range(self.rhino_surface.Points.CountV):
                    row.append(point_to_compas(self.rhino_surface.Points.GetControlPoint(i, j).Location))
                points.append(row)
            return points

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

    @property
    def u_domain(self):
        if self.rhino_surface:
            return self.rhino_surface.Domain(0)

    @property
    def v_domain(self):
        if self.rhino_surface:
            return self.rhino_surface.Domain(1)

    @property
    def is_u_periodic(self):
        if self.rhino_surface:
            return self.rhino_surface.IsPeriodic(0)

    @property
    def is_v_periodic(self):
        if self.rhino_surface:
            return self.rhino_surface.IsPeriodic(1)

    # ==============================================================================
    # Methods
    # ==============================================================================

    def u_isocurve(self, u):
        """Compute the isoparametric curve at parameter u.

        Parameters
        ----------
        u : float

        Returns
        -------
        :class:`compas.geometry.NurbsCurve`
        """
        curve = self.rhino_surface.IsoCurve(1, u)
        return RhinoCurve.from_geometry(curve).to_compas()

    def v_isocurve(self, v):
        """Compute the isoparametric curve at parameter v.

        Parameters
        ----------
        v : float

        Returns
        -------
        :class:`compas.geometry.NurbsCurve`
        """
        curve = self.rhino_surface.IsoCurve(0, v)
        return RhinoCurve.from_geometry(curve).to_compas()

    def boundary(self):
        """Compute the boundary curves of the surface.

        Returns
        -------
        List[:class:`compas.geometry.NurbsCurve`]
        """
        raise NotImplementedError

    def point_at(self, u, v):
        """Compute a point on the surface.

        Parameters
        ----------
        u : float
        v : float

        Returns
        -------
        :class:`compas.geometry.Point`
        """
        point = self.rhino_surface.PointAt(u, v)
        return point_to_compas(point)

    def curvature_at(self, u, v):
        """Compute the curvature at a point on the surface.

        Parameters
        ----------
        u : float
        v : float

        Returns
        -------
        :class:`compas.geometry.Vector`
        """
        vector = self.rhino_surface.CurvatureAt(u, v)
        return vector_to_compas(vector)

    def frame_at(self, u, v):
        """Compute the local frame at a point on the curve.

        Parameters
        ----------
        u : float
        v : float

        Returns
        -------
        :class:`compas.geometry.Frame`
        """
        result, plane = self.rhino_surface.FrameAt(u, v)
        if result:
            return plane_to_compas_frame(plane)

    def closest_point(self, point, return_parameters=False):
        """Compute the closest point on the curve to a given point.

        Parameters
        ----------
        point : :class:`compas.geometry.Point`
            The test point.
        return_parameters : bool, optional
            Return the UV parameters of the closest point in addition to the point location.

        Returns
        -------
        :class:`compas.geometry.Point`
            If ``return_parameters`` is False.
        :class:`compas.geometry.Point`, float, float
            If ``return_parameters`` is True.
        """
        result, u, v = self.rhino_curve.ClosestPoint(point_to_rhino(point))
        if not result:
            return
        point = self.point_at(u, v)
        if return_parameters:
            return point, u, v
        return point

    def aabb(self, precision=0.0, optimal=False):
        """Compute the axis aligned bounding box of the surface.

        Parameters
        ----------
        precision : float, optional
        optimal : float, optional
            Flag indicating that the box should be precise.

        Returns
        -------
        :class:`compas.geometry.Box`
        """
        box = self.rhino_surface.GetBoundingBox(optimal)
        return box_to_compas(box)
