from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import Rhino.Geometry  # type: ignore

from compas.geometry import Surface
from compas_rhino.conversions import box_to_compas
from compas_rhino.conversions import plane_to_compas_frame
from compas_rhino.conversions import point_to_compas
from compas_rhino.conversions import point_to_rhino
from compas_rhino.conversions import transformation_to_rhino
from compas_rhino.conversions import vector_to_compas
from compas_rhino.geometry.curves import RhinoCurve


class RhinoSurface(Surface):
    """Class representing a general surface object.

    Parameters
    ----------
    native_surface : :rhino:`Surface`
        A Rhino surface.
    name : str, optional
        The name of the surface.

    Attributes
    ----------
    domain_u: tuple[float, float]
        The parameter domain in the U direction.
    domain_v: tuple[float, float]
        The parameter domain in the V direction.
    is_periodic_u: bool
        True if the surface is periodic in the U direction.
    is_periodic_v: bool
        True if the surface is periodic in the V direction.

    """

    def __init__(self, native_surface, name=None):
        super(RhinoSurface, self).__init__(name=name)
        self._native_surface = native_surface

    @property
    def rhino_surface(self):
        return self._native_surface

    @property
    def native_surface(self):
        return self._native_surface

    @native_surface.setter
    def native_surface(self, surface):
        self._native_surface = surface

    # ==============================================================================
    # Properties
    # ==============================================================================

    @property
    def domain_u(self):
        if self.native_surface:
            return self.native_surface.Domain(0)

    @property
    def domain_v(self):
        if self.native_surface:
            return self.native_surface.Domain(1)

    @property
    def is_periodic_u(self):
        if self.native_surface:
            return self.native_surface.IsPeriodic(0)

    @property
    def is_periodic_v(self):
        if self.native_surface:
            return self.native_surface.IsPeriodic(1)

    # ==============================================================================
    # Constructors
    # ==============================================================================

    @classmethod
    def from_native(cls, native_surface):
        """Construct a surface from an existing Rhino surface.

        Parameters
        ----------
        native_surface : :rhino:`Rhino.Geometry.Surface`
            A Rhino surface.

        Returns
        -------
        :class:`compas_rhino.geometry.RhinoSurface`

        """
        return cls(native_surface)

    @classmethod
    def from_rhino(cls, native_surface):
        """Construct a surface from an existing Rhino surface.

        Parameters
        ----------
        native_surface : :rhino:`Rhino.Geometry.Surface`
            A Rhino surface.

        Returns
        -------
        :class:`compas_rhino.geometry.RhinoSurface`

        Warnings
        --------
        .. deprecated:: 2.3
            Use `from_native` instead.

        """
        return cls(native_surface)

    # ==============================================================================
    # Conversions
    # ==============================================================================

    # ==============================================================================
    # Methods
    # ==============================================================================

    def copy(self):
        """Make an independent copy of the current surface.

        Returns
        -------
        :class:`compas_rhino.geometry.RhinoSurface`

        """
        cls = type(self)
        return cls(self.native_surface.Duplicate())

    def transform(self, T):
        """Transform this surface.

        Parameters
        ----------
        T : :class:`compas.geometry.Transformation`
            A COMPAS transformation.

        Returns
        -------
        None

        """
        self.native_surface.Transform(transformation_to_rhino(T))  # type: ignore

    def isocurve_u(self, u):
        """Compute the isoparametric curve at parameter u.

        Parameters
        ----------
        u : float

        Returns
        -------
        :class:`compas_rhino.geometry.RhinoCurve`

        """
        curve = self.native_surface.IsoCurve(1, u)  # type: ignore
        return RhinoCurve.from_rhino(curve)

    def isocurve_v(self, v):
        """Compute the isoparametric curve at parameter v.

        Parameters
        ----------
        v : float

        Returns
        -------
        :class:`compas_rhino.geometry.RhinoCurve`

        """
        curve = self.native_surface.IsoCurve(0, v)  # type: ignore
        return RhinoCurve.from_rhino(curve)

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
        point = self.native_surface.PointAt(u, v)  # type: ignore
        return point_to_compas(point)

    def curvature_at(self, u, v):
        """Compute the curvature at a point on the surface.

        Parameters
        ----------
        u : float
        v : float

        Returns
        -------
        tuple[[float, float, float], [float, float, float], float, [float, float, float], float, [float, float, float], float, float] | None
            A tuple containing the point, normal vector, maximum principal curvature value, maximum principal curvature direction,
            minimun principal curvature value, minimun principal curvature direction, gaussian curvature value and mean curvature
            value for the point at UV. None at failure.

        """
        surface_curvature = self.native_surface.CurvatureAt(u, v)  # type: ignore
        if surface_curvature:
            point, normal, kappa_u, direction_u, kappa_v, direction_v, gaussian, mean = surface_curvature
            cpoint = point_to_compas(point)
            cnormal = vector_to_compas(normal)
            cdirection_u = vector_to_compas(direction_u)
            cdirection_v = vector_to_compas(direction_v)
            return (cpoint, cnormal, kappa_u, cdirection_u, kappa_v, cdirection_v, gaussian, mean)

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
        result, plane = self.native_surface.FrameAt(u, v)  # type: ignore
        if result:
            return plane_to_compas_frame(plane)

    # ==============================================================================
    # Methods continued
    # ==============================================================================

    def closest_point(self, point, return_parameters=False):
        """Compute the closest point on the curve to a given point.

        Parameters
        ----------
        point : :class:`compas.geometry.Point`
            The test point.
        return_parameters : bool, optional
            If True, return the UV parameters of the closest point as tuple in addition to the point location.

        Returns
        -------
        :class:`compas.geometry.Point`
            If `return_parameters` is False.
        :class:`compas.geometry.Point`, (float, float)
            If `return_parameters` is True.

        """
        result, u, v = self.native_surface.ClosestPoint(point_to_rhino(point))  # type: ignore
        if not result:
            return
        point = self.point_at(u, v)
        if return_parameters:
            return point, (u, v)
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
        box = self.native_surface.GetBoundingBox(optimal)  # type: ignore
        return box_to_compas(Rhino.Geometry.Box(box))

    def intersections_with_curve(self, curve, tolerance=1e-3, overlap=1e-3):
        """Compute the intersections with a curve.

        Parameters
        ----------
        line : :class:`compas.geometry.Curve`

        Returns
        -------
        list[:class:`compas.geometry.Point`]

        """
        intersections = Rhino.Geometry.Intersect.Intersection.CurveSurface(curve.rhino_curve, self.native_surface, tolerance, overlap)
        points = []
        for event in intersections:
            if event.IsPoint:
                point = point_to_compas(event.PointA)
                points.append(point)
        return points
