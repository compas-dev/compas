from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from math import cos, sin, sqrt
from math import pi

from compas.geometry import Frame
from .conic import Conic

PI2 = 2 * pi


class Hyperbola(Conic):
    r"""
    A hyperbola is defined by a coordinate frame and a major and minor axis.

    It is implemented using the equation

    .. math::

        \frac{x^2}{a^2} - \frac{y^2}{b^2} = 1

    and with parametric form

    .. math::

        x(t) &= a \times \sec(t) \\
        y(t) &= b \times \tan(t)

    This means that the center of the hyperbola is at the center of the coordinate frame,
    the vertices of the left and right branches are at (0, -a) and (0, +a) respectively,
    the linear eccentricity is math::`\sqrt{a^2 + b^2}`,
    and the eccentricity math::`\fraq{\sqrt{a^2 + b^2}}{a}`.

    Parameters
    ----------
    frame : :class:`compas.geometry.Frame`
        The coordinate frame of the hyperbola.
    major : float
        The major of the hyperbola.
    minor : float
        The minor of the hyperbola.

    Attributes
    ----------
    frame : :class:`compas.geometry.Frame`
        The coordinate frame of the hyperbola.
    major : float
        The major radius of the hyperbola.
    minor : float
        The minor radius of the hyperbola.
    center : :class:`compas.geometry.Point`
        The center of the hyperbola.
    normal : :class:`compas.geometry.Vector`, read-only
        The normal of the hyperbola.
    plane : :class:`compas.geometry.Plane`, read-only
        The plane of the hyperbola.
    semifocal : float, read-only
        The distance between the center and the focus points.
    focal : float, read-only
        The distance between the two focus points.
    eccentricity : float, read-only
        This is the ratio between the semifocal length to the length of the semi-major axis.
        The eccentricity of a hyperbola is a number higher than 1.
    vertex1 : :class:`compas.geometry.Point`, read-only
        The first vertex of the hyperbola is on the positive x axis.
    vertex2 : :class:`compas.geometry.Point`, read-only
        The second vertex of the hyperbola is on the negative x axis.
    focus1 : :class:`compas.geometry.Point`, read-only
        The first focus of the hyperbola is on the positive x axis.
    focus2 : :class:`compas.geometry.Point`, read-only
        The second focus of the hyperbola is on the negative x axis.
    asymptote1 : :class:`compas.geometry.Line`, read-only
        The first asymptote of the hyperbola.
    asymptote2 : :class:`compas.geometry.Line`, read-only
        The second asymptote of the hyperbola.
    domain : tuple[float, float], read-only
        The parameter domain: 0, 2pi
    is_closed : bool, read-only
        A hyperbola is not closed (False).
    is_periodic : bool, read-only
        A hyperbola is not periodic (False).

    """

    JSONSCHEMA = {
        "type": "object",
        "properties": {
            "frame": Frame.JSONSCHEMA,
            "major": {"type": "number", "minimum": 0},
            "minor": {"type": "number", "minimum": 0},
        },
        "required": ["frame", "major", "minor"],
    }

    def __init__(self, frame=None, major=1.0, minor=1.0, **kwargs):
        super(Hyperbola, self).__init__(frame=frame, **kwargs)
        self._major = None
        self._minor = None
        self.major = major
        self.minor = minor

    def __repr__(self):
        return "Hyperbola({0!r}, {1!r}, {2!r})".format(self.frame, self.major, self.minor)

    def __len__(self):
        return 3

    def __getitem__(self, key):
        if key == 0:
            return self.frame
        elif key == 1:
            return self.major
        elif key == 2:
            return self.minor
        else:
            raise KeyError

    def __setitem__(self, key, value):
        if key == 0:
            self.frame = value
        elif key == 1:
            self.major = value
        elif key == 2:
            self.minor = value
        else:
            raise KeyError

    def __iter__(self):
        return iter([self.frame, self.major, self.minor])

    # ==========================================================================
    # Data
    # ==========================================================================

    @property
    def data(self):
        return {"frame": self.frame, "major": self.major, "minor": self.minor}

    @data.setter
    def data(self, data):
        self.frame = data["frame"]
        self.major = data["major"]
        self.minor = data["minor"]

    # ==========================================================================
    # Properties
    # ==========================================================================

    @property
    def center(self):
        return self.frame.point

    @center.setter
    def center(self, point):
        self.frame.point = point

    @property
    def major(self):
        if not self._major:
            raise ValueError("Length of major axis is not set.")
        return self._major

    @major.setter
    def major(self, major):
        if major < 0:
            raise ValueError("Major axis length cannot be negative.")
        self._major = float(major)

    @property
    def minor(self):
        if not self._minor:
            raise ValueError("Length of minor axis is not set.")
        return self._minor

    @minor.setter
    def minor(self, minor):
        if minor < 0:
            raise ValueError("Minor axis length cannot be negative.")
        self._minor = float(minor)

    @property
    def semifocal(self):
        return sqrt(self.major**2 + self.minor**2)

    @property
    def focal(self):
        return 2 * self.semifocal

    @property
    def eccentricity(self):
        return self.semifocal / self.major

    @property
    def focus1(self):
        return self.point + self.xaxis * self.semifocal

    @property
    def focus2(self):
        return self.point + self.xaxis * -self.semifocal

    @property
    def vertex1(self):
        return self.point + self.xaxis * self.major

    @property
    def vertex2(self):
        return self.point + self.xaxis * -self.major

    @property
    def asymptote1(self):
        pass

    @property
    def asymptote2(self):
        pass

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
        t = t * PI2
        sec_t = 1 / cos(t)
        x = self.major * sec_t
        y = self.minor * sin(t) * sec_t
        return self.center + self.xaxis * x + self.yaxis * y

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
        raise NotImplementedError

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
        raise NotImplementedError

    def frame_at(self, t):
        """
        Frame at the parameter.

        Parameters
        ----------
        t : float
            The line parameter.

        Returns
        -------
        :class:`compas_future.geometry.Frame`

        """
        point = self.point_at(t)
        xaxis = self.tangent_at(t)
        yaxis = self.zaxis.cross(xaxis)
        return Frame(point, xaxis, yaxis)
