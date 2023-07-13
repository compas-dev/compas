from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from math import sqrt, pi, cos, sin

from compas.geometry import Frame
from .curve import Curve
from .line import Line

PI2 = 2 * pi


class Ellipse(Curve):
    """An ellipse is a curve defined by a coordinate system and a major and minor axis.

    The centre of the ellipse is at the origin of the coordinate system.
    The major axis is parallel to the local x-axis.
    The minor axis is parallel to the local y-axis.
    The parameter domain of an ellipse is ``[0, 2*pi]``.
    Moving along the ellipse in the parameter direction corresponds to moving counter-clockwise around the origin of the local coordinate system.

    Parameters
    ----------
    major : float
        The major of the ellipse.
    minor : float
        The minor of the ellipse.
    frame : :class:`~compas.geometry.Frame`, optional
        The local coordinate system of the ellipse.
        The default value is ``None``, in which case the ellipse is constructed in the XY plane of the world coordinate system.

    Attributes
    ----------
    frame : :class:`~compas.geometry.Frame`
        The coordinate frame of the ellipse.
    transformation : :class:`Transformation`, read-only
        The transformation from the local coordinate system of the ellipse (:attr:`frame`) to the world coordinate system.
    major : float
        The major of the ellipse.
    minor : float
        The minor of the ellipse.
    center : :class:`~compas.geometry.Point`
        The center of the ellipse.
    plane : :class:`~compas.geometry.Plane`, read-only
        The plane of the ellipse.
    area : float, read-only
        The area of the ellipse.
    circumference : float, read-only
        The length of the circumference of the ellipse.
    semifocal : float, read-only
        The semi-focal distance of the ellipse.
        This is the distance from the center of the ellipse to the focus points.
    focal : float, read-only
        The distance between the two focus points.
    eccentricity : float, read-only
        The eccentricity of the ellipse.
        This is the ratio between the semifocal length to the length of the semi-major axis.
    focus1 : :class:`~compas.geometry.Point`, read-only
        The first focus point of the ellipse.
    focus2 : :class:`~compas.geometry.Point`, read-only
        The second focus point of the ellipse.
    directix1 : :class:`~compas.geometry.Line`, read-only
        The first directix of the ellipse.
        The directix is perpendicular to the major axis
        and passes through a point at a distance ``major **2 / semifocal`` along the positive xaxis from the center of the ellipse.
    directix2 : :class:`~compas.geometry.Line`, read-only
        The second directix of the ellipse.
        The directix is perpendicular to the major axis
        and passes through a point at a distance ``major **2 / semifocal`` along the negative xaxis from the center of the ellipse.
    is_closed : bool, read-only
        True.
    is_periodic : bool, read-only
        True.
    is_circle : bool, read-only
        True if the ellipse is a circle.

    See Also
    --------
    :class:`compas.geometry.Circle`, :class:`compas.geometry.Hyperbola`, :class:`compas.geometry.Parabola`

    Examples
    --------
    >>> from compas.geometry import Frame, Ellipse
    >>> ellipse = Ellipse(frame=Frame.worldXY(), major=2, minor=1)
    >>> ellipse = Ellipse(major=2, minor=1)

    """

    JSONSCHEMA = {
        "type": "object",
        "properties": {
            "major": {"type": "number", "minimum": 0},
            "minor": {"type": "number", "minimum": 0},
            "frame": Frame.JSONSCHEMA,
        },
        "required": ["frame", "major", "minor"],
    }

    def __init__(self, major=1.0, minor=1.0, frame=None, **kwargs):
        super(Ellipse, self).__init__(frame=frame, **kwargs)
        self._major = None
        self._minor = None
        self.major = major
        self.minor = minor

    def __repr__(self):
        return "Ellipse(major={0!r}, minor={1!r}, frame={2!r})".format(self.major, self.minor, self.frame)

    def __eq__(self, other):
        try:
            other_frame = other.frame
            other_major = other.major
            other_minor = other.minor
        except Exception:
            return False
        return self.major == other_major and self.minor == other_minor, self.frame == other_frame

    # ==========================================================================
    # Data
    # ==========================================================================

    @property
    def data(self):
        return {"frame": self.frame, "major": self.major, "minor": self.minor}

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
        if self._major is None:
            raise ValueError("Length of major axis is not set.")
        return self._major

    @major.setter
    def major(self, major):
        if major < 0:
            raise ValueError("Major axis length cannot be negative.")
        self._major = float(major)

    @property
    def minor(self):
        if self._minor is None:
            raise ValueError("Length of minor axis is not set.")
        return self._minor

    @minor.setter
    def minor(self, minor):
        if minor < 0:
            raise ValueError("Minor axis length cannot be negative.")
        self._minor = float(minor)

    @property
    def semifocal(self):
        return sqrt(self.major**2 - self.minor**2)

    @property
    def focal(self):
        return 2 * self.semifocal

    @property
    def eccentricity(self):
        return self.semifocal / self.major

    @property
    def focus1(self):
        return self.center + self.xaxis * +self.semifocal

    @property
    def focus2(self):
        return self.center + self.xaxis * -self.semifocal

    @property
    def vertex1(self):
        return self.center + self.xaxis * self.major

    @property
    def vertex2(self):
        return self.center + self.xaxis * -self.major

    @property
    def directix1(self):
        d1 = self.major**2 / self.semifocal
        p1 = self.center + self.xaxis * +d1
        return Line.from_point_and_vector(p1, self.yaxis)

    @property
    def directix2(self):
        d2 = self.major**2 / self.semifocal
        p2 = self.center + self.xaxis * -d2
        return Line.from_point_and_vector(p2, self.yaxis)

    @property
    def area(self):
        return pi * self.major * self.minor

    @property
    def circumference(self):
        raise NotImplementedError

    @property
    def is_circle(self):
        return self.major == self.minor

    @property
    def is_closed(self):
        return True

    @property
    def is_periodic(self):
        return True

    # ==========================================================================
    # Constructors
    # ==========================================================================

    @classmethod
    def from_point_and_major_and_minor(cls, point, major, minor):
        """Construct a ellipse from a point and major and minor axis lengths.

        Parameters
        ----------
        point : :class:`compas.geometry.Point`
            The center point of the ellipse.
        major : float
            The major axis length.
        minor : float
            The minor axis length.

        Returns
        -------
        :class:`Ellipse`
            The constructed ellipse.

        """
        frame = Frame(point, [1, 0, 0], [0, 1, 0])
        return cls(frame=frame, major=major, minor=minor)

    # ==========================================================================
    # Methods
    # ==========================================================================

    def point_at(self, t):
        """Compute the point at a specific parameter.

        Parameters
        ----------
        t : float
            The parameter value.

        Returns
        -------
        :class:`compas.geometry.Point`
            The point at the parameter.

        See Also
        --------
        :meth:`normal_at`, :meth:`tangent_at`

        Notes
        -----
        The location of the point is expressed with respect to the world coordinate system.

        """
        t = t * PI2
        x = self.major * cos(t)
        y = self.minor * sin(t)
        return self.center + self.xaxis * x + self.yaxis * y

    def tangent_at(self, t):
        """Compute the tangent at a specific parameter.

        Parameters
        ----------
        t : float
            The parameter value.

        Returns
        -------
        :class:`compas.geometry.Vector`
            The tangent vector at the parameter.

        See Also
        --------
        :meth:`point_at`, :meth:`normal_at`

        Notes
        -----
        The orientation of the vector is expressed with respect to the world coordinate system.

        """
        yaxis = self.normal_at(t)
        zaxis = self.zaxis
        return yaxis.cross(zaxis).unitized()

    def normal_at(self, t):
        """Compute the normal at a specific parameter.

        Parameters
        ----------
        t : float
            The parameter value.

        Returns
        -------
        :class:`compas.geometry.Vector`
            The normal vector at the parameter.

        See Also
        --------
        :meth:`point_at`, :meth:`tangent_at`

        Notes
        -----
        The orientation of the vector is expressed with respect to the world coordinate system.

        """
        point = self.point_at(t)
        f1 = self.focus1  # in WCS
        f2 = self.focus2  # in WCS
        normal = (f1 - point).unitized() + (f2 - point).unitized()
        return normal.unitized()
