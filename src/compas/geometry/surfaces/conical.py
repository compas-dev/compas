from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from math import cos
from math import pi
from math import sin

from compas.geometry import Frame
from compas.geometry import Point

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
    name : str, optional
        The name of the surface.

    """

    DATASCHEMA = {
        "type": "object",
        "properties": {
            "radius": {"type": "number", "minimum": 0},
            "height": {"type": "number", "minimum": 0},
            "frame": Frame.DATASCHEMA,
        },
        "required": ["radius", "height", "frame"],
    }

    @property
    def __data__(self):
        return {
            "radius": self.radius,
            "height": self.height,
            "frame": self.frame.__data__,
        }

    @classmethod
    def __from_data__(cls, data):
        return cls(
            radius=data["radius"],
            height=data["height"],
            frame=Frame.__from_data__(data["frame"]),
        )

    def __init__(self, radius, height, frame=None, name=None):
        super(ConicalSurface, self).__init__(frame=frame, name=name)
        self._radius = None
        self._height = None
        self.radius = radius
        self.height = height

    def __repr__(self):
        return "{0}(radius={1}, height={2}, frame={3!r})".format(
            type(self).__name__,
            self.radius,
            self.height,
            self.frame,
        )

    def __eq__(self, other):
        try:
            other_frame = other.frame
            other_radius = other.radius
            other_height = other.height
        except Exception:
            return False
        return self.radius == other_radius and self.height == other_height and self.frame == other_frame

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
