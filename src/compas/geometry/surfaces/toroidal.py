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


class ToroidalSurface(Surface):
    """A spherical surface is defined by a radius and a frame.

    Parameters
    ----------
    radius : float
        The radius of the sphere.
    frame : :class:`Frame`
        The frame of the sphere.
    name : str, optional
        The name of the surface.

    Examples
    --------
    >>> from compas.geometry import Frame
    >>> from compas.geometry import ToroidalSurface
    >>> frame = Frame([0, 0, 0], [1, 0, 0], [0, 1, 0])
    >>> sphere = ToroidalSurface(1.0, frame)

    """

    DATASCHEMA = {
        "type": "object",
        "properties": {
            "radius_axis": {"type": "number", "minimum": 0},
            "radius_pipe": {"type": "number", "minimum": 0},
            "frame": Frame.DATASCHEMA,
        },
        "required": ["radius_axis", "radius_pipe", "frame"],
    }

    @property
    def __data__(self):
        return {
            "radius_axis": self.radius_axis,
            "radius_pipe": self.radius_pipe,
            "frame": self.frame.__data__,
        }

    @classmethod
    def __from_data__(cls, data):
        return cls(
            radius_axis=data["radius_axis"],
            radius_pipe=data["radius_pipe"],
            frame=Frame.__from_data__(data["frame"]),
        )

    def __init__(self, radius_axis, radius_pipe, frame=None, name=None):
        super(ToroidalSurface, self).__init__(frame=frame, name=name)
        self._radius_axis = None
        self._radius_pipe = None
        self.radius_axis = radius_axis
        self.radius_pipe = radius_pipe

    def __repr__(self):
        return "{0}(radius_axis={1}, radius_pipe={2}, frame={3!r})".format(
            type(self).__name__,
            self.radius_axis,
            self.radius_pipe,
            self.frame,
        )

    def __eq__(self, other):
        try:
            other_frame = other.frame
            other_radius_axis = other.radius_axis
            other_radius_pipe = other.radius_pipe
        except Exception:
            return False
        return self.radius_axis == other_radius_axis and self.radius_pipe == other_radius_pipe and self.frame == other_frame

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
    def radius_axis(self):
        if self._radius_axis is None:
            raise ValueError("The radius of the surface main axis has not been set yet.")
        return self._radius_axis

    @radius_axis.setter
    def radius_axis(self, radius):
        if radius < 0:
            raise ValueError("The radius of the main axis should be larger than or equal to zero.")
        self._radius_axis = float(radius)

    # =============================================================================
    # Constructors
    # =============================================================================

    @classmethod
    def from_plane_and_radius(cls, plane, radius_axis, radius_pipe):
        """Construct a sphere from a plane and a radius.

        Parameters
        ----------
        plane : :class:`compas.geometry.Plane`
            The plane of the sphere.
        radius : float
            The radius of the sphere.

        Returns
        -------
        :class:`compas.geometry.ToroidalSurface`
            A sphere.

        """
        return cls(radius_axis, radius_pipe, frame=Frame.from_plane(plane))

    # =============================================================================
    # Conversions
    # =============================================================================

    # =============================================================================
    # Methods
    # =============================================================================

    def point_at(self, u, v, world=True):
        """Construct a point on the sphere.

        Parameters
        ----------
        u : float
            The first parameter.
            The parameter value should be between zero and one,
            and will be mapped to the corresponding angle between zero and pi.
        v : float
            The second parameter.
            The parameter value should be between zero and one,
            and will be mapped to the corresponding angle between zero and 2 * pi.

        Returns
        -------
        :class:`compas.geometry.Point`
            A point on the sphere.

        """
        u = u * PI2
        v = v * PI2
        x = (self.radius_axis + self.radius_pipe * cos(v)) * cos(u)
        y = (self.radius_axis + self.radius_pipe * cos(v)) * sin(u)
        z = self.radius_pipe * sin(v)
        point = Point(x, y, z)
        if world:
            point.transform(self.transformation)
        return point

    def normal_at(self, u, v, world=True):
        """Construct a normal vector at a point on the sphere.

        Parameters
        ----------
        u : float
            The first parameter.
        v : float
            The second parameter.
        world : bool, optional
            If ``True``, the normal vector is transformed to world coordinates.

        Returns
        -------
        :class:`compas.geometry.Vector`
            The normal vector.

        """
        raise NotImplementedError
