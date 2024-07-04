from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from math import cos
from math import pi
from math import sin

from compas.geometry import Circle
from compas.geometry import Frame
from compas.geometry import Point
from compas.geometry import Vector

from .surface import Surface

PI2 = 2 * pi


class CylindricalSurface(Surface):
    """A cylindrical surface is defined by a radius and a local coordinate system.

    Parameters
    ----------
    radius : float
        The radius of the cylinder.
    frame : :class:`Frame`
        The local coordinate system of the cylinder.
    name : str, optional
        The name of the surface.

    """

    DATASCHEMA = {
        "type": "object",
        "properties": {
            "radius": {"type": "number", "minimum": 0},
            "frame": Frame.DATASCHEMA,
        },
        "required": ["radius", "frame"],
    }

    @property
    def __data__(self):
        return {
            "radius": self.radius,
            "frame": self.frame.__data__,
        }

    @classmethod
    def __from_data__(cls, data):
        return cls(
            radius=data["radius"],
            frame=Frame.__from_data__(data["frame"]),
        )

    def __init__(self, radius, frame=None, name=None):
        super(CylindricalSurface, self).__init__(frame=frame, name=name)
        self._radius = None
        self.radius = radius

    def __repr__(self):
        return "{0}(radius={1}, frame={2!r})".format(
            type(self).__name__,
            self.radius,
            self.frame,
        )

    def __eq__(self, other):
        try:
            other_frame = other.frame
            other_radius = other.radius
        except Exception:
            return False
        return self.radius == other_radius and self.frame == other_frame

    # =============================================================================
    # Properties
    # =============================================================================

    @property
    def center(self):
        return self.frame.point

    @center.setter
    def center(self, point):
        self.frame.point = point

    @property
    def radius(self):
        if self._radius is None:
            raise ValueError("The radius of the surface has not been set yet.")
        return self._radius

    @radius.setter
    def radius(self, radius):
        if radius < 0:
            raise ValueError("The radius of a sphere should be larger than or equal to zero.")
        self._radius = float(radius)

    @property
    def area(self):
        raise NotImplementedError

    @property
    def volume(self):
        raise NotImplementedError

    # =============================================================================
    # Constructors
    # =============================================================================

    @classmethod
    def from_plane_and_radius(cls, plane, radius):
        """Construct a cylindrical surface from a plane and a radius.

        Parameters
        ----------
        plane : :class:`compas.geometry.Plane`
            The plane of the surface.
        radius : float
            The radius of the surface.

        Returns
        -------
        :class:`compas.geometry.CylindricalSurface`
            A cylindrical surface.

        """
        return cls(radius, frame=Frame.from_plane(plane))

    @classmethod
    def from_three_points(cls, a, b, c):
        """Construct a cylindrical from three points.

        Parameters
        ----------
        a : :class:`compas.geometry.Point`
            The first point.
        b : :class:`compas.geometry.Point`
            The second point.
        c : :class:`compas.geometry.Point`
            The third point.

        Returns
        -------
        :class:`compas.geometry.CylindricalSurface`
            A cylindrical surface.

        """
        circle = Circle.from_three_points(a, b, c)
        return cls(circle.radius, frame=circle.frame)

    # =============================================================================
    # Conversions
    # =============================================================================

    # =============================================================================
    # Transformations
    # =============================================================================

    # =============================================================================
    # Methods
    # =============================================================================

    def point_at(self, u, v, world=True):
        """Compute a point on the surface at the given parameters.

        Parameters
        ----------
        u : float
            The first parameter.
        v : float
            The second parameter.
        world : bool, optional
            If ``True``, the point is transformed to world coordinates.

        Returns
        -------
        :class:`compas.geometry.Point`
            The point at the given parameters.

        """
        u = u * PI2
        x = self.radius * cos(u)
        y = self.radius * sin(u)
        z = v
        point = Point(x, y, z)
        if world:
            point.transform(self.transformation)
        return point

    def normal_at(self, u, world=True):
        """Compute the normal at a point on the surface at the given parameters.

        Parameters
        ----------
        u : float
            The first parameter.
        world : bool, optional
            If ``True``, the normal is transformed to world coordinates.

        Returns
        -------
        :class:`compas.geometry.Vector`
            The normal at the given parameters.

        """
        u = u * PI2
        x = self.radius * cos(u)
        y = self.radius * sin(u)
        z = 0
        vector = Vector(x, y, z)
        vector.unitize()
        if world:
            vector.transform(self.transformation)
        return vector

    def frame_at(self, u, v, world=True):
        """Compute the frame at a point on the surface at the given parameters.

        Parameters
        ----------
        u : float
            The first parameter.
        v : float
            The second parameter.
        world : bool, optional
            If ``True``, the frame is transformed to world coordinates.

        Returns
        -------
        :class:`compas.geometry.Frame`
            The frame at the given parameters.

        """
        u = u * PI2
        point = self.point_at(u, v, world=False)
        zaxis = self.normal_at(u, world=False)
        yaxis = self.frame.zaxis
        xaxis = yaxis.cross(zaxis)
        frame = Frame(point, xaxis, yaxis)
        if world:
            frame.transform(self.transformation)
        return frame
