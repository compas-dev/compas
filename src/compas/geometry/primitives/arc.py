import math

from compas.geometry import close
from compas.geometry.primitives import Frame
from compas.geometry.primitives import Primitive


class Arc(Primitive):
    """Represents a portion of a circle's arc.

    Parameters
    ----------
    frame : :class:`~compas.geometry.Frame`
        Coordinate frame at the center of the arc's circle.
    radius : float
        Radius of the arc's circle.
    end_angle : float
        The angle in radians of the end of this Arc.
    start_angle :
        The angle in radians of the start of this Arc.

    Attributes
    ----------
    length : float
        The length of the arc (radius * angle)
    angle : float
        The sweep angle in radians (between incrementing end angle and start angle).
    domain : tuple(float, float)
        A tuple containing the start and end angles of this arc, in radians.
    center : :class:`~compas.geometry.Point`
        The center point of the circle which coincides with this Arc.
    circumference : float
        The circumference of the circle which coincides with this Arc.
    diameter : float
        The diameter of the circle which coincides with this Arc.

    """

    def __init__(self, frame=None, radius=None, end_angle=None, start_angle=None, **kwargs):
        super(Arc, self).__init__(**kwargs)

        self._frame = frame
        self._radius = radius
        self._start_angle = start_angle if start_angle is not None else 0.0
        self._end_angle = end_angle

        if self._radius is not None and self._end_angle is not None:
            self._verify()

    @property
    def data(self):
        return {
            "frame": self._frame.data,
            "radius": self._radius,
            "start": self._start_angle,
            "end": self._end_angle,
        }

    @data.setter
    def data(self, value):
        self._frame = Frame.from_data(value["frame"])
        self._radius = value["radius"]
        self._start_angle = value["start"]
        self._end_angle = value["end"]

    @property
    def frame(self):
        return self._frame

    @frame.setter
    def frame(self, value):
        self._frame = value

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        self._radius = value

    @property
    def start_angle(self):
        return self._start_angle

    @start_angle.setter
    def start_angle(self, value):
        self._start_angle = value
        self._verify()

    @property
    def end_angle(self):
        return self._end_angle

    @end_angle.setter
    def end_angle(self, value):
        self._end_angle = value
        self._verify

    @property
    def length(self):
        return self.radius * self.angle

    @property
    def angle(self):
        return self._end_angle - self._start_angle

    @property
    def domain(self):
        return self._start_angle, self._end_angle

    @property
    def center(self):
        return self.frame.point

    @property
    def circumference(self):
        return 2.0 * math.pi * self.radius

    @property
    def diameter(self):
        return 2.0 * self.radius

    @property
    def is_circle(self):
        return close(abs(abs(self.angle) - 2.0 * math.pi), 0.0)

    @classmethod
    def from_circle(cls, circle, start_angle, end_angle):
        """Creates an Arc from a circle and start and end angles.

        Parameters
        ----------
        circle : :class:`~compas.geometry.Circle`
            The center point and radius of this circle will be used to create an Arc.
        start_angle : float
            The start angle in radians.
        end_angle : float
            The end angle in radians.

        Returns
        -------
        :class:`~compas.geometry.Arc`

        """
        frame = Frame.worldXY()
        # TODO: take circle.frame once it has one
        frame.point = circle.center.copy()
        return cls(frame, circle.radius, end_angle, start_angle)

    def _verify(self):
        if self.angle < 0.0 or self.angle > 2.0 * math.pi:
            raise ValueError("Sweep angle must satisfy 0 < angle < 2 * Pi. Currently:{}".format(self.angle))
