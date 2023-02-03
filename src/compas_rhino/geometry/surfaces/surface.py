from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry import Surface

from compas_rhino.conversions import point_to_rhino
from compas_rhino.conversions import point_to_compas
from compas_rhino.conversions import vector_to_compas
from compas_rhino.conversions import plane_to_compas_frame
from compas_rhino.conversions import frame_to_rhino_plane
from compas_rhino.conversions import plane_to_rhino
from compas_rhino.conversions import box_to_compas
from compas_rhino.conversions import xform_to_rhino
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
    def from_corners(cls, corners):
        """Creates a NURBS surface using the given 4 corners.

        The order of the given points determins the normal direction of the generated surface.

        Parameters
        ----------
        corners : list(:class:`~compas.geometry.Point`)
            4 points in 3d space to represent the corners of the planar surface.

        Returns
        -------
        :class:`~compas_rhino.geometry.RhinoNurbsSurface`

        """
        rhino_points = [Rhino.Geometry.Point3d(corner.x, corner.y, corner.z) for corner in corners]
        return cls.from_rhino(Rhino.Geometry.NurbsSurface.CreateFromCorners(*rhino_points))

    @classmethod
    def from_sphere(cls, sphere):
        """Creates a NURBS surface from a sphere.

        Parameters
        ----------
        sphere : :class:`~compas.geometry.Sphere`
            The surface's geometry.

        Returns
        -------
        :class:`~compas_rhino.geometry.RhinoNurbsSurface`

        """
        sphere = sphere_to_rhino(sphere)
        surface = Rhino.Geometry.NurbsSurface.CreateFromSphere(sphere)
        return cls.from_rhino(surface)

    @classmethod
    def from_cylinder(cls, cylinder):
        """Create a NURBS surface from a cylinder.

        Parameters
        ----------
        cylinder : :class:`~compas.geometry.Cylinder`
            The surface's geometry.

        Returns
        -------
        :class:`~compas_rhino.geometry.RhinoNurbsSurface`

        """
        cylinder = cylinder_to_rhino(cylinder)
        surface = Rhino.Geometry.NurbsSurface.CreateFromCylinder(cylinder)
        return cls.from_rhino(surface)

    @classmethod
    def from_torus(cls, torus):
        """Create a NURBS surface from a torus.

        Parameters
        ----------
        torus : :class:`~compas.geometry.Torus`
            The surface's geometry.

        Returns
        -------
        :class:`~compas_rhino.geometry.RhinoNurbsSurface`

        """
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

    @classmethod
    def from_plane(cls, plane, box):
        """Construct a surface from a plane.

        Parameters
        ----------
        plane : :class:`compas.geometry.Plane`
            The plane.

        Returns
        -------
        :class:`~compas_rhino.geometry.RhinoSurface`

        """
        plane = plane_to_rhino(plane)
        box = Rhino.Geometry.BoundingBox(box.xmin, box.ymin, box.zmin, box.xmax, box.ymax, box.zmax)
        rhino_surface = Rhino.Geometry.PlaneSurface.CreateThroughBox(plane, box)
        return cls.from_rhino(rhino_surface)

    @classmethod
    def from_frame(cls, frame, u_interval, v_interval):
        """Creates a planar surface from a frame and parametric domain information.

        Parameters
        ----------
        frame : :class:`~compas.geometry.Frame`
            A frame with point at the center of the wanted plannar surface and
            x and y axes the direction of u and v respectively.
        u_interval : tuple(float, float)
            The parametric domain of the U parameter. u_interval[0] => u_interval[1].
        v_interval : tuple(float, float)
            The parametric domain of the V parameter. v_interval[0] => v_interval[1].

        Returns
        -------
        :class:`compas_rhino.geometry.surface.RhinoSurface`

        """
        surface = Rhino.Geometry.PlaneSurface(
            frame_to_rhino_plane(frame),
            Rhino.Geometry.Interval(*u_interval),
            Rhino.Geometry.Interval(*v_interval),
        )
        if not surface:
            msg = "Failed creating PlaneSurface from frame:{} u_interval:{} v_interval:{}"
            raise ValueError(msg.format(frame, u_interval, v_interval))
        return cls.from_rhino(surface)

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
        tuple[[float, float, float], [float, float, float], float, [float, float, float], float, [float, float, float], float, float] | None
            A tuple containing the point, normal vector, maximum principal curvature value, maximum principal curvature direction,
            minimun principal curvature value, minimun principal curvature direction, gaussian curvature value and mean curvature
            value for the point at UV. None at failure.

        """
        surface_curvature = self.rhino_surface.CurvatureAt(u, v)
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

    def intersections_with_curve(self, curve, tolerance=1e-3, overlap=1e-3):
        """Compute the intersections with a curve.

        Parameters
        ----------
        line : :class:`~compas.geometry.Curve`

        Returns
        -------
        list[:class:`~compas.geometry.Point`]

        """
        intersections = Rhino.Geometry.Intersect.Intersection.CurveSurface(
            curve.rhino_curve, self.rhino_surface, tolerance, overlap
        )
        points = []
        for event in intersections:
            if event.IsPoint:
                point = point_to_compas(event.PointA)
                points.append(point)
        return points
