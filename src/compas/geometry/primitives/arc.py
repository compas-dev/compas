from compas.geometry.primitives import Frame
from compas.geometry.primitives import Primitive


class Arc(Primitive):
    """Represents a portion of a circle's arc.

    Parameters
    ----------
    frame : :class:`~compas.geometry.Frame`
        Oriented center of the arc's circle.
    radius : float
        Radius of the arc's circle.
    end_angle : float
        The angle in radians of the
    end_angle :

    """

    def __init__(self, frame=None, radius=None, end_angle=None, start_angle=None, **kwargs):
        super(Arc, self).__init__(**kwargs)

        self._frame = frame
        self._radius = radius
        self._start_angle = start_angle
        self._end_angle = end_angle

    @property
    def data(self):
        return {"frame": self._frame.data, "radius": self._radius, "start": self._start_angle, "end": self._end_angle}

    @data.setter
    def data(self, value):
        self._frame = Frame.from_data(value["frame"])
        self._radius = value["radius"]
        self._start_angle = value["start"]
        self._end_angle = value["end"]

    @property
    def frame(self):
        return self._frame

    @property
    def radius(self):
        return self._radius

    @property
    def start_angle(self):
        return self._start_angle

    @property
    def end_angle(self):
        return self._end_angle
