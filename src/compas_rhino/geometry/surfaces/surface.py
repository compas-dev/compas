from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry import Surface

from compas_rhino.conversions import point_to_rhino
from compas_rhino.conversions import point_to_compas
from compas_rhino.conversions import vector_to_compas
from compas_rhino.conversions import plane_to_compas_frame
from compas_rhino.conversions import box_to_compas
from compas_rhino.conversions import xform_to_rhino
from compas_rhino.conversions import plane_to_rhino
from compas_rhino.conversions import sphere_to_rhino
from compas_rhino.conversions import cylinder_to_rhino

from compas_rhino.geometry.curves import RhinoCurve

import Rhino.Geometry


class RhinoSurface(Surface):
    """Class representing a general surface object.

    Attributes
    ----------
    u_domain: tuple[float, float]
        The parameter domain in the U direction.
    v_domain: tuple[float, float]
        The parameter domain in the V direction.
    is_u_periodic: bool
        True if the surface is periodic in the U direction.
    is_v_periodic: bool
        True if the surface is periodic in the V direction.

    """

    def __init__(self, name=None):
        super(RhinoSurface, self).__init__(name=name)
        self._rhino_surface = None

    @property
    def rhino_surface(self):
        return self._rhino_surface

    @rhino_surface.setter
    def rhino_surface(self, surface):
        self._rhino_surface = surface

    # ==============================================================================
    # Data
    # ==============================================================================

    # ==============================================================================
    # Properties
    # ==============================================================================

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
    # Constructors
    # ==============================================================================

    @classmethod
    def from_plane(cls, plane, u_interval, v_interval, u_degree, v_degree, u_point_count, v_point_count):
        plane = plane_to_rhino(plane)
        u_interval = Rhino.Geometry.Interval(u_interval[0], u_interval[1])
        v_interval = Rhino.Geometry.Interval(v_interval[0], v_interval[1])
        rhino_surface = Rhino.Geometry.NurbsSurface.CreateFromPlane(plane, u_interval, v_interval, u_degree, v_degree, u_point_count, v_point_count)
        return cls.from_rhino(rhino_surface)

    @classmethod
    def from_corners(cls, corners):
        rhino_points = [Rhino.Geometry.Point3d(corner.x, corner.y, corner.z) for corner in corners]
        return cls.from_rhino(Rhino.Geometry.NurbsSurface.CreateFromCorners(*rhino_points))

    @classmethod
    def from_sphere(cls, sphere):
        sphere = sphere_to_rhino(sphere)
        surface = Rhino.Geometry.NurbsSurface.CreateFromSphere(sphere)
        return cls.from_rhino(surface)

    @classmethod
    def from_cylinder(cls, cylinder):
        cylinder = cylinder_to_rhino(cylinder)
        surface = Rhino.Geometry.NurbsSurface.CreateFromCylinder(cylinder)
        return cls.from_rhino(surface)

    @classmethod
    def from_torus(cls, cylinder):
        raise NotImplementedError

    @classmethod
    def from_rhino(cls, rhino_surface):
        """Construct a NURBS surface from an existing Rhino surface.

        Parameters
        ----------
        rhino_surface : :rhino:`Rhino.Geometry.Surface`
            A Rhino surface.

        Returns
        -------
        :class:`~compas_rhino.geometry.RhinoSurface`

        """
        curve = cls()
        curve.rhino_surface = rhino_surface
        return curve

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
        :class:`~compas_rhino.geometry.RhinoSurface`

        """
        cls = type(self)
        surface = cls()
        surface.rhino_surface = self.rhino_surface.Duplicate()
        return surface

    def transform(self, T):
        """Transform this surface.

        Parameters
        ----------
        T : :class:`~compas.geometry.Transformation`
            A COMPAS transformation.

        Returns
        -------
        None

        """
        self.rhino_surface.Transform(xform_to_rhino(T))

    def u_isocurve(self, u):
        """Compute the isoparametric curve at parameter u.

        Parameters
        ----------
        u : float

        Returns
        -------
        :class:`~compas_rhino.geometry.RhinoCurve`

        """
        curve = self.rhino_surface.IsoCurve(1, u)
        return RhinoCurve.from_rhino(curve)

    def v_isocurve(self, v):
        """Compute the isoparametric curve at parameter v.

        Parameters
        ----------
        v : float

        Returns
        -------
        :class:`~compas_rhino.geometry.RhinoCurve`

        """
        curve = self.rhino_surface.IsoCurve(0, v)
        return RhinoCurve.from_rhino(curve)

    def point_at(self, u, v):
        """Compute a point on the surface.

        Parameters
        ----------
        u : float
        v : float

        Returns
        -------
        :class:`~compas.geometry.Point`

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
        :class:`~compas.geometry.Vector`

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
        :class:`~compas.geometry.Frame`

        """
        result, plane = self.rhino_surface.FrameAt(u, v)
        if result:
            return plane_to_compas_frame(plane)

    # ==============================================================================
    # Methods continued
    # ==============================================================================

    def closest_point(self, point, return_parameters=False):
        """Compute the closest point on the curve to a given point.

        Parameters
        ----------
        point : :class:`~compas.geometry.Point`
            The test point.
        return_parameters : bool, optional
            If True, return the UV parameters of the closest point as tuple in addition to the point location.

        Returns
        -------
        :class:`~compas.geometry.Point`
            If `return_parameters` is False.
        :class:`~compas.geometry.Point`, (float, float)
            If `return_parameters` is True.

        """
        result, u, v = self.rhino_surface.ClosestPoint(point_to_rhino(point))
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
        :class:`~compas.geometry.Box`

        """
        box = self.rhino_surface.GetBoundingBox(optimal)
        return box_to_compas(Rhino.Geometry.Box(box))

    def extend_u_by(self, value):
        self._extend_domain(0, value)

    def extend_v_by(self, value):
        self._extend_domain(1, value)

    def _extend_domain(self, domain, value):
        if not (domain == 0 or domain == 1):
            raise ValueError("Expected domain: 0 or 1")
        lower = self.rhino_surface.Domain(domain)[0]
        upper = self.rhino_surface.Domain(domain)[1]
        self.rhino_surface.Extend(domain, Rhino.Geometry.Interval(lower - value, upper + value))

    def reverse(self):
        brep = self.rhino_surface.ToBrep()
        brep.Flip()
        self.rhino_surface = brep.Surfaces[0]
