from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import Rhino.Geometry  # type: ignore

import compas

if not compas.IPY:
    from typing import Tuple  # noqa: F401

from compas.geometry import Frame
from compas.geometry import Plane  # noqa: F401
from compas.geometry import Surface
from compas_rhino.conversions import box_to_compas
from compas_rhino.conversions import cylinder_to_rhino
from compas_rhino.conversions import frame_to_rhino_plane
from compas_rhino.conversions import plane_to_compas_frame
from compas_rhino.conversions import plane_to_rhino
from compas_rhino.conversions import point_to_compas
from compas_rhino.conversions import point_to_rhino
from compas_rhino.conversions import sphere_to_rhino
from compas_rhino.conversions import transformation_to_rhino
from compas_rhino.conversions import vector_to_compas
from compas_rhino.geometry.curves import RhinoCurve


class RhinoSurface(Surface):
    """Class representing a general surface object.

    Attributes
    ----------
    domain_u: tuple[float, float]
        The parameter domain in the U direction.
    domain_v: tuple[float, float]
        The parameter domain in the V direction.
    frame: :class:`compas.geometry.Frame`
        The frame of the surface at the parametric origin.
    is_periodic_u: bool
        True if the surface is periodic in the U direction.
    is_periodic_v: bool
        True if the surface is periodic in the V direction.
    native_surface: :class:`Rhino.Geometry.Surface`
        The underlying Rhino surface object.

    """

    @classmethod
    def __from_data__(cls, data):
        frame = Frame.__from_data__(data["frame"])
        u_interval = tuple(data["u_interval"])
        v_interval = tuple(data["v_interval"])
        return cls.from_frame(frame, u_interval, v_interval)

    def __new__(cls, *args, **kwargs):
        # needed because the Surface.__new__ now enforces creation via alternative constructors only
        return super(Surface, RhinoSurface).__new__(RhinoSurface, *args, **kwargs)

    def __init__(self, name=None):
        super(RhinoSurface, self).__init__(name=name)
        self._rhino_surface = None

    def _get_frame_from_planesurface(self):
        u_start = self.domain_u[0]
        v_start = self.domain_v[0]
        success, frame = self.native_surface.FrameAt(u_start, v_start)
        if not success:
            raise ValueError("Failed to get frame at u={} v={}".format(u_start, v_start))
        return plane_to_compas_frame(frame)

    # ==============================================================================
    # Implementation of abstract properties
    # ==============================================================================

    @property
    def native_surface(self):
        return self._rhino_surface

    @native_surface.setter
    def native_surface(self, surface):
        self._rhino_surface = surface

    @property
    def rhino_surface(self):
        # TODO: Deprecate. replace with native_surface
        return self._rhino_surface

    @rhino_surface.setter
    def rhino_surface(self, surface):
        # TODO: Deprecate. replace with native_surface
        self._rhino_surface = surface

    @property
    def is_closed(self):
        # TODO: implement this properly
        raise NotImplementedError

    @property
    def is_periodic_u(self):
        if self.rhino_surface:
            return self.rhino_surface.IsPeriodic(0)

    @property
    def is_periodic_v(self):
        if self.rhino_surface:
            return self.rhino_surface.IsPeriodic(1)

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

    @classmethod
    def from_rhino(cls, rhino_surface):
        """Construct a NURBS surface from an existing Rhino surface.

        .. deprecated:: 2.1.1
                ``from_rhino`` will be removed in the future. Use ``from_native`` instead.

        Parameters
        ----------
        rhino_surface : :rhino:`Rhino.Geometry.Surface`
            A Rhino surface.

        Returns
        -------
        :class:`compas_rhino.geometry.RhinoSurface`

        """
        from warnings import warn

        warn("RhinoSurface.from_rhino will be removed in the future. Use RhinoSurface.from_native instead.", DeprecationWarning)
        return cls.from_native(rhino_surface)

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
        instance = cls()
        instance.native_surface = native_surface
        instance.frame = instance._get_frame_from_planesurface()
        instance._domain_u = native_surface.Domain(0)[0], native_surface.Domain(0)[1]
        instance._domain_v = native_surface.Domain(1)[0], native_surface.Domain(1)[1]
        return instance

    @classmethod
    def from_plane(cls, plane, u_domain=(0.0, 1.0), v_domain=(0.0, 1.0)):
        # type: (Plane, Tuple[float, float], Tuple[float, float]) -> RhinoSurface
        """Construct a surface from a plane.

        Parameters
        ----------
        plane : :class:`compas.geometry.Plane` or :class:`compas.geometry.Frame`
            The plane or frame to use as origin and orientation of the surface.
        u_domain : tuple(float, float), optional
            The parametric domain of the U parameter. u_domain[0] => u_domain[1].
            Default is ``(0.0, 1.0)``.
        v_domain : tuple(float, float), optional
            The parametric domain of the V parameter. v_domain[0] => v_domain[1].
            Default is ``(0.0, 1.0)``.

        Note
        ----
        While the plane's origin is its center, the surface's parametric origin is at the surface's corner.
        For the plane to overlap with the surface, the plane's origin should be first shifted by half it's domain.
        Alternatively, the surface's domain can be adjusted to match the plane's origin.

        Returns
        -------
        :class:`compas_rhino.geometry.RhinoSurface`

        """
        if isinstance(plane, Frame):
            plane = Plane.from_frame(plane)
        plane = plane_to_rhino(plane)
        rhino_surface = Rhino.Geometry.PlaneSurface(plane, Rhino.Geometry.Interval(*u_domain), Rhino.Geometry.Interval(*v_domain))
        return cls.from_native(rhino_surface)

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
        surface = cls()
        surface.rhino_surface = self.rhino_surface.Duplicate()  # type: ignore
        return surface

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
        self.rhino_surface.Transform(transformation_to_rhino(T))  # type: ignore

    def u_isocurve(self, u):
        """Compute the isoparametric curve at parameter u.

        Parameters
        ----------
        u : float

        Returns
        -------
        :class:`compas_rhino.geometry.RhinoCurve`

        """
        curve = self.rhino_surface.IsoCurve(1, u)  # type: ignore
        return RhinoCurve.from_native(curve)

    def v_isocurve(self, v):
        """Compute the isoparametric curve at parameter v.

        Parameters
        ----------
        v : float

        Returns
        -------
        :class:`compas_rhino.geometry.RhinoCurve`

        """
        curve = self.rhino_surface.IsoCurve(0, v)  # type: ignore
        return RhinoCurve.from_native(curve)

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
        point = self.rhino_surface.PointAt(u, v)  # type: ignore
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
        surface_curvature = self.rhino_surface.CurvatureAt(u, v)  # type: ignore
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
        result, plane = self.rhino_surface.FrameAt(u, v)  # type: ignore
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
        result, u, v = self.rhino_surface.ClosestPoint(point_to_rhino(point))  # type: ignore
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
        box = self.rhino_surface.GetBoundingBox(optimal)  # type: ignore
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
        intersections = Rhino.Geometry.Intersect.Intersection.CurveSurface(curve.rhino_curve, self.rhino_surface, tolerance, overlap)
        points = []
        for event in intersections:
            if event.IsPoint:
                point = point_to_compas(event.PointA)
                points.append(point)
        return points
