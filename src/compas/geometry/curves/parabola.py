from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry import Vector
from compas.geometry import Point
from .line import Line
from .conic import Conic


class Parabola(Conic):
    """
    A parabola is defined by a plane and a major and minor axis.
    The origin of the coordinate frame is the center of the parabola.

    The parabola in this implementation is based on the equation ``y = a * x**2``.
    Therefore it will have the y axis of the coordinate frame as its axis of symmetry.

    Parameters
    ----------
    frame : :class:`compas.geometry.Frame`
        The coordinate frame of the parabola.
    major : float
        The major of the parabola.

    Attributes
    ----------
    frame : :class:`compas.geometry.Frame`
        The coordinate frame of the hyperbola.
    focal : float
        The distance between the two focus points.
    center : :class:`compas.geometry.Point`, read-only
        The center of the parabola.
    plane : :class:`compas.geometry.Plane`, read-only
        The plane of the parabola.
    latus : :class:`compas.geometry.Point`, read-only
        The latus rectum of the parabola.
    eccentricity : float, read-only
        The eccentricity of a parabola is between 0 and 1.
    focus : :class:`compas.geometry.Point`, read-only
        The focus of the parabola.
    directix : :class:`compas.geometry.Line`, read-only
        The directix is the line perpendicular to the y axis of the parabola
        at a distance ``d = + major / eccentricity`` from the center of the parabola.
        The second directix intersects the positive x axis.
    is_closed : bool, read-only
        False.
    is_periodic : bool, read-only
        False.

    """

    def __init__(self, focal, frame=None, **kwargs):
        super(Parabola, self).__init__(frame=frame, **kwargs)
        self._focal = None
        self.focal = focal

    def __repr__(self):
        return "Parabola(focal={0!r}, frame={1!r})".format(self.focal, self.frame)

    def __eq__(self, other):
        try:
            return self.focal == other.focal and self.frame == other.frame
        except AttributeError:
            return False

    # ==========================================================================
    # Data
    # ==========================================================================

    @property
    def data(self):
        return {"frame": self.frame, "focal": self.focal}

    @data.setter
    def data(self, data):
        self.frame = data["frame"]
        self.focal = data["focal"]

    # ==========================================================================
    # properties
    # ==========================================================================

    @property
    def focal(self):
        if self._focal is None:
            raise ValueError("The focal length of the parabola is not set.")
        return self._focal

    @focal.setter
    def focal(self, focal):
        self._focal = focal

    @property
    def a(self):
        return 1 / (4 * self.focal)

    @a.setter
    def a(self, a):
        self.focal = 1 / (4 * a)

    @property
    def eccentricity(self):
        return 1

    @property
    def latus(self):
        return 2 * self.focal

    @property
    def focus(self):
        return self.point + self.yaxis * self.focal

    @property
    def vertex(self):
        return self.point

    @property
    def directix(self):
        point = self.point + self.yaxis * -self.focal
        return Line(point, point + self.xaxis)

    @property
    def is_closed(self):
        return False

    @property
    def is_periodic(self):
        return False

    # ==========================================================================
    # Constructors
    # ==========================================================================

    # ==========================================================================
    # Methods
    # ==========================================================================

    def point_at(self, t):
        """
        Point at the parameter.

        Parameters
        ----------
        t : float

        Returns
        -------
        :class:`compas_future.geometry.Point`

        """
        x = t
        y = self.a * x**2
        z = 0
        point = Point(x, y, z)
        # point.transform(self.transformation)
        return point

    def tangent_at(self, t):
        """
        Tangent vector at the parameter.

        Parameters
        ----------
        t : float
            The line parameter.

        Returns
        -------
        :class:`compas_future.geometry.Vector`

        """
        x0 = t
        y0 = self.a * t**2
        x = 2 * t
        y = 2 * self.a * x0 * x - y0
        tangent = Vector(x - x0, y - y0, 0)
        tangent.unitize()
        tangent.transform(self.transformation)
        return tangent

    def normal_at(self, t):
        """
        Normal at a specific normalized parameter.

        Parameters
        ----------
        t : float
            The line parameter.

        Returns
        -------
        :class:`compas_future.geometry.Vector`

        """
        x0 = t
        y0 = self.a * t**2
        x = 2 * t
        y = 2 * self.a * x0 * x - y0
        normal = Vector(y0 - y, x - x0, 0)
        normal.unitize()
        normal.transform(self.transformation)
        return normal
