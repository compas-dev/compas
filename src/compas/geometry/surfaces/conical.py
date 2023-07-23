from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from math import pi, cos, sin

from compas.geometry import Point
from compas.geometry import Frame
from .surface import Surface

PI2 = 2 * pi


class ConicalSurface(Surface):
    """A cylindrical surface is defined by a radius and a local coordinate system.

    Parameters
    ----------
    radius : float
        The radius of the cone.
    frame : :class:`Frame`
        The local coordinate system of the cone.

    Attributes
    ----------

    Examples
    --------

    """

    JSONSCHEMA = {
        "type": "object",
        "properties": {
            "radius": {"type": "number", "minimum": 0},
            "height": {"type": "number", "minimum": 0},
            "frame": Frame.JSONSCHEMA,
        },
        "required": ["radius", "height", "frame"],
    }

    # overwriting the __new__ method is necessary
    # to avoid triggering the plugin mechanism of the base surface class
    def __new__(cls, *args, **kwargs):
        surface = object.__new__(cls)
        surface.__init__(*args, **kwargs)
        return surface

    def __init__(self, radius, height, frame=None, **kwargs):
        super(ConicalSurface, self).__init__(frame=frame, **kwargs)
        self._radius = None
        self._height = None
        self.radius = radius
        self.height = height

    def __repr__(self):
        return "ConicalSurface(radius={0!r}, height={1!r}, frame={2!r})".format(self.radius, self.height, self.frame)

    def __eq__(self, other):
        try:
            other_frame = other.frame
            other_radius = other.radius
            other_height = other.height
        except Exception:
            return False
        return self.radius == other_radius and self.height == other_height and self.frame == other_frame

    @property
    def data(self):
        return {"radius": self.radius, "height": self.height, "frame": self.frame}

    @data.setter
    def data(self, data):
        self.radius = data["radius"]
        self.height = data["height"]
        self.frame = data["frame"]

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
    def height(self):
        if self._height is None:
            raise ValueError("The height of the surface has not been set yet.")
        return self._height

    @height.setter
    def height(self, height):
        if height < 0:
            raise ValueError("The height of the surface should be larger than or equal to zero.")
        self._height = float(height)

    # =============================================================================
    # Constructors
    # =============================================================================

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
            If ``True``, return the point in world coordinates.

        Returns
        -------
        :class:`compas.geometry.Point`
            The point at the given parameters.

        """
        u = u * PI2
        radius = (1 - v) * self.radius
        x = radius * cos(u)
        y = radius * sin(u)
        z = v * self.height
        point = Point(x, y, z)
        if world:
            point.transform(self.transformation)
        return point

    # def normal_at(self, u):
    #     """Compute the normal at a point on the surface at the given parameters.

    #     Parameters
    #     ----------
    #     u : float
    #         The first parameter.

    #     Returns
    #     -------
    #     :class:`compas.geometry.Vector`
    #         The normal at the given parameters.

    #     """
    #     u = u * 2 * pi
    #     x = self.radius * cos(u)
    #     y = self.radius * sin(u)
    #     z = 0
    #     return self.frame.xaxis * x + self.frame.yaxis * y + self.frame.zaxis * z

    # def frame_at(self, u, v):
    #     """Compute the frame at a point on the surface at the given parameters.

    #     Parameters
    #     ----------
    #     u : float
    #         The first parameter.
    #     v : float
    #         The second parameter.

    #     Returns
    #     -------
    #     :class:`compas.geometry.Frame`
    #         The frame at the given parameters.

    #     """
    #     u = u * 2 * pi
    #     point = self.point_at(u, v)
    #     zaxis = self.normal_at(u)
    #     yaxis = self.frame.zaxis
    #     xaxis = yaxis.cross(zaxis)
    #     return Frame(point, xaxis, yaxis)
