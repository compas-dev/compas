from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from itertools import groupby

import Rhino.Geometry  # type: ignore

from compas.geometry import NurbsSurface
from compas.geometry import knots_and_mults_to_knotvector
from compas.itertools import flatten
from compas_rhino.conversions import cylinder_to_rhino
from compas_rhino.conversions import frame_to_rhino_plane
from compas_rhino.conversions import plane_to_rhino
from compas_rhino.conversions import point_to_compas
from compas_rhino.conversions import point_to_rhino
from compas_rhino.conversions import sphere_to_rhino

from .surface import RhinoSurface


class ControlPoints(object):
    def __init__(self, surface):
        self.native_surface = surface

    @property
    def points(self):
        points = []
        for i in range(self.native_surface.Points.CountU):
            row = []
            for j in range(self.native_surface.Points.CountV):
                row.append(point_to_compas(self.native_surface.Points.GetControlPoint(i, j).Location))
            points.append(row)
        return points

    def __getitem__(self, index):
        try:
            u, v = index
        except TypeError:
            return self.points[index]
        else:
            point = self.native_surface.Points.GetControlPoint(u, v).Location
            return point_to_compas(point)

    def __setitem__(self, index, point):
        u, v = index
        self.native_surface.Points.SetControlPoint(u, v, Rhino.Geometry.ControlPoint(point_to_rhino(point)))

    def __len__(self):
        return self.native_surface.Points.CountU

    def __iter__(self):
        return iter(self.points)


def native_surface_from_parameters(
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

    native_surface = Rhino.Geometry.NurbsSurface.Create(
        dimensions,
        is_rational,
        order_u,
        order_v,
        pointcount_u,
        pointcount_v,
    )

    if not native_surface:
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
        native_surface.KnotsU[index] = knot
    for index, knot in enumerate(knotvector_v):
        native_surface.KnotsV[index] = knot
    # add control points
    for i in range(pointcount_u):
        for j in range(pointcount_v):
            native_surface.Points.SetPoint(i, j, point_to_rhino(points[i][j]), weights[i][j])
    return native_surface


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

    # ==============================================================================
    # Properties
    # ==============================================================================

    @property
    def points(self):
        if self.native_surface:
            if not hasattr(self, "_points"):
                self._points = ControlPoints(self.native_surface)
            return self._points

    @property
    def weights(self):
        if self.native_surface:
            weights = []
            for i in range(self.native_surface.Points.CountU):
                row = []
                for j in range(self.native_surface.Points.CountV):
                    row.append(self.native_surface.Points.GetWeight(i, j))
                weights.append(row)
            return weights

    @property
    def knots_u(self):
        if self.native_surface:
            return [key for key, _ in groupby(self.native_surface.KnotsU)]

    @property
    def mults_u(self):
        if self.native_surface:
            return [len(list(group)) for _, group in groupby(self.native_surface.KnotsU)]

    @property
    def knotvector_u(self):
        if self.native_surface:
            return list(self.native_surface.KnotsU)

    @property
    def knots_v(self):
        if self.native_surface:
            return [key for key, _ in groupby(self.native_surface.KnotsV)]

    @property
    def mults_v(self):
        if self.native_surface:
            return [len(list(group)) for _, group in groupby(self.native_surface.KnotsV)]

    @property
    def knotvector_v(self):
        if self.native_surface:
            return list(self.native_surface.KnotsV)

    @property
    def degree_u(self):
        if self.native_surface:
            return self.native_surface.Degree(0)

    @property
    def degree_v(self):
        if self.native_surface:
            return self.native_surface.Degree(1)

    # ==============================================================================
    # Constructors
    # ==============================================================================

    @classmethod
    def from_corners(cls, corners):
        """Creates a NURBS surface using the given 4 corners.

        The order of the given points determins the normal direction of the generated surface.

        Parameters
        ----------
        corners : list(:class:`compas.geometry.Point`)
            4 points in 3d space to represent the corners of the planar surface.

        Returns
        -------
        :class:`compas_rhino.geometry.RhinoNurbsSurface`

        """
        rhino_points = [Rhino.Geometry.Point3d(corner.x, corner.y, corner.z) for corner in corners]
        return cls.from_native(Rhino.Geometry.NurbsSurface.CreateFromCorners(*rhino_points))

    @classmethod
    def from_cylinder(cls, cylinder):
        """Create a NURBS surface from a cylinder.

        Parameters
        ----------
        cylinder : :class:`compas.geometry.Cylinder`
            The surface's geometry.

        Returns
        -------
        :class:`compas_rhino.geometry.RhinoNurbsSurface`

        """
        cylinder = cylinder_to_rhino(cylinder)
        surface = Rhino.Geometry.NurbsSurface.CreateFromCylinder(cylinder)
        return cls.from_native(surface)

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
        native_surface = Rhino.Geometry.NurbsSurface.CreateRuledSurface(curve1, curve2)
        return cls.from_native(native_surface)

    @classmethod
    def from_frame(cls, frame, domain_u=(0, 1), domain_v=(0, 1), degree_u=1, degree_v=1, pointcount_u=2, pointcount_v=2):
        """Creates a planar surface from a frame and parametric domain information.

        Parameters
        ----------
        frame : :class:`compas.geometry.Frame`
            A frame with point at the center of the wanted plannar surface and
            x and y axes the direction of u and v respectively.
        domain_u : tuple[int, int], optional
            The domain of the U parameter.
        domain_v : tuple[int, int], optional
            The domain of the V parameter.
        degree_u : int, optional
            Degree in the U direction.
        degree_v : int, optional
            Degree in the V direction.
        pointcount_u : int, optional
            Number of control points in the U direction.
        pointcount_v : int, optional
            Number of control points in the V direction.

        Returns
        -------
        :class:`compas_rhino.geometry.RhinoNurbsSurface`

        """
        plane = frame_to_rhino_plane(frame)
        du = Rhino.Geometry.Interval(*domain_u)
        dv = Rhino.Geometry.Interval(*domain_v)
        native_surface = Rhino.Geometry.NurbsSurface.CreateFromPlane(plane, du, dv, degree_u, degree_v, pointcount_u, pointcount_v)
        return cls.from_native(native_surface)

    @classmethod
    def from_native(cls, native_surface):
        """Construct a NURBS surface from an existing Rhino surface.

        Parameters
        ----------
        native_surface : :rhino:`Rhino.Geometry.Surface`
            A Rhino surface.

        Returns
        -------
        :class:`compas_rhino.geometry.RhinoNurbsSurface`

        """
        return cls(native_surface)

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
        native_surface = native_surface_from_parameters(points, weights, knots_u, knots_v, mults_u, mults_v, degree_u, degree_v)
        return cls.from_native(native_surface)

    @classmethod
    def from_plane(cls, plane, domain_u=(0, 1), domain_v=(0, 1), degree_u=1, degree_v=1, pointcount_u=2, pointcount_v=2):
        """Construct a surface from a plane.

        Parameters
        ----------
        plane : :class:`compas.geometry.Plane`
            The plane.
        domain_u : tuple[int, int], optional
            The domain of the U parameter.
        domain_v : tuple[int, int], optional
            The domain of the V parameter.
        degree_u : int, optional
            Degree in the U direction.
        degree_v : int, optional
            Degree in the V direction.
        pointcount_u : int, optional
            Number of control points in the U direction.
        pointcount_v : int, optional
            Number of control points in the V direction.

        Returns
        -------
        :class:`compas_rhino.geometry.RhinoNurbsSurface`

        """
        plane = plane_to_rhino(plane)
        du = Rhino.Geometry.Interval(*domain_u)
        dv = Rhino.Geometry.Interval(*domain_v)
        native_surface = Rhino.Geometry.NurbsSurface.CreateFromPlane(plane, du, dv, degree_u, degree_v, pointcount_u, pointcount_v)
        return cls.from_native(native_surface)

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
        native_surface = Rhino.Geometry.NurbsSurface.CreateFromPoints(points, pointcount_u, pointcount_v, degree_u, degree_v)
        return cls.from_native(native_surface)

    @classmethod
    def from_sphere(cls, sphere):
        """Creates a NURBS surface from a sphere.

        Parameters
        ----------
        sphere : :class:`compas.geometry.Sphere`
            The surface's geometry.

        Returns
        -------
        :class:`compas_rhino.geometry.RhinoNurbsSurface`

        """
        sphere = sphere_to_rhino(sphere)
        surface = Rhino.Geometry.NurbsSurface.CreateFromSphere(sphere)
        return cls.from_native(surface)

    @classmethod
    def from_torus(cls, torus):
        """Create a NURBS surface from a torus.

        Parameters
        ----------
        torus : :class:`compas.geometry.Torus`
            The surface's geometry.

        Returns
        -------
        :class:`compas_rhino.geometry.RhinoNurbsSurface`

        """
        raise NotImplementedError

    # ==============================================================================
    # Conversions
    # ==============================================================================

    # ==============================================================================
    # Methods
    # ==============================================================================
